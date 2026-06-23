import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import numpy as np
import os

WIDTH, HEIGHT = 400, 300
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


def run_scroller():
    root = tk.Tk()
    root.title("Megademo Module: Sinusoidal Scroller (compA-2026)")
    root.resizable(False, False)

    canvas = tk.Canvas(root, width=WIDTH * SCALE, height=HEIGHT * SCALE,
                       bg='black', highlightthickness=0)
    canvas.pack()

    font = load_font(45)
    text_str = "*** DEMOSCENE REVIVAL in 'COMPUTER EXCISE A' DEMOSCENE "
    text_str += "*** CODING IS ART...  MINSIMPLE EQUATIONS CREATE"
    text_str += "INFINITE COMPLEXITY... GREETINGS TO ALL STUDENTS!"

    # Render full text string into a single wide grayscale image
    dummy_draw = ImageDraw.Draw(Image.new('L', (1, 1)))
    try:
        bbox = dummy_draw.textbbox((0, 0), text_str, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        ox, oy = -bbox[0], -bbox[1]
    except AttributeError:
        text_w, text_h = font.getsize(text_str)
        ox, oy = 0, 0

    text_img = Image.new('L', (text_w, text_h), 0)
    ImageDraw.Draw(text_img).text((ox, oy), text_str, fill=255, font=font)
    # shape: (text_h, text_w) — access column tex_x as text_array[:, tex_x]
    text_array = np.array(text_img)

    photo = [None]
    img_id = canvas.create_image(0, 0, anchor='nw')
    running = [True]
    scroll_x = [0]
    t = [0.0]

    def update():
        if not running[0]:
            return

        bg_array = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)

        t[0] += 0.1
        scroll_x[0] += 2
        if scroll_x[0] > text_w:
            scroll_x[0] = 0

        for scr_x in range(WIDTH):
            tex_x = (scroll_x[0] + scr_x) % text_w
            wave_y = int(
                (HEIGHT - text_h) / 2
                + np.sin(t[0] + scr_x * 0.05) * 30 * np.sin(t[0] * 0.9 + scr_x * 0.09)
            )
            if 0 <= wave_y < HEIGHT - text_h:
                bg_array[wave_y: wave_y + text_h, scr_x] = text_array[:, tex_x]

        r = ((bg_array > 0) * (np.sin(t[0]) * 127 + 128)).astype(np.uint8)
        g = ((bg_array > 0) * (np.sin(t[0] + 2) * 127 + 128)).astype(np.uint8)
        b = ((bg_array > 0) * (np.sin(t[0] + 4) * 127 + 128)).astype(np.uint8)
        rgb = np.stack((r, g, b), axis=-1)

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

    update()
    root.mainloop()


if __name__ == "__main__":
    run_scroller()
