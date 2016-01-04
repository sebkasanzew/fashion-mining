#!/usr/bin/env python

from distutils.core import setup

# TODO: complete the setup file
setup(
    name='fashing',
    version='0.1',
    url='https://cgmgit.beuth-hochschule.de/zalando-text-mining/fashion-mining/',
    description='fashion mining application',
    author='Benjamin Fischer, Raul Vinh Khoa Nguyen, Sebastian Kasanzew, Sebastian Krawczyk',
    author_email='...@..., ...@..., sebkasanzew@gmail.com, ...@...',
    install_requires=['gensim>=0.12.2',
                      'nltk>=2.0',
                      'lxml>=3.5.0',
                      'texttable>=0.8.4'
                      ],
    packages=["fashing"]
)
