from ursina import Vec3, color
from random import uniform
from classe.Habitants import Habitant

class Ville:
    def __init__(self, position, prix=0, population=0, acheter=False, max_visites=10):
        self.position = Vec3(position)  # Utilisation de Vec3 pour la position
        self.prix = prix
        self.population = population
        self.acheter = acheter  # La ville est acheter par défaut
        self.owner = None
        self.buildings = []  # Liste des bâtiments (hôtel, restaurant)
        self.revenue = 0
        self.habitants = []
        self.visites = 0  # Nombre de visites actuelles
        self.max_visites = max_visites  # Capacité maximale de la ville
        self.color = color.gray  # Couleur par défaut

    def creer_habitants(self, count):
        """Crée des habitants uniquement si la ville est acheter.sauf pour la premiere ville . cette fonction est faites pour la premiere ville"""
        if not self.acheter:

            print(f" La ville {self.position} est privée. Impossible d'ajouter des habitants.")


        for _ in range(count):
            habitant = Habitant(position=self.position + Vec3(uniform(-0.4, 0.4), 0.2, uniform(-0.4, 0.4)), ville_actuelle=self)
            self.habitants.append(habitant)

    def visiter_batiments(self):
        """Fait visiter les batiments aux habitants en fonction des probabilitee."""
        if not self.acheter:
            print(f" La ville {self.position} est fermee. Pas de visite possible.")
            return

        if self.visites >= self.max_visites:
            print(f" {self.position} est saturée et ne peut plus accueillir de visiteurs.")
            return

        for habitant in self.habitants:
            if uniform(0, 1) > 0.7:  # Seulement 70% des habitants décident de visiter un bâtiment
                continue

            batiment_choisi = None
            for batiment in self.buildings:
                if uniform(0, 1) < batiment.prob_visite:
                    batiment_choisi = batiment
                    break

            if batiment_choisi:
                batiment_choisi.visites += 1
                self.visites += 1
                print(f"Un habitant visite {batiment_choisi.nom} dans {self.position}. Visites actuelles: {self.visites}/{self.max_visites}")

    def peut_accueillir(self):
        """Retourne True si la ville peut encore recevoir des habitants."""
        return self.acheter and self.visites < self.max_visites

    def ajouter_visite(self):
        """Augmente le compteur de visites si la ville n'est pas saturée et acheter."""
        if self.peut_accueillir():
            self.visites += 1
        else:
            print(f" {self.position} est soit privée, soit saturée !")

    def verrouiller(self):
        """Rend la ville privée et  ."""
        self.acheter = True
        print(f" {self.position} est maintenant privée et inacheter aux visiteurs.")


    def deverouiller(self):
        """Rend la ville acheter aux habitants et visiteurs."""
        self.acheter = False
        print(f" {self.position} est maintenant acheter !")



    def update_visual(self):
        """Met à jour l'apparence de la ville en fonction de son propriétaire."""
        self.color = self.owner.color if self.owner else color.gray

    def update(self):
        """Met à jour les positions des habitants."""
        if self.acheter:
            for habitant in self.habitants:
                habitant.bouger()  # Appel à la méthode `bouger` de l'habitant
