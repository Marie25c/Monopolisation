










Recapitulatif 

    Des villes peuvent etre achetees par des genies.
    Chaque ville a des batiments (hotels et restaurants) qui generent des revenus.
    Des habitants se deplacent entre les villes et visitent les batiments, generant ainsi des revenus pour les genies.
    Les villes ont des limites de visiteurs, une probabilite d'attractivite et peuvent etre bloquees/debloquees.

 1. Les villes (Ville)

Chaque ville a :
Un prix d'achat.
Un proprietaire (Genie) (sinon elle est neutre).
Des habitants qui peuvent la visiter.
Deux batiments maximum : un hotel et un restaurant.
Une limite de visiteurs : une ville saturee ne peut plus accueillir d'habitants.
 Une attractivite qui influence la probabilite qu'un habitant s'y rende.

 Une ville bloquee (bloque=False) ne peut pas etre visitee tant qu'elle n'est pas debloquee.
 2. Les batiments (Hotel et Restaurant)

Chaque batiment :
A une capacite limitee de visiteurs en meme temps.
Genere un revenu base sur le nombre de visiteurs.
A une probabilite d'etre visite par un habitant dans la ville.

 Si un habitant veut visiter un batiment mais qu'il est plein, il peut soit attendre soit chercher une autre ville.
3. Les genies (Genie)

Les genies peuvent :
Acheter des villes s'ils ont assez d'argent.
Construire un hotel et un restaurant dans leurs villes (mais pas ailleurs).
Gagner de l'argent grace aux batiments qu'ils possedent.
Gerer leur budget : s'ils n'ont pas assez d'argent, ils ne peuvent pas acheter ou construire.
 4. Les habitants (Habitant)

Chaque habitant :
Commence dans une ville centrale.
Se deplace aleatoirement dans la ville.
Peut decider de visiter un batiment.
S'il n'y a plus de place dans les batiments, il peut :

    Attendre qu'une place se libere.
    Chercher une autre ville accessible.
    Ne peut pas traverser toute la carte d'un coup (distance minimale requise).
    Utilise une fonction bouger() qui le fait se deplacer progressivement vers une nouvelle ville.

 5. Revenus et gestion economique

Un genie collecte l'argent grace aux batiments.
Les habitants generent de l'argent en visitant les hotels et restaurants.
Un genie peut investir dans des nouvelles villes ou batiments.
Si un batiment atteint sa capacite maximale, il ne genere pas plus de revenus.
6. Ameliorations recentes

 Les habitants ne se teleportent plus : ils se deplacent progressivement.
 Mouvement realiste entre les villes en respectant une distance minimale.
 Gestion de la saturation des batiments :

    S'ils sont pleins, l'habitant peut attendre ou chercher une autre ville.
     Villes accessibles en fonction de leur attractivite et de la distance.
     