import unittest
import calc as CalcClass

# run test : python -m unittest test_calc
# with verbose : python -m unittest -v test_calc


class TestCalc(unittest.TestCase):

    calc = CalcClass.Calc()

    def test_add(self):
        self.assertEqual(3, self.calc.add(1, 2))

    def test_sub(self):
        self.assertEqual(-5, self.calc.sub(1, 6))

    def test_divide(self):
        self.assertEqual(2.5, self.calc.div(7.5, 3))


if __name__ == '__main__':
    unittest.main(verbosity=2)
