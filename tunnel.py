import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

WIDTH, HEIGHT = 400, 300
SCALE = 2


def run_tunnel():
    root = tk.Tk()
    root.title("Megademo Module: Warp Tunnel (CompA-2026)")
    root.resizable(False, False)

    canvas = tk.Canvas(root, width=WIDTH * SCALE, height=HEIGHT * SCALE,
                       bg='black', highlightthickness=0)
    canvas.pack()

    x = np.linspace(-1, 1, WIDTH)
    y = np.linspace(-1, 1, HEIGHT)
    xv, yv = np.meshgrid(x, y)

    r = np.sqrt(xv**2 + yv**2) + 0.001
    angle = np.arctan2(yv, xv)

    photo = [None]
    img_id = canvas.create_image(0, 0, anchor='nw')
    running = [True]
    t = [0.0]

    def update():
        if not running[0]:
            return

        t[0] += 0.08

        v = np.sin(3.0 / r + t[0]) + np.sin(angle * 3.0 + t[0])

        r_ch = (np.sin(v * np.pi) * 127 + 128).astype(np.uint8)
        g_ch = (np.cos(v * np.pi) * 64 + 64).astype(np.uint8)
        b_ch = (np.sin(v * np.pi + np.pi / 2) * 127 + 128).astype(np.uint8)

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
    run_tunnel()
