# Example file showing a basic pygame "game loop"
import pygame
import time
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
running = True

# Load the image and set initial parameters
bg = pygame.image.load("C:/Users/Kobe/OneDrive - KOGEKA/Afbeeldingen/noctua.jpg")
bgB = pygame.image.load("C:/Users/Kobe/OneDrive - KOGEKA/Afbeeldingen/9c6460b2ec1f740c18d5c33a2999e681.webp")
bg = pygame.transform.scale(bg, (200,200))
bgB = pygame.transform.scale(bgB, (200,200))
blockx, blocky = 0, 0
rotation_angle = 0
rotated_bg = bg
rotated_bgB = bgB

while running:
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        blocky -= 10
    elif keys[pygame.K_DOWN]:
        blocky += 10
    if keys[pygame.K_LEFT]: 
        rotation_angle -= 90 
        if img ==1:
            rotated_bgB = pygame.transform.rotate(bgB, rotation_angle)
            blockx -= 10
        elif img ==0:
            rotated_bg = pygame.transform.rotate(bg, rotation_angle)
            blockx -= 10

    elif keys[pygame.K_RIGHT]:
        # Rotate the image by 90 degrees
        rotation_angle += 90 
        if img ==1:
            rotated_bgB = pygame.transform.rotate(bgB, rotation_angle)
            blockx += 10
        elif img ==0:
            rotated_bg = pygame.transform.rotate(bg, rotation_angle)
            blockx += 10

    # Fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    if blockx <= 590:
        img = 0
        screen.blit(rotated_bg, (blockx, blocky))
    if blockx > 590:
        img = 1
        screen.blit(rotated_bgB, (blockx, blocky))

    # Flip the display to put your work on screen
    pygame.display.flip()  
    time.sleep(0.07)


pygame.quit()
