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
import csv
import pygame
from pygame.locals import *

from ursina import Vec3, color

from agents.classe.ville import Ville
from agents.classe.Genie import Genie
from agents.classe.habitant import Habitant
from agents.classe.Batiments import Hotel, Restaurant, MaisonGenie


###

versionTag = "2018-11-18_23h24"

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

# display screen dimensions
screenWidth = 930#930
screenHeight = 640 #640

# world dimensions (ie. nb of cells in total)
worldWidth = 100
worldHeight = 100
# set surface of displayed tiles (ie. nb of cells that are rendered) -- must be superior to worldWidth and worldHeight
viewWidth = 100 #32
viewHeight = 100 #32

scaleMultiplier = 0.08 # re-scaling of loaded images

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

pygame.display.set_caption('MONOPOLISATION')
#background = pygame.image.load("copilotBackground.png")

###

# spritesheet-specific -- as stored on the disk ==> !!! here, assume 128x111 with 64 pixels upper-surface !!!
# Values will be updated *after* image loading and *before* display starts
tileTotalWidth = 100 # width of tile image
tileTotalHeight = 128 # height of tile image
tileVisibleHeight = 64 # height "visible" part of the image, i.e. top part without subterranean part

###

def loadImage(filename):
    global tileTotalWidthOriginal,tileTotalHeightOriginal,scaleMultiplier
    image = pygame.image.load(filename).convert_alpha()
    image = pygame.transform.scale(image, (int(tileTotalWidthOriginal*scaleMultiplier), int(tileTotalHeightOriginal*scaleMultiplier)))
    return image

def loadBuilding(filename):
    global tileTotalWidthOriginal,tileTotalHeightOriginal,scaleMultiplier
    image = pygame.image.load(filename).convert_alpha()
    image = pygame.transform.scale(image, (int(tileTotalWidthOriginal*(scaleMultiplier*4)), int(tileTotalHeightOriginal*scaleMultiplier*4)))
    return image

def loadAllImages():
    global tileType, objectType, agentType

    tileType = []
    tileType.append(loadImage('assets/basic111x128/platformerTile_48_ret.png')) # grass 0
    tileType.append(loadImage('assets/ext/isometric-blocks/PNG/Abstract tiles/abstractTile_09.png')) # grey brock 1
    tileType.append(loadImage('assets/ext/isometric-blocks/PNG/Abstract tiles/abstractTile_26.png')) #water 2
    tileType.append(loadImage('assets/ext/isometric-blocks/PNG/Platformer tiles/platformerTile_33.png')), # brick 3
    tileType.append(loadImage('assets/ext/isometric-blocks/PNG/Abstract tiles/abstractTile_12.png')) # blue grass (?) 4
    tileType.append(loadImage('assets/ext/isometric-blocks/PNG/Voxel tiles/voxelTile_30.png')) # grey block 5
    tileType.append(loadImage('assets/ext/isometric-blocks/PNG/Voxel tiles/voxelTile_55.png')) #bleu vert 6
    tileType.append(loadImage('assets/ext/isometric-blocks/PNG/Platformer tiles/platformerTile_10.png')) # 7
    tileType.append(loadImage('assets/ext/isometric-blocks/PNG/Platformer tiles/platformerTile_31.png')) # 8
    tileType.append(loadImage('assets/ext/isometric-blocks/PNG/Platformer tiles/platformerTile_28.png')) #jaune 9
    tileType.append(loadImage('assets/ext/isometric-blocks/PNG/Platformer tiles/platformerTile_27.png')) #orange 10
    tileType.append(loadImage('assets/ext/isometric-blocks/PNG/Platformer tiles/platformerTile_02.png')) #rose 11
    tileType.append(loadImage('assets/ext/isometric-blocks/PNG/Platformer tiles/platformerTile_18.png')) #violet 12
    tileType.append(loadImage('assets/ext/isometric-blocks/PNG/Voxel tiles/voxelTile_26.png')) #bois 13
    

    objectType = []
    objectType.append(None) # default -- never drawn
    objectType.append(loadImage('assets/basic111x128/tree_small_NW_ret.png')) # normal tree
    objectType.append(loadImage('assets/ext/isometric-blocks/PNG/Voxel tiles/voxelTile_07.png')) # grey block
    objectType.append(loadImage('assets/basic111x128/blockHuge_N_ret.png')) # construction block
    objectType.append(loadImage('assets/basic111x128/tree_small_NW_ret_red.png')) # burning tree
    objectType.append(loadBuilding('images/bar.png')) # bar
    objectType.append(loadBuilding('images/restos1.png')) # restaurant
    objectType.append(loadBuilding('images/flat1d.png')) # flat
    objectType.append(loadBuilding('images/house1d.png')) # maison
    objectType.append(loadImage('assets/ext/isometric-blocks/PNG/Voxel tiles/voxelTile_05.png')) #block vert
    objectType.append(loadImage('assets/ext/isometric-blocks/PNG/Platformer tiles/platformerTile_26.png')) #bleu glace fondu
    objectType.append(loadImage('assets/ext/isometric-blocks/PNG/Platformer tiles/platformerTile_12.png')) #gris au blanc
    objectType.append(loadImage('assets/ext/isometric-blocks/PNG/Voxel tiles/voxelTile_10.png')) #gris au vert 
    objectType.append(loadImage('assets/ext/isometric-blocks/PNG/Voxel tiles/voxelTile_13.png')) #gris au blanc
    objectType.append(loadImage('assets/ext/isometric-blocks/PNG/Abstract tiles/abstractTile_26.png')) #water
    objectType.append(loadImage('assets/ext/isometric-blocks/PNG/Voxel tiles/voxelTile_50.png')) #gris au blanc
    objectType.append(loadBuilding('images/yellowhouse-removebg-preview.png')) # maison jaune
    objectType.append(loadBuilding('images/orangehouse-removebg-preview.png')) # maison orange
    objectType.append(loadBuilding('images/pinkhouse-removebg-preview.png')) # maison rose
    objectType.append(loadBuilding('images/purplehouse-removebg-preview.png')) # maison violette
    

    agentType = []
    agentType.append(None) # default -- never drawn
    agentType.append(loadImage('assets/basic111x128/invader_ret.png')) # invader
    agentType.append(loadImage('images/purple_car1.png'))
    agentType.append(loadImage('images/pink_car1.png'))
    agentType.append(loadImage('images/blue_car1.png')) #voitures
    agentType.append(loadImage('images/lambda1.png')) #personnes lambdas
    agentType.append(loadImage('images/malade.png')) #genies
    agentType.append(loadImage('images/magicien.png')) #magicien
    agentType.append(loadImage('images/guerie.png')) #gueris

