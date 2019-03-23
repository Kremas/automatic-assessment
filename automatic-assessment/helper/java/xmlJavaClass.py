# javac -cp junit-4.13-beta-1.jar:hamcrest-all-1.3.jar:. MaClasseTest.java TestRunner.java
# java -cp hamcrest-all-1.3.jar:junit-4.13-beta-1.jar:. TestRunner

from lxml import etree


class Java(object):
    '''
    Classe permettant de convertir le XML generé via l'interface en fichier de test JUNIT

    :param xml_path:
        Chemin vers le fichier xml à convertir en JUnit tests
    :type xml_path: str
    :param classname:
        Nom de la classe à tester
    :type classname: str
    :ivar classname:
        Nom de la classe à tester.
        Valeur: classname
    :ivar header:
        String comportant le header du fichier java
    :ivar main:
        String comportant le main de test
    :ivar root:
        Objet etree comportant le XML à parser
    :ivar compilation:
        Objet etree comportant le noeud de la ligne de compilation
    :ivar func:
        Liste comportant les fonctions à tester
    '''

    def __init__(self, xml, classname):
        self.classname = classname
        self.header = 'import org.junit.*; \n\
import static org.junit.Assert.*;\n'
        self.main = 'public class %sTest {\n' % self.classname
        # self.main += '  @BeforeClass\n'
        # self.main += '  public static void before(){\n'
        self.main += '   public static float res = 0;\n'
        self.main += '  @AfterClass\n'
        self.main += '  public static void res(){\n'
        self.main += '    System.out.print("[{\\"total\\":\\"" + res + "\\"},");\n  }\n'
        self.root = xml  # Get the XML
        self.compilation = self.root.find('compilation')
        self.func = {}  # To store the functions to test

    def convert(self):
        '''
        Conversion du fichier xml en classe Java de test
        '''
        # Iterate over the list of tests
        tests = self.root.findall('test')
        points = []
        for test in tests:
            if test.find('type').text == 'assert':
                # Get function and split it
                function = test.find('function').text
                function_split = function.split('(')
                print(function)

                # If it's the first time we see the function to test, store it in a dict with a list
                if function_split[0] not in self.func:
                    self.func[function_split[0]] = []

                # Add the tuple ([value to test], result) to the function dict
                self.func[function_split[0]].append((function_split[1].replace(')', ''), test.find('result').text))
                points.append(test.find('points').text)

        # Construct the asserts
        i = 0
        for key, value in self.func.items():
            self.main += '  @Test\n'
            self.main += '  public void %s() {\n' % key
            for val in value:
                if '"' in val[1]:
                    # String
                    self.main += '    assertEquals("%s(%s)", %s, %s.%s(%s));\n' % (key, val[0].replace('"', ''), val[1], self.classname, key, val[0])
                    self.main += '    res += ' + points[i] + ';'
                else:
                    # Others (double, float, int...)
                    self.main += '    assertEquals("%s(%s)", %s, %s.%s(%s), 0.0001);\n' % (key, val[0], val[1], self.classname, key, val[0])
                    self.main += '    res += ' + points[i] + ';'
                i += 1
            self.main += '  }\n\n'

        self.main += '}\n'

    def toString(self):
        '''
        Convertie l'objet en string
        '''
        return "%s%s" % (self.header, self.main)

    def toFile(self, path='.'):
        '''
        Écrit l'objet dans un fichier

        :param path: Chemin où écrire l'objet
        :type path: str
        '''
        with open(path + '/' + self.classname + 'Test.java', 'w') as f:
            f.write(self.toString())


if __name__ == '__main__':
    obj = Java("maclasse.xml", "MaClasse")
    obj.convert()
    print(obj.toString())
    obj.toFile()
