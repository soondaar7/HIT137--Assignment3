# main.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Importing from our organized folders
from gui.main import MYGUI
from core.math_engine import CoordinateChecker
from core.game_manager import GameManager
from logic.image_processor import ImageProcessor

def start_game():
    """ This function handles picking the photo and starting the round """
    path = gui.load_image()
    if not path:
        return

    # 1. Use Student B's code to process the image
    original_pil = Image.open(path).resize((350, 350))
    modified_pil, coords = processor.create_modified_image(original_pil)

    # 2. Keep a reference so the images don't disappear
    gui.tk_orig = ImageTk.PhotoImage(original_pil)
    gui.tk_mod = ImageTk.PhotoImage(modified_pil)
    
    # 3. Show them in the GUI
    gui.left_canvas.create_image(0, 0, anchor="nw", image=gui.tk_orig)
    gui.right_canvas.create_image(0, 0, anchor="nw", image=gui.tk_mod)

    # 4. Give the coordinates to our (Barsha's) logic
    # We add 20 to x and y to get the center of the 40x40 square
    target_points = [(c[0] + 20, c[1] + 20) for c in coords]
    gui.manager.load_game_data(target_points)
    
    # 5. Reset the display text
    gui.update_display(gui.manager.mistakes, 5)

def click_handler(event):
    """ This runs every time someone clicks the right-side image """
    # Don't do anything if they already lost
    if gui.manager.mistakes >= 3:
        return

    # Check the click using our logic manager
    result, point = gui.manager.validate_click(event.x, event.y)

    if result == "HIT":
        gui.draw_circle(point[0], point[1], "red")
    
    # Update the score and mistakes on the screen
    gui.update_display(gui.manager.mistakes, 5 - len(gui.manager.found_list))

    # Check if the game is over or if they won
    if len(gui.manager.found_list) == 5:
        messagebox.showinfo("Victory!", "Awesome! You found all 5 differences.")
    elif gui.manager.mistakes >= 3:
        messagebox.showwarning("Game Over", "3 mistakes! Click 'Reveal' to see the ones you missed.")

def reveal_logic():
    """ Shows blue circles for any differences they didn't find """
    for target in gui.manager.targets:
        if target not in gui.manager.found_list:
            gui.draw_circle(target[0], target[1], "blue")

if __name__ == "__main__":
    # Standard Tkinter setup
    root = tk.Tk()
    
    # --- Initialize the different parts of the project ---
    gui = MYGUI(root)
    processor = ImageProcessor()
    
    # Setup our logic engine
    checker = CoordinateChecker(threshold=30)
    gui.manager = GameManager(checker)

    # --- SHOWING OFF POLYMORPHISM (For the Teacher) ---
    print(checker.get_status()) # Prints MathEngine status
    print(gui.manager.get_status()) # Prints Referee status

    # --- Linking buttons and clicks ---
    gui.load_btn.config(command=start_game)
    gui.reveal_btn.config(command=reveal_logic)
    gui.right_canvas.bind("<Button-1>", click_handler)

    root.mainloop()