tileTotalWidthOriginal = 111  # width of tile image
tileTotalHeightOriginal = 128 # height of tile image
tileVisibleHeightOriginal = 64 # height "visible" part of the image, i.e. top part without subterranean part

def resetImages():
    global tileTotalWidth, tileTotalHeight, tileTotalWidthOriginal, tileTotalHeightOriginal, scaleMultiplier, heightMultiplier, tileVisibleHeight
    tileTotalWidth = tileTotalWidthOriginal * scaleMultiplier  # width of tile image, as stored in memory
    tileTotalHeight = tileTotalHeightOriginal * scaleMultiplier # height of tile image, as stored in memory
    tileVisibleHeight = tileVisibleHeightOriginal * scaleMultiplier # height "visible" part of the image, as stored in memory
    heightMultiplier = tileTotalHeight/2 # should be less than (or equal to) tileTotalHeight
    loadAllImages()
    return

#Tiles 

noObjectId = noAgentId = 0
grassId = 0
greyId=3
waterId=2
bluegrassId=4
greyblockId=5
grassn2Id=6
purpleblockId = 7
resetId = 12
boisId = 13

# object 

treeId = 1
blockId = 2
burningTreeId =3
barId = 5
resto1Id = 6
flat_1dId = 7
house_d1Id = 8
thegrassId = 9
meltingId = 10
greywhiteId = 11
greygreenId = 12
montId = 13
thewaterId = 14
mont2Id = 15
yellowhouseId = 16
orangehouseId = 17
pinkhouseId = 18
purplehouseId = 19


 
#agent

invaderId = 1
voitureId=[2,3,4]
personne1Id = 5
maladeId = 6
magicienId = 7
gueris = 8 

###

# re-scale reference image size -- must be done *after* loading sprites
tileTotalWidth = tileTotalWidth * scaleMultiplier  # width of tile image, as stored in memory
tileTotalHeight = tileTotalHeight * scaleMultiplier # height of tile image, as stored in memory
tileVisibleHeight = tileVisibleHeight * scaleMultiplier # height "visible" part of the image, as stored in memory

heightMultiplier = tileTotalHeight/2 # should be less than (or equal to) tileTotalHeight

###

terrainMap = [x[:] for x in [[0]* worldWidth] * worldHeight]
heightMap  = [x[:] for x in [[0] * worldWidth] * worldHeight]
objectMap = [ [ [ 0 for i in range(worldWidth) ] for j in range(worldHeight) ] for k in range(objectMapLevels) ]
agentMap   = [x[:] for x in [[0] * worldWidth] * worldHeight]
evolutionMap = [x[:] for x in [[None,None]* worldWidth] * worldHeight] # les différents niveaux débloqués

