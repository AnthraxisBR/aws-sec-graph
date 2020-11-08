"""
    Install this aws-sec-graph python module
    This module contains all dependencies and instructions to generate a
    installable module
"""
import setuptools
import codecs
import os.path

with open("README.md", "r") as fh:
    long_description = fh.read()


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim: str = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name='aws_sec_graph',
    version=get_version("aws_sec_graph/__init__.py"),
    author="Gabriel Mourão",
    author_email="gabrielmouraodemelo@gmail.com",
    description="A AWS Security graph generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'boto3',
        'packaging'
    ],
    entry_points={
        'console_scripts': ['aws-sec-graph=aws_sec_graph:main'],
    }
)
