#
# World of Isotiles
# Author: nicolas.bredeche(at)sorbonne-universite.fr
#
# Started: 2018-11-17
# purpose: basic code developped for teaching artificial life and ecological simulation at Sorbonne Univ. (SU)
# couse: L2, 2i013 Projet, "Vie Artificielle"
# licence: CC-BY-SA
#
# Credits for third party resources used in this project:
# - Assets: https://www.kenney.nl/ (great assets by Kenney Vleugels with *public domain license*)
# - https://www.uihere.com/free-cliparts/space-invaders-extreme-2-video-game-arcade-game-8-bit-space-invaders-3996521
#
# Random bookmarks:
# - scaling images: https://stackoverflow.com/questions/43196126/how-do-you-scale-a-design-resolution-to-other-resolutions-with-pygame
# - thoughts on grid worlds: http://www-cs-students.stanford.edu/~amitp/game-programming/grids/
# - key pressed? https://stackoverflow.com/questions/16044229/how-to-get-keyboard-input-in-pygame
# - basic example to display tiles: https://stackoverflow.com/questions/20629885/how-to-render-an-isometric-tile-based-world-in-python
# - pygame key codes: https://www.pygame.org/docs/ref/key.html
# - pygame capture key combination: https://stackoverflow.com/questions/24923078/python-keydown-combinations-ctrl-key-or-shift-key
# - methods to initialize a 2D array: https://stackoverflow.com/questions/2397141/how-to-initialize-a-two-dimensional-array-in-python
# - bug with SysFont - cf. https://www.reddit.com/r/pygame/comments/1fhq6d/pygamefontsysfont_causes_my_script_to_freeze_why/
#       myfont = pygame.font.SysFont(pygame.font.get_default_font(), 16)
#       myText = myfont.render("Hello, World", True, (0, 128, 0))
#       screen.blit(myText, (screenWidth/2 - text.get_width() / 2, screenHeight/2 - text.get_height() / 2))
#       ... will fail.

import sys
import datetime
from random import *
import math
import time

import pygame
from pygame.locals import *


from agents.classe.ville import Ville
from agents.classe.Genie import Genie
from agents.classe.habitant import Habitant
from agents.classe.Batiments import Hotel, Restaurant

###

versionTag = "2018-11-18_23h24"

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

# display screen dimensions
screenWidth = 1400 # 1400
screenHeight = 900 #900

# world dimensions (ie. nb of cells in total)
worldWidth = 64#64
worldHeight = 64#64

# set surface of displayed tiles (ie. nb of cells that are rendered) -- must be superior to worldWidth and worldHeight
viewWidth = 32 #32
viewHeight = 32 #32

scaleMultiplier = 0.25 # re-scaling of loaded images

objectMapLevels = 8 # number of levels for the objectMap. This determines how many objects you can pile upon one another.

# set scope of displayed tiles
xViewOffset = 0
yViewOffset = 0

addNoise = False

maxFps = 30 # set up maximum number of frames-per-second

verbose = False # display message in console on/off
verboseFps = True # display FPS every once in a while

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

pygame.init()

#pygame.key.set_repeat(5,5)

fpsClock = pygame.time.Clock()

screen = pygame.display.set_mode((screenWidth, screenHeight), DOUBLEBUF)

pygame.display.set_caption('World of Isotiles')

###

# spritesheet-specific -- as stored on the disk ==> !!! here, assume 128x111 with 64 pixels upper-surface !!!
# Values will be updated *after* image loading and *before* display starts
tileTotalWidth = 100 # width of tile image
tileTotalHeight = 128 # height of tile image
tileVisibleHeight = 64 # height "visible" part of the image, i.e. top part without subterranean part

###

def loadImage(filename):
    image = pygame.image.load(filename).convert_alpha()
    image = pygame.transform.scale(image, (int(tileTotalWidth*scaleMultiplier), int(tileTotalHeight*scaleMultiplier)))
    return image

tileType = [
    loadImage('assets/basic111x128/platformerTile_48_ret.png'), # grass
    loadImage('assets/ext/isometric-blocks/PNG/Abstract tiles/abstractTile_09.png'), # grey brock
    loadImage('assets/ext/isometric-blocks/PNG/Abstract tiles/abstractTile_26.png'), #water
    loadImage('assets/ext/isometric-blocks/PNG/Platformer tiles/platformerTile_33.png'), # brick
    loadImage('assets/ext/isometric-blocks/PNG/Abstract tiles/abstractTile_12.png'), # blue grass (?)
    loadImage('assets/ext/isometric-blocks/PNG/Voxel tiles/voxelTile_30.png'), # grey block
    
]




