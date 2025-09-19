from compteur import Compteur

filename = input("Entrez le nom du fichier : ")
with open(filename, "r", encoding="utf-8") as f:
    contenu = f.read()

compteur = Compteur(contenu)
print(compteur.compter_les_mots())
