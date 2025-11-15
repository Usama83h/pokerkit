# How to Run PokerKit

## What Just Happened

I've created several demo files for you:

### 1. **poker_demo.html** ✅ (OPENED IN BROWSER)
An interactive HTML visualization showing:
- The famous Tom Dwan vs Phil Ivey million-dollar pot
- Visual poker table with cards and players
- Complete action history
- PokerKit features overview
- Quick start code examples

**This should be open in your browser now!**

### 2. **demo_poker.py**
A Python script that simulates the same hand using PokerKit's API.

**To run:**
```bash
python demo_poker.py
```

### 3. **simple_demo.py**
A minimal test to verify PokerKit installation.

**To run:**
```bash
python simple_demo.py
```

### 4. **DEMO_GUIDE.md**
Comprehensive guide with multiple code examples showing:
- Basic game simulation
- Hand evaluation
- Equity calculations
- Range analysis
- Multi-runout scenarios

## Python Environment Issue

Your Python installation appears to have an issue where commands run but don't display output properly. To fix this:

### Option 1: Reinstall Python
1. Download Python 3.11+ from https://python.org
2. During installation, check "Add Python to PATH"
3. Restart your terminal

### Option 2: Use Python Launcher
Try using `py` instead of `python`:
```bash
py demo_poker.py
py simple_demo.py
```

### Option 3: Use Full Path
```bash
C:\Users\bmth8\AppData\Local\Microsoft\WindowsApps\python.exe demo_poker.py
```

## Install PokerKit

If not already installed:
```bash
pip install pokerkit
```

Or:
```bash
python -m pip install pokerkit
```

## Run the Streamlit UI

For an interactive web interface:
```bash
pip install streamlit pyttsx3
streamlit run pokerkit/poker_ui.py
```

This provides:
- Live poker game simulation
- RFID card integration support
- Text-to-speech announcements
- Visual game state

## Run Tests

To verify everything works:
```bash
python -m pytest pokerkit/tests/ -v
```

## What PokerKit Can Do

✅ **Simulate poker games** - Full state management for 15+ variants
✅ **Evaluate hands** - Lightning-fast hand strength calculations  
✅ **Calculate equity** - Monte Carlo simulations for any scenario
✅ **Parse ranges** - Analyze hand ranges like "AK+, QQ+"
✅ **Import hand histories** - From PokerStars, Full Tilt, etc.
✅ **Statistical analysis** - ICM, hand strength, and more
✅ **Custom variants** - Define your own poker games
✅ **RFID integration** - Physical card tracking (custom addition)

## Next Steps

1. Open **poker_demo.html** in your browser (should already be open)
2. Read **DEMO_GUIDE.md** for code examples
3. Fix Python environment if needed
4. Run **demo_poker.py** to see PokerKit in action
5. Explore the test files in `pokerkit/tests/` for more examples

## Documentation

- Official Docs: https://pokerkit.readthedocs.io/
- GitHub: https://github.com/uoftcprg/pokerkit
- Paper: IEEE Transactions on Games (2025)