objectType = [
    None, # default -- never drawn
    loadImage('assets/basic111x128/tree_small_NW_ret.png'), # normal tree
    loadImage('assets/ext/isometric-blocks/PNG/Voxel tiles/voxelTile_07.png'), # grey block
    loadImage('assets/basic111x128/blockHuge_N_ret.png'), # construction block
    loadImage('assets/basic111x128/tree_small_NW_ret_red.png'), # burning tree
]

agentType = [
    None, # default -- never drawn
    loadImage('assets/basic111x128/invader_ret.png'), # invader
    loadImage('images/purple_car1.png'),
    loadImage('images/pink_car1.png'),
    loadImage('images/blue_car1.png'), #voitures
    loadImage('images/lambda1.png'), #personnes lambdas
    loadImage('images/malade.png'), #genies
    loadImage('images/magicien.png')

    #personnes lambdas
    #genies
]

noObjectId = noAgentId = 0
grassId = 0
greyId=3
waterId=2
bluegrassId=4
greyblockId=5
grassn2Id=6

# object 

treeId = 1
blockId = 2
burningTreeId =3

# road tile


road_horizonId=4
road_verticId=5
road_corner1Id=6
road_corner2Id=7
road_corner3Id=8
road_corner4Id=9
road_crossT1Id=10
road_crossT2Id=11



invaderId = 1

voitureId= [2,3,4]
personneId = 5 
maladeId = 6

###

# re-scale reference image size -- must be done *after* loading sprites
tileTotalWidth = tileTotalWidth * scaleMultiplier  # width of tile image, as stored in memory
tileTotalHeight = tileTotalHeight * scaleMultiplier # height of tile image, as stored in memory
tileVisibleHeight = tileVisibleHeight * scaleMultiplier # height "visible" part of the image, as stored in memory

heightMultiplier = tileTotalHeight/2 # should be less than (or equal to) tileTotalHeight

###

#terrainMap = [x[:] for x in [[0]* worldWidth] * worldHeight]
terrainMap = [x[:] for x in [[0]* worldWidth] * worldHeight]
heightMap  = [x[:] for x in [[0] * worldWidth] * worldHeight]
objectMap = [ [ [ 0 for i in range(worldWidth) ] for j in range(worldHeight) ] for k in range(objectMapLevels) ]
agentMap   = [x[:] for x in [[0] * worldWidth] * worldHeight]
levelMap = [x[:] for x in [[-1]* worldWidth] * worldHeight] # les différents niveaux débloqués

###

# set initial position for display on screen
xScreenOffset = screenWidth/2 - tileTotalWidth/2
yScreenOffset = 3*tileTotalHeight # border. Could be 0.

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###


class Voiture:

    def __init__(self, pos_x,pos_y, id, mode):
        self.pos_x=pos_x
        self.pos_y=pos_y
        self.id=id
        self.mode=mode # R : droite / L : gauche / U : haut / D : bas

    def move(self):
        if self.mode == 'R':
            self.pos_x=(self.pos_x + 1 )%getWorldWidth()
        elif self.mode == 'L':
            self.pos_x=(self.pos_x - 1 )%getWorldWidth()
        elif self.mode == 'D':
            self.pos_y=(self.pos_y + 1 )%getWorldWidth()
        else :
            self.pos_y=(self.pos_y - 1 )%getWorldWidth()


###


def displayWelcomeMessage():

    print ("")
    print ("=-= =-= =-= =-= =-= =-= =-= =-= =-= =-= =-= =-= =-=")
    print ("=-=  World of Isotiles                          =-=")
    print ("=-=                                             =-=")
    print ("=-=  nicolas.bredeche(at)sorbonne-universite.fr =-=")
    print ("=-=  licence CC:BY:SA                           =-=")
    print ("=-= =-= =-= =-= =-= =-= =-= =-= =-= =-= =-= =-= =-=")
    print (">> v.",versionTag)
    print ("")

    print ("Screen resolution : (",screenWidth,",",screenHeight,")")
    print ("World surface     : (",worldWidth,",",worldHeight,")")
    print ("View surface      : (",viewWidth,",",viewHeight,")")
    print ("Verbose all       :",verbose)
    print ("Verbose fps       :",verboseFps)
    print ("Maximum fps       :",maxFps)
    print ("")

    print ("# Hotkeys:")
    print ("\tcursor keys : move around (use shift for tile-by-tile move)")
    print ("\tv           : verbose mode")
    print ("\tf           : display frames-per-second")
    print ("\to           : decrease view surface")
    print ("\tO           : increase view surface")
    print ("\tESC         : quit")
    print ("")

    return

