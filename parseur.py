import numpy as np

#Sujet : lien entite
#Predicat : relation/caracteristique
#Object : le precision/description


# Fonction qui prend une chaine de caractère
# la divise en sous-chaine séparées par des points-virgules (;)
# en prenant en compte les crochets ([...]) qui peuvent apparaître dans la chaîne
def split_property(string):

	splitted_string = []  # liste pour les sous-chaines résultantes
	current_split = ""  # stocke la sous-chaine courante
	current_bracket = ""  # stocke ce qu'il y entre les crochets présents (sup dès le crochet fermé)

	string_open = False  # indique qu'une chaine en cours de traitement (guillemet ouvert)
	bracket_open = False  # indique qu'un crochet a été ouvert (pas fermé)

	# Pour chaque caractère dans la string donnée
	for c in string:

		# Si on rencontre un guillement
		if c == "\"":
			string_open = not (string_open
			                   )  # changement d'état par rapport aux guillemets

		# Sinon Si c'est un crochet ouvrant et qu'une chaine est en cours de traitement
		elif c == "[" and not (string_open):
			bracket_open = True  # changement d'état par rapport aux crochets (ouverture)

		# Sinon Si c'est un crochet fermant et qu'une chaine est en cours de traitement
		elif c == "]" and not (string_open):
			current_split = current_split + "[" + current_bracket + "]"  # stockage sous-chaine + interieur crochet
			current_bracket = ""  # suppression de l'interieur des crochets
			bracket_open = False  # changer l'état par rapport aux crochets (fermeture)

		# Sinon Si  c'est un ; et chaine en cours de traitement et que crochet ouvert
		elif c == ";" and not (string_open) and not (bracket_open):
			splitted_string.append(current_split)  # ajout de la sous-chaine courante
			current_split = ""  # suppression de la sous-chaine courante

		# Sinon Si un crochet est ouvert
		elif bracket_open:
			current_bracket += c  # Ajout du caractère dans la sous-chaine entre les crochets

		# Sinon
		else:
			current_split += c  # Ajout du caractère dans la sous-chaine courante

	# Ajout de la sous-chaine courante
	splitted_string.append(current_split)

	# Return la liste des chaines
	return splitted_string


# Fonction qui prend en entré des entités
# renvoie un dictionnaire des propriétés de cette entité formatées
def formater(entity):

	# Liste des propriétés de l'entité (liste de sous-chaine) à l'aide de split_property pour chaque entity
	props = [prop.strip() for prop in split_property(" ".join(entity[1:]))]
	proprietes = {}  # propriétés formatées de l'entité

	# Pour chaque propriétés données
	for prop in props:

		cut = prop.index(" ")  # coupe la chaine en deux au niveau de l'espace
		key = prop[:cut].strip()  # première partie est stocké dans key
		object = prop[cut:].strip(". ")  # deuxième dans object sans les points

		# Si la valeur de la propriété commence par un crochet ouvrant
		if object.startswith("["):

			object_brckets = object.strip(
			 " []")  # suppression des crochets pour avoir la sous-chaine
			object_brckets_splitted = split_property(
			 object_brckets)  # parse la chaine à l'aide de split_property
			object_brckets_formated = {
			}  # définie un sous-dictionnaire courant pour stocker les sous chaines des propriétés

			# Pour chaque sous-propriété dans la liste
			for sub_prop in object_brckets_splitted:
				sps = sub_prop.strip()  # supprime les espace avt et après la chaine
				sub_cut = sps.index(
				 " ")  # trouver l'index de la première occurence d'un espace
				sub_key = sps[:sub_cut].strip()  # stocker dans la clé le début
				sub_object = sps[sub_cut:].strip(". ")  # stocker dans l'object la fin
				object_brckets_formated[
				 sub_key] = sub_object  # ajout dans le sous-dico avec comme clé le nom de la propriété

			proprietes[
			 key] = object_brckets_formated  # Ajout au dico des propriétés générales le sous-dico courant

# Sinon si c'est pas un crochet ouvrant
		else:
			proprietes[key] = object  # ajout au dictionnaire simplement

	return proprietes  # return le dico


