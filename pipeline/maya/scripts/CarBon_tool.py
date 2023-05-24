#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
'''
File    :   pm.py
Time    :   2022/07/29 18:17:53
Author  :   ZhenBao Liu
Version :   1.0
Contact :   3305510092@qq.com
Desc    :   None
'''

# import the libraries needed by this script here
import os
import sys
import json
import tempfile


from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtCore import Signal, QThread, Qt

import maya.OpenMayaUI as omui
import pymel.core as pm
from shiboken2 import wrapInstance
# Get maya main prt
maya_main_window_ptr = omui.MQtUtil.mainWindow() 
maya_main_window = wrapInstance(long(maya_main_window_ptr), QtWidgets.QDialog) 


UINAME = "CarBon-V001"
# here put the class script
"""

"""
class CarBon(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window):
        super(CarBon, self).__init__(parent=parent)
        self.temp_path = tempfile.gettempdir()
        self.setObjectName(UINAME)
        self.setWindowTitle(UINAME)
        self.resize(400, 100)
        self.ui_stuff()
        self.get_menu_data()
    # Populate the ui interface 
    def ui_stuff(self):
        main_lay = QtWidgets.QGridLayout(self)
        main_lay.setSpacing(10)
        lab_double = QtWidgets.QLabel(u"doubleSided:")
        lab_innerFatness = QtWidgets.QLabel(u"innerFatness:")
        lab_outerFatness = QtWidgets.QLabel(u"outerFatness:")
        lab_mass = QtWidgets.QLabel(u"mass:")

        self.let_double = QtWidgets.QLineEdit()
        self.let_double.setPlaceholderText("doubleSided")
        self.let_innerFatness = QtWidgets.QLineEdit()
        self.let_innerFatness.setPlaceholderText("innerFatness")
        self.let_outerFatness = QtWidgets.QLineEdit()
        self.let_outerFatness.setPlaceholderText("outerFatness")
        self.let_mass = QtWidgets.QLineEdit()
        self.let_mass.setPlaceholderText("mass")
        
        btn_run = QtWidgets.QPushButton(u"write")
        btn_run.clicked.connect(self.con_run)
        self.status_bar = QtWidgets.QStatusBar(self)
        self.status_bar.showMessage(u"这是一个测试工具")
        main_lay.addWidget(lab_double, 0, 0, 1, 1)
        main_lay.addWidget(self.let_double, 0, 1, 1, 1)

        main_lay.addWidget(lab_innerFatness, 1, 0, 1, 1)
        main_lay.addWidget(self.let_innerFatness, 1, 1, 1, 1)

        main_lay.addWidget(lab_outerFatness, 2, 0, 1, 1)
        main_lay.addWidget(self.let_outerFatness, 2, 1, 1, 1)
        

        main_lay.addWidget(lab_mass, 3, 0, 1, 1)
        main_lay.addWidget(self.let_mass, 3, 1, 1, 1)
        main_lay.addWidget(btn_run, 4, 0, 1, 2)
        main_lay.addWidget(self.status_bar, 5, 0, 1, 2)
        self.setLayout(main_lay)
        
    # Create a temporary file   
    def get_menu_data(self):
        data_file = "{}\\CarBon_data.json".format(tempfile.gettempdir())
        self.data_file = data_file.replace("\\", "/")
        if not os.path.exists(self.data_file):
            self.creat_new_file(self.data_file)
            return
        try:    
            with open(self.data_file, 'r') as load_f:
                load_dict = json.load(load_f)        
            self.let_double.setText(load_dict["doubleSided"])
            self.let_innerFatness.setText(load_dict["innerFatness"])
            self.let_outerFatness.setText(load_dict["outerFatness"])
            self.let_mass.setText(load_dict["mass"])
        except:
            pass
    # Executed script 
    def con_run(self):
        temp_data_dict = dict()
        sel_lst = pm.ls(sl=True)
        if not sel_lst or len(sel_lst)>1:
            return self.pop_ups()
        shape_nodes = pm.listRelatives(sel_lst[0], ad=1, type="CarbonShape")
        rigid_nodes = pm.listRelatives(sel_lst[0], ad=1, type="CarbonRigid")        
        for node in shape_nodes:
            pm.setAttr(node + ".doubleSided", float(self.let_double.text()))
            
            pm.setAttr(node + ".innerFatness", float(self.let_innerFatness.text()))
            
            pm.setAttr(node + ".outerFatness", float(self.let_outerFatness.text()))
            
        #rigid_nodes = pm.ls(sl=True, type='CarbonRigid')
        for node in rigid_nodes:
            try:
                pm.setAttr(node + ".mass", float(self.let_mass.text()))                
            except:                
                pass
        temp_data_dict["doubleSided"] = self.let_double.text()
        temp_data_dict["innerFatness"] = self.let_innerFatness.text()
        temp_data_dict["outerFatness"] = self.let_outerFatness.text()
        temp_data_dict["mass"] = str(self.let_mass.text())
        json_str = json.dumps(temp_data_dict, indent=4)
        with open(self.data_file, 'w') as load_f:
            load_dict = load_f.write(json_str)
        
    def creat_new_file(self, file_path):        
        open(file_path, "w+").close()
     
    def pop_ups(self):
        #self.mgx_pop_ups = QtWidgets.QMessageBox.warning(self, u"提示", u"请选择一个组!", QtWidgets.QMessageBox.Yes, QMessageBox.Yes)
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle(u"提示")
        msg_box.setText(u"请选择需要设置的物体或组")
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes)
        btn_yes = msg_box.button(QtWidgets.QMessageBox.Yes)
        btn_yes.setText(u"确认")
        msg_box.exec_()

def get_win_strat(window_name):
    if pm.window(window_name, query=True, exists=True):
        pm.deleteUI(window_name)
    if pm.windowPref(window_name, query=True, exists=True):
        pm.windowPref(window_name, remove=True)

def start():
    get_win_strat(UINAME)
    win = CarBon()
    win.show()

if __name__ == "__main__":
    start()