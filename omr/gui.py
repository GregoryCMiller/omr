#Copyright (C) 2013 Greg Miller <gmill002@gmail.com>
"""Graphical user interface""" 
from collections import OrderedDict
from pkg_resources import resource_filename
from subprocess import Popen, PIPE, STDOUT
from sys import platform
import Tkinter
from tkFileDialog import askdirectory

from omr.forms import FORMS

class Gui(Tkinter.Frame):
    """GUI to select omr arguments"""
    def __init__(self, master):
        """initialize frame, create variables, create widgets, verify
        command, and insert help text"""
        Tkinter.Frame.__init__(self, master, padx=5, pady=5)
        master.wm_title("Bubble Vision: Optical Mark Reader")
        self.pack()
        
        self.front = Tkinter.StringVar(self)
        self.back = Tkinter.StringVar(self)
        self.form = Tkinter.StringVar(self, value = sorted(FORMS.keys())[0])
        
        self.create_widgets()
        
        self.cmd = ['python', resource_filename(__name__, 'omrcmd.py')]
        try:
            self.call(['--help'], see="1.0")
        except:
            self.cmd = []

        self.prechecks = OrderedDict({
            'self.cmd'        : 'No command line application.\n',
            'self.front.get()': 'Choose front directory.\n',
            'self.form.get()' : 'Choose form.\n',
            })
    
    def create_widgets(self):
        """Create Tkinter widgets"""
        Tkinter.Label(self, text="Front Directory").grid(row=0, column=0)
        Tkinter.Label(self, text="Back Directory (optional)").grid(row=0, column=1)
        Tkinter.Label(self, text='Form').grid(row=0, column=2)
        
        Tkinter.Button(self, textvar=self.front, command=self.get_front, width=30).grid(row=1, column=0)
        Tkinter.Button(self, textvar=self.back, command=self.get_back, width=30).grid(row=1, column=1)        
        Tkinter.OptionMenu(self, self.form, *sorted(FORMS.keys())).grid(row=1, column=2)
        
        self.text = Tkinter.Text(self, height=15, width=80)
        self.text.grid(row=2, columnspan=3, pady=5)
        
        Tkinter.Button(self, text='Quit', command=self.quit, width=8).grid(row=3, column=0, sticky=Tkinter.W)
        Tkinter.Button(self, text='Run', command=self.run_app, width=8).grid(row=3, column=2, sticky=Tkinter.E)
                
    def run_app(self):
        """precheck arguments, run main application"""
        if [self.msg(v) for k, v in self.prechecks.items() if not eval(k)]:
            return None

        args = [self.front.get(), '--form={}'.format(self.form.get())]
        if self.back.get():
            args.append('--backdir={}'.format(self.back.get()))
        
        self.call(args)
        
    def call(self, args, see=Tkinter.END):
        """run the command with input args. Use echo and output to print
        the command and response"""         
        self.msg("$ " + " ".join(self.cmd + args) + '\n')
        p = Popen(self.cmd + args, stdout=PIPE, stderr=STDOUT, shell='win' in platform)        
        [self.msg(l, see) for l in iter(p.stdout.readline,'')]
        
    def msg(self, text, see=Tkinter.END):
        """insert string into gui text box"""
        self.text.config(state=Tkinter.NORMAL)
        self.text.insert(Tkinter.END, text)
        self.text.config(state=Tkinter.DISABLED)
        if see:
            self.text.see(see)

        self.text.update_idletasks()
        
    def get_front(self):
        """open directory selection dialog to set front directory"""
        self.front.set(askdirectory())

    def get_back(self):
        """open directory selection dialog to set back directory"""
        self.back.set(askdirectory())
        