import unittest
import pandas as pd
import os
from parameterized import parameterized
import xml.etree.ElementTree as ET
from ena_uploader import _studyFromRawDict

def read_study_tsv_to_dict(filename):
    return pd.read_csv(filename,header= None, index_col=0, delimiter='\t' ).squeeze("columns").to_dict() 

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

    INPUT0 = read_study_tsv_to_dict(fpath("data/minimal_study_structure.tsv"))
    INPUT1 = read_study_tsv_to_dict(fpath("data/study1.tsv"))
    INPUT2 = read_study_tsv_to_dict(fpath("data/study2.tsv"))
    INPUT3 = read_study_tsv_to_dict(fpath("data/study3.tsv"))
    INPUT4 = read_study_tsv_to_dict(fpath("data/study4.tsv"))
    
    expected_res_0 = ET.parse(fpath('data/minimal_study.xml'))
    expected_res_1 = ET.parse(fpath('data/study1.xml'))
    expected_res_2 = ET.parse(fpath('data/study2.xml'))
    expected_res_3 = ET.parse(fpath('data/study3.xml'))
    expected_res_4 = ET.parse(fpath('data/study4.xml'))

    @parameterized.expand([(INPUT0,expected_res_0),
                           (INPUT1,expected_res_1),
                           (INPUT2,expected_res_2),
                           (INPUT3,expected_res_3),
                           (INPUT4,expected_res_4),
                           ])
    def test_xml_structure(self,data,expected_res):
        study =  _studyFromRawDict(data)
        xml  = study.to_xml_element()
        self.assertXmlEqual(xml,expected_res)
    


if __name__ == "__main__":
     unittest.main()