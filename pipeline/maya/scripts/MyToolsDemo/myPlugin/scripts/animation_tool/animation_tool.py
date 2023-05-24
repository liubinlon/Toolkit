#!/usr/bin/python
# -*- coding:utf-8 -*-
import os

from PySide2.QtCore import Signal, QThread, Qt
from PySide2.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QSpinBox, QDialog, QGridLayout, QFileDialog, QMessageBox
import maya.OpenMayaUI as omui

import shiboken2, time


def get_maya_window():
    mayaPar = omui.MQtUtil.mainWindow()
    mayaWindow = shiboken2.wrapInstance(long(mayaPar), QMainWindow)
    return mayaWindow
    
class AnimationTool(QMainWindow):
    def __init__(self, parent = get_maya_window()):
        super(AnimationTool, self).__init__(parent)
        self.setWindowTitle("animation tool - v001")
        self.resize(256, 10)
        status = self.statusBar()
        status.showMessage("test tool for Rigging, please use with cautionthis is")
        self.initUI()
        
    def initUI(self):
        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)
        self.btn_plreference = QPushButton("batch reference")
        self.btn_plreference.clicked.connect(self.pl_reference)
        self.btn_ptreference = QPushButton("batch replacement reference")
        self.btn_ptreference.clicked.connect(self.pt_reference)
        self.btn_connectaim = QPushButton("connect animation curves")
        self.btn_connectaim.clicked.connect(self.connectaim)
        self.layout.addWidget(self.btn_plreference)
        self.layout.addWidget(self.btn_ptreference)
        self.layout.addWidget(self.btn_connectaim)
        self.setCentralWidget(self.widget)
        
    def get_name(self, name):
        namestr = name.split(":")
        return namestr[-1]

    def connectaim(self):
        selection = cmds.ls(sl = True)
        anim_list = cmds.ls(type = ["animCurveTU", "animCurveTL", "animCurveTA"])            
        for crv in selection: 
            name_number = self.get_name(crv)
            attr_list = cmds.listAttr(crv, keyable = True, unlocked = True)

            attr_number = len(attr_list)

            if attr_number != 0:        
                for attr in range(attr_number):
                    anim = name_number + "_" + attr_list[attr]

                    if anim in anim_list:

                        cmds.connectAttr(anim + ".output", crv + ".%s" % attr_list[attr])
            else:
                continue
    
    def pt_reference(self):
        ptwin = Ptreference(self)
        ptwin.show()
        # if self.btn_ptreference.isChecked():
        #     ptwin = Ptreference(self)
        #     ptwin.show()
        # else:
        #     pass


    def pl_reference(self):
        plwin = Plreference(self)
        plwin.show()
        # if self.btn_plreference.isChecked():
        #     plwin = Plreference(self)
        #     plwin.show()
        # else:
        #     pass
    
class Ptreference(QDialog):
    def __init__(self, parent = None):
        super(Ptreference, self).__init__(parent)
        self.setWindowTitle("batch reference - v001")
        self.resize(400, 10)
        self.initUI()
    
    def initUI(self):
        # self.widget = QWidget()
        self.layout = QVBoxLayout()
        # self.widget.setLayout(self.layout)
        self.lab_pathlabel = QLabel("file path:")
        self.let_filepath = QLineEdit()
        self.btn_ok = QPushButton("Ok")
        self.btn_ok.clicked.connect(self.pt_reference)
        self.layout.addWidget(self.lab_pathlabel)
        self.layout.addWidget(self.let_filepath)
        self.layout.addWidget(self.btn_ok)
        #self.setCentralWidget(self.layout)
        self.setLayout(self.layout)

    def pt_reference(self):
        path = self.getfilepath()
        newpath = eval(repr(path).replace("\\", "/"))
        selectlist = cmds.ls(sl = True)
        for i in selectlist:
            cmds.file(newpath, loadReference = str(i), options = "v=0;")

    def getfilepath(self):
        if not self.let_filepath:
            return
        return self.let_filepath.text()    
    # def open(self):
    #     self.show()

class Plreference(QDialog):
    def __init__(self, parent = None):
        super(Plreference, self).__init__(parent)
        self.setWindowTitle("batch reference - v001")
        self.resize(400, 10)
        self.initUI()
    
    def initUI(self):
        # self.widget = QWidget()
        self.layout = QGridLayout()
        # self.widget.setLayout(self.layout)
        self.lab_pathlabel = QLabel("file path:")
        self.let_filepath = QLineEdit()
        self.btn_open = QPushButton("Open")
        self.btn_open.clicked.connect(self.__open)
        self.lab_number = QLabel("number:")
        self.sbx_number = QSpinBox()
        self.btn_ok = QPushButton("OK")
        self.btn_ok.clicked.connect(self.run)
        self.layout.addWidget(self.lab_pathlabel, 1, 1)
        self.layout.addWidget(self.let_filepath, 1, 2)
        self.layout.addWidget(self.btn_open, 1, 3)
        self.layout.addWidget(self.lab_number, 2, 1)
        self.layout.addWidget(self.sbx_number, 2, 2)
        self.layout.addWidget(self.btn_ok, 2, 3)
        self.setLayout(self.layout)

    def referencefile(self, filepath, number, name):
        newfilepath = eval(repr(filepath).replace("\\", "/"))
        print "newfilepath" + newfilepath
        for i in range(number):
            cmds.file(newfilepath, reference = True, mergeNamespacesOnClash = False, namespace = name)
    
    
    def getfilename(self, filepath):
        filename = filepath.split('\\')[-1]
        print "filename:" + filename
        newfilename = filename.split('.')[0]
        print "newfilename:"+ newfilename
        return newfilename

    def path_dialog(self, path_data):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setViewMode(QFileDialog.Detail)
        if dialog.exec_():
            file_name = (dialog.selectedFiles())[0]
            path_data.setText(file_name)
            # return file_name
        else:
            QMessageBox.warning(self, "warning", "Please select directory")
        return file_name
        
    def __open(self):
        file_path = self.path_dialog(self.let_filepath)
        print file_path

        
    def run(self):
        filepath = self.getfilepath()
        print "filepath" + filepath
        number = self.getnumber()
        print "number" + str(number)
        name = self.getfilename(filepath)
        print "name" + name
        self.referencefile(filepath, number, name)
    

    
    # def open(self):
    #     self.show()
            
    def getfilepath(self):
        if not self.let_filepath:
            return
        return self.let_filepath.text()
        
    def getnumber(self):
        if not self.sbx_number:
            return
        return self.sbx_number.value()
def main():
    try:
       AnimationTool.close()
       shiboken2.delete(AnimationTool)
       del(AnimationTool)
    except:pass
    win = AnimationTool()
    # ptwin = Ptreference()
    # prwin = Prreference()
    win.show()


if __name__ == '__main__':
    try:
       AnimationTool.close()
       shiboken2.delete(AnimationTool)
       del(AnimationTool)
    except:pass
    win = AnimationTool()
    # ptwin = Ptreference()
    # prwin = Prreference()
    win.show()
    # win.btn_ptreference.clicked.connect(ptwin.open)
    # win.btn_plreference.clicked.connect(prwin.open))