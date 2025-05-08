import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter, ImageOps
import os

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Image Editor")
        self.root.geometry("800x600")

        self.image_path = None
        self.original_image = None
        self.edited_image = None

        self.setup_ui()

    def setup_ui(self):
        self.canvas = tk.Canvas(self.root, bg="gray")
        self.canvas.pack(fill="both", expand=True)

        toolbar = tk.Frame(self.root, bg="black")
        toolbar.pack(fill="x")

        tk.Button(toolbar, text="Load Image", command=self.load_image).pack(side="left")
        tk.Button(toolbar, text="Grayscale", command=self.apply_grayscale).pack(side="left")
        tk.Button(toolbar, text="Blur", command=self.apply_blur).pack(side="left")
        tk.Button(toolbar, text="Resize 200x200", command=self.resize_image).pack(side="left")
        tk.Button(toolbar, text="Save Image", command=self.save_image).pack(side="left")

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if not file_path:
            return

        self.image_path = file_path
        self.original_image = Image.open(file_path)
        self.edited_image = self.original_image.copy()
        self.display_image(self.edited_image)

    def display_image(self, img):
        img.thumbnail((self.root.winfo_width(), self.root.winfo_height()))
        self.tk_image = ImageTk.PhotoImage(img)
        self.canvas.create_image(self.root.winfo_width() // 2, self.root.winfo_height() // 2, image=self.tk_image, anchor="center")

    def apply_grayscale(self):
        if self.edited_image:
            self.edited_image = ImageOps.grayscale(self.edited_image)
            self.display_image(self.edited_image)

    def apply_blur(self):
        if self.edited_image:
            self.edited_image = self.edited_image.filter(ImageFilter.BLUR)
            self.display_image(self.edited_image)

    def resize_image(self):
        if self.edited_image:
            self.edited_image = self.edited_image.resize((200, 200))
            self.display_image(self.edited_image)

    def save_image(self):
        if self.edited_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                self.edited_image.save(file_path)
                messagebox.showinfo("Saved", "Image saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()
