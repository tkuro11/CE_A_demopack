import pygame
import numpy as np

WIDTH, HEIGHT = 320, 240
SCALE = 2

def run_deform_tunnel():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
    pygame.display.set_caption("Megademo Module: Texture Mapping Tunnel (CompA-2026)")
    clock = pygame.time.Clock()
    surface = pygame.Surface((WIDTH, HEIGHT))

    # --- 事前計算 (ルックアップテーブルの作成) ---
    x = np.linspace(-1, 1, WIDTH)
    y = np.linspace(-1, 1, HEIGHT)
    xv, yv = np.meshgrid(x, y)
    
    # 極座標の距離(r)と角度(angle)を計算
    r = np.sqrt(xv**2 + yv**2) + 0.001
    angle = np.arctan2(yv, xv)

    # 距離を反転させて奥行き(U)にし、角度を(V)にするテクスチャ座標マップ
    # 256x256のテクスチャにマッピングするために整数化しておく
    tex_u = (1.0 / r * 32).astype(np.int32) % 256
    tex_v = (((angle + np.pi) / (2 * np.pi)) * 256).astype(np.int32) % 256

    running = True
    t = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        t += 2  # アニメーション速度

        # 動的にテクスチャの参照位置をずらす（スクロール＝前進と回転）
        u_shifted = (tex_u + t) % 256
        v_shifted = (tex_v + t // 2) % 256

        # ビット演算子(XOR)だけでチェッカーボードテクスチャをその場で生成！
        # 16マス×16マスの市松模様
        texture_mask = ((u_shifted // 16) ^ (v_shifted // 16)) % 2 == 0

        # 色を適用 (奥に行くほど暗くするフォグ効果も追加)
        brightness = np.clip(r * 2, 0, 1)  # 中心(奥)ほどrが小さいので暗くなる
        
        r_ch = (texture_mask * 0   + (~texture_mask * 255) * brightness).astype(np.uint8)
        g_ch = (texture_mask * 128 + (~texture_mask * 0)   * brightness).astype(np.uint8)
        b_ch = (texture_mask * 255 + (~texture_mask * 128) * brightness).astype(np.uint8)

        rgb = np.stack((r_ch, g_ch, b_ch), axis=-1)
        pygame.surfarray.blit_array(surface, rgb.swapaxes(0, 1))
        screen.blit(pygame.transform.scale(surface, (WIDTH * SCALE, HEIGHT * SCALE)), (0, 0))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    run_deform_tunnel()
