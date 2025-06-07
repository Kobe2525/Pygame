import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [
    (255, 255, 255),  # White
    (255, 0, 0),      # Red
    (0, 255, 0),      # Green
    (0, 0, 255),      # Blue
    (255, 255, 0),    # Yellow
    (0, 255, 255),    # Cyan
    (255, 0, 255),    # Magenta
    (255, 128, 0),    # Orange
]

# Paddle settings
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 7

# Ball settings
BALL_SIZE = 20
BALL_SPEED_X, BALL_SPEED_Y = 5, 5

# Score
font = pygame.font.SysFont("Arial", 36)

def draw(win, paddles, ball, scores, color):
    win.fill(BLACK)
    pygame.draw.rect(win, color, paddles[0])
    pygame.draw.rect(win, color, paddles[1])
    pygame.draw.ellipse(win, color, ball)
    pygame.draw.aaline(win, color, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    score_text = font.render(f"{scores[0]}   {scores[1]}", True, color)
    win.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
    pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    left_paddle = pygame.Rect(30, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = pygame.Rect(WIDTH - 40, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
    ball_vel = [BALL_SPEED_X, BALL_SPEED_Y]
    scores = [0, 0]
    color_index = 0

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z] and left_paddle.top > 0:
            left_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
            left_paddle.y += PADDLE_SPEED
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
            right_paddle.y += PADDLE_SPEED

        # Ball movement
        ball.x += ball_vel[0]
        ball.y += ball_vel[1]

        # Collision with top/bottom
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_vel[1] = -ball_vel[1]

        # Collision with paddles
        if ball.colliderect(left_paddle) and ball_vel[0] < 0:
            ball_vel[0] = -ball_vel[0]
        if ball.colliderect(right_paddle) and ball_vel[0] > 0:
            ball_vel[0] = -ball_vel[0]

        # Score
        scored = False
        if ball.left <= 0:
            scores[1] += 1
            ball.center = (WIDTH // 2, HEIGHT // 2)
            ball_vel = [-BALL_SPEED_X, BALL_SPEED_Y]
            scored = True
        if ball.right >= WIDTH:
            scores[0] += 1
            ball.center = (WIDTH // 2, HEIGHT // 2)
            ball_vel = [BALL_SPEED_X, BALL_SPEED_Y]
            scored = True

        if scored:
            color_index = (color_index + 1) % len(COLORS)

        draw(WIN, [left_paddle, right_paddle], ball, scores, COLORS[color_index])

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()