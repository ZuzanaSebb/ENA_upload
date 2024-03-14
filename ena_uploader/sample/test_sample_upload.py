import requests
from ena_uploader.sample.sample_submission import SampleSet,Sample, Sample_Attribute
from xml.etree.ElementTree import ElementTree




# Example usage:
sample_set = SampleSet()

sample1 = Sample(alias="PO")
sample1.add_title("human gastric microbiota, mucosal")
#sample1.add_description("Description of sample 1")
sample1.add_sample_name(taxon_id=3, scientific_name="Scientific Name 1", common_name="stomach metagenome")
#sample1.add_sample_link("http://sample1.com")
sample1.add_attribute(Sample_Attribute("geographic location (country and/or sea)","Colombia"))
sample1.add_attribute(Sample_Attribute('collection date','2010'))
sample2 = Sample(alias ='MK' )
sample2.add_title("human gastric microbiota, mucosal")
#sample1.add_description("Description of sample 1")
sample2.add_sample_name(taxon_id=2, scientific_name="Scientific Name 1", common_name="stomach metagenome")
#sample1.add_sample_link("http://sample1.com")
sample2.add_attribute(Sample_Attribute("geographic location (country and/or sea)","Colombia"))
sample2.add_attribute(Sample_Attribute('collection date','2010'))

sample_set.add_sample(sample1)

test_xml = sample_set.to_xml_element()
tree = ElementTree(test_xml)

tree.write("ena_uploader/sample_set.xml", encoding="utf-8", xml_declaration=True)


url = "https://wwwdev.ebi.ac.uk/ena/submit/drop-box/submit/"
files = {
    'SUBMISSION': ('ena_uploader/submission.xml',open('ena_uploader/submission.xml','rb')),
    'SAMPLE': ('ena_uploader/sample_set.xml',open('ena_uploader/sample_set.xml','rb'))
}
auth = ('Webin-66822', 'Quaternion07!')

response = requests.post(url, files=files, auth=auth)

print(response.text)