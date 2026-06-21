import pygame
import numpy as np

WIDTH, HEIGHT = 400, 300
SCALE = 2


def run_scroller():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
    pygame.display.set_caption("Megademo Module: Sinusoidal Scroller (compA-2026)")
    clock = pygame.time.Clock()
    surface = pygame.Surface((WIDTH, HEIGHT))

    # フォントと流すテキスト
    font = pygame.font.SysFont("impact", 45)
    text_str = "*** DEMOSCENE REVIVAL in 'COMPUTER EXCICISE A' DEMOSCENE "
    text_str += "*** CODING IS ART...  MINSIMPLE EQUATIONS CREATE"
    text_str += "INFINITE COMPLEXITY... GREETINGS TO ALL STUDENTS!"

    # テキストをあらかじめ1枚の長い画像（サーフェス）としてレンダリング
    text_surf = font.render(text_str, False, (255, 255, 255))
    text_w, text_h = text_surf.get_size()
    text_array = pygame.surfarray.array2d(text_surf)  # 2D配列として取得

    scroll_x = 0
    t = 0.0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                running = False

        # 画面を黒でクリア（NumPy配列を0に）
        bg_array = np.zeros((HEIGHT, WIDTH), dtype=np.uint32)

        t += 0.1
        scroll_x += 2  # スクロール速度
        if scroll_x > text_w:
            scroll_x = 0

        # 1ピクセル（縦の列）ごとに処理
        for scr_x in range(WIDTH):
            # 長いテキスト配列のどこを読み込むか計算
            tex_x = (scroll_x + scr_x) % text_w

            # 【ここがミソ】列ごとにY座標をサイン波で上下にズラす！
            wave_y = int(
                (HEIGHT - text_h) / 2
                + np.sin(t + scr_x * 0.05) * 30 * np.sin(t * 0.9 + scr_x * 0.09)
            )

            # 画面内に収まる範囲で、縦1列のドットをコピー
            if 0 <= wave_y < HEIGHT - text_h:
                bg_array[wave_y : wave_y + text_h, scr_x] = text_array[tex_x,]

        # カラーサイクリングを乗せて虹色にする（オプション）
        # 単なる白黒の文字データを、サイン波のパレットで色付け
        r = ((bg_array > 0) * (np.sin(t) * 127 + 128)).astype(np.uint8)
        g = ((bg_array > 0) * (np.sin(t + 2) * 127 + 128)).astype(np.uint8)
        b = ((bg_array > 0) * (np.sin(t + 4) * 127 + 128)).astype(np.uint8)
        rgb = np.stack((r, g, b), axis=-1)

        pygame.surfarray.blit_array(surface, rgb.swapaxes(0, 1))
        screen.blit(
            pygame.transform.scale(surface, (WIDTH * SCALE, HEIGHT * SCALE)), (0, 0)
        )
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    run_scroller()
