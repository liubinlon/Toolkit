#!/user/bin/env python
# -*- coding: utf-8 -*-
# Author: Zhenbao Liu
# QQ: 3305510092
# Time: 2021/05/15 16:29:05

"""
file_name: threadUI.py
This is a script to rename objects.
"""

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
import os, sys, inspect

script_path = os.path.dirname(inspect.getsourcefile(lambda: 0))
# script_path = os.path.dirname(os.path.realpath(__file__))

Dir = r"{0}".format(script_path)
if Dir not in sys.path:
    sys.path.append(Dir)

import my_thread

reload(my_thread)

window_name = "ThreadWindow"


def get_maya_window():
    maya_main = omui.MQtUtil_mainWindow()
    ptr = wrapInstance(long(maya_main), QtWidgets.QMainWindow)
    return ptr


class ThreadUI(QtWidgets.QMainWindow):

    def __init__(self, parent=get_maya_window()):
        super(ThreadUI, self).__init__(parent)
        self.setObjectName(window_name)
        self.setWindowTitle(window_name)
        self.set_icon()
        self.cls_thread = my_thread.ThreadScript()
        self.init_ui()

    # Set ui
    def init_ui(self):
        # Main widget
        self.setFixedSize(360, 550)
        self.setWindowOpacity(0.9)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QGridLayout(self.main_widget)
        self.main_widget.setLayout(self.main_layout)
        # Add widget
        self.add_widget = QtWidgets.QWidget()
        self.add_widget.setObjectName("add_widget")
        self.add_layout = QtWidgets.QGridLayout(self.add_widget)
        self.add_group = QtWidgets.QGroupBox("Add")
        self.add_layout.addWidget(self.add_group)
        self.add_grp_layout = QtWidgets.QGridLayout(self.add_group)
        self.lab_prefix = QtWidgets.QLabel("Prefix: ")
        self.lin_prefix = QtWidgets.QLineEdit()
        self.lin_prefix.setObjectName("lin_prefix")
        self.lab_suffix = QtWidgets.QLabel("Suffix: ")
        self.lin_suffix = QtWidgets.QLineEdit()
        self.lin_suffix.setObjectName("lin_suffix")
        self.rdb_add_selected = QtWidgets.QRadioButton("Selected")
        self.rdb_add_hierarchy = QtWidgets.QRadioButton("Hierarchy")
        self.rdb_add_hierarchy.setChecked(True)
        # self.rdb_add_all = QtWidgets.QRadioButton("All")
        self.btn_add = QtWidgets.QPushButton("Add")

        self.add_button_group = QtWidgets.QButtonGroup()
        self.add_button_group.addButton(self.rdb_add_hierarchy, 0)
        self.add_button_group.addButton(self.rdb_add_selected, 1)
        self.add_grp_layout.addWidget(self.lab_prefix, 0, 0, 1, 1)
        self.add_grp_layout.addWidget(self.lin_prefix, 0, 1, 1, 4)
        self.add_grp_layout.addWidget(self.lab_suffix, 1, 0, 1, 1)
        self.add_grp_layout.addWidget(self.lin_suffix, 1, 1, 1, 4)
        self.add_grp_layout.addWidget(self.rdb_add_hierarchy, 2, 1, 1, 1)
        self.add_grp_layout.addWidget(self.rdb_add_selected, 2, 3, 1, 1)
        self.add_grp_layout.addWidget(self.btn_add, 3, 0, 1, 5)

        # Replace widget
        self.replace_widget = QtWidgets.QWidget()
        self.replace_widget.setObjectName("replace_widget")
        self.replace_layout = QtWidgets.QGridLayout(self.replace_widget)
        self.replace_group = QtWidgets.QGroupBox("Repalace")
        self.replace_layout.addWidget(self.replace_group)
        self.replace_grp_layout = QtWidgets.QGridLayout(self.replace_group)
        self.lab_find = QtWidgets.QLabel("Find: ")
        self.lin_find = QtWidgets.QLineEdit()
        self.lin_find.setObjectName("lin_find")
        self.lab_replace = QtWidgets.QLabel("replace: ")
        self.lin_replace = QtWidgets.QLineEdit()
        self.lin_replace.setObjectName("lin_replace")
        self.rdb_replace_selected = QtWidgets.QRadioButton("Selected")
        self.rdb_replace_hierarchy = QtWidgets.QRadioButton("Hierarchy")
        self.rdb_replace_hierarchy.setChecked(True)
        self.replace_button_group = QtWidgets.QButtonGroup()
        self.replace_button_group.addButton(self.rdb_replace_hierarchy, 0)
        self.replace_button_group.addButton(self.rdb_replace_selected, 1)
        self.btn_replace = QtWidgets.QPushButton("Repalace")

        self.replace_grp_layout.addWidget(self.lab_find, 0, 0, 1, 1)
        self.replace_grp_layout.addWidget(self.lin_find, 0, 1, 1, 4)
        self.replace_grp_layout.addWidget(self.lab_replace, 1, 0, 1, 1)
        self.replace_grp_layout.addWidget(self.lin_replace, 1, 1, 1, 4)
        self.replace_grp_layout.addWidget(self.rdb_replace_hierarchy, 2, 1, 1, 1)
        self.replace_grp_layout.addWidget(self.rdb_replace_selected, 2, 3, 1, 1)
        self.replace_grp_layout.addWidget(self.btn_replace, 3, 0, 1, 5)

        # Renaming widget
        self.rename_widget = QtWidgets.QWidget()
        self.rename_widget.setObjectName("rename_widget")
        self.rename_layout = QtWidgets.QGridLayout(self.rename_widget)
        self.rename_group = QtWidgets.QGroupBox("Rename")
        self.rename_layout.addWidget(self.rename_group)
        self.rename_grp_layout = QtWidgets.QGridLayout(self.rename_group)
        self.rdb_A_Z = QtWidgets.QRadioButton("a-z")
        self.rdb_number = QtWidgets.QRadioButton("0-9")
        self.rdb_None = QtWidgets.QRadioButton("None")
        self.rdb_None.setChecked(True)
        self.rename_item_group = QtWidgets.QButtonGroup()
        self.rename_item_group.addButton(self.rdb_A_Z, 0)
        self.rename_item_group.addButton(self.rdb_number, 1)
        self.rename_item_group.addButton(self.rdb_None, 2)
        self.rename_item_group.buttonPressed.connect(self.get_id)
        self.rdb_case_switch = QtWidgets.QCheckBox("Case switch")
        self.lab_rename_object = QtWidgets.QLabel("Object name")
        self.rename_suffix_widget = QtWidgets.QWidget()
        self.rename_suffix_widget.setObjectName("rename_suffix_widget")
        self.rename_suffix_layout = QtWidgets.QGridLayout(self.rename_suffix_widget)
        self.lin_rename_object = QtWidgets.QLineEdit()
        self.lab_rename_suffix = QtWidgets.QLabel("Add suffix")
        self.auto_textedit = QtWidgets.QTextEdit()
        self.auto_textedit.setPlainText("anim\ndriver\ncon")
        self.rename_suffix_layout.addWidget(self.lab_rename_suffix, 0, 0, 1, 1)
        self.rename_suffix_layout.addWidget(self.auto_textedit, 1, 0, 1, 1)
        self.cbx_rename = QtWidgets.QScrollArea()
        # self.cbx_rename.setWidgetResizable(True)
        self.cbx_rename.setMinimumHeight(70)
        self.cbx_layout = QtWidgets.QHBoxLayout(self.cbx_rename)
        self.rdb_rename_selected = QtWidgets.QRadioButton("Selected")
        self.rdb_rename_hierarchy = QtWidgets.QRadioButton("Hierarchy")
        self.rdb_rename_hierarchy.setChecked(True)
        self.rename_button_group = QtWidgets.QButtonGroup()
        self.rename_button_group.addButton(self.rdb_rename_hierarchy, 0)
        self.rename_button_group.addButton(self.rdb_rename_selected, 1)
        self.btn_rename = QtWidgets.QPushButton("Rename")

        self.rename_grp_layout.addWidget(self.lab_rename_object, 0, 0, 1, 3)
        self.rename_grp_layout.addWidget(self.lin_rename_object, 1, 0, 1, 3)

        self.rename_grp_layout.addWidget(self.rdb_A_Z, 2, 0, 1, 1)
        self.rename_grp_layout.addWidget(self.rdb_number, 2, 1, 1, 1)
        self.rename_grp_layout.addWidget(self.rdb_None, 2, 2, 1, 1)
        self.rename_grp_layout.addWidget(self.rdb_case_switch, 3, 0, 1, 3)
        self.rename_grp_layout.addWidget(self.rename_suffix_widget, 0, 3, 4, 1)
        self.rename_grp_layout.addWidget(self.rdb_rename_hierarchy, 4, 1, 1, 1)
        self.rename_grp_layout.addWidget(self.rdb_rename_selected, 4, 3, 1, 1)
        self.rename_grp_layout.addWidget(self.btn_rename, 5, 0, 1, 5)

        self.main_layout.addWidget(self.add_widget)
        self.main_layout.addWidget(self.replace_widget)
        self.main_layout.addWidget(self.rename_widget)
        self.main_layout.setSpacing(0)
        self.setCentralWidget(self.main_widget)
        # Connections execution script
        self.btn_add.clicked.connect(self.cls_thread.add_prefix_suffix)
        self.btn_replace.clicked.connect(self.cls_thread._replace)
        self.btn_rename.clicked.connect(self.cls_thread._rename)
        self.cls_thread.add_lin_prefix = self.lin_prefix
        self.cls_thread.add_lin_suffix = self.lin_suffix
        self.cls_thread.replace_lin_find = self.lin_find
        self.cls_thread.auto_textedit = self.auto_textedit
        self.cls_thread.replace_lin_replace = self.lin_replace
        self.cls_thread.rename_lin_object = self.lin_rename_object
        self.cls_thread.add_button_group = self.add_button_group
        self.cls_thread.replace_button_group = self.replace_button_group
        self.cls_thread.rename_button_group = self.rename_button_group
        self.cls_thread.rename_item_group = self.rename_item_group
        self.cls_thread.rename_suffix_widget = self.rename_suffix_widget
        self.cls_thread.rdb_case_switch = self.rdb_case_switch

    def get_id(self, value):
        if self.rename_item_group.id(value) == 2:
            self.rename_suffix_widget.setEnabled(True)
        else:
            self.rename_suffix_widget.setEnabled(False)

    def set_icon(self):
        app_icon = QtGui.QIcon(r"..//icon//logo.png")
        self.setWindowIcon(app_icon)


def show_ui(window_name):
    if cmds.window(window_name, query=True, exists=True):
        cmds.deleteUI(window_name)
    if cmds.windowPref(window_name, query=True, exists=True):
        cmds.windowPref(window_name, remove=True)


if __name__ == "__main__":
    show_ui(window_name)
    win = ThreadUI()
    win.show()
