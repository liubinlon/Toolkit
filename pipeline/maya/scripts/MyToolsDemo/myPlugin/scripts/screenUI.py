# -*- coding: utf-8 -*-
import os
import sys
import inspect

from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtCore import Signal, QThread, Qt
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
#configuration file path

path = os.path.dirname(inspect.getsourcefile(lambda:0))

Dir = r"{0}".format(path)
if Dir not in sys.path:
    sys.path.append(Dir)

from screen import btn




def get_maya_mainwindow():
    mayaPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(mayaPtr), QtWidgets.QWidget)

# def getMayaWindow():
#     mayaPtr = omui.MQtUtil.mainWindow() 
#     mayaWindow = shiboken2.wrapInstance(long(mayaPtr), QMainWindow)
#     return mayaWindow
'''
creat a widget about take screen information display
'''


class Playblast(QtWidgets.QWidget):
    def __init__(self, parent=get_maya_mainwindow()):
        super(Playblast, self).__init__(parent)
        
        self.setWindowTitle(u"playblast-v001")
        self.resize(360, 10)
        self.font = QtGui.QFont()
        self.font.setPointSize(11)
        self.font.setBold(False)
        self.font.setWeight(50)
        self.setFont(self.font)
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

        # Build a widget about renaming files
        self.gbox_name = QtWidgets.QGroupBox("video name")
        self.gridLayout_name = QtWidgets.QGridLayout(self.gbox_name)
        self.gridLayout_name.setObjectName("gridLayout_name")
        self.lbl_name = QtWidgets.QLabel(self.gbox_name)
        self.lbl_name.setObjectName("lbl_name")
        self.ledt_name = QtWidgets.QLineEdit(self.gbox_name)
        self.ledt_name.setObjectName("ledt_name")
        self.gridLayout_name.addWidget(self.lbl_name, 0, 0, 1, 1) 
        self.gridLayout_name.addWidget(self.ledt_name, 0, 1, 1, 1)
        # Build a widget about take screen information display settings
        self.gbox_font = QtWidgets.QGroupBox("font")
        self.gridLayout_font = QtWidgets.QGridLayout(self.gbox_font)
        self.gridLayout_font.setObjectName("gridLayout_font")
        self.lbl_color = QtWidgets.QLabel(self.gbox_font)
        self.lbl_color.setObjectName("lbl_color")   
        self.cbx_color = QtWidgets.QComboBox(self.gbox_font)
        self.cbx_color.setObjectName("cbx_color")
        self.lbl_size = QtWidgets.QLabel(self.gbox_font)
        self.lbl_size.setObjectName("lbl_size")
        self.sbx_size = QtWidgets.QSpinBox(self.gbox_font)
        self.gridLayout_font.addWidget(self.lbl_color, 0, 0, 1, 1)
        self.gridLayout_font.addWidget(self.cbx_color, 0, 1, 1, 1)
        self.gridLayout_font.addWidget(self.lbl_size, 0, 2, 1, 1)
        self.gridLayout_font.addWidget(self.sbx_size, 0, 3, 1, 1)
        # Build a widget about take screen settings
        self.gbox_screen = QtWidgets.QGroupBox("screen settings")
        self.gridLayout_screen = QtWidgets.QGridLayout(self.gbox_screen)
        self.lbl_format = QtWidgets.QLabel(self.gbox_screen)
        self.lbl_format.setObjectName("lbl_format")
        self.cbx_format = QtWidgets.QComboBox(self.gbox_screen)
        self.cbx_format.setObjectName("cbx_format")
        self.lbl_display = QtWidgets.QLabel(self.gbox_screen)
        self.lbl_display.setObjectName("lbl_display")
        self.ledt_width = QtWidgets.QLineEdit(self.gbox_screen)
        self.ledt_width.setObjectName("ledt_width")
        self.ledt_height = QtWidgets.QLineEdit(self.gbox_screen)
        self.ledt_height.setObjectName("ledt_height")
        self.gridLayout_screen.addWidget(self.lbl_format, 0, 0, 1, 1)
        self.gridLayout_screen.addWidget(self.cbx_format, 0, 1, 1, 1)
        self.gridLayout_screen.addWidget(self.lbl_display, 0, 2, 1, 1)
        self.gridLayout_screen.addWidget(self.ledt_width, 0, 3, 1, 1)
        self.gridLayout_screen.addWidget(self.ledt_height, 0, 4, 1, 1)

        # self.widget_location = QtWidgets.QWidget(self.gbox_screen)
        # self.widget_location.setObjectName("widget_location")
        # self.gridLayout_location = QtWidgets.QGridLayout(self.widget_location)
        # self.gridLayout_location.setObjectName("gridLayout_location")
        # self.lbl_location = QtWidgets.QLabel(self.gbox_screen)
        # self.lbl_location.setObjectName("lbl_location")
        # self.rbtn_lowerleft = QtWidgets.QRadioButton(self.gbox_screen)
        # self.rbtn_lowerleft.setObjectName("rbtn_lowerleft")
        # self.rbtn_lowerright = QtWidgets.QRadioButton(self.gbox_screen)
        # self.rbtn_lowerright.setObjectName("rbtn_lowerright")
        # self.rbtn_upperleft = QtWidgets.QRadioButton(self.gbox_screen)
        # self.rbtn_upperleft.setObjectName("rbtn_upperleft") 
        # self.rbtn_upperright = QtWidgets.QRadioButton(self.gbox_screen) 
        # self.rbtn_upperright.setObjectName("rbtn_upperright")
        # self.gridLayout_screen.addWidget(self.lbl_location, 1, 0, 1, 1)
        # self.gridLayout_screen.addWidget(self.rbtn_upperleft, 1, 1, 1, 1)
        # self.gridLayout_screen.addWidget(self.rbtn_upperright, 1, 2, 1, 1)
        # self.gridLayout_screen.addWidget(self.rbtn_lowerleft, 2, 1, 1, 1)
        # self.gridLayout_screen.addWidget(self.rbtn_lowerright, 2, 2, 1, 1)
        # self.gridLayout_screen.addWidget(self.widget_location, 1, 0, 1, 5) 
        
        self.frame_playblast = QtWidgets.QFrame()
        self.frame_playblast.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_playblast.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_playblast.setObjectName("frame_playblast")
        self.gridLayout_playblast = QtWidgets.QGridLayout(self.frame_playblast)
        self.gridLayout_playblast.setObjectName("gridLayout_playblast")
        self.btn_playblast = QtWidgets.QPushButton(self.frame_playblast)
        self.btn_playblast.setObjectName("btn_playblast")
        self.gridLayout_playblast.addWidget(self.btn_playblast, 0, 0, 1, 1)

        self.importclass()
        self.setupUi()
        self.mainlayout = QtWidgets.QVBoxLayout()
        self.mainlayout.addWidget(self.gbox_name)
        self.mainlayout.addWidget(self.gbox_font)
        self.mainlayout.addWidget(self.gbox_screen)
        self.mainlayout.addWidget(self.frame_playblast)
        self.setLayout(self.mainlayout)
    
    def importclass(self):
        self.btn = btn()

    def setupUi(self):
        self.lbl_name.setText("name:")
        self.lbl_color.setText("color:")
        icon_white = QtGui.QIcon(r"{0}/white.png".format(path))
        icon_blue = QtGui.QIcon(r"{0}/blue.png".format(path))
        icon_red = QtGui.QIcon(r"{0}/red.png".format(path))
        icon_yellow = QtGui.QIcon(r"{0}/yellow.png".format(path))
        self.cbx_color.insertItem(0, QtGui.QIcon(r"{0}/white.png".format(path)), "white")
        self.cbx_color.insertItem(1, QtGui.QIcon(r"{0}/blue.png".format(path)), "blue")
        self.cbx_color.insertItem(2, QtGui.QIcon(r"{0}/red.png".format(path)), "red")
        self.cbx_color.insertItem(3, QtGui.QIcon(r"{0}/yellow.png".format(path)), "yellow")

 
        self.lbl_size.setText("size:")
        self.cbx_format.addItems(["qt", "avi", "imge"])
        self.ledt_width.setPlaceholderText("width")
        self.ledt_width.setValidator(QtGui.QIntValidator(0, 99999))
        self.ledt_height.setPlaceholderText("height")
        self.ledt_height.setValidator(QtGui.QIntValidator(0, 99999))
        self.lbl_format.setText("format:")
        self.lbl_display.setText("display size:")
        # self.lbl_location.setText("location:")
        # self.rbtn_upperleft.setText("upperleft")
        # self.rbtn_upperright.setText("upperright")
        # self.rbtn_lowerleft.setText("lowerleft")
        # self.rbtn_lowerright.setText("lowerright")
        # self.rbtn_lowerright.toggle()
        self.btn_playblast.setText("playblast")
        #connect pushbutton 
        self.cbx_color.currentIndexChanged.connect(self.btn.foncolor)
        self.cbx_format.currentIndexChanged.connect(self.btn.setformat)
        self.btn_playblast.clicked.connect(self.btn.playblast)


        
        self.btn.filename = self.ledt_name
        self.btn.fonSizeValue = self.sbx_size
        self.btn.widthValue = self.ledt_width
        self.btn.height = self.ledt_height
        # self.btn.lowerleftValue = self.rbtn_lowerleft
        # self.btn.lowerrightValue = self.rbtn_lowerright
        # self.btn.upperleftValue = self.rbtn_upperleft
        # self.btn.upperrightValue = self.rbtn_upperright
        self.btn.setcbxformat = self.cbx_format
        self.btn.setfoncolor = self.cbx_color


def main():
    win = Playblast()  
    win.show()
    return win

if __name__ == "__main__":
    main()

