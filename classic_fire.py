import pygame
import numpy as np

WIDTH, HEIGHT = 320, 240  # 火を滑らかにするため、少し解像度を下げるとリアルになります
SCALE = 2


def run_fire():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
    pygame.display.set_caption("Megademo Module: Hellfire (CompA-2026)")
    clock = pygame.time.Clock()
    surface = pygame.Surface((WIDTH, HEIGHT))

    # 火の強度を記録するバッファ (2D配列)
    fire_pixels = np.zeros((HEIGHT, WIDTH), dtype=np.float32)

    # 炎用カスタムパレットの作成 (インデックス0〜255をRGBに変換)
    palette = np.zeros((256, 3), dtype=np.uint8)
    for i in range(256):
        # 0-85: 黒から赤、86-170: 赤から黄、171-255: 黄から白
        if i < 85:
            palette[i] = [i * 3, 0, 0]
        elif i < 170:
            palette[i] = [255, (i - 85) * 3, 0]
        else:
            palette[i] = [255, 255, (i - 170) * 3]

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                running = False

        # 1. 最下行にランダムな「火種」を発生させる
        fire_pixels[-1, :] = np.random.randint(0, 256, WIDTH)

        # 2. 炎の拡散処理 (NumPyスライスで上下左右の平均を取りつつ、上にスクロール＆冷却)
        # 自分の上、左、右、2マス下の値を混ぜて減衰させる
        fire_pixels[:-1, 1:-1] = (
            (
                fire_pixels[1:, 1:-1] * 1.2  # 下（メインの熱源）
                + fire_pixels[1:, :-2] * 0.8  # 左下
                + fire_pixels[1:, 2:] * 0.8  # 右下
                + fire_pixels[:-1, 1:-1] * 0.2  # 自分自身
            )
            / 3.02
        )  # 3.0より少し大きくすることで、上にいくほど冷えて消える(冷却係数)

        # 3. 浮動小数点数をパレットインデックス(0-255)にキャスト
        indices = np.clip(fire_pixels, 0, 255).astype(np.uint8)

        # 4. パレットを適用してRGB配列に変換
        rgb = palette[indices]

        pygame.surfarray.blit_array(surface, rgb.swapaxes(0, 1))
        screen.blit(
            pygame.transform.scale(surface, (WIDTH * SCALE, HEIGHT * SCALE)), (0, 0)
        )
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    run_fire()
