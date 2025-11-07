import json
import threading
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
        with self.lock or open('/dev/null', 'w'):
            poker_code = f"{rank}{suit[0].lower()}"
            self.registry[str(uid)] = {'rank': rank, 'suit': suit, 'poker_code': poker_code}
            with open(self.json_path, 'w') as f:
                json.dump(self.registry, f, indent=2)
    def list_all(self):
        return [(uid, card) for uid, card in self.registry.items()]
    def remove_card(self, uid):
        if str(uid) in self.registry:
            del self.registry[str(uid)]
            with open(self.json_path, 'w') as f:
                json.dump(self.registry, f, indent=2)
if __name__ == "__main__":
    print("This module exposes the RFIDCardRegistry class for use by PokerKit UI and admin tools.")
