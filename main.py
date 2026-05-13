import tkinter as tk
from src.cyber_wordle.ui import CyberWordleUI

def main():
    root = tk.Tk()
    # Explicitly set the window size or state before initializing UI if needed
    root.geometry("1200x800")
    app = CyberWordleUI(root)

    # Optional: ensure it's zoomed on supported platforms
    try:
        root.state('zoomed')
    except tk.TclError:
        pass

    root.mainloop()

if __name__ == "__main__":
    main()
