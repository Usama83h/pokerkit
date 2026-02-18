import streamlit as st
import time
import threading
from pokerkit.poker_rfid_integration import RFIDCardRegistry
from pokerkit.games import NoLimitTexasHoldem, Automation
import random

st.set_page_config(page_title="PokerKit Table", layout="wide", page_icon="🃏")

def tts_broadcast_action(action, player=None, amount=None):
    pass

try:
    from mfrc522 import SimpleMFRC522
    HAVE_RFID = True
except ImportError:
    HAVE_RFID = False
    SimpleMFRC522 = None

PLAYER_COUNT = 4
STARTING_STACKS = [1000] * PLAYER_COUNT
STARTING_BLINDS = (10, 20)
PLAYER_NAMES = ["Alice", "Bob", "Carol", "David"]

AUTOMATIONS = (
    Automation.ANTE_POSTING,
    Automation.BET_COLLECTION,
    Automation.BLIND_OR_STRADDLE_POSTING,
    Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
    Automation.HAND_KILLING,
    Automation.CHIPS_PUSHING,
    Automation.CHIPS_PULLING,
)

def make_state():
    return NoLimitTexasHoldem.create_state(
        AUTOMATIONS, True, 0, STARTING_BLINDS, 20,
        tuple(STARTING_STACKS), PLAYER_COUNT,
    )

if 'state' not in st.session_state:
    st.session_state['state'] = make_state()
    st.session_state['rfid_registry'] = RFIDCardRegistry()
    st.session_state['rfid_last_card'] = None
    st.session_state['rfid_last_uid'] = None
    st.session_state['rfid_thread_started'] = False
    st.session_state['log'] = []
    st.session_state['done'] = False

def start_new_hand():
    st.session_state['state'] = make_state()
    st.session_state['log'].append("New hand started.")
    st.session_state['rfid_last_card'] = None
    st.session_state['rfid_last_uid'] = None
    st.session_state['done'] = False

if HAVE_RFID and not st.session_state['rfid_thread_started']:
    def rfid_poll_loop():
        reader = SimpleMFRC522()
        reg = st.session_state['rfid_registry']
        last_uid = None
        while True:
            uid, _ = reader.read()
            if uid and uid != last_uid:
                poker_code = reg.get_poker_code(uid)
                st.session_state['rfid_last_uid'] = str(uid)
                st.session_state['rfid_last_card'] = poker_code or None
                label = poker_code if poker_code else "NOT REGISTERED"
                st.session_state['log'].append(f"RFID scan: UID={uid} -> {label}")
                last_uid = uid
            time.sleep(0.5)
    t = threading.Thread(target=rfid_poll_loop, daemon=True)
    t.start()
    st.session_state['rfid_thread_started'] = True

def process_deal(poker_code):
    s = st.session_state['state']
    if s.can_deal_hole():
        s.deal_hole(poker_code)
        st.session_state['log'].append(f"Dealt {poker_code} to a player")
    elif s.can_burn_card():
        s.burn_card(poker_code)
        st.session_state['log'].append("Burned a card")
    elif s.can_deal_board():
        s.deal_board(poker_code)
        st.session_state['log'].append(f"Dealt {poker_code} to board")
    else:
        st.session_state['log'].append("Cannot deal a card right now.")

def handle_player_action(action, amount=None):
    s = st.session_state['state']
    actor = s.actor_index
    pname = PLAYER_NAMES[actor] if actor is not None else "?"
    try:
        if action == 'fold':
            s.fold()
            msg = f"{pname} folds."
        elif action == 'call':
            s.check_or_call()
            msg = f"{pname} calls."
        elif action == 'raise':
            s.complete_bet_or_raise_to(amount)
            msg = f"{pname} raises to {amount}."
        elif action == 'check':
            s.check_or_call()
            msg = f"{pname} checks."
        else:
            msg = "Invalid action."
        st.session_state['log'].append(msg)
    except Exception as e:
        st.session_state['log'].append(f"Action error: {e}")

