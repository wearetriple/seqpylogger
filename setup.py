#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="seqpylogger",
    version='1.0.3',
    description="python loghandler for seq",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Triple",
    packages=["seqpylogger"],
    install_requires=["requests"],
    include_package_data=True,
    url = 'https://github.com/wearetriple/seqpylogger',
    download_url = 'https://github.com/wearetriple/seqpylogger/archive/1.0.3.tar.gz',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: System :: Logging',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ]
)