from pygame import *
from random import *
from time import sleep
import os

# Class pertaining to the main game
class Game:
    def __init__(self,menu):
        self.menu = menu
        self.screen = display.set_mode((1280,720))
        self.spaceDown = False
        self.totalNpc = 0 # Amount of NPC's on screen
        self.eg = [] # List of all enemy graphics
        self.enemies = [] # List of all enemy objects
        self.gui = [[]] # List to hold all of the GUI attributes
        self.mPos = [0,0] # Contains the mouse position
        self.mb = [] # Keeps track if the mouse is pressed
        os.chdir("Sprites/Enemies")
        for f in range(len(os.listdir()) - 1): # Imports all of the images
            self.eg.append([])
            os.chdir("e(%d)" % f) # Changes directories to different enemy img folders
            for i in range(len(os.listdir()) - 1):
                self.eg[f].append(image.load("e(%d).png" % i)) # Appends the individual imgs
            os.chdir('..')
        os.chdir('../..') # Returns to the original general directory
        for i in range(2):
            self.gui[0].append(image.load("Sprites/Health/hp(%d).png" % i)) # Holds the heart imgs
        self.target = image.load("Sprites/Main/target.png") # Target img displayed on screen
        self.genDrops = False # Sets the drop generation to false at the beginning of the game
        self.drop = [] # Holds the drop imgs
        self.drop.append(image.load("Sprites/golfclub.png")) # Appends the golfclub drop
        self.drop.append(image.load("Sprites/timhortons.png")) # Appends the tim hortons cup drop
        self.font = font.SysFont(None, 36)
        self.wave = 0 # Initially sets the wave to 0
        self.waveDisplay = self.font.render("Wave: %s"%str(self.wave),1,(250,50,50)) # Displays the current wave
        self.bossBattle = False # Sets the boss battle to false in the beginning of the game
        self.genBoss = False # Doesnt allow the boss to spawn
        self.waveLen = .5 # Sets the wave time 
        self.waveTrack = 0 # Keeps track of the current wave

    # Controls the event loop
    def eventLoop(self):
        for e in event.get():
            if e.type == QUIT:
                running = False 
            if e.type == KEYDOWN:
                if e.key == K_SPACE: # Keep track if the spacebar is pressed
                    self.spaceDown = True
            if e.type == KEYUP:
                self.spaceDown = False 

    # Spawn the enemies contained in the game
    def spawnEnemy(self):
        for i in range(round(5*p.stats[DIF])-self.totalNpc): # Calculates how many enemies needs to be spawned according to the amount already on the screen
            self.enemies.append(Enemy([],[],[],[],[])) # Appends enemy objects to a list declared by the enemy class 
            self.enemies[i].vel = [randint(5,15),0]  ## Generate Starting Velocity
            self.totalNpc += 1  ## Choose a random enemy
            x = randint(0,10) # Createa  random value to store in x...
            if x < 8: # 80% chance the enemy will be a bee...
                self.enemies[i].type = self.eg[0]
            else: # 20% chance the enemy will be a rock...
                self.enemies[i].type = self.eg[1] 
            self.enemies[i].frame = [0,0] # Set the starting frame
            self.enemies[i].pos = [1350,530] # Set the starting position
            if self.enemies[i].type  == self.eg[ROCK]: # If the enemy is a rock...
                self.enemies[i].pos = [1350,530] # Spawn it on the ground... and create a hitbox according to the position
                self.enemies[i].hBox = Rect([self.enemies[i].pos[X],self.enemies[i].pos[Y]+60,self.enemies[i].type[game.enemies[i].frame[0]].get_width(),self.enemies[i].type[game.enemies[i].frame[0]].get_height()-45])
            elif self.enemies[i].type == self.eg[BEE]: # If the enemy is a bee...
                self.enemies[i].pos = [1300,randint(150,550)]  ## Generate a random y position and x offscreen, base hitbox off of pos
                self.enemies[i].hBox = Rect([self.enemies[i].pos[X],self.enemies[i].pos[Y],self.enemies[i].type[game.enemies[i].frame[0]].get_width(),self.enemies[i].type[game.enemies[i].frame[0]].get_height()])
        self.gen = False

    # Function used to spawn the boss
    def spawnBoss(self):
        global boss
        boss = (Boss([],[],[],[],[],100,[False,False])) # Generate the boss object...
        boss.pos = [1320,p.pos[Y]] # Set the position...
        boss.img = self.eg[2] # Which imgs it uses when drawn...
        boss.frame = [0,0] # Which frame it starts on...
        boss.hBox = Rect([boss.pos[X],p.pos[Y],boss.img[boss.frame[0]].get_width(),boss.img[boss.frame[0]].get_height()]) # The hit box..
        boss.vel = [30+p.stats[DIF]*5,10] # Starting velocity...
        self.bossBattle = True # Begin the boss battle
        self.genBoss = False # Stop generating the boss

    # Get the current mouse position
    def mouseGet(self):
        self.mb = mouse.get_pressed()
        self.mPos = mouse.get_pos()

    # Used to check if the current score is a highscore when the player dies...
    def checkScore(self,score): # Function takes in current score...
        data = [] # Create a data list to store highscores and names...
        temp = [[],[]] # This list is used to sort the data list...
        f = open('scores.txt','r+') # Open the file
        for line in f: # For every line in the file
            data.append(line[:-1]) # Append it to the list 'data'
        for i in range(10):
            if score > int(data[i]): # If the score > a current score...
                cur = i # Keep track of the score
                p.stats[NAME] = self.getName() # Call the getName() function to take in the players name, and set it 
                self.highScores(p.stats[NAME],p.stats[SCORE],data,temp,cur) # Call the highscore function to write to the text file
                break

    # Function used to write the new highscores to a text document... 
    def highScores(self,name,score,data,temp,cur): # Takes in the players name, score, data list, and the modified temp list, and the current lowest score
        for i in range(cur):
            temp[0].append(data[i]) # Up to the new score, add values to list...
            temp[1].append(data[20-(10-i)]) # Add names corresponding to value...
        temp[0].append(str(score)) # Add the new score
        temp[1].append(name) # Add the new score name
        for i in range(cur,10):
            temp[0].append(data[i]) # Append remaining scores to list
            temp[1].append(data[i+10]) # Append remaining names to list
        temp[0].remove(temp[0][-1]) # Remove lowest score
        temp[1].remove(temp[1][-1]) # Remove lowest player
        myFile = open("scores.txt","w") # Create a new scores file
        for f in range(2): # Write to the new file...
            for i in range(10):
                if i == 0 and f == 0:
                    myFile.write(temp[f][i]) # For the first score without a new line
                else:
                    myFile.write('\n%s'%temp[f][i]) # For the rest of the scores

    # Function used to take in the name of the current player
    def getName(self):
        ans = ""                    # Build the player name off of the answer string
        arialFont = font.SysFont("Times New Roman", 16) # Set the current font used
        txt2 = game.font.render("NEW HIGHSCORE!",1,(250,250,250)) # Render "New highscore"
        txt3 = game.font.render("Enter your name! (Press 'enter' to submit):",1,(250,250,250)) # Render " Enter your name" msg
        game.screen.blit(txt2,(360,280)) # Add both msgs to the screen for the player input
        game.screen.blit(txt3,(360,320))
        typing = True # While the user is typing
        while typing:
            for t in event.get():
                if t.type == QUIT:
                    event.post(t)   # puts QUIT back in event list so main quits
                    return ""
                if t.type == KEYDOWN:
                    if t.key == K_BACKSPACE:  # If the player clicks backspace, remove the last letter
                        if len(ans)>0:
                            ans = ans[:-1]
                            game.screen.fill((0,0,0)) # Blit black over it so it 'deletes'
                    elif t.key == K_KP_ENTER or t.key == K_RETURN : # If the player 'enters' stop typing
                        typing = False 
                    elif t.key < 256:
                        ans += t.unicode       # Adds typed characters to the ans variable
            txt = arialFont.render(ans, True, (250,250,250))   # Render the answer
            game.screen.blit(txt,(360,360)) # Blits all of the information to the screen
            game.screen.blit(txt2,(360,280))
            game.screen.blit(txt3,(360,320))
            display.flip()
        return ans

    # Function used to run the actual program
    def run(self):
        global i
        self.mouseGet() # Get the mouse position
        #self.highScores()
        if self.menu == "Main":
            m.draw()  # Draw the main menu
            m.menuSelect() # Allow the user to select the next menu if they press 'space'
        elif self.menu == "Select": 
            cm.draw() # Draw the character selection menu
            cm.click() # Control the selection with the A and D keys
            cm.switch() # Cycles through the characters on the screen
            cm.menuSelect() # Allows the user to select the next menu if they press 'h' or 'space'
        elif self.menu == "Highscores":
            hm.draw() # Draw the highscore page
            hm.menuSelect() # Allows the user to select the next menu on 'esc'
        elif self.menu == "Play":
            p.tracePlayer() # Get player information
            gm.draw() # Draw the menu
            w.genMap() # Generate the map
            w.updateMap() # Draw and move the map
            if game.wave == 0: # If the current wave is zero/ in tutorial mode
                tm.draw() # Draw the tutorial menu to explain controls
            p.movePlayer() # Move the player
            self.mouseGet() # Get mouse inputs
            ## IF THE WAVE ISNT 0
            if game.wave != 0:
                if w.platGen:
                    w.genPlat() # Generate platforms and drops
                    w.genDrop()
                if self.genDrops:
                    w.genDrop()
                if w.platGen == False:
                    for i in range(len(w.plat)): # For the amounts of platforms on the screen
                        w.drawPlat() # Draw platforms
                        w.movePlat() # Move platforms
                if self.genDrops == False:
                    for i in range(len(w.dropObj)):
                        w.moveDrop() # Draw platforms
                        w.drawDrop() # Move platforms   
            p.drawPlayer() # Draw player
            if game.wave != 0:
                if self.gen: 
                    self.spawnEnemy() # Spawn enemies
                for i in range(len(game.enemies)):
                    if len(game.enemies) > 0 and self.gen == False:
                        game.enemies[i].drawEnemy() #Draw Enemies
                        game.enemies[i].moveEnemy() # Move enemies
                if self.genBoss: # Generate the boss
                    self.spawnBoss()
                if self.bossBattle: # Move and draw the boss during the battle
                    boss.moveBoss()
                    boss.drawBoss()
            p.attack()


