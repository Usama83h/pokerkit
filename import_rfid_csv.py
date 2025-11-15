#!/usr/bin/env python3
"""
Quick CSV Import Tool for RFID Cards
Imports card data from CSV and creates cards.json registry
"""

import csv
import json
import sys
from pathlib import Path

CARDS_JSON = 'cards.json'

def detect_csv_format(filename):
    """Detect the format of the CSV file"""
    with open(filename, 'r', encoding='utf-8-sig') as f:
        # Read first few lines
        lines = [f.readline().strip() for _ in range(3)]
    
    header = lines[0].lower()
    
    # Try to detect column format
    if 'uid' in header and 'rank' in header and 'suit' in header:
        return 'standard'
    elif 'rfid' in header or 'id' in header:
        return 'rfid_first'
    else:
        return 'unknown'

def import_csv(filename, output_json=CARDS_JSON):
    """Import CSV file and create JSON registry"""
    
    print(f"Reading CSV file: {filename}")
    
    registry = {}
    
    # Try to load existing registry
    if Path(output_json).exists():
        with open(output_json, 'r') as f:
            registry = json.load(f)
        print(f"Loaded {len(registry)} existing cards from {output_json}")
    
    # Suit mapping
    suit_map = {
        'h': 'hearts', 'heart': 'hearts', 'hearts': 'hearts', '♥': 'hearts',
        'd': 'diamonds', 'diamond': 'diamonds', 'diamonds': 'diamonds', '♦': 'diamonds',
        'c': 'clubs', 'club': 'clubs', 'clubs': 'clubs', '♣': 'clubs',
        's': 'spades', 'spade': 'spades', 'spades': 'spades', '♠': 'spades'
    }
    
    imported_count = 0
    skipped_count = 0
    error_count = 0
    
    try:
        with open(filename, 'r', encoding='utf-8-sig') as f:
            # Try to detect delimiter
            sample = f.read(1024)
            f.seek(0)
            
            delimiter = ','
            if '\t' in sample:
                delimiter = '\t'
            elif ';' in sample:
                delimiter = ';'
            
            reader = csv.DictReader(f, delimiter=delimiter)
            
            # Get headers
            headers = reader.fieldnames
            print(f"CSV Headers: {headers}")
            
            # Try to map headers to our format
            uid_col = None
            rank_col = None
            suit_col = None
            
            for header in headers:
                h_lower = header.lower().strip()
                if 'uid' in h_lower or 'rfid' in h_lower or 'id' in h_lower:
                    uid_col = header
                elif 'rank' in h_lower or 'value' in h_lower:
                    rank_col = header
                elif 'suit' in h_lower or 'color' in h_lower:
                    suit_col = header
            
            if not uid_col or not rank_col or not suit_col:
                print("\n⚠️  Could not auto-detect columns. Please specify:")
                print(f"Available columns: {', '.join(headers)}")
                uid_col = input(f"UID column [{uid_col}]: ").strip() or uid_col
                rank_col = input(f"Rank column [{rank_col}]: ").strip() or rank_col
                suit_col = input(f"Suit column [{suit_col}]: ").strip() or suit_col
            
            print(f"\nUsing columns:")
            print(f"  UID:  {uid_col}")
            print(f"  Rank: {rank_col}")
            print(f"  Suit: {suit_col}")
            print()
            
            # Process rows
            for row_num, row in enumerate(reader, start=2):
                try:
                    uid = str(row[uid_col]).strip()
                    rank = str(row[rank_col]).strip().upper()
                    suit_raw = str(row[suit_col]).strip().lower()
                    
                    if not uid or not rank or not suit_raw:
                        print(f"Row {row_num}: Skipping empty row")
                        skipped_count += 1
                        continue
                    
                    # Map suit
                    suit = suit_map.get(suit_raw, suit_raw)
                    if suit not in ['hearts', 'diamonds', 'clubs', 'spades']:
                        print(f"Row {row_num}: Invalid suit '{suit_raw}' - skipping")
                        error_count += 1
                        continue
                    
                    # Validate rank
                    valid_ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
                    if rank == '10':
                        rank = 'T'
                    if rank not in valid_ranks:
                        print(f"Row {row_num}: Invalid rank '{rank}' - skipping")
                        error_count += 1
                        continue
                    
                    # Create poker code
                    poker_code = f"{rank}{suit[0].lower()}"
                    
                    # Check for duplicates
                    if uid in registry:
                        old_code = registry[uid]['poker_code']
                        if old_code != poker_code:
                            print(f"Row {row_num}: UID {uid} already registered as {old_code}, updating to {poker_code}")
                    
                    # Register card
                    registry[uid] = {
                        'rank': rank,
                        'suit': suit,
                        'poker_code': poker_code
                    }
                    
                    print(f"Row {row_num}: ✓ {poker_code} -> UID {uid}")
                    imported_count += 1
                    
                except KeyError as e:
                    print(f"Row {row_num}: Missing column {e} - skipping")
                    error_count += 1
                except Exception as e:
                    print(f"Row {row_num}: Error - {e}")
                    error_count += 1
        
        # Save registry
        with open(output_json, 'w') as f:
            json.dump(registry, f, indent=2, sort_keys=True)
        
        print("\n" + "=" * 60)
        print("IMPORT COMPLETE")
        print("=" * 60)
        print(f"✓ Imported: {imported_count} cards")
        print(f"⊘ Skipped:  {skipped_count} rows")
        print(f"✗ Errors:   {error_count} rows")
        print(f"📁 Saved to: {output_json}")
        print(f"📊 Total cards in registry: {len(registry)}")
        print("=" * 60)
        
        # Show statistics
        suits_count = {'hearts': 0, 'diamonds': 0, 'clubs': 0, 'spades': 0}
        for card in registry.values():
            suits_count[card['suit']] += 1
        
        print("\nCards by suit:")
        symbols = {'hearts': '♥', 'diamonds': '♦', 'clubs': '♣', 'spades': '♠'}
        for suit, count in suits_count.items():
            print(f"  {symbols[suit]} {suit.capitalize():8s}: {count}/13")
        
        return True
        
    except FileNotFoundError:
        print(f"✗ Error: File '{filename}' not found")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function"""
    print("=" * 60)
    print("RFID CARD CSV IMPORT TOOL")
    print("=" * 60)
    
    # Get filename
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = input("\nEnter CSV filename: ").strip()
    
    if not filename:
        print("✗ No filename provided")
        return
    
    # Check if file exists
    if not Path(filename).exists():
        print(f"✗ File not found: {filename}")
        print("\nLooking for CSV files in current directory...")
        csv_files = list(Path('.').glob('*.csv'))
        if csv_files:
            print("Found:")
            for i, f in enumerate(csv_files, 1):
                print(f"  {i}. {f.name}")
            choice = input("\nSelect file number (or press Enter to cancel): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(csv_files):
                filename = str(csv_files[int(choice) - 1])
            else:
                return
        else:
            print("No CSV files found.")
            return
    
    # Import the CSV
    success = import_csv(filename)
    
    if success:
        print("\n✓ Import successful!")
        print(f"You can now use the cards.json file with PokerKit")
        print("\nNext steps:")
        print("  - Run: python register_cards.py (to view/edit cards)")
        print("  - Run: streamlit run pokerkit/poker_ui.py (to use in game)")
    
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
