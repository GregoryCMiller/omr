"""forms.py: import built in and user form specifications.


Forms are loaded (and overwritten) in the following order::
  
- Built in 882E form
- "forms.yaml" in the package directory if not executable 
- "*.yaml" in the current directory (if executable)

"""
import sys
import yaml

from collections import OrderedDict
from os.path import exists
from pathlib import Path
from pkg_resources import resource_filename

def read_form(path):
    try:
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    except yaml.YAMLError, e:
        print e

DEFAULT = """
882E:
    front:
        size: [50, 5]
        pos: [258, 130]
        space: [25.2, 49.2]
        bub: [15, 39]
        info: [746, 1234, 408, 575]
        score: [1350, 1395, 360, 405]
        refzone: 
        - [233, 249, 51, 81]
        - [106, 125, 571, 601]
        - [1574, 1592, 570, 600]
        - [1492, 1502, 50, 79]
        expected_dpi: [150, 150]
        expected_size: [1664, 664]
        size_tolerance: [0.04, 0.04]
        ref_rc: [175, 525]
        contrast: 178
        trim_std: 4
        min_ref: 127
        radius: 10
        signal: 1.1

    back:
        size: [50, 5]
        pos: [258, 130]
        space: [25.2, 49.2]
        bub: [15, 39]
        info: [746, 1234, 408, 575]
        score: [1350, 1395, 360, 405]
        refzone: 
        - [233, 249, 51, 81]
        - [106, 125, 571, 601]
        - [1574, 1592, 570, 600]
        - [1492, 1502, 50, 79]
        expected_dpi: [150, 150]
        expected_size: [1664, 664]
        size_tolerance: [0.04, 0.04]
        ref_rc: [175, 525]
        contrast: 178
        trim_std: 4
        min_ref: 127
        radius: 10
        signal: 1.1
        
"""
FORMS = OrderedDict(yaml.safe_load(DEFAULT))
FILES = [resource_filename(__name__, 'forms.yaml'), ]
if getattr(sys,'frozen', False):
    FILES += map(str, Path(sys.executable).parent().glob('*.yaml'))
    
map(FORMS.update, filter(None, map(read_form, filter(exists, FILES))))
