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
            root,
            text="Spot the Difference Game",
            font=("Arial", 20, "bold"),
            bg="#2C3E50",
            fg="white"
        )
        self.title_label.pack(pady=10)

        # ================= BUTTON FRAME =================
        self.button_frame = tk.Frame(root, bg="#2C3E50")
        self.button_frame.pack(pady=10)

        # Load Button
        self.load_btn = tk.Button(
            self.button_frame,
            text="Load Image",
            font=("Arial", 14, "bold"),
            bg="#1ABC9C",
            fg="white",
            padx=10,
            pady=5,
            command=self.load_image
        )
        self.load_btn.pack(side="left", padx=10)

        # Hover effects
        self.load_btn.bind("<Enter>", lambda e: self.load_btn.config(bg="#16A085"))
        self.load_btn.bind("<Leave>", lambda e: self.load_btn.config(bg="#1ABC9C"))

        # Reveal Button
        self.reveal_btn = tk.Button(
            self.button_frame,
            text="Reveal Differences",
            font=("Arial", 12),
            bg="#E74C3C",
            fg="white",
            padx=10,
            pady=5,
            command=self.reveal_differences
        )
        self.reveal_btn.pack(side="left", padx=10)

        self.reveal_btn.bind("<Enter>", lambda e: self.reveal_btn.config(bg="#C0392B"))
        self.reveal_btn.bind("<Leave>", lambda e: self.reveal_btn.config(bg="#E74C3C"))

        # ================= IMAGE FRAME =================
        self.image_frame = tk.Frame(root, bg="#2C3E50")
        self.image_frame.pack(pady=20)

        # Original Image Label
        self.left_label = tk.Label(
            self.image_frame,
            text="Original Image",
            bg="#34495E",
            fg="white",
            font=("Arial", 12),
            width=40,
            height=20
        )
        self.left_label.pack(side="left", padx=20)

        # Modified Image Label
        self.right_label = tk.Label(
            self.image_frame,
            text="Modified Image",
            bg="#34495E",
            fg="white",
            font=("Arial", 12),
            width=40,
            height=20
        )
        self.right_label.pack(side="right", padx=20)

        # ================= INFO =================
        self.remaining = 5
        self.mistakes = 0

        self.info_label = tk.Label(
            root,
            text=f"Remaining: {self.remaining} | Mistakes: {self.mistakes}",
            font=("Arial", 14, "bold"),
            bg="#2C3E50",
            fg="#F1C40F"
        )
        self.info_label.pack(pady=15)

    # ================= LOAD IMAGE =================
   
    def load_image(self):
        file_path = filedialog.askopenfilename()

        if file_path:
            img = Image.open(file_path)
            img = img.resize((350, 350))

            self.tk_image = ImageTk.PhotoImage(img)

            # Show same image on both sides (for now)
            self.left_label.config(image=self.tk_image, text="")
            self.right_label.config(image=self.tk_image, text="")

            self.left_label.image = self.tk_image
            self.right_label.image = self.tk_image

    # ================= REVEAL BUTTON =================
    def reveal_differences(self):
        print("Reveal clicked (connect OpenCV later)")

    # ================= UPDATE INFO =================
    def update_info(self):
        self.info_label.config(
            text=f"Remaining: {self.remaining} | Mistakes: {self.mistakes}"
        )

