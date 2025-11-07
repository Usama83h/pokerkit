import streamlit as st
import json
import time
import threading
from pokerkit.poker_rfid_integration import RFIDCardRegistry
from pokerkit.games import NoLimitTexasHoldem, Automation
import random
try:
    import pyttsx3
    tts_engine = pyttsx3.init()
    def tts_broadcast_action(action, player=None, amount=None):
        text = f"{player} {action.replace('_',' ')}" if player else action
        if amount is not None:
            text += f" {amount}"
        st.write(f"[SPEAK] {text}")
        tts_engine.say(text)
        tts_engine.runAndWait()
except ImportError:
    def tts_broadcast_action(action, player=None, amount=None):
        pass
try:
    from mfrc522 import SimpleMFRC522
    HAVE_RFID = True
except ImportError:
    HAVE_RFID = False
    SimpleMFRC522 = None

CARDS_JSON = 'cards.json'
PLAYER_NAMES = ["Alice","Bob","Carol","David"]
PLAYER_COUNT = 4
STARTING_STACKS = [1000] * PLAYER_COUNT
STARTING_BLINDS = (10, 20)  # SB, BB

if 'game_state' not in st.session_state:
    st.session_state['rfid_registry'] = RFIDCardRegistry()
    st.session_state['game'] = NoLimitTexasHoldem(
        (
            Automation.ANTE_POSTING,
            Automation.BET_COLLECTION,
            Automation.BLIND_OR_STRADDLE_POSTING,
            Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
            Automation.HAND_KILLING,
            Automation.CHIPS_PUSHING,
            Automation.CHIPS_PULLING,
        ),
        True,      # Uniform antes
        0,         # Antes
        STARTING_BLINDS, # Blinds
        20,        # Min-bet
        tuple(STARTING_STACKS),
        PLAYER_COUNT,
    )
    st.session_state['state'] = st.session_state['game'](sum(STARTING_STACKS), PLAYER_COUNT)
    st.session_state['rfid_last_card'] = None
    st.session_state['rfid_last_uid']  = None
    st.session_state['rfid_thread_started'] = False
    st.session_state['log'] = []
    st.session_state['winners'] = []
    st.session_state['awaiting_deal'] = False
    st.session_state['awaiting_action'] = False
    st.session_state['done'] = False

def start_new_hand():
    st.session_state['state'] = st.session_state['game'](sum(STARTING_STACKS), PLAYER_COUNT)
    st.session_state['log'].append(f"New hand started.")
    st.session_state['rfid_last_card'] = None
    st.session_state['rfid_last_uid'] = None
    st.session_state['winners'] = []
    st.session_state['done'] = False

# RFID polling
if HAVE_RFID and not st.session_state['rfid_thread_started']:
    def rfid_poll_loop():
        reader = SimpleMFRC522()
        reg = st.session_state['rfid_registry']
        last_uid = None
        while True:
            id, _ = reader.read()
            if id and id != last_uid:
                poker_code = reg.get_poker_code(id)
                st.session_state['rfid_last_uid'] = str(id)
                st.session_state['rfid_last_card'] = poker_code if poker_code else None
                if poker_code:
                    st.session_state['log'].append(f"RFID scan: UID={id} -> {poker_code}")
                else:
                    st.session_state['log'].append(f"RFID scan: UID={id} NOT REGISTERED")
                last_uid = id
            time.sleep(0.5)

    t = threading.Thread(target=rfid_poll_loop, daemon=True)
    t.start()
    st.session_state['rfid_thread_started'] = True

def process_deal(poker_code):
    s = st.session_state['state']
    if s.can_deal_hole():
        s.deal_hole(poker_code)
        st.session_state['log'].append(f"Dealt {poker_code} to player {s.actor_index+1}")
        tts_broadcast_action('deal', f"Player {s.actor_index+1}", poker_code)
    elif s.can_deal_board():
        s.deal_board(poker_code)
        st.session_state['log'].append(f"Dealt {poker_code} to board.")
        tts_broadcast_action('deal', "board", poker_code)
    else:
        st.session_state['log'].append("Cannot deal a card now.")

def handle_player_action(action, amount=None):
    s = st.session_state['state']
    pname = f"Player {s.actor_index+1}"
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

