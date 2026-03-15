from ursina import *

app = Ursina()

# Ajoutez un cube simple dans la scène
cube = Entity(model='cube', color=color.orange, scale=(2, 2, 2))

def input(key):
    if key == 'q':  # Appuyez sur Q pour quitter
        quit()

app.run()