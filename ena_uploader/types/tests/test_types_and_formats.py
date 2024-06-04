import unittest
import pandas as pd

from qiime2.plugin import ValidationError
from qiime2.plugin.testing import TestPluginBase

from ena_uploader.types import (
    ENAMetadataSamples, ENAMetadataSamplesFormat, ENAMetadataStudy,ENAMetadataStudyFormat,
    ENAMetadataSamplesDirFmt,ENAMetadataStudyDirFmt
)

class TestTypes(TestPluginBase):
    package = 'ena_uploader.types.tests'

    def test_ena_metadata_samples_semantic_type_registration(self):
        self.assertRegisteredSemanticType(ENAMetadataSamples)
    
    def test_ena_metadata_study_semantic_type_registration(self):
        self.assertRegisteredSemanticType(ENAMetadataStudy)
    
    def test_ena_metadata_samples_to_format_registration(self):
        self.assertSemanticTypeRegisteredToFormat(
            ENAMetadataSamples,ENAMetadataSamplesDirFmt
        )
    def test_ena_metadata_study_to_format_registration(self):
        self.assertSemanticTypeRegisteredToFormat(
            ENAMetadataStudy,ENAMetadataStudyDirFmt
        )
class TestFormats(TestPluginBase):
    package = 'ena_uploader.types.tests'

    def test_ena_metadata_samples_fmt(self):
        meta_path = self.get_data_path('ena_metadata_samples.tsv')
        format = ENAMetadataSamplesFormat(meta_path, mode='r')
        format.validate()

    def test_ena_samples_missing_attributes(self):
        meta_path = self.get_data_path('ena_missing_att_samples.tsv')
        format = ENAMetadataSamplesFormat(meta_path,mode='r')
        with self.assertRaisesRegex(
                ValidationError,
                'Some required sample attributes are missing from the metadata upload file: '
                'alias,taxon_id.'

        ):
           format.validate()
    def test_ena_samples_missing_values(self):
        meta_path = self.get_data_path('ena_missing_values_samples.tsv')
        format = ENAMetadataSamplesFormat(meta_path,mode='r')
        with self.assertRaisesRegex(
            ValidationError,
            'Some samples are missing values in the following fields: '
            'alias,taxon_id.'

        ):
            format.validate()


    def test_ena_metadata_study_fmt(self):
        meta_path = self.get_data_path('ena_metadata_study.tsv')
        format = ENAMetadataStudyFormat(meta_path, mode='r')
        format.validate()


class  TestTransformers(TestPluginBase):
    package = 'ena_uploader.types.tests'




if __name__ == "__main__":
    unittest.main()