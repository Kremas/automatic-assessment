#!/usr/bin/python3
# coding : utf-8

"""
Remarques :
 - Ce code créé un fichier 'calc_test.c' qui peut être utilisé pour tester le code C 'calc.c'
   avec la commande 'make' puis './calc_test'. Attention à utiliser un fichier XML valide, généré
   par le formulaire wtform. Ne pas oublier le 'make clean' après le test.
 - Les points à attribuer à chaque réussite de test sont stockés dans le dictionnaire
   mais non utilisés pour le moment.
"""
from lxml import etree
import re


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_float(s):
    if(re.match("^\d+?\.\d+?$", s) is None):
        return False
    else:
        return True


class C(object):
    def __init__(self, xml_path, classname, path='.'):
        c_header = path + "/" + classname + '.h'

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
        self.root = etree.parse(xml_path).getroot()  # Get the XML
        self.compilation = self.root.find('compilation')
        self.func = {}

    def convert(self):
        for child in self.root:
            if(child.tag == "test"):
                if(child[0].text == "assert"):
                    func = (child[1].text).split('(')[0]
                    if func not in self.func:
                        self.func[func] = []
                    self.func[func].append({child[1].text: [child[2].text, child[3].text]})

        # Génération des fonctions de test
        for elem in self.func:
            self.case_functions += "void " + elem + "_test(void) {\n"
            for x in self.func[elem]:
                for key, value in x.items():
                    if "\"" in value[0]:
                        self.case_functions += "    CU_ASSERT_STRING_EQUAL(" + key + ", " + value[0] + ");\n"
                    else:
                        if(is_int(value[0])):
                            self.case_functions += "    CU_ASSERT_EQUAL(" + key + ", " + value[0] + ");\n"
                        elif(is_float(value[0])):
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
                self.add_suite += "    if ((NULL == CU_add_test(pSuite, \"" + elem + "_test\", " + elem + "_test))\n"
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
        return self.header + self.case_functions + self.main + self.add_suite + self.footer

    def toFile(self, path='.'):
        with open(path + '/' + self.classname + '_test.c', 'w') as f:
            f.write(self.toString())


if __name__ == '__main__':
    obj = C('../xml/test.xml', 'calc')
    obj.convert()
    print(obj.toString())
    obj.toFile()
