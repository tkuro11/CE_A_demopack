import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

WIDTH, HEIGHT = 400, 300
SCALE = 2


def run_water_distortion():
    root = tk.Tk()
    root.title("Megademo Module: Wave Displacement (CompA-2026)")
    root.resizable(False, False)

    canvas = tk.Canvas(root, width=WIDTH * SCALE, height=HEIGHT * SCALE,
                       bg='black', highlightthickness=0)
    canvas.pack()

    x = np.linspace(0, 4 * np.pi, WIDTH)
    y = np.linspace(0, 4 * np.pi, HEIGHT)
    xv, yv = np.meshgrid(x, y)

    base_r = (np.sin(xv) * 37 + 38).astype(np.uint8)
    base_g = (np.cos(yv) * 37 + 37).astype(np.uint8)
    base_b = ((np.sin(xv + yv) * 0.5 + 0.5) * 255).astype(np.uint8)
    base_rgb = np.stack((base_r, base_g, base_b), axis=-1)

    x_indices = np.arange(WIDTH)
    y_indices = np.arange(HEIGHT)

    photo = [None]
    img_id = canvas.create_image(0, 0, anchor='nw')
    running = [True]
    t = [0.0]

    def update():
        if not running[0]:
            return

        t[0] += 0.1

        shift_x = (np.sin(y_indices[:, None] * 0.15 + t[0]) * np.sin(x_indices[None, :] * 0.46 + 1.34 * t[0]) * 15).astype(np.int32)
        shift_y = (np.cos(x_indices[None, :] * 0.05 + t[0] * 1.2) * np.sin(x_indices[None, :] * 0.2 + t[0] * 1.5) * 5).astype(np.int32)

        new_x = np.clip(x_indices[None, :] + shift_x, 0, WIDTH - 1)
        new_y = np.clip(y_indices[:, None] + shift_y, 0, HEIGHT - 1)

        distorted_rgb = base_rgb[new_y, new_x]

        img = Image.fromarray(distorted_rgb, 'RGB')
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
    run_water_distortion()
