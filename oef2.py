import pygame
import time

# pygame setup
pygame.init()
pygame.joystick.init()


joystick = None 
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()


screen = pygame.display.set_mode((640, 360))
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
        self.circle = 0

    def Up(self):
        self.playery -=10
        self.circle = 0

    def Down(self):
        self.playery +=10
        self.circle = 1


    def Right(self):
        self.playerx +=10
        self.circle = 0

    def Left(self):
        self.playerx -=10
        self.circle = 0

    def Blit(self):
        # print("x = ",self.playerx)
        # print("y = ",self.playery)
        self.Change()
        if self.circle == 1:
            pygame.draw.circle(screen, (0, 0, 255), (self.playerx, self.playery), 10)  # Green circle for the second image (Hond)


        screen.blit(self.player, (self.playerx, self.playery))

    def Change(self):
        if self.playerx <= 600:
            self.player = self.player1
        elif self.playerx >600:
            self.player = self.player2

def Change():
    global hond, hondA, hondB, state
    if state == 0:
        hond=hondA
    elif state == 1:
        hond=hondB
    state += 1
    if state == 2:
        state = 0

def JoystickAxis():
    y = joystick.get_axis(0)
    x = joystick.get_axis(1)
    if y > 0.5:
        hond.Down()
    elif y < -0.5:
        hond.Up()
    if x > 0.5:
        hond.Right()
    elif x < -0.5:
        hond.Left()
            

hondA = Player('Dog.jfif','Dog2.jfif')
hondB = Player('Dog3.webp','Dog4.webp')
hond = hondA
state = 0

while running:
    
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.JOYBUTTONDOWN:
            print(f"Motion on joystick {event.instance_id}")
            if event.button == 1:
                if event.value > 0.5:
                    Change()
                elif event.value < -0.5:
                    pass
            

        

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

    try:
        JoystickAxis()
    except:
        print("No Joysticks connected")
    
  

    hond.Blit()
    # Flip the display to put your work on screen
    pygame.display.flip()
    time.sleep(0.02)



pygame.quit()
