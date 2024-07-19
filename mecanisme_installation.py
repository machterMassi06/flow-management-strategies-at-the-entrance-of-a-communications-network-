# Mecanisme d'installation de notre application

# il faut s'assurer d'avoir une version python >=3 
# il faut s'assurer que vous avez les deux modules suivant sur votre version
import subprocess
import sys
 
def installer(liste_modules):
    for module in liste_modules:
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])
        print("package :",module," installer avec succes ")

# Installation des modules nécessaires
if __name__ == '__main__':
    # liste des modules a installer
    # Les modules tkinter,time , random et math font partis de la bibliothèque standard de python  
    liste_modules = ['numpy','matplotlib']
    installer(liste_modules)


