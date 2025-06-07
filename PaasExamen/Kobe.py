import pygame
import threading
import time
import random

# pygame setup
pygame.init()

pygame.mixer.init()
soundmeow = pygame.mixer.Sound('meow.mp3')
soundballoon = pygame.mixer.Sound('balloon.mp3')
soundcrash = pygame.mixer.Sound('crash.mp3')

ScreenSize = (1500, 600)
screen = pygame.display.set_mode(ScreenSize)
Gridsize = (ScreenSize[1]/8)
running = True

pygame.joystick.init()
joystick = None 
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

class Hit:
    def __init__(self, image_path,Gridsize,ScreenSize):
        self.hit = pygame.image.load(image_path)
        self.hit = pygame.transform.scale(self.hit, (Gridsize,Gridsize))
        self.hitx = int(random.randrange(0,int((ScreenSize[0])-(Gridsize)),int(Gridsize)))
        self.hity = int(random.randrange(0,int((ScreenSize[1])-(Gridsize)),int(Gridsize)))
        self.ScreenSize = ScreenSize
        self.Gridsize = Gridsize

    def Random(self):
        self.hitx = int(random.randrange(0,int((self.ScreenSize[0])-((Gridsize))),int(Gridsize)))
        self.hity = int(random.randrange(0,int((self.ScreenSize[1])-((Gridsize))),int(Gridsize)))
        

    def Blit(self):
        print("Balloon = ", self.hitx," , ",self.hity)
        screen.blit(self.hit, (self.hitx, self.hity))

class Player:
    def __init__(self, image_path, Gridsize,ScreenSize):

        self.player = pygame.image.load(image_path)
        self.player = pygame.transform.scale(self.player, (Gridsize,Gridsize))
        self.player = pygame.transform.rotate(self.player,90)
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
        self.playerx.append(self.playerx[len(self.playerx)-1]-Gridsize)
        self.playery.append(self.playery[len(self.playery)-1])

    def CheckLocation(self):
        global running,Sleep
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
                    soundcrash.play()
                    print("gameover")

        for i in range(0,len(self.playery),1):
            if (self.playerx[i] == balloon.hitx) and (self.playery[i] == balloon.hity):
                balloon.Random()
                self.Append()
                soundballoon.play()
                print("Balloon shot")
                Sleep +=0.1 
        
        for i in range(0,len(self.playery),1):
            if (self.playerx[i] == cat.hitx) and (self.playery[i] == cat.hity):
                cat.Random()
                self.Append()
                self.Append()
                soundmeow.play()
                print("cat shot")
                Sleep -=0.1 

    def Blit(self):
        # print("x = ",self.playerx)
        # print("y = ",self.playery)
        self.CheckLocation()
        for i in range(0,len(self.playery),1):
            screen.blit(self.player, (self.playerx[i], self.playery[i]))
        print("x= ",self.playerx[0],",",self.playerx[1],",",self.playerx[2])
        print("y= ",self.playery[0],",",self.playery[1],",",self.playery[2])

def play_background_music():
    pygame.mixer.music.load('BIMINI, Avi Snow - No Way (with Avi Snow) [NCS Release].mp3')
    pygame.mixer.music.play(-1, 0)

def GetJoystickAxis(): #Running in thread
    global x,y
    while running:
        y = joystick.get_axis(1)
        x = joystick.get_axis(0)    

def GetKeys():
    global x,y,Sleep,state,running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                x=0
                y=-1
            if keys[pygame.K_DOWN]:
                x=0
                y=1
            if keys[pygame.K_LEFT]:
                x=-1
                y=0
            if keys[pygame.K_RIGHT]:
                x=1
                y=0
            if keys[pygame.K_1] or keys[pygame.K_KP1]:
                print("1111111111111111111111")
                Sleep = 0.7
            if keys[pygame.K_2] or keys[pygame.K_KP2]:
                Sleep = 0.7
            if keys[pygame.K_3] or keys[pygame.K_KP3]:
                Sleep = 0.7
            if keys[pygame.K_s]:
                state = 1
        if event.type == pygame.JOYBUTTONDOWN:
            #print(f"Motion on joystick {event.instance_id}")
            if event.button == 1:
                if joystick.get_button(1) > 0.5:
                    pass
                elif joystick.get_button(1) < -0.5:
                    pass

def Start():
    while state ==0:
        print("hello")
        screen.fill("Green") 
        font = pygame.font.SysFont('arial', 30) 
        line1 = font.render(f"Kies moeilijkheid ", True, (255, 255, 255)) 
        screen.blit(line1, (200, 300)) 
        line2 = font.render("Makkelijk = 0.7s (1) / Middel = 0.5s (2) / Moeilijk = 0.3s (3) ", True, (255, 255, 255)) 
        screen.blit(line2,(200, 350)) 
        pygame.display.flip()
        GetKeys() 

def End():
    screen.fill("Green") 
    font = pygame.font.SysFont('arial', 30) 
    line1 = font.render(f"Game is over! Your score is {len(player.playerx)-3}", True, (255, 255, 255)) 
    screen.blit(line1, (200, 300)) 
    line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255)) 
    screen.blit(line2,(200, 350)) 
    pygame.display.flip() 
    time.sleep(999)

def Blit():
    screen.fill("Green")
    screen.blit(ImageBackground,(0,0))
    player.MovePlayerState()
    balloon.Blit()
    cat.Blit()
    player.Blit()
    pygame.display.flip()

balloon = Hit('balloon.png',Gridsize,ScreenSize)
cat = Hit('kitten.png',Gridsize,ScreenSize)
player = Player('sword.png',Gridsize,ScreenSize)


ImageBackground = pygame.image.load('background.jpg')
ImageBackground = pygame.transform.scale(ImageBackground, ScreenSize)

t1 = threading.Thread(target=GetJoystickAxis, args=())

state = 0
try:
    t1.start()
except:
    print("No Joysticks connected")
    pass

try:
    Start()
    while running:
        GetKeys()
        Blit()
        time.sleep(Sleep)
    End()

    

except KeyboardInterrupt:
    running = 0
    t1.join()
    pygame.quit()