###

# set initial position for display on screen
xScreenOffset = screenWidth/2 - tileTotalWidth/2
yScreenOffset = 3*tileTotalHeight # border. Could be 0.

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

####

class Voiture:

    def __init__(self, pos_x,pos_y, id, mode):
        self.pos_x=pos_x
        self.pos_y=pos_y
        self.id=id
        self.mode=mode # R : droite / L : gauche / U : haut / D : bas / M : mort

    def move(self):
        if self.mode == 'R':
            self.pos_x=(self.pos_x + 1 )%getWorldWidth()
        elif self.mode == 'L':
            self.pos_x=(self.pos_x - 1 )%getWorldWidth()
        elif self.mode == 'D':
            self.pos_y=(self.pos_y + 1 )%getWorldWidth()
        else :
            self.pos_y=(self.pos_y - 1 )%getWorldWidth()

    def disparition(self):
        self.id = noAgentId
        self.mode = 'M'
        
####

##### Probabilité #####

pb_loto = 0.00001
pb_malchance = 0.0001
pb_magicien = 0.002
pb_achatbatiment = 0.01
pb_achatdeville = 0.02
pb_ajout_hab = 0.1
pb_habitants = 0.05
pb_naissance = 0.00001

speed = 0.4

prix_terrain = 500

#####

def displayWelcomeMessage():

    print ("")
    print ("=-= =-= =-= =-= =-= =-= =-= =-= =-= =-= =-= =-= =-=")
    print ("=-=     MONOPOLISATION :)                       =-=")
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
    print ("\ts           : decrease view surface")
    print ("\tS           : increase view surface")
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

##### FONCTION VOITURE #####

def setVoitureAt(voiture):
    """ Place les voitures sur la carte """
    agentMap[voiture.pos_y][voiture.pos_x]=voiture.id

def stepVoiture(liste_voiture):
    """ Mouvement des voitures """
    for voiture in liste_voiture:
        setAgentAt(voiture.pos_x,voiture.pos_y,noAgentId)
        voiture.move()
        setVoitureAt(voiture)
    return

def disparition(voiture,niv):
    """ Fait disparaitre les voitures avec le niveau d'eau """
    voiture[niv].disparition()

##### CREATION / GENERATION D'HABITANTS #####

def position_agent(pos,liste):
    for agent in liste :
        if agent.position == pos :
            return False
    return True

def creer_habitants(count, ville, liste):
    """Crée des habitants tant que la ville est sous sa limite de population."""
    max_population = 30
    for _ in range(count):
        if ville.population >= max_population:
            break
        
        while True:
            x = randint(ville.position[0], ville.position[1])
            y = randint(ville.position[2], ville.position[3])
            if all(h.position != [x, y] for h in liste) and x<getWorldWidth() and y<getWorldWidth():
                break
    
        habitant = Habitant([x, y], ville)
        liste.append(habitant)
        setAgentAt(x, y, personne1Id)
        ville.population += 1

    return liste

def avancer_ou_pas(agent):
    """ Fait avancer les habitants """
    setAgentAt(agent.position[0],agent.position[1],noAgentId)
    position = agent.one_step()
    if position[0]<getWorldWidth() and position[1]<getWorldWidth():
        if getAgentAt(position[0],position[1])==noAgentId :
            agent.change_position(position)
            setAgentAt(agent.position[0],agent.position[1],agent.image_id)
    else :
        setAgentAt(agent.position[0],agent.position[1],agent.image_id)
    return agent 
    
def ajout_malade(ville,liste_agent):
    """ Ajoute un malade dans la ville de manière aléatoire """
    while True:
        x = randint(ville.position[0], ville.position[1]-1)
        y = randint(ville.position[2], ville.position[3]-1)
        if all(h.position != [x, y] for h in liste_agent):
            break

    #x = randint(ville.position[0], ville.position[1])
    #y = randint(ville.position[2], ville.position[3])
    habitant = Habitant([x,y], ville)
    habitant.malade()
    setAgentAt(x,y,habitant.image_id)
    liste_agent.append(habitant)
    
    return liste_agent

def ajout_malade_alea(genie,liste_agent):
    le_genie = genie[randint(0,len(genie)-1)]
    ville = le_genie.villes_possedees[randint(0,len(le_genie.villes_possedees)-1)]
    ajout_malade(ville,liste_agent)
    return liste_agent

