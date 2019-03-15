#!/usr/bin/python3
# coding : utf-8

from lxml import etree
from ciscoconfparse import CiscoConfParse
import re


class C(object):
    """ Classe permettant la correction / notation d'une configuration cisco
    """
    def __init__(self, xml_path, conf_path):
        """ Initialisation des attributs de la classe.
        Attributs :
            root   Fichier XML parsé
            conf   Configuration cisco parsée
        """
        self.root = etree.parse(xml_path).getroot()
        self.conf = CiscoConfParse(conf_path, syntax='ios')

    def print_xml(self):
        """ Affiche le contenu de tous les noeuds "tests" du fichier XML
        """
        for child in self.root:
            for elem in child:
                print(elem.tag, elem.text)
            print("")

    def check_misc(self, node):
        """ Vérifie si un motif est présent dans la configuration réseau
        Exemple : 'service password-encryption'
        """
        res = True
        for elem in node:
            if(elem.tag == 'motif'):
                if(len(self.conf.find_objects(elem.text)) == 0):
                   res = False
        return res

    def check_node(self, parent, node):
        """ Vérifie si un/des motif(s) est/sont présent(s) sous un node
        parent
        Exemple :
            parent : 'Interface FastEthernet 0/0'
            motif : 'ip address 172.16.17.1 255.255.255.0'
            Vérifie que l'adresse IP ci-dessus il bien configurée dans
            l'interface fa0/0
        Il est possible de vérifier des configurations d'interface, OSPF,
        IS-IS, EIGRP, RIP, BGP, line
        """
        result = node.find('parent').text
        l_result = []
        for elem in node:
            if(elem.tag == 'motif'):
                l_result.append(self.conf.find_parents_w_child(parent,
                                                               elem.text))
        #print(l_result)
        res = True
        for l in l_result:
            if result not in l:
                res = False
        return res

    def assess(self):
        """ Fait appel aux fonctions de recherches de motifs et note
        l'étudiant en fonctions des points définis dans le formulaire selon la
        présence ou non du motif donné
        """
        points = 0
        for child in self.root:
            for elem in child:
                if(elem.tag == 'type'):
                    if(elem.text == 'misc'):
                        if(self.check_misc(child)):
                            points += int(child.find('points').text)
                    else:
                        if(self.check_node(elem.text, child)):
                            points += int(child.find('points').text)
                    """
                    if(elem.text == 'interface configuration'):
                        if(self.check_node('interface', child)):
                            points += int(child.find('points').text)
                    if(elem.text == 'ospf configuration'):
                        if(self.check_node('router ospf', child)):
                            points += int(child.find('points').text)
                    if(elem.text == 'isis configuration'):
                        if(self.check_node('router isis', child)):
                            points += int(child.find('points').text)
                    if(elem.text == 'eigrp configuration'):
                        if(self.check_node('router eigrp', child)):
                            points += int(child.find('points').text)
                    if(elem.text == 'rip configuration'):
                        if(self.check_node('router rip', child)):
                            points += int(child.find('points').text)
                    if(elem.text == 'bgp configuration'):
                        if(self.check_node('router bgp', child)):
                            points += int(child.find('points').text)
                    if(elem.text == 'line configuration'):
                        if(self.check_node('line', child)):
                            points += int(child.find('points').text)
                    """
        return points

if __name__ == '__main__':
    obj = C('check_run_conf.xml', 'S2.txt')
    obj.print_xml()
    print(obj.assess())
