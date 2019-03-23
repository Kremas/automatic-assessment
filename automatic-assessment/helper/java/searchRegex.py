#!/usr/bin/python3
# coding : utf8

import re
import sys
from lxml import etree


class Motif(object):
    def __init__(self, xml, class_name):
        self.class_name = class_name
        self.root = xml
        self.motif = {}

        for elem in self.root:
            if(elem.tag == 'test'):
                if(elem.find('type').text == 'motif'):
                    self.motif[elem.find('motif').text] = elem.find('points').text

    def search(self):
        java_file = open(self.class_name, 'r')
        filetext = java_file.read()
        java_file.close()
        res = {}
        for key, value in self.motif.items():
            if re.search(key, filetext):
                print(re.search(key, filetext))
                print(value)
                print('Hbbbbbbbbbbbbbb')
                res[key] = value
            else:
                res[key] = 0
        return (res)


if __name__ == '__main__':
    if(len(sys.argv) != 3 or '.xml' not in sys.argv[2]):
        print('Usage : ./searchRegex.py maClasse.java xml_root_object')
        exit()
    obj = Motif(sys.argv[2], sys.argv[1])
    print(obj.search())
