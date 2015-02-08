from pygame import *
from random import *
from time import sleep
import os

class game:
    def __init__(self,menu):
        self.menu = menu
        self.screen = display.set_mode((1280,720))
        self.spaceDown = False
    def eventLoop(self):
        for e in event.get():
            if e.type == QUIT:
                running = False
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    self.spaceDown = True
            if e.type == KEYUP:
                self.spaceDown = False
    def run(self):
        if self.menu == "Main":
            main.draw()
            main.menuSelect()
        elif self.menu == "Select":
            cm.draw()
            cm.click()
            cm.switch()
            cm.menuSelect()
        elif self.menu == "Play":
            gm.draw()
            w.genMap()
            w.updateMap()
            p.movePlayer()
            p.drawPlayer()
            e.spawn()
            e.move()
            e.draw()

class mainMenu:
    def __init__(self):
        self.mainFrame = 0
        self.mainSpeed = 0
        self.hairFrame = 0
        self.hairSpeed = 0
        self.main = []
        for i in range(20):
            self.main.append(image.load("Map/Main/main(%d).png" % i))
        self.hair = []
        for i in range(4):
            self.hair.append(image.load("Map/Main/hair(%d).png" % i))
        self.beeFrame = [0,0]
    def draw(self):
        game.screen.blit(self.main[self.mainFrame],(0,0))
        game.screen.blit(self.hair[self.hairFrame],(65,365))
        game.screen.blit(e.enemy[BEE][self.beeFrame[0]],(200,160))
        game.screen.blit(e.enemy[BEE][self.beeFrame[0]],(150,225))
        game.screen.blit(e.enemy[BEE][self.beeFrame[0]],(100,110))
        # Menu Animation
        if self.mainSpeed == 6:
            self.mainFrame += 1
            self.mainSpeed = 0
        if self.mainFrame == 20:
            self.mainFrame = 0
        self.mainSpeed+= 3
        # Hair movement
        if self.hairSpeed == 6:
            self.hairFrame += 1
            self.hairSpeed = 0
        if self.hairFrame == 4:
            self.hairFrame = 0
        self.hairSpeed+= 2
        # Bee Movement
        if self.beeFrame[1] == 10:
            self.beeFrame[0] += 1
            self.beeFrame[1] = 0
        if self.beeFrame[0] == 2:
            self.beeFrame[0] = 0
        self.beeFrame[1]+= 2
    def menuSelect(self):
        if music.play:
            music.playMain()
            music.play = False
        if game.spaceDown == True:
            game.menu = "Select"
            sleep(.1)

class charMenu:
    def __init__(self,name,scroll,pos):
        self.name = name
        self.scroll = scroll
        self.pos = pos
        self.char = []
        for f in range(len(os.listdir('Sprites/Main/Movement'))-1):
            self.char.append([])
            for i in range(3): 
                self.char[f].append((image.load("Sprites/Main/Movement/c(%d)/movement(%d).png" % (f,i))))
        self.gui = image.load("Map/Select/select.png")
        self.background = Surface((1280,720))
        self.background.fill((85,177,255))
        for f in range(len(self.char)):
            for i in range(len(self.char[f])):
                self.char[f][i] = transform.scale(self.char[f][i],(self.char[f][i].get_width()*2,self.char[f][i].get_height()*2))
        self.filter = []
    def draw(self):
        game.screen.blit(self.background,(0,0))
        for i in range(len(self.char)):
            game.screen.blit(self.char[i][0],self.pos[i])
            if self.pos[i][X] == 550:
                cm.name = p.char[i]
        game.screen.blit(self.gui,(0,0))
    def click(self):
        keys = key.get_pressed()
        if keys[K_LEFT]:
            self.scroll[LEFT] = True
        else:
            self.scroll[LEFT] = False
        if keys[K_RIGHT]:
            self.scroll[RIGHT] = True
        else:
            self.scroll[RIGHT] = False
    def switch(self):
        if self.scroll[LEFT]:
            for i in range(len(self.pos)):
                self.pos[i][0] -= 100
                if self.pos[i][0] == 250:
                    self.pos[i][0] = 750
            sleep(.05)
        elif self.scroll[RIGHT]:
            for i in range(len(self.pos)):
                self.pos[i][0] += 100
                if self.pos[i][0] == 850:
                    self.pos[i][0] = 350
            sleep(.05)
    def menuSelect(self):
        if game.spaceDown == True:
            mixer.music.fadeout(1000)
            fx.fadeOut()
            fx.fade = True
            fx.fadeIn()
            music.play = True
            music.playGame()
            game.menu = "Play"

