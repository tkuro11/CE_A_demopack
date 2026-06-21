import pygame
import numpy as np

WIDTH, HEIGHT = 400, 300
SCALE = 2


def run_moire():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
    pygame.display.set_caption("Megademo Module: Moire Illusion (Comp-A 2026)")
    clock = pygame.time.Clock()
    surface = pygame.Surface((WIDTH, HEIGHT))

    x = np.linspace(-2, 2, WIDTH)
    y = np.linspace(-2, 2, HEIGHT)
    xv, yv = np.meshgrid(x, y)

    running = True
    t = 0.0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                running = False

        t += 0.03

        # レイヤー1: 回転するグリッド
        s, c = np.sin(t), np.cos(t)
        x1 = xv * c - yv * s
        y1 = xv * s + yv * c
        grid1 = (np.sin(x1 * 40) > 0) ^ (np.sin(y1 * 40) > 0)

        # レイヤー2: 歪む（拡大縮小する）グリッド
        z = np.sin(t * 1.5) * 15 + 16
        grid2 = (np.sin(xv * z) > 0) ^ (np.sin(yv * z) > 0)

        # 2つのグリッドを排他的論理和(XOR)で合成
        final_grid = grid1 ^ grid2

        # 白黒（またはレトロな緑と黒）にマッピング
        # 1のときは黄緑色(128, 255, 0)、0のときは黒(0, 0, 0)
        r_ch = (final_grid * 128).astype(np.uint8)
        g_ch = (final_grid * 255).astype(np.uint8)
        b_ch = np.zeros_like(r_ch)

        rgb = np.stack((r_ch, g_ch, b_ch), axis=-1)
        pygame.surfarray.blit_array(surface, rgb.swapaxes(0, 1))
        screen.blit(
            pygame.transform.scale(surface, (WIDTH * SCALE, HEIGHT * SCALE)), (0, 0)
        )
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    run_moire()
