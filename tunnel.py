import pygame
import numpy as np

WIDTH, HEIGHT = 400, 300
SCALE = 2

def run_tunnel():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
    pygame.display.set_caption("Megademo Module: Warp Tunnel (CompA-2026)")
    clock = pygame.time.Clock()
    surface = pygame.Surface((WIDTH, HEIGHT))

    # 中心からの相対座標グリッド
    x = np.linspace(-1, 1, WIDTH)
    y = np.linspace(-1, 1, HEIGHT)
    xv, yv = np.meshgrid(x, y)

    # 極座標への変換: 距離 r と 角度 angle
    r = np.sqrt(xv**2 + yv**2) + 0.001  # ゼロ除算防止
    angle = np.arctan2(yv, xv)

    running = True
    t = 0.0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        t += 0.08  # 前進スピード

        # トンネルの計算: 1/r で奥に行くほど高密度に、angle * 3 で3条の渦に
        v = np.sin(3.0 / r + t) + np.sin(angle * 3.0 + t)

        # カラーマッピング (ディープパープルからサイバーシアンへのグラデーション)
        r_ch = (np.sin(v * np.pi) * 127 + 128).astype(np.uint8)
        g_ch = (np.cos(v * np.pi) * 64 + 64).astype(np.uint8)
        b_ch = (np.sin(v * np.pi + np.pi/2) * 127 + 128).astype(np.uint8)

        rgb = np.stack((r_ch, g_ch, b_ch), axis=-1)
        pygame.surfarray.blit_array(surface, rgb.swapaxes(0, 1))
        screen.blit(pygame.transform.scale(surface, (WIDTH * SCALE, HEIGHT * SCALE)), (0, 0))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    run_tunnel()
