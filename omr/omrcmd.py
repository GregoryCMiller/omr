#!/usr/bin/python
#Copyright (C) 2013 Greg Miller <gmill002@gmail.com>
"""
Run app with command line arguments.
Run GUI if no arguments are provided.
"""
from argparse import ArgumentParser
from sys import argv
from omr.forms import FORMS

def parse_args():
    """parse command line arguments."""
    parser = ArgumentParser(description=
        "Extract answer choices from scanned jpg bubble forms.")
    
    parser.add_argument('frontdir', help="Image directory.")
    
    parser.add_argument('-b', '--backdir', default=None, help=
                        'Optional back side image directory')
        
    parser.add_argument('-f', '--form', default='882E', 
                        choices=sorted(FORMS.keys()), help='Form string')
    
    return parser.parse_args()
    
if __name__ == '__main__':
    if len(argv) > 1:
        from multiprocessing import Pool, log_to_stderr        
        from omr.exam_group import Main

        log_to_stderr()
        args = parse_args()
        args.pool = Pool()
        
        Main(**vars(args))
        
        args.pool.close()
        args.pool.join()
        print 'completed'
    
    else:
        from Tkinter import Tk
        from omr.gui import Gui
    
        root = Tk()
        app = Gui(root)
        root.update_idletasks()
        root.mainloop()
    