def ajout_magicien(ville,liste_agent):
    """ Ajoute un malade dans la ville de manière aléatoire """
    while True:
        x = randint(ville.position[0], ville.position[1]-1)
        y = randint(ville.position[2], ville.position[3]-1)
        if all(h.position != [x, y] for h in liste_agent):
            break

    #x = randint(ville.position[0], ville.position[1])
    #y = randint(ville.position[2], ville.position[3])
    habitant = Habitant([x,y], ville)
    habitant.magicien()
    setAgentAt(x,y,habitant.image_id)
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


def gueri_ou_pas(agent, liste_agent):
    """ Vérifie si l'agent est à côté d'un magicien """
    x, y = agent.position

    voisins = [
        [(x + 1) % 99, y], 
        [(x - 1) % 99, y], 
        [x, (y + 1) % 99], 
        [x, (y - 1) % 99], 
    ]

    for a in liste_agent:
        if a.position in voisins and a.etat == 'S':
            agent.gueri()
            break

    return 


def revenu_batiment(habitant):
    """ Chaque agent se situant dans un batiment rapporte de l'argent au génie """
    posx = habitant.position[0]
    posy = habitant.position[1]
    if evolutionMap[posx][posy] :
        genie = evolutionMap[posx][posy][0]
        if evolutionMap[posx][posy][1]:
            genie.money += evolutionMap[posx][posy][1].visiteur_batiment()
            #print(genie.name," a gagné ",evolutionMap[posx][posy][1].visiteur_batiment()," euros." )
            genie.revenu_batiment +=  evolutionMap[posx][posy][1].visiteur_batiment()


def monde_habitant(liste_agent):
    """ Avance les habitants """
    update_agent=[]
    for a in liste_agent :
        
        if random() < 0.6 :
            avancer_ou_pas(a)

        a.vie()
        revenu_batiment(a)
    
        if a.point_de_vie < 0 or a.age >=84 or getTerrainAt(a.position[0],a.position[1]) == waterId:
            a.ville_actuelle.population -= 1
            setAgentAt(a.position[0],a.position[1],0)
            continue

        elif a.etat == 'M' :
            gueri_ou_pas(a,liste_agent)
            a.point_de_vie -= 1
            if evolutionMap[a.position[0]][a.position[1]]:
                evolutionMap[a.position[0]][a.position[1]][0].money -= 10

        elif a.etat == 'V' :
            malade(a,liste_agent)
            if a.etat == 'V' and random()<pb_naissance and a.age == 50:
                creer_habitants(randint(0,3),a.ville_actuelle,update_agent)
        
        update_agent.append(a)
            

    return update_agent

def total_malade(liste_agent):
    """ Fonction qui compte le nombre de malade """
    count = 0
    for a in liste_agent:
        #print(a.etat)
        if a.etat=='M':
            count+=1
    return count

def total_gueri(liste_agent):
    """ Fonction qui compte le nombre de malade """
    count = 0
    for a in liste_agent:
        #print(a.etat)
        if a.etat=='G':
            count+=1
    return count

def total_non_malade(liste_agent):
    count = 0
    for a in liste_agent:
        #print(a.etat)
        if a.etat!='M' and a.etat!='S':
            count+=1
    return count

def total_magicien(liste_agent):
    count = 0
    for a in liste_agent:
        #print(a.etat)
        if a.etat=='S':
            count+=1
    return count


###### MONTAGNES ET INNONDATION ##########

mont2 = [81,100,61,80]

def init_mont():
    """ Initialise les montagnes """
    level = 0
    pos1 = 21
    pos2 = 60 
    pos3 = 100
    pos4 = 80
    leblock = mont2Id
    while level <=5 :
        if level == 2 :
            leblock = 13

        for i in range(pos1-(20-level*2),pos1-(level*2)):
            for j in range(pos2-(20-level*2),pos2-(level*2)):
                setObjectAt(i,j,leblock,level)
        for i in range(pos3-(20-level*2),pos3-(level*2)):
            for j in range(pos4-(20-level*2),pos4-(level*2)):
                setObjectAt(i,j,leblock,level)

        level +=1
    return
    
def fonte_glace_mont(level):
    """ Réalise la fonte des glaciers """
    pos1 = 21
    pos2 = 60 
    pos3 = 100
    pos4 = 80
    for i in range(pos1-(20-level*2),pos1-(level*2)):
            for j in range(pos2-(20-level*2),pos2-(level*2)):
                if getObjectAt(i,j,level) in [montId,mont2Id]:
                    setObjectAt(i,j,meltingId,level)

    for i in range(pos3-(20-level*2),pos3-(level*2)):
        for j in range(pos4-(20-level*2),pos4-(level*2)):
                if getObjectAt(i,j,level) in [montId,mont2Id]:
                    setObjectAt(i,j,meltingId,level)
    return

