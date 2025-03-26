import pygame
import threading
import time
import random



# pygame setup
pygame.init()

ScreenSize = (2400, 1200)
screen = pygame.display.set_mode(ScreenSize)
Gridsize = (ScreenSize[1]/16)
running = True

pygame.joystick.init()
joystick = None 
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()



class Apple:
    def __init__(self, image_path,Gridsize,ScreenSize):
        self.apple = pygame.image.load(image_path)
        self.apple = pygame.transform.scale(self.apple, (Gridsize,Gridsize))
        self.applex = int(random.randrange(0,int((ScreenSize[0])-(Gridsize)),int(Gridsize)))
        self.appley = int(random.randrange(0,int((ScreenSize[1])-(Gridsize)),int(Gridsize)))
        self.ScreenSize = ScreenSize
        self.Gridsize = Gridsize
    
    def Random(self):
        self.applex = int(random.randrange(0,int((self.ScreenSize[0])-((Gridsize))),int(Gridsize)))
        self.appley = int(random.randrange(0,int((self.ScreenSize[1])-((Gridsize))),int(Gridsize)))

    def Blit(self):
        screen.blit(self.apple, (self.applex, self.appley))



class Player:
    def __init__(self, image_path, image2_path, Gridsize,ScreenSize):

        self.player1 = pygame.image.load(image_path)
        self.player1 = pygame.transform.scale(self.player1, (Gridsize,Gridsize))
        self.player2 = pygame.image.load(image2_path)
        self.player2 = pygame.transform.scale(self.player2, (Gridsize,Gridsize))
        self.player = self.player1
        self.playerx = [150,75,0]
        self.playery = [0,0,0]
        self.playerRotate = 1
        self.playerRotateOld = 1
        self.playerState = "Right"
        self.Gridsize = Gridsize
        self.ScreenSize = ScreenSize

    def Up(self):
        
        for i in range(len(self.playery)-1,0,-1):
            self.playery[i] = self.playery[i-1]
            self.playerx[i] = self.playerx[i-1]
        self.playery[0] -=(self.Gridsize) 

    def Down(self): 
           
        for i in range(len(self.playery)-1,0,-1):
            self.playery[i] = self.playery[i-1]
            self.playerx[i] = self.playerx[i-1]
        self.playery[0] +=(self.Gridsize)

    def Right(self):
        
        for i in range(len(self.playerx)-1,0,-1):
            self.playerx[i] = self.playerx[i-1]
            self.playery[i] = self.playery[i-1]
        self.playerx[0] +=(self.Gridsize)

    def Left(self):
        
        for i in range(len(self.playerx)-1,0,-1):
            self.playerx[i] = self.playerx[i-1]
            self.playery[i] = self.playery[i-1]
        self.playerx[0] -=(self.Gridsize)

    def MovePlayerState(self):
        global x,y
        #print(x,y)
        if y > 0.5:
            self.playerState = "Down"
            self.playerRotate = 2
            self.RotatePlayer()
        elif y < -0.5:
            self.playerState = "Up"
            self.playerRotate = 0
            self.RotatePlayer()
        elif x > 0.5:
            self.playerState = "Right"
            self.playerRotate = 1
            self.RotatePlayer()
        elif x < -0.5:
            self.playerState = "Left"
            self.playerRotate = 3
            self.RotatePlayer()
        self.MovePlayer()
    
    def MovePlayer(self):
        
        if self.playerState == "Down":
            self.Down()
        elif self.playerState == "Up":
            self.Up()
        elif self.playerState == "Right":
            self.Right()
        elif self.playerState == "Left":
            self.Left()
        
    def RotatePlayer(self):
        self.player = pygame.transform.rotate(self.player,90*(self.playerRotateOld - self.playerRotate))
        self.playerRotateOld = self.playerRotate

    def Append(self):
        self.playerx.append(self.playerx[len(self.playerx)-1])
        self.playery.append(self.playery[len(self.playery)-1])

    def CheckLocation(self):
        global running
        for i in range(0,len(self.playery),1):
            if self.playerx[i] >= ((ScreenSize[0])-(Gridsize)):
                self.playerx[i] = ScreenSize[0]-(Gridsize)
            elif self.playerx[i] <= 0:
                self.playerx[i] = 0
            if self.playery[i] >= ((ScreenSize[1])-(Gridsize)):
                self.playery[i] = ScreenSize[1]-Gridsize
            elif self.playery[i] <= 0:
                self.playery[i] = 0

            for j in range(0,len(self.playery),1):
                if(self.playerx[i] == self.playerx[j] and self.playery[i] == self.playery[j] and i!=j):
                    running = 0
                    print("gameover")

            if (self.playerx[i] == apple.applex) and (self.playery[i] == apple.appley):
                apple.Random()
                self.Append()
                print("apple eaten")

    def Blit(self):
        # print("x = ",self.playerx)
        # print("y = ",self.playery)
        self.CheckLocation()
        for i in range(0,len(self.playery),1):
            screen.blit(self.player, (self.playerx[i], self.playery[i]))
        print("x= ",self.playerx[0],",",self.playerx[1],",",self.playerx[2])
        print("y= ",self.playery[0],",",self.playery[1],",",self.playery[2])

def Change():
    global player, playerA, playerB, state
    if state == 0:
        player=playerA
    elif state == 1:
        player=playerB
    state += 1
    if state == 2:
        state = 0

def GetJoystickAxis(): #Running in thread
    global x,y
    while running:
        y = joystick.get_axis(1)
        x = joystick.get_axis(0)    

playerA = Player('f22gif2.gif','Dog2.jfif',Gridsize,ScreenSize)
playerB = Player('Dog3.webp','Dog4.webp',Gridsize,ScreenSize)
apple = Apple('balloon.png',Gridsize,ScreenSize)
player = playerA
state = 0
y=0
x=0

ImageBackground = pygame.image.load('wolken.jpg')
ImageBackground = pygame.transform.scale(ImageBackground, ScreenSize)

t1 = threading.Thread(target=GetJoystickAxis, args=())
try:
    t1.start()
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
                    player.MoveStateF('Up')
                if keys[pygame.K_DOWN]:
                    player.MoveStateF('Down')
                if keys[pygame.K_LEFT]:
                    player.MoveStateF('Left')
                if keys[pygame.K_RIGHT]:
                    player.MoveStateF('Right')
                if keys[pygame.K_r]:
                    Change()
        # Fill the screen with a color to wipe away anything from last frame
        screen.fill("Green")
        screen.blit(ImageBackground,(0,0))
        player.MovePlayerState()
        apple.Blit()
        player.Blit()
        pygame.display.flip()
        #print("flipped")
        time.sleep(0.25)
    screen.fill("Green") 
    font = pygame.font.SysFont('arial', 30) 
    line1 = font.render(f"Game is over! Your score is {len(player.playerx)-3}", True, (255, 255, 255)) 
    screen.blit(line1, (200, 300)) 
    line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255)) 
    screen.blit(line2,(200, 350)) 
    pygame.display.flip() 
    time.sleep(999)

    

except KeyboardInterrupt:
    running = 0
    t1.join()
    pygame.quit()
