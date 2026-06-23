import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

WIDTH, HEIGHT = 800, 600


def run_particles():
    root = tk.Tk()
    root.title("Educational Module: Gravity Attractor Chaos")
    root.resizable(False, False)

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT,
                       bg='black', highlightthickness=0)
    canvas.pack()

    NUM_PARTICLES = 2000
    pos = np.random.normal(loc=[WIDTH / 2, HEIGHT / 2], scale=50, size=(NUM_PARTICLES, 2))
    vel = np.random.normal(loc=[0, 0], scale=1.0, size=(NUM_PARTICLES, 2))
    to_center = pos - [WIDTH / 2, HEIGHT / 2]
    vel[:, 0] = -to_center[:, 1] * 0.02 + np.random.normal(0, 0.5, NUM_PARTICLES)
    vel[:, 1] =  to_center[:, 0] * 0.02 + np.random.normal(0, 0.5, NUM_PARTICLES)

    # Persistent float buffer for trail effect
    screen_arr = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float32)
    fade_factor = 1.0 - 20.0 / 255.0

    photo = [None]
    img_id = canvas.create_image(0, 0, anchor='nw')
    running = [True]

    def update():
        if not running[0]:
            return

        # Trail fade (equivalent to blitting a semi-transparent black surface)
        screen_arr[:] *= fade_factor

        cx, cy = WIDTH / 2, HEIGHT / 2
        dx = cx - pos[:, 0]
        dy = cy - pos[:, 1]
        dist_sq = dx**2 + dy**2 + 500

        accel_magnitude = 50.0 / dist_sq
        ax = dx * accel_magnitude
        ay = dy * accel_magnitude

        vel[:, 0] += ax
        vel[:, 1] += ay
        pos[:] += vel

        speed = np.sqrt(vel[:, 0]**2 + vel[:, 1]**2)
        color_r = np.clip(speed * 30, 0, 255)
        color_g = np.clip(speed * 50, 0, 255)

        xi = pos[:, 0].astype(np.int32)
        yi = pos[:, 1].astype(np.int32)
        valid = (xi >= 0) & (xi < WIDTH) & (yi >= 0) & (yi < HEIGHT)

        xv = xi[valid]
        yv = yi[valid]
        screen_arr[yv, xv, 0] = np.minimum(255, screen_arr[yv, xv, 0] + color_r[valid])
        screen_arr[yv, xv, 1] = np.minimum(255, screen_arr[yv, xv, 1] + color_g[valid])
        screen_arr[yv, xv, 2] = 255

        img = Image.fromarray(screen_arr.astype(np.uint8), 'RGB')
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
    run_particles()