def setwater(x,y):
    """ Enlève tous les objets touchant l'eau de l'innondation produit par la fonte """
    setTerrainAt(x,y,waterId)
    if getObjectAt(x,y,1)!=mont2Id and getObjectAt(x,y,1)!=meltingId :
        setObjectAt(x,y,thewaterId,0)
        setObjectAt(x,y,0,1)
        setObjectAt(x,y,0,2)
        setObjectAt(x,y,0,3)
        setObjectAt(x,y,0,4)
        setObjectAt(x,y,0,5)
    return

def innondation(niveau_eau,water_pos):
    """ Produit l'innondation """
    for i in range(len(water_pos)):
        if water_pos[i][1]+niveau_eau < getWorldWidth():
            setwater(water_pos[i][0],water_pos[i][1]+niveau_eau)
        if water_pos[i][1]+niveau_eau > 0:
            setwater(water_pos[i][0],water_pos[i][1]-niveau_eau)
    return

#######################################
#  LEVEL INITIALISATION               #
#######################################

zone_level1=[[21,40,21,40],[21,40,41,60],[21,40,61,80],
            [41,60,21,40],[41,60,61,80],
            [61,80,21,40],[61,80,41,60],[61,80,61,80]]

ville_level1=[]

zone_level2=[[0,20,0,20],[0,20,21,40],[0,20,61,80],[0,20,81,100], # ligne du haut g->d [0,20,41,60]
            [81,100,0,20],[81,100,21,40],[81,100,41,60],[81,100,81,100], # ligne doite h->bas
            [0,20,81,100],[21,40,81,100],[41,60,81,100],[61,80,81,100], #ligne ??
            [0,20,0,20],[21,40,0,20],[41,60,0,20],[61,80,0,20],[81,100,0,20]]

ville_level2=[]

genie=[]

nom_couleur=["jaune","orange","rose","violet"]
couleur=[9,10,11,resetId]

liste_emplacement=[[3, 3], [3, 9], [3, 15], [9, 3], [9, 9], [9, 15], [15, 3], [15, 9], [15, 15]]
indice_emp=[0,1,2,3,4,5,6,7,8]


def deforestation(position,type):
    for i in range(position[0]-1,position[0]+3):
        for j in range(position[1]-1,position[1]+3):
            evolutionMap[i][j]=type
    return

def initGenie():
    for i in range(len(couleur)):
        genie.append(Genie({i},0,0.2,0.4,couleur[i]))
        print("Génie : ",i," Couleur : " ,nom_couleur[i])
    return

def initlevel0(genies):
    init_ville=Ville([41,60,41,60])
    init_ville.update_visual(terrainMap,3)
    init_ville.deverouiller(terrainMap,objectMap)
    placement = [[45,48],[45,55],[55,55],[55,48]]
    colorhouses = [yellowhouseId,orangehouseId,pinkhouseId,purplehouseId]
    for i in range(len(genies)) :
        g = genies[i]
        house = MaisonGenie(init_ville,g)
        deforestation(placement[i],[g,house])
        #print("init")
        setObjectAt(placement[i][0],placement[i][1],colorhouses[i],4)
    #print("LEVEL 0 !")
    return init_ville

def initLevel():
    for i in range(len(zone_level1)):
        v=Ville(zone_level1[i],0)
        v.verrouiller(terrainMap,objectMap)
        ville_level1.append(v)
    for j in range(len(zone_level2)):        
        v=Ville(zone_level2[j],0)
        v.verrouiller(terrainMap,objectMap)
        ville_level2.append(v)
    return

def setLevel1():
    for i in range(len(ville_level1)):
        ville_level1[i].deverouiller(terrainMap,objectMap)
    return
    
def setLevel2():
    for i in range(len(ville_level2)):
        ville_level2[i].deverouiller(terrainMap,objectMap)
    return

##### FONCTIONS SUR LE MONDE ##########


"""
def suppression_voiture(liste):
    for i in range(min(5, len(liste))):  
        setAgentAt(liste[i].pos_x, liste[i].pos_y, noAgentId)  
    return liste[5:]  
"""

def random_placement():
    """ Choix random de l'emplacement du futur batiment """
    indice = randint(0,len(indice_emp)-1)
    return liste_emplacement[indice]

def emplacement_check(ville, placement):
    """ Verifie si la place est prise """
    if placement in ville.emplacement :
        return False
    return True

def choix_ville_lvl(genie, liste_level,liste):
    """ Possibilité de debloquer une ville ou autre """
    indice = randint(0,len(liste_level)-1)
    if liste_level[indice].owner == None:

        ville = liste_level[indice]
        
        genie.villes_possedees.append(ville)
        ville.owner = genie.name
        ville.update_visual(terrainMap,genie.color)
        #liste = creer_habitants(1,ville,liste)
        
        for j in range(ville.position[0],ville.position[1]):
            for i in range(ville.position[2],ville.position[3]):
                    evolutionMap[i][j]=[genie,0]
                    setObjectAt(j,i,noObjectId,0)

        return liste
    return liste

