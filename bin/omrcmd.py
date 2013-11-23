#!/usr/bin/python
#Copyright (C) 2013 Greg Miller <gmill002@gmail.com>
"""Command line application"""
import argparse
import multiprocessing 
import os
import sys
import Tkinter

from omr.forms import FORMS
from omr.exam_group import Main
from omr.gui import Gui

def command_args():
    """parse command line arguments returning namespace object. adds --help option"""
    parser = argparse.ArgumentParser(description=
        "Extract answer choices from scanned jpg bubble forms. ")
    
    parser.add_argument('frontdir', 
                        help="image directory (front). ")
    
    parser.add_argument('-b', '--backdir', 
                        default=None, 
                        help='optional back side image directory')
        
    parser.add_argument('-f', '--form', 
                        default='882E', 
                        choices=FORMS.keys(), 
                        help='set form')
    
    return parser.parse_args()


if __name__ == '__main__':
    # has input args: use command line, else GUI
    if sys.argv[1:]:               
        multiprocessing.log_to_stderr()
        args = command_args()              
        args.pool = multiprocessing.Pool()
    
        Main( **vars(args) )

        args.pool.close()                   
        args.pool.join()

    else:                        
        root = Tkinter.Tk()
        app = Gui(root, cmd=['python', os.path.abspath(__file__)])
        root.update_idletasks()   
        root.mainloop()
        