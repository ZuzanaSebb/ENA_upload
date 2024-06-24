import importlib
from qiime2.plugin import Plugin
from qiime2.plugin import Str, Bool
from q2_types.ordination import PCoAResults
from ena_uploader.types._types_and_formats import (
    ENAMetadataSamplesFormat, ENAMetadataSamplesDirFmt,ENAMetadataSamples,
    ENAMetadataStudyFormat, ENAMetadataStudyDirFmt, ENAMetadataStudy,
    ENASubmissionReceiptFormat,ENASubmissionReceiptDirFmt,ENASubmissionReceipt
)
from ena_uploader.uploader import uploadToEna

plugin = Plugin(
    name='ena_uploader',
    version='1.0',
    website='https://github.com/TBD',
    package='ena_uploader',
    description=('This is a QIIME2 plugin supporting upload of the metadata and raw data files to ENA.'),
    short_description='Plugin for data upload to ENA.',
)


plugin.register_semantic_types(ENAMetadataStudy,ENAMetadataSamples,ENASubmissionReceipt)

plugin.register_formats(
    ENAMetadataSamplesFormat,ENAMetadataStudyFormat,
    ENAMetadataSamplesDirFmt,ENAMetadataStudyDirFmt,
    ENASubmissionReceiptFormat,ENASubmissionReceiptDirFmt)


plugin.register_artifact_class(ENAMetadataStudy,
                               ENAMetadataStudyDirFmt,
                               description = "Study submission tsv file."

)

plugin.register_artifact_class(ENAMetadataSamples,
                               ENAMetadataSamplesDirFmt,
                               description = "Samples submission tsv file."

)

plugin.register_artifact_class(ENASubmissionReceipt,
                               ENASubmissionReceiptDirFmt,
                               description = "ENA submission receipt xml file")

plugin.methods.register_function(
    function=uploadToEna,
    inputs = {
            'study': ENAMetadataStudy,
            'samples': ENAMetadataSamples,
            },
    parameters={
            'submission_hold_date': Str,
            'dev' : Bool
            },
    outputs=[('submission_receipt', ENASubmissionReceipt)],
    
    input_descriptions={
            'study': 'Artifact containing study submission parameters.',
            'samples': 'Artifact containing submission metadata of the samples.',
            },
    parameter_descriptions={
        'submission_hold_date':"TBD",
        'dev' : ('False by default, true in case of submission to ENA dev server.')
    },
    output_descriptions={
        'submission_receipt': 'Artifact containing the submission summary.'
    },
    name='ENA Submission',
    description=("ENA Study and Samples Metadata submission upload."),
    citations=[]
)

importlib.import_module('ena_uploader.types._transformer')