pb_restaurant = 0.01
pb_bar = 0.1
pb_hotel = 0.3

def genie_building(genie,liste):
    """ Possibilité de mettre un building """
    if genie.villes_possedees == [] :
        return liste
    
    indice_ville = randint(0,len(genie.villes_possedees)-1)
    ville = genie.villes_possedees[indice_ville]
    placement = random_placement()

    if emplacement_check(ville,placement) :

        hasard = random()
        #objet = [resto1Id, flat_1dId, barId, house_d1Id]
        #id_objet = randint(0,3)

        if hasard < pb_restaurant : 
            batiment = genie.construire_batiment(ville,"restaurant")
            if batiment :
                deforestation((ville.position[0]+placement[0],ville.position[2]+placement[1]),[genie,batiment])
                setObjectAt(ville.position[0]+placement[0]-1,ville.position[2]+placement[1]+1,resto1Id,5)
                liste = creer_habitants(4,ville,liste)
                return liste

        elif hasard < pb_bar:  
            batiment = genie.construire_batiment(ville,"restaurant")
            if batiment is None :
                return liste
            deforestation((ville.position[0]+placement[0],ville.position[2]+placement[1]),[genie,batiment])
            setObjectAt(ville.position[0]+placement[0]-1,ville.position[2]+placement[1]+1,barId,5)
            liste = creer_habitants(5,ville,liste)
            
        elif hasard < pb_hotel:
            batiment = genie.construire_batiment(ville,"hotel")
            if batiment is None :
                return liste
            deforestation((ville.position[0]+placement[0],ville.position[2]+placement[1]),[genie,batiment])
            setObjectAt(ville.position[0]+placement[0]-1,ville.position[2]+placement[1]+1,flat_1dId,4)
            liste = creer_habitants(3,ville,liste)
            
        else:
            batiment = genie.construire_batiment(ville,"maison")
            if batiment is None :
                return liste
            deforestation((ville.position[0]+placement[0],ville.position[2]+placement[1]),[genie,batiment])
            setObjectAt(ville.position[0]+placement[0]-1,ville.position[2]+placement[1]+1,house_d1Id,4)
            liste = creer_habitants(2,ville,liste)
        
        #print("Genie ",genie.name," +5 habs")
        ville.emplacement.append(placement)

        return liste
    
    return liste

def level1_done():
    for ville in ville_level1 :
        if ville.owner==None :
            return False
    return True

###### SOMME DES TERRAINS #######

def total_terrain(liste_genie):
    total = 0
    for g in liste_genie:
        total += len(g.villes_possedees)
    return total

###### REVENUE AFFICHAGE ########

def revenue(liste_genie):
    somme = 0
    for g in liste_genie :
        # print("Génie ",g.name," possède ",g.money," euros.")
        somme += g.money
    return somme


##### Affichage nombre de buildings #####

def total_building(genie):
    total = 0
    for v in genie.villes_possedees:
        total += v.getNombreBuildings()
    return total

def calcul_nbterrain_building(nb_ville,nb_building):
    if nb_ville == 0 :
        return True
    return ((nb_building * 0.25)/nb_ville) > 1
    
###### LE JEU ########



def play_lvl(genie,liste_level,liste):

    global prix_terrain
    des = random()
    
    if des < pb_loto :
        genie.money += 10000
       # print(genie.name," VOUS AVEZ GAGNE AU LOTO, vous avez recu 10 000 euros !!! ")

    elif des<pb_malchance:
        if genie.villes_possedees != [] :
            nb_villes = len(genie.villes_possedees)
            ville = genie.villes_possedees[randint(0,nb_villes-1)]
            ajout_malade(ville,liste)
           # print(genie.name," PAS DE CHANCE, un virus se répend sur l'une de tes villes")
        return liste
    
    elif des<pb_magicien:
        if genie.villes_possedees != [] :
            nb_villes = len(genie.villes_possedees)
            ville = genie.villes_possedees[randint(0,nb_villes-1)]
            ajout_magicien(ville,liste)

    elif genie.money <= 0 : 
        genie.money+=5
       # print("Vous n'avez plus d'argent, vous recevez 5 euros...")

    elif genie.money > prix_terrain and des < pb_achatdeville and calcul_nbterrain_building(len(genie.villes_possedees),total_building(genie)) :
        liste = choix_ville_lvl(genie,liste_level,liste)
        genie.money -= prix_terrain
        prix_terrain+=200
      #  print(genie.name," UN NOUVEAU TERRAIN !!! ")

    elif genie.money > 50 and des < pb_achatbatiment :
        liste = genie_building(genie,liste)
      #  print(genie.name," UN NOUVEAU BATIMENT A ETE CONSTRUIT !!! ")
    elif des < pb_ajout_hab :
        if genie.villes_possedees != [] :
            nb_villes = len(genie.villes_possedees)
            ville = genie.villes_possedees[randint(0,nb_villes-1)]
            creer_habitants(2,ville,liste)
         #   print(genie.name," VOUS GAGNEZ 10 HABITANTS (dans l'une de tes villes) !!! ")

    return liste

