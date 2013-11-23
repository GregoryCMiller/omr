#Copyright (C) 2013 Greg Miller <gmill002@gmail.com>
"""Form specification


Grid parameters specified as [height, width] in pixels.  

================  ===============================================================================
Parameter         Description
================  ===============================================================================
size              h,w size of answer bubble matrix (n questions, n answer choices)
pos               h,w coordinate of answer matrix upper left corner (i0, j0) in pixels
bub               h,w answer bubble surrounding box in pixels (float ok)         
space             h,w unit cell edge lengths in pixels (float ok)
offset            h,w fitted reference offset applied to pos
================  ===============================================================================

::
    
    |
    |        |-bub-|
    |        |---space---|
    |
    |       j0    j1    j2
    |        ___________________
    |    i0 |0                  |  
    |       | [ A ]       [ B ] |  
    |    i1 |      1            |  
    |       |                   |
    |    i2 |            2      |
    |       | [ A ]       [ B ] |
    |       |___________________|
    |


Region rectangles
-----------------

rectangels are specified as [min height, max height, min width, max width] in pixels

================  ==========================================================
Parameter         Description
================  ==========================================================
refzone           list of black reference box rectangles (or None).
info              name info rectangle (or None)
score             machine printed score rectangle (or None)
================  ==========================================================

Image properties 
----------------

================  ====================================================================
Parameter         Description
================  ====================================================================
expected_dpi      h,w image dpi (CRITICAL - relates pixels to distance)
expected_size     h,w expected image size (after conversion to proper dpi) 
size_tolerance    allowed percent error in actual image size 
contrast          black/white contrast split value 0<=x<=255
trim_std          minimum stdev to remove image edge during trimming
radius            reference box fitting search radius in pixels
min_ref           minimum pixel value for black box match 0<=x<=255
ref_x, ref_y      validation image reference fit summary panel coordinates
signal            minimum ratio of darkest to second darkest answer choice    
================  ====================================================================

"""

FORMS = {
    '882E': {
        'front': {
            'size': [50, 5],
            'pos': [258, 130],
            'space': [25.2, 49.2],
            'bub': [15, 39],

            'info': [746, 1234, 408, 575],
            'score': [1350, 1395, 360, 405],
            'refzone': [[233, 249, 51, 81],
                        [106, 125, 571, 601],
                        [1574, 1592, 570, 600],
                        [1492, 1502, 50, 79]],

            'expected_dpi': [150, 150],
            'expected_size': [1664, 664],
            'size_tolerance': [0.04, 0.04],
            'ref_rc': [175, 525],
            'contrast': 178,
            'trim_std': 4,
            'min_ref': 127,
            'radius': 10,
            'signal': 1.1,
        },
        'back': {
            'size': [50, 5],
            'pos': [258, 130],
            'space': [25.2, 49.2],
            'bub': [15, 39],

            'info': [746, 1234, 408, 575],
            'score': [1350, 1395, 360, 405],
            'refzone': [[233, 249, 51, 81],
                        [106, 125, 571, 601],
                        [1574, 1592, 570, 600],
                        [1492, 1502, 50, 79]],

            'expected_dpi': [150, 150],
            'expected_size': [1664, 664],
            'size_tolerance': [0.04, 0.04],
            'ref_rc': [175, 525],
            'contrast': 178,
            'trim_std': 4,
            'min_ref': 127,
            'radius': 10,
            'signal': 1.1,
        },
    },
}
