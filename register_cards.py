#!/usr/bin/env python3
"""
RFID Card Registration Tool
Easy-to-use interface for registering poker cards with RFID tags
"""

import json
import os
from pathlib import Path

CARDS_JSON = 'cards.json'

# Standard deck of 52 cards
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
SUITS = {
    'h': 'hearts',
    'hearts': 'hearts',
    'd': 'diamonds', 
    'diamonds': 'diamonds',
    'c': 'clubs',
    'clubs': 'clubs',
    's': 'spades',
    'spades': 'spades'
}

class RFIDCardRegistry:
    def __init__(self, json_path=CARDS_JSON):
        self.json_path = json_path
        self.registry = self._load_registry()
    
    def _load_registry(self):
        """Load existing registry or create new one"""
        try:
            with open(self.json_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def _save_registry(self):
        """Save registry to file"""
        with open(self.json_path, 'w') as f:
            json.dump(self.registry, f, indent=2, sort_keys=True)
    
    def get_poker_code(self, uid):
        """Get poker code for a UID"""
        card = self.registry.get(str(uid))
        return card.get('poker_code') if card else None
    
    def register_card(self, uid, rank, suit):
        """Register a card with its RFID UID"""
        # Validate rank
        rank = rank.upper()
        if rank not in RANKS:
            raise ValueError(f"Invalid rank '{rank}'. Must be one of: {', '.join(RANKS)}")
        
        # Validate and normalize suit
        suit_lower = suit.lower()
        if suit_lower not in SUITS:
            raise ValueError(f"Invalid suit '{suit}'. Must be: hearts, diamonds, clubs, or spades (or h/d/c/s)")
        
        full_suit = SUITS[suit_lower]
        poker_code = f"{rank}{full_suit[0].lower()}"
        
        # Check if card already registered
        for existing_uid, card_data in self.registry.items():
            if card_data['poker_code'] == poker_code and existing_uid != str(uid):
                print(f"⚠️  Warning: {poker_code} is already registered to UID {existing_uid}")
                response = input("   Overwrite? (yes/no): ").strip().lower()
                if response not in ['yes', 'y']:
                    print("   Registration cancelled.")
                    return False
                # Remove old registration
                del self.registry[existing_uid]
                break
        
        # Register the card
        self.registry[str(uid)] = {
            'rank': rank,
            'suit': full_suit,
            'poker_code': poker_code
        }
        self._save_registry()
        print(f"✓ Registered: {poker_code} ({rank} of {full_suit}) -> UID {uid}")
        return True
    
    def register_batch(self, cards):
        """Register multiple cards at once"""
        for uid, rank, suit in cards:
            try:
                self.register_card(uid, rank, suit)
            except ValueError as e:
                print(f"✗ Error registering UID {uid}: {e}")
    
    def list_all(self, sort_by='poker'):
        """List all registered cards"""
        if not self.registry:
            print("No cards registered yet.")
            return
        
        print("\n" + "=" * 60)
        print("REGISTERED CARDS")
        print("=" * 60)
        
        # Sort cards
        if sort_by == 'poker':
            items = sorted(self.registry.items(), key=lambda x: x[1]['poker_code'])
        else:
            items = sorted(self.registry.items(), key=lambda x: x[0])
        
        for uid, card in items:
            poker_code = card['poker_code']
            rank = card['rank']
            suit = card['suit']
            
            # Add suit symbol
            suit_symbol = {'hearts': '♥', 'diamonds': '♦', 'clubs': '♣', 'spades': '♠'}[suit]
            
            print(f"  {poker_code:4s} ({rank}{suit_symbol:2s}) -> UID: {uid}")
        
        print("=" * 60)
        print(f"Total: {len(self.registry)} cards")
    
    def remove_card(self, uid):
        """Remove a card from registry"""
        uid_str = str(uid)
        if uid_str in self.registry:
            card = self.registry[uid_str]
            del self.registry[uid_str]
            self._save_registry()
            print(f"✓ Removed: {card['poker_code']} (UID {uid})")
            return True
        else:
            print(f"✗ UID {uid} not found in registry.")
            return False
    
    def lookup(self, uid):
        """Look up a card by UID"""
        card = self.registry.get(str(uid))
        if card:
            suit_symbol = {'hearts': '♥', 'diamonds': '♦', 'clubs': '♣', 'spades': '♠'}[card['suit']]
            print(f"UID {uid} -> {card['poker_code']} ({card['rank']}{suit_symbol} of {card['suit']})")
            return card
        else:
            print(f"UID {uid} is NOT REGISTERED")
            return None
    
    def export_to_csv(self, filename='cards_export.csv'):
        """Export registry to CSV"""
        import csv
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['UID', 'Rank', 'Suit', 'Poker Code'])
            for uid, card in sorted(self.registry.items(), key=lambda x: x[1]['poker_code']):
                writer.writerow([uid, card['rank'], card['suit'], card['poker_code']])
        print(f"✓ Exported {len(self.registry)} cards to {filename}")
    
    def import_from_csv(self, filename='cards_import.csv'):
        """Import registry from CSV"""
        import csv
        count = 0
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    self.register_card(row['UID'], row['Rank'], row['Suit'])
                    count += 1
                except Exception as e:
                    print(f"✗ Error importing row {row}: {e}")
        print(f"✓ Imported {count} cards from {filename}")
    
    def get_stats(self):
        """Get statistics about registered cards"""
        if not self.registry:
            print("No cards registered.")
            return
        
        suits_count = {'hearts': 0, 'diamonds': 0, 'clubs': 0, 'spades': 0}
        ranks_count = {r: 0 for r in RANKS}
        
        for card in self.registry.values():
            suits_count[card['suit']] += 1
            ranks_count[card['rank']] += 1
        
        print("\n" + "=" * 40)
        print("REGISTRY STATISTICS")
        print("=" * 40)
        print(f"Total cards: {len(self.registry)}/52")
        print(f"\nBy Suit:")
        for suit, count in suits_count.items():
            symbol = {'hearts': '♥', 'diamonds': '♦', 'clubs': '♣', 'spades': '♠'}[suit]
            print(f"  {symbol} {suit.capitalize():8s}: {count}/13")
        
        print(f"\nBy Rank:")
        for rank in RANKS:
            count = ranks_count[rank]
            print(f"  {rank:2s}: {count}/4")
        print("=" * 40)