# Class pertaining to the drawing and functionality of the main menu
class MainMenu:
    def __init__(self):
        self.mainFrame = 0
        self.mainSpeed = 0
        self.hairFrame = 0
        self.hairSpeed = 0
        self.main = [] # Main menu sprites to fade text in and out
        for i in range(20):
            self.main.append(image.load("Map/Main/main(%d).png" % i).convert())
        self.hair = [] # Hair sprites to make hair appear to move
        for i in range(4):
            self.hair.append(image.load("Map/Main/hair(%d).png" % i))
        self.beeFrame = [0,0]

    # This function actually draws the main menu together    
    def draw(self):
        game.screen.blit(self.main[self.mainFrame],(0,0))
        game.screen.blit(self.hair[self.hairFrame],(65,365))
        game.screen.blit(game.eg[BEE][self.beeFrame[0]],(200,160))
        game.screen.blit(game.eg[BEE][self.beeFrame[0]],(150,225))
        game.screen.blit(game.eg[BEE][self.beeFrame[0]],(100,110))
        ## These if statements cycle through the frames of the images and rests them after a set amount
        ## of time
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

    ## This function allows the user to select the next menu and adds a transition as well as switches the background
    ## Music to the new updated song
    def menuSelect(self):
        if music.play:
            music.playMain()
            music.play = False
        if game.spaceDown == True: # if the spacebar is pressed
            game.menu = "Select" # Change the menu
            sleep(.1) # Delay so wrong menu isnt selected


