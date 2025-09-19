import operator
import re

class Compteur():
    def __init__(self, texte):
        self.texte = texte

    def compter_les_mots(self):
        mots = re.findall(r'\b\w+\b', self.texte.lower())
        compte_des_mots = {}
        for mot in mots:
            if mot not in compte_des_mots:
                compte_des_mots[mot] = 1
            else:
                compte_des_mots[mot] += 1
        mots_tries = sorted(compte_des_mots.items(), key=operator.itemgetter(1), reverse=True)
        return mots_tries