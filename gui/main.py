import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class MYGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Spot the Difference Game")
        self.root.geometry("1000x650")
        self.root.configure(bg="#2C3E50")

        # ================= TITLE =================
        self.title_label = tk.Label(
            root, text="Spot the Difference Game",
            font=("Arial", 20, "bold"), bg="#2C3E50", fg="white"
        )
        self.title_label.pack(pady=10)

        # ================= BUTTON FRAME =================
        self.button_frame = tk.Frame(root, bg="#2C3E50")
        self.button_frame.pack(pady=10)

        # Load Button
        self.load_btn = tk.Button(
            self.button_frame, text="Load Image",
            font=("Arial", 14, "bold"), bg="#1ABC9C", fg="white",
            padx=10, pady=5, command=self.load_image
        )
        self.load_btn.pack(side="left", padx=10)

        # Reveal Button
        self.reveal_btn = tk.Button(
            self.button_frame, text="Reveal Differences",
            font=("Arial", 12), bg="#E74C3C", fg="white",
            padx=10, pady=5, command=self.reveal_differences
        )
        self.reveal_btn.pack(side="left", padx=10)

        # ================= IMAGE FRAME (NOW USING CANVAS) =================
        self.image_frame = tk.Frame(root, bg="#2C3E50")
        self.image_frame.pack(pady=20)

        # Original Image Canvas (Left)
        self.left_canvas = tk.Canvas(
            self.image_frame, width=350, height=350, 
            bg="#34495E", highlightthickness=0
        )
        self.left_canvas.pack(side="left", padx=20)

        # Modified Image Canvas (Right)
        self.right_canvas = tk.Canvas(
            self.image_frame, width=350, height=350, 
            bg="#34495E", highlightthickness=0
        )
        self.right_canvas.pack(side="right", padx=20)

        # ================= INFO =================
        self.remaining = 5
        self.mistakes = 0

        self.info_label = tk.Label(
            root, text=f"Remaining: {self.remaining} | Mistakes: {self.mistakes}",
            font=("Arial", 14, "bold"), bg="#2C3E50", fg="#F1C40F"
        )
        self.info_label.pack(pady=15)

    # ================= LOAD IMAGE =================
    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.png *.bmp")]
        )

        if file_path:
            # Open and force resize to 350x350 so coordinates ALWAYS match
            img = Image.open(file_path).resize((350, 350))
            self.tk_image = ImageTk.PhotoImage(img)

            # Clear old drawings/images
            self.left_canvas.delete("all")
            self.right_canvas.delete("all")

            # Place images on Canvases
            self.left_canvas.create_image(0, 0, anchor="nw", image=self.tk_image)
            self.right_canvas.create_image(0, 0, anchor="nw", image=self.tk_image)
            
            # Keep a reference to prevent garbage collection
            self.left_canvas.image = self.tk_image
            self.right_canvas.image = self.tk_image

    def reveal_differences(self):
        # Student C will override this in logic_manager.py
        pass

    def update_info(self):
        self.info_label.config(
            text=f"Remaining: {self.remaining} | Mistakes: {self.mistakes}"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = MYGUI(root)
    root.mainloop()