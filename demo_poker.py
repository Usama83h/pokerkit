"""Simple PokerKit Demo - Texas Hold'em Hand"""

from math import inf
from pokerkit import Automation, NoLimitTexasHoldem

print("=" * 60)
print("PokerKit Demo - Tom Dwan vs Phil Ivey")
print("First televised million-dollar pot")
print("=" * 60)

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
print(f"  Phil Ivey:       ${state.stacks[0]:,}")
print(f"  Patrik Antonius: ${state.stacks[1]:,} (inf)")
print(f"  Tom Dwan:        ${state.stacks[2]:,}")

# Pre-flop
print("\n--- PRE-FLOP ---")
state.deal_hole('Ac2d')  # Ivey
state.deal_hole('????')  # Antonius
state.deal_hole('7h6h')  # Dwan

print("Hole cards dealt:")
print("  Ivey: Ac2d")
print("  Antonius: ????")
print("  Dwan: 7h6h")

state.complete_bet_or_raise_to(7000)  # Dwan
print("\nDwan raises to $7,000")

state.complete_bet_or_raise_to(23000)  # Ivey
print("Ivey re-raises to $23,000")

state.fold()  # Antonius
print("Antonius folds")

state.check_or_call()  # Dwan
print("Dwan calls")

# Flop
print("\n--- FLOP ---")
state.burn_card('??')
state.deal_board('Jc3d5c')
print("Board: Jc 3d 5c")

state.complete_bet_or_raise_to(35000)  # Ivey
print("\nIvey bets $35,000")

state.check_or_call()  # Dwan
print("Dwan calls")

# Turn
print("\n--- TURN ---")
state.burn_card('??')
state.deal_board('4h')
print("Board: Jc 3d 5c 4h")

state.complete_bet_or_raise_to(90000)  # Ivey
print("\nIvey bets $90,000")

state.complete_bet_or_raise_to(232600)  # Dwan
print("Dwan raises to $232,600")

state.complete_bet_or_raise_to(1067100)  # Ivey
print("Ivey raises to $1,067,100 (ALL-IN!)")

state.check_or_call()  # Dwan
print("Dwan calls (ALL-IN!)")

# River
print("\n--- RIVER ---")
state.burn_card('??')
state.deal_board('Jh')
print("Board: Jc 3d 5c 4h Jh")

# Final results
print("\n" + "=" * 60)
print("FINAL STACKS:")
print("=" * 60)
print(f"  Phil Ivey:       ${state.stacks[0]:,}")
print(f"  Patrik Antonius: ${state.stacks[1]:,} (inf)")
print(f"  Tom Dwan:        ${state.stacks[2]:,}")

print("\n" + "=" * 60)
print("Dwan wins with a straight (7-6-5-4-3)!")
print("Ivey had a wheel (5-4-3-2-A) but the river paired the board")
print("=" * 60)
