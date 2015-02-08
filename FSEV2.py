from pygame import *
from random import *
from time import sleep
import os

class Game:
    def __init__(self,menu):
        self.menu = menu
        self.screen = display.set_mode((1280,720))
        self.spaceDown = False
        self.totalNpc = 0 # Amount of NPC's on screen
        self.eg = [] # List of all enemy graphics
        self.enemies = [] # List of all enemy objects
        self.gui = [[]]
        os.chdir("Sprites/Enemies")
        for f in range(len(os.listdir()) - 1):
            self.eg.append([])
            os.chdir("e(%d)" % f)
            for i in range(len(os.listdir()) - 1):
                self.eg[f].append(image.load("e(%d).png" % i))
            os.chdir('..')
        os.chdir('../..')
        for i in range(2):
            self.gui[0].append(image.load("Sprites/Health/hp(%d).png" % i))
            
    def eventLoop(self):
        for e in event.get():
            if e.type == QUIT:
                running = False
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    self.spaceDown = True
            if e.type == KEYUP:
                self.spaceDown = False
                
    def spawnEnemy(self):
        for i in range(round(5*p.stats[DIF])-self.totalNpc):
            self.enemies.append(enemy([],[],[],[],[]))
            self.enemies[i].vel = [randint(5,15),0]  ## Generate Starting Velocity
            self.totalNpc += 1  ## Choose a random enemy
            x = randint(0,10)
            if x < 8:
                self.enemies[i].type = self.eg[0]
            else:
                self.enemies[i].type = self.eg[1]
            self.enemies[i].frame = [0,0]
            self.enemies[i].pos = [1350,530]
            if self.enemies[i].type  == self.eg[ROCK]:
                self.enemies[i].pos = [1350,530]
                self.enemies[i].hBox = Rect([self.enemies[i].pos[X],self.enemies[i].pos[Y]+60,self.enemies[i].type[game.enemies[i].frame[0]].get_width(),self.enemies[i].type[game.enemies[i].frame[0]].get_height()-45])
            elif self.enemies[i].type == self.eg[BEE]:
                self.enemies[i].pos = [1300,randint(150,550)]  ## Generate Starting Position
                self.enemies[i].hBox = Rect([self.enemies[i].pos[X],self.enemies[i].pos[Y],self.enemies[i].type[game.enemies[i].frame[0]].get_width(),self.enemies[i].type[game.enemies[i].frame[0]].get_height()])
        self.gen = False
        
    def run(self):
        global i
        if self.menu == "Main":
            m.draw()
            m.menuSelect()
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
            if w.platGen:
                w.genPlat()
            if w.platGen == False:
                for i in range(len(w.plat)):
                    w.drawPlat()
                    w.movePlat()
            p.drawPlayer()
            p.tracePlayer()
            if self.gen: 
                self.spawnEnemy()
            for i in range(len(game.enemies)):
                if len(game.enemies) > 0 and self.gen == False:
                    game.enemies[i].drawEnemy()
                    game.enemies[i].moveEnemy()


class mainMenu:
    def __init__(self):
        self.mainFrame = 0
        self.mainSpeed = 0
        self.hairFrame = 0
        self.hairSpeed = 0
        self.main = []
        for i in range(20):
            self.main.append(image.load("Map/Main/main(%d).png" % i).convert())
        self.hair = []
        for i in range(4):
            self.hair.append(image.load("Map/Main/hair(%d).png" % i))
        self.beeFrame = [0,0]
        
    def draw(self):
        game.screen.blit(self.main[self.mainFrame],(0,0))
        game.screen.blit(self.hair[self.hairFrame],(65,365))
        game.screen.blit(game.eg[BEE][self.beeFrame[0]],(200,160))
        game.screen.blit(game.eg[BEE][self.beeFrame[0]],(150,225))
        game.screen.blit(game.eg[BEE][self.beeFrame[0]],(100,110))
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
        self.back = image.load("background.png").convert()
        self.backLava = image.load("backlava.png").convert()
    def draw(self):
        if w.ground == "Grass" or w.ground == "Mountain":
            game.screen.blit(self.back,(0,0))
        elif w.ground == "Lava":
            game.screen.blit(self.backLava,(0,0))
        self.drawHealth()
        
    def drawHealth(self):
        if p.stats[HP] > 0:
            for h in range(round(p.stats[HP]/10)):
                game.screen.blit(game.gui[0][0],(20+ h*(50),20))
            for h in range(10):
                game.screen.blit(game.gui[0][1],(20+ h*(50),20))


