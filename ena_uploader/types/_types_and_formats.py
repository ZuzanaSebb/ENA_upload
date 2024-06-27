from xml.etree import ElementTree
from qiime2.plugin import SemanticType, TextFileFormat, model, ValidationError
from ena_uploader.sample import _sampleSetFromListOfDicts
from ena_uploader.study import _studyFromRawDict
import xml.etree.ElementTree as ET
import pandas as pd 
import csv

ENAMetadataSamples = SemanticType('ENAMetadataSamples')
ENAMetadataStudy = SemanticType('ENAMetadataStudy')
ENASubmissionReceipt = SemanticType('ENASubmissionReceipt')


class ENAMetadataSamplesFormat(model.TextFileFormat):
    """"
    This format is utilized to store ENA Samples submission metadata, 
    including compulsary attributes such as alias and taxon_id,
    along with various other optional attributes for the samples submission.
    """

    REQUIRED_ATTRIBUTES = ['alias','taxon_id']
    
    def _validate(self):
        df = pd.read_csv(str(self), sep='\t')
        missing_cols = [ x for x in self.REQUIRED_ATTRIBUTES if x not in df.columns]
        if missing_cols:
            raise ValidationError(
                'Some required sample attributes are missing from the metadata upload file: '
                f'{",".join(missing_cols)}.'
                )
        

        nans = (df.isnull() | (df == '')).sum(axis=0)[self.REQUIRED_ATTRIBUTES]
        missing_ids = nans.where(nans > 0).dropna().index.tolist()
        if missing_ids:
            raise ValidationError(
                'Some samples are missing values in the following fields: '
                f'{",".join(missing_ids)}.'
            )

    def _validate_(self, level):
        self._validate()

    def toXml(self):
        with open(str(self), 'r') as f:
            dicts = [d for d in csv.DictReader(f, delimiter='\t')]
            elementTree = _sampleSetFromListOfDicts(dicts).to_xml_element()
            return ElementTree.tostring(elementTree.getroot(), encoding='utf8')


ENAMetadataSamplesDirFmt = model.SingleFileDirectoryFormat(
        'ENAMetadataSamplesDirFmt', 'ena_metadata_samples.tsv', ENAMetadataSamplesFormat

)

def is_valid_value(x):
    return not pd.isnull(x) and len(str(x).strip()) > 0

class ENAMetadataStudyFormat(model.TextFileFormat):
    """"
    This format is utilized to store ENA Study submission metadata, 
    including compulsary attributes such as alias and title,
    along with various other optional attributes for the study submission.
    """
    REQUIRED_ATTRIBUTES = ['alias','title']

    def _validate(self):
        df_dict = pd.read_csv(str(self), header= None, index_col=0, sep='\t').squeeze("columns").to_dict() 
        missing_keys = [x for x in self.REQUIRED_ATTRIBUTES if x not in df_dict.keys()]
        if missing_keys:
            raise ValidationError(
                "Some required study attributes are missing from the metadata upload file: "
                f'{",".join(missing_keys)}.'
                )
        missing_values = [y for y  in self.REQUIRED_ATTRIBUTES if not is_valid_value(df_dict[y]) ]
        if len(missing_values) > 0:
            raise ValidationError(
                "The study is missing values in the following fields: "
                f'{",".join(missing_values)}.'
                )
    
    def toXml(self):
        df_dict = pd.read_csv(str(self), header= None, index_col=0, sep='\t').squeeze("columns").to_dict() 
        elementTree = _studyFromRawDict(df_dict).to_xml_element()
        return ElementTree.tostring(elementTree.getroot(), encoding='utf8')

        
    def _validate_(self,level):
        self._validate()

ENAMetadataStudyDirFmt = model.SingleFileDirectoryFormat(
    'ENAMetadataStudyDirFmt','ena_metadata_study.tsv',ENAMetadataStudyFormat
)

class ENASubmissionReceiptFormat(model.BinaryFileFormat):
    """
    This class provides a structured format to handle and inspect the receipt details
    following a data upload to the ENA.
    The success attribute indicates whether the submission was successful. 
    The receipt also contains the accession numbers of the submitted objects.
    """
    
    @staticmethod
    def readETfromfile(filename):
        with open(filename,'r') as file:
            contents = file.read()
            return ET.fromstring(contents)

    def _validate(self):
        try:
            et = self.readETfromfile(str(self))
        except ET.ParseError:
            raise ValidationError("ENA receipt is not a valid xml form.")
        receipt_element = et
        required_att = ['receiptDate', 'submissionFile', 'success']
        missing_att = [x for x in required_att if x not in receipt_element.attrib ]
        if missing_att:
            raise ValidationError(
                "Xml response is missing values in the following fields: "
                f'{",".join(missing_att)}.'
            )

    def _validate_(self,level):
       return self._validate()

ENASubmissionReceiptDirFmt = model.SingleFileDirectoryFormat(
    'ENASubmissionReceiptDirFmt','ena_submission_receipt.xml',ENASubmissionReceiptFormat
)