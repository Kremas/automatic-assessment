Correction Java
***************

hamcrest-all-1.3.jar
====================

Archive `Hamcrest <http://hamcrest.org/JavaHamcrest/tutorial>`_. Hamcrest est un framework permettant d'écrire des règles de correspondance utilisables avec d'autres frameworks. Il est utilisé avec JUnit dans le cadre de tests unitaires et est donc livré avec ce dernier.


junit-4.13-beta-1.jar
=====================

Archive `JUnit <https://junit.org/junit5/>`_. JUnit est un framework de tests unitaires pour le langage Java.

MaClasse.java
=============

Exemple de classe à tester. La classe est composée comme suit :

.. code-block:: java
   :linenos:

   public class MaClasse{
     public static int add(int a, int b) {
       int res = a + b;
       return res;
     }

     public static int sub(int a, int b) {
       int res = a - b;
       return res;
     }

     public static int multiply(int a, int b) {
       int res = a * b;
       return res;
     }

     public static double divide(int a, int b) {
       double res;
       if(b != 0) res = a / b;
       else res = 0.0;
       return res;
     }

     public static String concatenate(String a, String b) {
       return a + b;
     }
   }

maclasse.xml
============

XML exemple de tests unitaires, généré par le formulaire. Par exemple :

.. code-block:: xml
   :linenos:

   <tp>
     <langage>java</langage>
     <compilation>
       <command>javac MaClass.java</command>
       <point>2</point>
     </compilation>
     <test>
       <type>assert</type>
       <function>add(1,2)</function>
       <result>3</result>
       <points>2</points>
     </test>

     <test>
       <type>assert</type>
       <function>sub(5,2)</function>
       <result>3</result>
       <points>2</points>
     </test>
   </tp>

MaClasseTest.java
=================

Fichier créé automatiquement par le script xmlJavaClass. Il comprend les tests unitaires qui seront effectués. Pour lancer manuellement les tests unitaires :

Compilation
-----------

.. code-block:: console

   javac -cp junit-4.13-beta-1.jar:hamcrest-all-1.3.jar:. MaClasseTest.java TestRunner.java

Exécution
---------

.. code-block:: console

   java -cp hamcrest-all-1.3.jar:junit-4.13-beta-1.jar:. TestRunner

TestRunner.java
===============

Ce fichier lance le test JUnit sur la classe "MaClasseTest" et affiche un résultat sous forme d'un document XML, regroupant les différentes erreurs s'il y en a.
Par exemple en cas de réussite :

.. code-block:: xml
   :linenos:

   <result>
     <testrun>3</testrun>
     <failure>
     </failure>
     <success>true</success>
   </result>

Dans le cas où l'un des tests unitaires n'est ps validé :

.. code-block:: xml
   :linenos:

   <result>
     <testrun>3</testrun>
     <failure>
       <test>
         <function>add(MaClasseTest)</function>
         <message>add(1,2) expected:<4.0> but was:<3.0></message>
       </test>
     </failure>
     <success>true</success>
   </result>

xmlJavaClass.py
===============
.. automodule:: xmlJavaClass
   :members:
   :undoc-members:
