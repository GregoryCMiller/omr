from setuptools import setup

setup(
    name = "omr",
    version = "0.0.7",
    author = "Greg Miller",
    author_email = "gmill002@gmail.com",
    description = "Bubble Vision: Optical Mark Reader",
    long_description = open('README.rst').read(),
    url = "http://github.com/GregoryCMiller/omr", 
    packages = [
      "omr", 
      "test_omr"
      ],
    package_dir = {
      "omr": "omr", 
      "test_omr": "test_omr"
      },
    scripts = ["omr/omrcmd.py", ],     
    package_data = {'': ['forms.yaml'], },    
    install_requires = [
      "numpy >= 1.8.0",
      "pillow >= 2.2.1",
      "openpyxl >= 1.6.2",
      "PyYAML >= 3.10",],
    classifiers=[
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 2.7',
      #'Programming Language :: Python :: 3',
      #'Programming Language :: Python :: 3.3',
      'Topic :: Scientific/Engineering :: Image Recognition',
      'Topic :: Education :: Testing',
      ],
    platform = 'any',
)