class Fx:
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


class Music:
    def __init__(self):
        self.play = True
        
    def playMain(self, loops = -1, pos= 0.0):
        mixer.music.load("Music/main.mp3")
        mixer.music.play(loops, pos)
        
    def playGame(self,loops = -1, pos= 0.0):
        mixer.music.load("Music/back.mp3")
        mixer.music.play(loops, pos)


class platform:
    def __init__(self,pos,hBox,pType):
        self.pos = pos
        self.hBox = hBox
        self.type = pType


        
class world:
    def __init__(self,gen,world,ground,pos,width):
        self.gen = gen
        self.world = world
        self.pos = pos
        self.width = width
        self.ground = ground
        self.biomes = [[],[],[]]
        self.platGen = True
        self.plat = []
        self.platImg = []
        for i in range(4):
            self.platImg.append(image.load("Map/Platforms/p(%d).png" % i))
        self.i = 0
        for i in range(5):
            self.biomes[0].append(image.load("Map/Biomes/Grass/biome(%d).png" % i).convert())
        for i in range(6):
            self.biomes[1].append(image.load("Map/Biomes/Lava/biome(%d).png" % i).convert())
        for i in range(1):
            self.biomes[2].append(image.load("Map/Biomes/Mountain/biome(%d).png" % i).convert())
            
    def updateMap(self):
        if p.move:
            for i in range(len(self.world)):
                self.world[i][1][X]-= p.vel[X]
        for i in range(len(self.world)):
            game.screen.blit(self.world[i][0],self.world[i][1])
           
    def genMap(self):
        if self.gen:
            for i in range(15):
                if self.ground == "Grass":
                    x = randint(0,4)
                    self.world.append((self.biomes[0][x],[self.width,400]))
                    self.width+= self.biomes[0][x].get_width()
                elif self.ground == "Lava":
                    x = randint(0,5)
                    self.world.append((self.biomes[1][x],[self.width,400]))
                    self.width+= self.biomes[1][x].get_width()
                elif self.ground == "Mountain":
                    x = randint(0,0)
                    self.world.append((self.biomes[2][x],[self.width,400]))
                    self.width+= self.biomes[2][x].get_width()
            self.gen = False
        if self.world[-1][1][X] - p.stats[STEPS] < 1280 and self.gen == False:
            self.width = self.world[-1][1][X]
            self.gen = True
        if p.stats[STEPS] > 50000:
            self.ground = "Lava"

    def genPlat(self):
        self.plat.append(platform([],[],[]))
        self.plat[0].pos = [1320, randint(430,530)]
        self.plat[0].hBox = Rect([self.plat[0].pos[X],self.plat[0].pos[Y], 100, 20])
        self.plat[0].type = self.platImg[0]
        p = randint(15,25)
        for i in range(1,p):
            self.plat.append(platform([],[],[]))
            y = self.plat[-2].pos[Y] + randint(-100,100)
            if y < 100:
                y = self.plat[-2].pos[Y] + randint(100,150)
            elif y > 500:
                y = self.plat[-2].pos[Y] - randint(100,150)
            self.plat[i].pos = [self.plat[-2].pos[X] + randint(200,300),y]
            self.plat[i].hBox = Rect([self.plat[i].pos[X],self.plat[i].pos[Y],100,20])
            if w.ground == "Grass":
                self.plat[i].type = self.platImg[randint(0,2)]
            else:
                self.plat[i].type = self.platImg[3]
        self.platGen = False

    def movePlat(self):
        if self.plat[i].hBox.collidepoint((p.pos[X]+50,p.pos[Y]+80)):
            p.pos[Y] = self.plat[i].hBox[Y] - 80
            p.stand = True
            p.vel[Y] = 0
            p.dJump = 0
        if p.move:
            self.plat[i].pos[X] -= p.vel[X]
            self.plat[i].hBox[X] -= p.vel[X]
        if self.plat[-1].pos[X] < -100:
            self.plat = []
            self.platGen = True
        
    def drawPlat(self):
        game.screen.blit(self.plat[i].type,(self.plat[i].pos[X],self.plat[i].pos[Y]))
        #draw.rect(game.screen,(250,250,250),self.plat[i].hBox,1)
                    


