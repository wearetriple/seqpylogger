#! /bin/bash

rm -rf dist
python setup.py sdist
twine upload dist/*
git tag `cat setup.py | awk '/VERSION =/' | awk -F'"' '{ print $2; }'`
git push origin --tags