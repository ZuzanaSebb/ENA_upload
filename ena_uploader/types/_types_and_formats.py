from qiime2.plugin import SemanticType, TextFileFormat, model, ValidationError
import pandas as pd 

ENAMetadataSamples = SemanticType('ENAMetadataSamples')
ENAMetadataStudy = SemanticType('ENAMetadataStudy')


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


ENAMetadataSamplesDirFmt = model.SingleFileDirectoryFormat(
        'ENAMetadataSamplesDirFmt', 'ena_metadata_samples.tsv', ENAMetadataSamples

)

class ENAMetadataStudyFormat(model.TextFileFormat):
    """"
    This format is utilized to store ENA Study submission metadata, 
    including compulsary attributes such as alias and title,
    along with various other optional attributes for the study submission.
    """

    def _validate(self):
        df_dict = pd.read_csv(str(self), header= None, index_col=0, sep='\t').squeeze("columns").to_dict() 
        if 'alias' not in df_dict.keys():
            raise ValidationError(
                "Study alias must have a value for a study submission."
            )
    
        if 'title' not in df_dict.keys():
            raise ValidationError(
                "Study title must have a value for a study submission."
            )
    def _validate_(self,level):
        self._validate()

ENAMetadataStudyDirFmt = model.SingleFileDirectoryFormat(
    'ENAMetadataStudyDirFmt','ena_metadata_study.tsv',ENAMetadataStudyFormat
)

        