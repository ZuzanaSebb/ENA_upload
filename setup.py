from setuptools import setup, find_packages

setup(
    name="ena_uploader",
    version='0.1',
    packages=find_packages(),
    author="Zuzana Sebechlebska",
    author_email="zuzanasebechlebska@gmail.com",
    description="ENA UPLOADER.",
    url="TBD",
    entry_points={
        'qiime2.plugins': ['ena_uploader=ena_uploader.plugin_setup:plugin']
    },
    package_data={
        'ena_uploader.types.tests': ['data/*', 'data/*/*'],
    },
    zip_safe=False,
)