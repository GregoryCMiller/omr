#Copyright (C) 2013 Greg Miller <gmill002@gmail.com>
"""process a group of test images contained in a directory"""
import glob
import itertools
import os
from os.path import abspath, basename, dirname, join
import re
import shutil
import numpy as num
import openpyxl, openpyxl.drawing

from omr.exam import star_process_exam

def Main(frontdir, form, backdir=None, pool=None):
    """Main command line application.
    
    - process front side
    - (optional) process and join back side 
    - write output
    
    """
    
    images, choices = process_exam_group(frontdir, form, 'front', pool)
    
    if backdir:
        backimages, backchoices = process_exam_group(backdir, form, 'back', pool)
        choices = num.hstack((choices, backchoices))
            
    write_exam_group(images, choices, os.path.join(frontdir,'OMR'))


def process_exam_group(testdir, formstr, side, pool=None, outname='OMR'):
    """Process all test images in a directory returning image path list and 
    choice matrix. 
    
    - find .jpg images, sort in place by first 2 numeric blocks
    - Create output directory in input test image dir.  
    - Run each test (possibly in parallel). 
    
    Parameters::
        
        testdir  input folder containing test images 
        formstr  string identifying form in FORMS dictionary
        side     test side (front, back)
        pool     parallel processing pool 
        outname  name of output folder created in testdir
        
    """
    images = glob.glob(join(abspath(testdir), '*.jpg'))
    images.sort(key=lambda x: float(".".join(re.findall('[0-9]+', basename(x))[:2])))
    if not images:
        raise StandardError('at least one image is required')
    
    outdir = join(abspath(testdir), outname)
    shutil.rmtree(outdir, ignore_errors=True)
    [os.makedirs(join(outdir, s)) for s in ['', 'validation', 'names']]
    
    args = [[im, formstr, side] for im in images]
    if pool:
        choice_list = pool.map(star_process_exam, args, chunksize=1)
    else:
        choice_list = map(star_process_exam, args)
    
    return images, num.vstack(choice_list)

def write_exam_group(images, choices, outdir, csv=False, xls=True):
    """Write exam group output
    
    - Score tests using first image as the key.  
    - Count choice frequency by question. 
    - Write csv and xlsx data files 
    
    Parameters::
        
        images   list of image paths 
        choices  matrix of choices with tests in rows
        outdir   output path 
        csv      write csv output tables 
        xls      write xls workbook output 
    
    """
    key = num.array(choices[0])   # key is the first test
    key[key == -1] = -2           # -2 key allows -1 tests to score 0
    scoring = choices == key      # score the tests
    total_score = num.sum(scoring, axis=1)
    
    counts_header = ['Question', 'Key', 'CorrectCount', 
                     'None(-1)', 'A(0)', 'B(1)', 'C(2)', 'D(3)', 'E(4)']
                     
    counts = num.zeros((choices.shape[1], 9))
    counts[:, 0] = 1 + num.arange(choices.shape[1])    # question
    counts[:, 1] = choices[0, :]                       # key
    counts[:, 2] = num.sum(scoring[1:, :], axis=0)     # correct count by question (ex key)
    for i in range(counts.shape[0]):                   # choice frequencies by question
        counts[i, 3:9], x = num.histogram(choices[1:, i], bins=range(-1, 6))
    
    name_files = glob.glob(join(outdir, 'names', "*"))
        
    if csv:
        num.savetxt(join(outdir, 'imagefiles.csv'), map(basename, images), fmt='%s')     
        num.savetxt(join(outdir, 'choices.csv'), choices, fmt='%i', delimiter=',')        
        num.savetxt(join(outdir, 'scoring.csv'), scoring, fmt='%i', delimiter=',')
        num.savetxt(join(outdir, 'questioninfo.csv'), counts, fmt='%i', delimiter=',', 
                    header=",".join(counts_header))

    if xls:
        wb = openpyxl.Workbook()
        wb = write_xls_images(wb, name_files, total_score, 'summary')
        wb = write_xls_array(wb, counts, 'question info', counts_header, width=6)
        wb = write_xls_array(wb, scoring.astype('i'), 'scoring', width=3)
        wb = write_xls_array(wb, choices, 'choices', width=3)    
        wb.save(join(outdir, 'results.xlsx'))
    
    
def write_xls_array(workbook, inarray, title=None, header=None, row=0, col=0, width=None, height=None):
    """write input array to a new sheet in input xlsx workbook
    
    Parameters::
        
        workbook  (openpyxl) xlsx workbook     
        inarray   input array 
        title     name of sheet 
        header    header as list of strings 
        row       starting row 
        col       starting column
        width     row width
        height    row height
    
    """
    ws = workbook.create_sheet()
    
    if title:
        ws.title = title    
    
    if header:
        [setattr(ws.cell(row=row, column=col+j), 'value', h) for j, h in enumerate(header)]
        row += 1
            
    for i,j in itertools.product(*map(range, inarray.shape)):
        setattr(ws.cell(row=row+i, column=col+j), 'value', str(inarray[i, j]))
    
    if width:
        if not hasattr(width, '__iter__'):
            width = itertools.repeat(width)
    
        for w, a in zip(width, sorted(ws.column_dimensions.keys())):
            setattr(ws.column_dimensions[a], 'width', w)
    
    if height:
        for k in ws.row_dimensions.keys():
            setattr(ws.row_dimensions[k], 'height', height)
    
    return workbook

def write_xls_images(workbook, name_images, scores, title=None, header=['Info', 'Score', 'File'], 
                     height=23, width=[47, 5, 20], scale=[0.65, 0.65]):
    """write xlsx file containing a table of extracted info box images,
    score, and file name for each test"""
    ws = workbook.get_active_sheet()
    if title:
        ws.title = title
    
    if header:
        [setattr(ws.cell(row=0, column=j), 'value', h) for j, h in enumerate(header)]
        
    for row, (score, name_file) in enumerate(zip(scores, name_images)):
        ws.cell(row=row+1, column=1).value = score
        ws.cell(row=row+1, column=2).value = basename(name_file)
    
    if width:
        for w, a in zip(width, sorted(ws.column_dimensions.keys())):
            setattr(ws.column_dimensions[a], 'width', w)
    
    if height:
        for k in ws.row_dimensions.keys():
            setattr(ws.row_dimensions[k], 'height', height)
    
    if name_images:
        try: 
            size = openpyxl.drawing.Image(name_images[0]).image.size * num.array(scale)
            for r, im in enumerate(name_images):
                img = openpyxl.drawing.Image(im, size=size)
                img.anchor(ws.cell(row=r+1, column=0))
                ws.add_image(img)
        except:
            setattr(ws.cell(row=1, column=0), 'value', 'ERROR: Info images could not be loaded')
    else:
        setattr(ws.cell(row=1, column=0), 'value', 'ERROR: Info images not found')
    
    return workbook
    