#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# @Time         : 2018/12/22 23:31
# @email        : spirit_az@foxmail.com
# @fileName     : GUIImport.py
__author__ = 'ChenLiang.Miao'

# --+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+--#
import re
import pymel.core as pm

# --+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+--#
maya_qt_ver = int(re.match('\d', pm.about(qt=True)).group())


# --+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+--#
if maya_qt_ver == 4:
    try:
        from PyQt4.QtGui import *
        from PyQt4.QtCore import *
        from PyQt4 import uic
        import sip
        from PyQt4.QtCore import pyqtSignal as signal
        USE_PYQT_MODULE = True
    except ImportError:
        from PySide.QtCore import *
        from PySide.QtGui import *
        import shiboken
        from PySide.QtCore import Signal as signal
        import pysideuic as uic
        USE_PYQT_MODULE = False


if maya_qt_ver == 5:
    try:
        from PyQt5.QtGui import *
        from PyQt5.QtCore import *
        from PyQt5.QtWidgets import *
        from PyQt5 import uic
        # from PyQt5 import sip
        import sip
        from PyQt5.QtCore import pyqtSignal as signal
        import shiboken2 as shiboken
        USE_PYQT_MODULE = True
    except ImportError:
        from PySide2.QtCore import *
        from PySide2.QtGui import *
        from PySide2.QtWidgets import *
        import shiboken2 as shiboken
        from PySide2.QtCore import Signal as signal
        import pyside2uic as uic
        USE_PYQT_MODULE = False


