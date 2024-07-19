import tkinter as tk
from structure import *
import numpy as np
import time
import math
import random

# ce module comporte le visual de la dynamicité de reseau  de la partie 1
# simulation faite a l'aide de deux sources ,et un buffer
# les parametre ( lambda,capacité buffer,taux_transmission de lien ) sont a saisir par l'utilisateur

class Interface:
    ''' Cette classe modèle une interface graphique  pour visualiser la dynamicité de la partie 1'''

    def __init__(self):
        # Fenêtre principale ou l'utilisateur peut entrez ses parametre
        self.fenetre_principale = tk.Tk()
        self.fenetre_principale.title("Configuration du système")

        # Création des champs de saisie pour les paramètres
        lbl_taux_trans = tk.Label(self.fenetre_principale, text="Taux de transmission (paquets/sec):")
        lbl_taux_trans.grid(row=2, column=0, sticky="w")
        self.entry_taux_trans = tk.Entry(self.fenetre_principale)
        self.entry_taux_trans.grid(row=2, column=1)

        lbl_capacite_buff = tk.Label(self.fenetre_principale, text="Capacité du Buffer (Entier):")
        lbl_capacite_buff.grid(row=1, column=0, sticky="w")
        self.entry_capacite_buff = tk.Entry(self.fenetre_principale)
        self.entry_capacite_buff.grid(row=1, column=1)

        lbl_lambda = tk.Label(self.fenetre_principale, text="Paramètre lambda (moyenne d'arrivée de paquets/sec):")
        lbl_lambda.grid(row=0, column=0, sticky="w")
        self.entry_lambda = tk.Entry(self.fenetre_principale)
        self.entry_lambda.grid(row=0, column=1)

        # Bouton pour démarrer la simulation
        # cliquer sur ce btn lancer la simulation (self.demarrer_simulation)
        btn_demarrer = tk.Button(self.fenetre_principale, text="Démarrer", command=self.demarrer_simulation)
        btn_demarrer.grid(row=4, columnspan=2)
        
        self.fenetre_principale.mainloop()

    def demarrer_simulation(self):
        ''' Methode qui recupere les parametre saisies par l'utilisateur et lance la simulation de reseau
            avec les parametres saisies 
        '''
        
        # Récupérer les valeurs saisies par l'utilisateur
        taux_transmission = int(self.entry_taux_trans.get())
        capacite_buff = int(self.entry_capacite_buff.get())
        lmbda = int(self.entry_lambda.get())
        # detruire la fenetre de saisie de parametre 
        self.fenetre_principale.destroy()
        
        # Créer un buffer avec les paramètres saisis
        self.__buffer = Buffer(capacite_buff, taux_transmission)
        
        # simulation faite avec 2 source juste pour visualiser la dynamicité de reseau 
        # Créer une liste de sources (2 sources) avec les paramètres saisis
        self.__liste_sources = [Source(self.__buffer) for _ in range(2)]
 
        # lancer la simulation de reseau avec les paramètres saisis
        try:
            self.lancer_simulation(lmbda, taux_transmission)
        except tk.TclError:
            pass
        
        
    def lancer_simulation(self, parametreL, taux_trans):
        ''' Methode qui cree la fentre principale et affiche les sources , buffer , les liens , et lance la dynamicité de
            reseau , cad l'arrivée des paquets dans le buffer, retrait du buffer et leur transmission'''
        # Créer et afficher la fenêtre de simulation et le canvas de simulation
        self.fenetre_simulation = tk.Tk()
        self.fenetre_simulation.title("Simulation du système")
        self.canvas_simulation = tk.Canvas(self.fenetre_simulation, width=1000, height=500, bg="white")
        self.canvas_simulation.pack()

        # Affichage de la capacité du buffer ET le parametre lambda
        lbl_capacite = tk.Label(self.fenetre_simulation, text=f"Capacité du buffer: {self.__buffer.get_capacite()}")
        lbl_capacite.pack()
        lbl_lambda = tk.Label(self.fenetre_simulation, text=f"Parametre Lambda: {parametreL}")
        lbl_lambda.pack()
        
        # Creation des labels pour les statistiques a tps reel
        self.label_paquets_envoyes = tk.Label(self.canvas_simulation, text="Total Paquets envoyés par les sources : 0")
        self.label_paquets_envoyes.place(x=10, y=10)
        
        self.label_paquets_rejetes = tk.Label(self.canvas_simulation, text="Total Paquets rejetés : 0")
        self.label_paquets_rejetes.place(x=10, y=30)

        self.label_paquets_transmis = tk.Label(self.canvas_simulation, text="Total Paquets transmis au destainataires : 0")
        self.label_paquets_transmis.place(x=10, y=50)
        
        # labels pour les taux d'arrivee et le taux de transmission
        self.label_taux_arrivee=tk.Label(self.canvas_simulation, text=f"Taux d'arrivée R=  paquets/sec")
        self.label_taux_arrivee.place(x=100, y=200)
        
        self.label_taux_transmission=tk.Label(self.canvas_simulation, text=f"Taux de transmission du Lien R={taux_trans}  paquets/sec")
        self.label_taux_transmission.place(x=630, y=200)
       
        # Afficher les sources, le buffer et les liens
        self.afficher_sources()
        self.afficher_buffer()
        self.afficher_lien_arrivee()
        self.afficher_lien_transmission()

        # Démarrer la simulation dynamique
        self.dynamicite(parametreL)

        self.fenetre_simulation.mainloop()

    def generer_process_poisson(self, lmbda):
        ''' Génère la liste des taux d'arrivée selon le processus de Poisson de paramètre lambda durant une heure'''
        # Liste de simulation de processus pendant une heure (3600 sec),varient selon lambda
        arrivees = np.random.poisson(lmbda, 3600)
        return arrivees

    def dynamicite(self,lmbda):
        ''' Methode qui nous permet de voir la dynamicté de system ,
        mis a jour notre affichage de systeme , selon les arrivees des paquets et leurs transmission '''
        
        # pour les stats 
        paquets_envoyes=0
        paquets_rejetes=0
        paquets_transmis=0
        
        # recuperer les taux d'arrivee generer par le processus poisson de parametre lambda
        arrivees = self.generer_process_poisson(lmbda)
        
        
        for arr in arrivees:
            # boolean que pour s'assurer de faire taux_trans de paquet par seconde
            t=True 
            # les sources envoies nb_paquet de chaque arrivee
            nbpaquet=int(arr/len(self.__liste_sources))
            #affiche le taux d'arrivee pour les 2 sources
            self.afficher_taux_arrivee(nbpaquet*2)
            #affiche les paquets envoyes par les sources
            self.afficher_paquets_envoyes(nbpaquet*2)
            
            for s in self.__liste_sources:
                # envoie de nbpaquet
                s.envoie_paquets(nbpaquet)
                paquets_envoyes+=nbpaquet
                # afficher les paquets envoyes et rejete dans le canvas
                paquets_rejetes=self.__buffer.nb_paquets_rejete
                self.maj_stats(paquets_envoyes, paquets_rejetes, paquets_transmis)
                
                if t :# transmettre taux_trans /sec
                    # transmission vers les destinataires
                    nbpaquet=self.__buffer.transmission()
                    self.afficher_paquets_transmis(nbpaquet)
                    paquets_transmis+=nbpaquet
                    # mettre a jour les stats apres transmission
                    self.maj_stats(paquets_envoyes, paquets_rejetes, paquets_transmis)
                    t=False # transmission jusqu'a la prochaine seconde
                    
            # definir le delai entre deux arrive
            u=random.random()# genere un nombre entre 0 et 1
            delai_avant_autre_arrivee=(-1/lmbda)*math.log(u)
            # delai avant l'autre arrivee ( *1.2 juste pour que sa soit visuelle ) 
            time.sleep(delai_avant_autre_arrivee*1.2)
              
    def maj_stats(self, paquets_envoyes, paquets_rejetes, paquets_transmis):
        ''' mis a jour les labels des statistiques a temps reel '''
        # Mettre à jour les labels avec les nouvelles valeurs
        self.label_paquets_envoyes.config(text=f"Total Paquets envoyés par les sources : {paquets_envoyes}")
        self.label_paquets_rejetes.config(text=f"Total Paquets rejetés : {paquets_rejetes}")
        self.label_paquets_transmis.config(text=f"Total Paquets transmis au destinataires : {paquets_transmis}")
        
    def afficher_paquets_envoyes(self, nb_paquets):
        ''' cree un carree rouge pour chaque paquet envoyes par les sources et deplace ses paquets vers le buffer'''
        # deplacer nb_paquet envoyes par les sources vers le buffer
        for _ in range(nb_paquets):
            paquet = self.canvas_simulation.create_rectangle(110, 300, 130, 320, fill="red", outline="black", width=1)
            self.deplacer_paquet(paquet, 110, 280)# deplacer ce paquet
            # mise a jour de buffer apres envoie de paquet 
            self.mise_a_jour_buffer()
    
    def afficher_paquets_transmis(self,n):
        ''' afficher les paquets (n) transmis au destinataire '''
        # deplace les paquets transmis de buffer vers les distinataire sur le lien 
        for _ in range(n):
            paquet = self.canvas_simulation.create_rectangle(800, 300, 820, 320, fill="red", outline="black", width=1)
            self.deplacer_paquet(paquet, 800, 1000)# deplacer ce paquet
            # mise a jour du buffer apres transmission du paquet 
            self.mise_a_jour_buffer()
            
    def deplacer_paquet(self, p, xst, xend):
        ''' deplace le paquet p de xst jusqu'a xend et cela pendant 8 pas de deplacement '''
        steps = 8 # le nb de pas de paquet (nb_de_deplacement)
        # definir les coords de deplacemennts 
        dx = (xend - xst) / steps 
        dy = 0
        
        for step in range(steps):
            # deplacer le paquet sur le canvas
            self.canvas_simulation.move(p, dx, dy)
            self.canvas_simulation.update()
            # simule une vitesse de deplacement de paquet juste pour qu'il soit visuel
            self.canvas_simulation.after(50)
        
        self.canvas_simulation.delete(p)

        
    def mise_a_jour_buffer(self):
        ''' mis a jour le buffer selon son taux d'occupation '''
        # Coordonnées pour le remplissage du buffer
        # Coords : La partie non remplie du buffer
        x2 = 300 + int(500 * self.__buffer.pourcentage_non_occupe())  

        # Colorer la partie remplie du buffer en rouge et le reste en vert
        self.canvas_simulation.create_rectangle(x2, 300, 800, 350, fill="red", outline="black")
        self.canvas_simulation.create_rectangle(300, 300, x2, 350, fill="green", outline="black")
        
    def afficher_taux_arrivee(self, arr):
        ''' affiche le taux d'arrivée au-dessus depuis les sources '''
        # Afficher le taux d'arrivée des sources 
        self.label_taux_arrivee.config(text=f"Taux d'arrivée R= {arr} paquets/sec")
        
    def afficher_sources(self):
        ''' affiche les sources des paquets '''
        # Afficher les sources à gauche du canvas (fentre)
        x_source = 50
        y_source = 240
        for i, source in enumerate(self.__liste_sources):
            self.canvas_simulation.create_rectangle(x_source, y_source, x_source + 50, y_source + 50, fill="plum")
            self.canvas_simulation.create_text(x_source + 25, y_source + 25, text=f"Source {i+1}")
            y_source += 120

    def afficher_buffer(self):
        ''' affiche le buffer (la file d'attente )'''
        # Afficher le buffer au milieu du canvas (fenetre)
        self.buffer_rectangle=self.canvas_simulation.create_rectangle(300, 300, 800, 350, fill="green", outline="black", width=2)
        self.canvas_simulation.create_text(700, 325, text="Buffer")

    def afficher_lien_arrivee(self):
        ''' affiche le lien sur lequels il arrivent les paquets vers le buffer '''
        self.canvas_simulation.create_line(110, 325, 300, 325, arrow=tk.LAST)
        self.canvas_simulation.create_text(200, 335, text="Arrivée des paquets", anchor=tk.CENTER)

    def afficher_lien_transmission(self):
        ''' affiche le lien qui transmis les paquets du buffer vers leurs distination '''
        self.canvas_simulation.create_line(810, 325, 1000, 325, arrow=tk.LAST)
        self.canvas_simulation.create_text(900, 335, text="Transmission des paquets", anchor=tk.CENTER)



