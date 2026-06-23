import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

WIDTH, HEIGHT = 400, 300
SCALE = 2


def run_moire():
    root = tk.Tk()
    root.title("Megademo Module: Moire Illusion (Comp-A 2026)")
    root.resizable(False, False)

    canvas = tk.Canvas(root, width=WIDTH * SCALE, height=HEIGHT * SCALE,
                       bg='black', highlightthickness=0)
    canvas.pack()

    x = np.linspace(-2, 2, WIDTH)
    y = np.linspace(-2, 2, HEIGHT)
    xv, yv = np.meshgrid(x, y)

    photo = [None]
    img_id = canvas.create_image(0, 0, anchor='nw')
    running = [True]
    t = [0.0]

    def update():
        if not running[0]:
            return

        t[0] += 0.03

        s, c = np.sin(t[0]), np.cos(t[0])
        x1 = xv * c - yv * s
        y1 = xv * s + yv * c
        grid1 = (np.sin(x1 * 40) > 0) ^ (np.sin(y1 * 40) > 0)

        z = np.sin(t[0] * 1.5) * 15 + 16
        grid2 = (np.sin(xv * z) > 0) ^ (np.sin(yv * z) > 0)

        final_grid = grid1 ^ grid2

        r_ch = (final_grid * 128).astype(np.uint8)
        g_ch = (final_grid * 255).astype(np.uint8)
        b_ch = np.zeros_like(r_ch)

        rgb = np.stack((r_ch, g_ch, b_ch), axis=-1)

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
    run_moire()
