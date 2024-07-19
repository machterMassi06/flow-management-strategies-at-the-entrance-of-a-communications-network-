import random
import time
# ici dans la partie 2 on considere que chaque source i possede un buffer bi 

# file principale est la file d'attente principale de systeme B(voir la figure)

def choisirFileAvecPlusDePaquets(liste_source,file_principale):
    ''' La file d’attente(bi) choisie est celle contenant le plus grand nombre de paquets.
        on suppose que la liste liste_source est une liste de source
    
        return l'indice de la source qui a ete choisi 
    '''
    # recuperer la source avec le buffer bi qui contient le plus de paquets dans smax
    smax=liste_source[0]
    for s in liste_source :
        if s.get_buffer().get_len_fifo()>smax.get_buffer().get_len_fifo():
            smax=s
            
    # recuperer le buffer de la source smax
    Bi=smax.get_buffer()
    # retrait d'un paquets dans le buffer Bi de la source Simax
    
    paquet=Bi.retrait()
    if paquet :
        # definir le temps d'attente de paquet 
        paquet.set_temps_attente(time.time())
        # l'ajout de paquet dans la file principale B
        file_principale.append(paquet)
    
    return liste_source.index(smax)
    
def choisirChaqueFileTourDeRole(source,file_principale):
    ''' Un paquet est pris de chaque file d’attente, à tour de rôle.
        source est la source qui detient le role a l'instant 
    '''
    
    # buffer bi de la source "source" qui a son role  
    Bi=source.get_buffer()
    # retrait d'un paquet dans bi
    paquet=Bi.retrait()
    if paquet!=None:
        # definir le temps d'attente de paquet 
        paquet.set_temps_attente(time.time())
        # envoie de paquet vers la file principale bi 
        file_principale.append(paquet)


def choisirFileAleatoirement(liste_source,file_principale):
    ''' La file d’attente est choisie de manière aléatoire
    cette strategie elle consiste à traiter tous les paquets de la file tiré aleat
    
    return l'indice de la source qui a ete choisi'''
    
    # tiré aleatoirement une source  
    x=random.randint(0,len(liste_source)-1)
    source=liste_source[x]
    
    # buffer bi de la source tiré aleatoirement 
    Bi=source.get_buffer()
    paquet=Bi.retrait()
    if paquet :
        # definir le temps d'attente de paquet
        paquet.set_temps_attente(time.time())
        # l'ajout de paquet dans la file principale B
        file_principale.append(paquet)
        
    return liste_source.index(source)
