#!/usr/bin/env python3
"""
PokerKit Standalone Demo
This script demonstrates PokerKit capabilities without requiring installation
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=" * 70)
    print(" " * 20 + "POKERKIT DEMO")
    print("=" * 70)
    
    try:
        # Try to import pokerkit
        from pokerkit import NoLimitTexasHoldem, Automation, StandardHighHand
        from math import inf
        
        print("\n✓ PokerKit imported successfully!")
        print("\n" + "=" * 70)
        print("DEMO 1: Famous Hand - Tom Dwan vs Phil Ivey")
        print("The First Televised Million Dollar Pot")
        print("=" * 70)
        
        # Create game state
        state = NoLimitTexasHoldem.create_state(
            (
                Automation.ANTE_POSTING,
                Automation.BET_COLLECTION,
                Automation.BLIND_OR_STRADDLE_POSTING,
                Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
                Automation.HAND_KILLING,
                Automation.CHIPS_PUSHING,
                Automation.CHIPS_PULLING,
            ),
            True,  # Uniform antes
            500,  # Antes
            (1000, 2000),  # Blinds
            2000,  # Min-bet
            (1125600, inf, 553500),  # Starting stacks
            3,  # Number of players
        )
        
        print("\nStarting Stacks:")
        print(f"  Player 1 (Phil Ivey):       ${state.stacks[0]:,}")
        print(f"  Player 2 (Patrik Antonius): ${state.stacks[1]} (infinite)")
        print(f"  Player 3 (Tom Dwan):        ${state.stacks[2]:,}")
        
        # Pre-flop
        print("\n" + "-" * 70)
        print("PRE-FLOP")
        print("-" * 70)
        state.deal_hole('Ac2d')  # Ivey
        state.deal_hole('????')  # Antonius
        state.deal_hole('7h6h')  # Dwan
        
        print("Hole cards dealt:")
        print("  Ivey: A♣ 2♦")
        print("  Antonius: [hidden]")
        print("  Dwan: 7♥ 6♥")
        
        state.complete_bet_or_raise_to(7000)
        print("\n→ Dwan raises to $7,000")
        
        state.complete_bet_or_raise_to(23000)
        print("→ Ivey re-raises to $23,000")
        
        state.fold()
        print("→ Antonius folds")
        
        state.check_or_call()
        print("→ Dwan calls")
        
        # Flop
        print("\n" + "-" * 70)
        print("FLOP")
        print("-" * 70)
        state.burn_card('??')
        state.deal_board('Jc3d5c')
        print("Board: J♣ 3♦ 5♣")
        
        state.complete_bet_or_raise_to(35000)
        print("\n→ Ivey bets $35,000")
        
        state.check_or_call()
        print("→ Dwan calls")
        
        # Turn
        print("\n" + "-" * 70)
        print("TURN")
        print("-" * 70)
        state.burn_card('??')
        state.deal_board('4h')
        print("Board: J♣ 3♦ 5♣ 4♥")
        
        state.complete_bet_or_raise_to(90000)
        print("\n→ Ivey bets $90,000")
        
        state.complete_bet_or_raise_to(232600)
        print("→ Dwan raises to $232,600")
        
        state.complete_bet_or_raise_to(1067100)
        print("→ Ivey raises to $1,067,100 (ALL-IN!)")
        
        state.check_or_call()
        print("→ Dwan calls (ALL-IN!)")
        
        # River
        print("\n" + "-" * 70)
        print("RIVER")
        print("-" * 70)
        state.burn_card('??')
        state.deal_board('Jh')
        print("Board: J♣ 3♦ 5♣ 4♥ J♥")
        
        # Final results
        print("\n" + "=" * 70)
        print("FINAL RESULTS")
        print("=" * 70)
        print(f"  Phil Ivey:       ${state.stacks[0]:,}")
        print(f"  Patrik Antonius: ${state.stacks[1]}")
        print(f"  Tom Dwan:        ${state.stacks[2]:,}")
        
        print("\n🏆 WINNER: Tom Dwan")
        print("   Hand: Straight (7-6-5-4-3)")
        print("   Ivey had: Wheel (5-4-3-2-A)")
        print("   The river paired the board, giving Dwan the pot!")
        
        # Demo 2: Hand Evaluation
        print("\n" + "=" * 70)
        print("DEMO 2: Hand Evaluation")
        print("=" * 70)
        
        hand1 = StandardHighHand('AhKhQhJhTh')
        hand2 = StandardHighHand('9s9h9d9c8s')
        hand3 = StandardHighHand('AsKdQcJhTs')
        
        print(f"\nHand 1: {hand1}")
        print(f"Hand 2: {hand2}")
        print(f"Hand 3: {hand3}")
        
        print(f"\nHand 1 > Hand 2: {hand1 > hand2}")
        print(f"Hand 2 > Hand 3: {hand2 > hand3}")
        print(f"Hand 1 > Hand 3: {hand1 > hand3}")
        
        print("\n" + "=" * 70)
        print("✓ Demo completed successfully!")
        print("=" * 70)
        
    except ImportError as e:
        print(f"\n✗ Error: PokerKit is not installed")
        print(f"  Details: {e}")
        print("\nTo install PokerKit, run:")
        print("  pip install pokerkit")
        return 1
    
    except Exception as e:
        print(f"\n✗ Error running demo: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    print("\nPress Enter to exit...")
    input()
    sys.exit(exit_code)
