import sys

if sys.version_info < (2, 7):
    raise Exception("Python >= 2.7 is required.")

from setuptools import setup

import omr
    
setup(
    name = "omr",
    version = omr.__version__,
    author = omr.__author__,
    author_email = omr.__author_email__,
    description = ("Bubble Vision: Optical Mark Reader"),
    long_description = open('README.rst').read(),
    url = omr.__url__, 
    packages = ["omr", "test_omr"],
    package_dir = {"omr": "omr", 
                   "test_omr": "test_omr"},    
    scripts = ["omr/exam.py", ], 
    install_requires = ["numpy >= 1.8.0", 
                        "pillow >= 2.2.1",
                        "openpyxl >= 1.6.2"],
)