# Class pertaining to the functionality of the character selection menu
class CharMenu:
    def __init__(self,name,scroll,pos):
        self.name = name
        self.scroll = scroll
        self.pos = pos
        self.char = []
        ## Load all of the character sprites and append them to the char list
        for f in range(len(os.listdir('Sprites/Main/Movement'))-1):
            self.char.append([])
            for i in range(3): 
                self.char[f].append((image.load("Sprites/Main/Movement/c(%d)/movement(%d).png" % (f,i))))
        self.gui = image.load("Map/Select/select.png")
        self.background = Surface((1280,720))
        self.background.fill((85,177,255))
        ## For all of the character sprites
        for f in range(len(self.char)):
            for i in range(len(self.char[f])):
                # Scale them down to a smaller size to be drawn to the menu
                self.char[f][i] = transform.scale(self.char[f][i],(self.char[f][i].get_width()*2,self.char[f][i].get_height()*2))
                
    ## Draw the entire menu
    def draw(self):
        game.screen.blit(self.background,(0,0)) # Draw the background
        for i in range(len(self.char)): # and all of the characters at the positions declared above
            game.screen.blit(self.char[i][0],self.pos[i])
            if self.pos[i][X] == 550:
                cm.name = p.char[i]
        game.screen.blit(self.gui,(0,0)) # Blit the surround gui

    ## Function used to control the character selection the main menu
    def click(self):
        keys = key.get_pressed()
        if keys[K_a]:
            self.scroll[LEFT] = True
        else:
            self.scroll[LEFT] = False
        if keys[K_d]:
            self.scroll[RIGHT] = True
        else:
            self.scroll[RIGHT] = False

    # Switch between the characters, cycles through the character selection
    def switch(self):
        if self.scroll[LEFT]: # If the user clicks left, characters shift left, last one resets to the right
            for i in range(len(self.pos)):
                self.pos[i][0] -= 100
                if self.pos[i][0] == 250:
                    self.pos[i][0] = 750
            sleep(.05)
        elif self.scroll[RIGHT]: # If the user clicks right, characters shift right, last one resets to the left
            for i in range(len(self.pos)):
                self.pos[i][0] += 100
                if self.pos[i][0] == 850:
                    self.pos[i][0] = 350
            sleep(.05)

    ## Allows the user to select the next menu from the current one
    def menuSelect(self):
        keys = key.get_pressed()
        # Moving the player
        if keys[K_h]: # Switch to the highscores page when 'h' is clicked
            game.menu = "Highscores"
        if game.spaceDown == True: # if the space bar is pressed...
            mixer.music.fadeout(1000) # Apply effects and switch the menu...
            fx.fadeOut()
            fx.fade = True
            fx.fadeIn()
            music.play = True
            music.playGame()
            game.menu = "Play"

