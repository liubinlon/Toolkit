#!/user/bin/env python
# -*- coding: utf-8 -*-
# Author: Zhenbao Liu
# QQ: 3305510092
# Time: 2021/07/25 16:56:30

'''
File_name: playbast_ui.py
plase enter description
'''

try:
    from PySide import QtGui as QtWidgets
    from PySide import QtCore
    from PySide import QtGui 
except:
    from PySide2 import QtWidgets as QtWidgets
    from PySide2 import QtCore
    from PySide2 import QtGui 

import maya.cmds as cmds
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
import os, sys


script_path = os.path.split(r'C:\\Users\\liubi\\Documents\\maya\\scripts\\MayaDev\\MyToolsDemo\\myPlugin\\scripts\\playblast_tool\\scripts\\playblast_tool.py')[0]
# script_path = os.path.dirname(os.path.realpath(__file__))

Dir = r"{0}".format(script_path)
if Dir not in sys.path:
    sys.path.append(Dir)
    
import playblast_tool
reload(playblast_tool)

from FU import uiLoader

window_name = "PlaybastTool_V001"


def get_maya_window():
    maya_main = omui.MQtUtil_mainWindow()
    ptr = wrapInstance(long(maya_main), QtWidgets.QMainWindow)
    return ptr

class PlaybastUI(QtWidgets.QMainWindow):   
    def __init__(self, parent=get_maya_window()):
        super(PlaybastUI, self).__init__(parent)
        self.setObjectName(window_name)
        self.setWindowTitle(window_name)
        self.cls_playblast = playblast_tool.Playblast()
        self.init_ui()
        mainlayout = QtWidgets.QGridLayout()
        mainlayout.addWidget(self.mainWidget)
        mainlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mainlayout)
        self.setCentralWidget(self.mainWidget)
        QtCore.QMetaObject.connectSlotsByName(mainlayout)
    #Set ui 
    def init_ui(self):
        # path = os.path.split(os.path.dirname(__file__))[0]
        uiFile = (r'{}\\playblast_tool.ui'.format(Dir))
        self.mainWidget = uiLoader(uiFile)
        btn_selected = self.mainWidget.findChild(QtWidgets.QPushButton, "btn_selected")
        btn_selected.clicked.connect(self.cls_playblast.selected_file)
        
        btn_open = self.mainWidget.findChild(QtWidgets.QPushButton, "btn_open")
        btn_open.clicked.connect(self.cls_playblast.open_save_path)
        
        btn_playblast = self.mainWidget.findChild(QtWidgets.QPushButton, "btn_playblast")
        btn_playblast.clicked.connect(self.cls_playblast.run_playblast)
        
        self.cls_playblast.let_ainfile = self.mainWidget.findChild(QtWidgets.QLineEdit, "let_ainfile")
        self.cls_playblast.let_ainfile.setText(self.cls_playblast.getfilename(full_path=True))
        self.cls_playblast.let_playfile = self.mainWidget.findChild(QtWidgets.QLineEdit, "let_playfile")
        self.cls_playblast.let_playfile.setText(self.cls_playblast.setup_filename())
        self.cls_playblast.let_start = self.mainWidget.findChild(QtWidgets.QLineEdit, "let_start")
        self.cls_playblast.let_start.setText(self.cls_playblast.get_timeslider_data()[0])
        self.cls_playblast.let_end = self.mainWidget.findChild(QtWidgets.QLineEdit, "let_end")
        self.cls_playblast.let_end.setText(self.cls_playblast.get_timeslider_data()[1])
        self.cls_playblast.let_height = self.mainWidget.findChild(QtWidgets.QLineEdit, "let_height")
        self.cls_playblast.let_width = self.mainWidget.findChild(QtWidgets.QLineEdit, "let_width")
        self.cls_playblast.let_suffix = self.mainWidget.findChild(QtWidgets.QLineEdit, "let_suffix")
        
def showUI(window_name):
    if cmds.window(window_name, query=True, exists=True):
        cmds.deleteUI(window_name)
    if cmds.windowPref(window_name, query=True, exists=True):
        cmds.windowPref(window_name, remove=True)
     
if __name__ == "__main__":
    showUI(window_name)
    win = PlaybastUI()
    win.show()