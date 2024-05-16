import unittest
import pandas as pd
import os
from parameterized import parameterized
import xml.etree.ElementTree as ET
from ena_uploader import _parseSampleSetFromTsv,_sampleSetFromListOfDicts


THIS_DIR = os.path.dirname(os.path.abspath(__file__))

def fpath(fname):
    return os.path.join(THIS_DIR, fname)

def elements_equal(e1, e2):
    if e1.tag != e2.tag: 
        return False
    if e1.text != e2.text: 
        if  e1.text!=None and e2.text!=None :
            return False
    if e1.tail != e2.tail:
        if e1.tail!=None and e2.tail!=None:
            return False
    if e1.attrib != e2.attrib: 
        return False
    if len(e1) != len(e2): 
        return False
    return all(elements_equal(c1, c2) for c1, c2 in zip(e1, e2))

def is_two_xml_equal(tree1, tree2):
    root1 = tree1.getroot()
    root2 = tree2.getroot()
    return elements_equal(root1,root2)


class CustomAssertions:
    def assertXmlEqual(self, xml1,xml2):
        if not is_two_xml_equal(xml1,xml2):
            raise AssertionError('Two xml files are not equal!')


class OptimizationContext_tests(unittest.TestCase,CustomAssertions):

    INPUT1 = _parseSampleSetFromTsv(fpath("data/test_sample1.tsv"))
    INPUT2 = _parseSampleSetFromTsv(fpath("data/test_sample2.tsv"))
    INPUT3 = _parseSampleSetFromTsv(fpath("data/test_sample3.tsv"))
    INPUT4 = _parseSampleSetFromTsv(fpath("data/test_sample4.tsv"))


    exp_res1 = ET.parse(fpath('data/test_sample1.xml'))
    exp_res2 = ET.parse(fpath('data/test_sample2.xml'))
    exp_res3 = ET.parse(fpath('data/test_sample3.xml'))
    exp_res4 = ET.parse(fpath('data/test_sample4.xml'))

    @parameterized.expand([ (INPUT1,exp_res1),
                            (INPUT2,exp_res2),
                            (INPUT3,exp_res3),
                            (INPUT4,exp_res4)
                           ])
    
    def test_xml_structure(self,data,expected_res):
        sample_xml =  _sampleSetFromListOfDicts(data).to_xml_element()
        self.assertXmlEqual(sample_xml,expected_res)


if __name__ == "__main__":
     unittest.main()