import pygame
import numpy as np

WIDTH, HEIGHT = 400, 300
SCALE = 2

def run_water_distortion():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
    pygame.display.set_caption("Megademo Module: Wave Displacement (CompA-2026)")
    clock = pygame.time.Clock()
    surface = pygame.Surface((WIDTH, HEIGHT))

    # ベースとなる静止背景（サイバーな縦縞ストライプ）を事前作成
    x = np.linspace(0, 4 * np.pi, WIDTH)
    y = np.linspace(0, 4 * np.pi, HEIGHT)
    xv, yv = np.meshgrid(x, y)
    
    # 縞模様ベースのRGB配列
    base_r = (np.sin(xv) * 37 + 38).astype(np.uint8)
    base_g = (np.cos(yv) * 37 + 37).astype(np.uint8)
    base_b = ((np.sin(xv + yv) * 0.5 + 0.5) * 255).astype(np.uint8)
    base_rgb = np.stack((base_r, base_g, base_b), axis=-1)

    # 座標参照用の標準インデックス
    x_indices = np.arange(WIDTH)
    y_indices = np.arange(HEIGHT)

    running = True
    t = 0.0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        t += 0.1

        # 各行(Y座標)ごとに、X座標をどれだけズラすかをsinで計算
        shift_x = (np.sin(y_indices[:, None] * 0.15 + t)*np.sin(x_indices[None, :]*0.46 + 1.34 * t) * 15).astype(np.int32)
        
        # 各列(X座標)ごとも縦にズラす
        shift_y = (np.cos(x_indices[None, :] * 0.05 + t * 1.2)*np.sin(x_indices[None, :]*0.2+ t*1.5) * 5).astype(np.int32)

        # 新しい参照インデックスの作成（画面外にはみ出さないようクリップ）
        new_x = np.clip(x_indices[None, :] + shift_x, 0, WIDTH - 1)
        new_y = np.clip(y_indices[:, None] + shift_y, 0, HEIGHT - 1)

        # NumPyの条件代入で、ピクセルを波形に沿って再配置（歪み発生）
        distorted_rgb = base_rgb[new_y, new_x]

        pygame.surfarray.blit_array(surface, distorted_rgb.swapaxes(0, 1))
        screen.blit(pygame.transform.scale(surface, (WIDTH * SCALE, HEIGHT * SCALE)), (0, 0))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    run_water_distortion()
