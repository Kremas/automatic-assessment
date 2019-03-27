Docker
******

Docker est une solution de conteneurisation. Elle permet de créer des
environnement isolés dans lesquels nous exécutons les tests sur les codes des
étudiants.

dockerJava.py
=============

.. py:class:: dockerJava(code, c, name)
    
    Permet de créer les images et de lancer les containers afin de lancer les tests xUnit

    :param codes:
        Liste des codes étudiants
    :type codes: list
    :param c:
        Nom des classes Java. Tous les étudiants nomment leur classe du même
        nom
    :type c: str
    :param name:
        Nom du test
    :type name: str

    :ivar client:
        Permet la connection à docker en obtenant un client du docker engine
    :ivar dockerfile:
        Variable contenant le dockerfile. Un dockerfile est un fichier
        permettant de construire une image docker correspondante à nos besoin.
        Ici on utilise un environnement Java openjdk8 sur machine Alpine. On inclut
        également les codes à corriger à notre environnement.
    :ivar ret:
        JSon contenant les résultats de l'exécution, ensuite utilisé
        par le site pour afficher les résultats.

dockerC.py
=============

.. py:class:: dockerC(codes, classname, name)

    Permet de créer les images et de lancer les containers afin de lancer les tests xUnit

    :param dockerC.codes:
        Liste des noms de fichier à corriger
    :type dockerC.codes: list

    :param dockerC.classname:
        Nom de la classe à corriger
    :type dockerC.classname: str
    
    :param dockerC.name:
        Nom du TP
    :type dockerC.name: str

    :ivar client:
        Permet la connection à docker en obtenant un client du docker engine
    :ivar dockerfile:
        Variable contenant le dockerfile. Un dockerfile est un fichier
        permettant de construire une image docker correspondante à nos besoin.
        Ici on utilise un environnement gcc sur machine Alpine. On inclut
        également les codes à corriger à notre environnement.

    :ivar makefile:
        Makefile permettant de compiler le code à tester et la classe de test cUnit
    :type makefile: str

    :ivar ret:
         Contenant les résultats de l'exécution, ensuite utilisé par le site pour afficher les résultats.
