# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains the gen_node Sphinx extension.

.. add description here ..
'''

requires = ['Sphinx>=0.6']

setup(
    name='sphinxcontrib-gen_node',
    version='0.1',
    url='http://bitbucket.org/birkenfeld/sphinx-contrib',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-gen_node',
    license='BSD',
    author='Jean-Philippe Camguilhem',
    author_email='jean-philippe.camguilhem__at__makina-corpus.com',
    description='Sphinx generic nodes "todo like" extension',
    long_description=long_desc,
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
