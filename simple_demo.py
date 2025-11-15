#!/usr/bin/env python3
"""PokerKit Simple Demo"""

try:
    from pokerkit import NoLimitTexasHoldem, Automation
    
    # Create a simple 2-player game
    state = NoLimitTexasHoldem.create_state(
        (Automation.ANTE_POSTING, Automation.BET_COLLECTION, 
         Automation.BLIND_OR_STRADDLE_POSTING),
        True, 0, (10, 20), 20, (1000, 1000), 2
    )
    
    print("PokerKit is working!")
    print(f"Players: {state.player_count}")
    print(f"Stacks: {state.stacks}")
    
except ImportError as e:
    print(f"Error importing PokerKit: {e}")
    print("Please install: pip install pokerkit")
