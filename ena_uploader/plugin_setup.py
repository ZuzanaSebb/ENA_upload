from qiime2.plugin import Plugin
from qiime2.plugin import Str
from q2_types.ordination import PCoAResults
from ena_uploader.types._types_and_formats import (
    ENAMetadataSamplesFormat, ENAMetadataSamplesDirFmt,ENAMetadataSamples,
    ENAMetadataStudyFormat, ENAMetadataStudyDirFmt, ENAMetadataStudy
)


plugin = Plugin(
    name='ena_uploader',
    version='1.0',
    website='https://github.com/TBD',
    package='ena_uploader',
    description=('testing_function'),
    short_description='Test.',
)

def test_func():
    print('Halooo')

plugin.register_semantic_types(ENAMetadataStudy,ENAMetadataSamples)

plugin.register_formats(
    ENAMetadataSamplesFormat,ENAMetadataStudyFormat,
    ENAMetadataSamplesDirFmt,ENAMetadataStudyDirFmt)

plugin.register_artifact_class(ENAMetadataStudy,
                               ENAMetadataStudyDirFmt,
                               description = "Study submission tsv file."

)

plugin.register_artifact_class(ENAMetadataSamples,
                               ENAMetadataSamplesDirFmt,
                               description = "Samples submission tsv file."

)

