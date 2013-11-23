
python bin\omrcmd.py --help

nosetests -v

epydoc.py --config DocConfig.py > doc\build_result.txt

python omr\omrcmd.py

RMDIR test_tmp /Q /S
RMDIR test_data\OMR /Q /S
RMDIR build /Q /S
RMDIR dist /Q /S
