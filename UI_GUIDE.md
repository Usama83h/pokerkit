# PokerKit UI Guide

## Available User Interfaces

You have **3 different UI options** to view and manage your RFID cards:

### 1. 🌐 Web Browser (HTML) - **Simplest, No Installation**
**File**: `view_cards.html`

**How to run**:
```bash
start view_cards.html
```
Or just double-click the file.

**Features**:
- ✅ No Python required
- ✅ Works immediately
- ✅ Visual card display
- ✅ Search functionality
- ✅ Organized by suit
- ✅ Color-coded

**Best for**: Quick viewing, no setup needed

---

### 2. 🖥️ Desktop GUI (Tkinter) - **Native Windows App**
**File**: `card_viewer_gui.py`

**How to run**:
```bash
python card_viewer_gui.py
```

**Features**:
- ✅ Native Windows interface
- ✅ Tabbed view by suit
- ✅ Scrollable card grid
- ✅ Search box
- ✅ No extra installation (tkinter comes with Python)

**Best for**: Desktop application feel

---

### 3. 🎮 Streamlit Game UI - **Full Poker Game**
**File**: `pokerkit/poker_ui.py`

**How to run**:
```bash
# Option A: Use launcher (installs dependencies)
python launch_ui.py

# Option B: Manual
pip install streamlit pyttsx3
streamlit run pokerkit/poker_ui.py
```

**Features**:
- ✅ Full poker game interface
- ✅ Live RFID card scanning
- ✅ Text-to-speech announcements
- ✅ Multi-player support
- ✅ Game state visualization
- ✅ Action logging

**Best for**: Playing actual poker games with RFID cards

---

## Quick Start Guide

### Step 1: Choose Your Interface

**Just want to view cards?**
→ Use `view_cards.html` (double-click it)

**Want a desktop app?**
→ Run `python card_viewer_gui.py`

**Want to play poker?**
→ Run `python launch_ui.py`

### Step 2: Running the UI

#### For HTML Viewer:
```bash
# Windows
start view_cards.html

# Or just double-click the file in File Explorer
```

#### For Tkinter GUI:
```bash
python card_viewer_gui.py
```

#### For Streamlit Game:
```bash
# Easy way (auto-installs dependencies)
python launch_ui.py

# Manual way
pip install streamlit pyttsx3
streamlit run pokerkit/poker_ui.py
```

---

## Comparison Table

| Feature | HTML | Tkinter GUI | Streamlit |
|---------|------|-------------|-----------|
| Installation | None | None | pip install |
| Card Viewing | ✅ | ✅ | ✅ |
| Search | ✅ | ✅ | ✅ |
| RFID Scanning | ❌ | ❌ | ✅ |
| Play Poker | ❌ | ❌ | ✅ |
| Text-to-Speech | ❌ | ❌ | ✅ |
| Offline | ✅ | ✅ | ✅ |
| Speed | Instant | Fast | Medium |

---

## Troubleshooting

### "No module named 'streamlit'"
**Solution**: Install Streamlit
```bash
pip install streamlit
```
Or use the launcher:
```bash
python launch_ui.py
```

### "No module named 'tkinter'"
**Solution**: Tkinter should come with Python. If missing:
- Reinstall Python with "tcl/tk" option checked
- Or use the HTML viewer instead

### HTML file shows code instead of UI
**Solution**: 
- Right-click → Open with → Browser (Chrome, Firefox, Edge)
- Or drag the file into your browser window

### Streamlit won't start
**Solution**:
```bash
# Check if streamlit is installed
pip list | findstr streamlit

# If not found, install it
pip install streamlit

# Try running directly
python -m streamlit run pokerkit/poker_ui.py
```

---

## Screenshots & Examples

### HTML Viewer
- Opens in your default browser
- Shows all 52 cards organized by suit
- Search box at top
- Click-free, instant viewing

### Tkinter GUI
- Native Windows window
- Tabs for each suit (Hearts, Diamonds, Clubs, Spades)
- Scrollable grid of cards
- Search functionality

### Streamlit Game UI
- Web-based interface (runs locally)
- Full poker table visualization
- Player positions and stacks
- Action buttons
- RFID card scanning support
- Game log and history

---

## Command-Line Tools (Text Interface)

If you ran something and got text-only output, you probably ran one of these:

### `register_cards.py` - Card Management
```bash
python register_cards.py
```
**Purpose**: Register, edit, and manage cards
**Interface**: Text menu with options
**Use when**: Adding/removing cards

### `import_rfid_csv.py` - CSV Import
```bash
python import_rfid_csv.py cards_import.csv
```
**Purpose**: Bulk import cards from CSV
**Interface**: Text output with progress
**Use when**: Importing many cards at once

### `pokerkit/rfid_registry_tool.py` - CLI Tool
```bash
python pokerkit/rfid_registry_tool.py
```
**Purpose**: Command-line card management
**Interface**: Interactive text prompts
**Use when**: Quick card operations

---

## Recommended Workflow

### For Viewing Cards:
1. **Quick look**: Double-click `view_cards.html`
2. **Desktop app**: Run `python card_viewer_gui.py`

### For Managing Cards:
1. **Add cards**: Run `python register_cards.py`
2. **Import CSV**: Run `python import_rfid_csv.py your_file.csv`

### For Playing Poker:
1. **First time**: Run `python launch_ui.py` (installs dependencies)
2. **After that**: Run `streamlit run pokerkit/poker_ui.py`

---

## Installation Requirements

### HTML Viewer
- ✅ No requirements
- Just a web browser

### Tkinter GUI
- ✅ Python 3.11+
- ✅ Tkinter (included with Python)
- ✅ cards.json file

### Streamlit Game UI
- ✅ Python 3.11+
- ✅ Streamlit: `pip install streamlit`
- ✅ pyttsx3 (optional): `pip install pyttsx3`
- ✅ cards.json file
- ✅ RFID reader (optional, for scanning)

---

## Next Steps

1. **View your cards**: Open `view_cards.html`
2. **Try the GUI**: Run `python card_viewer_gui.py`
3. **Play poker**: Run `python launch_ui.py`

---

## Getting Help

- **HTML not working?** → Try a different browser
- **Python errors?** → Check Python version: `python --version` (need 3.11+)
- **Streamlit issues?** → Run `python launch_ui.py` to auto-install
- **Cards not showing?** → Make sure `cards.json` exists

---

## Summary

**Fastest way to see your cards**:
```bash
start view_cards.html
```

**Best desktop experience**:
```bash
python card_viewer_gui.py
```

**Full poker game**:
```bash
python launch_ui.py
```

Choose the one that fits your needs!
