from Levenshtein import distance
from Levenshtein import jaro as jaro_similarity
from nltk.corpus import wordnet
import nltk
import re
import ngram
# import numpy as np
import math
from py_stringmatching.similarity_measure import monge_elkan as monge_elkan_import

nltk.download('wordnet')  # sans ca, il y a une erreur

###############################
#### SIMILARITE DIFFERENTE ####
###############################


## Identité:
def identite_similarity(string_1, string_2):

	# Si identique
	if string_1 == string_2:
		return 1
	return 0


## Similarité de Levenshtein en utilisant la distance de levenshtein
def levenshtein_similarity(chaine1, chaine2):
	
	dist = distance(chaine1, chaine2) # calcul de la distance de levenshtein
	norm_dist = dist / max(len(chaine1), len(chaine2))  # normalisation
	
	return 1 - norm_dist # retourne l'inverse


## Similarité SMOA
# def smoa_similarity(chaine1, chaine2, matrice_poids):

# 	taille1, taille2 = len(chaine1), len(
# 	 chaine2)  # cacul des taille des deux chaines

# 	# Initialisation de la matrice
# 	tab_similarite = np.zeros(
# 	 (taille1 + 1, taille2 + 1))  # initialisation de la matrice
# 	for i in range(taille1 + 1):
# 		tab_similarite[i, 0] = i  # initialisation par i de la premiere ligne
# 	for j in range(taille2 + 1):
# 		tab_similarite[0, j] = j  # initialisation par j de la premiere colonne

# 	# Remplissage de la matrice de similarité
# 	for i in range(taille1):
# 		for j in range(taille2):

# 			# Coût d'alignement de deux sous-chaînes par la matrice des poid
# 			cout = matrice_poids[chaine1[i], chaine2[j]]

# 			# Calcul de la similarité d'alignement en fonction des similarité d'avant
# 			tab_similarite[i, j] = min(tab_similarite[i, j] + cout,
# 			                           tab_similarite[i + 1, j] + 1,
# 			                           tab_similarite[i, j + 1] + 1)

# 	# Normalisation de la similarité
# 	max_len = max(taille1, taille2)
# 	similarite = 1 - tab_similarite[taille1, taille2] / max_len

# 	return similarite


## Similarity de N-Grammes
def NGrams_similarity(chaine1, chaine2):

	# Calcul de n pour que ce soit de la forme f(chaine1, chaine2)
	n = math.ceil(min(len(chaine1), len(chaine2)) / 10)

	# Calcul des n-grames pour chaque chaine
	nG1 = [chaine1[i:i + n] for i in range(len(chaine1) - n + 1)]
	nG2 = [chaine2[i:i + n] for i in range(len(chaine2) - n + 1)]

	# Calcule de l'intersection entre les deux ensembles
	intersection = set(nG1) & set(nG2)
	taille_inter = len(intersection)

	# Calcul de la taille minimum entre les chaines
	taille_min = min(len(chaine1), len(chaine2))

	# Calcul de la similarité
	similarite_ngram = taille_inter / (taille_min - n + 1)

	return similarite_ngram


## Similarite des synonymes deuxième version
def synonymy_similarity(chaine1, chaine2):

	# URIs have no synonyms
	if ("http" in chaine1) or ("http" in chaine2):
		return 0

	# Split pour chaque " ", ":", "_", "-", ",", ";"
	wordlist1 = re.split('[ \'\":_\-,;]', chaine1)
	wordlist2 = re.split('[ \'\":_\-,;]', chaine2)

	# Effacement des "" dans la liste
	wordlist1 = list(filter(None, wordlist1))
	wordlist2 = list(filter(None, wordlist2))

	# Création de listes de synonymes de chaque mot
	synonymes1 = []
	synonymes2 = []

	# Ajout des mots dans les ensembles de synonymes
	for word1 in wordlist1:
		synonymes1.extend(wordnet.synsets(word1))
	for word2 in wordlist2:
		synonymes2.extend(wordnet.synsets(word2))

	# Trouver les synonymes communs des deux listes
	common_synonymes = len(list(set(synonymes1) & set(synonymes2)))
	max_synonymes = max(len(synonymes1), len(synonymes2), 1)

	return min(1, (common_synonymes / max_synonymes))


## Similarité de jaccard
def jaccard_similarity(chaine1, chaine2):

	# Récuperation des mots en liste
	words1 = set(re.findall(r'\w+', chaine1))
	words2 = set(re.findall(r'\w+', chaine2))

	# Calcul de l'intersection ainsi que de l'union
	intersection = len(words1.intersection(words2))
	union = len(words1.union(words2))

	# Calcul de la similarité
	return intersection / union


## Similarité de monge_elkan symmetrique en utilisant un import
def monge_elkan_symmetric(chaine1, chaine2):

	list1 = [str(chaine1)]  # transforme la chaine en liste
	list2 = [str(chaine2)]  # transforme la chaine en liste

	return monge_elkan_import.MongeElkan().get_raw_score(list1, list2)  # applique la similarité importé


def moyenne_des_similarites(str1, str2):
    simil1 = levenshtein_similarity(str1, str2)
    simil2 = jaro_similarity(str1, str2)
    simil3 = ngram.NGram.compare(str1, str2)
    simil4 = jaccard_similarity(str1, str2)
    simil5 = monge_elkan_symmetric(str1, str2)
    return (simil1 + simil2 + simil3 + simil4 + simil5) / 5