# UI rendering
st.title('PokerKit Table (RFID + Real PokerKit Logic)')
s = st.session_state['state']

# Players
cols = st.columns([2]*PLAYER_COUNT)
for idx in range(PLAYER_COUNT):
    with cols[idx]:
        st.markdown(f"**Player {idx+1}**")
        st.markdown(f"Stack: {s.stacks[idx]}")
        st.markdown(f"Hole: {''.join(map(str, s.hole_cards[idx])) if s.hole_cards[idx] else '-'}")
        status = "Active" if s.statuses[idx] else "Out"
        st.markdown(f"Status: {status}")
        if idx == s.actor_index and s.status:
            st.markdown(f"_Acting now_ :point_left:")

# Board/Pot
st.write(f"### Board: {' '.join(map(str, s.board_cards)) if s.board_cards else '-'}")
st.write(f"**Pot:** {s.pot_amounts[0] if hasattr(s, 'pot_amounts') and s.pot_amounts else 0}")

# RFID Panel
st.write("---")
with st.container():
    st.write("## RFID Card Scanning")
    if HAVE_RFID:
        if st.session_state.get('rfid_last_uid'):
            if st.session_state.get('rfid_last_card'):
                st.success(f"Detected: UID={st.session_state['rfid_last_uid']} → {st.session_state['rfid_last_card']}")
                if st.button('Deal scanned card (RFID)'):
                    process_deal(st.session_state['rfid_last_card'])
                    st.session_state['rfid_last_card'] = None
                    st.session_state['rfid_last_uid'] = None
            else:
                st.warning(f"UID={st.session_state['rfid_last_uid']} not registered. Register it using CLI tool or card registry UI.")
        else:
            st.info("No card scanned yet.")
    else:
        st.info("RFID hardware not found. Using demo mode.")
        if st.button('Simulate card scan (give random card)'):
            demo_card = random.choice([c for c in s.deck if c not in s.board_cards and all(c not in h for h in s.hole_cards)])
            process_deal(str(demo_card))

# Player actions (only legal moves are enabled)
actions_list = []
if s.status:
    if s.can_fold():
        actions_list.append(('Fold', 'fold'))
    if s.can_check_or_call():
        if s.checking_or_calling_amount == 0:
            actions_list.append(('Check', 'check'))
        else:
            actions_list.append(('Call', 'call'))
    if s.can_complete_bet_or_raise_to():
        actions_list.append(('Raise', 'raise'))
    st.subheader(f"Actions for Player {s.actor_index+1}")
    act_cols = st.columns(len(actions_list))
    for idx, (label, action) in enumerate(actions_list):
        with act_cols[idx]:
            if st.button(label):
                if action == 'raise':
                    # For UI simplicity, hardcode raise amount, ideally prompt user
                    handle_player_action(action, amount=max(s.bets)+100)
                else:
                    handle_player_action(action)

# Show hand winner/ending
if not s.status and not st.session_state['done']:
    payoffs = getattr(s, 'payoffs', None)
    if payoffs:
        winning = max(payoffs)
        winners = [f"Player {ix+1}" for ix, p in enumerate(payoffs) if p == winning]
        st.success(f"{' and '.join(winners)} win(s) this hand!")
        tts_broadcast_action('win', ', '.join(winners), winning)
        st.session_state['log'].append(f"Winner(s): {', '.join(winners)} get(s) {winning}")
    else:
        st.success("Hand finished. Chips distributed.")
    st.session_state['done'] = True
    if st.button("Start New Hand"):
        start_new_hand()

# Action log
st.write('---')
st.write('#### Hand Log')
for line in st.session_state['log'][-15:][::-1]:
    st.code(line, language=None)

# FAQ
with st.expander("Help/Frequently Asked Questions"):
    st.write("- Scan a card on the reader or simulate for demo mode. Only able to deal valid cards at the proper stage by rules.")
    st.write("- Player controls are only enabled when it is legal to act for that player, by real poker rules.")
    st.write("- To register cards, use the CLI card registry tool or future admin UI update.")
    st.write("- If TTS announcements are not heard, ensure pyttsx3 installs and your system supports it.")
    st.write("- Need remote/multi-tablet support? See project docs for WAN extensions.")

st.caption("PokerKit x RFID x Streamlit: Full Poker Logic, Real Hardware, Action Announce, Live Audit Log")
