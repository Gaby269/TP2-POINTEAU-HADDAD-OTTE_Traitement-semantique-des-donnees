import rdflib
import utilities
from parseur import *
import similarites
import time
import ngram
import datetime
import os
#UNUSED : normalized_levenshtein_similarity, jaro_similarity, synonymy_similarity, smoa_similarity

###########
# Données #
###########

nbPrints = -1  # nombre fixé pour n'afficher qu'une parties des valeurs
DEBUG = 0  # 1 pour afficher les prints et le temps pris (temps+), 0 sinon
x = str(datetime.datetime.now()).split()
time_key = (x[0] + "-" + x[1].split('.')[0]).replace(":", "-")

# Liste des fonctions de similarités possibles
listSimilarite = [
    similarites.levenshtein_similarity,
    similarites.jaro_similarity, 
    ngram.NGram.compare,
    # similarites.synonymy_similarity, beaucoup trop de temps
    similarites.jaccard_similarity,
    similarites.monge_elkan_symmetric,
    similarites.moyenne_des_similarites
]

# Liste de seuil allant de 0,55 à 1,00 avec un pas de 0,05 pour modéliser les similarité
listThresholds = [str(i/100) for i in range(50, 101)]

utilities.cleanScreen()


########################
# Test des similarites #
########################

print("\n##########################\n## Test des similarites ##\n##########################\n")

# print("Test des similarites\n")
mot1, mot2 = ["je vais me   promener dans la foret", "je vais   promener dans la foret"]
print(f'Test des similarite avec les mots "{mot1}" et "{mot2}"\n')

# Pour chaque fonction de similarité
for similarite in listSimilarite:
    temps_deb = time.time()
    print(similarite.__name__, ":", round(similarite(mot1, mot2), 5), "- temps :", round(time.time() - temps_deb, 5))
print()


##########################
# Choix de l'utilisateur #
##########################

print("\n############################\n## Choix de l'utilisateur ##\n############################\n")

### Choix par l'utilisateur de la fonction de similarité

print("Liste des similarités : \n\n  1 - Similarité de Levenshtein\n  2 - Similarité de Jaro\n  3 - Similarité N-gram\n  4 - Similarité étendue de Jaccard\n  5 - Similarité de Monge-Elkan\n  6 - Moyenne des similarités\n")
nb_function = input("Veuillez choisir une similarité : ")

# Vérification si le nombre entré est bien dans la liste
while (nb_function not in [str(i) for i in range(7)]):
    nb_function = input("\nVeuillez choisir une option valide : ")

# Permet de sortir du code si on met 0
if nb_function == "0":
    exit(1)

# Récuperer le nom de la similarité choisis
similarity_function = listSimilarite[int(nb_function) - 1]
print("\n\nVous avez choisi la fonction", similarity_function.__name__, "\n")



### Choix par l'utilisateur du seuil

threshold = input("Veuillez entrer la valeur du threshold entre 0.50 et 1.0 : ")

# Vérification si le nombre entré est bien dans la liste
while (threshold not in listThresholds) and (threshold != "1") and (threshold != "0"):
    threshold = input("\nVeuillez choisir une option valide : ")

# Permet de sortir du code si on met 0
if threshold == "0":
	print("\nAu revoir !! \n\n")
	exit(1)


print(f"\nVous avez choisi un seuil de {threshold} \n\n")
threshold = float(threshold)
# threshold = 0.99



###########
# PARSING #
###########

print("\n#############\n## PARSING ##\n#############\n")

### Parsing des fichier .ttl

# Parsing des graphes source et target, g1 et g2 sont des dictionnaires
g1 = parseur("files/source.ttl")
g2 = parseur("files/target.ttl")

# Transformer les dictionnaires en liste de triplet
liste_g1 = spo_formater(g1)
liste_g2 = spo_formater(g2)
print(f"Nombres d'entités de g1 : {len(liste_g1)}")
print(f"Nombres d'entités de g2 : {len(liste_g2)}\n")

# nombre de propriétés
nb_proprietes_g1 = count_properties(liste_g1)
nb_proprietes_g2 = count_properties(liste_g2)


### Parsing du fichier .rdf
# ground_truth = rdflib.Graph()
# ground_truth.parse("files/refDHT.rdf")
true_triplets = ground_truth_parser()  # parsing du fichier rdf
nbTrueMatches = len(true_triplets)     # taille de la liste des vrais triplets


############################
# Comparaison des fichiers #
############################

# Clean du terminal
utilities.cleanScreen()

print("\n##############################\n## Comparaison des fichiers ##\n##############################\n")

triplets = [] # liste des triplets
deb_time = 0 # Temps au départ

