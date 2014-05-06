START /MIN epydoc.py --config DocConfig.py

python omr\omrcmd.py --help

nosetests -v

python omr\omrcmd.py

RMDIR test_omr\test_tmp /Q /S
RMDIR test_omr\test_data\OMR /Q /S
RMDIR build /Q /S
RMDIR dist /Q /S
PAUSE
