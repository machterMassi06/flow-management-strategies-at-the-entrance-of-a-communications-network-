# module principale a executer pour lancer l'appli 
import tkinter as tk
from structure import Buffer,Source# importer nos classes

# importer les modules d'analyse performance et visual1 de la partie 1
import analysePerformance
import Visual1
# importer les modules d'analyseperformanceStrategie et visual2 avec strategies de la partie 2
# fait appel a son role a strategies.py
import analysePerformanceStrategie 
import Visual2 

class Main(tk.Tk):
    def __init__(self):
        ''' cette classe modelise l'interface graphique finale de notre application ,modelise un choix entre
        les deux parties de projet 
        '''
        # herité de la classe tk.Tk
        super().__init__() 
        self.title("Application")
        lbl=tk.Label(self,text="Gestion de flux à l’entrée d’un un réseau de communication ")
        lbl.pack(pady=10)
        lbl1=tk.Label(self,text=" Choisir la partie de projet :")
        lbl1.pack(pady=10)
        btn_partie1 = tk.Button(self, text="Partie 1  ", command=self.partie1)
        btn_partie1.pack(pady=10)
        
        btn_partie2 = tk.Button(self, text="Partie 2  ", command=self.partie2)
        btn_partie2.pack(pady=10)
        lbl2=tk.Label(self,text="Projet mené en binôme : MACHTER Massinissa, KHAZEM Lynda , Année : 23/24")
        lbl2.pack(pady=10)
        # lancer la feetrre
        self.mainloop()
    
    def partie1(self):
        ''' lance l'interface de la partie 1 '''
        Choix1(self)
    
    def partie2(self):
        ''' lance l'interface de la partie 2 '''
        Choix2(self)

class Choix1(tk.Toplevel):
    ''' cette classe modelise un choix entre choisir entre visualiser la dynamicité de systeme 
         ou la performance de systeme (Partie1) '''
    def __init__(self,master):
        # herité de la classe tk.Tk
        super().__init__(master)
        self.title("Choix (Partie 1)")
        
        btn_visualiser = tk.Button(self, text="Visualiser les performances performances du réseau en fonction λ", command=self.visualiser_performances)
        btn_visualiser.pack(pady=10)
        
        btn_lancer_simulation = tk.Button(self, text="Lancer la simulation pour voir la dynamicité du système ", command=self.lancer_simulation)
        btn_lancer_simulation.pack(pady=10)
        self.mainloop()
    def visualiser_performances(self):
        ''' Methode permattant de voir le graphisme qui indique le taux de pertes de paquets en fct de lambda
            qui varient (Partie1)'''
        self.destroy()  # Fermer la fenetre de choix
        # definir une capacité de buffer
        capacite = 15 
        # et le taux de transmission du lien  p/sec
        taux_trans = 3
         # creation du buffer
        buffer = Buffer(capacite, taux_trans)
         # init 2 source avec le buffer principale en commun
        liste_source = [Source(buffer) for _ in range(2)]
        # faire appel a nos fonction d'analyse
        # dans le module analysePerformance de la partie 1
        lmbda, paquets_rejetes = analysePerformance.analyse(buffer, liste_source)
        analysePerformance.performance(lmbda, paquets_rejetes)
    
    def lancer_simulation(self):
        ''' Methode qui fait appel Interface du module visual.py , permattant de visualiser
            la dynamicité de reseau (partie 1 ) '''
        # Fermer la fenêtre de choix
        self.destroy()  
        Visual1.Interface() # Lancer l'interface partie 1

class Choix2(tk.Toplevel):
    ''' classe modelise un choix entre choisir entre visualiser la dynamicité de systeme
        ou la performance de systeme avec strategies (Partie2)'''
    def __init__(self,master):
        # herité de la classe tk.TopLevel cad la fenetre mere Main
        super().__init__(master)
        self.title("Choix (Partie 2)")
        
        btn_visualiser = tk.Button(self, text="Comparer les performances des 3 stratégies ", command=self.visualiser_performances)
        btn_visualiser.pack(pady=10)
        
        btn_lancer_simulation = tk.Button(self, text="Dynamicité du système avec stratégie a Choix", command=self.lancer_simulation)
        btn_lancer_simulation.pack(pady=10)
        # lancer la feetrre
        self.mainloop()
    def visualiser_performances(self):
        ''' Methode pour visualiser les performance des strategies en fonction de temps moyen d'attente d'un paquet et
        en fonction de taux de pertes des paquets en %'''
    
        self.destroy()  # Fermer la fenêtre de choix
        # Init la file principale B
        file_principale=[]
        # creation du buffer bi de chaque source i ( ici simulation a l'aide de 3 sources)
        buffers = [Buffer(15),Buffer(10),Buffer(18)] 
        liste_source = [Source(buffers[i]) for i in range(3)] # init 3 source avec leurs buffer bi 
        # faire appel a nos fonction d'analyse des performance
        # dans le module analysePerformanceStrategie
        temps_moyen_att, paquets_rejetes = analysePerformanceStrategie.analyse(liste_source,file_principale)
        analysePerformanceStrategie.performance(temps_moyen_att, paquets_rejetes)
    
    def lancer_simulation(self):
        ''' Methode permattent d'appeler Interface() dans le module visual2.py
            qui nous permet de voir la dynamicite de reseau avec choix de strategie '''
        self.destroy()  # Fermer la fenêtre de choix
        Visual2.Interface() # Lancer l'interface

if __name__=="__main__":
    Main()