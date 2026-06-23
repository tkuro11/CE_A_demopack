import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import numpy as np
import random
import os

WIDTH, HEIGHT = 320, 240
SCALE = 2

FONT_PATHS = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/System/Library/Fonts/SFNS.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]


def load_font(size):
    for path in FONT_PATHS:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def run_text_fire():
    root = tk.Tk()
    root.title("Megademo Module: Burning Typography (CompA-2026)")
    root.resizable(False, False)

    canvas = tk.Canvas(root, width=WIDTH * SCALE, height=HEIGHT * SCALE,
                       bg='black', highlightthickness=0)
    canvas.pack()

    font = load_font(58)

    words = ["FIRE!", "BURN!", "Explosion!", "Comp-A", "MEGA!!", "DEMO",
             "TKINTER", "Splendid!!", "CooooL!", "HOT!HOT!"]

    fire_pixels = np.zeros((HEIGHT, WIDTH), dtype=np.float32)

    palette = np.zeros((256, 3), dtype=np.uint8)
    for i in range(256):
        if i < 85:
            palette[i] = [i * 3, 0, 0]
        elif i < 170:
            palette[i] = [255, (i - 85) * 3, 0]
        else:
            palette[i] = [255, 255, (i - 170) * 3]

    photo = [None]
    img_id = canvas.create_image(0, 0, anchor='nw')
    running = [True]

    def drop_word():
        if not running[0]:
            return
        word = random.choice(words)

        # Render word to a grayscale PIL image sized just large enough
        dummy = ImageDraw.Draw(Image.new('L', (1, 1)))
        try:
            bbox = dummy.textbbox((0, 0), word, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            ox, oy = -bbox[0], -bbox[1]
        except AttributeError:
            tw, th = font.getsize(word)
            ox, oy = 0, 0

        text_img = Image.new('L', (tw, th), 0)
        ImageDraw.Draw(text_img).text((ox, oy), word, fill=255, font=font)
        text_arr = np.array(text_img)  # (th, tw)

        tx = (WIDTH - tw) // 2
        ty = (HEIGHT // 2) + 20

        if 0 <= tx and tx + tw <= WIDTH and 0 <= ty and ty + th <= HEIGHT:
            mask = text_arr > 0
            fire_pixels[ty:ty + th, tx:tx + tw][mask] = 255.0

        root.after(3000 + random.randint(0, 4000), drop_word)

    def update():
        if not running[0]:
            return

        fire_pixels[-1, :] = np.random.randint(0, 256, WIDTH)
        fire_pixels[:-1, 1:-1] = (
            fire_pixels[1:, 1:-1] * 1.3
            + fire_pixels[1:, :-2] * 0.7
            + fire_pixels[1:, 2:] * 0.7
            + fire_pixels[:-1, 1:-1] * 0.2
        ) / 2.93

        indices = np.clip(fire_pixels, 0, 255).astype(np.uint8)
        rgb = palette[indices]

        img = Image.fromarray(rgb, 'RGB')
        img = img.resize((WIDTH * SCALE, HEIGHT * SCALE), Image.NEAREST)
        photo[0] = ImageTk.PhotoImage(img)
        canvas.itemconfig(img_id, image=photo[0])

        root.after(16, update)

    def on_key(event):
        if event.keysym == 'Escape':
            running[0] = False
            root.destroy()

    root.bind('<Key>', on_key)
    root.protocol("WM_DELETE_WINDOW", root.destroy)

    root.after(3000, drop_word)
    update()
    root.mainloop()


if __name__ == "__main__":
    run_text_fire()
