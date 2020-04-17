#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name="seqpylogger",
    version='1.0.0',
    description="logging seqhandler for python",
    author="Triple",
    packages=["seqpylogger"],
    install_requires=["requests"],
    include_package_data=True,
    url = 'https://github.com/wearetriple/seqpylogger',
    download_url = 'https://github.com/wearetriple/seqpylogger/archive/1.0.0.tar.gz',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: System :: Logging',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ]
)