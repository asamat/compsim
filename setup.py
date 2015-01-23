import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Don't import analytics-python module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'compsim'))

long_description = '''
compsim is a library for matching 2 company names, the algorithm is a combination
of jacard distance, tfidf and levenstein distance
'''

setup(
    name='compsim',
    packages = ['compsim'],
    version= '0.0.3',
    url='https://github.com/asamat/compsim',
    author='Arunim Samat',
    author_email='arunimsamat@gmail.com',
    license='MIT License',
    description='Company Name Similarity Computer',
    long_description=long_description
)