def getWorldWidth():
    return worldWidth

def getWorldHeight():
    return worldHeight

def getViewWidth():
    return viewWidth

def getViewHeight():
    return viewHeight

def getTerrainAt(x,y):
    return terrainMap[y][x]

def setTerrainAt(x,y,type):
    terrainMap[y][x] = type

def getHeightAt(x,y):
    return heightMap[y][x]

def setHeightAt(x,y,height):
    heightMap[y][x] = height

def getObjectAt(x,y,level=0):
    if level < objectMapLevels:
        return objectMap[level][y][x]
    else:
        print ("[ERROR] getObjectMap(.) -- Cannot return object. Level does not exist.")
        return 0

def setObjectAt(x,y,type,level=0): # negative values are possible: invisible but tangible objects (ie. no display, collision)
    if level < objectMapLevels:
        objectMap[level][y][x] = type
    else:
        print ("[ERROR] setObjectMap(.) -- Cannot set object. Level does not exist.")
        return 0

def setCityAt(x,y,type): # negative values are possible: invisible but tangible objects (ie. no display, collision)
    return setObjectAt(x,y,type,1)

def getAgentAt(x,y):
    return agentMap[y][x]

def setAgentAt(x,y,type):
    agentMap[y][x] = type

def setVoitureAt(voiture):
    agentMap[voiture.pos_y][voiture.pos_x]=voiture.id

##### INITIALISATION DES DIFFERENTS LEVELS #####

def initLevel():
    for x in range(getWorldWidth()-1):
        for y in range(getWorldWidth()-1):
            if(terrainMap[y][x]!=waterId and terrainMap[x][y]!=greyId):
                setObjectAt(x,y,treeId,0)

def setLevel1():
    for x in range(10,20):
        for y in range(10,20):
            levelMap[x][y]=0
            setObjectAt(x,y,noObjectId,0)
    
def setLevel2():
    for x in range(5,25):
        for y in range(5,25):
            if levelMap[x][y]!=0:
                levelMap[x][y]=0
                setObjectAt(x,y,noObjectId,0)

def stepVoiture(liste_voiture):
    
    for voiture in liste_voiture:
        setAgentAt(voiture.pos_x,voiture.pos_y,noAgentId)
        voiture.move()
        setVoitureAt(voiture)

##### Création habitants/malade #####

def position_agent(pos,liste):
    for agent in liste :
        if agent.position == pos :
            return False
    return True

def creer_habitants(count, ville, liste):
    """Crée des habitants tant que la ville est sous sa limite de population."""

    max_population = 10
    for _ in range(count):
        #if ville.population >= max_population:
          #  break
        
        x = randint(ville.position[0], ville.position[1])
        y = randint(ville.position[2], ville.position[3])
        habitant = Habitant([x, y], ville)
        
        #if all(h.position != [x, y] for h in liste_agent):
        liste.append(habitant)
        setAgentAt(x, y, personne1Id)
        ville.population += 1

    return liste


def avancer_ou_pas(agent):

    setAgentAt(agent.position[0],agent.position[1],noAgentId)
    agent.one_step()
    setAgentAt(agent.position[0],agent.position[1],agent.image_id)

    return agent 
    
def ajout_malade(ville,liste_agent):

    x = randint(ville.position[0], ville.position[1])
    y = randint(ville.position[2], ville.position[3])
    habitant = Habitant([x,y], ville)
    habitant.malade()
    liste_agent.append(habitant)
    
    return liste_agent


def malade(agent, liste_agent):
    """ Vérifie si l'agent est à côté d'un malade """

    x, y = agent.position

    voisins = [
        [(x + 1) % 99, y], 
        [(x - 1) % 99, y], 
        [x, (y + 1) % 99], 
        [x, (y - 1) % 99], 
    ]

    for a in liste_agent:
        if a.position in voisins and a.etat == 'M':
            agent.malade()
            break

    return 

def monde_habitant(liste_agent):
    """ Avance les habitants """

    update_agent=[]
    for a in liste_agent :
        
        avancer_ou_pas(a)
    
        if a.point_de_vie < 0 or a.age >=50 :
            setAgentAt(a.position[0],a.position[1],0)
            continue

        elif a.etat == 'M' :
            a.point_de_vie -= 1

        elif a.etat == 'V' :
            malade(a,liste_agent)
        
        update_agent.append(a)

    return update_agent

def total_malade(liste_agent):
    count = 0
    for a in liste_agent:
        print(a.etat)
        if a.etat=='M':
            count+=1
    return count



### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