# Parser les fichiers source.ttl, target.ttl, et refDHT.rdf
# Pour obtenir un dictionnaire de toutes les entités et les propriétés de chaque
def parseur(file):

	RDF_parse = {
	}  # dictionnaire vide qui sera rempli avec les entités du fichier
	prefixes = {}  # dictionnaire qui stocke les préfixes du fichier
	entite_raw = [
	]  # liste qui stocke les lignes brut d'une entité en cours de traitement

	# Parcours du fichier en lecture
	for line in open(file, "r", encoding='utf8'):

		ls = line.strip()  # on enleve les espaces avant et après

		# Si la ligne est vide
		if ls == "":
			continue  # skip des lignes vides

		# Sinon Si la ligne commence par "@prefix"
		elif ls.startswith("@prefix"):

			prefixe = ls.split()  # on split par les espaces
			prefixes[prefixe[1].split(":")[0]] = prefixe[
			 2]  # separation entre le nom et le lien
			# regex : <[^>]*>

		# Sinon
		else:

			entite_raw.append(ls)  # on ajoute la ligne à l'entité courrante
			# Si la ligne se termine par un point
			if ls[-1] == ".":
				entite_form = formater(entite_raw)  # formater la liste des entités
				RDF_parse[entite_raw[
				 0]] = entite_form  # remplir le dico par la liste des entités formatter (clé : entité)
				entite_raw = []  # vider le tableau courant

	return RDF_parse  # return du dictionnaire


# Prend en entrée un parsed_graph de la fonction parser()
# Renvoie une liste de 3-tuples, un pour chaque relation dans le graphe
def spo_formater(parsed_graph):

	list_of_triplets = []  # liste qui va contenir

	# Pour chaque clé valeur, du parseur
	for key, value in parsed_graph.items():

		preds, objs = list(zip(*value.items()))  # recupère les predicats et les objets dans deux listes
		keys = tuple(np.repeat(key, len(value.items())))  # repéter les clés autant de fois qu'il y a de propriétés
		sol = list(zip(keys, preds, objs))  # creation des triplets à l'aide de zip pour rassembler les listes keys, preds et objs
		list_of_triplets.append(sol)  #  ajout à la liste pour chaque entité du graph

	# Former les triplets à l'aide de la liste
	triplets = [item for sublist in list_of_triplets for item in sublist]

	return triplets # retourne les triplets



	
# Parse le fichier refDHT.rdf 
# tel que la sortie soit de la forme (s, p, o) 
# de le même manière que les fichier source.ttl et target.ttl
def ground_truth_parser():

	entite_1 = []  # les entites dans rdfDHT qui appartiennent à source
	entite_2 = []  # les entites dans rdfDHT qui appartiennent à target
	true_triplets = []  # liste des true triplets

	file = open("files/refDHT.rdf") # lecture du fichier rdfDHT.rdf

	# Pour chaque ligne du fichier
	for line in file:

		# Si le début de la ligne est entite1
		if line[1:8] == "entity1":
			entite_1.append(line[23:-4]) # on ajoute à la liste des entité1 le lien URI associé

		# Si le début de la ligne est entite2
		if line[1:8] == "entity2":
			entite_2.append(line[23:-4]) # on ajoute à la liste des entite2 le lien URI associé

	# Pour chaque élément de chaque liste d'entite
	for i in range(len(entite_1)):
		true_triplets.append((entite_1[i], "owl:sameAs", entite_2[i])) # ajout du triplet dans true_triplet

	return true_triplets 


# Cutter efface les <, > au debut et fin des arguments dans les triplets
def cutter(triplet_list):

	for index, triplet in enumerate(triplet_list):

		subj, pred, obj = triplet
		if subj[-1] == ">":
			subj = subj[1:-1]
		if obj[-1] == ">":
			obj = obj[1:-1]
		if pred[-1] == ">":
			pred = pred[1:-1]
		triplet_list[index] = (subj, pred, obj)

	return triplet_list

# fonction qui compte le nombre de propriétés de chaque entité et renvoie un dictionnaire
def count_properties(triplets):
    properties_count = {}
    for triplet in triplets:
        properties_count[triplet[0]] = properties_count.get(triplet[0], 0) + 1
    return properties_count