#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from setuptools import find_packages, setup

setup(
    name="seqpylogger",
    version=int(time.time()),
    description="Add seqhandler for python",
    author="Triple",
    packages=find_packages(),
    install_requires=["requests"],
    include_package_data=True,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ]
)