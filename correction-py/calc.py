class Calc:

    def add(self, a, b):
        return a + b

    def sub(self, a, b):
        return a - b

    def mul(self, a, b):
        return a * b

    def divide(self, a, b):
        return a / b

    def concat(self, a, b):
        return str(a) + str(b)


if __name__ == '__main__':
    calc = Calc()
