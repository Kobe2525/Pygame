import pygame
import time
import random

pygame.init()

ScreenSize = (1500, 600)
screen = pygame.display.set_mode(ScreenSize)
running = True
RED = (255, 0, 0)

sysfont = pygame.font.get_default_font()
print('system font :', sysfont)
font = pygame.font.SysFont(None, 48)



pygame.joystick.init()
joystick = None 
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

class Player:
    def __init__(self, image_path):

        self.player1 = pygame.image.load(image_path)
        self.player1 = pygame.transform.scale(self.player1, (150,150))
        self.player = self.player1
        self.playerx = 0
        self.playery = 0
        self.playerState = 0

    def Up(self):
        self.playery -=(25)
    def Down(self):
        self.playery +=(25)

    def Blit(self):
        #print("x = ",self.playerx)
        #print("y = ",self.playery)
        self.CheckLocation()
        screen.blit(self.player, (self.playerx, self.playery))

    def CheckLocation(self):
        if self.playerx >= 25:
            self.playerx = 25
        elif self.playerx <= 0:
            self.playerx = 0

        if self.playery >= 450:
            self.playery = 450
        elif self.playery <= 0:
            self.playery = 0

    def Shoot(self):
        global score
        if (self.playery+50) == putin.playery:
            putin.Random()
            score +=1 

class Target:
    def __init__(self, image_path):

        self.player1 = pygame.image.load(image_path)
        self.player = self.player1
        self.playerx = 1000
        self.playery = 0
        self.playerState = 0
    
    def Random(self):
        self.playery = random.randrange(75,450,25)


    def Blit(self):
        screen.blit(self.player, (self.playerx, self.playery))


f22 = Player('f22gif2.gif')
f35 = Player('f35gif2.gif')
f = f22

putin = Target('putingif.gif')

score = 0

try:
    img = pygame.image.load('wolken.jpg')
    img = pygame.transform.scale(img, (1500,600))
    putin.Random()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.JOYBUTTONDOWN:
                #print(f"Motion on joystick {event.instance_id}")
                if event.button == 1:
                    if joystick.get_button(1) == 1:
                        print("A pressed")
                        f.Shoot()
                    elif joystick.get_button(0) == 1:
                        print("bbbbb") 

            if event.type == pygame.JOYAXISMOTION:
                print(f"Motion on joystick {event.instance_id}")
                if event.axis == 1:
                    if event.value > 0.5:
                        f.Down()
                    elif event.value < -0.5:
                        f.Up()
        
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    f.Up()
                if keys[pygame.K_DOWN]:
                    f.Down()
                if keys[pygame.K_a]:
                    f = f22
                elif keys[pygame.K_b]:
                    f = f35

        
        text = font.render(str(score), True, RED)
        fonts = pygame.font.get_fonts()
        
        screen.blit(img,(0,0))
        f.Blit()
        putin.Blit()
        screen.blit(text, (20, 20))
        pygame.display.flip()

except KeyboardInterrupt:
    running = 0
    pygame.quit()