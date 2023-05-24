#!/usr/bin/python
# -*- coding:utf-8 -*-
import os

from PySide2.QtCore import Signal, QThread, Qt
from PySide2.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit
import maya.OpenMayaUI as omui
import shiboken2, time


class Ptreference(QMainWindow):
    def __init__(self, parent = None):
        super(Ptreference, self).__init__(parent)
        self.setWindowTitle("batch reference - v001")
        self.resize(400, 10)
        self.initUI()
    
    def initUI(self):
        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)
        self.lab_pathlabel = QLabel("file path:")
        self.let_filepath = QLineEdit()
        self.btn_ok = QPushButton("OK")
        self.btn_ok.clicked.connect(self.pt_reference)
        self.layout.addWidget(self.lab_pathlabel)
        self.layout.addWidget(self.let_filepath)
        self.layout.addWidget(self.btn_ok)
        self.setCentralWidget(self.widget)


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

def main():
    win = Ptreference()
    win.show()
if __name__ == "__main__":
    win = Ptreference()
    win.show()