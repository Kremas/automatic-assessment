Correction C
************


calc.c
==============

Fichier de test avec diverses fonctions simples (additions, soustraction, ...) permettant de tester les test unitaires générés par notre script python et définis dans un fichier XML généré par le formulaire.

calc.h
==============

Header du fichier calc.c

calc_test.c
===================

Fichier de tests unitaires CUnit généré par le script xmlCClass.py

Makefile
========

Fichier permettant la compilation du code en exécutable avec la commande 'make', puis le nettoyage des fichiers générés avec la commande 'make clean'

xmlCClass.py
====================

Ce script créé un fichier “calc_test.c” qui peut être utilisé pour tester le code C “calc.c” avec la commande “make” puis “./calc_test”. Attention à utiliser un fichier XML valide, généré par le formulaire. Ne pas oublier le “make clean” après le test.
Les points à attribuer à chaque exécution de test sont stockés dans un dictionnaire mais non utilisés pour le moment.


.. automodule:: xmlCClass
   :members:
   :undoc-members:
