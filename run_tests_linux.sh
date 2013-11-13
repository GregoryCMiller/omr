#!/bin/bash

# check module can import by trying help interface 
python omr/exam.py --help

#doc tests
python -m doctest omr/exam.py -v

# run the unit tests
rm -rf test_tmp
nosetests -v test_omr/test_omr.py
rm -rf test_tmp

# run as gui
rm -rf test_data/OMR
python omr/exam.py
rm -rf test_data/OMR




