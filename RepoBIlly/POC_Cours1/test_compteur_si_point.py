import unittest
from compteur import Compteur

class TestCompteur(unittest.TestCase):
    def test_compter_les_mots(self):
        texte = "chat cHat chien chat."
        compteur = Compteur(texte)

        motsTries = compteur.compter_les_mots()

        # On vérifie que le résultat contient les bons comptes
        self.assertEqual('chat', motsTries[0][0])
        self.assertEqual('chien', motsTries[1][0])

if __name__ == '__main__':
    unittest.main()