def render_card(card_str):
    suit_map = {'s': ('♠', '#222'), 'h': ('♥', '#cc0000'), 'd': ('♦', '#cc0000'), 'c': ('♣', '#222')}
    if not card_str:
        return "🂠"
    rank = card_str[0]
    suit = card_str[1] if len(card_str) > 1 else '?'
    sym, color = suit_map.get(suit, ('?', '#222'))
    return f'<span style="background:white;color:{color};border:1px solid #bbb;border-radius:4px;padding:2px 5px;margin:1px;font-weight:bold;font-size:15px;display:inline-block">{rank}{sym}</span>'

def render_player(idx, s):
    name = PLAYER_NAMES[idx]
    stack = s.stacks[idx]
    active = s.statuses[idx]
    is_actor = s.actor_index == idx and bool(s.status)
    hole = s.hole_cards[idx]

    cards_html = ""
    if hole:
        for c in hole:
            cards_html += render_card(repr(c))
    else:
        cards_html = '<span style="color:#aaa;font-size:13px">No cards</span>'

    border = "3px solid #FFD700" if is_actor else ("2px solid #555" if active else "2px solid #333")
    bg = "rgba(60,40,0,0.92)" if is_actor else ("rgba(20,40,20,0.85)" if active else "rgba(30,30,30,0.6)")
    opacity = "1" if active else "0.5"
    glow = "box-shadow: 0 0 18px 4px #FFD700;" if is_actor else ""
    name_color = "#FFD700" if is_actor else ("#fff" if active else "#aaa")
    acting_badge = '<br/><span style="background:#FFD700;color:#000;border-radius:4px;padding:1px 7px;font-size:11px;font-weight:bold">&#9658; ACTING</span>' if is_actor else ""
    crown = '&#128081; ' if is_actor else ''

    return (
        f'<div style="border:{border};background:{bg};border-radius:12px;padding:10px 14px;'
        f'text-align:center;opacity:{opacity};{glow}min-width:120px;display:inline-block">'
        f'<div style="color:{name_color};font-weight:bold;font-size:15px">{crown}{name}</div>'
        f'<div style="color:#7CFC00;font-size:13px;margin:2px 0">&#128176; ${stack}</div>'
        f'<div style="margin:4px 0">{cards_html}</div>'
        f'{acting_badge}'
        f'</div>'
    )

