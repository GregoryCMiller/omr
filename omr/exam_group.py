#Copyright (C) 2013 Greg Miller <gmill002@gmail.com>
"""process a group of test images contained in a directory"""
from itertools import repeat, product
from re import findall
from shutil import rmtree
from functools import partial

from numpy import array, histogram, hstack, savetxt, sum, vstack, zeros
import openpyxl, openpyxl.drawing
from pathlib import Path

from omr.exam import process_exam
from omr.forms import FORMS

_NUMSORT = lambda x: float(".".join(findall('[0-9]+', x.name)[:2])) 
"""extract the first two numeric blocks of a path as a float"""

def Main(frontdir, form, backdir=None, pool=None):
    """Main command line application. """
    
    fimg, fchoice, fout = process_exam_group(frontdir, form, 'front', pool)    

    if backdir:
        bimg, bchoice, bout = process_exam_group(backdir, form, 'back', pool)
        fchoice = hstack((fchoice, bchoice))
    
    write_exam_group(fimg, fchoice, fout)
    
def process_exam_group(testdir, formstr, side, pool=None):
    """Process all test images in a directory returning image path list and 
    choice matrix. 
    
    - Create output directory in input test image dir.
    - find .jpg images, sort in place by first 2 numeric blocks
    - Run each test (possibly in parallel). 
    
    Parameters::
        
        testdir  input folder containing test images 
        formstr  string identifying form in FORMS dictionary
        side     test side (front, back)
        pool     parallel processing pool 
        
    """
    wd = Path(testdir)['OMR']
    rmtree(str(wd), True)
    [wd[p].mkdir() for p in ['', 'validation', 'names']]
    
    images = sorted(wd.parent().glob('*.jpg'), key=_NUMSORT)
    if not images:
        raise StandardError('at least one image is required')
    
    func = partial(process_exam, formcfg=FORMS[formstr][side])
    if pool:
        choices = pool.map(func, images)
    else:
        choices = map(func, images)
    
    return images, vstack(choices), wd

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
    key = choices[0]              # key is the first test
    key[key == -1] = -2           # -2 key allows -1 tests to score 0
    scoring = choices == key      # score the tests    
    score_by_test = sum(scoring, 1)
    score_by_question = sum(scoring[1:, :], 0)
    
    counts_header = ['Question', 'Key', 'CorrectCount', 
                     'None(-1)', 'A(0)', 'B(1)', 'C(2)', 'D(3)', 'E(4)']
                     
    counts = zeros((choices.shape[1], 9))
    counts[:, 0] = range(1, 1 + choices.shape[1])      # question
    counts[:, 1] = choices[0, :]                       # key
    counts[:, 2] = score_by_question                   # correct count by question (ex key)
    for i in range(counts.shape[0]):                   # choice frequencies by question
        counts[i, 3:9], _x = histogram(choices[1:, i], range(-1, 6))
        
    if csv:
        savetxt(outdir['imagefiles.csv'], [i.name for i in images], fmt='%s')     
        savetxt(outdir['choices.csv'], choices, fmt='%i', delimiter=',')        
        savetxt(outdir['scoring.csv'], scoring, fmt='%i', delimiter=',')
        savetxt(outdir['questioninfo.csv'], counts, fmt='%i', delimiter=',', 
                    header=",".join(counts_header))

    if xls:
        name_files = sorted(outdir['names'].glob('*'), key=_NUMSORT)
    
        wb = openpyxl.Workbook()
        wb = write_xls_images(wb, name_files, score_by_test, 'summary')
        wb = write_xls_array(wb, counts, 'question info', counts_header, width=6)
        wb = write_xls_array(wb, scoring.astype('i'), 'scoring', width=3)
        wb = write_xls_array(wb, choices, 'choices', width=3)    
        wb.save(str(outdir['results.xlsx']))
    
    
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
            
    for i,j in product(*map(range, inarray.shape)):
        setattr(ws.cell(row=row+i, column=col+j), 'value', str(inarray[i, j]))
    
    if width:
        if not hasattr(width, '__iter__'):
            width = repeat(width)
    
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
        ws.cell(row=row+1, column=2).value = name_file.name
    
    if width:
        for w, a in zip(width, sorted(ws.column_dimensions.keys())):
            setattr(ws.column_dimensions[a], 'width', w)
    
    if height:
        for k in ws.row_dimensions.keys():
            setattr(ws.row_dimensions[k], 'height', height)
    
    if name_images:
        try: 
            size = openpyxl.drawing.Image(str(name_images[0])).image.size * array(scale)
            for r, im in enumerate(name_images):
                img = openpyxl.drawing.Image(str(im), size=size)
                img.anchor(ws.cell(row=r+1, column=0))
                ws.add_image(img)
        except:
            setattr(ws.cell(row=1, column=0), 'value', 'ERROR: Info images could not be loaded')
    else:
        setattr(ws.cell(row=1, column=0), 'value', 'ERROR: Info images not found')
    
    return workbook
