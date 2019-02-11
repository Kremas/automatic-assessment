#!/usr/bin/python3
# coding : utf-8

from lxml import etree
from ciscoconfparse import CiscoConfParse
import re


class C(object):
    def __init__(self, xml_path, conf_path):
        self.root = etree.parse(xml_path).getroot()
        self.conf = CiscoConfParse(conf_path, syntax='ios')

    def print_xml(self):
        """prints content of all 'test' nodes in the XML file parsed in
        self.root
        """
        for child in self.root:
            for elem in child:
                print(elem.tag, elem.text)
            print("")

    def check_misc(self, node):
        res = True
        for elem in node:
            if(elem.tag == 'motif'):
                if(len(self.conf.find_objects(elem.text)) == 0):
                   res = False
        return res

    def check_node(self, parent, node):
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
        points = 0
        for child in self.root:
            for elem in child:
                if(elem.tag == 'type'):
                    if(elem.text == 'misc'):
                        if(self.check_misc(child)):
                            points += int(child.find('points').text)
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

        return points

if __name__ == '__main__':
    obj = C('check_run_conf.xml', 'S2.txt')
    obj.print_xml()
    print(obj.assess())
