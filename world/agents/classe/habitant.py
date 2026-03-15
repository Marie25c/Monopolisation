from ursina import Vec3, color
from random import uniform, choices, randint

class Habitant:
    # = 4.0  # Distance minimale pour changer de ville

    def __init__(self, position, ville_actuelle):
        self.position = position
        self.ville_actuelle = ville_actuelle
        self.point_de_vie = 5
        self.age = 0
        self.etat = 'V' # 'M' -> Malade 'G' -> Gueri 'V' -> rien 'D' -> mort
        self.image_id= 5

    def visiter_ville(self, ville):
        """Tente de visiter un bâtiment dans la ville."""
        for batiment in ville.buildings:
            if batiment.ajouter_visiteur():  # Vérifie si un bâtiment a de la place
                print(f"Habitant {self} visite {batiment.__class__.__name__} à {ville.position}")
                return True  # Il a trouvé un bâtiment disponible
            return False  # Aucun bâtiment disponible
        
    def one_step(self):
        """ Bouge les habitants pas à pas en restant dans la ville """
        pas = randint(1, 4)
        new_position = self.position[:]  # Copie la position actuelle
        ville_position = self.ville_actuelle.position

        if pas == 1:
            new_position[0] = (new_position[0] + 1 - ville_position[0]) % (ville_position[1] - ville_position[0] + 1) + ville_position[0]
        elif pas == 2:
            new_position[1] = (new_position[1] + 1 - ville_position[2]) % (ville_position[3] - ville_position[2] + 1) + ville_position[2]
        elif pas == 3:
            new_position[1] = (new_position[1] - 1 - ville_position[2]) % (ville_position[3] - ville_position[2] + 1) + ville_position[2]
        else:
            new_position[0] = (new_position[0] - 1 - ville_position[0]) % (ville_position[1] - ville_position[0] + 1) + ville_position[0]

        #self.position = new_position
  
        return new_position
    
    def vie(self):
        self.age += 0.1
        self.point_de_vie += 0.1

    
    def change_position(self,position):
        self.position=position
    
    def malade(self):
        self.etat = 'M'
        self.image_id = 6

    def gueri(self):
        self.etat = 'G'
        self.image_id = 8

    def magicien(self):
        self.etat = 'S'
        self.image_id = 7






