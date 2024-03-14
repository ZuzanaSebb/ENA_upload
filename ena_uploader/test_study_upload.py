import requests
from ena_uploader.study_submission import Study,StudySet
from xml.etree.ElementTree import ElementTree

study_set = StudySet()

project1 = Study(alias="MT51761")
project1.add_title("human gastric microbiota, mucosal")



study_set.add_study(project1)

test_xml = study_set.to_xml_element()
tree = ElementTree(test_xml)

tree.write("study_set.xml", encoding="utf-8", xml_declaration=True)


url = "https://wwwdev.ebi.ac.uk/ena/submit/drop-box/submit/"
files = {
    'SUBMISSION': ('submission.xml',open('submission.xml','rb')),
    'PROJECT': ('study_set.xml',open('study_set.xml','rb'))
}
auth = ('Webin-66822', 'Quaternion07!')

response = requests.post(url, files=files, auth=auth)

print(response.text)