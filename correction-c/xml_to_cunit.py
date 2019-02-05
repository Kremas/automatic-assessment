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

from lxml.builder import E
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

# ouverture du fichier XML
with open('../xml/test.xml', 'r') as myfile:
    xml=myfile.read().replace('\n', '')

liste = []

# parse du fichier XML
root = etree.fromstring(xml)

# Recupération des balises <test>
for child in root:
    if(child.tag == "test"):
        liste.append(child)

# Création du dictionnaire
# format :
#
# fonction1 
# {'fonction1(...)' : [result, points]}
# {'fonction1(...)' : [result, points]}
# fonction2
# {'fonction2(...)' : [result, points]}
# {'fonction2(...)' : [result, points]}
# {'fonction2(...)' : [result, points]}
# C'est donc un dictionnaire de listes qui contiennent chacune un dictionnaire

dico = {}
for child in root:
    if(child.tag == "test"):
        if(child[0].text == "assert"):
            func = (child[1].text).split('(')[0]
            if func not in dico:
                dico[func] = []
            dico[func].append({child[1].text : [child[2].text, child[3].text]})

# Affichage du dictionnaire
# Exemple :
#    add
#    {'add(1,2)': ['3', '2']}
#    {'add(-5,2)': ['-3', '2']}
#    sub
#    {'sub(3,4)': ['-1', '2']}
"""
for x in dico:
    print(x)
    for y in dico[x]:
        print(y)
        for z, v in y.items():
            print(z, v)
"""
print(len(dico))
for x in dico:
    print(x)
# Retrouver nom du fichier C via l'import de code
c_header = "calc.h"

# Génération du header
header =  ("#include <stdio.h>\n"
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
           "\n"
          )

# Génération des fonctions de test
case_functions =""
for elem in dico:
    case_functions += "void " + elem + "_test(void) {\n"
    for x in dico[elem]:
        for key, value in x.items():
            print(value[0])
            if "\"" in value[0]:
                case_functions += "    CU_ASSERT_STRING_EQUAL(" + key + ", " + value[0] + ");\n"
            else:
                if(is_int(value[0])):
                    case_functions += "    CU_ASSERT_EQUAL(" + key + ", " + value[0] + ");\n"
                elif(is_float(value[0])):
                    case_functions += "    CU_ASSERT_DOUBLE_EQUAL(" + key + ", " + value[0] + ", 0.001);\n"
                else:
                    print("Error : result must be one of the following types : string, int, float")
                    exit(-1)
    case_functions += "}\n"

# Création du main
main = ("\n/* main */\n"
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

# Ajout des tests à l'ensemble
i = 0
add_suite = ""
for elem in dico:
    i += 1
    # Si on a qu'un seul test
    if(len(dico) == 1):
        add_suite += "    if ((NULL == CU_add_test(pSuite, \""+elem+"_test\", "+elem+"_test))\n"
    else: #sinon
        # si on est sur le premier test
        if(i == 1):
            add_suite += "    if ((NULL == CU_add_test(pSuite, \""+elem+"_test\", "+elem+"_test)) ||\n"
        # sinon si c'est ni le premier ni le dernier test
        elif(i < (len(dico))):
            add_suite += "        (NULL == CU_add_test(pSuite, \""+elem+"_test\", "+elem+"_test)) ||\n"
        # sinon c'est le dernier test
        else:
            add_suite += "        (NULL == CU_add_test(pSuite, \""+elem+"_test\", "+elem+"_test))\n"
            
add_suite += ("       )\n"
              "    {\n"
              "        // Si probleme : Nettoyage du registre et return\n"
              "        CU_cleanup_registry();\n"
              "        return CU_get_error();\n"
              "    }\n"
             )
# Création de la fin du main
footer = ("\n"
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

output_string = header + case_functions + main + add_suite + footer
print(output_string)

with open("calc_test.c", "w") as output:
    print("{}".format(output_string), file=output)

exit(0)
