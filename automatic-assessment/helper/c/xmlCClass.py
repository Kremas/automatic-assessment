#!/usr/bin/python3
# coding : utf-8

from lxml import etree
import re


class C(object):
    '''
    Classe permettant de convertir le XML généré via l'interface en fichier de
    test CUNIT

    :param xml_path:
        Chemin vers le fichier XML à convertir en test CUnit
    :type xml_path str
    :param classname:
        Nom de la classe à tester
    :type classname: str
    :ivar c_header:
        Chemin vers le header
    :ivar header:
        String comportant le header (début) du fichier C
    :ivar main:
        String comportant le main du fichier C
    :ivar footer:
        String comportant le footer (fin) du fichier C
    :ivar case_functions:
        String comportant les fonctions de test, qui se placent entre le header
        et le main
    :ivar add_suite:
        String comportant les ajouts des tests à l'ensemble de tests, permettant
        de faire lancer les tests. Cette String se place après la String 'main'
    :ivar root:
        Objet etree comportant le XML à parser
    :ivar compilation:
        Objet etree comportant le noeud de la ligne de compilation
    :ivar func:
        Dictionnaire comportant une liste de dictionnaires de liste. Exemple:

        {'add': [{'add(1,2)': ['3', '2']}],
        'concat': [{'concat("aaa","bbb")': ["aaabbb", '2']}],
        'divide': [{'divide(7,2)': ['3.5', '2']}, {'divide(7,1)': ['1': '2']}]}

        add:
            {'add(1,2)': ['3', '2']},
        concat:
            {'concat("aaa","bbb")': ["aaabbb", '2']},
        divide:
            {'divide(7,2)': ['3.5', '2']},

            {'divide(7,1)': ['1': '2']}

        Il y a un appel à la fonction 'add', avec (1,2) en paramètres, le
        résultat attendu est '3' et le test vaut 2 points.

        Il y a deux appels à 'divide', le premier avec comme paramètres (7,2),
        résultat attendu '3.5' pour '2' points. Deuxième appel avec comme
        paramètres (7,1), résultat attendu '1', pour '2' points.

    '''

    def __init__(self, xml, classname, path='.'):

        c_header = 'myapp' + "/" + classname + '.h'
        self.classname = classname
        self.header = ("#include <stdio.h>\n"
                       "#include <math.h>\n"
                       "#include \"CUnit/CUnit.h\"\n"
                       "#include \"CUnit/Basic.h\"\n"
                       "#include \"" + c_header + "\"\n"
                       "\n"
                       "// required : libcunit1 libcunit1-doc libcunit1-dev\n"
                       "\n"
                       "/* Test fonctions init de suite et cleanup */\n"
                       "int init_suite(void) { return 0; }\n"
                       "int clean_suite(void) { return 0; }\n"
                       "\n"
                       "/* Fonctions de test */\n"
                       "\n")
        self.main = ("\n/* main */\n"
                     "\n"
                     "int main (int argc, char **argv) {\n\n"
                     "    CU_pSuite pSuite = NULL;\n"
                     "\n"
                     "    /* Initialisation du registre de CUnit */\n"
                     "    if (CUE_SUCCESS != CU_initialize_registry())\n"
                     "        return CU_get_error();\n"
                     "\n"
                     "    /* Ajout de l'ensemble de tests au registre */\n"
                     "    pSuite = CU_add_suite( \"test_suite\", init_suite, clean_suite );\n"
                     "    if (NULL == pSuite) {\n"
                     "        // Si probleme : Nettoyage du registre et return\n"
                     "        CU_cleanup_registry();\n"
                     "        return CU_get_error();\n"
                     "    }\n"
                     "\n"
                     "    /* Ajout des tests a l'ensemble de tests */\n"
                     )

        self.footer = ("\n"
                       "    /* Execution des tests avec l'interface basique */\n"
                       "    CU_basic_set_mode(CU_BRM_VERBOSE);\n"
                       "    CU_basic_run_tests();\n"
                       "    CU_basic_show_failures(CU_get_failure_list());\n"
                       "\n"
                       "    /* Nettoyage du registre et return */\n"
                       "    CU_cleanup_registry();\n"
                       "    return CU_get_error();\n"
                       "} // Fin du main"
                       )
        self.case_functions = ""
        self.add_suite = ""
        self.root = xml
        self.compilation = self.root.find('compilation')
        self.func = {}

    def is_int(self, s):
        '''
        Vérifie si la String passée en paramètre est un nombre entier

        :param s:
            String à tester
        :type s: str
        :return: True si s est entier, False sinon
        :rtype: boolean

        '''
        try:
            int(s)
            return True
        except ValueError:
            return False


    def is_float(self, s):
        '''
        Vérifie si la String passée en paramètre est un nombre décimal

        :param s:
            String à tester
        :type s: str
        :return: True si s est décimal, False sinon
        :rtype: boolean

        '''
        if(re.match("^\d+?\.\d+?$", s) is None):
            return False
        else:
            return True

    def convert(self):
        '''
        Conversion du fichier xml en programme de test C
        '''
        for child in self.root:
            if(child.tag == "test"):
                if(child[0].text == "assert"):
                    func = (child[1].text).split('(')[0]
                    if func not in self.func:
                        self.func[func] = []
                    self.func[func].append({child[1].text: [child[2].text,
                                                            child[3].text]})
        # Génération des fonctions de test
        for elem in self.func:
            self.case_functions += "void " + elem + "_test(void) {\n"
            for x in self.func[elem]:
                for key, value in x.items():
                    if "\"" in value[0]:
                        self.case_functions += "    CU_ASSERT_STRING_EQUAL(" + key + ", " + value[0] + ");\n"
                    else:
                        if(self.is_int(value[0])):
                            self.case_functions += "    CU_ASSERT_EQUAL(" + key + ", " + value[0] + ");\n"
                        elif(self.is_float(value[0])):
                            self.case_functions += "    CU_ASSERT_DOUBLE_EQUAL(" + key + ", " + value[0] + ", 0.001);\n"
                        else:
                            print("Error : result must be one of the following types : string, int, float")
                            exit(-1)
            self.case_functions += "}\n"
        # Ajout des tests à l'ensemble
        i = 0
        for elem in self.func:
            i += 1
            # Si on a qu'un seul test
            if(len(self.func) == 1):
                self.add_suite += "    if ((NULL == CU_add_test(pSuite, \""
                + elem + "_test\", " + elem + "_test))\n"
            else:  # sinon
                # si on est sur le premier test
                if(i == 1):
                    self.add_suite += "    if ((NULL == CU_add_test(pSuite, \"" + elem + "_test\", " + elem + "_test)) ||\n"
                # sinon si c'est ni le premier ni le dernier test
                elif(i < (len(self.func))):
                    self.add_suite += "        (NULL == CU_add_test(pSuite, \"" + elem + "_test\", " + elem + "_test)) ||\n"
                # sinon c'est le dernier test
                else:
                    self.add_suite += "        (NULL == CU_add_test(pSuite, \"" + elem + "_test\", " + elem + "_test))\n"

        self.add_suite += ("       )\n"
                           "    {\n"
                           "        // Si probleme : Nettoyage du registre et return\n"
                           "        CU_cleanup_registry();\n"
                           "        return CU_get_error();\n"
                           "    }\n"
                           )

    def toString(self):
        '''
        Assemble les différentes String en une seule, composant le fichier
        C final

        :return: La String complète dans laquelle est le fichier C
        :rtype: str

        '''
        return self.header + self.case_functions + self.main + self.add_suite + self.footer

    def toFile(self, path='.'):
        '''
        Écrit la string fans un fichier

        :param path:
            Chemin où écrire la String
        :type path: str

        '''
        with open(path + '/' + self.classname + '_test.c', 'w') as f:
            f.write(self.toString())


if __name__ == '__main__':
    obj = C('../xml/test.xml', 'calc')
    obj.convert()
    #print(obj.toString())
    obj.toFile()
