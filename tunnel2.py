import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

WIDTH, HEIGHT = 320, 240
SCALE = 2


def run_deform_tunnel():
    root = tk.Tk()
    root.title("Megademo Module: Texture Mapping Tunnel (CompA-2026)")
    root.resizable(False, False)

    canvas = tk.Canvas(root, width=WIDTH * SCALE, height=HEIGHT * SCALE,
                       bg='black', highlightthickness=0)
    canvas.pack()

    x = np.linspace(-1, 1, WIDTH)
    y = np.linspace(-1, 1, HEIGHT)
    xv, yv = np.meshgrid(x, y)

    r = np.sqrt(xv**2 + yv**2) + 0.001
    angle = np.arctan2(yv, xv)

    tex_u = (1.0 / r * 32).astype(np.int32) % 256
    tex_v = (((angle + np.pi) / (2 * np.pi)) * 256).astype(np.int32) % 256

    photo = [None]
    img_id = canvas.create_image(0, 0, anchor='nw')
    running = [True]
    t = [0]

    def update():
        if not running[0]:
            return

        t[0] += 2

        u_shifted = (tex_u + t[0]) % 256
        v_shifted = (tex_v + t[0] // 2) % 256

        texture_mask = ((u_shifted // 16) ^ (v_shifted // 16)) % 2 == 0

        brightness = np.clip(r * 2, 0, 1)

        r_ch = (texture_mask * 0   + (~texture_mask * 255) * brightness).astype(np.uint8)
        g_ch = (texture_mask * 128 + (~texture_mask * 0)   * brightness).astype(np.uint8)
        b_ch = (texture_mask * 255 + (~texture_mask * 128) * brightness).astype(np.uint8)

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
    run_deform_tunnel()