##### AFFICHAGE #####

def init_fichier():
    tous_fichiers= [
        "habitants.csv",
        "revenue_batiments_g1.csv",
        "revenue_batiments_g2.csv",
        "revenue_batiments_g3.csv",
        "revenue_batiments_g4.csv",
        "genie0.csv", 
        "genie1.csv", 
        "genie2.csv", 
        "genie3.csv"

    ]
    for i in range(len(tous_fichiers)):
        with open(tous_fichiers[i], "w") as f:
            pass  


def revenu_batiment_datas(it, liste_genie):
    """Affiche et enregistre le revenu des bâtiments pour chaque génie"""
    liste_fichier = [
        "revenue_batiments_g1.csv",
        "revenue_batiments_g2.csv",
        "revenue_batiments_g3.csv",
        "revenue_batiments_g4.csv"
    ]

    for i, g in enumerate(liste_genie):
        print(g.name, "Revenue batiments :", g.revenu_batiment," Nb de villes: ",len(g.villes_possedees)," Argent : ",g.money)

        # Sécurité : si on a plus de génies que de fichiers
        if i < len(liste_fichier):
            with open(liste_fichier[i], "a", encoding="utf-8") as f:
                f.write(f"{it},{g.revenu_batiment}\n")
        else:
            print(f"Avertissement : pas de fichier pour le génie {g.name} (index {i})")

    return



def affichage(it,genie):
    revenu_batiment_datas(it,genie)
    print("Revenue total :",revenue(genie)," Prix terrain: ",prix_terrain," Total d'habitants :",len(liste_agent)," Nb terrains :",total_terrain(genie))
    print("Malade total:",total_malade(liste_agent), "Niveau eau",niveau_eau, "Nombre voitures",len(voiture))


def efface_revenu(liste_genie):
    for g in liste_genie :
        g.init_revenu()
    return

def end_game_datas(liste,endgame):
    for g in liste :
        datas = [g.name,g.color,g.money,len(g.villes_possedees),total_building(g)]
        endgame.append(datas)
    return

def end_game_print(endgame):
    for d in endgame :
        print(" Genie n° ",d[0],"(",d[1],")"," a ",d[2]," euros possède ",d[3]," villes et ",d[4],"batiments.")
    return

def coeff_gagnant(nb_argent,nb_villes,nb_batiment):
    return 0.5 * nb_argent + 90 * nb_villes + 10 * nb_batiment

def choix_gagnant(endgame):
    gagnant = []
    max = 0
    for d in endgame :
        total = coeff_gagnant(d[2],d[3],d[4])
        if max < total :
            max = total
            gagnant = d
    print("Le gagnant est génie : ",gagnant[0])
    return 

##### DONNEES POUR LES GRAPHES #####

def datas_graphes_monde(it, liste):
    fichiers = ["genie0.csv", "genie1.csv", "genie2.csv", "genie3.csv"]

    for i, g in enumerate(liste):
        if i < len(fichiers):
            with open(fichiers[i], "a", encoding="utf-8", newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    it,
                    g.color,
                    g.money,
                    len(g.villes_possedees),
                    total_building(g),
                    coeff_gagnant(g.money, len(g.villes_possedees), total_building(g))
                ])

