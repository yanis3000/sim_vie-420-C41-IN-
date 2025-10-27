# ------------------------------------------------------------
# SimVie_Vue.py  (avec affichage sélectif et pointes avant)
# ------------------------------------------------------------
import tkinter as tk
import math
import random
import statistics

class Vue:
    def __init__(self, controleur, modele):
        self.controleur = controleur
        self.modele = modele

        # --- Fenêtre principale ---
        self.root = tk.Tk()
        self.root.title("ÉcoSim - Vie Artificielle")

        # --- État de simulation ---
        self.en_pause = False
        self.vitesse = 1.0
        self.tick = 0
        self.afficher_odeurs = tk.BooleanVar(value=False)     # décoché par défaut
        self.afficher_champs = tk.BooleanVar(value=False)     # décoché par défaut

        self.largeur = 1000
        self.hauteur = 800

        # ========================================================
        # FRAME PRINCIPAL (GAUCHE = config, DROITE = monde)
        # ========================================================
        self.frame_principal = tk.Frame(self.root)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        # --------------------------------------------------------
        # 1️⃣ FRAME DE CONFIGURATION
        # --------------------------------------------------------
        self.frame_config = tk.Frame(
            self.frame_principal, width=200, bg="#dde7ec",
            padx=10, pady=10, relief=tk.GROOVE, borderwidth=2
        )
        self.frame_config.pack(side=tk.LEFT, fill=tk.Y)
        self.frame_config.pack_propagate(False)

        # --- Configuration de base ---
        tk.Label(self.frame_config, text="⚙️  Configuration", bg="#dde7ec", font=("Arial", 12, "bold")).pack(pady=5)

        tk.Label(self.frame_config, text="Seed aléatoire :", bg="#dde7ec").pack(anchor="w", pady=3)
        self.entree_seed = tk.Entry(self.frame_config, width=10, justify="center")
        self.entree_seed.pack(anchor="w")
        self.entree_seed.insert(0, "0")

        # ✅ Nouveaux champs configurables
        tk.Label(self.frame_config, text="Créatures :", bg="#dde7ec").pack(anchor="w", pady=(8, 0))
        self.entree_nb_creatures = tk.Entry(self.frame_config, width=10, justify="center")
        self.entree_nb_creatures.insert(0, "10")
        self.entree_nb_creatures.pack(anchor="w")

        tk.Label(self.frame_config, text="Aliments :", bg="#dde7ec").pack(anchor="w", pady=(5, 0))
        self.entree_nb_aliments = tk.Entry(self.frame_config, width=10, justify="center")
        self.entree_nb_aliments.insert(0, "10")
        self.entree_nb_aliments.pack(anchor="w")

        tk.Label(self.frame_config, text="Largeur :", bg="#dde7ec").pack(anchor="w", pady=(5, 0))
        self.entree_largeur = tk.Entry(self.frame_config, width=10, justify="center")
        self.entree_largeur.insert(0, "1000")
        self.entree_largeur.pack(anchor="w")

        tk.Label(self.frame_config, text="Hauteur :", bg="#dde7ec").pack(anchor="w", pady=(5, 0))
        self.entree_hauteur = tk.Entry(self.frame_config, width=10, justify="center")
        self.entree_hauteur.insert(0, "800")
        self.entree_hauteur.pack(anchor="w")

        # --- Bouton relancer ---
        self.bouton_seed = tk.Button(self.frame_config, text="Relancer simulation",
                                     command=self.reinitialiser_simulation)
        self.bouton_seed.pack(pady=8)

        self.label_info = tk.Label(self.frame_config, text="", bg="#dde7ec", fg="#333", wraplength=180)
        self.label_info.pack(anchor="w", pady=5)

        # --- Contrôles dynamiques ---
        tk.Label(self.frame_config, text="🕹️  Contrôles", bg="#dde7ec", font=("Arial", 11, "bold")).pack(pady=(20, 5))
        self.bouton_pause = tk.Button(self.frame_config, text="⏸️ Pause", command=self.basculer_pause)
        self.bouton_pause.pack(fill=tk.X, pady=3)

        frame_vitesse = tk.Frame(self.frame_config, bg="#dde7ec")
        frame_vitesse.pack(fill=tk.X, pady=5)
        tk.Label(frame_vitesse, text="Vitesse :", bg="#dde7ec").pack(side=tk.LEFT)
        tk.Button(frame_vitesse, text="×0.5", width=5, command=self.ralentir).pack(side=tk.LEFT, padx=2)
        tk.Button(frame_vitesse, text="×2", width=5, command=self.accelerer).pack(side=tk.LEFT, padx=2)

        # --- Options d’affichage ---
        tk.Label(self.frame_config, text="👁️  Affichage", bg="#dde7ec", font=("Arial", 11, "bold")).pack(pady=(20, 5))
        tk.Checkbutton(self.frame_config, text="Afficher odeurs", variable=self.afficher_odeurs,
                       bg="#dde7ec", command=self.maj_visibilite).pack(anchor="w")
        tk.Checkbutton(self.frame_config, text="Afficher champs sensoriels", variable=self.afficher_champs,
                       bg="#dde7ec", command=self.maj_visibilite).pack(anchor="w")

        # --- Statistiques dynamiques ---
        tk.Label(self.frame_config, text="📈 Statistiques", bg="#dde7ec", font=("Arial", 11, "bold")).pack(pady=(20, 5))
        self.label_tick = tk.Label(self.frame_config, text="Temps simulé : 0", bg="#dde7ec", anchor="w")
        self.label_tick.pack(fill=tk.X)
        self.label_pop = tk.Label(self.frame_config, text="Créatures : -", bg="#dde7ec", anchor="w")
        self.label_pop.pack(fill=tk.X)
        self.label_alim = tk.Label(self.frame_config, text="Aliments : -", bg="#dde7ec", anchor="w")
        self.label_alim.pack(fill=tk.X)
        self.label_energie = tk.Label(self.frame_config, text="Énergie moyenne : -", bg="#dde7ec", anchor="w")
        self.label_energie.pack(fill=tk.X)

        # --------------------------------------------------------
        # 2️⃣ FRAME MONDE (à droite)
        # --------------------------------------------------------
        frame_monde = tk.Frame(self.frame_principal)
        frame_monde.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canevas = tk.Canvas(frame_monde, width=self.largeur, height=self.hauteur,
                                 bg="#e8f4f8", highlightthickness=0)
        self.canevas.grid(row=0, column=0, sticky="nsew")

        self.scroll_x = tk.Scrollbar(frame_monde, orient=tk.HORIZONTAL, command=self.canevas.xview)
        self.scroll_y = tk.Scrollbar(frame_monde, orient=tk.VERTICAL, command=self.canevas.yview)
        self.scroll_x.grid(row=1, column=0, sticky="ew")
        self.scroll_y.grid(row=0, column=1, sticky="ns")

        frame_monde.rowconfigure(0, weight=1)
        frame_monde.columnconfigure(0, weight=1)
        self.canevas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        self.canevas.config(scrollregion=(0, 0, self.modele.largeur_terrain, self.modele.hauteur_terrain))



        # Premier affichage
        self.afficher_elements()


    # ========================================================
    # CONTRÔLES DE SIMULATION
    # ========================================================
    def basculer_pause(self):
        self.en_pause = not self.en_pause
        if self.en_pause:
            self.bouton_pause.config(text="▶️ Continuer")
        else:
            self.bouton_pause.config(text="⏸️ Pause")

    def ralentir(self):
        self.vitesse = max(0.25, self.vitesse / 2)
        self.label_info.config(text=f"Vitesse : ×{self.vitesse:.2f}")

    def accelerer(self):
        self.vitesse = min(4.0, self.vitesse * 2)
        self.label_info.config(text=f"Vitesse : ×{self.vitesse:.2f}")

    # ========================================================
    # REINITIALISATION
    # ========================================================
    def reinitialiser_simulation(self):
        params = {
            "seed": int(self.entree_seed.get()),
            "nb_creatures": int(self.entree_nb_creatures.get()),
            "nb_aliments": int(self.entree_nb_aliments.get()),
            "largeur": int(self.entree_largeur.get()),
            "hauteur": int(self.entree_hauteur.get())
        }
        self.controleur.reinitialiser_simulation(params)

    # ========================================================
    # AFFICHAGE INITIAL
    # ========================================================
    def afficher_elements(self):
        self.canevas.delete("all")
        # Dictionnaires graphiques
        self.id_creatures = {}
        self.id_pointes = {}
        self.id_aliments = {}
        self.id_olfaction = {}
        self.id_odeur = {}

        for aliment in self.modele.aliments:
            self.creer_aliment(aliment)
        for creature in self.modele.creatures:
            self.creer_creature(creature)
        self.maj_visibilite()

    def creer_aliment(self, aliment):
        x, y = aliment.position
        r = aliment.taille
        id_a = self.canevas.create_oval(x - r, y - r, x + r, y + r, fill="#5cd65c", outline="")
        self.id_aliments[aliment] = id_a

        # Cercles d’odeur
        self.id_odeur[aliment] = []
        niveaux = 3
        for i in range(niveaux):
            frac = (i + 1) / niveaux
            portee = aliment.rayon_senteur * frac
            dash_pattern = (2 * (i + 1), 4 * (i + 1))
            id_c = self.canevas.create_oval(
                x - portee, y - portee, x + portee, y + portee,
                outline="#99ccff", width=1, dash=dash_pattern
            )
            self.id_odeur[aliment].append(id_c)

    def creer_creature(self, creature):
        x, y = creature.position
        r = creature.taille
        couleur = self.couleur_energie(creature.energie)

        # Corps ovale orienté
        pts = self.forme_ovale(x, y, r, creature.orientation)
        id_c = self.canevas.create_polygon(pts, fill=couleur, outline="#333", smooth=True, splinesteps=10)

        # Pointe directionnelle
        angle = math.radians(creature.orientation)
        px = x + math.cos(angle) * r * 1.2
        py = y + math.sin(angle) * r * 1.2
        id_p = self.canevas.create_oval(px - 2, py - 2, px + 2, py + 2, fill="black", outline="")

        # Champ olfactif
        portee = creature.portee_olfactive
        id_o = self.canevas.create_oval(x - portee, y - portee, x + portee, y + portee,
                                        outline="#00cccc", width=1, dash=(4, 4))

        self.id_creatures[creature] = id_c
        self.id_pointes[creature] = id_p
        self.id_olfaction[creature] = id_o

    # ========================================================
    # RAFRAÎCHISSEMENT
    # ========================================================
    def rafraichir(self):
        if self.en_pause:
            return
        self.tick += 1

        for aliment in list(self.id_aliments.keys()):
            if aliment not in self.modele.aliments:
                for cid in self.id_odeur[aliment]:
                    self.canevas.delete(cid)
                self.canevas.delete(self.id_aliments[aliment])
                del self.id_aliments[aliment], self.id_odeur[aliment]

        for creature in self.modele.creatures:
            self.maj_creature(creature)

        self.mettre_a_jour_stats()

    def maj_creature(self, creature):
        x, y = creature.position
        r = creature.taille
        couleur = self.couleur_energie(creature.energie)

        pts = self.forme_ovale(x, y, r, creature.orientation)
        self.canevas.coords(self.id_creatures[creature], *pts)
        self.canevas.itemconfig(self.id_creatures[creature], fill=couleur)

        angle = math.radians(creature.orientation)
        px = x + math.cos(angle) * r * 1.2
        py = y + math.sin(angle) * r * 1.2
        self.canevas.coords(self.id_pointes[creature], px - 2, py - 2, px + 2, py + 2)

        portee = creature.portee_olfactive
        self.canevas.coords(self.id_olfaction[creature], x - portee, y - portee, x + portee, y + portee)

    # ========================================================
    # VISIBILITÉ DES CHAMPS
    # ========================================================
    def maj_visibilite(self):
        etat_odeur = 'normal' if self.afficher_odeurs.get() else 'hidden'
        for liste in self.id_odeur.values():
            for cid in liste:
                self.canevas.itemconfig(cid, state=etat_odeur)

        etat_champ = 'normal' if self.afficher_champs.get() else 'hidden'
        for cid in self.id_olfaction.values():
            self.canevas.itemconfig(cid, state=etat_champ)

    # ========================================================
    # STATS & OUTILS
    # ========================================================
    def forme_ovale(self, x, y, r, orientation):
        pts_base = [(r, 0), (-r * 0.6, r * 0.6), (-r, 0), (-r * 0.6, -r * 0.6)]
        angle = math.radians(orientation)
        pts = []
        for px, py in pts_base:
            xr = x + (px * math.cos(angle) - py * math.sin(angle))
            yr = y + (px * math.sin(angle) + py * math.cos(angle))
            pts.extend((xr, yr))
        return pts

    def mettre_a_jour_stats(self):
        nb_creatures = len(self.modele.creatures)
        nb_aliments = len(self.modele.aliments)
        energie_moy = statistics.mean([c.energie for c in self.modele.creatures]) if nb_creatures > 0 else 0
        self.label_tick.config(text=f"Temps simulé : {self.tick}")
        self.label_pop.config(text=f"Créatures : {nb_creatures}")
        self.label_alim.config(text=f"Aliments : {nb_aliments}")
        self.label_energie.config(text=f"Énergie moyenne : {energie_moy:.1f}")

    def couleur_energie(self, energie):
        e = max(0, min(energie, 100)) / 100
        r = 255
        g = int(180 * e)
        b = int(40 * (1 - e))
        return f'#{r:02x}{g:02x}{b:02x}'
