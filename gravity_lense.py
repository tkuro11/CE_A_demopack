import pygame
import numpy as np

WIDTH, HEIGHT = 800, 600

def run_particles():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Educational Module: Gravity Attractor Chaos")
    clock = pygame.time.Clock()

    NUM_PARTICLES = 2000
    # 初期位置：画面中心付近にランダム配置
    pos = np.random.normal(loc=[WIDTH/2, HEIGHT/2], scale=50, size=(NUM_PARTICLES, 2))
    # 初期速度：中心の周りを回るように少し回転方向の速度を与える
    vel = np.random.normal(loc=[0, 0], scale=1.0, size=(NUM_PARTICLES, 2))
    # 中心に向かう直交ベクトルを作って軌道速度っぽくする
    to_center = pos - [WIDTH/2, HEIGHT/2]
    vel[:, 0] = -to_center[:, 1] * 0.02 + np.random.normal(0, 0.5, NUM_PARTICLES)
    vel[:, 1] =  to_center[:, 0] * 0.02 + np.random.normal(0, 0.5, NUM_PARTICLES)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        # トレール（残像）効果のための半透明黒塗り
        fade = pygame.Surface((WIDTH, HEIGHT))
        fade.set_alpha(20) # これが残像を生む
        fade.fill((0, 0, 0))
        screen.blit(fade, (0, 0))

        # 中心の重力源
        cx, cy = WIDTH / 2, HEIGHT / 2

        # ベクトル演算で全粒子の重力計算を一括処理！
        dx = cx - pos[:, 0]
        dy = cy - pos[:, 1]
        dist_sq = dx**2 + dy**2 + 500 # ゼロ除算・無限大防止の緩和項

        # 加速度 = G * M / dist_sq
        accel_magnitude = 50.0 / dist_sq
        ax = dx * accel_magnitude
        ay = dy * accel_magnitude

        # 速度と位置の更新 (単純な足し算)
        vel[:, 0] += ax
        vel[:, 1] += ay
        pos += vel

        # 描画 (速度が速い粒子ほど青〜白く光らせる)
        speed = np.sqrt(vel[:, 0]**2 + vel[:, 1]**2)
        for i in range(NUM_PARTICLES):
            x, y = int(pos[i, 0]), int(pos[i, 1])
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                # 速度に応じた色
                color_r = int(min(255, speed[i] * 30))
                color_g = int(min(255, speed[i] * 50))
                pygame.draw.circle(screen, (color_r, color_g, 255), (x, y), 1)

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    run_particles()
