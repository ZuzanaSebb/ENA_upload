from .sample.sample_submission import SampleSet,Sample,Sample_Attribute
from .study.create_study_from_tsv import _studyFromRawDict
from .sample.create_samples_from_tsv import _sampleSetFromListOfDicts,_parseSampleSetFromTsv
from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions


from . import _version
__version__ = _version.get_versions()['version']
