#!/usr/bin/python3
# coding : utf-8

from lxml import etree
import re


class C(object):
    def __init__(self, xml_path):
        self.root = etree.parse(xml_path).getroot()

    def print_xml(self):
        for child in self.root:
            for elem in child:
                print(elem.tag, elem.text)
            print("")

if __name__ == '__main__':
    obj = C('check_run_conf.xml')
    obj.print_xml()