## Class pertaining to the highscore menu functionality
class HighscoreMenu:
    def __init__(self):
        self.background = Surface((1280,720))
        self.background.fill((85,177,255))
        self.data = []
    ## Draw the highscore menu
    def draw(self):
        game.screen.blit(self.background,(0,0))
        f = open('scores.txt','r+') # Open the file
        for line in f: # For every line in the file
            self.data.append(line[:-1]) # Append it to the list 'data'
        game.font.set_bold(True)
        self.title = game.font.render("Highscores",1,(250,250,250)) # Display a highscore title
        game.screen.blit(self.title,(350,100))
        game.font.set_bold(False)
        for i in range(10):
            self.highScore = game.font.render(str(self.data[i]),1,(250,250,250)) # Render the names
            game.screen.blit(self.highScore,(350,100+50*(i+1))) # Blit the score names
        for i in range(10,20):
            self.highName = game.font.render(str(self.data[i]),1,(250,250,250)) # Render the scores
            game.screen.blit(self.highName,(550,100+50*(i-9))) # Blit the scores corresponding to the names
    ## Allows the user to select a different menu when the 'esc' key is pressed
    def menuSelect(self):
        keys = key.get_pressed()
        # Moving the player
        if keys[K_ESCAPE]:
            game.menu = "Select"

## Class pertaining to the drawing of the gameplay
class GameMenu:
    def __init__(self):
        self.back = image.load("background.png").convert()
        self.backLava = image.load("backlava.png").convert()
    ## Draws the gameplay
    def draw(self):
        if w.ground == "Grass" or w.ground == "Mountain": ## Draws the default back screen for other imgs to blitted to
            game.screen.blit(self.back,(0,0))
        elif w.ground == "Lava":
            game.screen.blit(self.backLava,(0,0))
        self.drawHealth() ## draw the player health gui...
        game.screen.blit(p.score,(1150,25)) ## display the score...
        game.screen.blit(game.waveDisplay,(1100,680)) ## display the current game wave
        if game.bossBattle: ## if there is a boss battle
            game.screen.blit(boss.hpDisplay,(1100,630)) # Display the bosses hp
    ## Draws the player health accoring to the percentage calculated...
    def drawHealth(self):
        if p.stats[HP] > 0:
            for h in range(round(p.stats[HP]/10)): ## Uses the percentage to determine the amount of hearts blitted
                game.screen.blit(game.gui[0][0],(20+ h*(50),20)) ## Blits transparent hearts
            for h in range(10): ## Blits filled hearts over top
                game.screen.blit(game.gui[0][1],(20+ h*(50),20))

## Class pertainging to the tutorial displayed in the beginning of the game
class TutorialMenu:
    def draw(self):
        ## Depending on the players distance away from the start, display instructions for the user
        if 0 < p.stats[STEPS] < 500:
            move = game.font.render("D - Move",1,(250,250,250))
            jump = game.font.render("W - Jump",1,(250,250,250))
            fall = game.font.render("LShift - Speedfall ",1,(250,250,250))
            aim = game.font.render("Use the mouse to aim!",1,(250,250,250))
            shoot = game.font.render("Summon rocks from the sky to smite da beeZ!",1,(250,250,250))
            game.screen.blit(move,(50,100))
            game.screen.blit(jump,(50,150))
            game.screen.blit(fall,(50,200))
            game.screen.blit(aim,(50,250))
            game.screen.blit(shoot,(50,300))
        elif 550 < p.stats[STEPS] < 750:
            ready = game.font.render("READY!?",1,(250,50,50))
            game.screen.blit(ready,(50,100))
        elif 750 < p.stats[STEPS] < 950:
            go = game.font.render("GOOOOO KILL DAAA BEEEEZ!",1,(250,50,50))
            game.screen.blit(go,(50,100))
        ## if the player takes more than 1000 steps, start the game and end the tutorial
        elif p.stats[STEPS] > 1000:
            game.wave+=1
            p.stats[STEPS] = 0

## Class relating to the effects used in the game
class Fx:
    def __init__(self):
        self.fadeBackground = Surface((1280,720))
        self.fade = False
        
    ## Fade Out Menu Effect
    def fadeOut(self):
        self.fadeBackground.fill((0,0,0)) # Fills screen black
        self.fadeBackground.set_alpha(0) # Set it to transparent
        for i in range(255):
            self.fadeBackground.set_alpha(i) ## Slowly make it less transparent to appear black and faded
            game.screen.blit(self.fadeBackground,(0,0))
            display.flip()
            time.wait(25)
            
    ## Changes opacity of black screen to transparent
    def fadeIn(self):
        if self.fade == True:
            self.fadeBackground.fill((0,0,0)) # Fills screen black
            self.fadeBackground.set_alpha(255)
            for i in range(255,0,-5): ## SLowly becomes transparent until it vanishes 
                self.fadeBackground.set_alpha(i)
                game.screen.blit(gm.back,(0,0))
                game.screen.blit(self.fadeBackground,(0,0))
                display.flip()
            self.fade = False


