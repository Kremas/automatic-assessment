from lxml import etree


class Python(object):
    def __init__(self, xml_path, classname):
        self.classname = classname
        self.header = ('import unittest\n'
                       'import ' + self.classname.lower() + ' as ' + classname + 'Class\n'
                       '# run test : python -m unittest test_calc\n'
                       '# with verbose : python -m unittest -v test_calc\n\n')

        self.root = etree.parse(xml_path).getroot()  # Get the XML
        self.main = ('class Test' + classname + '(unittest.TestCase):\n'
                     '    ' + classname.lower() + ' = ' + classname + 'Class.' + classname + '()\n')
        self.footer = ('\n\nif __name__ == "__main__":\n'
                       '    unittest.main(verbosity=2)\n')
        self.func = {}

    def convert(self):
        tests = self.root.findall('test')
        for test in tests:
            if test.find('type').text == 'assert':
                # Get function and split it
                function = test.find('function').text
                function_split = function.split('(')

                # If it's the first time we see the function to test, store it in a dict with a list
                if function_split[0] not in self.func:
                    self.func[function_split[0]] = []

                # Add the tuple ([value to test], result) to the function dict
                self.func[function_split[0]].append((function_split[1].replace(')', ''), test.find('result').text))

        for key, value in self.func.items():
            self.main += '    def test_%s(self):\n' % key
            for val in value:
                self.main += '        self.assertEqual(%s, self.%s.%s(%s));\n\n' % (val[1], self.classname.lower(), key, val[0])

    def toString(self):
        return (self.header + self.main + self.footer)

    def toFile(self, path='.'):
        with open(path + '/' + self.classname.lower() + '_test.py', 'w') as f:
            f.write(self.toString())


if __name__ == '__main__':
    obj = Python('../xml/test.xml', 'Calc')
    obj.convert()
    print(obj.toString())
    obj.toFile()