def print_menu():
    """Print main menu"""
    print("\n" + "=" * 60)
    print("RFID CARD REGISTRATION TOOL")
    print("=" * 60)
    print("1. Register single card")
    print("2. Register multiple cards (batch)")
    print("3. List all cards")
    print("4. Look up card by UID")
    print("5. Remove card")
    print("6. Show statistics")
    print("7. Export to CSV")
    print("8. Import from CSV")
    print("9. Quick register (52 cards)")
    print("0. Exit")
    print("=" * 60)


def register_single(registry):
    """Register a single card"""
    print("\n--- Register Single Card ---")
    uid = input("Enter RFID UID: ").strip()
    if not uid:
        print("✗ UID cannot be empty")
        return
    
    print(f"Valid ranks: {', '.join(RANKS)}")
    rank = input("Enter rank (A, 2-9, T, J, Q, K): ").strip()
    
    print("Valid suits: hearts (h), diamonds (d), clubs (c), spades (s)")
    suit = input("Enter suit: ").strip()
    
    try:
        registry.register_card(uid, rank, suit)
    except ValueError as e:
        print(f"✗ Error: {e}")


def register_batch(registry):
    """Register multiple cards"""
    print("\n--- Batch Registration ---")
    print("Enter cards in format: UID,RANK,SUIT")
    print("Example: 123456789,A,hearts")
    print("Enter blank line when done.")
    
    cards = []
    while True:
        line = input("> ").strip()
        if not line:
            break
        
        parts = line.split(',')
        if len(parts) != 3:
            print("✗ Invalid format. Use: UID,RANK,SUIT")
            continue
        
        cards.append([p.strip() for p in parts])
    
    if cards:
        print(f"\nRegistering {len(cards)} cards...")
        registry.register_batch(cards)
    else:
        print("No cards to register.")


def quick_register_52(registry):
    """Quick registration template for full deck"""
    print("\n--- Quick Register 52 Cards ---")
    print("This will help you register a complete deck.")
    print("You'll need to scan each card's RFID tag.")
    
    response = input("\nReady to start? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        return
    
    for suit_code, suit_name in [('h', 'hearts'), ('d', 'diamonds'), ('c', 'clubs'), ('s', 'spades')]:
        suit_symbol = {'hearts': '♥', 'diamonds': '♦', 'clubs': '♣', 'spades': '♠'}[suit_name]
        print(f"\n--- {suit_symbol} {suit_name.upper()} ---")
        
        for rank in RANKS:
            poker_code = f"{rank}{suit_code}"
            
            # Check if already registered
            already_registered = False
            for card in registry.registry.values():
                if card['poker_code'] == poker_code:
                    already_registered = True
                    break
            
            if already_registered:
                print(f"  {poker_code} - Already registered (skipping)")
                continue
            
            while True:
                uid = input(f"  Scan {poker_code} ({rank}{suit_symbol}): ").strip()
                if not uid:
                    skip = input("    Skip this card? (yes/no): ").strip().lower()
                    if skip in ['yes', 'y']:
                        break
                    continue
                
                try:
                    registry.register_card(uid, rank, suit_name)
                    break
                except ValueError as e:
                    print(f"    ✗ Error: {e}")
    
    print("\n✓ Quick registration complete!")
    registry.get_stats()


def main():
    """Main program loop"""
    registry = RFIDCardRegistry()
    
    print("=" * 60)
    print("RFID POKER CARD REGISTRATION TOOL")
    print("=" * 60)
    print(f"Registry file: {os.path.abspath(CARDS_JSON)}")
    
    if os.path.exists(CARDS_JSON):
        print(f"Loaded {len(registry.registry)} existing cards")
    else:
        print("No existing registry found - will create new one")
    
    while True:
        print_menu()
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            register_single(registry)
        elif choice == '2':
            register_batch(registry)
        elif choice == '3':
            registry.list_all()
        elif choice == '4':
            uid = input("Enter UID to lookup: ").strip()
            registry.lookup(uid)
        elif choice == '5':
            uid = input("Enter UID to remove: ").strip()
            registry.remove_card(uid)
        elif choice == '6':
            registry.get_stats()
        elif choice == '7':
            filename = input("Export filename (default: cards_export.csv): ").strip()
            registry.export_to_csv(filename if filename else 'cards_export.csv')
        elif choice == '8':
            filename = input("Import filename (default: cards_import.csv): ").strip()
            if os.path.exists(filename if filename else 'cards_import.csv'):
                registry.import_from_csv(filename if filename else 'cards_import.csv')
            else:
                print(f"✗ File not found: {filename}")
        elif choice == '9':
            quick_register_52(registry)
        elif choice == '0':
            print("\nGoodbye!")
            break
        else:
            print("✗ Invalid option. Please try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