## Class containing functions that holds the music used in the game
class Music:
    def __init__(self):
        self.play = True
    def playMain(self, loops = -1, pos= 0.0): ## Continuosly loop, start in the beginning of the song
        mixer.music.load("Music/main.mp3") ## Import song
        mixer.music.play(loops, pos) # play the music
        
    def playGame(self,loops = -1, pos= 0.0):
        mixer.music.load("Music/boss2.wav")
        #mixer.music.load("Music/back.mp3")
        mixer.music.play(loops, pos)
        
    def playBoss(self,loops = -1, pos= 0.0):
        mixer.music.load("Music/boss2.wav")
        #mixer.music.play(loops, pos)


## Platform class that declares common platform characteristics
class Platform:
    def __init__(self,pos,hBox,pType,broken):
        self.pos = pos ## Platform location
        self.hBox = hBox ## Hitbox location
        self.type = pType ## Type of hitbox (ie. grass, cracked, stone)
        self.broken = broken ## Decides if the platform breaks when the user steps on it

class World:
    def __init__(self,gen,world,ground,pos,width):
        self.gen = gen  # Used to determine if the world continues to generate
        self.world = world # A list used to determing the current position of the world biome generation
        self.pos = pos # Sets the initial position of the world (0,0)
        self.width = width # Keeps track of the total width of the world
        self.ground = ground # Which ground is the player stepping on (ie. grass)
        self.biomes = [[],[],[]]  # Contains the biome imgs (Grass, Mountain, Lava)
        self.platGen = True # Start generating the platforms
        self.plat = [] # Used to hold platform objects
        self.lavaPlat = []
        self.dropObj = [] # List of drop objects
        self.platImg = [] # List containing platform imgs
        self.cur = ''
        for i in range(4):
            self.platImg.append(image.load("Map/Platforms/p(%d).png" % i))
        self.i = 0
        for i in range(5):
            self.biomes[0].append(image.load("Map/Biomes/Grass/biome(%d).png" % i).convert())
        for i in range(6):
            self.biomes[1].append(image.load("Map/Biomes/Lava/biome(%d).png" % i).convert())
        for i in range(1):
            self.biomes[2].append(image.load("Map/Biomes/Mountain/biome(%d).png" % i).convert())

    ## Updates the entire world
    def updateMap(self):
        if p.move:
            for i in range(len(self.world)):
                # Shifts the world down as the player moves to the right
                self.world[i][1][X]-= p.vel[X]
        for i in range(len(self.world)):
            ## Blits the current biome at the current in the world
            game.screen.blit(self.world[i][0],self.world[i][1])

    ## Generates the map as the player moves accross the world
    def genMap(self):
        if self.gen:
            # For the next 15 'chunks' generate land
            for i in range(15):
                if self.ground == "Grass":
                    x = randint(0,4) # Pick a biome from (0,4)
                    self.world.append((self.biomes[0][x],[self.width,400])) # Add the biome img to the 'end' of the world
                    self.width+= self.biomes[0][x].get_width() # Add to the width of the world
                #elif self.ground == "Lava":
                #    x = randint(0,5)
                #    self.world.append((self.biomes[1][x],[self.width,400]))
                #    self.width+= self.biomes[1][x].get_width()
                #elif self.ground == "Mountain":
                #    x = randint(0,0)
                #    self.world.append((self.biomes[2][x],[self.width,400]))
                #    self.width+= self.biomes[2][x].get_width()
            self.gen = False # Stop generating
        # If the world comes within 1280 pixels of the player, begin generating again
        if self.world[-1][1][X] - p.stats[STEPS] < 1280 and self.gen == False:
            self.width = self.world[-1][1][X]
            self.gen = True

    ## Generates platforms
    def genPlat(self):
        global pNum
        self.plat.append(Platform([],[],[],False))  ## Append the first platform object to the platform list
        self.plat[0].pos = [1320, randint(430,530)]
        self.plat[0].hBox = Rect([self.plat[0].pos[X],self.plat[0].pos[Y], 100, 20])
        self.plat[0].type = self.platImg[0]
        pNum = randint(15,25) # Choose the amount of platforms to spawn
        for i in range(1,pNum): # Spawn them
            self.plat.append(Platform([],[],[],False)) ## Append platform objects to the platform list
            y = self.plat[-2].pos[Y] + randint(-100,100)  # Generate the next platform within 200 pixels of the previous platform
            if y < 100: # If the y coord is < 100 add (100,150) px to it
                y = self.plat[-2].pos[Y] + randint(100,150) 
            elif y > 500: # If the y coord is < 100 subtract (100,150) px to it
                y = self.plat[-2].pos[Y] - randint(100,150)
            self.plat[i].pos = [self.plat[-2].pos[X] + randint(200,300),y]  # Set the position
            self.plat[i].hBox = Rect([self.plat[i].pos[X],self.plat[i].pos[Y],100,20]) # Set the hitbox based off of the position
            if w.ground == "Grass":
                self.plat[i].type = self.platImg[randint(0,2)] # Choose the type of platform
            else:
                self.plat[i].type = self.platImg[3] ## Not implemented ***
        self.platGen = False # Stop generating

    ## Moves the platforms
    def movePlat(self):
        if self.plat[i].hBox.collidepoint((p.pos[X]+50,p.pos[Y]+80)) and self.plat[i].broken == False: ## If the player steps on a platform and it isnt broken...
            p.pos[Y] = self.plat[i].hBox[Y] - 80 # Make the players y pos == to the platforms
            p.stand = True # Set the player to standing mode
            p.vel[Y] = 0 # Set the players y velocity to 0
            p.dJump = 0 # Reset double jump
            if self.plat[i].type == self.platImg[2]:
                self.plat[i].broken = True # Break the players platform if the platform is cracked
        if p.move:
            ## Shift the platforms
            self.plat[i].pos[X] -= p.vel[X]
            self.plat[i].hBox[X] -= p.vel[X]
        if self.plat[-1].pos[X] < -100:
            ## Reset the platforms as the last one passes
            self.dropObj = []
            self.genDrops = True
            self.plat = []
            self.platGen = True

    ## Draws the platforms
    def drawPlat(self):
        if self.plat[i].broken == False: ## If the platform isnt broken, continue to display it
            game.screen.blit(self.plat[i].type,(self.plat[i].pos[X],self.plat[i].pos[Y]))
        #draw.rect(game.screen,(250,250,250),self.plat[i].hBox,1)

    ## Generates the drops that spawn on the platforms
    def genDrop(self):
        global d,s,t
        d = randint(1,3) # How many drops
        for z in range(0,d):
            s = randint(0,pNum-1) # Which platform drop spawns on
            t = randint(0,1) # Drop Type
            self.dropObj.append(Drops([],[],[],[])) # Set a list of drop objects
            self.dropObj[z].pos = [self.plat[s].pos[X] + 25,self.plat[s].pos[Y] - 75] ## Set the position relative to platforms
            self.dropObj[z].hBox = Rect([self.dropObj[z].pos[X],self.dropObj[z].pos[Y],60,100])
            self.dropObj[z].type = game.drop[t] # Set the drop type
            self.dropObj[z].pick = True # Declare if the drop has been picked up by the player yet
        game.genDrops = False

    ## Shift the drops with the platforms
    def moveDrop(self):
        if self.dropObj[i].hBox.colliderect(p.hBox) and self.dropObj[i].pick:
            if self.dropObj[i].type == game.drop[0]: ## If the player picks up a golfclub
                p.stats[SCORE] += 3000 # Add score
            elif self.dropObj[i].type == game.drop[1] and p.stats[HP] < 100: ## If the player picks up timmies, increase score + hp
                p.stats[HP] += 10
                p.stats[SCORE] += 1000
            self.dropObj[i].pick = False
        if p.move:  # Shift the drops across the screen with the platforms and player
            self.dropObj[i].pos[X] -= p.vel[X]
            self.dropObj[i].hBox[X] -= p.vel[X]

    # Draw the drops to the screen
    def drawDrop(self):
        if self.dropObj[i].pick: # Draw all of the dropped objects
            game.screen.blit(self.dropObj[i].type,self.dropObj[i].pos)
        #draw.rect(game.screen,(250,250,250),self.dropObj[i].hBox,1)

