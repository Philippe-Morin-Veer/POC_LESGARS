import unittest
from compteur import Compteur

class TestCompteur(unittest.TestCase):
    def test_compter_le_mots(self):
        texte = "Chat chat. CHAT, chat!"
        compteur = Compteur(texte)
        resultat = compteur.compter_le_mots()
        self.assertEqual('chat', resultat[0][0])
        self.assertEqual(4, resultat[0][1])

if __name__ == '__main__':
    unittest.main()