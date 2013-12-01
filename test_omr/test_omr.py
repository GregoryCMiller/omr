#!/usr/bin/python
#Copyright (C) 2013 Greg Miller <gmill002@gmail.com>
"""optical mark reader test suite

run via nosetests called from package root.

"""
from pathlib import Path
from random import randrange
from shutil import copytree
from unittest import TestCase

from omr.exam_group import process_exam_group, write_exam_group
from omr.exam import process_exam, Form
from omr.forms import FORMS
 
PACKAGE_ROOT = Path(str(__file__)).parent(2)    # package root
TEST_DATA = PACKAGE_ROOT['test_data']  # testing data folder
TEST_TEMP = PACKAGE_ROOT['test_tmp']   # temporary test output folder

class OmrTestCase(TestCase):
    """create temp dir with required source image files"""
    @classmethod  
    def setUpClass(self):        
        """setup test fixture attributes (inherited by all tests)"""
        rand_hex_str = '{}030x'.format(randrange(16**30))
        self.path = TEST_TEMP[rand_hex_str]       # temp test dir
        self.outdir = self.path['OMR']            # output dir
        self.imfile = self.path['Image (0).jpg']  # single image
        self.form = '882E'
        self.side = 'front'
        self.formcfg = FORMS['882E']['front']
        
        copytree(str(TEST_DATA), str(self.path))           # copy test data tp temp dir

class mock_exam_group(OmrTestCase):
    """setup exam group conditions to test single exam processing"""
    @classmethod  
    def setUpClass(self):
        """setup exam group conditions to test single exam processing"""
        super(mock_exam_group, self).setUpClass()
        [x.mkdir() for x in [self.outdir, self.outdir['validation'], self.outdir['names']]]
        
    def test_outpath_exists(self):
        """single exam: mock output directories created"""
        self.assertTrue(self.outdir.exists())
        self.assertTrue(self.outdir['names'].exists())    
        self.assertTrue(self.outdir['validation'].exists())


class test_single_exam(mock_exam_group):
    """single exam tests"""
    @classmethod  
    def setUpClass(self):
        """setup single exam test fixture"""
        super(test_single_exam, self).setUpClass()
        
        self.choices = process_exam(self.imfile, self.formcfg)

    def test_choice(self):
        """single exam: choices exist"""
        self.assertTrue(len(self.choices) > 0)
        
class test_exam_group(OmrTestCase):
    """exam group tests"""
    @classmethod  
    def setUpClass(self):
        """setup exam group test fixture"""
        super(test_exam_group, self).setUpClass()
        
        self.images, self.choices, self.outdir = process_exam_group(self.path, self.form, self.side)
        
    def test_outpath_exists(self):
        """exam group: output directories created"""
        self.assertTrue(self.outdir.exists())
        self.assertTrue(self.outdir['validation'].exists())
        self.assertTrue(self.outdir['names'].exists())
                
    def test_validation_images_exist(self):
        """exam group: all validation images written"""
        val_images = list(self.outdir['validation'].glob('*'))
        self.assertEqual(len(self.images), len(val_images))
    
    def test_name_images_exist(self):
        """exam group: all name images written"""
        name_images = list(self.outdir['names'].glob('*'))
        self.assertEqual(len(self.images), len(name_images)) 

class test_write_exam_group(test_exam_group):
    """write exam group tests"""
    @classmethod  
    def setUpClass(self):
        """setup write exam group test fixture"""
        super(test_write_exam_group, self).setUpClass()
        
        write_exam_group(self.images, self.choices, self.outdir)
    
    def test_output_files(self):
        """exam group: output files exist"""
        self.assertTrue(self.outdir['results.xlsx'].exists())