# ── Global CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0d1b0e; }
    .block-container { padding-top: 1rem; }
    h1, h2, h3 { color: #FFD700 !important; }
    .stButton > button {
        background: #1a4a1a;
        color: white;
        border: 1px solid #3a8a3a;
        border-radius: 8px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background: #2d8a2d;
        border-color: #FFD700;
        color: #FFD700;
    }
</style>
""", unsafe_allow_html=True)

# ── State ─────────────────────────────────────────────────────────────
s = st.session_state['state']

# ── Title ─────────────────────────────────────────────────────────────
st.markdown("<h1 style='text-align:center'>🃏 PokerKit Table</h1>", unsafe_allow_html=True)

# ── Table ─────────────────────────────────────────────────────────────
# Top player (Alice - idx 0)
_, top_col, _ = st.columns([1, 2, 1])
with top_col:
    st.markdown(f"<div style='text-align:center'>{render_player(0, s)}</div>", unsafe_allow_html=True)

# Middle row: left player, table, right player
left_col, table_col, right_col = st.columns([1, 3, 1])

with left_col:
    st.markdown(f"<div style='text-align:center;margin-top:60px'>{render_player(3, s)}</div>", unsafe_allow_html=True)

with table_col:
    # Board cards
    board_html = ""
    flat_board = [c for group in s.board_cards for c in group]
    if flat_board:
        for c in flat_board:
            board_html += render_card(repr(c))
    else:
        board_html = '<span style="color:rgba(255,255,255,0.3);font-size:13px">No board cards yet</span>'

    pot = s.total_pot_amount

    table_inner = f"""
    <div style="
        background: radial-gradient(ellipse at center, #2d8a4e 0%, #1a5c30 65%, #0d3d1f 100%);
        border-radius: 120px;
        border: 10px solid #5c3d1e;
        box-shadow: 0 0 40px rgba(0,0,0,0.9), inset 0 0 40px rgba(0,0,0,0.4);
        padding: 40px 30px;
        text-align: center;
        min-height: 180px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 12px;
    ">
        <div style="color:rgba(255,255,255,0.12);font-size:22px;font-weight:bold;letter-spacing:6px">POKERKIT</div>
        <div style="background:rgba(0,0,0,0.5);color:#FFD700;border-radius:20px;padding:5px 18px;font-size:15px;font-weight:bold">
            💵 Pot: ${pot}
        </div>
        <div style="display:flex;gap:6px;justify-content:center;flex-wrap:wrap">
            {board_html}
        </div>
    </div>
    """
    st.markdown(table_inner, unsafe_allow_html=True)

with right_col:
    st.markdown(f"<div style='text-align:center;margin-top:60px'>{render_player(1, s)}</div>", unsafe_allow_html=True)

# Bottom player (Carol - idx 2)
_, bot_col, _ = st.columns([1, 2, 1])
with bot_col:
    st.markdown(f"<div style='text-align:center'>{render_player(2, s)}</div>", unsafe_allow_html=True)

st.write("")

# ── Controls ──────────────────────────────────────────────────────────
st.markdown("---")
col_deal, col_action = st.columns([1, 2])

with col_deal:
    st.markdown("### 🃏 Deal Cards")
    if not HAVE_RFID:
        if st.button("🎴 Deal Random Card", use_container_width=True):
            available = list(s.deck_cards)
            if available:
                demo_card = random.choice(available)
                card_str = repr(demo_card)
                try:
                    if s.can_deal_hole():
                        s.deal_hole(card_str)
                        st.session_state['log'].append(f"Dealt {card_str} to a player")
                    elif s.can_burn_card():
                        s.burn_card(card_str)
                        st.session_state['log'].append("Burned a card")
                    elif s.can_deal_board():
                        s.deal_board(card_str)
                        st.session_state['log'].append(f"Dealt {card_str} to board")
                    else:
                        st.error("Cannot deal right now — complete player actions first.")
                except Exception as e:
                    st.error(f"Error: {e}")
                st.rerun()
            else:
                st.error("No cards left in deck.")
    else:
        uid = st.session_state.get('rfid_last_uid')
        card = st.session_state.get('rfid_last_card')
        if uid and card:
            st.success(f"Card detected: **{card}**")
            if st.button("Deal RFID Card", use_container_width=True):
                process_deal(card)
                st.session_state['rfid_last_card'] = None
                st.session_state['rfid_last_uid'] = None
                st.rerun()
        else:
            st.info("Scan a card on the RFID reader...")

with col_action:
    st.markdown("### 🎮 Player Actions")
    if s.status:
        actor = s.actor_index
        actor_name = PLAYER_NAMES[actor] if actor is not None else "?"
        stack_val = s.stacks[actor] if actor is not None else 0
        st.markdown(f"**{actor_name}'s turn** — Stack: 💰 ${stack_val}")

        actions_list = []
        if s.can_fold():
            actions_list.append(('🚫 Fold', 'fold'))
        if s.can_check_or_call():
            if s.checking_or_calling_amount == 0:
                actions_list.append(('✅ Check', 'check'))
            else:
                actions_list.append((f'📞 Call ${s.checking_or_calling_amount}', 'call'))
        if s.can_complete_bet_or_raise_to():
            actions_list.append(('📈 Raise', 'raise'))

        # Raise slider (show before buttons if raise is available)
        raise_amount = None
        if s.can_complete_bet_or_raise_to():
            min_raise = s.min_completion_betting_or_raising_to_amount
            max_raise = s.max_completion_betting_or_raising_to_amount
            if min_raise is not None and max_raise is not None and min_raise <= max_raise:
                st.markdown(f"**Raise amount** (min: ${min_raise} — max/all-in: ${max_raise})")
                raise_amount = st.slider(
                    "Raise to:", min_value=int(min_raise), max_value=int(max_raise),
                    value=int(min_raise), step=10, key="raise_slider"
                )
                c1, c2 = st.columns(2)
                with c1:
                    if st.button(f"📈 Raise to ${raise_amount}", use_container_width=True, key="action_raise"):
                        handle_player_action('raise', amount=raise_amount)
                        st.rerun()
                with c2:
                    if st.button(f"💥 All-In (${max_raise})", use_container_width=True, key="action_allin"):
                        handle_player_action('raise', amount=int(max_raise))
                        st.rerun()

        # Other action buttons (fold / check / call)
        other_actions = [(l, a) for l, a in actions_list if a != 'raise']
        if other_actions:
            btn_cols = st.columns(len(other_actions))
            for i, (label, action) in enumerate(other_actions):
                with btn_cols[i]:
                    if st.button(label, key=f"action_{action}", use_container_width=True):
                        handle_player_action(action)
                        st.rerun()

        if not actions_list:
            st.info("Deal all hole cards first.")
    else:
        st.info("Hand not in progress.")

# ── Hand result ───────────────────────────────────────────────────────
# Check if game is over (only one player has chips)
players_with_chips = [i for i in range(PLAYER_COUNT) if s.stacks[i] > 0]
game_over = len(players_with_chips) == 1

if not s.status and not st.session_state['done']:
    try:
        payoffs = list(s.payoffs)
        if any(p > 0 for p in payoffs):
            best = max(payoffs)
            winners = [PLAYER_NAMES[i] for i, p in enumerate(payoffs) if p == best]
            st.success(f"🏆 {' and '.join(winners)} win(s) this hand!")
            st.session_state['log'].append(f"Winner(s): {', '.join(winners)}")
        else:
            st.success("Hand finished. Chips distributed.")
    except Exception:
        st.success("Hand finished.")
    st.session_state['done'] = True
    st.rerun()

if st.session_state['done']:
    if game_over:
        champion = PLAYER_NAMES[players_with_chips[0]]
        st.markdown(f"""
        <div style="text-align:center;background:linear-gradient(135deg,#1a1a00,#3a3a00);
                    border:3px solid #FFD700;border-radius:16px;padding:30px;margin:20px 0">
            <div style="font-size:48px">🏆</div>
            <div style="color:#FFD700;font-size:32px;font-weight:bold">GAME OVER</div>
            <div style="color:white;font-size:20px;margin-top:10px">{champion} wins the entire game!</div>
            <div style="color:#aaa;font-size:14px;margin-top:6px">All chips collected</div>
        </div>
        """, unsafe_allow_html=True)
        st.session_state['log'].append(f"🏆 GAME OVER — {champion} wins!")
        if st.button("🔄 New Game (Reset All Chips)", use_container_width=False):
            st.session_state['state'] = make_state()
            st.session_state['log'] = ["New game started."]
            st.session_state['done'] = False
            st.rerun()
    else:
        if st.button("🔄 Start New Hand"):
            start_new_hand()
            st.rerun()

# ── Hand Log ──────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📋 Hand Log")
log_lines = st.session_state['log'][-20:][::-1]
if log_lines:
    rows = "".join(
        f'<div style="font-family:monospace;font-size:13px;padding:3px 10px;'
        f'border-left:3px solid #2d8a4e;margin:2px 0;color:#ccc">{line}</div>'
        for line in log_lines
    )
    st.markdown(
        f'<div style="background:#0a1a0a;border-radius:8px;padding:10px;'
        f'max-height:220px;overflow-y:auto;border:1px solid #1a4a1a">{rows}</div>',
        unsafe_allow_html=True
    )
else:
    st.caption("No actions yet — deal cards to begin!")

st.caption("PokerKit × RFID × Streamlit | Demo Mode")
