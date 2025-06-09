import pygame
import time

# Function to calculate screen dimensions with a 16:9 aspect ratio
def calculate_screen_size(base_width):
    aspect_ratio = 16 / 9
    width = base_width
    height = int(base_width / aspect_ratio)
    return width, height

# Function to initialize Pygame and set up the screen
def initialize_game(base_width):
    pygame.init()
    width, height = calculate_screen_size(base_width)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Scalable Platformer")
    return screen, width, height

# Function to load and scale the background image
def load_background(image_path, width, height):
    bg = pygame.image.load(image_path)
    bg = pygame.transform.scale(bg, (width, height))
    return bg

# Function to scale player attributes dynamically
def scale_player_attributes(base_width, width, height):
    global player_width, player_height, player_x, player_y, player_speed, jump_height, gravity
    scale_factor = base_width / 400
    player_width = int(10 * scale_factor)
    player_height = int(15 * scale_factor)
    player_x = int(width // 2)
    player_y = height - player_height
    player_speed = int(5 * scale_factor)
    jump_height = int(15 * scale_factor)
    gravity = int(1 * scale_factor)
    return player_width, player_height, player_x, player_y, player_speed, jump_height, gravity

# Function to handle screen resizing
def resize_screen(base_width, screen):
    width, height = calculate_screen_size(base_width)
    screen = pygame.display.set_mode((width, height))
    return screen, width, height

# Function to apply gravity
def apply_gravity(player_y, velocity_y, gravity, player_height, height, scale_factor):
    player_y += velocity_y
    velocity_y += gravity
    ground_level = height - player_height
    if player_y >= ground_level:
        player_y = ground_level
        velocity_y = 0
        is_jumping = False
    else:
        is_jumping = True
    return player_y, velocity_y, is_jumping

def increase_screen_size(BASE_WIDTH, screen, WIDTH, HEIGHT):
    WIDTH += 50
    screen, WIDTH, HEIGHT = resize_screen(WIDTH, screen)
    scale_player_attributes(WIDTH, WIDTH, HEIGHT)


def decrease_screen_size(WIDTH, screen, WIDTH, HEIGHT):
    WIDTH = max(400, BASE_WIDTH - 50)  # Minimum width is 400
    screen, WIDTH, HEIGHT = resize_screen(BASE_WIDTH, screen)
    scale_player_attributes(BASE_WIDTH, WIDTH, HEIGHT)

# Main game loop
def game_loop():
    global player_width, player_height, player_x, player_y, player_speed, jump_height, gravity,BASE_WIDTH, WIDTH, HEIGHT
    BASE_WIDTH = 400
    screen, WIDTH, HEIGHT = initialize_game(BASE_WIDTH)
    bg = load_background("Bg.webp", WIDTH, HEIGHT)  # Load and scale the background image
    scale_factor = BASE_WIDTH / 400
    BLUE = (0, 0, 255)
    clock = pygame.time.Clock()



    scale_player_attributes(BASE_WIDTH, WIDTH, HEIGHT)

    print(gravity)

    for i in range(25):
        increase_screen_size(BASE_WIDTH, screen, WIDTH, HEIGHT)
        bg = load_background("Bg.webp", WIDTH, HEIGHT)  # Reload and scale the background image
    print(gravity)


    velocity_y = 0
    is_jumping = False

    last_key_press_time = 0
    key_press_delay = 0.2  # 200ms delay between key presses




    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get keys
        keys = pygame.key.get_pressed()

        # Prevent the player from moving out of bounds
        if keys[pygame.K_LEFT]:  # Move left
            player_x = max(0, player_x - player_speed)  # Ensure player_x doesn't go below 0
        if keys[pygame.K_RIGHT]:  # Move right
            player_x = min(WIDTH - player_width, player_x + player_speed)  # Ensure player_x doesn't exceed screen width
        if keys[pygame.K_SPACE] and not is_jumping:  # Jump
            is_jumping = True
            velocity_y = -jump_height
        if keys[pygame.K_PLUS] or keys[pygame.K_KP_PLUS]:  # Increase screen size
            if time.time() - last_key_press_time > key_press_delay:
                increase_screen_size(BASE_WIDTH, screen, WIDTH, HEIGHT)
                bg = load_background("Bg.webp", WIDTH, HEIGHT)  # Reload and scale the background image
                last_key_press_time = time.time()
        if keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]:  # Decrease screen size
            if time.time() - last_key_press_time > key_press_delay:
                decrease_screen_size(BASE_WIDTH, screen, WIDTH, HEIGHT)
                bg = load_background("Bg.webp", WIDTH, HEIGHT)  # Reload and scale the background image
                last_key_press_time = time.time()

        # Apply gravity and ensure the player stays within the screen bounds
        player_y, velocity_y, is_jumping = apply_gravity(player_y, velocity_y, gravity, player_height, HEIGHT, scale_factor)
        player_y = min(HEIGHT - player_height, player_y)  # Ensure player_y doesn't exceed screen height

        # Draw background
        screen.blit(bg, (0, 0))

        # Draw player
        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))

        # Update display
        pygame.display.flip()

        # Control frame rate
        clock.tick(60)

    pygame.quit()

# Run the game
if __name__ == "__main__":
    game_loop()