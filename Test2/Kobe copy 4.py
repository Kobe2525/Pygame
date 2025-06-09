import pygame
import sys
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound

# Play background music
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)  # Loop forever

# Load bullet sound
bullet_sound = pygame.mixer.Sound("bullet.mp3")

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
gravity = 0.5    # Was 1, now slower falling
jump_power = 10  # Was 18, now slower rise
player_speed = 3  # Slower walking speed

# Bullet settings
bullets = []
bullet_width, bullet_height = 20, 20
bullet_speed = 10

# Enemy bullet settings
enemy_bullets = []
enemy_bullet_width, enemy_bullet_height = 20, 20
enemy_bullet_speed = 3  # Slower enemy bullets
enemy_bullet_size_multiplier = 1

# Add font for hit text
hit_font = pygame.font.SysFont("Arial", 60)
last_hit_time = 0
show_hit = False

# Score
score = 0

clock = pygame.time.Clock()

# Load player sprites
def load_sprites(folder):
    sprites = []
    folder_path = os.path.join("M_IMG", folder)
    if os.path.exists(folder_path):
        for file in sorted(os.listdir(folder_path)):
            if file.lower().endswith((".png", ".jpg")):
                img = pygame.image.load(os.path.join(folder_path, file)).convert_alpha()
                img = pygame.transform.scale(img, (player_width, player_height))
                sprites.append(img)
    return sprites

left_sprites = load_sprites("L")
right_sprites = load_sprites("R")
sprite_index = 0
sprite_timer = 0
sprite_interval = 7  # frames per sprite
direction = "right"  # Start facing right

# Load enemy sprites
def load_enemy_sprites(folder):
    sprites = []
    folder_path = os.path.join("E_IMG", folder)
    if os.path.exists(folder_path):
        for file in sorted(os.listdir(folder_path)):
            if file.lower().endswith((".png", ".jpg")):
                img = pygame.image.load(os.path.join(folder_path, file)).convert_alpha()
                img = pygame.transform.scale(img, (player_width, player_height))
                sprites.append(img)
    return sprites

enemy_sprites = load_enemy_sprites("L")
enemy_sprite_index = 0
enemy_sprite_timer = 0
enemy_sprite_interval = 7  # frames per sprite

# Enemy settings
enemy_x = WIDTH
enemy_y = HEIGHT - player_height
enemy_jumping = False
enemy_vel_y = 0
enemy_gravity = gravity
enemy_jump_power = jump_power
enemy_speed = 1

