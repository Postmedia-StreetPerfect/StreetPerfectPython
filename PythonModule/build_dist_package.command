#!/bin/sh
cd "${0%/*}"

rm -r dist

# bmiller oct 2021
# build a source or wheel distro, wheel is always better
# python setup.py sdist
python3 setup.py bdist_wheel

echo You can install the package using PIP: pip install streetperfect-11.0.0-py3-none-any.whl
