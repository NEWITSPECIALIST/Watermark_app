import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont

# Global
image_path = None

def upload_image():
    global image_path
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
    )
    if file_path:
        image_path = file_path
        status_label.config(text=f"Image uploaded: {file_path.split('/')[-1]}")

def apply_watermark():
    global image_path
    if not image_path:
        messagebox.showerror("Error", "Please upload an image first!")
        return

    try:
        # Open image
        image = Image.open(image_path).convert("RGBA")

        # Transparent layer
        watermark = Image.new("RGBA", image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark)

        # Font
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except:
            font = ImageFont.load_default()

        # Text setup
        text = watermark_text.get()
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        width, height = image.size
        x = (width - text_width) // 2
        y = (height - text_height) // 2

        # Draw watermark
        draw.rectangle(
            [x - 10, y - 10, x + text_width + 10, y + text_height + 10],
            fill=(0, 0, 0, 128)
        )
        draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))

        # Merge layers
        watermarked = Image.alpha_composite(image, watermark)
        watermarked_rgb = watermarked.convert("RGB")

        # Save
        save_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")]
        )
        if save_path:
            watermarked_rgb.save(save_path)
            status_label.config(text="Watermark applied and saved!")
            messagebox.showinfo("Saved", f"Image saved to:\n{save_path}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


# --- GUI ---
root = tk.Tk()
root.title("Watermark App")
root.geometry("400x300")

watermark_text = tk.StringVar(value="Your Watermark")

# Upload Button
tk.Button(root, text="Upload Image", command=upload_image).pack(pady=20)

# Watermark Entry
tk.Label(root, text="Watermark Text:").pack()
tk.Entry(root, textvariable=watermark_text, width=30).pack(pady=10)

# Apply Button
tk.Button(root, text="Apply Watermark", command=apply_watermark).pack(pady=20)

# Status Label
status_label = tk.Label(root, text="")
status_label.pack(pady=10)

root.mainloop()