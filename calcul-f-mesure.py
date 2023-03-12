import rdflib
import utilities
from parseur import *
import similarites
import time
import datetime
# pip install -r requirements.txt

nbPrintMax = 2
x = str(datetime.datetime.now()).split()
time_key = (x[0] + "-" + x[1].split('.')[0]).replace(":", "-")

###########
# Données #
###########

# Liste de seuil allant de 0,55 à 1,00 avec un pas de 0,05 pour modéliser les similarité
listThresholds = [x / 100 for x in range(55, 101, 5)]

# Choix de la similarité par l'utilisateur
listSimilarite = [
    similarites.levenshtein_similarity,
    similarites.jaro_similarity, 
    similarites.NGrams_similarity,
    # similarites.synonymy_similarity, trop de temps zbi
    similarites.jaccard_similarity,
    similarites.monge_elkan_symmetric
]

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
print(f"nombres de triplets de g1 : {len(liste_g1)}")
print(f"nombres de triplets de g2 : {len(liste_g2)}\n")


### Parsing du fichier .rdf

ground_truth = rdflib.Graph()
ground_truth.parse("files/refDHT.rdf")

# Recuperation des valeurs de vérités formatées en triplet par le fichiers rdf (on le fait hors la boucle)
true_triplets = ground_truth_parser()  # parsing du fichier rdf
nbTrueMatches = len(true_triplets)     # taille de la liste des vrais triplets


#################################
# Préparation des deux fichiers #
#################################

with open(f'results/fmeasuresFull{time_key}.csv', 'w', encoding='utf8') as f:
    f.write("Fonction de similarite\Seuil")
    for threshold in listThresholds:
        f.write(f";{threshold}")
    f.write("\n")

with open(f'results/timesFull{time_key}.csv', 'w', encoding='utf8') as f:
    f.write("Fonction de similarite\Seuil")
    for threshold in listThresholds:
        f.write(f";{threshold}")
    f.write("\n")

	
############################
# Comparaison des fichiers #
############################

utilities.cleanScreen()
print("\n##############################\n## Comparaison des fichiers ##\n##############################\n")

start_total_time = time.time()

for similarity_function in listSimilarite:
    print("\nFonction : ", similarity_function.__name__, "\n\n")

    # Liste des triplets et liste des f_measures
    triplets = []
    f_measures = []
    times = []

    # Boucle pour chaque seuil de similarité
    for threshold in listThresholds:

        # nbPrint = 0
        print(f"Threshold à {threshold}...")
        start_threshold_time = time.time()  # stockage du temps de départ

        # Boucle sur toutes les entités du graphe source, O(n²)
        for sujet, predicat, objet in liste_g1:

            # nbPrint += 1
            # if nbPrint == nbPrintMax:
            #     break

            # Boucle sur les entités du graphe cible
            for sujet2, _, objet2 in liste_g2:

                # Cas special si un objet est un blank node
                if isinstance(objet, dict) or isinstance(objet2, dict):
                    objet = str(objet)  # convertir en chaine de caractere
                    objet2 = str(objet2)  # convertir en chaine de caractere

                # Calcul de la similarité entre le sujet de la source et le sujet du target
                similarity_sujets = similarity_function(sujet, sujet2)
                # Si la similarité calculé est plus grand que le seuil courant
                if similarity_sujets > threshold:
                    triplets.append((sujet, "owl:sameAs", sujet2))  # ajout aux triplets

                # De même pour les objets
                similarity_objets = similarity_function(objet, objet2)
                if similarity_objets > threshold:
                    triplets.append((objet, "owl:sameAs", objet2))


        # Temps total de calcul
        temps_threshold = str(round(time.time() - start_threshold_time, 2))
        times.append(temps_threshold)
        print(f"Temps total : {temps_threshold}s")



        #####################################################
        # Calcul de la précision, le rappel et la f-measure #
        #####################################################
		
        print("\n#######################################################\n## Calcul de la précision, du rappel et la f-measure ##\n#######################################################\n")


        precision_valeur = 0
        recall_valeur = 0
        f_measure_valeur = 0.0

		# Données utiles pour le calcul
        nbMatchesFound = len(triplets)  # taille des triplets calculés
        true_matches_found = 0  # nombre des triplets qui sont

        triplets = list(set(triplets)) # Effacer les doubles de triplets
        triplets = cutter(triplets)  # effacer <, > pour la comparaison
		
        # Calcul des vrais valeurs
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

        # Affichage des calculs
        print("Precision : ", round(precision_valeur, 5))
        print("Rappel : ", round(recall_valeur, 5))
        print("F-measure : ", round(f_measure_valeur, 5), "\n\n")

        # Ajout à la liste
        f_measures.append(round(f_measure_valeur, 5))

		
    ############################################
    # Ecriture de f-mesure dans le fichier csv #
    ############################################

    print("\n##############################################\n## Ecriture de f-mesure dans le fichier csv ##\n##############################################\n")


    with open(f'results/fmeasuresFull{time_key}.csv', 'a', encoding='utf8') as f:
        f.write(f"{similarity_function.__name__}")
        for f_measure in f_measures:
            f.write(f";{f_measure}")
        f.write("\n")    
        
    with open(f'results/timesFull{time_key}.csv', 'a', encoding='utf8') as f:
        f.write(f"{similarity_function.__name__}")
        for temps in times:
            f.write(f";{temps}")
        f.write("\n")
            
    print("\n ## Comparaisons pour tout les thresholds terminée ##\n")


print("Calcul de toutes les f-mesures terminées")
print(f"Temps total : {str(round(time.time() - start_total_time,1))}s")