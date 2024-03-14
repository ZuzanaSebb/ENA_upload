import pandas as pd
from xml.etree.ElementTree  import Element, SubElement, tostring
import csv

class SampleAttribute:
    def __init__(self,tag,value):
        self.tag = tag
        self.value = value
    
    def to_xml_element(self):
        sample_element = Element('SAMPLE_ATTRIBUTE')

        tag_element = SubElement(sample_element, "TAG")
        tag_element.text = self.tag

        value_element = SubElement(sample_element,"VALUE")
        value_element.text = self.value 

        return sample_element

class Sample:
    def __init__(self,
                 alias='Hihi',
                 center_name= "Huhu",
                 title = "Hehe",
                 description = None,
                 links = [],
                 taxon_id =None,
                 scientific_name = None,
                 common_name = None,
                 attributes = [] # should contain ENA-CHECKLIST item
                  ):
        self.alias = alias
        self.center_name = center_name
        self.title = title
        self.description = description
        self.taxon_id = taxon_id
        self.scientific_name = scientific_name
        self.common_name = common_name
        self.links = links
        self.attributes = attributes

    def to_xml_element(self):
        sample_element = Element('SAMPLE', {'alias': self.alias, 'center_name' : self.center_name})
        name_element = SubElement(sample_element,"SAMPLE_NAME")
        taxon_element = SubElement(name_element,"TAXON_ID")
        print(self.taxon_id)
        taxon_element.text = self.taxon_id
        if self.scientific_name is not None:
            SubElement(name_element, "SCIENTIFIC_NAME").text = str(self.scientific_name)
        if self.common_name is not None:
            SubElement(name_element, "COMMON_NAME").text = str(self.common_name)
        if self.title is not None:
           SubElement(sample_element, "TITLE").text = str(self.title)
        if self.description is not None:
            SubElement(sample_element, "DESCRIPTION").text = str(self.description)
        if len(self.links) >0:
            links_element = SubElement(sample_element, "SAMPLE_LINKS")
            for link in self.links:
                SubElement(links_element, "SAMPLE_LINK").text = str(link)
        if len(self.attributes) > 0:
            att_elements = SubElement(sample_element, "SAMPLE_ATTRIBUTES")
            for att in self.attributes:
                att_element = att.to_xml_element()
                att_elements.append(att_element)

        
        return sample_element

class SampleSet:
    def __init__(self):
        self.samples = []

    def add_sample(self, sample):
        self.samples.append(sample)

    def to_xml_element(self):
        sample_set_element = Element('SAMPLE_SET')
        for sample in self.samples:
            sample_element = sample.to_xml_element()
            sample_set_element.append(sample_element)
        return sample_set_element

def sampleFromRowDict(rowDict):
    specialAttributes = {"center_name", "title", "description", "links", "taxon_id", "scientific_name", "common_name"}
    kwArgs = {k:v for k,v in rowDict.items() if k in specialAttributes}
    kwArgs['alias'] = rowDict['sample-id']
    kwArgs['taxon_id'] = '42'
    attributes  = [SampleAttribute(k,v) for k,v in rowDict.items() if k not in specialAttributes]
    kwArgs['attributes'] = attributes
    return Sample(**kwArgs)

if __name__ == "__main__":

# Read the csv file with sep = '\t'
#df = pd.read_csv('ena_uploader/sample/test_metadata.tsv', sep='\t')

    filename = 'ena_uploader/sample/test_metadata.tsv'
    c = SampleSet()
    with open(filename, 'r') as f:
        reader_obj = csv.DictReader(f,delimiter="\t")
        for row in reader_obj:
            c.add_sample(sampleFromRowDict(row))
    print(tostring(c.to_xml_element()))

                


        