class gameMenu:
    def __init__(self):
        self.back = image.load("background.png")
    def draw(self):
        game.screen.blit(self.back,(0,0))

class fx:
    def __init__(self):
        self.fadeBackground = Surface((1280,720))
        self.fade = False
    ## Fade Out Menu Effect    
    def fadeOut(self):
        self.fadeBackground.fill((0,0,0))
        self.fadeBackground.set_alpha(0)
        ## Changes opacity of black screen to opaque
        for i in range(255):
            self.fadeBackground.set_alpha(i)
            game.screen.blit(self.fadeBackground,(0,0))
            display.flip()
            time.wait(25)
    ## Changes opacity of black screen to transparent
    def fadeIn(self):
        if self.fade == True:
            self.fadeBackground.fill((0,0,0))
            self.fadeBackground.set_alpha(255)
            ## Checks if spacebar is pressed to exit menu
            for i in range(255,0,-5):
                self.fadeBackground.set_alpha(i)
                game.screen.blit(gm.back,(0,0))
                game.screen.blit(self.fadeBackground,(0,0))
                display.flip()
            self.fade = False

class music:
    def __init__(self):
        self.play = True
    def playMain(self, loops = -1, pos= 0.0):
        mixer.music.load("Music/main.mp3")
        mixer.music.play(loops, pos)
    def playGame(self,loops = -1, pos= 0.0):
        mixer.music.load("Music/back.mp3")
        mixer.music.play(loops, pos)       
        
class world:
    def __init__(self,gen,world,ground,pos,width):
        self.gen = gen
        self.world = world
        self.pos = pos
        self.width = width
        self.biomes = []
        self.i = 0
        for i in range(5):
            self.biomes.append(image.load("Map/Biomes/biome(%d).png" % i))
    def updateMap(self):
        if p.move:
            for i in range(len(self.world)):
                self.world[i][1][X]-= p.vel[X]
        for i in range(len(self.world)):
            game.screen.blit(self.world[i][0],self.world[i][1])
    def genMap(self):
        if self.gen:
            for i in range(15):
                x = randint(0,4)
                self.world.append((self.biomes[x],[self.width,400]))
                self.width+= self.biomes[x].get_width()
            self.gen = False
        if self.world[-1][1][X] - p.stats[STEPS] < 1280 and self.gen == False:
            self.width = self.world[-1][1][X]
            self.gen = True

class player:
    def __init__(self,pos,act,vel,frame,stats):
        self.pos = pos
        self.act = act
        self.vel = vel
        self.frame = frame
        self.stats = stats
        self.char = []
        self.move = self.act[0]
        self.jump = self.act[1]
        self.dJump = self.act[2]
        self.atk = self.act[3]
        for f in range(len(os.listdir('Sprites/Main/Movement'))-1):
            self.char.append([])
            for i in range(3): 
                self.char[f].append(image.load("Sprites/Main/Movement/c(%d)/movement(%d).png" % (f,i)))
    def movePlayer(self):
        keys = key.get_pressed()
        if keys[K_RIGHT]:
            self.move = True
            self.vel[X] = 10
            self.stats[STEPS]+= 10
            if self.frame[1] == 3:
                self.frame[0] += 1
                self.frame[1] = 0
            if self.frame[0] == 3:
                self.frame[0] = 0
            self.frame[1] += 1
        else:
            self.move = False
        if keys[K_UP] and self.dJump <= 2:
            self.jump = True
            self.dJump+=1
            self.vel[Y] = 10
        else:
            self.jump = False
        self.pos[Y]-=self.vel[Y]   
        if self.pos[Y] >= 535:
            self.pos[Y] = 535
            self.vel[Y] = 0
            self.dJump = 0
        self.vel[Y]-=1.3   
    def drawPlayer(self):
        if self.move or self.jump:
            game.screen.blit(cm.name[self.frame[0]],self.pos)
        else:
            game.screen.blit(cm.name[0],self.pos)
  
