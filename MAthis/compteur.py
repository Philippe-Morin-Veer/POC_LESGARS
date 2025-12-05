import operator 
import string

class Compteur():
    def __init__(self,texte):
        self.texte = texte
    
    def compter_le_mots(self):
        mots = self.texte.split()
        compte_des_mots = {}
        for mot in mots:
            mot_nettoyer = mot.strip(string.punctuation).lower()
            if mot_nettoyer not in compte_des_mots:
                compte_des_mots[mot_nettoyer] = 1
            else:
                compte_des_mots[mot_nettoyer] += 1
        mots_tries = sorted(compte_des_mots.items(), key = operator.itemgetter(1), reverse = True)
        return mots_tries
                        
