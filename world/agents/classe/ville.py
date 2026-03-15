from ursina import Vec3, color
from random import uniform, randint
from agents.classe.habitant import Habitant 

class Ville:
    def __init__(self, position, prix=0, accessible=True, max_visites=10):
        self.position = position  # Utilisation de Vec3 pour la position
        self.prix = prix
        self.population = 0
        self.accessible = accessible  # La ville est accessible par défaut
        self.owner = None
        self.buildings = []  # Liste des bâtiments (hôtel, restaurant)
        self.revenue = 0
        self.habitants = [] 
        self.visites = 0  # Nombre de visites actuelles
        self.max_visites = max_visites  # Capacité maximale de la ville
        self.color = 6  # Couleur par défaut
        self.emplacement = [] # Emplcement des buildings 
    
    def visiter_batiments(self):
        #Fait visiter les bâtiments aux habitants en fonction des probabilités.
        if not self.accessible:
            #print(f"❌ La ville {self.position} est privée. Pas de visite possible.")
            return False

        if self.visites >= self.max_visites:
            # print(f"⚠ {self.position} est saturée et ne peut plus accueillir de visiteurs.")
            return False

        for habitant in self.habitants:
            if uniform(0, 1) > 0.7:  # Seulement 70% des habitants décident de visiter un bâtiment
                continue

            batiment_choisi = None
            for batiment in self.buildings:
                if uniform(0, 1) < batiment.proba_visite:
                    batiment_choisi = batiment
                    break

            if batiment_choisi:
                batiment_choisi.visites += 1
                self.visites += 1
                print(f"🏛 Un habitant visite {batiment_choisi.nom} dans {self.position}. Visites actuelles: {self.visites}/{self.max_visites}")
        
        return True
    
    def ajout_building(self,building):
        self.buildings.append(building)

    def peut_accueillir(self):
        #Retourne True si la ville peut encore recevoir des habitants.
        return self.accessible and self.visites < self.max_visites

    def ajouter_visite(self):
        #Augmente le compteur de visites si la ville n'est pas saturée et accessible.
        if self.peut_accueillir():
            self.visites += 1
            return True
        else:
            print(f"🚫 {self.position} est soit privée, soit saturée !")
            return False
    
    def verrouiller(self,terrain,objetmap):
        """Rend la ville privée et inaccessible aux visiteurs."""
        self.accessible = False
        print("position: ",self.position)
        for j in range(self.position[0],self.position[1]):
            for i in range(self.position[2],self.position[3]):
                if terrain[i][j]!= 2 and terrain[i][j]!=3 : # 2 -> waterId
                    terrain[i][j]= 6
                    objetmap[0][i][j]=1
        return

    def deverouiller(self,terrain,objetmap):
        """Rend la ville accessible aux habitants et visiteurs."""
        self.accessible = True
        for j in range(self.position[0],self.position[1]):
            for i in range(self.position[2],self.position[3]):
                if terrain[i][j]!= 2 : # 2 -> waterId
                    terrain[i][j]=6

        #print(f"🔓 {self.position} est maintenant accessible !")
        return

    def update_visual(self, terrain, color):
        """ Met à jour l'apparence du terran """
        #self.owner=owner
        for j in range(self.position[0],self.position[1]):
            for i in range(self.position[2],self.position[3]):
                if terrain[i][j]!= 2 : # 2 -> waterId
                    terrain[i][j]= color
        return
    
    def getNombreBuildings(self):
        return len(self.buildings)
    