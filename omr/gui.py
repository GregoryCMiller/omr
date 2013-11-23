#Copyright (C) 2013 Greg Miller <gmill002@gmail.com>
"""Graphical user interface""" 
import subprocess
import sys
import Tkinter
from tkFileDialog import askdirectory

from omr.forms import FORMS

class Gui(Tkinter.Frame):
    """GUI to select input args"""
    def __init__(self, master, cmd):
        """initialize frame, create output variables and widgets, verify
        command and get help text"""
        Tkinter.Frame.__init__(self, master, padx=5, pady=5)
        master.wm_title("Bubble Vision:  Optical Mark Reader")
        self.pack()
        
        self.front = Tkinter.StringVar(self)
        Tkinter.Label(self, text="Front Directory").grid(row=0, column=0)
        Tkinter.Button(self, textvar=self.front, command=self.get_front, width=30).grid(row=1, column=0)
        
        self.back = Tkinter.StringVar(self)
        Tkinter.Label(self, text="Back Directory (optional)").grid(row=0, column=1)
        Tkinter.Button(self, textvar=self.back, command=self.get_back, width=30).grid(row=1, column=1)
        
        self.form = Tkinter.StringVar(self)
        Tkinter.Label(self, text='Form').grid(row=0, column=2)
        Tkinter.OptionMenu(self, self.form, *sorted(FORMS.keys())).grid(row=1, column=2)
        if FORMS:
            self.form.set(sorted(FORMS.keys())[0])
        
        self.text = Tkinter.Text(self, height=15, width=80)
        self.text.grid(row=2, columnspan=3, pady=5)
        
        Tkinter.Button(self, text='Quit', command=self.quit, width=8).grid(row=3, column=0, sticky=Tkinter.W)
        Tkinter.Button(self, text='Run', command=self.run_app, width=8).grid(row=3, column=2, sticky=Tkinter.E)
        
        self.cmd = cmd
        try:
            self.run_command(['--help'], see="1.0")
        except:
            self.cmd = []
            self.run_app()
    
    def run_app(self):
        """collect and verify user selected arguments, run main
        application"""
        if not self.cmd:
            self.insert_text('ERROR: No application!\n')
            return None
            
        if not self.front.get():
            self.insert_text('ERROR: Choose front directory!\n')
            return None

        if not self.form.get():
            self.insert_text('ERROR: Choose form!\n')
            return None
            
        args = [self.front.get(), ] 
        args.append('--form={}'.format(self.form.get()))
        if self.back.get():
            args.append('--backdir={}'.format(self.back.get()))
        
        self.run_command(args)
        
    def run_command(self, args, echo=True, output=True, see=Tkinter.END):
        """run the command with input args. Use echo and output to print
        the command and response""" 
        if echo:
            self.insert_text("$ " + " ".join(self.cmd + args) + '\n')
        
        p = subprocess.Popen(self.cmd + args, shell='win' in sys.platform, 
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        if output:
            [self.insert_text(l, see) for l in iter(p.stdout.readline,'')]
            
    def insert_text(self, text, see=Tkinter.END):
        """insert string into gui text box"""
        self.text.config(state=Tkinter.NORMAL)
        self.text.insert(Tkinter.END, text)
        self.text.config(state=Tkinter.DISABLED)
        if see:
            self.text.see(see)

        self.text.update_idletasks()
        
    def get_front(self):
        """open directory selection dialog to set front directory or empty string"""
        self.front.set(askdirectory())

    def get_back(self):
        """open directory selection dialog to set back directory or empty string"""
        self.back.set(askdirectory())
        
        