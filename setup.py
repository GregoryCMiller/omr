import sys

if sys.version_info < (2, 7):
    raise Exception("Python >= 2.7 is required.")

from setuptools import setup

setup(
    name = "omr",
    version = "0.0.4a",
    author = "Greg Miller",
    author_email = "gmill002@gmail.com",
    description = ("Bubble Vision: Optical Mark Reader"),
    long_description = open('README.rst').read(),
    url = "http://github.com/GregoryCMiller/omr", 
    packages = ["omr", "test_omr"],
    package_dir = {"omr": "omr", 
                   "test_omr": "test_omr"},    
    scripts = ["bin/omrcmd.py", ], 
    install_requires = ["numpy >= 1.8.0", 
                        "pillow >= 2.2.1",
                        "openpyxl >= 1.6.2"],
)
