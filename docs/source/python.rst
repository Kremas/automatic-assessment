Correction Python
*****************

calc.py
=======

Exemple de code à tester.

.. code-block:: python
   :linenos:

   class Calc:

      def add(self, a, b):
          return a + b

      def sub(self, a, b):
          return a - b

   if __name__ == '__main__':
      calc = Calc()

test_calc.py
============

Fichier contenant les tests unitaires à effectuer. Utilisation de la bibliothèque `unittest <https://docs.python.org/3/library/unittest.html>`_.
Pour lancer les tests unitaires manuellement :

.. code-block:: console

   python -m unittest test_calc

xmlPythonClass.py
=================

.. automodule:: xmlPythonClass
   :members:
   :undoc-members:
