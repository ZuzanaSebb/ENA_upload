import pandas as pd 
from ._types_and_formats import ENAMetadataSamplesFormat, ENAMetadataStudyFormat, ENASubmissionReceiptFormat
from ..plugin_setup import plugin
import qiime2



def _samples_fmt_to_metadata(ff):
    with ff.open() as fh:
        df = pd.read_csv(fh, sep='\t')
        df = df.rename(columns={'alias':'id'}).set_index('id')
        return qiime2.Metadata(df)

def study_fmt_to_metadata(ff):
    with ff.open() as fh:
        df = pd.read_csv(fh,header= None, index_col=0, delimiter='\t')
        df = df.T.rename(columns={'alias':'id'}).set_index('id')
        return qiime2.Metadata(df)


@plugin.register_transformer
def _1(ff: ENAMetadataSamplesFormat) -> (pd.DataFrame):
    with ff.open() as fh:
        df = pd.read_csv(fh, delimiter='\t' )
        return df   


@plugin.register_transformer
def _2(ff: ENAMetadataStudyFormat) -> (dict):
    with ff.open() as fh:
        df_dict = pd.read_csv(fh,header= None, index_col=0, delimiter='\t' ).squeeze("columns").to_dict() 
        return df_dict     


@plugin.register_transformer
def _3(data: bytes) ->  (ENASubmissionReceiptFormat):
    ff = ENASubmissionReceiptFormat()
    with ff.open() as fh:
        fh.write(data)
    return ff

@plugin.register_transformer
def _4(ff: ENAMetadataSamplesFormat) -> (qiime2.Metadata):
    return _samples_fmt_to_metadata(ff)

@plugin.register_transformer
def _5(ff:ENAMetadataStudyFormat) -> (qiime2.Metadata):
    return study_fmt_to_metadata(ff)