class player:
    def __init__(self,pos,act,vel,frame,stats):
        self.pos = pos
        #self.hBox = hBox
        self.act = act
        self.vel = vel
        self.frame = frame
        self.stats = stats
        self.char = []
        self.move = self.act[0]
        self.jump = self.act[1]
        self.dJump = self.act[2]
        self.atk = self.act[3]
        self.stand = self.act[4]
        for f in range(len(os.listdir('Sprites/Main/Movement'))-1):
            self.char.append([])
            for i in range(3): 
                self.char[f].append(image.load("Sprites/Main/Movement/c(%d)/movement(%d).png" % (f,i)))
        self.hBox = Rect([self.pos[0],self.pos[1],self.char[0][0].get_width(),self.char[0][0].get_height()])
        
    def movePlayer(self):
        keys = key.get_pressed()
        # Moving the player
        if keys[K_RIGHT]:
            self.move = True
            self.vel[X] = 10
            self.stats[STEPS]+= 10
        elif keys[K_LEFT]:
            self.move = True
            self.vel[X] = -10
        else:
            self.move = False
        if keys[K_UP] and self.dJump <= 2:
            self.jump = True
            self.dJump+=1
            self.vel[Y] = 15
        else:
            self.jump = False
        self.hBox = Rect([p.pos[0]+25,p.pos[1]+17,self.char[0][0].get_width()-50,self.char[0][0].get_height()-30])
        self.pos[Y]-=self.vel[Y]   
        if self.pos[Y] >= 535:
            self.pos[Y] = 535
            self.vel[Y] = 0
            self.dJump = 0
        self.vel[Y]-=1.3
        
        
    def drawPlayer(self):
        if self.move or self.jump:
            if self.frame[1] == 3:
                self.frame[0] += 1
                self.frame[1] = 0
            if self.frame[0] == 3:
                self.frame[0] = 0
            self.frame[1] += 1
            game.screen.blit(cm.name[self.frame[0]],self.pos)
        else:
            game.screen.blit(cm.name[0],self.pos)
        #draw.rect(game.screen,(250,250,250),p.hBox,1)

    def tracePlayer(self):
        if self.stats[HP] <= 0:
            mixer.music.fadeout(1000)
            fx.fadeOut()
            main()
        if self.stats[STEPS] == 10000*self.stats[DIF]:
            print(self.stats[DIF])
            self.stats[DIF] += 0.5

