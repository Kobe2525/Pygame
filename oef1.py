import pygame
import time
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
running = True

# Load the image and set initial parameters
Noctua = pygame.image.load("C:/Users/Kobe/OneDrive - KOGEKA/Afbeeldingen/noctua.jpg")
Hond = pygame.image.load("C:/Users/Kobe/OneDrive - KOGEKA/Afbeeldingen/9c6460b2ec1f740c18d5c33a2999e681.webp")
Noctua = pygame.transform.scale(Noctua, (200, 200))
Hond = pygame.transform.scale(Hond, (200, 200))
blockx, blocky = 0, 0
rotation_angle = 0
rotated_Noctua = Noctua
rotated_hond = Hond

# Variable to track which image is being used
img = 0
circle = 0

while running:
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    # Handle key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        blocky -= 10
        circle = 0
    elif keys[pygame.K_DOWN]:
        circle = 1
        blocky += 10
        
    if keys[pygame.K_LEFT]:
        circle = 0
        rotation_angle -= 90
        if img == 1:
            rotated_hond = pygame.transform.rotate(Hond, rotation_angle)
            blockx -= 10
        elif img == 0:
            rotated_Noctua = pygame.transform.rotate(Noctua, rotation_angle)
            blockx -= 10

    elif keys[pygame.K_RIGHT]:
        circle = 0
        rotation_angle += 90
        if img == 1:
            rotated_hond = pygame.transform.rotate(Hond, rotation_angle)
            blockx += 10
        elif img == 0:
            rotated_Noctua = pygame.transform.rotate(Noctua, rotation_angle)
            blockx += 10

    if img == 1 and circle == 1:
            pygame.draw.circle(screen, (0, 255, 0), (blockx, blocky), 10)  # Green circle for the second image (Hond)
    elif img == 0 and circle == 1:
            pygame.draw.circle(screen, (0, 0, 255), (blockx, blocky), 10)  # Blue circle for the first image (Noctua)
    

    # Display the appropriate image
    if blockx <= 590:
        img = 0
        screen.blit(rotated_Noctua, (blockx, blocky))
    else:
        img = 1
        screen.blit(rotated_hond, (blockx, blocky))

    # Flip the display to put your work on screen
    pygame.display.flip()
    time.sleep(0.07)

pygame.quit()
