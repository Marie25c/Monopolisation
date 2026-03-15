import pygame

# Initialisation
pygame.init()
largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Jeu avec popup gagnant")

# Fond du monde
fond_monde = pygame.Surface((largeur, hauteur))
fond_monde.fill((50, 150, 200))  # Un fond bleu clair

# Police et texte
police = pygame.font.SysFont(None, 48)
texte_gagnant = police.render("🎉 Joueur 1 a gagné ! 🎉", True, (255, 255, 255))

# Popup (rectangle semi-transparent)
popup_largeur, popup_hauteur = 400, 150
popup_surface = pygame.Surface((popup_largeur, popup_hauteur), pygame.SRCALPHA)
popup_surface.fill((0, 0, 0, 180))  # Noir avec transparence

# Boucle principale
clock = pygame.time.Clock()
running = True
afficher_popup = True  # Toggle selon si tu veux afficher le message ou non

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dessine le monde
    fenetre.blit(fond_monde, (0, 0))

    # Affiche le popup si besoin
    if afficher_popup:
        x = (largeur - popup_largeur) // 2
        y = (hauteur - popup_hauteur) // 2
        fenetre.blit(popup_surface, (x, y))
        fenetre.blit(texte_gagnant, (x + 40, y + 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
