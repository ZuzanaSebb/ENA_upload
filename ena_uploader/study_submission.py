from xml.etree.ElementTree import Element, SubElement

class Study_link:
    def __init__(self, db, id):
        self.db = db
        self.id = id        
    
    def to_xml_element(self):
        link_element = Element('PROJECT_LINK')

        xref_element = SubElement(link_element, "XREF_LINK")

        db_element = SubElement(xref_element,"DB")
        db_element.text = self.db

        id_element = SubElement(xref_element,"ID")
        id_element.text = self.id

        return link_element

class Study:
    def __init__(self,
                 alias=None
                  ):
        self.alias = alias
        self.features = {}

    def add_name(self, name):
        self.features['NAME'] = name
    def add_title(self, title):
        self.features['TITLE'] = title
    def add_description(self, description):
        self.features['DESCRIPTION'] = description
    def add_links(self, link):
        if 'PROJECT_LINKS' not in self.features:
            self.features['PROJECT_LINKS'] = []
        self.features['PROJECT_LINKS'].append(link)
        

    def to_xml_element(self):
        study_element = Element('PROJECT', {'alias': self.alias})
        for key, value in self.features.items():
            if isinstance(value, list):
                links_element = SubElement(study_element, key)
                for link in value:
                        study_link = link.to_xml_element()
                        links_element.append(study_link)
                
            else:
                SubElement(study_element, key).text = str(value)
        return study_element


class StudySet:
    def __init__(self):
        self.studies = []

    def add_study(self, study):
        self.studies.append(study)

    def to_xml_element(self):
        study_set_element = Element('PROJECT_SET')
        for study in self.studies:
            study_element = study.to_xml_element()
            study_set_element.append(study_element)
        return study_set_element


