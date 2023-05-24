# -*- coding: utf-8 -*-
import os
import sys

path = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]

Dir = r"{0}".format(path)
if Dir not in sys.path:
    sys.path.append(Dir)

import PySide2.QtWidgets as QtWidgets
from PySide2 import QtCore, QtGui

from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance

from uiLoader.FU import uiLoader
from jointTool.jointbut import btnjnt
import pymel.core as pm


def getMayaWindow():
    maya_par = omui.MQtUtil_mainWindow()
    maya_window = wrapInstance(long(maya_par), QtWidgets.QMainWindow)
    return maya_window


def get_dock(name="MyTool"):
    delete_dock(name)
    ctrl = pm.workspaceControl(name, dockToMainWindow=("left", 1), label="My Tool")
    qt_ctrl = omui.MQtUtil_findControl(ctrl)
    prt = wrapInstance(long(qt_ctrl), QtWidgets.QMainWindow)
    return prt


def delete_dock(name="MyTool"):
    if pm.workspaceControl(name, query=True, exists=True):
        pm.deleteUI(name)


class myTool(QtWidgets.QWidget):
    
    def __init__(self, dock=True):
        if dock:
            parent = get_dock()
        else:
            delete_dock()
            try:
                pm.deleteUI("mytool")
            except:
                pass
            parent = QtWidgets.QMainWindow(parent=getMayaWindow())
            parent.setObjectName("mytool")
            parent.setWindowTitle("My Tool")
            layout = QtWidgets.QVBoxLayout(parent)
        super(myTool, self).__init__(parent=parent)

        # if parent:
        #     self.setWindowFlags(parent.windowFlags())


        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.resize(450, 600)
        self.iconList = QtWidgets.QListWidget()
        self.initInstance()
        self.initUI()

        mainLayout = QtWidgets.QGridLayout()
        mainLayout.addWidget(self.mainWidget, 0, 0)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mainLayout)
        # mainLayout.addWidget(getMayaWindow())

        self.parent().layout().addWidget(self)
        if not dock:
            parent.show()

    def initInstance(self):
        self.btnjnt = btnjnt()

    def initUI(self):
        path = os.path.split(os.path.dirname(__file__))[0]
        uiFile = (r'{0}/uifile/rigging.ui'.format(path))
        self.mainWidget = uiLoader(uiFile)

        btn_part_old_modle = self.mainWidget.findChild(QtWidgets.QPushButton, "btn_addpartjoints")
        btn_part_old_modle.clicked.connect(self.btnjnt.addpart)

        btn_stretch_old_modle = self.mainWidget.findChild(QtWidgets.QPushButton, "btn_buildstretchrig")
        btn_stretch_old_modle.clicked.connect(self.btnjnt.stretch)

        btn_motion_old_modle = self.mainWidget.findChild(QtWidgets.QPushButton, "btn_buildjoints")
        btn_motion_old_modle.clicked.connect(self.btnjnt.motionJoint)

        btn_fk_old_model = self.mainWidget.findChild(QtWidgets.QPushButton, "btn_fkcontorller")
        btn_fk_old_model.clicked.connect(self.btnjnt.fkContorller)
        #contorller shape
        btn_cube_old_model = self.mainWidget.findChild(QtWidgets.QPushButton, "btn_cubeShape")
        icon_cube = QtGui.QIcon(r"{0}/icons/cube.png". format(path))
        btn_cube_old_model.setIcon(icon_cube)
        btn_cube_old_model.clicked.connect(self.btnjnt.cubeShape)

        btn_ball_old_model = self.mainWidget.findChild(QtWidgets.QPushButton, "btn_ballShape")
        icon_ball = QtGui.QIcon(r"{0}/icons/ball.png".format(path))
        btn_ball_old_model.setIcon(icon_ball)
        btn_ball_old_model.clicked.connect(self.btnjnt.ballShape)


        #contorller color
        btn_blue_old_model = self.mainWidget.findChild(QtWidgets.QPushButton, "btn_blue")
        icon_blue = QtGui.QIcon(r"{0}/icons/blue.png". format(path))
        btn_blue_old_model.setIcon(icon_blue)
        btn_blue_old_model.clicked.connect(self.btnjnt.blue)

        btn_red_old_model = self.mainWidget.findChild(QtWidgets.QPushButton, "btn_red")
        icon_red = QtGui.QIcon(r"{0}/icons/red.png". format(path))
        btn_red_old_model.setIcon(icon_red)
        btn_red_old_model.clicked.connect(self.btnjnt.red)

        btn_yellow_old_model = self.mainWidget.findChild(QtWidgets.QPushButton, "btn_yellow")
        icon_yellow = QtGui.QIcon(r"{0}/icons/yellow.png". format(path))
        btn_yellow_old_model.setIcon(icon_yellow)
        btn_yellow_old_model.clicked.connect(self.btnjnt.yellow)

        btn_skyblue_old_model = self.mainWidget.findChild(QtWidgets.QPushButton, "btn_skyblue")
        icon_skyblue = QtGui.QIcon(r"{0}/icons/skyblue.png". format(path))
        btn_skyblue_old_model.setIcon(icon_skyblue)
        btn_skyblue_old_model.clicked.connect(self.btnjnt.skyblue)

        btn_darkred_old_model = self.mainWidget.findChild(QtWidgets.QPushButton, "btn_darkred")
        icon_darkred = QtGui.QIcon(r"{0}/icons/darkred.png". format(path))
        btn_darkred_old_model.setIcon(icon_darkred)
        btn_darkred_old_model.clicked.connect(self.btnjnt.darkred)

        btn_green_old_model = self.mainWidget.findChild(QtWidgets.QPushButton, "btn_green")
        icon_green = QtGui.QIcon("{0}/icons/green.png". format(path))
        btn_green_old_model.setIcon(icon_green)
        btn_green_old_model.clicked.connect(self.btnjnt.green)

        btn_darkblue_old_model = self.mainWidget.findChild(QtWidgets.QPushButton, "btn_darkblue")
        icon_darkblue = QtGui.QIcon(r"{0}/icons/darkblue.png". format(path))
        btn_darkblue_old_model.setIcon(icon_darkblue)
        btn_darkblue_old_model.clicked.connect(self.btnjnt.darkblue)

        btn_white_old_model = self.mainWidget.findChild(QtWidgets.QPushButton, "btn_white")
        icon_white = QtGui.QIcon(r"{0}/icons/white.png". format(path))
        btn_white_old_model.setIcon(icon_white)
        btn_white_old_model.clicked.connect(self.btnjnt.white)

