# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 14:59:26 2022

@author: marga
"""
# Librairies 
import unittest
import praw
from PyQt5.QtWidgets import *

from Classes import Post
from TPs import suspendu
from TPs import plageHoraire
from TPs import postASucces
from TPs import pourcentage

# Identification
reddit = praw.Reddit(client_id='qfGg1ZCyWvsU9etXwc1uzA', client_secret='qVMQes3UvGw0LL3rnaPsiFWcpdv-nA', user_agent='Projet Python', check_for_async=False)

# Classe de test
class test:
    def __init__(self, succes, horaire, score, upvote, downvote):
         self.succes = succes
         self.horaire = horaire
         self.score = score
         self.upvote = upvote
         self.downvote = downvote
         
         

test1 = test(True, "09:00:00", 15, 10, 5)
test2 = test(True, "15:00:00",30, 25, 5 )
test3 = test(True, "22:00:00", 10, 5,5)
test4 = test(True, "00:00:00", 100, 50, 50)  
test5 = test(False, "10:00:00", 200, 150, 50)
test6 = test(False, "16:00:00", 100, 40, 60)  
test7 = test(False, "23:00:00", 2000, 300, 1700)  
test8 = test(False, "06:00:00", 0, 0, 0)

tab1 = [test1,test5,test2]       
tab2 = [test1,test2,test6] 
tab3 = [test3,test7,test6]
tab4 = [test4,test3,test8]

class TestUtils(unittest.TestCase):
    def test_nettoyer_texte(self):
        self.assertEqual(Post.nettoyer_texte("CouCou"), 'coucou')
        self.assertEqual(Post.nettoyer_texte("!#$c%&'()o*+,-.u/:;c<=>?@[o\]^_`{u|}~"), "coucou")
        self.assertEqual(Post.nettoyer_texte("co5uco9u"), "coucou")
        self.assertEqual(Post.nettoyer_texte("cou’co‘u"), "cou co u")
        self.assertEqual(Post.nettoyer_texte("coucou \n"), "coucou ")
        self.assertEqual(Post.nettoyer_texte("coucou \n j'ai 20 ans ! Et toi ? aussi‘"), "coucou  jai  ans  et toi  aussi ")
    
    def test_suspendue(self):
        self.assertFalse(suspendu('the_Diva',reddit))
        self.assertTrue(suspendu('foreverwasted', reddit))
        
    
    def test_plageHoraire(self):
        heure = QLabel("")
        self.assertEqual(plageHoraire(tab1, heure), "Le moment de la journée où les gens postent le plus est: le matin")
        self.assertEqual(plageHoraire(tab2, heure), "Le moment de la journée où les gens postent le plus est: l après midi")
        self.assertEqual(plageHoraire(tab3, heure), "Le moment de la journée où les gens postent le plus est: le soir")
        self.assertEqual(plageHoraire(tab4, heure), "Le moment de la journée où les gens postent le plus est: la nuit")
    
    def test_postASucces(self):
        postasucces = QLabel("")
        self.assertEqual(postASucces(tab1, postasucces), "En moyenne, les auteurs des posts à succès produisent des posts du même type")
        self.assertEqual(postASucces(tab3, postasucces), "En moyenne, les auteurs des posts à succès ne produisent pas forcément des posts du même type ")
    
    def test_pourcentage(self):
        pourcentageup = QLabel("")
        pourcentagedown = QLabel("")
        self.assertEqual(pourcentage(tab4, pourcentageup, pourcentagedown), "Le pourcentage moyen d'upvote et downvote est 50.0 et 50.0")
        self.assertEqual(pourcentage(tab1, pourcentageup, pourcentagedown), "Le pourcentage moyen d'upvote et downvote est 75.0 et 25.0")
        self.assertEqual(pourcentage(tab3, pourcentageup, pourcentagedown), "Le pourcentage moyen d'upvote et downvote est 35.0 et 65.0")
        
if __name__ == '__main__':
    unittest.main()