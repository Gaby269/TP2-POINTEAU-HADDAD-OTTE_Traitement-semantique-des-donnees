import os

## Affichage d'un dictionnaire correctement (dictionnaires dans des dictionnaires)
def pttl(k, v):
	# Affichage des cléfs
    print(k)
	# Pour chaque valeurs
    for prop in v:
		# Si la valeur est un dictionnaire
        if isinstance(v[prop], dict):
			# Affichage de la première valeur puis l'accolade
            print(prop,": {") 
			# Pour chaque sous valeur
            for sub_prop in v[prop]:
				# Affichage de la sous clé puis de la sous valeur (on a que une fois un sous disctionnaire)
                print(f"   {sub_prop} : {v[prop][sub_prop]}")
			# Affichage de fermeture d'une accolade
            print("}")
		# Sinon
        else:
			# Affichage simple de la clé et de la valeur
            print(f"{prop} : {v[prop]}")
	# Retour chariot
    print("\n")


## Fonction qui efface l'écran du terminal en fonction du système d'exploitation
def cleanScreen():
    if (os.name == "nt"): # Si c'est sur windows
        os.system('cls')
    elif (os.name == "posix"): #Si c'est sur Linux ou Unix
        os.system("clear")