## Class that declares drop objects attributes
class Drops:
    def __init__(self,pos,hBox,dType,pick):
        self.pos = pos
        self.hBox = hBox
        self.type = dType
        self.pick = pick

## Class pertaining to player attributes
class Player:
    def __init__(self,pos,act,vel,frame,stats):
        self.pos = pos # Player position
        #self.hBox = hBox
        self.act = act # Player actions
        self.vel = vel
        self.frame = frame 
        self.stats = stats # Relating to the players stats
        self.char = []
        self.move = self.act[0]
        self.jump = self.act[1]
        self.dJump = self.act[2]
        self.atk = self.act[3]
        self.stand = self.act[4]
        self.atkAni = False
        ## Add all of the player movement sprites to a list
        for f in range(len(os.listdir('Sprites/Main/Movement'))-1):
            self.char.append([])
            for i in range(3): 
                self.char[f].append(image.load("Sprites/Main/Movement/c(%d)/movement(%d).png" % (f,i)))
        self.hBox = Rect([self.pos[0],self.pos[1],self.char[0][0].get_width(),self.char[0][0].get_height()]) # Set the player hitbox

    ## Move the player across the screen
    def movePlayer(self):
        keys = key.get_pressed()
        ## Moving the player
        if keys[K_d]: # If the player clicks, move the player
            self.move = True 
            self.vel[X] = 10
            self.stats[STEPS]+= 10
            if game.wave != 0: # As the player moves add to the score
                self.stats[SCORE] += 1
        else:
            self.move = False
        if keys[K_w]: # Allows the player to jump
            if self.dJump == 0:
                self.jump = True
                self.vel[Y] = 15
                self.dJump = 1
            elif self.dJump == 1 and self.jump!= True:
                self.vel[Y] += 15
                self.dJump = 2
        else:
            self.jump = False
        # Allows for player to fast fall
        if keys[K_LSHIFT] and self.jump == False:
            self.vel[Y]-=3
        else:
            self.vel[Y]-=1.3
        self.hBox = Rect([p.pos[0]+25,p.pos[1]+17,self.char[0][0].get_width()-50,self.char[0][0].get_height()-30])
        # Move the player and set the velocity when they are airborne
        self.pos[Y]-=self.vel[Y]   
        if self.pos[Y] >= 535:
            self.pos[Y] = 535
            self.vel[Y] = 0
        if self.pos[Y] == 535 or self.vel[Y] == 0:
            self.dJump = 0

    ## Function relating to an attacking player
    def attack(self):
        game.screen.blit(game.target,(game.mPos[X]-50,game.mPos[Y]-50)) # Draw the target icon where the mouse is
        if self.atkAni == False and game.mb[0] == 1: ## If the player clicks set the attack to true
            atk.pos = [game.mPos[0],-150]
            atk.hBox[X] = atk.pos[0]
            self.atkAni = True
        if self.atkAni: 
            atk.vel[Y] += 1.3 ## Shift the attack rock down the screen
            atk.pos[Y] += atk.vel[Y]
            atk.hBox[Y] += atk.vel[Y]
            if atk.pos[Y] > 800: ## If the rock reaches the end, reset the position
                atk.pos = [game.mPos[0],-150]
                atk.hBox = Rect([game.mPos[0], -150,100,100])
                atk.vel[Y] = 20
                self.atkAni = False
            game.screen.blit(atk.img,atk.pos)

    ## Function relating to the drawing of the player
    def drawPlayer(self):
        if self.move or self.jump: ## If the player is moving, cycle through the walking sprites
            if self.frame[1] == 3:
                self.frame[0] += 1
                self.frame[1] = 0
            if self.frame[0] == 3:
                self.frame[0] = 0
            self.frame[1] += 1
            game.screen.blit(cm.name[self.frame[0]],self.pos)
        else: ## Else draw the typical standing sprite
            game.screen.blit(cm.name[0],self.pos)
        #draw.rect(game.screen,(250,250,250),p.hBox,1)

    ## Function to track the current player score and health
    def tracePlayer(self):
        self.score = game.font.render(str(p.stats[SCORE]),1,(250,250,250))
        if self.stats[HP] <= 0: ## If the player dies...
            mixer.music.fadeout(1000)
            fx.fadeOut() ## Fade the screen out
            game.checkScore(p.stats[SCORE]) ## Call the checkScore() function in the game class to see if it matches a leaderboard score
            main() ## Call the main menu
        #if self.stats[STEPS] == 10000*self.stats[DIF]:
        #    print(self.stats[DIF])


