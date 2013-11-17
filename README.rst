==================================
Bubble Vision: Optical Mark Reader
==================================

Extract answer choices from scanned jpg bubble forms.

Graphical User Interface
------------------------
::
    
    $ exam.py


Command Line
------------
::
    
    $ exam.py imagedir [options]


imagedir           
  Input image directory (front side). Lowest numbered image identifies the key.

`--backdir=BACKDIR`
  Optional back side image directory                                                

`--form=FORM`        
  Set the form string (default and only supported="882E")                       

`--help`             
  Show this help message and exit                                               


Output
------

validation images
    Answer bubble means and reference box fits drawn over each input
    image.
    
results.xlsx
    summary            
        Image path, name box image, and total score for each test.
    
    questioninfo       
        Answer choice counts by question. Key excluded.
    
    scoring            
        Answer choice matches key (0/1). Same indices as choices. Score
        is 0 if key is -1.
    
    choices            
        Answer choice matrix. Tests in rows and questions in columns.
        0-4=A-E, -1=n/a.


Install
-------
::
    
    $ pip install omr
    $ pip install --upgrade omr
    $ pip uninstall omr
    
* Requirements

  * `python <http://www.python.org>`_ 2.7+
  * `pip <http://www.pip-installer.org/en/latest/installing.html>`_ ``$ easy_install pip``

* Dependencies (installed by pip)

  * `numpy 1.8.0 <http://www.numpy.org>`_ numerical array object
  * `pillow 2.2.1 <http://python-imaging.github.io/>`_ image module
  * `openpyxl 1.6.2 <http://openpyxl.readthedocs.org/en/latest/>`_ write xlsx files


Example Validation Image
------------------------

.. image:: https://raw.github.com/GregoryCMiller/omr/master/ExampleValidation.jpg


Troubleshooting
---------------

* Windows 

  * ``$ exam.py --help`` gives ``exam.py: error: too few arguments``
    
    * fix argument passing to "py" file associations from ``python %1`` to ``python %1 %*``
    
  * ``unable to find vcvarsall.bat``
    
    * I was able to use ``$ easy_install Pillow`` when pip failed to install Pillow 2.2.1
    

`api docs <https://raw.github.com/GregoryCMiller/omr/master/doc/index.html>`_

Author
------

Greg Miller gmill002@gmail.com
