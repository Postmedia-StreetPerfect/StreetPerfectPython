#from distutils.core import setup
from setuptools import setup, find_packages

setup(name='StreetPerfect',
	version='12.3.1',
	packages=['StreetPerfect'],
	url='http://www.streetperfect.com/',
	author='Bill Miller',
	author_email='bmiller@postmedia.com',
	license='Copyright © 1993-2024, Postmedia Network Inc',
	description='This package interfaces with the StreetPerfect low level (XPC) API.',
	#long_description=open('README.txt').read(),
	include_package_data=True,
	package_data={	 "": ["*.dll", "*.so"],},
	#install_requires=[],
)
