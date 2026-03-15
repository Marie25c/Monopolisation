from agents.classe.Batiments import Hotel, Restaurant, Batiment

class Genie:
    def __init__(self, name, money, pb_achat, pb_construction, color):
        self.name = name
        self.money = money
        self.pb_achat = pb_achat  # Probabilité d'achat
        self.pb_construction = pb_construction  # Probabilité de construire un bâtiment
        self.color = color
        self.villes_possedees = []  # Liste des villes possédées
        self.revenu_batiment = 0

    def buy_city(self, ville):
        """Le Génie achète une ville si elle est disponible et devient propriétaire."""
        
        if not ville.accessible and ville.owner is None:  # La ville ne peut être achetée que si elle est inaccessible et sans propriétaire
            if self.money >= ville.prix:
                self.money -= ville.prix
                ville.owner = self
                ville.acheter = True  # La ville devient acheter après l'achat
                ville.color = self.color
                self.villes_possedees.append(ville)
                ville.update_visual() 

                print(f" {self.name} a acheté la ville {ville.position} pour {ville.prix}. Argent restant : {self.money}")
            else:
                print(f" {self.name} n'a pas assez d'argent pour acheter {ville.position}.")
        else:
            print(f"{ville.position} ne peut pas être achetée (déjà achetée ou acheter).")

    def construire_batiment(self, ville, type_batiment):

        """Construit un bâtiment (Hôtel ou Restaurant) dans une ville possédée."""
        """
        if ville not in self.villes_possedees:
            print(f"🚫 {self.name} ne possède pas cette ville ({ville.position}) !")
            return False

        if any(isinstance(b, Hotel) for b in ville.buildings) and type_batiment == "hotel":
            print(f"🏨 {self.name} a déjà un hôtel dans cette ville !")
            return False

        if any(isinstance(b, Restaurant) for b in ville.buildings) and type_batiment == "restaurant":
            print(f"🍽 {self.name} a déjà un restaurant dans cette ville !")
            return False
        """

        # Définition des coûts
        cout_hotel = 50
        cout_restaurant = 40
        cout_maison = 10

        if type_batiment == "hotel" and self.money >= cout_hotel:
            self.money -= cout_hotel
            hotel=Hotel(ville)
            ville.buildings.append(hotel)
            #print(f"🏨 Hotel ! {self.name} . Argent restant : {self.money}")
            return hotel

        elif type_batiment == "restaurant" and self.money >= cout_restaurant:
            self.money -= cout_restaurant
            resto = Restaurant(ville)
            ville.buildings.append(resto)
            #print(f"🍽 Restaurant ! {self.name} 💶 : {self.money}")
            return resto
        
        elif type_batiment == "maison" and self.money >= cout_maison:
            self.money -= cout_restaurant
            resto = Batiment(ville,0,0.5,3)
            ville.buildings.append(resto)
            #print(f"🏠 Maison ! {self.name} 💶 : {self.money}")
            return resto

        else:

            return None
    
    def init_revenu(self):
        self.revenu_batiment=0
