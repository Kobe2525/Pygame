import pygame
import os
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 1920, 1080  # 16:9 aspect ratio
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Move")

# Load background
bg_path = "game_background_1.png"
background = pygame.image.load(bg_path)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Load spaceship
ship_path = os.path.join("F_IMG", "Ship_1_C_Small.png")
ship = pygame.image.load(ship_path).convert_alpha()
ship_rect = ship.get_rect()
ship_rect.midbottom = (WIDTH // 2, HEIGHT - 30)
ship_speed = 10

# Load missile
missile_path = os.path.join("M_IMG", "missile_C_Small.png")
missile_img = pygame.image.load(missile_path).convert_alpha()
missile_speed = 15
missiles = []
homing_missiles = []  # Each item: {"rect": ..., "target": ...}

# Load only Enemy2ASmall and Enemy2BSmall from E_IMG folder
enemy_folder = "E_IMG"
enemy_filenames = [f for f in os.listdir(enemy_folder) if f.startswith("Enemy_2_A") or f.startswith("Enemy_2_B")]
enemy_images = [pygame.image.load(os.path.join(enemy_folder, f)).convert_alpha() for f in enemy_filenames]

enemies = []
ENEMY_SPEED = 6
ENEMY_SPAWN_DELAY = 120  # fewer enemies
enemy_spawn_timer = 0

# Power-up setup
POWERUP_FOLDER = "P_IMG"
POWERUP_TYPES = [
    {"name": "extra_missiles", "img": "Pickup_3_C_Small.png"},
    {"name": "homing", "img": "Pickup_2_D_Small.png"},
    {"name": "shield", "img": "Pickup_2_A_Small.png"},
]
powerup_images = {
    p["name"]: pygame.image.load(os.path.join(POWERUP_FOLDER, p["img"])).convert_alpha()
    for p in POWERUP_TYPES
}
POWERUP_SPEED = 5
powerups = []

# Power-up counters
missile_count = 10  # Start with 10 missiles
homing_count = 0
shield_active = False
shield_timer = 0
SHIELD_DURATION = 300  # frames (~5 seconds)

score = 0
level = 1
LEVEL_UP_SCORE = 10 
ENEMY_SPEED = 4 
ENEMY_SPAWN_DELAY = 120

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)  # 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and missile_count > 0:
                # Fire a missile from the center top of the ship
                missile_rect = missile_img.get_rect()
                missile_rect.midbottom = ship_rect.midtop
                missiles.append(missile_rect)
                missile_count -= 1
            if event.key == pygame.K_h and homing_count > 0 and enemies:
                # Fire a homing missile: instantly destroy the closest enemy
                # Find the closest enemy to the ship
                closest_idx = min(
                    range(len(enemies)),
                    key=lambda i: abs(enemies[i][1].centerx - ship_rect.centerx) + abs(enemies[i][1].centery - ship_rect.centery)
                )
                enemy_img, enemy_rect = enemies[closest_idx]
                missile_rect = missile_img.get_rect()
                missile_rect.midbottom = ship_rect.midtop
                homing_missiles.append({"rect": missile_rect, "target": enemy_rect})
                homing_count -= 1

    # Key handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship_rect.x -= ship_speed
    if keys[pygame.K_RIGHT]:
        ship_rect.x += ship_speed

    # Keep ship within screen bounds
    ship_rect.x = max(0, min(WIDTH - ship_rect.width, ship_rect.x))

    # Move missiles
    for missile in missiles:
        missile.y -= missile_speed
    missiles = [m for m in missiles if m.bottom > 0]

    # Move homing missiles
    homing_speed = 15
    for hm in homing_missiles:
        missile = hm["rect"]
        target = hm["target"]
        dx = target.centerx - missile.centerx
        dy = target.centery - missile.centery
        dist = max(1, (dx**2 + dy**2) ** 0.5)
        missile.x += int(homing_speed * dx / dist)
        missile.y += int(homing_speed * dy / dist)

    # Spawn enemies
    enemy_spawn_timer += 1
    if enemy_spawn_timer >= ENEMY_SPAWN_DELAY:
        enemy_spawn_timer = 0
        enemy_img = random.choice(enemy_images)
        enemy_rect = enemy_img.get_rect()
        enemy_rect.midtop = (random.randint(0, WIDTH - enemy_rect.width), 0)
        enemies.append((enemy_img, enemy_rect))

    # Move enemies
    for i, (enemy_img, enemy_rect) in enumerate(enemies):
        enemy_rect.y += ENEMY_SPEED

    # Remove enemies that are off the screen
    enemies = [(img, rect) for img, rect in enemies if rect.top < HEIGHT]

    # --- Missile-enemy collision ---
    missiles_to_remove = []
    enemies_to_remove = []
    for mi, missile in enumerate(missiles):
        for ei, (enemy_img, enemy_rect) in enumerate(enemies):
            if missile.colliderect(enemy_rect):
                missiles_to_remove.append(mi)
                enemies_to_remove.append(ei)
                score += 1  # Add point for normal missile hit
    # Remove hit missiles and enemies (avoid double-removal)
    missiles = [m for i, m in enumerate(missiles) if i not in missiles_to_remove]
    enemies = [e for i, e in enumerate(enemies) if i not in enemies_to_remove]

    # Remove homing missiles and enemies on collision
    to_remove = []
    for i, hm in enumerate(homing_missiles):
        for ei, (enemy_img, enemy_rect) in enumerate(enemies):
            if hm["target"] == enemy_rect and hm["rect"].colliderect(enemy_rect):
                to_remove.append(i)
                enemies.pop(ei)
                score += 1  # Add point for homing missile hit
                break
    homing_missiles = [hm for i, hm in enumerate(homing_missiles) if i not in to_remove]

    # Randomly spawn powerups (e.g. 1% chance per frame)
    if random.random() < 0.01:
        ptype = random.choice(POWERUP_TYPES)
        p_img = powerup_images[ptype["name"]]
        p_rect = p_img.get_rect()
        p_rect.midtop = (random.randint(0, WIDTH - p_rect.width), 0)
        powerups.append({"type": ptype["name"], "img": p_img, "rect": p_rect})

    # Move powerups
    for p in powerups:
        p["rect"].y += POWERUP_SPEED

    # Remove powerups off screen
    powerups = [p for p in powerups if p["rect"].top < HEIGHT]

    # Powerup collision with ship
    for p in powerups[:]:
        if ship_rect.colliderect(p["rect"]):
            if p["type"] == "extra_missiles":
                missile_count += 10
            elif p["type"] == "homing":
                homing_count += 3
            elif p["type"] == "shield":
                shield_active = True
                shield_timer = SHIELD_DURATION
            powerups.remove(p)

    # Shield timer
    if shield_active:
        shield_timer -= 1
        if shield_timer <= 0:
            shield_active = False

    # Level up logic
    if score // LEVEL_UP_SCORE + 1 > level:
        level += 1
        ENEMY_SPEED += 1  # Increase enemy speed
        ENEMY_SPAWN_DELAY = max(20, ENEMY_SPAWN_DELAY - 10)  # Enemies spawn more often, but not too fast

    # Draw everything
    screen.blit(background, (0, 0))
    screen.blit(ship, ship_rect)
    # Draw shield if active
    if shield_active:
        pygame.draw.ellipse(screen, (0, 200, 255, 128), ship_rect.inflate(40, 20), 4)
    for missile in missiles:
        screen.blit(missile_img, missile)
    for enemy_img, enemy_rect in enemies:
        screen.blit(enemy_img, enemy_rect)
    for p in powerups:
        screen.blit(p["img"], p["rect"])
    # Draw homing missiles
    for hm in homing_missiles:
        screen.blit(missile_img, hm["rect"])
    # Draw counters
    font = pygame.font.SysFont(None, 36)
    screen.blit(font.render(f"Missiles: {missile_count}", True, (255,255,0)), (20, 20))
    screen.blit(font.render(f"Homing: {homing_count}", True, (0,255,0)), (20, 60))
    screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (20, 100))
    screen.blit(font.render(f"Level: {level}", True, (255,128,0)), (20, 140))
    if shield_active:
        screen.blit(font.render("Shield!", True, (0,200,255)), (20, 180))
    pygame.display.flip()

pygame.quit()
sys.exit()