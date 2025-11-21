from abc import ABC

# ------------------------------------------------------------
# SimVie_Neurone.py
# ------------------------------------------------------------
import random

class Neurone():
    """Unité de base : reçoit plusieurs entrées (dendrites) et transmet un signal
       à plusieurs autres neurones (axones)."""
    def __init__(self, seuil=1.0):
        self.refractaire = 0  # temps restant avant de pouvoir tirer à nouveau
        self.delai_refractaire = 3  # durée fixe (en cycles)
        self.seuil = seuil # stimulation nécessaire pour que le neurone s'active
        self.entrees = []       # [(neurone_source, poids)]
        self.sorties = []       # [(neurone_cible, poids)]
        self.potentiel = 0.0  #accumuler les signaux entrants avant de décider de "décharger" ou non
        self.actif = False

    def connecter_a(self, cible, poids):
        self.sorties.append((cible, poids))
        cible.entrees.append((self, poids))

    def recevoir(self, signal):
        self.potentiel += signal

    def evaluer(self):
        """Évalue l’état du neurone en fonction des entrées et du seuil."""

        # Si le neurone est encore dans sa phase de repos, il ne peut pas s’activer
        if self.refractaire > 0:
            self.refractaire -= 1
            self.actif = False
            return

        # Calcul du potentiel reçu à partir des neurones d’entrée
        somme = 0
        for src, poids in self.entrees:
            somme += src.actif * poids
        self.potentiel = somme

        # Si le potentiel dépasse le seuil → activation
        if self.potentiel >= self.seuil:
            self.actif = True
            self.refractaire = self.delai_refractaire  # entre en période de repos
        else:
            self.actif = False


class SystemeNerveux:
    """Réseau neuronal hiérarchique :
       capteurs -> ganglions sensoriels -> interneurones -> ganglions moteurs -> moteurs"""
    def __init__(self, ganglion, nb_ganglions=4, nb_inter=10, nb_moteurs=4):

        self.ganglions = ganglion

        self.interneurones = []
        for i in range(nb_inter):
            neurone = Neurone(seuil=1.2)
            self.interneurones.append(neurone)

        self.ganglions_moteurs = []
        for i in range(nb_ganglions):
            neurone = Neurone(seuil=1.0)
            self.ganglions_moteurs.append(neurone)

        self.moteurs = []
        for i in range(nb_moteurs):
            neurone = Neurone(seuil=0.8)
            self.moteurs.append(neurone)

        for g in self.ganglions.neurone:
            for i in random.sample(self.interneurones, k=3):
                g.connecter_a(i, random.uniform(0.5, 1.0))
        for i in self.interneurones:
            for gm in random.sample(self.ganglions_moteurs, k=2):
                i.connecter_a(gm, random.uniform(0.4, 1.0))
        for gm in self.ganglions_moteurs:
            for m in random.sample(self.moteurs, k=2):
                gm.connecter_a(m, random.uniform(0.5, 1.0))

    # --- Simulation d'un cycle d'activité ---
    def cycle(self, capteurs, vomeronasal, stimulations):
        """stimulations : liste de valeurs entre 0 et 1 pour chaque capteur"""
        # Activer les capteurs
        for neurone, valeur in zip(capteurs, stimulations["aliments"]):
            neurone.actif = random.random() < valeur
        
        for neurone, valeur in zip(vomeronasal, stimulations["phéromones"]):
            neurone.actif = random.random() < valeur

        # Propagation à travers le réseau
        for couche in [self.ganglions.neurone,
                       self.interneurones,
                       self.ganglions_moteurs,
                       self.moteurs]:
            for n in couche:
                n.evaluer()

        # Retourne le taux d’activation motrice global (0-1)
        actifs = sum(1 for m in self.moteurs if m.actif)
        return actifs / len(self.moteurs)
