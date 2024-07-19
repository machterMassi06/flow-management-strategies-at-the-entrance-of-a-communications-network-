import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from strategies import *

# ce module comporte l'analyse des performance des 3 strategies de la partie 2
def analyse(liste_source,file_principale):
    ''' lance la simulation de systeme avec chque bi de source i et la file principale B '''
    #init 
    paquets_rejetes = []
    tps_moyen_att=[]
    
    # analyser  pendant 10 sec <-> 10 arrivee qui varient selon chaque poisson(li)
    d_simulation =10
    # liste des fonction ( strategies du module strategies.py)
    strategies=[choisirFileAvecPlusDePaquets,choisirChaqueFileTourDeRole,choisirFileAleatoirement]
    # choisir aleatoiremnt les lambda i de chaque source i 
    lmbda = [random.randint(6,8),random.randint(2,4),random.randint(1,2)]
    # simulé des arrivee qui varient selon le process poission de chaque lamba i 
    arrivees= [np.random.poisson(l, d_simulation) for l in lmbda]
    for s in strategies:
        
        total_envoyes=0
        for i in range(d_simulation):
            for j,source in enumerate(liste_source):
                nb_paquets=arrivees[j][i]
                source.envoie_paquets(nb_paquets)
                total_envoyes+=nb_paquets
                # transmission vers le buffer principale B selon la stratege
                if s==choisirChaqueFileTourDeRole:
                    s(source,file_principale)
                else:
                    s(liste_source,file_principale) 
            
            # definir le temps entre 2 arrivees
            time.sleep(0.04)
            
        # ajouter les taux de pertes et le tps moyenne d'attente de chaque strategie
        # total de paquets rejetes par les buffer de chaque source
        nb_paquets_rejete=sum(source.get_buffer().nb_paquets_rejete for source in liste_source)
        taux_pertes=(nb_paquets_rejete*100)/total_envoyes
        paquets_rejetes.append(taux_pertes)
        tps=sum(p.get_temps_attente() for p in file_principale if p!=None)/len(file_principale)
        tps_moyen_att.append(tps*10)# rendre en secondes
        
        # remise a zero des buffer bi et de la file principale B pour la prochaine strategie
        for source in liste_source:
            source.get_buffer().remise_zero()
        file_principale=[]
        
    return tps_moyen_att, paquets_rejetes

def performance(tps_moyen_att, paquets_rejetes):
    ''' trace les barres selon le tps_moyen_att et les taux de paquets_rejetes'''
    strategies = ["Max paquets", "Tour de rôle", "Aléatoire"]

    # Creation des données pour les barres
    x = np.arange(len(strategies))
    bar_width = 0.35

    # Creation du graphique à barres pour le taux de pertes
    fig, ax1 = plt.subplots()
    ax1.bar(x, paquets_rejetes, bar_width,label=' ')
    ax1.set_ylabel('Taux de pertes (%)', color="blue")
    ax1.set_ylim(0, 60 * 1.2)
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    

    # Creation d'un axe partagé pour le temps moyen d'attente
    ax2 = ax1.twinx()
    ax2.bar(x+bar_width , tps_moyen_att, bar_width,label='', color='tab:red', edgecolor='none')  # Ajout de edgecolor='none'
    ax2.set_ylabel('Temps moyen d\'attente (s)', color="red")
    ax2.set_ylim(0, 2 * 1.1)
    ax2.tick_params(axis='y', labelcolor='tab:red')
    
    # Ajout des étiquettes, titre et legendes
    plt.xlabel('Stratégies')
    plt.title('Performance des stratégies')
    plt.xticks(x + bar_width / 2, strategies)
    
    # Affichage du graphique
    plt.tight_layout()
    # Creer une fenetre tkinter pour afficher le graphique
    fenetre = tk.Tk()
    fenetre.title("Performance des stratégies")

    # Intégrer la figure Matplotlib dans tkinter
    canvas = FigureCanvasTkAgg(fig, master=fenetre)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


    # Lancer la boucle principale tkinter
    fenetre.mainloop()

    