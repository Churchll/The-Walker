#Pygame
from pygame import *
from random import *

# -------- Classes + Functions ----------- #
## Class used to setup game variables and background functions
class Game:
    def __init__(self):
        ## setting screen dimensions to 1280x720
        self.screen = display.set_mode((1280,720))
        self.menu = 'main'
        self.arena = Rect(55,115,1150,500)
        #Level Details
        self.lvlMultiplyer = 3
        self.lvl = 1
        self.clock = time.Clock()

          ##TIMERS
        self.fspeed = 0
        self.frame = 0
        
        ## IMAGES ##
        ## Import Menus
        self.title = []
        for i in range(20):
            self.title.append(image.load("Graphics/Menus/Main/main(%d).png" % i))
        self.gameplay = image.load("Graphics/Menus/Play/background.png")
        self.healthPic = image.load("Graphics/Sprites/Health/hpsprite.png")
        self.noHealthPic = image.load("Graphics/Sprites/Health/nohp.png")
        ## Import Drops
        self.drops = [] ##Available Drops
        self.nodrops = [] ##Doesnt have Drops
        for i in range(5):
            self.drops.append(image.load("Graphics/Sprites/Drops/Available/drop(%d).png" % i))
            self.nodrops.append(image.load("Graphics/Sprites/Drops/None/drop(%d).png" % i))
        self.chest = image.load("Graphics/Sprites/Drops/chest(0).png")
        self.lockchest = image.load("Graphics/Sprites/Drops/chest(1).png")
        ## Import Living Sprites
        self.psprite = [] ##Player Sprites
        self.pasprite = [] ##Player Attack Sprite
        self.bug = [] ##Bug Sprites
        self.ghost = [] ##Ghost Sprites
        self.worm = [] ##Worm Sprites
        for i in range(9):
            self.pasprite.append(image.load("Graphics/Sprites/Entities/Player/Attack/g(%d).png" % i))
        for i in range(2):
            self.psprite.append(image.load("Graphics/Sprites/Entities/Player/Docile/g(%d).png" % i))
        for i in range(2):
            self.bug.append(image.load("Graphics/Sprites/Entities/Enemies/bug(%d).png" % i))
            self.ghost.append(image.load("Graphics/Sprites/Entities/Enemies/ghost(%d).png" % i))
            self.worm.append(image.load("Graphics/Sprites/Entities/Enemies/worm(%d).png" % i))
        ## Enemy Attacks
        self.laser = []
        for i in range(2):
            self.laser.append(image.load("Graphics/Sprites/Entities/Enemies/Attacks/laser(%d).png" % i))
        ## Perks
        self.perk = []
        self.noperk = []
        for i in range(5):
            self.perk.append(image.load("Graphics/Sprites/Drops/Available/drop(%d).png" % i))
            self.noperk.append(image.load("Graphics/Sprites/Drops/None/drop(%d).png" % i))
        ## Environment
        self.cloud = []
        for i in range(3):
            self.cloud.append(image.load("Graphics/Sprites/Environment/cloud(%d).png" % i))
            
        ## SOUND EFFECTS ##
        self.fx = []
        self.playMusic = False
        for i in range(9):
            self.fx.append(mixer.Sound("Graphics/Sound/FX/fx(%d).ogg" % i))
    ## Used to get key input     
    def eventLoop(self):
        global running
        self.spacebar = False
        for e in event.get():
            if e.type == QUIT:
                running - False
            if e.type == KEYDOWN:
                if e.key == K_LEFT:
                    p.speed[0] = -5
                elif e.key == K_RIGHT:
                    p.speed[0] = 5
                elif e.key == K_UP:
                    p.speed[1] = -5
                elif e.key == K_DOWN:
                    p.speed[1] = 5
                if self.spacebar != True:
                    if e.key == K_SPACE:
                        self.spacebar = True
            elif e.type == KEYUP:
                p.speed[0] = 0
                p.speed[1] = 0
                self.spacebar = False
    ## Distance Formula          
    def dist(self,coord1,coord2):
        return ((coord1[0]-coord2[0])**2 + (coord1[1]-coord2[1])**2)**0.5
    ## Actually runs the game ~ Chooses menu based on game.menu()    
    def play(self):
        if self.menu == 'main':
            menu.mainDraw()
            music.playTitle()
            if game.spacebar == True:
                music.fadeOut()
                animateMenu.fadeOut()
                game.playMusic = True
                self.menu = 'play'
        if self.menu == 'play':
            menu.gameDraw()
            menu.powerDraw()
            menu.healthDraw()
            animateMenu.fadeIn()
            

            p.drawPlayer()
            p.movePlayer()
            p.atkPlayer()

            enemy.genEnemy()
            enemy.drawEnemy()
            enemy.moveEnemy()

            collision.collDetect()
            music.playGame()