def datas_graphes_habitant(it, liste):
    nb_malade = total_malade(liste)
    nb_gueri = total_gueri(liste)
    nb_nonmalade = total_non_malade(liste)
    nb_magicien = total_magicien(liste)

    print(f"{it},{nb_malade},{nb_gueri},{nb_nonmalade},{nb_magicien}")

    with open("habitants.csv", "a", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([it, nb_malade, nb_gueri, nb_nonmalade, nb_magicien])


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

def initWorld():
    global argent
    global voiture
    global liste_agent
    global init_ville
    global liste_level
    global level_eau, niveau_eau, water_pos, endgame
    global break_water,arret_mondial

    liste_level = ville_level1
    liste_agent =[]
    argent=0
    endgame = []
    arret_mondial = False 
    break_water = randint(12,23)

    level_eau = 5
    niveau_eau = 0
    
    amplitude = 3  # Amplitude de la courbe en S
    frequence = 0.2  # Fréquence de la sinusoïde
    decalage = 50 # Départ au centre
    inclinaison= 0.25

    # Générer les coordonnées du ruisseau
    water_pos = []
    for i in range(100):
        j = int(decalage + amplitude * math.sin(frequence * i)+ (inclinaison*i))  # Forme en S
        if 0 <= j < 100:
            setTerrainAt(i,j,waterId)
            water_pos.append([i,j])
        if 0 <= j+1 < 100:  
            setTerrainAt(i, j+1, waterId)
            water_pos.append([i,j+1])
        if 0 <= j+2 < 100:  
            setTerrainAt(i, j+2, waterId)
            water_pos.append([i,j+2])

    voiture=[]

    for j in range(1,5):
        for i in range(getWorldWidth()):
            setTerrainAt(i,j*20,greyId)
            setTerrainAt(j*20,i,greyId)
            if len(voiture)<50 and i%20==0:
                new_v1=Voiture(j*20,i,voitureId[randint(0,2)],'U')
                setVoitureAt(new_v1)
                voiture.append(new_v1)

    init_fichier()
    initGenie()
    init_ville = initlevel0(genie)
    initLevel()
    init_mont()
    liste_agent = creer_habitants(20,init_ville,liste_agent)
    #ajout_malade(init_ville,liste_agent)

def stepWorld( it = 0 ):
    global xViewOffset, yViewOffset
    global argent
    global voiture, init_ville
    global liste_level
    global prix_terrain
    global liste_agent
    global level_eau, niveau_eau, water_pos
    global break_water, arret_mondial

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

    
    #### Mouvement des Voitures #####

    stepVoiture(voiture)

    #### Mouvement des habitants #######

    liste_agent = monde_habitant(liste_agent)

    if total_terrain(genie) == 10 and total_malade(liste_agent) == 0 :
        ajout_malade_alea(genie,liste_agent)

    
    if total_terrain(genie) > 12 and total_malade(liste_agent) == 0 and random()<0.02:
        ajout_malade_alea(genie,liste_agent)

    if arret_mondial is False : 

        for g in genie :
            liste_agent = play_lvl(g,liste_level,liste_agent)
            
        if level1_done() :
            liste_level = ville_level2

        if(it%20 == 0):
            affichage(it,genie)
            datas_graphes_monde(it,genie)
            datas_graphes_habitant(it,liste_agent)
        
    if  level_eau == 4 :
        end_game_datas(genie,endgame)
        end_game_print(endgame)
    
    ##### PARTIE FONTE DES GLACES ######

    if total_terrain(genie) > break_water and niveau_eau < 125 and random()<0.4:
        arret_mondial = True
        if level_eau > -1 :
            fonte_glace_mont(level_eau)
            level_eau-=1
        else :
            if niveau_eau < len(voiture):
                disparition(voiture,niveau_eau)
            innondation(niveau_eau,water_pos)
            niveau_eau+=1

    if niveau_eau == 124 :
        choix_gagnant(endgame)

    return

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

timestamp = datetime.datetime.now().timestamp()

loadAllImages()

displayWelcomeMessage()

initWorld()

print ("initWorld:",datetime.datetime.now().timestamp()-timestamp,"second(s)")
timeStampStart = timeStamp = datetime.datetime.now().timestamp()

it = itStamp = 0

userExit = False

while userExit == False:

    if it != 0 and it % 100 == 0 and verboseFps:
        #print ("[fps] ", ( it - itStamp ) / ( datetime.datetime.now().timestamp()-timeStamp ) )
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
            elif event.key == pygame.K_s and not( pygame.key.get_mods() & pygame.KMOD_SHIFT ) :
                if scaleMultiplier > 0.08:
                    scaleMultiplier = scaleMultiplier / 2
                if scaleMultiplier < 0.08:
                    scaleMultiplier = 0.08
                resetImages()
                if verbose:
                    print ("scaleMultiplier is ",scaleMultiplier)
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                if scaleMultiplier < 1.0:
                    scaleMultiplier = scaleMultiplier * 2
                if scaleMultiplier > 1.0:
                    scaleMultiplier = 1.0
                resetImages()
                if verbose:
                    print ("scaleMultiplier is ",scaleMultiplier)

    

    pygame.display.flip()
    fpsClock.tick(maxFps) # recommended: 30 fps

    it += 1

fps = it / ( datetime.datetime.now().timestamp()-timeStampStart )
print ("[Quit] (", fps,"frames per second )")

pygame.quit()
sys.exit()