def initWorld():
    global xAgent, yAgent
    global argent
    global voiture

    argent=0
    
    """
    for iniw in range(0,getWorldWidth()-1):
        for inih in range(0,getWorldHeight()-1):
            setTerrainAt(iniw,inih,waterId)
    """
    
    for i in range(getWorldWidth()-1):
        for j in range(getWorldWidth()-1):
            setTerrainAt(i,j,grassn2Id)

    amplitude = 3  # Amplitude de la courbe en S
    frequence = 0.2  # Fréquence de la sinusoïde
    decalage = getWorldWidth()//2 # Départ au centre
    inclinaison= 0.25

    # Générer les coordonnées du ruisseau
    for i in range(getWorldWidth()):
        j = int(decalage + amplitude * math.sin(frequence * i)+ (inclinaison*i))  # Forme en S
        if 0 <= j < getWorldWidth()-1:
            setTerrainAt(i,j,waterId)
        if 0 <= j+1 < getWorldWidth()-1:  
            setTerrainAt(i, j+1, waterId)
        if 0 <= j+2 < getWorldWidth()-1:  
            setTerrainAt(i, j+2, waterId)

    voiture=[]

    for j in range(1,5):
        for i in range(getWorldWidth()):
            setTerrainAt(i,j*6,greyId)
            setTerrainAt(j*6,i,greyId)
            if len(voiture)<10 and i%20==0:
                new_v1=Voiture(j*6,i,voitureId[randint(0,2)],'U')
                setVoitureAt(new_v1)
                voiture.append(new_v1)


    initLevel()
    setLevel2()
        
    # add a pyramid-shape building
    
    xAgent = yAgent = 0
    while getTerrainAt(xAgent,yAgent) != 0:
        xAgent = randint(0,getWorldWidth()-1)
        yAgent = randint(0,getWorldHeight()-1)
    setAgentAt(xAgent,yAgent,invaderId)
"""
    nbTrees = 50
    for i in range(nbTrees):
        x = randint(0,getWorldWidth()-1)
        y = randint(0,getWorldHeight()-1)
        while getTerrainAt(x,y) != 0 or getObjectAt(x,y) != 0:
            x = randint(0,getWorldWidth()-1)
            y = randint(0,getWorldHeight()-1)
        setObjectAt(x,y,treeId)

"""

##

def stepWorld( it = 0 ):
    global xAgent, yAgent, xViewOffset, yViewOffset
    global argent
    global voiture

    pygame.draw.rect(screen, (0,0,0), (0, 0, screenWidth, screenHeight), 0) # overkill - can be optimized. (most sprites are already "naturally" overwritten)
    #pygame.display.update()

    for y in range(getViewHeight()):
        for x in range(getViewWidth()):
            # assume: north-is-upper-right

            xTile = ( xViewOffset + x + getWorldWidth() ) % getWorldWidth()
            yTile = ( yViewOffset + y + getWorldHeight() ) % getWorldHeight()

            heightNoise = 0
            if addNoise == True: # add sinusoidal noise on height positions
                if it%int(math.pi*2*199) < int(math.pi*199):
                    # v1.
                    heightNoise = math.sin(it/23+yTile) * math.sin(it/7+xTile) * heightMultiplier/10 + math.cos(it/17+yTile+xTile) * math.cos(it/31+yTile) * heightMultiplier
                    heightNoise = math.sin(it/199) * heightNoise
                else:
                    # v2.
                    heightNoise = math.sin(it/13+yTile*19) * math.cos(it/17+xTile*41) * heightMultiplier
                    heightNoise = math.sin(it/199) * heightNoise

            height = getHeightAt( xTile , yTile ) * heightMultiplier + heightNoise

            xScreen = xScreenOffset + x * tileTotalWidth / 2 - y * tileTotalWidth / 2
            yScreen = yScreenOffset + y * tileVisibleHeight / 2 + x * tileVisibleHeight / 2 - height

            screen.blit( tileType[ getTerrainAt( xTile , yTile ) ] , (xScreen, yScreen)) # display terrain

            for level in range(objectMapLevels):
                if getObjectAt( xTile , yTile , level)  > 0: # object on terrain?
                    screen.blit( objectType[ getObjectAt( xTile , yTile, level) ] , (xScreen, yScreen - heightMultiplier*(level+1) ))

            if getAgentAt( xTile, yTile ) != 0: # agent on terrain?
                screen.blit( agentType[ getAgentAt( xTile, yTile ) ] , (xScreen, yScreen - heightMultiplier ))

    # move agent
    if it % (maxFps/10) == 0:
        xAgentNew = xAgent
        yAgentNew = yAgent
        if random() < 0.5:
            xAgentNew = ( xAgent + [-1,+1][randint(0,1)] + getWorldWidth() ) % getWorldWidth()
        else:
            yAgentNew = ( yAgent + [-1,+1][randint(0,1)] + getWorldHeight() ) % getWorldHeight()
        if getObjectAt(xAgentNew,yAgentNew) == 0: # dont move if collide with object (note that negative values means cell cannot be walked on)
            setAgentAt(xAgent,yAgent,noAgentId)
            xAgent = xAgentNew
            yAgent = yAgentNew
            setAgentAt(xAgent,yAgent,invaderId)
        #if verbose == True:
        #    print (it,": agent(",xAgent,",",yAgent,")")

        stepVoiture(voiture)

    if argent>20:
        setLevel2()

   

    argent+=argent

    return

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

