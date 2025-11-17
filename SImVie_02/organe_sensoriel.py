import math

class Narine:
    def __init__(self, sensibilite_olfactive):
        self.hemi_nourriture_gauche = 0
        self.hemi_nourriture_droite = 0
        self.hemi_pheromone_droite = 0
        self.hemi_pheromone_gauche = 0

        self.sensibilite_olfactive = sensibilite_olfactive
        self.portee_olfactive = (150 + math.sqrt(self.taille) * 30) * self.sensibilite_olfactive