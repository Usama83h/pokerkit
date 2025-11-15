# 🃏 RFID Card Integration for PokerKit

> Physical poker games with RFID-tagged cards

This extension adds RFID card reading and management capabilities to PokerKit, enabling real-world poker games with physical RFID-tagged cards.

## ✨ Features

- 🎴 **Card Registry System** - Map RFID UIDs to poker cards
- 🔧 **Management Tools** - Interactive registration and bulk import
- 🎮 **Game Integration** - Streamlit UI with live RFID scanning
- 📊 **Visual Browser** - Web-based card registry viewer
- 📁 **CSV Support** - Import/export card data
- 🎯 **Complete Deck** - Sample 52-card registry included

## 🚀 Quick Start

### 1. Register Your Cards

#### Import from CSV
```bash
python import_rfid_csv.py cards_import.csv
```

#### Interactive Registration
```bash
python register_cards.py
```

### 2. View Your Registry

Open `view_cards.html` in a browser to see all registered cards with search functionality.

### 3. Play Poker

```bash
pip install streamlit pyttsx3
streamlit run pokerkit/poker_ui.py
```

## 📦 What's Included

### Core Modules
- `pokerkit/poker_rfid_integration.py` - RFID registry system
- `pokerkit/poker_ui.py` - Streamlit game interface
- `pokerkit/rfid_registry_tool.py` - CLI management tool

### Management Tools
- `register_cards.py` - Interactive card registration
- `import_rfid_csv.py` - CSV import utility
- `view_cards.html` - Visual card browser

### Demo Files
- `demo_poker.py` - Famous hand simulation
- `poker_demo_standalone.py` - Comprehensive demo
- `poker_demo.html` - Interactive browser demo
- `simple_demo.py` - Quick test

### Documentation
- `RFID_FEATURES.md` - Complete guide
- `CHANGELOG_RFID.md` - Detailed changelog
- `DEMO_GUIDE.md` - Usage examples
- `RUN_INSTRUCTIONS.md` - Setup guide

### Sample Data
- `cards.json` - 52-card registry
- `cards_import.csv` - Sample CSV

## 💻 Usage Example

```python
from pokerkit.poker_rfid_integration import RFIDCardRegistry

# Load registry
registry = RFIDCardRegistry('cards.json')

# Look up a card
card_code = registry.get_poker_code('184097028')
print(card_code)  # Output: 'Ah'

# Register a new card
registry.register_card('123456789', 'K', 'spades')
```

## 🎯 Card Format

- **Ranks**: `A`, `2-9`, `T` (10), `J`, `Q`, `K`
- **Suits**: `h` (hearts), `d` (diamonds), `c` (clubs), `s` (spades)
- **Examples**: `Ah`, `Ks`, `Qd`, `Jc`, `Th`

## 🔌 Hardware Support

### RFID Reader
- **Type**: MFRC522 (13.56 MHz)
- **Interface**: SPI
- **Platform**: Raspberry Pi

### RFID Cards
- **Type**: MIFARE Classic 1K
- **Frequency**: 13.56 MHz
- **Quantity**: 52 cards (standard deck)

## 📋 CSV Format

```csv
UID,Rank,Suit
184097028,A,hearts
4202573316,2,hearts
3807453188,3,hearts
...
```

## 🛠️ Installation

```bash
# Core PokerKit
pip install pokerkit

# RFID support (Raspberry Pi)
pip install mfrc522 RPi.GPIO

# UI support
pip install streamlit pyttsx3
```

## 📊 Registry Statistics

Sample deck included:
- ♥ Hearts: 13/13 ✓
- ♦ Diamonds: 13/13 ✓
- ♣ Clubs: 13/13 ✓
- ♠ Spades: 13/13 ✓
- **Total: 52/52 complete!**

## 🎮 Interactive Tools

### Card Registration Tool
```bash
python register_cards.py
```

Features:
- Register single cards
- Batch registration
- Quick 52-card wizard
- Search and lookup
- Export/import CSV
- Statistics

### Visual Browser
Open `view_cards.html` for:
- All cards organized by suit
- Search by UID or card code
- Color-coded display
- Registry statistics

### Streamlit UI
```bash
streamlit run pokerkit/poker_ui.py
```

Features:
- Live RFID scanning
- Automatic card recognition
- Text-to-speech announcements
- Visual game state
- Multi-player support

## 📖 Documentation

- **[RFID_FEATURES.md](RFID_FEATURES.md)** - Complete integration guide
- **[DEMO_GUIDE.md](DEMO_GUIDE.md)** - Code examples and tutorials
- **[CHANGELOG_RFID.md](CHANGELOG_RFID.md)** - Detailed changelog
- **[RUN_INSTRUCTIONS.md](RUN_INSTRUCTIONS.md)** - Setup instructions

## 🎬 Demos

### Browser Demo
```bash
start poker_demo.html
```

### Python Demo
```bash
python demo_poker.py
```

### Comprehensive Demo
```bash
python poker_demo_standalone.py
```

## 🔧 Platform Support

| Platform | Card Management | RFID Reading | Game UI |
|----------|----------------|--------------|---------|
| Raspberry Pi | ✅ | ✅ | ✅ |
| Windows | ✅ | ❌ | ✅ |
| Linux | ✅ | ✅ | ✅ |
| macOS | ✅ | ❌ | ✅ |

## 🤝 Contributing

This RFID integration is an extension to PokerKit. Contributions welcome!

1. Fork the repository
2. Create your feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

MIT License - Same as PokerKit

## 🙏 Credits

RFID integration developed as an extension to PokerKit by the Universal, Open, Free, and Transparent Computer Poker Research Group.

## 📞 Support

- 📚 Check [RFID_FEATURES.md](RFID_FEATURES.md) for detailed documentation
- 🐛 Open an issue on GitHub
- 💬 Review example files and demos

## 🎯 Future Enhancements

- [ ] NFC card support
- [ ] Mobile app integration
- [ ] Cloud registry sync
- [ ] Multi-deck support
- [ ] Tournament mode
- [ ] Advanced analytics

## ⭐ Star This Repo

If you find this RFID integration useful, please star the repository!

---

**Part of [PokerKit](https://github.com/uoftcprg/pokerkit)** - A comprehensive Python library for poker game simulations
