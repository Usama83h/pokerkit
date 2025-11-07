import json
import os
import threading
try:
    from mfrc522 import SimpleMFRC522
    import RPi.GPIO as GPIO
except ImportError:
    SimpleMFRC522 = None
    GPIO = None
    print("Warning: SimpleMFRC522 or RPi.GPIO not found, RFID reading will not work on this platform.")

CARDS_JSON = 'cards.json'

class RFIDCardRegistry:
    def __init__(self, json_path=CARDS_JSON):
        self.json_path = json_path
        self.lock = threading.Lock() if threading.current_thread() else None
        self.registry = self._load_registry()
    def _load_registry(self):
        try:
            with open(self.json_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    def get_poker_code(self, uid):
        return self.registry.get(str(uid), {}).get('poker_code')
    def register_card(self, uid, rank, suit):
        with self.lock or open(os.devnull, 'w'):
            poker_code = f"{rank}{suit[0].lower()}"
            self.registry[str(uid)] = {'rank': rank, 'suit': suit, 'poker_code': poker_code}
            with open(self.json_path, 'w') as f:
                json.dump(self.registry, f, indent=2)
            print(f"Registered: {poker_code} -> UID {uid}")
    def list_all(self):
        print("Registered cards:")
        for uid, card in self.registry.items():
            print(f"  UID {uid}: {card['poker_code']} ({card['rank']} of {card['suit']})")
    def remove_card(self, uid):
        if str(uid) in self.registry:
            del self.registry[str(uid)]
            with open(self.json_path, 'w') as f:
                json.dump(self.registry, f, indent=2)
            print(f"Removed UID {uid}")
        else:
            print(f"UID {uid} not found.")

if __name__ == "__main__":
    print("RFID Card Registry Admin Tool:")
    reg = RFIDCardRegistry()
    while True:
        print("\nActions: [register, list, remove, lookup, exit]")
        action = input("Enter action: ").strip().lower()
        if action == 'register':
            uid = input("Enter card UID (scan or type): ").strip()
            rank = input("Enter rank (e.g., A, K, Q, J, 10, ...): ").strip().upper()
            suit = input("Enter suit (hearts, diamonds, clubs, spades): ").strip().lower()
            reg.register_card(uid, rank, suit)
        elif action == 'list':
            reg.list_all()
        elif action == 'remove':
            uid = input("UID to remove: ").strip()
            reg.remove_card(uid)
        elif action == 'lookup':
            uid = input("UID to look up: ").strip()
            code = reg.get_poker_code(uid)
            if code:
                print(f"UID {uid} => {code}")
            else:
                print(f"UID {uid} NOT REGISTERED")
        elif action == 'exit':
            break
        else:
            print("Unknown action.")