class enemy:
    def __init__(self,eType,ePos,eVel,hBox,eFrame):
        self.type = eType
        self.pos = ePos
        self.vel = eVel
        self.frame = eFrame
        self.hBox = hBox
        self.reset = False
        self.curEnemy = 0
        self.passed =0
    def moveEnemy(self):
        if game.enemies[i].type == game.eg[ROCK] and p.move:
            game.enemies[i].pos[X] -= p.vel[X]
            game.enemies[i].hBox[X] -= p.vel[X]
        if game.enemies[i].type == game.eg[BEE]:
            if p.vel[X] > 0:
                game.enemies[i].pos[X] -= game.enemies[i].vel[X] + p.vel[X]
                game.enemies[i].hBox[X] -= game.enemies[i].vel[X] + p.vel[X]
            elif p.vel[X] < 0:
                game.enemies[i].pos[X] -= game.enemies[i].vel[X] - p.vel[X]
                game.enemies[i].hBox[X] -= game.enemies[i].vel[X] - p.vel[X]
        # Checking if there is a collision
        if p.hBox.colliderect(game.enemies[i].hBox):
            self.reset = True
            self.resetPosEnemy()
            if self.reset == False:
                p.stats[HP] -= 10
        for e in range(len(game.enemies)):
            if game.enemies[e].pos[X] < -100:
                self.passed+=1
            else:
                self.passed = 0
        if self.passed >= len(game.enemies):
            game.totalNpc = 0
            game.enemies = []
            game.gen = True         

    def drawEnemy(self):
        if game.enemies[i].frame[1] == 3:
            game.enemies[i].frame[0] += 1
            game.enemies[i].frame[1] = 0
        if game.enemies[i].frame[0] == len(game.enemies[i].type):
            game.enemies[i].frame[0] = 0
        game.enemies[i].frame[1]+=1
        game.screen.blit(game.enemies[i].type[game.enemies[i].frame[0]],game.enemies[i].pos)
        #draw.rect(game.screen,(250,250,250),game.enemies[i].hBox,1)
        
    def resetPosEnemy(self):
        self.curEnemy = i
        if self.reset:
            x = randint(0,10)
            if x < 8:
                game.enemies[i].type = game.eg[0]
            else:
                game.enemies[i].type = game.eg[1]
            game.enemies[self.curEnemy].frame = [0,0]
            if game.enemies[self.curEnemy].type == game.eg[ROCK]:
                game.enemies[self.curEnemy].pos = [1300,530]  ## Generate Starting Position
                game.enemies[self.curEnemy].hBox = Rect([game.enemies[self.curEnemy].pos[X],game.enemies[self.curEnemy].pos[Y]+60,game.enemies[self.curEnemy].type[game.enemies[self.curEnemy].frame[0]].get_width(),game.enemies[self.curEnemy].type[game.enemies[self.curEnemy].frame[0]].get_height()-45])
            elif game.enemies[self.curEnemy].type == game.eg[BEE]:
                game.enemies[self.curEnemy].pos = [1300,randint(150,550)]  ## Generate Starting Position
                game.enemies[self.curEnemy].hBox = Rect([game.enemies[self.curEnemy].pos[X],game.enemies[self.curEnemy].pos[Y],game.enemies[self.curEnemy].type[game.enemies[self.curEnemy].frame[0]].get_width(),game.enemies[self.curEnemy].type[game.enemies[self.curEnemy].frame[0]].get_height()])
            game.enemies[self.curEnemy].vel = [randint(5,30),0]
            self.reset = False

def main():
    global game,m,cm,gm,w,p,e,fx,music
    global X,Y
    global BEE,ROCK
    global NAME,HP,STEPS,SCORE,DIF
    global LEFT,RIGHT
    global HP
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
    DIF = 4
    # Character Select
    LEFT = 0
    RIGHT = 1
    init()
    mixer.init()
    running = True
    # Main Game Class
    game = Game("Main")
    game.gen = True
    # World and Entity Classes
    w = world(True,[],"Grass",[0,0],0)
    p = player([50,535],[False,False,0,False,False],[0,0],[0,0],['p1',100,10,0,1])
    # Menu Classes
    m = mainMenu()
    gm = gameMenu()
    cm = charMenu(p.char[2],[False,False],[[350,280],[450,280],[550,280],[650,280],[750,280]])
    # Music and Effect Classes
    fx = Fx()
    music = Music()
    music.play = False
    display.set_caption("~The Walker~")
    myClock = time.Clock()
    while running:
        game.eventLoop()
        game.run()
        display.flip()
        myClock.tick(25)
    quit()

main()
