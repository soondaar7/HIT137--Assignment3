# MAIN ENTRY POINT - RUN THIS FILE TO START THE GAME
# This file connects the GUI, Logic, and Image Processing.

import tkinter as tk
from gui.main import MYGUI 
from logic.logic_manager import CoordinateChecker, GameManager

if __name__ == "__main__":
    # 1. Start the Tkinter root
    root = tk.Tk()
    
    # 2. Initialize  GUI
    gui_app = MYGUI(root)
    
    # 3. Initialize  Logic Classes
    # We pass the Checker into the Manager
    math_engine = CoordinateChecker(threshold=30)
    game_logic = GameManager(math_engine)
    
    # 4. Attach the logic to the GUI (Integration)
    # This allows the GUI to talk to  logic
    gui_app.manager = game_logic
    
    # 5. Bind the click event to the logic
    # When the right canvas is clicked, it calls your validation logic
    gui_app.right_canvas.bind(
        "<Button-1>", 
        lambda e: gui_app.manager.validate_click(e.x, e.y)
    )

    root.mainloop()