## Class pertaining to the meteor attack object 
class Meteor:
    def __init__(self,pos,hBox,vel,img):
        self.pos = pos
        self.hBox = hBox
        self.hBox = Rect([game.mPos[0], -150,100,100])
        self.vel = vel
        self.img = img
        self.img = image.load("Sprites/Main/atk.png")


## Class pertaining to enemies on the screen  
class Enemy:
    def __init__(self,eType,ePos,eVel,hBox,eFrame):
        self.type = eType
        self.pos = ePos
        self.vel = eVel
        self.frame = eFrame
        self.hBox = hBox
        self.reset = False
        self.curEnemy = 0
        self.passed =0
    ## Class pertaining to enemy movement
    def moveEnemy(self):
        if game.enemies[i].type == game.eg[ROCK] and p.move: ## If the enemy is a rock, shift it with the player
            game.enemies[i].pos[X] -= p.vel[X]
            game.enemies[i].hBox[X] -= p.vel[X]
        if game.enemies[i].type == game.eg[BEE]: ## If the enemy is a bee
            ## Move with the player regardless if standing in a stationary position
            if p.vel[X] > 0:
                game.enemies[i].pos[X] -= game.enemies[i].vel[X] + p.vel[X]
                game.enemies[i].hBox[X] -= game.enemies[i].vel[X] + p.vel[X]
            elif p.vel[X] < 0:
                game.enemies[i].pos[X] -= game.enemies[i].vel[X] - p.vel[X]
                game.enemies[i].hBox[X] -= game.enemies[i].vel[X] - p.vel[X]
        # Checking if there is a collision with the character + enemy
        if p.hBox.colliderect(game.enemies[i].hBox):
            self.reset = True
            self.resetPosEnemy()
            if self.reset == False:
                p.stats[HP] -= 10
        # Checking if there is a collision with the attack + enemy
        if atk.hBox.colliderect(game.enemies[i].hBox):
            self.reset = True
            self.resetPosEnemy()
            p.stats[SCORE]+=25
        # Keep track of the amount of enemies that have passed the end of the screen
        for e in range(len(game.enemies)):
            if game.enemies[e].pos[X] < -100:
                self.passed+=1
            else:
                self.passed = 0
        if self.passed >= len(game.enemies): ## If all enemies have passed
            game.totalNpc = 0 ## Reset enemy numbers
            game.enemies = [] ## Empty object list
            game.waveTrack += .5 ## Add .5 to the wave counter
            if game.waveTrack == game.waveLen: # If the counter is == to the wave, increase the wave and reset the counter
                ##(adds length to the waves as difficulty progresses)
                game.wave+=1
                game.waveTrack = 0
            if game.bossBattle:
                game.waveDisplay = game.font.render("BOSS BATTLE",1,(250,50,50))
            else:
                game.waveDisplay = game.font.render("Wave: %s"%str(game.wave),1,(250,50,50))
            if game.wave % 5 == 0: ## Every 5 waves generate a boss
                game.genBoss = True
            else: ## Once the boss battle is over, generate regular enemies again
                game.gen = True         

    ## Draw the enemies to the screen with their current frame
    def drawEnemy(self):
        if game.enemies[i].frame[1] == 3:
            game.enemies[i].frame[0] += 1
            game.enemies[i].frame[1] = 0
        if game.enemies[i].frame[0] == len(game.enemies[i].type):
            game.enemies[i].frame[0] = 0
        game.enemies[i].frame[1]+=1
        game.screen.blit(game.enemies[i].type[game.enemies[i].frame[0]],game.enemies[i].pos)
        #draw.rect(game.screen,(250,250,250),game.enemies[i].hBox,1)

    ## Function used to reset the enemy attributes (positions etc.)
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