timestamp = datetime.datetime.now().timestamp()

displayWelcomeMessage()

initWorld()

print ("initWorld:",datetime.datetime.now().timestamp()-timestamp,"second(s)")
timeStampStart = timeStamp = datetime.datetime.now().timestamp()

it = itStamp = 0

userExit = False

while userExit == False:

    if it != 0 and it % 100 == 0 and verboseFps:
        print ("[fps] ", ( it - itStamp ) / ( datetime.datetime.now().timestamp()-timeStamp ) )
        timeStamp = datetime.datetime.now().timestamp()
        itStamp = it

    #screen.blit(pygame.font.render(str(currentFps), True, (255,255,255)), (screenWidth-100, screenHeight-50))



    stepWorld(it)

    # continuous stroke
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and not ( keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] ):
        xViewOffset  = (xViewOffset - 1 + getWorldWidth() ) % getWorldWidth()
        if verbose:
            print("View at (",xViewOffset ,",",yViewOffset,")")
    elif keys[pygame.K_RIGHT] and not ( keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] ):
        xViewOffset = (xViewOffset + 1 ) % getWorldWidth()
        if verbose:
            print("View at (",xViewOffset ,",",yViewOffset,")")
    elif keys[pygame.K_DOWN] and not ( keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] ):
        yViewOffset = (yViewOffset + 1 ) % getWorldHeight()
        if verbose:
            print("View at (",xViewOffset,",",yViewOffset,")")
    elif keys[pygame.K_UP] and not ( keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] ):
        yViewOffset = (yViewOffset - 1 + getWorldHeight() ) % getWorldHeight()
        if verbose:
            print("View at (",xViewOffset,",",yViewOffset,")")

    # single stroke
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                userExit = True
            elif event.key == pygame.K_n and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                addNoise = not(addNoise)
                print ("noise is",addNoise) # easter-egg
            elif event.key == pygame.K_v:
                verbose = not(verbose)
                print ("verbose is",verbose)
            elif event.key == pygame.K_f:
                verboseFps = not(verboseFps)
                print ("verbose FPS is",verboseFps)
            elif event.key == pygame.K_LEFT and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                xViewOffset  = (xViewOffset - 1 + getWorldWidth() ) % getWorldWidth()
                if verbose:
                    print("View at (",xViewOffset ,",",yViewOffset,")")
            elif event.key == pygame.K_RIGHT and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                xViewOffset = (xViewOffset + 1 ) % getWorldWidth()
                if verbose:
                    print("View at (",xViewOffset ,",",yViewOffset,")")
            elif event.key == pygame.K_DOWN and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                yViewOffset = (yViewOffset + 1 ) % getWorldHeight()
                if verbose:
                    print("View at (",xViewOffset,",",yViewOffset,")")
            elif event.key == pygame.K_UP and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                yViewOffset = (yViewOffset - 1 + getWorldHeight() ) % getWorldHeight()
                if verbose:
                    print("View at (",xViewOffset,",",yViewOffset,")")
            elif event.key == pygame.K_o and not( pygame.key.get_mods() & pygame.KMOD_SHIFT ) :
                if viewWidth > 1:
                    viewWidth = viewWidth - 1
                    viewHeight = viewHeight - 1
                if verbose:
                    print ("View surface is (",viewWidth,",",viewHeight,")")
            elif event.key == pygame.K_o and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                if viewWidth < worldWidth :
                    viewWidth = viewWidth + 1
                    viewHeight = viewHeight + 1
                if verbose:
                    print ("View surface is (",viewWidth,",",viewHeight,")")

    pygame.display.flip()
    fpsClock.tick(maxFps) # recommended: 30 fps

    it += 1

fps = it / ( datetime.datetime.now().timestamp()-timeStampStart )
print ("[Quit] (", fps,"frames per second )")

pygame.quit()
sys.exit()
