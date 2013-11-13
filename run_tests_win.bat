
python omr\exam.py --help

python -m doctest omr\exam.py -v

nosetests -v

python omr\exam.py

RMDIR test_tmp /Q /S
RMDIR test_data\OMR /Q /S
RMDIR build /Q /S
RMDIR dist /Q /S

