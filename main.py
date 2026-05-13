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
    """
    Cleans up old game state and handles picking a new photo.
    """
    # 1. CLEANUP: Wipe the canvases so old red/blue circles disappear
    gui.left_canvas.delete("all")
    gui.right_canvas.delete("all")
    
    # 2. Pick the photo via GUI
    path = gui.load_image()
    if not path:
        return

    # 3. Process the image (Student B's logic)
    # Resizing to match the canvas dimensions
    original_pil = Image.open(path).resize((350, 350))
    modified_pil, coords = processor.create_modified_image(original_pil)

    # 4. Convert and keep references so images don't disappear (Garbage Collection)
    gui.tk_orig = ImageTk.PhotoImage(original_pil)
    gui.tk_mod = ImageTk.PhotoImage(modified_pil)
    
    # 5. Display images on the canvases
    gui.left_canvas.create_image(0, 0, anchor="nw", image=gui.tk_orig)
    gui.right_canvas.create_image(0, 0, anchor="nw", image=gui.tk_mod)

    # 6. Load coordinates into the Game Manager
    # Add 20 to x and y to target the center of the 40x40 modifications
    target_points = [(c[0] + 20, c[1] + 20) for c in coords]
    gui.manager.load_game_data(target_points)
    
    # 7. Reset the GUI display text
    gui.update_display(gui.manager.mistakes, 5)

def click_handler(event):
    """
    Handles user clicks on the modified image.
    """
    # Don't do anything if they have already lost
    if gui.manager.mistakes >= 3:
        return

    # Check the click using the logic manager
    result, point = gui.manager.validate_click(event.x, event.y)

    if result == "HIT":
        gui.draw_circle(point[0], point[1], "red")
    
    # Update score and mistakes display
    gui.update_display(gui.manager.mistakes, 5 - len(gui.manager.found_list))

    # --- VICTORY CONDITION ---
    if len(gui.manager.found_list) == 5:
        # Ask to play again immediately
        play_again = messagebox.askyesno("Victory!", 
            "Awesome! You found all 5 differences.\n\nWould you like to play again with a new image?")
        if play_again:
            start_game()
        else:
            root.destroy()

    # --- FAILURE CONDITION ---
    elif gui.manager.mistakes >= 3:
        messagebox.showwarning("Game Over", 
            "3 mistakes! Click 'Reveal Differences' to see the ones you missed.")

def reveal_logic():
    """
    Draws blue circles for unfound differences and prompts for a restart.
    """
    # 1. Draw blue circles for any target not yet found
    for target in gui.manager.targets:
        if target not in gui.manager.found_list:
            gui.draw_circle(target[0], target[1], "blue")
    
    # 2. Update the display so the circles appear immediately
    root.update_idletasks() 

    # 3. Wait 3 seconds (3000 milliseconds) then show the popup
    # We use root.after(delay_ms, function_to_run)
    root.after(1000, ask_to_restart)

def ask_to_restart():
    """
    The popup function called after the delay.
    """
    play_again = messagebox.askyesno("Revealed", 
        "The missing differences are marked in blue.\n\nWould you like to start a new game?")
    if play_again:
        start_game()
    else:
        root.destroy()
        
if __name__ == "__main__":
    # Standard Tkinter setup
    root = tk.Tk()
    root.title("Spot the Difference - Group Project")
    
    # Initialize components
    gui = MYGUI(root)
    processor = ImageProcessor()
    
    # Setup Logic Engines
    checker = CoordinateChecker(threshold=30)
    gui.manager = GameManager(checker)

    # Optional: Log status for debugging/polymorphism demonstration
    print(checker.get_status())
    print(gui.manager.get_status())

    # Link Buttons and Canvas Events
    gui.load_btn.config(command=start_game)
    gui.reveal_btn.config(command=reveal_logic)
    gui.right_canvas.bind("<Button-1>", click_handler)

    root.mainloop()