from qiime2.plugin import Plugin
from qiime2.plugin import Str
from q2_types.ordination import PCoAResults

plugin = Plugin(
    name='ena_uploader',
    version=0.11,
    website='https://github.com/TBD',
    package='ena_uploader',
    description=('testing_function'),
    short_description='Test.',
)

def test_func():
    print('Halooo')

plugin.methods.register_function(
    function=test_func,
    inputs={},
    parameters={
    },
    outputs=[('test',PCoAResults)],
    input_descriptions={},
    parameter_descriptions={
    },
    output_descriptions={
        'test':'halo'
    },
    name='test ',
    description=(
        'testing.'
    ),
    citations=[]
)

