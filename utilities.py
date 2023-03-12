import os


## Fonction qui efface l'écran du terminal en fonction du système d'exploitation
def cleanScreen():
    if (os.name == "nt"): # Si c'est sur windows
        os.system('cls')
    elif (os.name == "posix"): #Si c'est sur Linux ou Unix
        os.system("clear")