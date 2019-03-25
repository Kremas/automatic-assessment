.. Automatic assessment documentation master file, created by
   sphinx-quickstart on Fri Mar 15 09:37:23 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Bienvenue dans notre documentation!
***********************************


Le projet
=========

Contexte
--------

De nombreux projets et travaux pratiques sont réalisés dans le cadre de la formation des étudiants.
Aujourd’hui, ces travaux pratiques sont corrigés à la main par les enseignants, c’est une tâche très longue et complexe.
Le but du projet de correction automatisée de codes et de configuations est d’automatiser cette phase de correction, via un outil informatique. Le processus de correction de codes et configurations devrait se rapprocher du schéma suivant :

* `Architecture <./architecture.html>`_

Enjeux et objectifs
-------------------

L’enjeu est de disposer d’un outil commun et centralisé, utilisé par différentes populations d’enseignants, et suffisamment ergonomique pour que les enseignants scientifiques puissent exiger une correction automatisée des travaux pratiques de leurs étudiants, tout en délimitant la correction par des critères précis.
Dans ce contexte et avec ces enjeux, l’objectif est de lancer un projet de mise en œuvre d’un outil novateur de correction automatisée de codes et de configurations systèmes et réseaux
Ce projet s’insère dans une trajectoire de modernisation et de simplification des corrections de TP, pour que les enseignants passent moins de temps sur ces tâches redondantes.

Documentation
=============

Prérequis
---------

* docker
* python 3
* pip
  
   * flask
   * flask_wtf
   * lxml
   * docker
   * ciscoconfparse
   * sphinx (documentation)
   * sphinx_rtd_theme (documentation)

.. toctree::
   :maxdepth: 3
   :caption: Contenu

   architecture
   form
   reseau
   java
   python
   c
   docker

