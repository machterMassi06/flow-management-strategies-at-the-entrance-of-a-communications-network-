# structure.py

# dans ce module on defini nos classes (buffer,source,paquet)

import time # juste pour definir le temps d'envoie du paquet 

class Buffer(object):
    ''' dans cette class tout objet est un Buffer.
     Représente la file d'attente où les paquets sont stockés ou rejete avant d'être transmis. '''
    
    # calcluler le nombre de paquets rejetes dans ce buffer
    nb_paquets_rejete=0
    
    def __init__(self,capacite,taux_trans=0):
        self.__capacite=capacite
        self.__taux_transmission=taux_trans
        self.__fifo=[] # la file init a vide 
    
    def est_plein(self):
        ''' Retourne True si le buffer est plein , false sinon '''
        # si la capacité est depassé donc plein
        return len(self.__fifo)>=self.__capacite
    
    def est_vide(self):
        ''' retourne True si le buffer est vide '''
        return self.__fifo==[]
    
    def pourcentage_non_occupe(self):
        ''' retourne le porcentage de la partie non occupée du buffer (nbr entre 0 et 1)'''
        return ((self.__capacite-len(self.__fifo))/self.__capacite)
    
    def __iadd__(self,paquet):
        ''' methode self+=paquet jumelée permattent l'ajout et l'arrivée d'un paquet dans le buffer tant que possible,
        cad tant que le buffer n'est pas plein , sinon le paquet est rejeté '''
        
        # l'ajout de paquet dans le buffer tant que il n'est pas plein 
        if not self.est_plein():
            self.__fifo.append(paquet)
        else:
            # sinon le paquet est rejeté
            self.nb_paquets_rejete+=1
  
        return self
    
    def retrait(self):
        ''' Methode qui fait le retrait d'un paquet dans le buffer pour
        le transmettre au destinataires avec le lien '''
        
        # return le paquet le plus ancien dans la file
        return self.__fifo.pop(0) if not self.est_vide() else None
    

        
    def transmission(self):
        ''' Methode permattent de transmettre sur le lien a la fois le min entre ('self.taux_transmission:Int'
        et la longeur de la file fifo ) de Paquets/sec
        Methode qui retourne le nbr de paquets transmis
        '''
         
        nbpaquet=min(self.__taux_transmission,len(self.__fifo))
        # transsmission de nbpaquet sur le lien
        # revient a realiser nbpaquet retrait()
        for _ in range(nbpaquet):
            self.retrait()
        return nbpaquet
    
    def get_capacite(self):
        ''' retourne la capacite de buffer '''
        return self.__capacite
    
    def get_len_fifo(self):
        ''' retounr le nombre de paquets stocké dans le buffer '''
        return len(self.__fifo)
    
    def get_taux_transmission(self):
        ''' retourne le taux de transmission de lien '''
        return self.__taux_transmission
    
    def remise_zero(self):
        ''' mise a zero de buffer '''
        self.nb_paquets_rejete=0
        self.__fifo=[]
    
        

class Source(object):
    ''' Représente une source de paquets.
    Chaque objet de cette classe générera des paquets à des intervalles aléatoires '''

    # attribué des id aux paquets envoyé par la source lors de leurs creations 
    id_paquet=0
    
    def __init__(self,buffer):
        self.__buffer=buffer # le buffer ou le paquets est envoyé
        
    def envoie_paquets(self,n):
        '''Methode permattent d'envoyer n paquets vers le buffer
            n-> represente le taux d'arrive de la source cad R= paquets/sec '''
        
        for _ in range(n):
            # creer un paquet , lors de sa creation le paquet definit son temps d'envoie
            paquet=Paquet(self.id_paquet)
            self.id_paquet+=1
            # l'envoyé au buffer 
            self.__buffer+=paquet
    
    def get_buffer(self):
        ''' retourne le buffer ou la source envoie ses paquets '''
        return self.__buffer
    
class Paquet(object):
    ''' dans cette classe les objets Représente un paquet de données.
        '''
    
    def __init__(self,idp):
        # Un paquet est representé juste par un id
        self.__idp=idp
        # le temps au le paquet a été generer( cad envoyé par la source)
        self.__temps_arrivee=time.time()
        self.__temps_attente=None
    
    def set_temps_attente(self,t):
        ''' definir le temps d'attente de paquet ,
            cad le temps ou il est retiré de la file - le temps ou il est envoyé par la source '''
        self.__temps_attente=t-self.__temps_arrivee
    
    def get_temps_attente(self):
        ''' retourne le temps d'attente de paquet '''
        return self.__temps_attente
    