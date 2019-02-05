# javac -cp junit-4.13-beta-1.jar:hamcrest-all-1.3.jar:. MaClasseTest.java TestRunner.java
# java -cp hamcrest-all-1.3.jar:junit-4.13-beta-1.jar:. TestRunner

from lxml import etree


class Java(object):
    def __init__(self, xml_path, classname):
        self.classname = classname
        self.header = 'import org.junit.*; \n\
import static org.junit.Assert.*;\n'
        self.main = 'public class %sTest {\n' % self.classname

        self.root = etree.parse(xml_path).getroot()  # Get the XML
        self.compilation = self.root.find('compilation')
        self.func = {}  # To store the functions to test

    def convert(self):
        # Iterate over the list of tests
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

        # Construct the asserts
        for key, value in self.func.items():
            self.main += '  @Test\n'
            self.main += '  public void %s() {\n' % key
            for val in value:
                if '"' in val[1]:
                    # String
                    self.main += '    assertEquals("%s(%s)", %s, %s.%s(%s));\n' % (key, val[0].replace('"', ''), val[1], self.classname, key, val[0])
                else:
                    # Others (double, float, int...)
                    self.main += '    assertEquals("%s(%s)", %s, %s.%s(%s), 0.0001);\n' % (key, val[0], val[1], self.classname, key, val[0])

            self.main += '  }\n\n'

        self.main += '}\n'

    def toString(self):
        return "%s%s" % (self.header, self.main)

    def toFile(self, path='.'):
        with open(path + '/' + self.classname + 'Test.java', 'w') as f:
            f.write(self.toString())


if __name__ == '__main__':
    obj = Java("maclasse.xml", "MaClasse")
    obj.convert()
    print(obj.toString())
    obj.toFile()