#adv add attribute
        btn_follow_old_model = self.mainWidget.findChild(QtWidgets.QPushButton, "btn_addFKFollow")
        btn_follow_old_model.clicked.connect(self.btnjnt.addFkFollow)

        btn_tun_old_model = self.mainWidget.findChild(QtWidgets.QPushButton, "btn_importtun")
        btn_tun_old_model.clicked.connect(self.btnjnt.importTun)

        btn_hisfist_old_model = self.mainWidget.findChild(QtWidgets.QPushButton, "btn_addhisfist")
        btn_hisfist_old_model.clicked.connect(self.btnjnt.addHisFist)

        btn_key_old_model = self.mainWidget.findChild(QtWidgets.QPushButton, "btn_key")
        btn_key_old_model.clicked.connect(self.btnjnt.key)

        btn_ttozero_old_model = self.mainWidget.findChild(QtWidgets.QPushButton, "btn_translatetozero")
        btn_ttozero_old_model.clicked.connect(self.btnjnt.translateToZero)

        btn_rtozero_old_model = self.mainWidget.findChild(QtWidgets.QPushButton, "btn_rotatetozero")
        btn_rtozero_old_model.clicked.connect(self.btnjnt.rotateToZero)

        btn_rivetlocator_model = self.mainWidget.findChild(QtWidgets.QPushButton, "btn_RivetLocator")
        btn_rivetlocator_model.clicked.connect(self.btnjnt.jobRivetLocator)

        sld_contorllerScaleValue_old_model = self.mainWidget.findChild(QtWidgets.QPushButton, "btn_contorllersize")
        sld_contorllerScaleValue_old_model.clicked.connect(self.btnjnt.contorllerScale)


        self.btnjnt.contorllerName = self.mainWidget.findChild(QtWidgets.QLineEdit, "le_contorllername")
        self.btnjnt.contorllerScaleValue = self.mainWidget.findChild(QtWidgets.QDoubleSpinBox, "dsb_contorllersize")
        self.btnjnt.addPartValue = self.mainWidget.findChild(QtWidgets.QSpinBox, "sb_part")
        self.btnjnt.stretchJointValue = self.mainWidget.findChild(QtWidgets.QSpinBox, "sb_stretch")
        self.btnjnt.addsineValue = self.mainWidget.findChild(QtWidgets.QCheckBox, "ckx_addsine")
        self.btnjnt.addtensileValue = self.mainWidget.findChild(QtWidgets.QCheckBox, "ckx_addtensile")
        self.btnjnt.modelName = self.mainWidget.findChild(QtWidgets.QLineEdit, "le_name")
        self.btnjnt.addContorller = self.mainWidget.findChild(QtWidgets.QCheckBox, "cbx_addcontorller")

def main():
    global win
    try:
        win.close()
    except:
        pass
    win = myTool()
    win.show()
    return win
    # if __name__ == "__main__":
    #     ui = myTool()
    #     ui.show()
if __name__ == "__main__":
    main()

