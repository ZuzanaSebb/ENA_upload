import pandas as pd
from xml.etree.ElementTree import ElementTree
import requests
from ena_uploader.sample.sample_submission import SampleSet,Sample, Sample_Attribute



sample_set = SampleSet()

# Example usage:
tsv_file = 'ena_uploader/testing_qiime_metadata.tsv'
df = pd.read_csv(tsv_file, sep='\t')

sample_set = SampleSet()
for row in df.values:
    #var_name = 'sample'+str(i)
    print(row[0])
    #var_name = Sample(alias=row[0])
    #sample_set.add_sample(var_name)
    

test_xml = sample_set.to_xml_element()
tree = ElementTree.tostring(test_xml)

