import sys

PyVersion = sys.version_info[0]
if(PyVersion == 3):
    from mtor.scripts.mtor3 import mainwindow as mtor
else:
    from mtor.scripts.mtor2 import mainwindow as mtor

mtor.MainWindows()
