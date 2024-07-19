import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np


def analyse(buff, liste_source):
    '''lance la simulation de systeme en interne , cad les arrivees des paquet des sources vers le buffer
        selon le process poisson(lambda) , et fait les calcule pour chaque lambda le taux de pertes de paquets '''
    # faire varier le lambda entre 1 et 30 
    lmbda = [l for l in range(1, 30)]
    paquets_rejetes = []
    # analyser pour chaque parametre lambda pendant 10 sec <-> 10 arrivee
    d_simulation = 10
    
    for l in lmbda:
        # liste des 10  arrivees qui varient selon poisson de parametre l
        arrivees = np.random.poisson(l, d_simulation)
        total_envoyes=0
        for arr in arrivees:
            nb_paquets = int(arr / len(liste_source))
            # chaque source envoie nb paquets 
            for s in liste_source:
                s.envoie_paquets(nb_paquets)
                total_envoyes+=nb_paquets
            buff.transmission()# transmission sur le lien 
        
        # ajout de taux de pertes
        taux_pertes=(buff.nb_paquets_rejete*100)/total_envoyes
        paquets_rejetes.append(taux_pertes)
        # remise a zero du buffer pour simulé avec le prochain lambda
        buff.remise_zero()
    
    return lmbda, paquets_rejetes

def performance(lambdas, paquets_rejetes):
    ''' Methode qui permet de dessiner le graphhisme avec matplot de taux de pertes de paquets en fct
        des lamba qui varient '''
    
    # Creer une application tkinter
    fenetre = tk.Tk()
    fenetre.title("Avec un buffer de capacité=15 et un taux_transmission du lien =3 p/sec")
    
    # Creer une figure Matplotlib
    figure, ax = plt.subplots()
    ax.plot(lambdas, paquets_rejetes, label="Paquets perdus")
    
    # Ajout des titres et des legendes
    ax.set_title("Performances du réseau simulé pendant 10 arrivées en fonction de λ")
    ax.set_xlabel("λ")
    ax.set_ylabel("taux de perte des paquets en %")
    ax.legend()
    
    # Integrer la figure Matplotlib dans tkinter
    canvas = FigureCanvasTkAgg(figure, master=fenetre)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
    # Ajouter un bouton pour quitter l'application
    button_quit = tk.Button(fenetre, text="Quitter", command=fenetre.quit)
    button_quit.pack(side=tk.BOTTOM)
    
    # Lancer la boucle principale tkinter
    fenetre.mainloop()

