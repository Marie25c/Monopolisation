MAX_VALUE = 100

class Voiture:

    def __init__(self, pos_x,pos_y, id, mode):
        self.pos_x=pos_x
        self.pos_y=pos_y
        self.id=id
        self.mode=mode # R : droite / L : gauche / U : haut / D : bas

    def move(self):
        if self.mode == 'R':
            self.pos_x+=1
        elif self.mode == 'L':
            self.pos_x-=1
        elif self.mode == 'U':
            self.pos_y-=1
        else :
            self.pos_y+=1



    

    
