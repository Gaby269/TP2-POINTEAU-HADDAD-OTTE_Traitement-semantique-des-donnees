# TP2- POINTEAU/HADDAD/OTTE - Traitement semantique des donnees


## Différents dossiers

Il y a deux dossiers : 

 * [***files***](https://github.com/Gaby269/TP2-POINTEAU-HADDAD-OTTE_Traitement-semantique-des-donnees/tree/main/files) : contient les fichiers [_source.ttl_](https://github.com/Gaby269/TP2-POINTEAU-HADDAD-OTTE_Traitement-semantique-des-donnees/blob/main/files/source.ttl) et [_target.ttl_](https://github.com/Gaby269/TP2-POINTEAU-HADDAD-OTTE_Traitement-semantique-des-donnees/blob/main/files/target.ttl) ainsi que [_rdfDHT.rdf_](https://github.com/Gaby269/TP2-POINTEAU-HADDAD-OTTE_Traitement-semantique-des-donnees/blob/main/files/rdfDHT.rdf).
 
 * [***result***](https://github.com/Gaby269/TP2-POINTEAU-HADDAD-OTTE_Traitement-semantique-des-donnees/tree/main/result) : Contient les fichiers résultats obtenus comme le fichier texte avec les triplets, ainsi que le fichier csv contenant les f-measures calculés. Il faut l'ajouter avec :
 ```
 mkdir result
 ```

## Autres fichiers

* [***calcul-f-mesure.py***](https://github.com/Gaby269/TP2-POINTEAU-HADDAD-OTTE_Traitement-semantique-des-donnees/blob/main/calcul-f-mesure.py) : comme le fichier main 
* [***graph.py***](https://github.com/Gaby269/TP2-POINTEAU-HADDAD-OTTE_Traitement-semantique-des-donnees/blob/main/graph.py) : fichier créeant le graph à partir des f-measures calculées;
* [***main.py***](https://github.com/Gaby269/TP2-POINTEAU-HADDAD-OTTE_Traitement-semantique-des-donnees/blob/main/main.py) : fichier qui parse les fichiers .ttl et .rdf et compare les deux fichiers source et target pour obtenir les triplets indiquant les deux entités sont similaires. Les triplets seront écrit dans le fichier text dans le dossier [result](https://github.com/Gaby269/TP2-POINTEAU-HADDAD-OTTE_Traitement-semantique-des-donnees/tree/main/result). Il calcul la precision, le rappel et la f-measure et les écrits dans le fichier csv créé dans le dossier [result](https://github.com/Gaby269/TP2-POINTEAU-HADDAD-OTTE_Traitement-semantique-des-donnees/tree/main/result);
* [***parseur.py***](https://github.com/Gaby269/TP2-POINTEAU-HADDAD-OTTE_Traitement-semantique-des-donnees/blob/main/parseur.py) : fichier qui parse les différents fichiers pour pouvoir les exploiter à notre manière;
* [***similarites.py***](https://github.com/Gaby269/TP2-POINTEAU-HADDAD-OTTE_Traitement-semantique-des-donnees/blob/main/similarites.py) : fichier contenant toutes les fonctions de similarités qu'on utilise qu'elle soit écrite par nous ou importer;
* [***utilities.py***](https://github.com/Gaby269/TP2-POINTEAU-HADDAD-OTTE_Traitement-semantique-des-donnees/blob/main/utilities.py) : fichier qui contient des fonctions d'affichages;

* [***utilities.py***](https://github.com/Gaby269/TP2-POINTEAU-HADDAD-OTTE_Traitement-semantique-des-donnees/blob/main/utilities.py) : 
