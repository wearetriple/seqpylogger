#! /bin/bash

rm -rf dist
python setup.py sdist
twine upload dist/*
git tag `cat .version`
git push origin --tags