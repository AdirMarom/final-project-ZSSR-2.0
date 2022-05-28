import os

# fill your ZSSR run path here, train.py full path
ZSSR_RUN_PATH = "/home/dor2/KernalGan-Master/train.py"

CURRENT_FOLER_PATH = os.path.dirname(os.path.realpath(__file__))

#the path of the output of zssr code
ZSSR_RESULTS_PATH = CURRENT_FOLER_PATH + os.sep + 'results'

#boolean that indicate from where you running the code, deafult suppose to be 'False'.
IN_CSE_LABS = False
