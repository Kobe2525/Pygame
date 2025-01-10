# Example file showing a basic pygame "game loop"
import pygame
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# Load the image and set initial parameters
bg = pygame.image.load("C:/Users/Kobe/OneDrive - KOGEKA/Afbeeldingen/noctua.jpg")
pygame.transform.scale(bg, (200,200))
blockx, blocky = 0, 0
rotation_angle = 0
rotated_bg = bg

while running:
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        blocky -= 1
    elif keys[pygame.K_DOWN]:
        blocky += 1
    if keys[pygame.K_LEFT]: 
        blockx -= 1
    elif keys[pygame.K_RIGHT]:
        # Rotate the image by 90 degrees
        rotation_angle = (rotation_angle + 90) % 360
        rotated_bg = pygame.transform.rotate(bg, rotation_angle)
        blockx += 1

    # Fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    screen.blit(rotated_bg, (blockx, blocky))

    # Flip the display to put your work on screen
    pygame.display.flip()  

    clock.tick(60)  # Limits FPS to 60

pygame.quit()
