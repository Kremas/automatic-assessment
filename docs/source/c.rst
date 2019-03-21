Correction C
************


calc.c
==============

Fichier de test avec diverses fonctions simples (additions, soustraction, ...) permettant de tester les test unitaires générés par notre script python et définis dans un fichier XML généré par le formulaire. Par exemple :

.. code-block:: c
   :linenos:

   #include "calc.h"
   #include <stdlib.h>
   #include <string.h>

   int add(int a, int b) {
      return a + b;
   }

   int sub(int a, int b) {
      return a - b;
   }

   int mul(int a, int b) {
      return a * b;
   }


calc.h
==============

Header du fichier calc.c

.. code-block:: c
   :linenos:

   #ifndef CALC_H 
   #define CALC_H

   int add(int, int);
   int sub(int, int);
   int mul(int, int);
   #endif


calc_test.c
===================

Fichier de tests unitaires CUnit généré par le script xmlCClass.py. L'exécution de tests unitaire en C nécessite les paquets libcunit1 et libcunit1-dev. Voir la `Documentation CUnit <http://cunit.sourceforge.net/doc/index.html>`_.

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
