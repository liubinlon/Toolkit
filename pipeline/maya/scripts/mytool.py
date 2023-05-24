#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
'''
File    :   link_cg.py
Time    :   2022/06/24 21:53:47
Author  :   ZhenBao Liu
Version :   1.0
Contact :   3305510092@qq.com
Desc    :   None
'''
#
import sys
# import cgtw2 
import pymel.core as pm
from maya import OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from shiboken2 import wrapInstance 
#
# dir = r"C:/CgTeamWork_v6/bin/base"
# if dir not in sys.path:
#     sys.path.append(dir)

try:
    from PySide2 import QtWidgets
    from PySide2 import QtCore
    from PySide2 import QtGui
    from PySide2 import QtUiTools
except ImportError:
    from PyQt5 import QtWidgets
    from PyQt5 import QtCore

maya_main_window_ptr = omui.MQtUtil.mainWindow() 
maya_main_window = wrapInstance(long(maya_main_window_ptr), QWidget) 

"""
获取当前cgtw登录用户的信息
"""
# m_tw = cgtw2.tw()
# m_td = m_tw.login.account_id()
# #id_list = m_tw.info.get_id("public", "account", [])
# #m_tw.task.fields("public", "account")
# user_data = m_tw.info.get("public", "account", [m_td], field_sign_list=["account.name", "account.department"])
# user_department = user_data[0]["account.department"]
# user_name = user_data[0]["account.name"]

NAME = "Public"
"""

"""
class LinkCgtw(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(LinkCgtw, self).__init__(parent=parent)
        self.setParent(maya_main_window)
        # self.m_tw = tw()
        self.setWindowFlags(Qt.Window)
        self.init_ui()
        
    
    def init_ui(self):
        """
        ui
        """
        self.setObjectName(NAME)
        self.setWindowTitle(NAME)
        self.resize(360, 50)
        lay = QtWidgets.QVBoxLayout(self)
        lay.setSpacing(10)
        self.setLayout(lay)
        #显示项目列表和个人信息
        lay_info = QtWidgets.QFormLayout()
        lay.addLayout(lay_info)
        self.lab_info_department = QtWidgets.QLabel(u"  Department:")
        self.lab_info_department.setFixedSize(150, 10)
        self.lab_info_name = QtWidgets.QLabel(u"  Artist:")
        self.lab_info_name.setFixedSize(150, 10)
        lay_info.addRow(self.lab_info_department, self.lab_info_name)
        
        lab_info = QtWidgets.QLabel(u"     project:")
        lab_info.setFixedSize(53, 20)
        self.cbx_info = QtWidgets.QComboBox()
        self.cbx_info.setFixedSize(200, 20)        
        lay_info_project = QHBoxLayout()
        lay.addLayout(lay_info_project)
        lay_info_project.addWidget(lab_info, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        lay_info_project.addWidget(self.cbx_info, 1, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        
        lay_file_path = QHBoxLayout()
        lay.addLayout(lay_file_path)        
        self.lab_file_path = QLabel(u"  File Path:")
        self.ledt_file_path = QLineEdit()
        self.btn_import_path = QPushButton(u"<<<")
        self.btn_import_path.setFixedSize(60, 20)
        lay_file_path.addWidget(self.lab_file_path)
        lay_file_path.addWidget(self.ledt_file_path)
        lay_file_path.addWidget(self.btn_import_path)

        lay_transmit_btn = QHBoxLayout()
        lay.addLayout(lay_transmit_btn)
        self.btn_public = QPushButton(u"Public")
        self.btn_public.setFixedSize(60, 20)
        lay_transmit_btn.addWidget(self.btn_public, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)  
    # def set_info_tbw(self):
    #     pass

    # def import_btn(self):
    #     pass

    # def path_ledt(self):
    #     pass
# def dock_able_widget_ui(restore=False):
#     global customMixinWindow
#     if restore == True:
#             # Grab the created workspace control with the following.
#         restoredControl = omui.MQtUtil.getCurrentParent()
    
#     if customMixinWindow is None:
#         # Create a custom mixin widget for the first time
#         customMixinWindow = LinkCgtw()     
#         customMixinWindow.setObjectName('customMayaMixinWindow')
        
#     if restore == True:
#         # Add custom mixin widget to the workspace control
#         mixinPtr = omui.MQtUtil.findControl(customMixinWindow.objectName())
#         omui.MQtUtil.addWidgetToMayaLayout(long(mixinPtr), long(restoredControl))
#     else:
#         # Create a workspace control for the mixin widget by passing all the needed parameters. See workspaceControl command documentation for all available flags.
#         customMixinWindow.show(dockable=True, height=600, width=480, uiScript='DockableWidgetUIScript(restore=True)')
    
#     return customMixinWindow

def show_ui(window_name):
    if pm.window(window_name, query=True, exists=True):
        pm.deleteUI(window_name)
    if pm.windowPref(window_name, query=True, exists=True):
        pm.windowPref(window_name, remove=True)
    win = LinkCgtw()
    win.show()
    return win
    # dock_able_widget_ui(restore=False)

if __name__ =="__main__":
    show_ui(NAME)