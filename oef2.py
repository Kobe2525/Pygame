import pygame
import time

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
running = True




class Player:
    def __init__(self, image_path, image2_path):
        
        self.player1 = pygame.image.load(image_path)
        self.player1 = pygame.transform.scale(self.player1, (200, 200))
        self.player2 = pygame.image.load(image2_path)
        self.player2 = pygame.transform.scale(self.player2, (200, 200))
        self.player = self.player1
        self.playerx = 0
        self.playery = 0
        self.playerState = 0
    
    def Up(self):
        self.playery -=10

    def Down(self):
        self.playery +=10

    def Right(self):
        self.playerx +=10

    def Left(self):
        self.playerx -=10

    def Blit(self):
        print("x = ",self.playerx)
        print("y = ",self.playery)
        self.Change()
        
        screen.blit(self.player, (self.playerx, self.playery))

    def Change(self):
        if self.playerx <= 600:
            self.player = self.player1
        elif self.playerx >600:
            self.player = self.player2

def Change():
    global hond, hondA, hondB
    state = 0
    if state == 0:
        hond=hondA
    elif state == 1:
        hond=hondB
    state += 1
    if state == 2:
        state = 0

hondA = Player('Dog.jfif','Dog2.jfif')
hondB = Player('Dog3.webp','Dog4.webp')
hond = hondA

while running:
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color to wipe away anything from last frame
    screen.fill("Green")
    # Handle key presses

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        hond.Up()
    if keys[pygame.K_DOWN]:
        hond.Down()
    if keys[pygame.K_LEFT]:
        hond.Left()
    if keys[pygame.K_RIGHT]:
        hond.Right()
    if keys[pygame.K_r]:
        
        Change()
    hond.Blit()
    
        

    # Flip the display to put your work on screen
    pygame.display.flip()
    time.sleep(0.07)

pygame.quit()
