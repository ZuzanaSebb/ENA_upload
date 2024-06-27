import unittest
import qiime2
import pandas as pd
import xml.etree.ElementTree as ET


from qiime2.plugin import ValidationError
from qiime2.plugin.testing import TestPluginBase

from ena_uploader.types import (
    ENAMetadataSamples, ENAMetadataSamplesFormat, ENAMetadataStudy,ENAMetadataStudyFormat,
    ENAMetadataSamplesDirFmt,ENAMetadataStudyDirFmt,
    ENASubmissionReceipt,ENASubmissionReceiptDirFmt,ENASubmissionReceiptFormat
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
    def test_ena_submission_receipt_semantic_type_registration(self):
        self.assertRegisteredSemanticType(ENASubmissionReceipt)

    def test_ena_submission_receipt_to_format_registration(self):
        self.assertSemanticTypeRegisteredToFormat(
            ENASubmissionReceipt,ENASubmissionReceiptDirFmt
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
    
    def test_ena_study_missing_attributes(self):
      meta_path = self.get_data_path('ena_study_missing_att.tsv')
      format = ENAMetadataStudyFormat(meta_path,mode='r')
      with self.assertRaisesRegex(
          ValidationError,
          'Some required study attributes are missing from the metadata upload file: '
          'alias,title.'
      ):
           format.validate()
    
    def test_ena_study_missing_values(self):
        meta_path = self.get_data_path('ena_study_missing_values.tsv')
        format = ENAMetadataStudyFormat(meta_path,mode='r')
        with self.assertRaisesRegex(
            ValidationError,
            "The study is missing values in the following fields: "
            'alias,title.'
        ):
           format.validate()
    
    def test_valid_xml_receipt(self):
        meta_path = self.get_data_path('ena_submission_receipt.xml')
        format = ENASubmissionReceiptFormat(meta_path, mode = 'r')
        format.validate()



    def test_valid_xml_receipt_broken_xml(self):
        meta_path = self.get_data_path('ena_submission_missing_values.xml')
        format = ENASubmissionReceiptFormat(meta_path, mode = 'r')
        with self.assertRaisesRegex(
            ValidationError,
            "Xml response is missing values in the following fields: "
            'receiptDate,submissionFile.'
        ):
            format.validate()



class  TestTransformers(TestPluginBase):
    package = 'ena_uploader.types.tests'
    
    def setUp(self):
        super().setUp()
        xml_path = self.get_data_path('ena_submission_receipt.xml')
        self.xml_response = xml_path
        meta_path1 = self.get_data_path('ena_metadata_samples.tsv')
        meta_path2 = self.get_data_path('ena_metadata_study.tsv')
        self.ena_meta_df = pd.read_csv(meta_path1, sep='\t')
        self.ena_meta_study_df = pd.read_csv(meta_path2, header= None, index_col=0, sep = '\t')
  
    def test_str_ena_receipt(self):
        transformer = self.get_transformer(bytes, ENASubmissionReceiptFormat)
        obs = transformer(self.xml_response.encode('utf-8'))
        self.assertIsInstance(obs, ENASubmissionReceiptFormat)
    
    def test_ena_samples_metadata_to_df(self):
        _, obs = self.transform_format(ENAMetadataSamplesFormat,pd.DataFrame,'ena_metadata_samples.tsv')
        self.assertIsInstance(obs, pd.DataFrame)
        pd.testing.assert_frame_equal(obs,self.ena_meta_df)
    
    def test_ena_study_metadata_to_dict(self):
        _, obs = self.transform_format(ENAMetadataStudyFormat,dict,'ena_metadata_study.tsv')
        self.assertIsInstance(obs, dict)
    
    def test_ena_samples_meta_to_q2_meta(self):
        _, obs = self.transform_format(
            ENAMetadataSamplesFormat, qiime2.Metadata, 'ena_metadata_samples.tsv'
        )
        ena_meta_samples = self.ena_meta_df
        ena_meta_samples = ena_meta_samples.rename(columns={'alias':'id'}).set_index('id')
        exp = qiime2.Metadata(ena_meta_samples)
        self.assertEqual(obs, exp)
    
    def test_ena_study_meta_to_q2_meta(self):
        _, obs = self.transform_format(
            ENAMetadataStudyFormat, qiime2.Metadata, 'ena_metadata_study.tsv'
        )
        ena_meta_study = self.ena_meta_study_df
        ena_meta_study = ena_meta_study.T.rename(columns={'alias':'id'}).set_index('id')
        exp = qiime2.Metadata(ena_meta_study)
        self.assertEqual(obs, exp)








        







if __name__ == "__main__":
    unittest.main()