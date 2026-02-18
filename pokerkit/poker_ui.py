import streamlit as st
import time
import threading
from pokerkit.poker_rfid_integration import RFIDCardRegistry
from pokerkit.games import NoLimitTexasHoldem, Automation
import random

def tts_broadcast_action(action, player=None, amount=None):
    pass  # TTS disabled in web mode

try:
    from mfrc522 import SimpleMFRC522
    HAVE_RFID = True
except ImportError:
    HAVE_RFID = False
    SimpleMFRC522 = None

PLAYER_COUNT = 4
STARTING_STACKS = [1000] * PLAYER_COUNT
STARTING_BLINDS = (10, 20)

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
        AUTOMATIONS,
        True,
        0,
        STARTING_BLINDS,
        20,
        tuple(STARTING_STACKS),
        PLAYER_COUNT,
    )

# Initialize session state once
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

# RFID polling thread
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
        tts_broadcast_action('deal', 'player', poker_code)
    elif s.can_deal_board():
        s.deal_board(poker_code)
        st.session_state['log'].append(f"Dealt {poker_code} to board")
        tts_broadcast_action('deal', 'board', poker_code)
    else:
        st.session_state['log'].append("Cannot deal a card right now.")

def handle_player_action(action, amount=None):
    s = st.session_state['state']
    actor = s.actor_index
    pname = f"Player {actor + 1}" if actor is not None else "Player ?"
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
        tts_broadcast_action(action, pname, amount)
    except Exception as e:
        st.session_state['log'].append(f"Action error: {e}")

# ── UI ──────────────────────────────────────────────────────────────
st.title('PokerKit Table (RFID + Real PokerKit Logic)')
s = st.session_state['state']

# Player panels
cols = st.columns(PLAYER_COUNT)
for idx in range(PLAYER_COUNT):
    with cols[idx]:
        st.markdown(f"**Player {idx + 1}**")
        st.markdown(f"Stack: {s.stacks[idx]}")
        hole = s.hole_cards[idx]
        hole_str = ' '.join(repr(c) for c in hole) if hole else '-'
        st.markdown(f"Hole: {hole_str}")
        status = "Active" if s.statuses[idx] else "Out"
        st.markdown(f"Status: {status}")
        if s.actor_index is not None and idx == s.actor_index and s.status:
            st.markdown("_Acting now_ 👈")

# Board / Pot
board_str = ' '.join(repr(c) for c in s.board_cards) if s.board_cards else '-'
st.write(f"### Board: {board_str}")
st.write(f"**Pot:** {s.total_pot_amount}")

# RFID panel
st.write("---")
st.write("## RFID Card Scanning")
if HAVE_RFID:
    uid = st.session_state.get('rfid_last_uid')
    card = st.session_state.get('rfid_last_card')
    if uid:
        if card:
            st.success(f"Detected: UID={uid} → {card}")
            if st.button('Deal scanned card (RFID)'):
                process_deal(card)
                st.session_state['rfid_last_card'] = None
                st.session_state['rfid_last_uid'] = None
        else:
            st.warning(f"UID={uid} not registered.")
    else:
        st.info("No card scanned yet.")
else:
    st.info("RFID hardware not found. Using demo mode.")
    if st.button('Simulate card scan (give random card)'):
        available = list(s.deck_cards)
        if available:
            demo_card = random.choice(available)
            card_str = repr(demo_card)
            try:
                if s.can_deal_hole():
                    s.deal_hole(card_str)
                    st.session_state['log'].append(f"Dealt {card_str} to a player")
                elif s.can_deal_board():
                    s.deal_board(card_str)
                    st.session_state['log'].append(f"Dealt {card_str} to board")
                else:
                    st.error("Cannot deal right now — game may be waiting for player action.")
            except Exception as e:
                st.error(f"Error dealing card: {e}")
            st.rerun()
        else:
            st.error("No cards left in deck.")

# Player actions
st.write("---")
if s.status:
    actor = s.actor_index
    actor_label = f"Player {actor + 1}" if actor is not None else "?"
    st.subheader(f"Actions for {actor_label}")
    actions_list = []
    if s.can_fold():
        actions_list.append(('Fold', 'fold'))
    if s.can_check_or_call():
        if s.checking_or_calling_amount == 0:
            actions_list.append(('Check', 'check'))
        else:
            actions_list.append(('Call', 'call'))
    if s.can_complete_bet_or_raise_to():
        actions_list.append(('Raise', 'raise'))

    if actions_list:
        act_cols = st.columns(len(actions_list))
        for idx, (label, action) in enumerate(actions_list):
            with act_cols[idx]:
                if st.button(label, key=f"action_{action}"):
                    if action == 'raise':
                        bets = [b for b in s.bets if b is not None and b > 0]
                        raise_amount = (max(bets) if bets else 0) + 100
                        handle_player_action(action, amount=raise_amount)
                    else:
                        handle_player_action(action)
                    st.rerun()
    else:
        st.info("No actions available — deal cards first.")

# Hand result
if not s.status and not st.session_state['done']:
    try:
        payoffs = list(s.payoffs)
        if any(p > 0 for p in payoffs):
            best = max(payoffs)
            winners = [f"Player {i + 1}" for i, p in enumerate(payoffs) if p == best]
            st.success(f"{' and '.join(winners)} win(s) this hand!")
            st.session_state['log'].append(f"Winner(s): {', '.join(winners)}")
        else:
            st.success("Hand finished. Chips distributed.")
    except Exception:
        st.success("Hand finished.")
    st.session_state['done'] = True
    if st.button("Start New Hand"):
        start_new_hand()
        st.rerun()

# Action log
st.write('---')
st.write('#### Hand Log')
for line in st.session_state['log'][-15:][::-1]:
    st.code(line, language=None)

st.caption("PokerKit x RFID x Streamlit | Demo Mode")