## Class containing all in game menus
class Menu():
    ## Draws and animates the main titlescreen

    def mainDraw(self):
        animateMenu.main()
    ## Draws the game screen
    def gameDraw(self):
        game.screen.blit(game.gameplay,(0,0))
    ## HUD ~ Draws Powerups, coins etc.
    def powerDraw(self):
        for i in range(5):
            game.screen.blit(game.noperk[i],(905 + i*(75),20))
    ## Health Bar ~ Updates Player Health
    def healthDraw(self):
        if p.hp > 0:
            for i in range(round(p.hp/10)):
                game.screen.blit(game.healthPic,(20+ i*(50),20))
            for i in range(10):
                game.screen.blit(game.noHealthPic,(20+ i*(50),20))
        if p.hp <= 0:
            mixer.music.fadeout(1000)
            animateMenu.fadeOut()
            main()
            

## Class Relating to Animated Menu Effects
class menuAnimations():
    def __init__(self):
        self.fspeed = 0
        self.frame = 0
        self.background = Surface(game.screen.get_size())
        menu.stop = False
        self.fade = True
        self.drawParticles = False
    ## Main Menu ~ Circulates through Titlescreen animations    
    def main(self): 
        game.screen.blit(game.title[self.frame],(0,0))
        if self.fspeed == 15:
            self.frame += 1
            self.fspeed = 0
        if self.frame == 20:
            self.frame = 0
        self.fspeed += 3
    ## Fade Out Menu Effect    
    def fadeOut(self):
        self.background.fill((0,0,0))
        self.background.set_alpha(0)
        ## Changes opacity of black screen to opaque
        for i in range(255):
            self.background.set_alpha(i)
            game.screen.blit(self.background,(0,0))
            display.flip()
            time.wait(25)
    ## Changes opacity of black screen to transparent
    def fadeIn(self):
        if self.fade == True:
            self.background.fill((0,0,0))
            self.background.set_alpha(255)
            ## Checks if spacebar is pressed to exit menu
            for i in range(255,0,-5):
                self.background.set_alpha(i)
                game.screen.blit(game.gameplay,(0,0))
                game.screen.blit(self.background,(0,0))
                display.flip()
            self.fade = False
    ## Adds cloud effect to gameplay
    def cloudEff(self):
        if self.drawParticles == True:
            self.partX = enemy.loc[collision.currentObject][0]
            self.partY = enemy.loc[collision.currentObject][1]
            for i in range(50):
                draw.rect(screen, (0,0,0), (self.partX,self.partY,10,10), 0)
                self.partX+=1
                self.partY+=1
            self.drawParticles == False

            
## Class Relating to in game music
class Music():
    def __init__(self):
        self.changespeed = 0
    ## Plays main title music
    def playTitle(self):
        if game.playMusic == True:
            mixer.music.load("Graphics/Sound/theme.ogg")
            mixer.music.play()
        game.playMusic = False
    def playGame(self):
        if game.playMusic == True:
            mixer.music.load("Graphics/Sound/dungeon.ogg")
            mixer.music.play()
        game.playMusic = False
    ## Fades music out with sound effect
    def fadeOut(self):
        mixer.music.fadeout(1000) 
        game.fx[0].play()


## Class Used to track mouse information
class Mouse:
    def __init__(self,loc,b):
        self.loc = loc
        self.b = b
    ## Gets the Mouses cursor location
    def getCursor(self):
        self.b = mouse.get_pressed()
        if self.b[0] == 1:
            self.loc = mouse.get_pos()


## Class pertaining to the player      
class Player:
    def __init__(self,name,loc,speed,hp,perks,frame,score):
        self.name = name
        self.loc = loc
        self.speed = speed
        self.hp = hp
        self.perks = perks
        self.frame = frame
        self.score = score
        self.atkframe = frame
        
        self.fspeed = 0
        self.fatkspeed = 0
        self.attack = False
        
    def drawPlayer(self):
        if self.attack != True:
            game.screen.blit(game.psprite[self.frame],(self.loc[0],self.loc[1]))
            if self.fspeed == 15:
                self.frame += 1
                self.fspeed = 0
            if self.frame == 2:
                self.frame = 0
            self.fspeed += 1
    def movePlayer(self):
        if game.arena.collidepoint(self.loc):
            if game.arena.collidepoint((self.loc[0] + self.speed[0]),(self.loc[1] + self.speed[1])):
                self.loc[0] += self.speed[0]
                self.loc[1] += self.speed[1]
                self.hitBox = (self.loc[0],self.loc[1], 77, 77)
                #draw.rect(game.screen,(0,0,0),p.hitBox,0) <-- Visually demonstrates size of hitbox
    def atkPlayer(self):
        if game.spacebar == True:
            self.attack = True
        if self.attack == True:
            game.screen.blit(game.pasprite[self.atkframe],(self.loc[0],self.loc[1]))
            if self.atkframe == 0:
                game.fx[8].play()
            if self.fatkspeed == 15:
                self.atkframe += 1
                self.fatkspeed = 0
            if self.atkframe == 8:
                self.atkframe = 0
                self.attack = False
            self.fatkspeed += 5


