import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class MYGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Spot the Difference Game")
        self.root.geometry("1000x700")
        self.root.configure(bg="#2C3E50") # Dark blue-ish background color

        # This will hold our game logic later (connected in main.py)
        self.manager = None 

        # Store image references
        self.left_img = None
        self.right_img = None

        # --- TOP TITLE ---
        self.title_label = tk.Label(
            root, text="Spot the Difference Game",
            font=("Arial", 24, "bold"), bg="#2C3E50", fg="white"
        )
        self.title_label.pack(pady=10)

        # --- BUTTONS AREA ---
        self.button_frame = tk.Frame(root, bg="#2C3E50")
        self.button_frame.pack(pady=10)

        # Button to pick an image
        self.load_btn = tk.Button(
            self.button_frame, text="Load Image",
            font=("Arial", 12, "bold"), bg="#1ABC9C", fg="white",
            padx=20, command=self.load_image 
        )
        self.load_btn.pack(side="left", padx=10)

        # Button to show all the answers
        self.reveal_btn = tk.Button(
            self.button_frame, text="Reveal Differences",
            font=("Arial", 12), bg="#E74C3C", fg="white",
            padx=20, command=self.reveal_all
        )
        self.reveal_btn.pack(side="left", padx=10)

        # Reset button
        self.reset_btn = tk.Button(
            self.button_frame,
            text="Reset",
            font=("Arial", 12, "bold"),
            bg="#3498DB",
            fg="white",
            padx=20,
            command=self.reset_game
        )
        self.reset_btn.pack(side="left", padx=10)

        # --- THE TWO IMAGES SIDE BY SIDE ---
        self.image_frame = tk.Frame(root, bg="#2C3E50")
        self.image_frame.pack(pady=10)

        # Left side (The normal image)
        self.left_canvas = tk.Canvas(self.image_frame, width=350, height=350, bg="#34495E")
        self.left_canvas.pack(side="left", padx=20)

        # Right side (The one we click on)
        self.right_canvas = tk.Canvas(self.image_frame, width=350, height=350, bg="#34495E")
        self.right_canvas.pack(side="right", padx=20)

        # --- STATS AT THE BOTTOM (Score & Mistakes) ---
        self.stats_frame = tk.Frame(root, bg="#2C3E50")
        self.stats_frame.pack(pady=10)

        self.label_remaining = tk.Label(
            self.stats_frame, text="Remaining: 5",
            font=("Arial", 14), bg="#2C3E50", fg="#F1C40F"
        )
        self.label_remaining.pack(side="left", padx=30)

        self.label_mistakes = tk.Label(
            self.stats_frame, text="Mistakes: 0/3",
            font=("Arial", 14), bg="#2C3E50", fg="#E67E22"
        )
        self.label_mistakes.pack(side="left", padx=30)

    # --- HELPER STUFF ---

    def draw_circle(self, x, y, color="red"):
        #This draws circles on both pictures when we find something
        for canvas in [self.left_canvas, self.right_canvas]:
            # Drawing a circle at the (x, y) coordinates
            canvas.create_oval(x-15, y-15, x+15, y+15, outline=color, width=3)

    def update_display(self, mistakes, remaining):
        #Just updates the text labels on the screen so we can see the score
        self.label_mistakes.config(text=f"Mistakes: {mistakes}/3")
        self.label_remaining.config(text=f"Remaining: {remaining}")

    def load_image(self):
        # Opens the file browser so we can pick a picture
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.bmp")])
        return file_path

    def reveal_all(self):
        #This is a placeholder, we'll code the reveal logic in main.py
        pass

    def reset_game(self):
        # Clear both canvases
        self.left_canvas.delete("all")
        self.right_canvas.delete("all")

        # Remove stored images
        self.left_img = None
        self.right_img = None

        # Reset labels
        self.label_remaining.config(text="Remaining: 5")
        self.label_mistakes.config(text="Mistakes: 0/3")