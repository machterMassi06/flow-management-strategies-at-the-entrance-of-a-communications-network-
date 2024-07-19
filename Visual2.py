# module visual2.py
import tkinter as tk
from structure import *
import numpy as np
import time
import math
import random
import strategies

# ce module comporte le visual de la dynamicité de reseau avec strategies de la partie 2
# simulation faite a l'aide de deux sources , un buffer bi pour chaque source i et une file principale B 
class Interface:
    ''' Cette classe modèlise une interface graphique pour visualiser la dynamicité de la partie 2 '''

    def __init__(self):
        # Fenêtre de choix
        self.fenetre_choix = tk.Toplevel()
        self.fenetre_choix.title("stratégie: ")
        # init strategie a defaut a la strategie max_paquets 
        self.var_strategie = tk.StringVar()
        self.var_strategie.set("max_paquets")
        # Bouton radio pour la stratégie "Max paquets"
        max_paquets_radio = tk.Radiobutton(self.fenetre_choix, text="   Max paquets  ", variable=self.var_strategie, value="max_paquets")
        max_paquets_radio.grid(row=1, column=2, sticky="w")

        # Bouton radio pour la stratégie "Tour de rôle"
        tour_de_role_radio = tk.Radiobutton(self.fenetre_choix, text="  Tour de rôle  ", variable=self.var_strategie, value="tour_de_role")
        tour_de_role_radio.grid(row=2, column=2, sticky="w")

        # Bouton radio pour la stratégie "Aléatoire"
        aleatoire_radio = tk.Radiobutton(self.fenetre_choix, text="  Aléatoire  ", variable=self.var_strategie, value="aleatoire")
        aleatoire_radio.grid(row=3, column=2, sticky="w")

        # Bouton pour lancer le traitement
        btn_traitement = tk.Button(self.fenetre_choix, text="Lancer le traitement", command=self.lancer_simulation)
        btn_traitement.grid(row=4, column=2, columnspan=2)
        self.buffers_rectangle=[]

        self.fenetre_choix.mainloop()
    
    def lancer_simulation(self):
        # Récupérer la stratégie sélectionnée
        strategie = self.var_strategie.get()
        # Definir la file principale B (fifo)
        self.file_principale=[]
        # simulation faite avec 2 sources
        # Créer des buffer pour chaque source avec une capacite 4 et 8
        buffers = [Buffer(random.randint(4,8)) for _ in range(2)]
        # Créer une liste de sources (2 sources) avec leurs buffer
        self.liste_sources = [Source(buffers[i]) for i in range(2)]
        
        # generer des lambda(taux d'arrive nbpaquet/sec) pour chaque source
        lmbdas=[random.randint(2,4) for _ in range(2)]
        
        # Créer et afficher la fenêtre de simulation avec les paramètres saisis
        self.fenetre_simulation = tk.Toplevel(self.fenetre_choix)
        self.fenetre_simulation.title("Simulation du système")
        # creer le canvas de simulation
        self.canvas_simulation = tk.Canvas(self.fenetre_simulation, width=1000, height=500, bg="white")
        self.canvas_simulation.pack()
        # Création des labels pour les statistiques a tps reel
        self.label_strategie_choisi=tk.Label(self.canvas_simulation, text=f"Strategie : {strategie}")
        self.label_strategie_choisi.place(x=300,y=10)
        self.label_paquets_envoyes = tk.Label(self.canvas_simulation, text="Total Paquets envoyés par les sources : 0")
        self.label_paquets_envoyes.place(x=10, y=30)

        self.label_paquets_rejetes = tk.Label(self.canvas_simulation, text="Total Paquets rejetés : 0")
        self.label_paquets_rejetes.place(x=10, y=50)
        # definir les taux d'arrivee des sources
        self.label_taux_arrivees=[]
        dy=200
        for _ in range(len(self.liste_sources)):
            t=tk.Label(self.canvas_simulation, text=f"Taux d'arrivée R=  paquets/sec")
            t.place(x=100, y=dy)
            self.label_taux_arrivees.append(t)
            dy+=110
            
        # Afficher les sources, leur buffer 
        self.afficher_sources()
        self.afficher_buffers_sources()
        self.afficher_liens_arrivees()
        self.afficher_file_principale()
        self.afficher_liens_transmissions()
        
        # lancer la simulation de reseau 
        try:
            self.dynamicite(strategie,lmbdas)
        except tk.TclError:
            pass
    
    def dynamicite(self,strategie,lambdas):
        # pour les stats 
        paquets_envoyes=0
        paquets_rejetes=0
        # recuperer les taux d'arrivee generer par le processus poisson de parametre lambda i
        arrivees = self.generer_process_poisson(lambdas)
        # les sources envoies arr de chaque arrivee
        for i in range(len(arrivees[0])):
            ## taux d'arrivee pour les 2 sources
            for j,s in enumerate(self.liste_sources):
                nbpaquet=arrivees[j][i]
                s.envoie_paquets(nbpaquet)
                paquets_envoyes+=nbpaquet
                # mise a jour d'affichage
                self.afficher_taux_arrivees(j,nbpaquet)
                self.maj_stats(paquets_envoyes, paquets_rejetes)
                # prendre des paquets selon la strategie
                if strategie =="tour_de_role":
                    # passer la source qui a son role a la strategie 
                    self.strategie(strategie,source=s)
                else:
                    self.strategie(strategie)
                
            # mettre a jour les stats 
            paquets_rejetes=sum(s.get_buffer().nb_paquets_rejete for s in self.liste_sources)
            self.maj_stats(paquets_envoyes, paquets_rejetes)
        
        # definir le delai entre deux arrive
        u=random.random()# genere un nombre entre 0 et 1
        delai_avant_autre_arrivee=(-1/lambdas[0])*math.log(u)
        # delai avant l'autre arrivee ( *10 juste pour que sa soit visuelle ) 
        time.sleep(delai_avant_autre_arrivee*10)
    
    def strategie(self,s,source=None):
        ''' lance la strategies selon la strategie choisie s de traitement de paquet '''
        if s=="max_paquets":
            # bi est le buffer de la source choisi dans cette strategie a cet instant
            bi=strategies.choisirFileAvecPlusDePaquets(self.liste_sources,self.file_principale)
            self.transmission_paquet_depuis(bi)
        elif s=="tour_de_role":
             # bi est le buffer de la source choisi dans cette strategie a cet instant
            strategies.choisirChaqueFileTourDeRole(source,self.file_principale)
            bi=self.liste_sources.index(source)
            self.transmission_paquet_depuis(bi)
        else:
            # bi est le buffer de la source choisi dans cette strategie a cet instant
            bi=strategies.choisirFileAleatoirement(self.liste_sources,self.file_principale)
            self.transmission_paquet_depuis(bi)
            
    def generer_process_poisson(self,lambdas):
        ''' Génère la liste des taux d'arrivée de chauque source selon le processus de Poisson de paramètre lambdas:liste des lambda
        de different source ,durant une heure'''
        return [np.random.poisson(l,3600) for l in lambdas]
    
    def maj_stats(self, paquets_envoyes, paquets_rejetes):
        ''' mis a jour les stats a temps reel '''
        # Mettre à jour les labels avec les nouvelles valeurs
        self.label_paquets_envoyes.config(text=f"Total Paquets envoyés par les sources : {paquets_envoyes}")
        self.label_paquets_rejetes.config(text=f"Total Paquets rejetés : {paquets_rejetes}")
    
    def afficher_sources(self):
        ''' affiche les sources des paquets '''
        # Afficher les sources à gauche du canvas (fenetre)
        x_source = 50
        y_source = 230
        for i, source in enumerate(self.liste_sources):
            self.canvas_simulation.create_rectangle(x_source, y_source, x_source + 50, y_source + 50, fill="plum")
            self.canvas_simulation.create_text(x_source + 25, y_source + 25, text=f"Source {i+1}")
            y_source += 110
    def afficher_buffers_sources(self):
        ''' affiche les buffer (la file d'attente ) de chaque source'''
        y=240
        for i in range(len(self.liste_sources)):
            self.buffers_rectangle.append(self.canvas_simulation.create_rectangle(200, y, 350, y+40, fill="green", outline="black", width=2))
            self.canvas_simulation.create_text(270, y+20, text=f" B{i} ,capacité={self.liste_sources[i].get_buffer().get_capacite()}")
            y+=110
            
    def afficher_taux_arrivees(self,i, arr):
        ''' affiche le taux d'arrivée de la source i  '''
        # Afficher le taux d'arrivée arr de la source i
        time.sleep(0.3)
        self.label_taux_arrivees[i].config(text=f"Taux d'arrivée R= {arr} paquets/sec")
        
    def afficher_liens_arrivees(self):
        ''' affiche le liens sur lequels il arrivent les paquets de leurs sources vers leur buffer '''
        y=260
        for _ in range(len(self.liste_sources)):
            self.canvas_simulation.create_line(100, y, 200, y, arrow=tk.LAST,fill="red")
            y+=110

    def afficher_file_principale(self):
        ''' affiche la file d'attente principale '''
        # Afficher le buffer au milieu de la fenêtre
        self.canvas_simulation.create_rectangle(600, 240, 900, 390, fill="blue", outline="black", width=2)
        self.canvas_simulation.create_text(750, 325, text="File d'attente principale")

    def afficher_liens_transmissions(self):
        ''' affiche les liens entre les buffer bi et la file principale B '''
        y=280
        for _ in range(len(self.liste_sources)):
            self.canvas_simulation.create_line(350, y, 600, y, arrow=tk.LAST)
            y+=110
            
    def transmission_paquet_depuis(self,bi):
        ''' transmis le paquet du buffer Bi vers la file principale B
            bi est l'indice de buffer bi (0,1,..)
        '''
        # trouver la coord y selon le buffer bi
        y=260+bi*110
        # creation d'un paquet = juste un rectangle rouge, puis deplacement de ce paquet vers la file principale B
        
        paquet = self.canvas_simulation.create_rectangle(350, y, 370, y+20, fill="red", outline="black", width=1)
        self.deplacer_paquet(paquet, 350, 600)# deplacer ce paquet


    def deplacer_paquet(self, p, xst, xend):
        ''' deplace le paquet p de xst jusqu'a xend et cela pendant 10 pas de deplacement '''
        steps = 10 # le pas de paquet (nb_de_deplacement)
        dx = (xend - xst) / steps
        dy = 0
        for step in range(steps):
            # deplacer le paquet sur le canvas
            self.canvas_simulation.move(p, dx, dy)
            self.canvas_simulation.update()
            # simule une vitesse de deplacement de paquet juste pour qu'il soit visuel
            self.canvas_simulation.after(80)
        
        self.canvas_simulation.delete(p)
        