## Class pertaining to the enemies
class Enemy:
    def __init__(self):
        self.enemy = [game.bug,game.worm,game.ghost]
        self.totalEnemies = 0
        self.x = []
        self.etype = []
        
        self.loc = []
        self.height = []
        self.width = []
        self.speed = []
        self.eHitBox = []
        
        self.frame = 0
        self.fspeed = 0
        
    def genEnemy(self):
        if self.totalEnemies < 5:
            self.gen = True
        if self.totalEnemies >= 5:
            self.gen = False
        if self.gen == True:
            for i in range(6):
                self.x.append(randint(0,2))
                self.etype.append(self.enemy[self.x[i]])
                self.loc.append([1280,randint(115,500)])
                self.height.append(self.loc[i][1] - self.etype[i][self.frame].get_height())
                self.width.append(self.loc[i][0] + self.etype[i][self.frame].get_width())
                self.eHitBox.append(Rect(self.loc[i][0],self.loc[i][1],self.width[i],self.height[i]))
                self.speed.append(randint(1,6))
            self.gen = False
    def drawEnemy(self):
        for i in range(6):
            game.screen.blit((self.etype[i][self.frame]),(self.loc[i]))
    #        self.ghostAtk()
            if self.fspeed == 30:
                self.frame += 1
                self.fspeed = 0
            if self.frame == 2:
                self.frame = 0
            self.fspeed += 1
    #def ghostAtk(self):
    #    for i in range(6):
    #        if self.frame == 1 and self.etype[i] == game.ghost:
    #            self.atkObject = i
    #            self.chance = randint(1,500)
    #            if self.chance == 1 and self.loc[self.atkObject][0] < 1000:
    #                game.screen.blit(game.laser[0],((self.loc[self.atkObject][0] + self.fireSpeed),self.loc[self.atkObject][1] + 13))
    def resetPos(self):
        self.totalEnemies-=1
        self.x[collision.currentObject] = randint(0,2)
        self.etype[collision.currentObject] = (self.enemy[self.x[collision.currentObject]])
        self.loc[collision.currentObject] = [1280,randint(115,500)]
        self.speed[collision.currentObject] = randint(1,6)
    def moveEnemy(self):
        for i in range(6):
            self.getHitbox()
            self.loc[i][0] -= self.speed[i]
            if self.loc[i][0] < -50:
                self.totalEnemies-=1
                self.x[i] = randint(0,2)
                self.etype[i] = (self.enemy[self.x[i]])
                self.loc[i] = [1280,randint(115,500)]
                self.speed[i] = randint(1,6)
                p.hp -= 10
    def getHitbox(self):
        for i in range(6):
            self.height[i] = (self.etype[i][self.frame].get_height())
            self.width[i] = (self.etype[i][self.frame].get_width())
            self.eHitBox[i] = (Rect(self.loc[i][0],self.loc[i][1],self.width[i],self.height[i]))
            #draw.rect(game.screen,(250,250,250),enemy.eHitBox[i],0) <-- Visually demonstrates size of hitbox

class Collision:
    def __init__(self):
        self.currentObject = 0
    def collDetect(self):
        for i in range(6):
            if enemy.eHitBox[i].colliderect(p.hitBox) and p.attack == True:
                self.currentObject = i
                p.score += 10
                #animateMenu.drawCloud = True
                #animateMenu.cloudEff()
        enemy.resetPos()
                
            
## Runs Main Program
def main():
    global running,game,play,menu,animateMenu,music,enemy,collision,p,m
    init()
    mixer.init()
    running = True

    #Mouse1 = Mouse((x,y,),Buttondown(0))
    m = Mouse((0,0),0)
    #Player1 = Player(name(p1),(x,y),(xspeed,yspeed),health(100),(perk1,perk2,perk3),frame(0))
    p = Player('p1',[80,360],[0,0],100,(0,0,0),0,0)
    game = Game() 
    enemy = Enemy()
    collision = Collision()
    menu = Menu()
    music = Music()
    animateMenu = menuAnimations()

    display.set_caption("~The Adventures of Goosh~")
    game.playMusic = True
    while running:
        game.eventLoop()
        game.play()
        display.flip()
    quit()

main()

