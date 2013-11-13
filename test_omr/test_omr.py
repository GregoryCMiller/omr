#!/sr/bin/python
#Copyright (C) 2013 Greg Miller <gmill002@gmail.com>
"""optical mark reader test suite

run via nosetests called from package root.

"""
import os
from os.path import dirname, join, exists 
import random
import shutil
import unittest

import numpy as num
import omr

PACKAGE_ROOT = dirname(dirname(__file__))    # package root
TEST_DATA = join(PACKAGE_ROOT, 'test_data')  # testing data folder
TEST_TEMP = join(PACKAGE_ROOT, 'test_tmp')   # temporary test output folder

class temp_data(unittest.TestCase):
    """create temp dir with required source image files"""
    @classmethod  
    def setUpClass(self):        
        """setup test fixture attributes (inherited by all tests)"""
        rand_hex_str = '%030x' % random.randrange(16**30)
        self.path = join(TEST_TEMP, rand_hex_str)       # temp test dir
        self.outdir = join(self.path, 'OMR')            # output dir
        self.names = join(self.outdir, 'names')         # 
        self.validate = join(self.outdir, 'validation') #
        self.imfile = join(self.path, 'Image (0).jpg')  # single image
        self.form = omr.exam.FORMS['882E']['front']     # form
        
        shutil.copytree(TEST_DATA, self.path)           # copy test data tp temp dir

class test_exam_group(temp_data):
    """exam group tests"""
    @classmethod  
    def setUpClass(self):
        """setup exam group test fixture"""
        super(test_exam_group, self).setUpClass()
        
        self.images, self.choices = omr.exam.exam_group(self.path, self.form)
        
    def test_outpath_exists(self):
        """exam group: output directories created"""
        self.assertTrue(exists(self.outdir))
                
    def test_validation_images_exist(self):
        """exam group: all validation images written"""
        self.assertTrue(exists(self.names))
        files = os.listdir(join(self.outdir, 'validation'))
        self.assertEqual(len(files), len(self.images))
    
    def test_name_images_exist(self):
        """exam group: all name images written"""
        self.assertTrue(exists(self.validate))
        files = os.listdir(join(self.outdir, 'names'))
        self.assertEqual(len(files), len(self.images))

class test_write_exam_group(test_exam_group):
    """write exam group tests"""
    @classmethod  
    def setUpClass(self):
        """setup write exam group test fixture"""
        super(test_write_exam_group, self).setUpClass()
        
        omr.exam.write_exam_group(self.images, self.choices, self.outdir)
    
    def test_output_files(self):
        """exam group: output files exist"""
        self.assertTrue(exists(join(self.outdir, 'results.xlsx')))
    
class test_single_exam(temp_data):
    """single exam tests"""
    @classmethod  
    def setUpClass(self):
        """setup single exam test fixture"""
        super(test_single_exam, self).setUpClass()
        os.makedirs(self.validate)
        os.makedirs(self.names)

        self.choices = omr.exam.process_exam(self.imfile, self.form())

    def test_outpath_exists(self):
        """single exam: mock output directories created"""
        self.assertTrue(exists(self.outdir))
        self.assertTrue(exists(join(self.outdir, 'names')))    
        self.assertTrue(exists(join(self.outdir, 'validation')))
    
    def test_choice(self):
        """single exam: choices exist"""
        self.assertTrue(len(self.choices) > 0)
        
        
class test_form(unittest.TestCase):
    """form tests"""
    def setUp(self):
        """setup form test fixture"""
        self.form = omr.exam.FORMS['882E']['front']()

    def test_coords(self):
        """form: all coordinates are integers"""
        for d in self.form.coords.flatten():
            self.assertTrue(num.issubdtype(d, int))

    def test_set_offset(self):
        """form: offsets update"""
        off = [2, 2]
        self.form.set_offset(*off)
        self.assertItemsEqual(self.form.offset, off)


if __name__ == '__main__':
    unittest.main()
