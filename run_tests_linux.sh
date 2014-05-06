#!/bin/bash

# build documents
#python epydoc.py --config DocConfig.py

# check module can import by trying help interface 
python omr/omrcmd.py --help 2>&1 | tee test_results.txt

# run the unit tests
rm -rf test_tmp
nosetests -v test_omr/test_omr.py 2>&1 | tee -a test_results.txt
rm -rf test_tmp

# run gui
#rm -rf test_data/OMR
#python omr/omrcmd.py
#rm -rf test_data/OMR
