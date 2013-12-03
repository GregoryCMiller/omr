from collections import OrderedDict
from os.path import exists
from pkg_resources import resource_filename
import yaml

FILES = ['forms.yaml']
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

def read_form(path):
    data = {}
    try:
        with open(path, 'r') as f:
            d = yaml.load(f)
            if d:
                data = d
        
    except yaml.scanner.ScannerError as e:
        print "{} : {}".format(path, "yaml.scanner.ScannerError")
    
    except:
        print 'unexpected error'
    
    return data


FORMS = OrderedDict(yaml.load(DEFAULT))
files = filter(exists, [resource_filename(__name__, f) for f in FILES])
[FORMS.update(read_form(f)) for f in files]

