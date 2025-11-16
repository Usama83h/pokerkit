#!/usr/bin/env python3
"""
Simple GUI Card Viewer using Tkinter
Shows registered RFID cards in a graphical window
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
from pathlib import Path

CARDS_JSON = 'cards.json'

class CardViewerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PokerKit RFID Card Viewer")
        self.root.geometry("900x600")
        
        # Load cards
        self.cards = self.load_cards()
        
        # Create UI
        self.create_widgets()
        self.populate_cards()
    
    def load_cards(self):
        """Load cards from JSON"""
        try:
            with open(CARDS_JSON, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found: {CARDS_JSON}")
            return {}
    
    def create_widgets(self):
        """Create UI widgets"""
        # Title
        title = tk.Label(
            self.root,
            text="🃏 RFID Card Registry",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=10
        )
        title.pack(fill=tk.X)
        
        # Stats frame
        stats_frame = tk.Frame(self.root, bg="#ecf0f1", pady=10)
        stats_frame.pack(fill=tk.X)
        
        total_label = tk.Label(
            stats_frame,
            text=f"Total Cards: {len(self.cards)}/52",
            font=("Arial", 12, "bold"),
            bg="#ecf0f1"
        )
        total_label.pack()
        
        # Search frame
        search_frame = tk.Frame(self.root, bg="#ecf0f1", pady=10)
        search_frame.pack(fill=tk.X, padx=10)
        
        tk.Label(
            search_frame,
            text="Search:",
            font=("Arial", 10),
            bg="#ecf0f1"
        ).pack(side=tk.LEFT, padx=5)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search)
        
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Arial", 10),
            width=40
        )
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Notebook for suits
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs for each suit
        self.suit_frames = {}
        suits = [
            ('Hearts', '♥', '#e74c3c'),
            ('Diamonds', '♦', '#3498db'),
            ('Clubs', '♣', '#2ecc71'),
            ('Spades', '♠', '#34495e')
        ]
        
        for suit_name, symbol, color in suits:
            frame = tk.Frame(self.notebook, bg="white")
            self.notebook.add(frame, text=f"{symbol} {suit_name}")
            self.suit_frames[suit_name.lower()] = frame
    
    def populate_cards(self):
        """Populate cards in each suit tab"""
        # Group cards by suit
        suits_cards = {
            'hearts': [],
            'diamonds': [],
            'clubs': [],
            'spades': []
        }
        
        for uid, card in self.cards.items():
            suit = card['suit']
            suits_cards[suit].append((uid, card))
        
        # Sort by rank
        rank_order = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
        
        for suit, cards in suits_cards.items():
            cards.sort(key=lambda x: rank_order.index(x[1]['rank']))
            self.create_suit_grid(self.suit_frames[suit], cards, suit)
    
    def create_suit_grid(self, parent, cards, suit):
        """Create grid of cards for a suit"""
        # Suit colors
        colors = {
            'hearts': '#e74c3c',
            'diamonds': '#3498db',
            'clubs': '#2ecc71',
            'spades': '#34495e'
        }
        
        symbols = {
            'hearts': '♥',
            'diamonds': '♦',
            'clubs': '♣',
            'spades': '♠'
        }
        
        color = colors.get(suit, 'black')
        symbol = symbols.get(suit, '')
        
        # Create scrollable frame
        canvas = tk.Canvas(parent, bg="white")
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Grid layout
        col = 0
        row = 0
        max_cols = 4
        
        for uid, card in cards:
            card_frame = tk.Frame(
                scrollable_frame,
                bg="white",
                relief=tk.RAISED,
                borderwidth=2,
                padx=10,
                pady=10
            )
            card_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            # Card display
            rank_label = tk.Label(
                card_frame,
                text=f"{card['rank']}{symbol}",
                font=("Arial", 24, "bold"),
                fg=color,
                bg="white"
            )
            rank_label.pack()
            
            code_label = tk.Label(
                card_frame,
                text=card['poker_code'],
                font=("Arial", 10),
                bg="white"
            )
            code_label.pack()
            
            uid_label = tk.Label(
                card_frame,
                text=f"UID: {uid}",
                font=("Arial", 8),
                fg="gray",
                bg="white"
            )
            uid_label.pack()
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def on_search(self, *args):
        """Handle search"""
        search_term = self.search_var.get().lower()
        # For now, just show message
        # Full implementation would filter cards
        if search_term:
            # Could implement filtering here
            pass

def main():
    """Main function"""
    if not Path(CARDS_JSON).exists():
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Error",
            f"Card registry not found: {CARDS_JSON}\n\n"
            "Please run 'python register_cards.py' first to create your card registry."
        )
        return
    
    root = tk.Tk()
    app = CardViewerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
