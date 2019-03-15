#!/usr/bin/python3
# coding : utf8

import re
import sys
from lxml import etree


class Motif(object):
    def __init__(self, xml_path, class_name):
        self.class_name = class_name
        self.root = etree.parse(xml_path).getroot()
        self.motif = {}
        for elem in self.root:
            if(elem.tag == 'test'):
                if(elem.find('type').text == 'motif'):
                    self.motif[elem.find('motif').text] = elem.find('points').text

    def search(self):
        java_file = open(self.class_name, 'r')
        filetext = java_file.read()
        java_file.close()
        points_etudiant = 0
        for key, value in self.motif.items():
            if(re.findall(key, filetext)):
                points_etudiant += int(value)
        return points_etudiant


if __name__ == '__main__':
    if(len(sys.argv) != 3 or '.xml' not in sys.argv[2]):
        print('Usage : ./searchRegex.py maClasse.java monFichier.xml')
        exit()
    obj = Motif(sys.argv[2], sys.argv[1])
    print(obj.search())


