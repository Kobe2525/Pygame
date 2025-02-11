import pygame
import threading
import time

# pygame setup
pygame.init()
pygame.joystick.init()


joystick = None 
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

ScreenSize = (1500, 800)
screen = pygame.display.set_mode(ScreenSize)
running = True





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
        if self.playerx <= ((ScreenSize[0]/2)-(ScreenSize[1]/8)):
            self.player = self.player1
        elif self.playerx > ((ScreenSize[0]/2)-(ScreenSize[1]/8)):
            self.player = self.player2

        if self.playerx >= ((ScreenSize[0])-((ScreenSize[1]/4))):
            self.playerx = ScreenSize[0]-(ScreenSize[1]/4)
        elif self.playerx <= 0:
            self.playerx = 0

        if self.playery >= ((ScreenSize[1])-((ScreenSize[1]/4))):
            self.playery = ScreenSize[1]-(ScreenSize[1]/4)
        elif self.playery <= 0:
            self.playery = 0

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
    global MoveState
    y = joystick.get_axis(0)
    x = joystick.get_axis(1)
    if y > 0.5:
        MoveState = 'Down'
    elif y < -0.5:
        MoveState = 'Up'
    if x > 0.5:
        MoveState = 'Right'
    elif x < -0.5:
        MoveState = 'Left'
            
def Move():
    global running 
    while running:
        MoveState = hond.MoveState
        if MoveState == 'Up':
            hond.Up()
        elif MoveState == 'Down':
            hond.Down()
        elif MoveState == 'Left':
            hond.Left()
        elif MoveState == 'Right':
            hond.Right()
        #print(MoveState)
        time.sleep(0.052)

hondA = Player('Dog.jfif','Dog2.jfif',ScreenSize)
hondB = Player('Dog3.webp','Dog4.webp',ScreenSize)
hond = hondA
state = 0

t1 = threading.Thread(target=Move, args=())
t1.start()
try:
    while running:

        # Poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.JOYBUTTONDOWN:
                #print(f"Motion on joystick {event.instance_id}")
                if event.button == 1:
                    if event.value > 0.5:
                        Change()
                    elif event.value < -0.5:
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
        # Handle key presses



        try:
            JoystickAxis()
        except:
            #print("No Joysticks connected")
            pass


        hond.Blit()
        # Flip the display to put your work on screen
        pygame.display.flip()
        time.sleep(0.05)

except KeyboardInterrupt:
    running = 0
    t1.join()
    pygame.quit()
