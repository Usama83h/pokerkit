# 🚀 Quick Start - PokerKit RFID UI

## You Have 3 UI Options!

### 1. 🌐 **HTML Viewer** (Easiest - Works Now!)

**Just double-click this file**:
```
view_cards.html
```

Or in command line:
```bash
start view_cards.html
```

✅ **No Python needed**  
✅ **Works immediately**  
✅ **Shows all 52 cards**  
✅ **Has search function**  

---

### 2. 🖥️ **Desktop GUI** (Native Windows App)

**Run this**:
```bash
python card_viewer_gui.py
```

✅ **Native Windows interface**  
✅ **Tabbed by suit**  
✅ **Scrollable cards**  
✅ **Built-in search**  

---

### 3. 🎮 **Streamlit Game UI** (Full Poker Game)

**Run this**:
```bash
python launch_ui.py
```

This will:
1. Check if Streamlit is installed
2. Install it if needed
3. Launch the full poker game UI

✅ **Play actual poker**  
✅ **RFID card scanning**  
✅ **Voice announcements**  
✅ **Multi-player**  

---

## What You Ran (Text Interface)

If you ran `python register_cards.py` or similar, you got the **text menu interface** for managing cards.

That's correct! It's for:
- Adding new cards
- Editing cards
- Importing CSV
- Managing registry

---

## To Get Graphical UI:

### Option A: HTML (Instant)
1. Find `view_cards.html` in File Explorer
2. Double-click it
3. Done! Your browser opens with all cards

### Option B: Desktop App
1. Open Command Prompt or PowerShell
2. Navigate to: `C:\Users\bmth8\.kiro\POKER\pokerkit`
3. Run: `python card_viewer_gui.py`
4. A window opens with your cards

### Option C: Full Game
1. Open Command Prompt or PowerShell
2. Navigate to: `C:\Users\bmth8\.kiro\POKER\pokerkit`
3. Run: `python launch_ui.py`
4. Follow prompts to install Streamlit
5. Browser opens with poker game

---

## Files You Have:

| File | Type | Purpose |
|------|------|---------|
| `view_cards.html` | HTML | Visual card browser |
| `card_viewer_gui.py` | Python | Desktop GUI app |
| `launch_ui.py` | Python | Game UI launcher |
| `register_cards.py` | Python | Card management (text) |
| `import_rfid_csv.py` | Python | CSV import (text) |
| `cards.json` | Data | Your 52 cards |

---

## Simplest Way Right Now:

**Just open `view_cards.html` in your browser!**

1. Go to: `C:\Users\bmth8\.kiro\POKER\pokerkit`
2. Find: `view_cards.html`
3. Double-click it
4. See all your cards in a nice interface!

---

## If Python Commands Don't Work:

Your Windows Store Python has issues. But the HTML file works without Python!

**Alternative**: Use the HTML file for viewing, and fix Python later for the game features.

---

## Summary:

✅ **Your 52 cards are registered** in `cards.json`  
✅ **HTML viewer works** without any setup  
✅ **Desktop GUI available** if Python works  
✅ **Full game UI available** with Streamlit  

**Start with**: `view_cards.html` (just double-click it!)
