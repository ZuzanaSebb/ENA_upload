import pandas as pd 
from ._types_and_formats import ENAMetadataSamplesFormat, ENAMetadataStudyFormat, ENASubmissionReceiptFormat
from ..plugin_setup import plugin
import qiime2


def _meta_fmt_to_metadata(ff):
    with ff.open() as fh:
        df = pd.read_csv(fh, sep='\t', header=0, index_col=0, dtype='str')
        return qiime2.Metadata(df)


@plugin.register_transformer
def _1(ff: ENAMetadataStudyFormat) -> (dict):
    with ff.open() as fh:
        df_dict = pd.read_csv(fh,header= None, index_col=0, delimiter='\t' ).squeeze("columns").to_dict() 
        return df_dict     


@plugin.register_transformer
def _2(ff: ENAMetadataSamplesFormat) -> (pd.DataFrame):
    with ff.open() as fh:
        df = pd.read_csv(fh,header= 0, index= False, delimiter='\t' )
        return df   
    
@plugin.register_transformer
def _3(ff: ENAMetadataSamplesFormat) ->  (qiime2.Metadata):
    return  _meta_fmt_to_metadata(ff)  

@plugin.register_transformer
def _4(data: str) ->  (ENASubmissionReceiptFormat):
    ff = ENASubmissionReceiptFormat()
    with ff.open() as fh:
        fh.write(data)
    return ff