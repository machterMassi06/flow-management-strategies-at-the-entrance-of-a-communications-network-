#test.py
from structure import *
import random as rd 
import numpy as np

# ce programme comporte des tests demontrant les fonctionnalités de l'application(partie1)

if __name__=="__main__":
    # recuperer les parametres saisies 
    taux_transmission=int(input("Saisir le taux de transmission du Lien (paquets/sec): "))
    capacite_buff=int(input("Saisir la capacité de Buffer(Entier): "))
    
    #generer un processus poisson d'arrive de paquets depuis la source Si
    # lambda est le nbr de paquets envoyé en moyenne depuis les sources 
    
    lmbda=int(input("Saisir le Parametre lambda(moyenne d'arrivee de paquets/sec) :") )
    d_simulation=60 # durée de process en secondes ( 60 sec<-> 1 min)
    # taux d'arrive des paquets de sources vers le buffer gener avec poisson(lambda)
    arrivees=np.random.poisson(lmbda,d_simulation)
    #initialiser un buffer avec une capacité et le taux de transmission du lien saisie
    Buff=Buffer(capacite_buff,taux_transmission)
    
    #initialisation de n source emmettant des paquets selon le process poisson 
    n=int(input(" Nombre de sources :") )
    liste_sources=[Source(Buff) for _ in range(n) ]
    
    total_paquets_envoyes=0 # par tous les sources
    total_paquets_rejetes=0 # total paquets perdus
    
    # arr est le taux d'arrivee qui suit le process P(lambda) 
    for arr in arrivees :
        # pour chaque source : envoyer arr Paquets par seconde
        nb_paquets=int(arr/len(liste_sources))
        for s in liste_sources:
            s.envoie_paquets(nb_paquets)
            total_paquets_envoyes+=nb_paquets
            
        Buff.transmission() # transmission sur le lien

       
        
    print(" -----------------------Simulation pendant une Minute -----------------------------------------")
    print("total paquets envoie par les source :",total_paquets_envoyes)
    print("total paquets rejete :",Buff.nb_paquets_rejete)
