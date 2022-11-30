@echo off
%~d0
cd %~p0

del /Q/S "dist\*.*"
del /Q/S "build\*.*"
:: bmiller oct 2021
:: build a source or wheel distro, wheel is always better
::python setup.py sdist
python setup.py bdist_wheel

echo You can install the package using PIP: pip install streetperfect-12.0.0-py3-none-any.whl
pause