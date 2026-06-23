import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

WIDTH, HEIGHT = 320, 240
SCALE = 2


def run_fire():
    root = tk.Tk()
    root.title("Megademo Module: Hellfire (CompA-2026)")
    root.resizable(False, False)

    canvas = tk.Canvas(root, width=WIDTH * SCALE, height=HEIGHT * SCALE,
                       bg='black', highlightthickness=0)
    canvas.pack()

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

    def update():
        if not running[0]:
            return

        fire_pixels[-1, :] = np.random.randint(0, 256, WIDTH)
        fire_pixels[:-1, 1:-1] = (
            (
                fire_pixels[1:, 1:-1] * 1.2
                + fire_pixels[1:, :-2] * 0.8
                + fire_pixels[1:, 2:] * 0.8
                + fire_pixels[:-1, 1:-1] * 0.2
            )
            / 3.02
        )

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

    update()
    root.mainloop()


if __name__ == "__main__":
    run_fire()
