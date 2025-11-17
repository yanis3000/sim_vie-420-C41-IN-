# ------------------------------------------------------------
# Glandes
# ------------------------------------------------------------

class Glande() :
    def __init__(self, valeur_envie, position):
        self.position = position
        self.valeur_pheromone = valeur_envie * 0.1
        self.rayon_senteur = valeur_envie * 5

    def emettre_pheromones(self, valeur_envie):
        self.valeur_envie = valeur_envie
        self.rayon_senteur = valeur_envie * 5


# ------------------------------------------------------------
# Aliment
# ------------------------------------------------------------
class Aliment:
    def __init__(self, position, valeur_nourriture):
        self.position = position
        self.valeur_nourriture = valeur_nourriture
        self.taille = valeur_nourriture * 0.1
        self.rayon_senteur = valeur_nourriture * 5