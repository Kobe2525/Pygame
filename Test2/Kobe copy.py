import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jump Game")

# Load background
bg = pygame.image.load("bg.jpg")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# Player settings
player_width, player_height = 50, 60
player_x = 100
player_y = HEIGHT - player_height
player_vel_y = 0
jumping = False
gravity = 1
jump_power = 18
player_speed = 7  # Add this line under player settings

# Bullet settings
bullets = []
bullet_width, bullet_height = 20, 20
bullet_speed = 10

clock = pygame.time.Clock()

def draw_window():
    WIN.blit(bg, (0, 0))
    pygame.draw.rect(WIN, (255, 0, 0), (player_x, player_y, player_width, player_height))
    for bullet in bullets:
        # Draw black circle for each bullet
        center = (bullet.x + bullet_width // 2, bullet.y + bullet_height // 2)
        radius = bullet_height // 2
        pygame.draw.circle(WIN, (0, 0, 0), center, radius)
    pygame.display.update()

def main():
    global player_y, player_vel_y, jumping, player_x  # Add player_x to globals

    last_shot_time = 0
    shot_cooldown = 300  # milliseconds

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        # Walk left/right
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed
        # Jump with UP arrow
        if keys[pygame.K_UP] and not jumping:
            jumping = True
            player_vel_y = -jump_power
        # Shoot with SPACEBAR (with cooldown)
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE]:
            if current_time - last_shot_time > shot_cooldown:
                bullet = pygame.Rect(player_x + player_width, player_y + player_height // 2 - bullet_height // 2, bullet_width, bullet_height)
                bullets.append(bullet)
                last_shot_time = current_time

        if jumping:
            player_y += player_vel_y
            player_vel_y += gravity
            if player_y >= HEIGHT - player_height:
                player_y = HEIGHT - player_height
                jumping = False
                player_vel_y = 0

        # Move bullets
        for bullet in bullets:
            bullet.x += bullet_speed
        # Remove bullets that are off screen
        bullets[:] = [b for b in bullets if b.x < WIDTH]

        draw_window()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()