class enemy:
    def __init__(self,gen,enemiesOnScreen,eType,ePos,eVel,eFrame):
        self.gen = gen
        self.eos = enemiesOnScreen
        self.enemy = eType
        self.pos = ePos
        self.vel = eVel
        self.frame = eFrame
        self.reset = False
        self.curEnemy = 0
        os.chdir("Sprites/Enemies")
        for f in range(len(os.listdir()) - 1):
            self.enemy.append([])
            os.chdir("e(%d)" % f)
            for i in range(len(os.listdir()) - 1):
                self.enemy[f].append(image.load("e(%d).png" % i))
            os.chdir('..')
        os.chdir('../..')
    def spawn(self):
        if len(self.eos) < 10:
            self.gen = True
        if self.gen:
            for i in range(10-len(self.eos)):
                self.vel.append([randint(5,15),0])  ## Generate Starting Velocity
                self.eos.append(self.enemy[randint(0,len(self.enemy)-1)])  ## Choose a random enemy
                self.frame.append([0,0])
                if self.eos[i] == self.enemy[ROCK]:
                    if self.pos[-1][X] > 1280:
                        self.pos.append([self.pos[-1][X] + randint(300,500),530])  ## Generate Starting Position
                    else:
                        self.pos.append([1350,530])
                elif self.eos[i] == self.enemy[BEE]:
                    self.pos.append([1300,randint(150,550)])  ## Generate Starting Position
            self.gen = False
    def move(self):
        for i in range(len(self.eos)):
            if self.eos[i] == self.enemy[ROCK] and p.move:
                self.pos[i][X] -= p.vel[X]
            if self.eos[i] == self.enemy[BEE]:
                self.pos[i][X] -= self.vel[i][X] + p.vel[X]
            if self.pos[i][X] < -100:
                self.curEnemy = i
                self.reset = True
                self.resetPos()
    def resetPos(self):
        if self.reset:
            self.eos[self.curEnemy] = (self.enemy[randint(0,len(self.enemy)-1)])
            if self.eos[self.curEnemy] == self.enemy[ROCK]:
                self.pos[self.curEnemy] = ([1300,530])  ## Generate Starting Position
            elif self.eos[self.curEnemy] == self.enemy[BEE]:
                self.pos[self.curEnemy] = ([1300,randint(150,550)])  ## Generate Starting Position
            self.vel[self.curEnemy] = [randint(5,15),0]
            self.frame[self.curEnemy] = [0,0]
            self.reset = False
    def draw(self):
        for i in range(len(self.eos)):
            if self.frame[i][1] == 3:
                self.frame[i][0] += 1
                self.frame[i][1] = 0
            if self.frame[i][0] == len(self.eos[i]):
                self.frame[i][0] = 0
            self.frame[i][1]+=1
            game.screen.blit(self.eos[i][self.frame[i][0]],self.pos[i])

def main():
    global game,main,cm,gm,w,p,e,fx,music
    global X,Y
    global BEE,ROCK
    global NAME,HP,STEPS,SCORE
    global LEFT,RIGHT
    # Movement
    X = 0
    Y = 1
    # Enemies
    BEE = 0
    ROCK = 1
    # Stats
    NAME = 0
    HP = 1
    STEPS = 2
    SCORE = 3
    # Character Select
    LEFT = 0
    RIGHT = 1
    init()
    mixer.init()
    running = True
    music.play = False
    # Main Game Class
    game = game("Main")
    # World and Entity Classes
    w = world(True,[],"Grass",[0,0],0)
    p = player([50,535],[False,False,0,False],[0,0],[0,0],['p1',100,0,0])
    e = enemy(True,[],[],[],[],[])
    # Menu Classes
    main = mainMenu()
    gm = gameMenu()
    cm = charMenu(p.char[2],[False,False],[[350,280],[450,280],[550,280],[650,280],[750,280]])
    # Music and Effect Classes
    fx = fx()
    music = music()
    display.set_caption("~The Walker~")
    while running:
        game.eventLoop()
        game.run()
        display.flip()
    quit()

main()
