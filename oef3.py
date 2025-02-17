import pygame
import threading
import time
import random



# pygame setup
pygame.init()
pygame.joystick.init()


joystick = None 
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

ScreenSize = (1500, 600)
screen = pygame.display.set_mode(ScreenSize)
running = True

class Apple:
    def __init__(self, image_path,screensize):
        self.apple = pygame.image.load(image_path)
        self.apple = pygame.transform.scale(self.apple, ((screensize[1]/4),(screensize[1]/4)))
        self.applex = random.randrange(0,(ScreenSize[0])-((ScreenSize[1]/4)),screensize[1]/4)
        self.appley = random.randrange(0,(ScreenSize[1])-((ScreenSize[1]/4)),screensize[1]/4)
    
    def Blit(self):
        screen.blit(self.apple, (self.applex, self.appley))



class Player:
    def __init__(self, image_path, image2_path, screensize):

        self.player1 = pygame.image.load(image_path)
        self.player1 = pygame.transform.scale(self.player1, ((screensize[1]/4),(screensize[1]/4)))
        self.player2 = pygame.image.load(image2_path)
        self.player2 = pygame.transform.scale(self.player2, ((screensize[1]/4),(screensize[1]/4)))
        self.player = self.player1
        self.playerx = 0
        self.playery = 0
        self.playerState = 0
        self.circle = 0
        self.MoveState = 'Right'
        self.screensize = screensize

    def Up(self):
        self.playery -=(self.screensize[1]/4)
        self.circle = 0

    def Down(self):
        self.playery +=(self.screensize[1]/4)
        self.circle = 1


    def Right(self):
        self.playerx +=(self.screensize[1]/4)
        self.circle = 0

    def Left(self):
        self.playerx -=(self.screensize[1]/4)
        self.circle = 0
    
    def MoveStateF(self,HelpA):
        self.MoveState = HelpA


    def Blit(self):
        # print("x = ",self.playerx)
        # print("y = ",self.playery)
        self.CheckLocation()
        if self.circle == 1:
            pygame.draw.circle(screen, (0, 0, 255), (self.playerx, self.playery), 10)  # Green circle for the second image (Hond)


        screen.blit(self.player, (self.playerx, self.playery))

    def CheckLocation(self):
        if self.playerx >= ((ScreenSize[0])-((ScreenSize[1]/4))):
            self.playerx = ScreenSize[0]-(ScreenSize[1]/4)
        elif self.playerx <= 0:
            self.playerx = 0

        if self.playery >= ((ScreenSize[1])-((ScreenSize[1]/4))):
            self.playery = ScreenSize[1]-(ScreenSize[1]/4)
        elif self.playery <= 0:
            self.playery = 0

        if (self.playerx == apple.applex) and (self.playery == apple.appley):
            print("apple eaten")

        print(self.playerx)
        print((ScreenSize[0])-((ScreenSize[0]/4)))

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
    print("hello")
    global MoveState
    while running:
        y = joystick.get_axis(0)
        x = joystick.get_axis(1)
        if y > 0.5:
            MoveState = 'Down'
            print("Down")
        elif y < -0.5:
            MoveState = 'Up'
            print("uppp")
        if x > 0.5:
            MoveState = 'Right'
        elif x < -0.5:
            MoveState = 'Left'
            
def Move():
    MoveState = hond.MoveState
    if MoveState == 'Up':
        hond.Up()
    elif MoveState == 'Down':
        print("downnnn")
        hond.Down()
    elif MoveState == 'Left':
        hond.Left()
    elif MoveState == 'Right':
        hond.Right()
        #print(MoveState)
        

hondA = Player('Dog.jfif','Dog2.jfif',ScreenSize)
hondB = Player('Dog3.webp','Dog4.webp',ScreenSize)
apple = Apple('apple.png',ScreenSize)
hond = hondA
state = 0

t1 = threading.Thread(target=Move, args=())
t1.start()
t2 = threading.Thread(target=JoystickAxis, args=())
try:
    t2.start()
except:
    print("No Joysticks connected")
    pass

try:
    while running:

        # Poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.JOYBUTTONDOWN:
                #print(f"Motion on joystick {event.instance_id}")
                if event.button == 1:
                    if joystick.get_button(1) > 0.5:
                        Change()
                    elif joystick.get_button(1) < -0.5:
                        pass
            
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    hond.MoveStateF('Up')
                if keys[pygame.K_DOWN]:
                    hond.MoveStateF('Down')
                if keys[pygame.K_LEFT]:
                    hond.MoveStateF('Left')
                if keys[pygame.K_RIGHT]:
                    hond.MoveStateF('Right')
                if keys[pygame.K_r]:
                    Change()
        # Fill the screen with a color to wipe away anything from last frame
        screen.fill("Green")
        Move()
        apple.Blit()
        hond.Blit()
        pygame.display.flip()
        time.sleep(0.5)

except KeyboardInterrupt:
    running = 0
    t1.join()
    t2.join()
    pygame.quit()
