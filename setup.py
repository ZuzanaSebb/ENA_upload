from setuptools import setup, find_packages
import versioneer

setup(
    name="ena_uploader",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
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