import pygame
import numpy as np
import random

WIDTH, HEIGHT = 320, 240  # 解像度は低めが一番綺麗に燃えます
SCALE = 2

def run_text_fire():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
    pygame.display.set_caption("Megademo Module: Burning Typography (CompA-2026)")
    clock = pygame.time.Clock()
    surface = pygame.Surface((WIDTH, HEIGHT))

    # フォントの初期化（レトロ感を出すため太めのシステムフォントを選択）
    font = pygame.font.SysFont("impact", 58, bold=False)
    
    # 燃やす文字列のリスト
    words = ["FIRE!", "BURN!", "Explosion!", "Comp-A", "MEGA!!", "DEMO", "PYGAME", "Splendid!!", "CooooL!", "HOT!HOT!"]

    # 火の強度バッファ
    fire_pixels = np.zeros((HEIGHT, WIDTH), dtype=np.float32)

    # 炎用カラーパレット (0=黒, 255=白)
    palette = np.zeros((256, 3), dtype=np.uint8)
    for i in range(256):
        if i < 85:
            palette[i] = [i * 3, 0, 0]
        elif i < 170:
            palette[i] = [255, (i - 85) * 3, 0]
        else:
            palette[i] = [255, 255, (i - 170) * 3]

    # タイマーイベントの設定 (3000ms = 3秒ごとに文字を投入)
    TEXT_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(TEXT_EVENT, 3000)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            
            # 3秒ごとの文字生成処理
            if event.type == TEXT_EVENT:
                word = random.choice(words)
                # 文字を白(255)でサーフェスに描画
                text_surface = font.render(word, True, (255, 255, 255))
                
                # 配置位置の計算：中央やや下
                tx = (WIDTH - text_surface.get_width()) // 2
                ty = (HEIGHT // 2) + 20 
                
                # 文字サーフェスから2D配列(255か0か)を取り出す
                text_array = pygame.surfarray.array2d(text_surface)
                # 描画範囲をスライスで指定
                tw, th = text_array.shape
                
                # 画面外にはみ出さないよう安全にバッファに「熱源」を上書き
                # text_arrayは(W, H)なので、fire_pixelsの(H, W)に合わせて転置(.T)して適応
                if tx + tw <= WIDTH and ty + th <= HEIGHT:
                    # 完全に上書きするか、+= で既存の火と混ぜる（255でクリップ）
                    mask = (text_array.T < 0)
                    fire_pixels[ty:ty+th, tx:tx+tw][mask] = 255.0

                # 以降はランダムなタイミングで文字が飛び出す
                pygame.time.set_timer(TEXT_EVENT, 3000+random.randint(0, 4000))

        # 1. 最下行にランダムな「基本火種」を供給し続ける
        fire_pixels[-1, :] = np.random.randint(0, 256, WIDTH)

        # 2. 炎の拡散・冷却処理（文字のドットもこのアルゴリズムで上にメラメラと流れる）
        fire_pixels[:-1, 1:-1] = (
            fire_pixels[1:, 1:-1] * 1.3 +  # 下からの熱
            fire_pixels[1:, :-2] * 0.7 +   # 左下からの熱
            fire_pixels[1:, 2:] * 0.7 +    # 右下からの熱
            fire_pixels[:-1, 1:-1] * 0.2   # 前フレームの残熱
        ) / 2.93  # 冷却係数

        # 3. カラーパレット適用
        indices = np.clip(fire_pixels, 0, 255).astype(np.uint8)
        rgb = palette[indices]

        # 4. 画面描画
        pygame.surfarray.blit_array(surface, rgb.swapaxes(0, 1))
        screen.blit(pygame.transform.scale(surface, (WIDTH * SCALE, HEIGHT * SCALE)), (0, 0))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    run_text_fire()
