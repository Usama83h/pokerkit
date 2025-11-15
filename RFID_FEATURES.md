# RFID Card Integration for PokerKit

This extension adds RFID card reading and management capabilities to PokerKit, enabling physical poker games with RFID-tagged cards.

## Features

### 1. RFID Card Registry System
- Map RFID UIDs to poker cards
- Store mappings in JSON format
- Support for complete 52-card deck
- Thread-safe registry operations

### 2. Card Management Tools
- **`register_cards.py`** - Interactive card registration tool
- **`import_rfid_csv.py`** - Bulk import from CSV files
- **`view_cards.html`** - Visual card registry browser

### 3. Game Integration
- **`pokerkit/poker_ui.py`** - Streamlit UI with RFID support
- **`pokerkit/poker_rfid_integration.py`** - Core RFID integration module
- **`pokerkit/rfid_registry_tool.py`** - Command-line registry tool

## Quick Start

### 1. Register Your Cards

#### Option A: Import from CSV
```bash
python import_rfid_csv.py cards_import.csv
```

CSV format:
```csv
UID,Rank,Suit
184097028,A,hearts
4202573316,2,hearts
...
```

#### Option B: Interactive Registration
```bash
python register_cards.py
```

Features:
- Register single cards
- Batch registration
- Quick 52-card registration wizard
- List, search, and manage cards
- Export/import CSV
- Statistics and validation

### 2. View Your Registry

Open `view_cards.html` in a browser to see:
- All registered cards organized by suit
- Search by UID or card code
- Visual card display with suit symbols
- Registry statistics

### 3. Use in Games

#### Streamlit UI (Recommended)
```bash
pip install streamlit pyttsx3
streamlit run pokerkit/poker_ui.py
```

Features:
- Live RFID card scanning
- Automatic card recognition
- Text-to-speech announcements
- Visual game state
- Multi-player support

#### Python Integration
```python
from pokerkit.poker_rfid_integration import RFIDCardRegistry

# Load registry
registry = RFIDCardRegistry('cards.json')

# Look up a card by UID
card_code = registry.get_poker_code('184097028')
print(card_code)  # Output: 'Ah'

# Register a new card
registry.register_card('123456789', 'K', 'spades')

# List all cards
all_cards = registry.list_all()
```

## File Structure

```
pokerkit/
├── poker_rfid_integration.py   # Core RFID module
├── poker_ui.py                  # Streamlit game UI
├── rfid_registry_tool.py        # CLI registry tool
├── register_cards.py            # Interactive registration
├── import_rfid_csv.py           # CSV import utility
├── view_cards.html              # Visual registry browser
├── cards.json                   # Card registry (generated)
└── cards_import.csv             # Sample CSV data
```

## Card Registry Format

### JSON Structure (`cards.json`)
```json
{
  "184097028": {
    "rank": "A",
    "suit": "hearts",
    "poker_code": "Ah"
  },
  "4202573316": {
    "rank": "2",
    "suit": "hearts",
    "poker_code": "2h"
  }
}
```

### Poker Code Format
- **Ranks**: `A`, `2-9`, `T` (10), `J`, `Q`, `K`
- **Suits**: `h` (hearts), `d` (diamonds), `c` (clubs), `s` (spades)
- **Examples**: `Ah`, `Ks`, `Qd`, `Jc`, `Th`

## Hardware Requirements

### RFID Reader
- **Recommended**: MFRC522 RFID reader module
- **Interface**: SPI
- **Frequency**: 13.56 MHz
- **Compatible with**: Raspberry Pi, Arduino

### RFID Cards
- **Type**: MIFARE Classic 1K or compatible
- **Frequency**: 13.56 MHz
- **Recommended**: 52 cards (standard deck)

### Python Dependencies
```bash
pip install mfrc522  # For Raspberry Pi
pip install RPi.GPIO  # For Raspberry Pi GPIO
pip install streamlit  # For UI
pip install pyttsx3  # For text-to-speech (optional)
```

## Platform Support

### Raspberry Pi (Full Support)
- RFID reading via GPIO
- Real-time card scanning
- Hardware integration

### Desktop/Laptop (Limited Support)
- Card management tools work
- Manual UID entry
- No hardware RFID reading

## Usage Examples

### Example 1: Register a Complete Deck
```bash
python register_cards.py
# Select option 9: Quick register (52 cards)
# Follow the prompts to scan each card
```

### Example 2: Import Existing Data
```bash
python import_rfid_csv.py my_cards.csv
```

### Example 3: Look Up a Card
```bash
python register_cards.py
# Select option 4: Look up card by UID
# Enter UID: 184097028
# Output: UID 184097028 -> Ah (A♥ of hearts)
```

### Example 4: Export for Backup
```bash
python register_cards.py
# Select option 7: Export to CSV
# Creates: cards_export.csv
```

### Example 5: Use in Game
```python
from pokerkit import NoLimitTexasHoldem, Automation
from pokerkit.poker_rfid_integration import RFIDCardRegistry

# Load card registry
registry = RFIDCardRegistry('cards.json')

# Create game
state = NoLimitTexasHoldem.create_state(
    (Automation.ANTE_POSTING, Automation.BET_COLLECTION),
    True, 0, (10, 20), 20, (1000, 1000), 2
)

# Scan and deal cards
uid = scan_rfid_card()  # Your RFID reading function
card_code = registry.get_poker_code(uid)
if card_code:
    state.deal_hole(card_code)
```

## API Reference

### RFIDCardRegistry Class

#### `__init__(json_path='cards.json')`
Initialize registry from JSON file.

#### `get_poker_code(uid) -> str | None`
Get poker code for a given UID.

#### `register_card(uid, rank, suit) -> None`
Register a new card or update existing.

#### `list_all() -> list[tuple[str, dict]]`
Get all registered cards.

#### `remove_card(uid) -> None`
Remove a card from registry.

## Troubleshooting

### Card Not Recognized
1. Check UID is correct in `cards.json`
2. Verify RFID reader is working
3. Ensure `cards.json` is in the correct directory
4. Check card is within reader range

### Import Errors
1. Verify CSV format matches expected structure
2. Check for duplicate UIDs
3. Validate rank and suit values
4. Ensure file encoding is UTF-8

### RFID Reader Issues
1. Check GPIO connections (Raspberry Pi)
2. Verify SPI is enabled
3. Test with `SimpleMFRC522` examples
4. Check power supply to reader

## Demo Files

Several demo and documentation files are included:

- **`demo_poker.py`** - Famous poker hand simulation
- **`poker_demo_standalone.py`** - Comprehensive demo
- **`poker_demo.html`** - Interactive browser demo
- **`DEMO_GUIDE.md`** - Code examples and tutorials
- **`RFID_IMPORT_COMPLETE.md`** - Import documentation

## Contributing

To add RFID support for other card types or readers:

1. Extend `RFIDCardRegistry` class
2. Add new reader interface in `poker_rfid_integration.py`
3. Update UI to support new hardware
4. Add tests for new functionality

## License

This RFID integration follows the same MIT license as PokerKit.

## Credits

RFID integration developed as an extension to PokerKit by the Universal, Open, Free, and Transparent Computer Poker Research Group.

## Support

For issues or questions:
- Check existing documentation
- Review example files
- Open an issue on GitHub
- Consult PokerKit main documentation

## Future Enhancements

Planned features:
- [ ] Support for NFC cards
- [ ] Mobile app integration
- [ ] Cloud-based registry sync
- [ ] Multi-deck support
- [ ] Card wear tracking
- [ ] Tournament mode with RFID
- [ ] Real-time game streaming
- [ ] Advanced analytics dashboard
