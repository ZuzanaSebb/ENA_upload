from xml.etree.ElementTree import Element, SubElement

class Sample_Attribute:
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
                 alias=None,
                 center_name="",
                  ):
        self.alias = alias
        self.center_name = center_name
        self.features = {}



    def add_title(self, title):
        self.features['TITLE'] = title

    def add_description(self, description):
        self.features['DESCRIPTION'] = description

    def add_sample_name(self, taxon_id=None, scientific_name=None, common_name=None):
        self.features['SAMPLE_NAME'] = {
            'TAXON_ID': taxon_id,
            'SCIENTIFIC_NAME': scientific_name,
            'COMMON_NAME': common_name
        }

    def add_sample_link(self, link):
        self.features['LINK'] = link
    

    def add_attribute(self, attribute):
        if 'SAMPLE_ATTRIBUTES' not in self.features:
            self.features['SAMPLE_ATTRIBUTES'] = []
        
        self.features['SAMPLE_ATTRIBUTES'].append(attribute)
        

    def to_xml_element(self):
        sample_element = Element('SAMPLE', {'alias': self.alias, 'center_name' : self.center_name})
        for key, value in self.features.items():
            if isinstance(value, dict):
                name_element = SubElement(sample_element, key)
                for sub_key, sub_value in value.items():
                    SubElement(name_element, sub_key).text = str(sub_value)
            elif isinstance(value, list):
                links_element = SubElement(sample_element, key)
                for attribute in value:
                        sample_att = attribute.to_xml_element()
                        links_element.append(sample_att)
                
            else:
                SubElement(sample_element, key).text = str(value)
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


