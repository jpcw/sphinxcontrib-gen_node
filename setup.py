# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os


version = '0.2.dev0'

here = os.path.abspath(os.path.dirname(__file__))

def read_file(*pathes):
    path = os.path.join(here, *pathes)
    if os.path.isfile(path):
        with open(path, 'r') as desc_file:
            return desc_file.read()
    else:
        return ''

desc_files = (('README.rst',), ('docs', 'CHANGES.rst'),
              ('docs', 'CONTRIBUTORS.rst'))

long_description = '\n\n'.join([read_file(*pathes) for pathes in desc_files])
requires = ['Sphinx>=0.6']

setup(
    name='sphinxcontrib-gen_node',
    version=version,
    download_url='http://pypi.python.org/pypi/sphinxcontrib-gen_node',
    license='BSD',
    author='Jean-Philippe Camguilhem',
    author_email='jean-philippe.camguilhem__at__makina-corpus.com',
    description='Sphinx generic nodes "todo like" extension',
    long_description=long_description,
    url='https://github.com/jpcw/sphinxcontrib-gen_node',
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir = {'': 'src'},
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)
