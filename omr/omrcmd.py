#!/usr/bin/python
#Copyright (C) 2013 Greg Miller <gmill002@gmail.com>
"""
Run app with command line arguments.
Run GUI if no arguments are provided.
"""
import argparse
import multiprocessing    
import sys
import Tkinter

from omr.exam_group import Main
from omr.forms import FORMS
from omr.gui import Gui

def parse_args():
    """parse command line arguments."""
    parser = argparse.ArgumentParser(description=
        "Extract answer choices from scanned jpg bubble forms.")
    
    parser.add_argument('frontdir', help="Image directory.")
    
    parser.add_argument('-b', '--backdir', default=None, help=
                        'Optional back side image directory')
        
    parser.add_argument('-f', '--form', default='882E', 
                        choices=sorted(FORMS.keys()), help='Form string')
    
    return parser.parse_args()

if __name__ == '__main__':
    multiprocessing.freeze_support()
        
    if len(sys.argv) > 1:
        multiprocessing.log_to_stderr()
        args = parse_args()
        
        if getattr(sys, 'frozen', False):
            args.pool = None
        else:
            args.pool = multiprocessing.Pool()
        
        Main(**vars(args))
        
        if args.pool:
            args.pool.close()
            args.pool.join()
            
        print 'completed'
    
    else:
        root = Tkinter.Tk()
        app = Gui(root)
        root.update_idletasks()
        root.mainloop()
    