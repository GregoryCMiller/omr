
python omr\exam.py --help

nosetests -v

epydoc.py --config DocConfig.py > doc\build_result.txt
DEL doc\toc-everything.html
COPY doc\toc-omr.exam-module.html doc\toc-everything.html

python omr\exam.py

RMDIR test_tmp /Q /S
RMDIR test_data\OMR /Q /S
RMDIR build /Q /S
RMDIR dist /Q /S
