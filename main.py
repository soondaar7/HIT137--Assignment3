# MAIN ENTRY POINT - RUN THIS FILE TO START THE GAME
# This file connects the GUI, Logic, and Image Processing.

from gui import MYGUI
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = MYGUI(root)
    root.mainloop()