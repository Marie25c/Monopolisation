Agent et environnement : Marie-Christine MUSA

--- INTRODUCTION ----

Le projet s'inspire du jeu du monopoly.
D'après Wiképédia, le Monopoly est déféni comme étant un jeu de société sur parcours dont le but est, à travers l'achat et la vente de propriétés, de ruiner ses adversaires et ainsi parvenir au monopole. Le hasard y joue une part importante.
Dans notre projet, on reprend l'idée d'emprise de terrains et l'achat de batiment avec le hasard.
Pour présenter le projet avant d'executer le programme, on a 4 génies. Les génies sont les joueurs du jeu.
Chaque joueurs possède une couleur.
Le Génie 0 a la couleur jaune, le génie 1 a la couleur orange, le génie 2 est rose et le génie 3 est violet.
Les Génies ne sont pas visibles car ce sont nous. 

---- NIVEAU INITIAL ----

Au lancement du jeu, nous pouvons apercevoir la ville initiale qui contient 4 maisons liées à chaque génie et 10 habitants.
Les génies n'ont pas d'argent au début. Mais, c'est grâce aux habitants qu'ils obtiennent de l'argent. Chaque passage d'habitant dans l'une des maisons rapporte de l'argent au génie dont la couleur est celle de la maison.

----- NIVEAU 1 ET 2 ---------

Une fois que les génies ont pu récolté une somme d'argent supérieur à 100, ils peuvent passé au niveau 1 puis 2, c'est-à- dire qu'ils pourront acheté des terrains. 
Plus les terrains sont achetés plus le prix augmente. Une fois que les génies achètent des terrains, ils peuvent se permette d'acheter des batiments. 

----- ATTENTION, IL EST POSSIBLE D'AVOIR DES EVENEMNTS IMPROBABLES ------

* Il est possible qu'une maladie se propage dans la population ce qui peut impacter sur les revenues des génies
* Il est également possible d'avoir une innondation qui se propage dans la monde à cause de la pollution produite par l'urbanisation du monde

----- OU L'INVERSE -----

* Il est possible d'avoir des magiciens, des êtres qui guérissent les malades ce qui peut être avantageux.

Graphes :

* cd plotCSV-pythpn3

-Génération revenue des batiments-

python plot.py <dossier>/revenue_batiments_g?+1.csv 0 2 -xLabel "Nombre d'itération" -yLabel "Revenue généré grâce au batiments (money)" -title "Evolution des revenues générés grâce aux batiments du génie ?"

