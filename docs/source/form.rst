Formulaire
**********

helper/
=======

Ce dossier contient les sripts Python utilisés pour lancer les tests
unitaires, les recherches de motif, et les conteneurs Docker

templates/
==========

Ce dossier contient tous les templates HTML utilisés par le fichier server.py. On peut lister :
   - test.html : template principal, pour le formulaire de correction de code
   - result.html : template utilisé pour l'affichage des résultats
   - nav.html : template de la barre de navigation
   - liste.html : template de la liste des tests sauvegardés
   - cisco.html : template du formulaire propre aux corrections de configurations cisco

saved_test/
===========

Ce dossier contient un dossier pour chaque test sauvegardé. On peut y retrouver les codes étudiants, les sujets ainsi que les champs remplis du formulaire.
     
server.py
=========

Ce module est basé sur 
   - `WTForm <https://wtforms.readthedocs.io>`_
   - `flask <http://flask.pocoo.org/docs>`_

C'est le composant principal du projet. 

.. automodule:: server
   :members:

