import csv

# Ouvre le fichier texte en lecture
with open('datas1.txt', 'r', encoding='utf-8') as fichier_texte:
    lignes = fichier_texte.readlines()

# Garde seulement les lignes dont l'index (ligne 3, 6, 9...) est divisible par 3
lignes_div3 = [ligne.strip() for i, ligne in enumerate(lignes, start=1) if i % 5 == 0]

# Écrit dans le fichier CSV
with open('datas1_genie0.csv', 'w', newline='', encoding='utf-8') as fichier_csv:
    writer = csv.writer(fichier_csv)
    for ligne in lignes_div3:
        writer.writerow([ligne])  # Une seule colonne

# Garde seulement les lignes dont l'index (ligne 3, 6, 9...) est divisible par 3
lignes_div3 = [ligne.strip() for i, ligne in enumerate(lignes, start=1) if i % 5 == 1]

# Écrit dans le fichier CSV
with open('datas1_genie1.csv', 'w', newline='', encoding='utf-8') as fichier_csv:
    writer = csv.writer(fichier_csv)

    for ligne in lignes_div3:
        writer.writerow([ligne])  # Une seule colonne

# Garde seulement les lignes dont l'index (ligne 3, 6, 9...) est divisible par 3
lignes_div3 = [ligne.strip() for i, ligne in enumerate(lignes, start=1) if i % 5 == 2]

# Écrit dans le fichier CSV
with open('datas1_genie2.csv', 'w', newline='', encoding='utf-8') as fichier_csv:
    writer = csv.writer(fichier_csv)
    for ligne in lignes_div3:
        writer.writerow([ligne])  # Une seule colonne

# Garde seulement les lignes dont l'index (ligne 3, 6, 9...) est divisible par 3
lignes_div3 = [ligne.strip() for i, ligne in enumerate(lignes, start=1) if i % 5 == 3]

# Écrit dans le fichier CSV
with open('datas1_genie3.csv', 'w', newline='', encoding='utf-8') as fichier_csv:
    writer = csv.writer(fichier_csv)
    for ligne in lignes_div3:
        writer.writerow([ligne])  # Une seule colonne

# Garde seulement les lignes dont l'index (ligne 3, 6, 9...) est divisible par 3
lignes_div3 = [ligne.strip() for i, ligne in enumerate(lignes, start=1) if i % 5 == 4]

# Écrit dans le fichier CSV
with open('datas1_habitants.csv', 'w', newline='', encoding='utf-8') as fichier_csv:
    writer = csv.writer(fichier_csv)
    for ligne in lignes_div3:
        writer.writerow([ligne])  # Une seule colonne

