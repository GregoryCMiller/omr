from collections import OrderedDict
from os.path import exists
from pkg_resources import resource_string
import yaml

FORMS = OrderedDict()
CFG_FILES = ['default_forms.yaml', 'forms.yaml']

for path in CFG_FILES:
    try:
        FORMS.update(yaml.load(resource_string(__name__, path)))
    except IOError as e:
        print "{} : {}".format(path, e.strerror)
    except yaml.scanner.ScannerError as e:
        print "{} : {}".format(path, "yaml.scanner.ScannerError")
    