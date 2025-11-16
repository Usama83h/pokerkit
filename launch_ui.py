#!/usr/bin/env python3
"""
Launch PokerKit RFID UI
Checks dependencies and launches the Streamlit interface
"""

import sys
import subprocess

def check_streamlit():
    """Check if streamlit is installed"""
    try:
        import streamlit
        return True
    except ImportError:
        return False

def check_pyttsx3():
    """Check if pyttsx3 is installed"""
    try:
        import pyttsx3
        return True
    except ImportError:
        return False

def install_package(package):
    """Install a package using pip"""
    print(f"Installing {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    print("=" * 60)
    print("PokerKit RFID UI Launcher")
    print("=" * 60)
    
    # Check Streamlit
    if not check_streamlit():
        print("\n⚠️  Streamlit not found!")
        response = input("Install Streamlit? (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            try:
                install_package('streamlit')
                print("✓ Streamlit installed successfully!")
            except Exception as e:
                print(f"✗ Error installing Streamlit: {e}")
                return
        else:
            print("Cannot launch UI without Streamlit.")
            return
    else:
        print("✓ Streamlit found")
    
    # Check pyttsx3 (optional)
    if not check_pyttsx3():
        print("\n⚠️  pyttsx3 (text-to-speech) not found (optional)")
        response = input("Install pyttsx3 for voice announcements? (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            try:
                install_package('pyttsx3')
                print("✓ pyttsx3 installed successfully!")
            except Exception as e:
                print(f"⚠️  Could not install pyttsx3: {e}")
                print("   (Continuing without voice announcements)")
    else:
        print("✓ pyttsx3 found")
    
    # Launch Streamlit
    print("\n" + "=" * 60)
    print("Launching PokerKit UI...")
    print("=" * 60)
    print("\nThe UI will open in your browser.")
    print("Press Ctrl+C to stop the server.\n")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            "pokerkit/poker_ui.py"
        ])
    except KeyboardInterrupt:
        print("\n\nUI stopped by user.")
    except Exception as e:
        print(f"\n✗ Error launching UI: {e}")

if __name__ == "__main__":
    main()