def draw_window():
    WIN.blit(bg, (0, 0))
    # Player
    if direction == "left" and left_sprites:
        WIN.blit(left_sprites[sprite_index], (player_x, player_y))
    elif direction == "right" and right_sprites:
        WIN.blit(right_sprites[sprite_index], (player_x, player_y))
    else:
        pygame.draw.rect(WIN, (255, 0, 0), (player_x, player_y, player_width, player_height))
    # Enemy
    if enemy_sprites:
        WIN.blit(enemy_sprites[enemy_sprite_index], (enemy_x, enemy_y))
    else:
        pygame.draw.rect(WIN, (0, 0, 255), (enemy_x, enemy_y, player_width, player_height))
    # Bullets
    for bullet in bullets:
        center = (bullet.x + bullet_width // 2, bullet.y + bullet_height // 2)
        radius = bullet_height // 2
        pygame.draw.circle(WIN, (0, 0, 0), center, radius)
    # Enemy bullets
    for e_bullet in enemy_bullets:
        e_center = (e_bullet.x + enemy_bullet_width // 2, e_bullet.y + enemy_bullet_height // 2)
        e_radius = enemy_bullet_height // 2
        pygame.draw.circle(WIN, (255, 0, 0), e_center, e_radius)
    # Show -5 if hit
    if show_hit:
        hit_text = hit_font.render("-5", True, (255, 0, 0))
        WIN.blit(hit_text, (player_x + player_width // 2 - hit_text.get_width() // 2, player_y - 60))
    # Draw score at top center
    score_text = hit_font.render(str(score), True, (0, 0, 0))
    WIN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
    pygame.display.update()

def main():
    global player_y, player_vel_y, jumping, player_x, sprite_index, sprite_timer, direction
    global enemy_x, enemy_sprite_index, enemy_sprite_timer
    global last_hit_time, show_hit
    global score
    global enemy_bullet_width, enemy_bullet_height
    global enemy_bullet_size_multiplier
    global enemy_jumping, enemy_y, enemy_vel_y  # <-- Add this line

    last_shot_time = 0
    shot_cooldown = 300  # milliseconds

    running = True
    while running:
        clock.tick(60)
        moved = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        # Walk left/right
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
            direction = "left"
            moved = True
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed
            direction = "right"
            moved = True
        # Jump with UP arrow
        if keys[pygame.K_UP] and not jumping:
            jumping = True
            player_vel_y = -jump_power
            # Enemy jumps too
            if not enemy_jumping:
                enemy_jumping = True
                enemy_vel_y = -enemy_jump_power

        if jumping:
            player_y += player_vel_y
            player_vel_y += gravity
            if player_y >= HEIGHT - player_height:
                player_y = HEIGHT - player_height
                jumping = False
                player_vel_y = 0

        # Enemy jump logic
        if enemy_jumping:
            enemy_y += enemy_vel_y
            enemy_vel_y += enemy_gravity
            if enemy_y >= HEIGHT - player_height:
                enemy_y = HEIGHT - player_height
                enemy_jumping = False
                enemy_vel_y = 0

        # Shoot with SPACEBAR (with cooldown)
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE]:
            if current_time - last_shot_time > shot_cooldown:
                bullet = pygame.Rect(player_x + player_width, player_y + player_height // 2 - bullet_height // 2, bullet_width, bullet_height)
                bullets.append(bullet)
                bullet_sound.play()  # Play bullet sound
                last_shot_time = current_time

        # Sprite animation cycling for player
        if moved:
            sprite_timer += 1
            if sprite_timer >= sprite_interval:
                if direction == "left" and left_sprites:
                    sprite_index = (sprite_index + 1) % len(left_sprites)
                elif direction == "right" and right_sprites:
                    sprite_index = (sprite_index + 1) % len(right_sprites)
                sprite_timer = 0
        else:
            sprite_index = 0  # Reset to first frame when not moving

        # Enemy movement and animation
        enemy_x -= enemy_speed
        if enemy_x < -player_width:
            enemy_x = WIDTH  # Reset to right side
        enemy_sprite_timer += 1
        if enemy_sprite_timer >= enemy_sprite_interval:
            if enemy_sprites:
                enemy_sprite_index = (enemy_sprite_index + 1) % len(enemy_sprites)
                # Check if the current sprite file is L9E.png
                sprite_files = sorted(os.listdir(os.path.join("E_IMG", "L")))
                if sprite_files:
                    current_sprite_file = sprite_files[enemy_sprite_index]
                    if current_sprite_file == "L9E.png":
                        e_bullet = pygame.Rect(
                            enemy_x, enemy_y + player_height // 2 - enemy_bullet_height // 2,
                            enemy_bullet_width, enemy_bullet_height
                        )
                        enemy_bullets.append(e_bullet)
            enemy_sprite_timer = 0

        # Move bullets
        for bullet in bullets:
            bullet.x += bullet_speed
        # Remove bullets that are off screen
        bullets[:] = [b for b in bullets if b.x < WIDTH]

        # Move enemy bullets
        for e_bullet in enemy_bullets:
            e_bullet.x -= enemy_bullet_speed
        # Remove enemy bullets that are off screen
        enemy_bullets[:] = [e_b for e_b in enemy_bullets if e_b.x > 0]

        # Check collision with player
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for e_bullet in enemy_bullets:
            if player_rect.colliderect(e_bullet):
                show_hit = True
                last_hit_time = pygame.time.get_ticks()
                break

        # Check collision with enemy and remove bullet if hit
        enemy_rect = pygame.Rect(enemy_x, enemy_y, player_width, player_height)
        for bullet in bullets[:]:
            if enemy_rect.colliderect(bullet):
                score += 1
                bullets.remove(bullet)
                # Increase enemy bullet size every 10 points
                if score % 10 == 0:
                    enemy_bullet_size_multiplier += 1
                    enemy_bullet_width = 20 * enemy_bullet_size_multiplier
                    enemy_bullet_height = 20 * enemy_bullet_size_multiplier
                    enemy_x = WIDTH  # Reset enemy to right side
                break

        # Hide -5 after 1 second
        if show_hit and pygame.time.get_ticks() - last_hit_time > 1000:
            show_hit = False

        draw_window()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()