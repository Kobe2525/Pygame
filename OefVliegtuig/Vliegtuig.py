import pygame
import sys
import os
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 1200, 900  # Increased screen size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("F-15 Flight")

# Load images
bg_path = os.path.join("IMG", "Background.jpg")
jet_path = os.path.join("IMG", "F-15-Fighter-Jet.png")
enemy_path = os.path.join("IMG", "E_plane.webp")
background = pygame.image.load(bg_path)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
jet = pygame.image.load(jet_path)
jet = pygame.transform.scale(jet, (120, 80))
enemy = pygame.image.load(enemy_path)
enemy = pygame.transform.scale(enemy, (100, 70))
enemy = pygame.transform.rotate(enemy, 180)  # Turn enemy 180 degrees

# Jet starting position
jet_x = WIDTH // 2 - jet.get_width() // 2
jet_y = HEIGHT - jet.get_height() - 30
jet_speed = 15

# Background scroll variables
bg_y1 = 0
bg_y2 = -HEIGHT
bg_scroll_speed = 4

# Bullet variables
bullets = []
bullet_speed = 10
bullet_width, bullet_height = 6, 18
bullet_color = (255, 255, 0)  # Yellow

# Enemy starting position and speed
enemy_x = random.randint(0, WIDTH - enemy.get_width())
enemy_y = -enemy.get_height()
enemy_speed = 5

# Score variable
score = 0

# Main game loop
clock = pygame.time.Clock()
running = True
game_over = False
while running:
    clock.tick(60)  # 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_x = jet_x + jet.get_width() // 2 - bullet_width // 2
                bullet_y = jet_y
                bullets.append([bullet_x, bullet_y])

    if not game_over:
        # Key handling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            jet_x -= jet_speed
        if keys[pygame.K_RIGHT]:
            jet_x += jet_speed

        # Keep jet within screen bounds
        jet_x = max(0, min(WIDTH - jet.get_width(), jet_x))

        # Scroll background
        bg_y1 += bg_scroll_speed
        bg_y2 += bg_scroll_speed

        if bg_y1 >= HEIGHT:
            bg_y1 = -HEIGHT
        if bg_y2 >= HEIGHT:
            bg_y2 = -HEIGHT

        # Move enemy
        enemy_y += enemy_speed

        # Move bullets
        for bullet in bullets:
            bullet[1] -= bullet_speed
        # Remove bullets that are off-screen
        bullets = [b for b in bullets if b[1] > -bullet_height]

        # Check for bullet-enemy collision
        enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy.get_width(), enemy.get_height())
        hit = False
        for bullet in bullets:
            bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_width, bullet_height)
            if enemy_rect.colliderect(bullet_rect):
                hit = True
                bullets.remove(bullet)
                break
        if hit:
            score += 1
            # Increase speed every 10 points
            if score % 10 == 0:
                enemy_speed += 1
                bg_scroll_speed += 1
                jet_speed += 1
            enemy_x = random.randint(0, WIDTH - enemy.get_width())
            enemy_y = -enemy.get_height()

        # Check for jet-enemy collision or enemy out of screen (lose)
        jet_rect = pygame.Rect(jet_x, jet_y, jet.get_width(), jet.get_height())
        if enemy_rect.colliderect(jet_rect) or enemy_y > HEIGHT:
            game_over = True

    # Draw everything
    screen.blit(background, (0, bg_y1))
    screen.blit(background, (0, bg_y2))
    screen.blit(jet, (jet_x, jet_y))
    screen.blit(enemy, (enemy_x, enemy_y))
    for bullet in bullets:
        pygame.draw.rect(screen, bullet_color, (bullet[0], bullet[1], bullet_width, bullet_height))

    # Draw score
    font = pygame.font.SysFont(None, 48)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

    if game_over:
        font = pygame.font.SysFont(None, 120)
        text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    pygame.display.flip()

pygame.quit()
sys.exit()