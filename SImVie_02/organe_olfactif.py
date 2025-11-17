import math, random
from SimVie_Neurone import Neurone

class Narine:
    def __init__(self, taille_creature, sensibilite_olfactive):
        self.hemi_nourriture_gauche = 0
        self.hemi_nourriture_droite = 0
        self.hemi_pheromone_droite = 0
        self.hemi_pheromone_gauche = 0

        self.sensibilite_olfactive = sensibilite_olfactive
        self.portee_olfactive = (150 + math.sqrt(taille_creature) * 30) * self.sensibilite_olfactive

        self.capteur = CapteurOlfactif()

class CapteurOlfactif:

    def __init__(self, nb_capteurs=8, nb_vomeronasal=8):
        self.capteurs = []
        for i in range(nb_capteurs):
            neurone = Neurone(seuil=0.5)
            self.capteurs.append(neurone)

        self.vomeronasal = []
        for i in range(nb_vomeronasal):
            neurone = Neurone(seuil=1.0)
            self.vomeronasal.append(neurone)

        self.ganglion = GanglionOlfactif(self.capteurs, self.vomeronasal)

class GanglionOlfactif:

    def __init__(self, capteur, vomeronasal, nb_ganglions=4):

        self.neurone = []
        for i in range(nb_ganglions):
            neurone = Neurone(seuil=1.0)
            self.neurone.append(neurone)

        # Connexions aléatoires entre couches
        ## Première couche
        for c in capteur:
            for g in random.sample(self.neurone, k=2):
                c.connecter_a(g, random.uniform(0.5, 1.0))
        for v in vomeronasal:
            for g in random.sample(self.neurone, k=2):
                v.connecter_a(g, random.uniform(0.5, 1.0))