## Class pertaining to the boss the player encounters
class Boss:
    def __init__(self,pos,hBox,vel,img,frame,hp,dmg):
        self.pos = pos
        self.hBox = hBox
        self.vel = vel
        self.frame = frame
        self.hp = hp
        self.img = img
        self.dmg = dmg
        self.reset = False
        self.hpDisplay = game.font.render("Boss HP: %s"%str(100),1,(250,50,50))
    ## Function used to move the boss across the screen
    def moveBoss(self):
        self.pos[X]-= self.vel[X] ## Shift the boss according to its velocity
        self.hBox[X]-= self.vel[X] 
        if self.pos[X] < -1200: ## If the boss runs off the screen, reset the position and damage tracker
            self.pos = [1320,p.pos[Y]]
            self.hBox[X] = 1320
            self.hBox[Y] = p.pos[Y]
            self.dmg = [False,False]
        if self.frame[1] == 3: ## Cycle through frames
            self.frame[0] += 1
            self.frame[1] = 0
        if self.frame[0] == 3:
            self.frame[0] = 0
        self.frame[1]+=1
        if self.hBox.colliderect(p.hBox) and self.dmg[0] == False: ## If the boss hits the player only take dmg once
            self.dmg[0] = True
            p.stats[HP]-=20
        if self.hBox.colliderect(atk.hBox) and self.dmg[1] == False: ## If the player attacks the boss, only take dmg once
            self.dmg[1] = True
            self.hp-=10
        if self.hp < 10: ## If the boss dies, reset the positions
            self.pos = [1320,p.pos[Y]]
            self.hBox[X] = 1320
            self.hBox[Y] = p.pos[Y]
            self.dmg = False
            p.stats[SCORE] += 10000 ## Add to the players score
            if p.stats[HP] + 30 > 100: ## Increase the players health
                h = 100-p.stats[HP]
                p.stats[HP] += h
            else:
                p.stats[HP]+=30
            game.wave+=1 ## Change the wave
            if p.stats[DIF] < 4: ## Increase the difficulty
                p.stats[DIF] += 1
            game.waveLen += .5 ## Increase the wave counter
            game.bossBattle = False ## End the boss battle
            game.gen = True ## Generate common enemies
        elif self.hp > 0: ## Display the boss health if it isnt dead
            self.hpDisplay = game.font.render("Boss HP: %s"%str(self.hp),1,(250,50,50))

    ## Function that draws the boss to the screen
    def drawBoss(self):
        game.screen.blit(boss.img[boss.frame[0]],boss.pos)
        #draw.rect(game.screen,(250,250,250),boss.hBox,1)

def main():
    global game,m,cm,gm,hm,tm,w,p,e,b,fx,music,atk
    ## Variables used to make lists more understandable
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
    w = World(True,[],"Grass",[0,0],0)
    p = Player([50,535],[False,False,1,False,False],[0,0],[0,0],['p1',100,10,0,1])
    atk = Meteor([game.mPos[0], -150],[],[10,10],[])
    d = Drops([],[],[],[])
    # Menu Classes(self,pos,hBox,vel,img):
    m = MainMenu()
    gm = GameMenu()
    hm = HighscoreMenu()
    cm = CharMenu(p.char[2],[False,False],[[350,280],[450,280],[550,280],[650,280],[750,280]])
    tm = TutorialMenu()
    # Music and Effect Classes
    fx = Fx()
    music = Music()
    music.play = True
    display.set_caption("~The Walker~")
    mouse.set_visible(False)
    myClock = time.Clock()
    init()
    while running: ## While the game is running
        game.eventLoop() ## Run the game loop
        game.run() ## Run the game
        display.flip() ## Update the screen
        myClock.tick(30) ## Set the frame rate to 30FPS
    quit()

main()
