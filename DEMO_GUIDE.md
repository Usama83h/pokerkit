# PokerKit Demo Guide

## Running PokerKit

Since there appear to be Python environment issues, here's how to run PokerKit once Python is properly configured:

### Installation
```bash
pip install pokerkit
```

### Quick Start Examples

#### 1. Simple Texas Hold'em Hand
```python
from pokerkit import NoLimitTexasHoldem, Automation

# Create a 2-player game
state = NoLimitTexasHoldem.create_state(
    (Automation.ANTE_POSTING, Automation.BET_COLLECTION, 
     Automation.BLIND_OR_STRADDLE_POSTING),
    True,  # Uniform antes
    0,     # Antes amount
    (10, 20),  # Blinds (SB, BB)
    20,    # Min bet
    (1000, 1000),  # Starting stacks
    2      # Number of players
)

# Deal hole cards
state.deal_hole('AhKh')  # Player 1
state.deal_hole('QsQd')  # Player 2

# Pre-flop action
state.complete_bet_or_raise_to(60)  # Player 1 raises
state.check_or_call()  # Player 2 calls

# Deal flop
state.burn_card('??')
state.deal_board('KsQh2c')

# Post-flop action
state.check_or_call()  # Player 2 checks
state.complete_bet_or_raise_to(100)  # Player 1 bets
state.check_or_call()  # Player 2 calls

print(f"Pot: {state.total_pot_amount}")
print(f"Stacks: {state.stacks}")
```

#### 2. Hand Evaluation
```python
from pokerkit import StandardHighHand

# Create hands
hand1 = StandardHighHand('AhKhQhJhTh')  # Royal Flush
hand2 = StandardHighHand('9s9h9d9c8s')  # Four of a Kind

print(hand1)  # Royal flush (AhKhQhJhTh)
print(hand2)  # Four of a kind (9s9h9d9c8s)
print(hand1 > hand2)  # True
```

#### 3. Equity Calculation
```python
from pokerkit import calculate_equities, StandardHighHand

# Calculate equity between two hands
equities = calculate_equities(
    [['AhKh'], ['QsQd']],  # Hole cards
    ['Ks', 'Qh', '2c'],    # Board cards
    StandardHighHand,
    sample_count=10000
)

print(f"Player 1 equity: {equities[0]:.2%}")
print(f"Player 2 equity: {equities[1]:.2%}")
```

#### 4. Range Analysis
```python
from pokerkit import parse_range, RankOrder

# Parse a range like "AK, QQ+"
hands = list(parse_range('AKs', RankOrder.STANDARD))
print(f"AKs contains {len(hands)} combinations")

# Parse pocket pairs
pairs = list(parse_range('AA', RankOrder.STANDARD))
print(f"AA contains {len(pairs)} combinations")
```

#### 5. Multi-Runout Example
```python
from math import inf
from pokerkit import NoLimitTexasHoldem, Automation, Mode

# Famous Phil Hellmuth vs Ernest Wiggins hand
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
    False,
    {-1: 600},  # Antes
    (200, 400, 800),  # Blinds
    400,
    (inf, 116400, 86900, inf, 50000, inf),
    6,
    mode=Mode.CASH_GAME,
)

# ... deal cards and play hand ...
# After all-in, select multiple runouts
state.select_runout_count(4)  # Run it 4 times!
```

## Available Demos

### Run the comprehensive demo:
```bash
python demo_poker.py
```

### Run the simple test:
```bash
python simple_demo.py
```

### Run the Streamlit UI (requires streamlit):
```bash
pip install streamlit
streamlit run pokerkit/poker_ui.py
```

### Run the RFID registry tool:
```bash
python pokerkit/rfid_registry_tool.py
```

## Supported Poker Variants

- **Texas Hold'em** (No-Limit, Fixed-Limit, Pot-Limit)
- **Omaha Hold'em** (Pot-Limit, Hi-Lo Split)
- **Short-Deck Hold'em** (No-Limit)
- **Seven Card Stud** (Fixed-Limit, Hi-Lo Split)
- **Razz** (Fixed-Limit)
- **Badugi** (Fixed-Limit)
- **Deuce-to-Seven Lowball** (Triple Draw, Single Draw)
- **Royal Hold'em** (No-Limit)

## Key Features

1. **Game Simulation** - Full poker game state management
2. **Hand Evaluation** - Fast hand strength calculations
3. **Equity Calculations** - Monte Carlo simulations
4. **Range Analysis** - Parse and analyze hand ranges
5. **Hand History Parsing** - Import from major poker sites
6. **Statistical Analysis** - ICM, hand strength, etc.
7. **Custom Games** - Define your own poker variants

## Troubleshooting

If you see "Python" output without actual results, your Python installation may need repair:

1. Check Python installation: `python --version`
2. Reinstall Python from python.org
3. Ensure Python is in your PATH
4. Try using `py` command instead of `python` on Windows

## Documentation

Full documentation: https://pokerkit.readthedocs.io/
