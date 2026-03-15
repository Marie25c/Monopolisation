<<<<<<< HEAD
=======
from ursina import Vec3, color
from random import uniform, choices, random

class Habitant:
    DISTANCE_MINIMALE = 4.0  # Distance minimale pour changer de ville

    def __init__(self, position, ville_actuelle):
        self.position = Vec3(position)  # Utilisation de Vec3 pour la position
        self.ville_actuelle = ville_actuelle  
        self.color = color.green  # Garde la couleur d'Ursina
        self.speed = 0.01
        self.cible = None  # Nouvelle position cible
        self.en_deplacement = False  # Indique s'il est en train de se déplacer

    def villes_accessibles(self, villes):
        """Retourne les villes proches et disponibles."""
        return [v for v in villes if v.acheter and v.peut_accueillir() and self.est_proche(v)]

    def est_proche(self, ville):
        """Vérifie si la ville est assez proche pour être rejointe."""
        return self.distance_2d(self.position, ville.position) <= self.DISTANCE_MINIMALE

    def choisir_ville(self, villes):
        villes_disponibles = self.villes_accessibles(villes)
        if not villes_disponibles:
            return self.ville_actuelle  

        villes_disponibles.sort(key=lambda v: self.distance_2d(self.position, v.position))
        return villes_disponibles[0] if villes_disponibles else self.ville_actuelle

    def visiter_ville(self, ville):
        """Tente de visiter un bâtiment dans la ville."""
        for batiment in ville.buildings:
            if batiment.ajouter_visiteur():  # Vérifie si un bâtiment a de la place
                print(f"Habitant {self} visite {batiment.__class__.__name__} à {ville.position}")
                return True  # Il a trouvé un bâtiment disponible
        return False  # Aucun bâtiment disponible

    def bouger(self, villes):
        """Gère le déplacement des habitants et le changement de ville."""
        
        # Si l'habitant est en déplacement vers une cible, continue son mouvement
        if self.en_deplacement and self.cible:
            direction = (self.cible - self.position).normalized()
            self.position += direction * self.speed
            
            # Vérifier si l'habitant est arrivé à destination
            if self.distance_2d(self.position, self.cible) < 0.1:
                self.position = self.cible  # Ajuster la position finale
                self.en_deplacement = False
                self.cible = None
            return

        # Essayer de visiter un bâtiment dans la ville actuelle
        if self.visiter_ville(self.ville_actuelle):
            return  # Il a trouvé une place et ne bouge pas

        # Chercher une nouvelle ville si nécessaire
        nouvelle_ville = self.choisir_ville(villes)
        if nouvelle_ville and nouvelle_ville != self.ville_actuelle:
            print(f"Habitant {self} se déplace vers {nouvelle_ville.position}")
            self.ville_actuelle = nouvelle_ville
            self.cible = nouvelle_ville.position
            self.en_deplacement = True  # Début du mouvement progressif 

    @staticmethod
    def distance_2d(pos1, pos2):
        """Retourne la distance 2D entre deux positions (ignorer l'axe Y)."""
        return ((pos1.x - pos2.x) ** 2 + (pos1.z - pos2.z) ** 2) ** 0.5






>>>>>>> origin
