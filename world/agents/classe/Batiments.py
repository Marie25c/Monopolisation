class Batiment:
    def __init__(self, ville, cout, prob_visite, capacite_max):
        self.ville = ville
        self.cout = cout
        self.prob_visite = prob_visite
        self.capacite_max = capacite_max  # Nombre max d'habitants à la fois
        self.visiteurs_actuels = 0        # Nombre d'habitants actuellement dans le bâtiment
        self.visites_total = 0            # Total des visites (historique)

    def generer_revenue(self):
        """Calcule le revenu en fonction du nombre de visiteurs et réinitialise les visiteurs."""
        revenue = self.visiteurs_actuels * self.revenu_base
        self.visites_total += self.visiteurs_actuels  # Historique des visites
        self.visiteurs_actuels = 0  # Réinitialiser les visiteurs après collecte
        return revenue

    def peut_accueillir(self):
        """Vérifie si le bâtiment peut encore accueillir des visiteurs."""
        return self.visiteurs_actuels < self.capacite_max

    def ajouter_visiteur(self):
        """Ajoute un visiteur si la capacité n'est pas atteinte."""
        if self.peut_accueillir():
            self.visiteurs_actuels += 1
            return True
        return False
    
    def visiteur_batiment(self):
        return self.cout

class Hotel(Batiment):
    def __init__(self, ville):
        super().__init__(ville, 10, 0.8, 5)  # 5 visiteurs max

class Restaurant(Batiment):
    def __init__(self, ville):
        super().__init__(ville, 15, 0.6, 3)  # 3 visiteurs max

class MaisonGenie(Batiment):
        def __init__(self,ville,genie):
            super().__init__(ville,10,0.5,3)
            self.genie=genie