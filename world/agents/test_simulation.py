import unittest
from ursina import Vec3, color
from classe.ville import Ville
from classe.Genie import Genie
from classe.Habitants import Habitant
from classe.Batiments import Hotel, Restaurant

class TestSimulation(unittest.TestCase):
    
    def test_creation_ville(self):
        ville = Ville(position=Vec3(0, 0, 0), prix=100, population=5, acheter=False)
        self.assertEqual(ville.position, Vec3(0, 0, 0))
        self.assertEqual(ville.prix, 100)
        self.assertEqual(ville.population, 5)
        
    
    def test_ajout_habitants(self):
        ville = Ville(position=Vec3(1, 0, 1),acheter=True, prix=50)
        ville.creer_habitants(3)
        self.assertEqual(len(ville.habitants), 3)
    
    def test_habitant_deplacement(self):
        ville1 = Ville(position=Vec3(0, 0, 0))
        ville2 = Ville(position=Vec3(3, 0, 3))
        habitant = Habitant(position=Vec3(0, 0, 0), ville_actuelle=ville1)
        nouvelles_villes = [ville1, ville2]
        habitant.bouger(nouvelles_villes)
        self.assertIn(habitant.ville_actuelle, nouvelles_villes)
    
    def test_genie_achat_ville(self):
        genie = Genie(name="Aladdin", money=200, pb_achat=0.5, pb_construction=0.5, color=color.blue)
        ville = Ville(position=Vec3(5, 0, 5), prix=100, acheter=False)
        genie.buy_city(ville)
        self.assertEqual(ville.owner, genie)
        self.assertTrue(ville.acheter)
        self.assertEqual(genie.money, 100)  # 200 - 100 après l'achat
    
    def test_construction_batiment(self):
        genie = Genie(name="Aladdin", money=100, pb_achat=0.5, pb_construction=0.5, color=color.blue)
        ville = Ville(position=Vec3(2, 0, 2), prix=50, acheter=False)
        genie.buy_city(ville)
        print(f"Propriétaire de la ville après achat: {ville.owner}")
        self.assertEqual(ville.owner, genie)  # Vérifie que le génie est bien propriétaire
        genie.construire_batiment(ville, "hotel")
        
        self.assertEqual(len(ville.buildings), 1)
        self.assertIsInstance(ville.buildings[0], Hotel)
        self.assertEqual(genie.money, 0)  # 100 - 50 -50 (hotel et ville) après construction
    
    def test_revenu_batiments(self):
        ville = Ville(position=Vec3(0, 0, 0))
        hotel = Hotel(ville)
        restaurant = Restaurant(ville)
        ville.buildings.append(hotel)
        ville.buildings.append(restaurant)
        
        hotel.ajouter_visiteur()
        hotel.ajouter_visiteur()
        restaurant.ajouter_visiteur()
        
        revenu_total = hotel.generer_revenue() + restaurant.generer_revenue()
        self.assertEqual(revenu_total, 35)  # (10 * 2) + (15 * 1) = 35

if __name__ == '__main__':
    unittest.main()