# Pour affichage
if DEBUG:
    input(f"Threshold à {threshold}, appuyez sur Entrer pour continuer...")
    utilities.cleanScreen()
else:
    print(f"Threshold à {threshold}...")
printCount = 0  # compteur d'affichage
startTime = time.time()  # stockage du temps de départ


# Boucle sur toutes les entités du graphe source, O(n²)
for sujet1, predicat1, objet1 in liste_g1:

    printCount += 1
    # Arret si le compteur d'affichage est arrivé à la fin
    # if printCount == nbPrints + 1:
    #     break

    if printCount % 500 == 0:
        print(f"Triplet : {printCount}/{len(liste_g1)}")

    similarites_predicats = {}

    # Boucle sur les entités du graphe cible
    for sujet2, predicat2, objet2 in liste_g2:

        # similarity_predicats = similarity_function(predicat1, predicat2)
        # if similarity_predicats >= 0.9:
        if predicat1 == predicat2:
            # Cas special si un objet est un blank node
            if isinstance(objet1, dict) or isinstance(objet2, dict):
                objet1 = str(objet1) # convertir en chaine de caractere
                objet2 = str(objet2) # convertir en chaine de caractere

            # Calcul de la similarité entre les objets
            similarity_objets = similarity_function(objet1, objet2)
            # on va chercher la similarité totale entre les deux entités
            if similarity_objets >= threshold:
                # on met à jour la similarité entre les deux entités
                similarity = similarites_predicats.get(predicat2, 0) + (similarity_objets/min(nb_proprietes_g1[sujet1],nb_proprietes_g2[sujet2]))
                if similarity >= threshold:
                    # print(f"{objet1} - {objet2} : {round(similarity, 5)}")
                    triplets.append((sujet1, "owl:sameAs", sujet2))


# Temps total de calcul
tempsTotal = str(round(time.time() - startTime, 2))
print(f"Temps total : {tempsTotal}s\n")

# Effacer les doubles de triplets
triplets = list(set(triplets))



###################################################
# Ecriture des triplets dans results/triplets.txt #
###################################################

print("\n#####################################################\n## Ecriture des triplets dans results/triplets.txt ##\n#####################################################\n")

os.makedirs(f"results/{time_key}", exist_ok=True)

f_results = open(f"results/{time_key}/triplets.txt", "w", encoding='utf8')

for triplet in triplets:
    f_results.write(triplet[0] + ", " + triplet[1] + ", " + triplet[2] + "\n")

f_results.close()

print("## Ecriture des triplets terminé ! ##\n\n")
		
#####################################################
# Calcul de la précision, le rappel et la f-measure #
#####################################################

print("\n#######################################################\n## Calcul de la précision, du rappel et la f-measure ##\n#######################################################\n")

precision_valeur = 0
recall_valeur = 0
f_measure_valeur = 0.0

# Données utiles pour le calcul
nbMatchesFound = len(triplets)  # taille des triplets calculés
true_matches_found = 0  # nombre des triplets qui sont dans le fichier rdf (vrai)

triplets = cutter(triplets)  # effacer <, > pour la comparaison

# Calcul du nombre de valeurs correspondantes aux valeurs de vérité
for triplet in triplets:
    if triplet in true_triplets:
        true_matches_found += 1

# Calcul en fonction des données
if nbMatchesFound > 0:
    precision_valeur = true_matches_found / nbMatchesFound
if nbTrueMatches > 0:
    recall_valeur = true_matches_found / nbTrueMatches
if (precision_valeur + recall_valeur) > 0:
    f_measure_valeur = (2*precision_valeur*recall_valeur) / (precision_valeur + recall_valeur)


print(f"Nombre de triplets trouvés : {len(triplets)}")
print(f"Nombre de triplets de vérité : {nbTrueMatches}")
print(f"Nombre de triplets de trouvés et vérités : {true_matches_found}")

# Affichage des calculs
print("Precision : ", round(precision_valeur, 5))
print("Rappel : ", round(recall_valeur, 5))
print("F-measure : ", round(f_measure_valeur, 5), "\n\n")


############################################
# Ecriture de f-mesure dans le fichier csv #
############################################

print("\n##############################################\n## Ecriture des mesures dans le fichier csv ##\n##############################################\n")

with open(f'results/{time_key}/measures.csv', 'w', encoding='utf8') as f:
    f.write("Nom fonction;threshold;precision;rappel;f-mesure")  # ecriture du nom de la fonction choisie
    f.write(f"{similarity_function.__name__};{threshold};{round(precision_valeur, 5)};{round(recall_valeur, 5)};{round(f_measure_valeur, 5)}\n")

print("## Ecriture des fmeasures dans le fichier csv terminé ##\n")