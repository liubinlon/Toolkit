#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
'''
    File    :   link_cgtw.py
    Time    :   2022/06/26 18:36:46
    Author  :   ZhenBao Liu
    Version :   1.0
    Contact :   3305510092@qq.com
    Desc    :   None
'''
#################################################
'''
    Version :   2.0
    Desc    :   添加abc和fbx上传功能
'''
#################################################
'''
    Version :   3.0
    Desc    :   适配shot环节
'''
#################################################
'''
    Version:    4.0
    Desc   :    添加了检查项
'''
#################################################
'''
    import link_maya_cgtw
    reload(link_maya_cgtw)
    link_maya_cgtw.run()
'''
#################################################

import sys, os
import pymel.core as pm
from maya import OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from shiboken2 import wrapInstance 
#Add working path
file_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
if file_dir not in sys.path:
    sys.path.append(file_dir)

from link_maya_cgtw.commands import link_cgtw_com
reload(link_cgtw_com)

try:
    from PySide2 import QtWidgets
    from PySide2 import QtCore
    from PySide2 import QtGui
    from PySide2 import QtUiTools
except ImportError:
    from PyQt5 import QtWidgets
    from PyQt5 import QtCore
# 获取maya窗口接口
maya_main_window_ptr = omui.MQtUtil.mainWindow() 
maya_main_window = wrapInstance(long(maya_main_window_ptr), QtWidgets.QMainWindow) 

NAME = "Public - V004"
"""
    This is class for public tool ui
"""
class LinkCgtwUi(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(LinkCgtwUi, self).__init__(parent=parent)
        self.setParent(maya_main_window)
        self.setWindowFlags(QtCore.Qt.Window)
        self.link_com = link_cgtw_com.LinkCgtwCom()
        self._data = self.link_com._data_dict
        self.init_ui()
        self.set_up()
        self.stuff_data()
         
    def init_ui(self):
        """
            ui
        """
        self.setObjectName(NAME)
        self.setWindowTitle(NAME)
        self.resize(700, 400)
        self.setWindowOpacity(0.9)
        self.widget_main = QtWidgets.QWidget(self)
        lay = QtWidgets.QVBoxLayout(self.widget_main)
        lay.setSpacing(10)
        self.setLayout(lay)
        #鏄剧ず椤圭洰鍒楄〃鍜屼釜浜轰俊鎭?
        self.widget_info = QtWidgets.QWidget()
        lay.addWidget(self.widget_info)
        lay_info = QtWidgets.QFormLayout(self.widget_info)       
        self.lab_info_department = QtWidgets.QLabel()
        self.lab_info_department.setFixedSize(500, 30)
        self.lab_info_name = QtWidgets.QLabel()
        self.lab_info_name.setFixedSize(150, 30)
        lay_info.addRow(self.lab_info_department, self.lab_info_name)        
        lab_project = QtWidgets.QLabel(u"     项目")
        lab_project.setFixedSize(70, 30)
        self.cbx_project = QtWidgets.QComboBox()
        self.cbx_project.setFixedSize(150, 30)
        lab_asset_name = QtWidgets.QLabel(u"   资产名字")
        self.cbx_asset_name = QtWidgets.QComboBox()
        self.cbx_asset_name.setFixedSize(150, 30)
        lab_type = QtWidgets.QLabel(u"  资产类型")
        lab_type.setFixedSize(70, 30)
        self.cbx_type = QtWidgets.QComboBox()
        self.cbx_type.setFixedSize(150, 30)

        self.widget_info_project = QtWidgets.QWidget()
        lay.addWidget(self.widget_info_project)
        lay_info_project = QtWidgets.QHBoxLayout(self.widget_info_project)
        lay_info_project.addWidget(lab_project, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        lay_info_project.addWidget(self.cbx_project, 1, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        lay_info_project.addWidget(lab_asset_name, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        lay_info_project.addWidget(self.cbx_asset_name, 1, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        lay_info_project.addWidget(lab_type, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        lay_info_project.addWidget(self.cbx_type, 1, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        """
            test_result
        """
        self.widget_test = QtWidgets.QWidget()
        lay.addWidget(self.widget_test)
        lay_test_result =  QtWidgets.QVBoxLayout(self.widget_test)
        self.btn_check_name = QtWidgets.QPushButton(u" 检查命名")
        self.btn_check_mesh = QtWidgets.QPushButton(u" 检查模型拓扑")
        self.btn_check_playblast = QtWidgets.QPushButton(u" 检查拍屏信息")
        self.btn_check_zore = QtWidgets.QPushButton(u" 检查控制器是否归零")
        self.btn_check_cache = QtWidgets.QPushButton(u" 检查缓存信息")
        lay_test_result.addWidget(self.btn_check_name)
        lay_test_result.addWidget(self.btn_check_mesh)
        lay_test_result.addWidget(self.btn_check_playblast)
        lay_test_result.addWidget(self.btn_check_zore)
        # 需要上传的截屏或拍屏
        self.widget_screen = QtWidgets.QWidget()
        lay.addWidget(self.widget_screen)
        lay_screenshot_path = QtWidgets.QGridLayout(self.widget_screen)
        self.btn_screenshot = QtWidgets.QPushButton(u"  截屏  ")
        self.btn_screenshot.setFixedSize(60, 30)
        self.ledt_screenshot_path = QtWidgets.QLineEdit()
        self.ledt_screenshot_path.setFixedSize(600, 30)
        self.btn_playblast = QtWidgets.QPushButton(u"  打开  ")
        self.btn_playblast.setFixedSize(60, 30)
        lay_screenshot_path.addWidget(self.btn_screenshot, 0, 0, 1, 1)
        lay_screenshot_path.addWidget(self.ledt_screenshot_path, 0, 1, 1, 1)
        lay_screenshot_path.addWidget(self.btn_playblast, 0, 2, 1, 1)
        # 提交文件的路径
        self.widget_file = QtWidgets.QWidget()
        lay.addWidget(self.widget_file)
        self.lay_file_path = QtWidgets.QGridLayout(self.widget_file)
        self.lab_file_path = QtWidgets.QLabel(u" 制作文件:")
        self.ledt_file_path = QtWidgets.QLineEdit()
        self.ledt_file_path.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ledt_file_path.setText(self.link_com.make_file_path())
        self.btn_import_path = QtWidgets.QPushButton(u"<<<")
        self.btn_import_path.setFixedSize(60, 30)
        self.lay_file_path.addWidget(self.lab_file_path, 0, 0, 1, 1)
        self.lay_file_path.addWidget(self.ledt_file_path, 0, 1, 1, 1)
        self.lay_file_path.addWidget(self.btn_import_path, 0, 2, 1, 1)

        self.widget_transmit = QtWidgets.QWidget()
        lay.addWidget(self.widget_transmit)
        lay_transmit_btn = QtWidgets.QVBoxLayout(self.widget_transmit)
        self.tedt_file_describe = QtWidgets.QTextEdit()
        self.btn_public = QtWidgets.QPushButton(u"提交")
        self.btn_public.setFixedSize(60, 30)
        lay_transmit_btn.addWidget(self.tedt_file_describe)
        lay_transmit_btn.addWidget(self.btn_public, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        

        self.widget_message = QtWidgets.QWidget()
        lay.addWidget(self.widget_message)
        lay_message_display = QtWidgets.QVBoxLayout(self.widget_message)
        self.tedt_feedback = QtWidgets.QTextEdit()
        self.tedt_feedback.setReadOnly(True)
        lay_message_display.addWidget(self.tedt_feedback)
        self.setCentralWidget(self.widget_main)

    def stuff_data(self):
        self.lab_info_department.setText(u"   模块:  {}".format(self._data["personal"]["department"]))
        self.lab_info_name.setText(u"   艺术家:  {}".format(self._data["personal"]["name"]))
        try:
            self.cbx_project.addItem(self._data["project"][self._data['comparison_information']["basedata"]])
            self.cbx_asset_name.addItem(self._data["comparison_information"]["asset_entity"])
            self.cbx_type.addItem(self._data["comparison_information"]["task_entity"])
            self.add_stuff_wiget()
        except:
            message_str = u"请找制片给任务或核对大组名字是否正确"
            QtWidgets.QMessageBox.information(maya_main_window, u"提示", message_str)
            self.widget_main.setEnabled(False)

    def add_stuff_wiget(self):
        try:
            type_str = self._data["comparison_information"]["task_entity"]
            type_lst = ["RIG"]
            if "TEX" in type_str:
                lab_material_path = QtWidgets.QLabel(u" 材质文件:")
                self.ledt_material_path = QtWidgets.QLineEdit()
                self.ledt_material_path.setFocusPolicy(QtCore.Qt.NoFocus)
                self.btn_material_path = QtWidgets.QPushButton(u" 打开")
                self.btn_material_path.setFixedSize(60, 30)
                self.lay_file_path.addWidget(lab_material_path, 2, 0, 1, 1)
                self.lay_file_path.addWidget(self.ledt_material_path, 2, 1, 1, 1)
                self.lay_file_path.addWidget(self.btn_material_path, 2, 2, 1, 1)
                self.btn_material_path.clicked.connect(self.open_material)
            if type_str not in type_lst:
                lab_appendix_path = QtWidgets.QLabel(u" fbx和abc:")
                self.lwgt_appendix_path = QtWidgets.QListWidget()
                self.btn_appendix_path = QtWidgets.QPushButton(u" 打开")
                self.btn_appendix_path.setFixedSize(60, 30)
                self.lay_file_path.addWidget(lab_appendix_path, 1, 0, 1, 1)
                self.lay_file_path.addWidget(self.lwgt_appendix_path, 1, 1, 1, 1)
                self.lay_file_path.addWidget(self.btn_appendix_path, 1, 2, 1, 1)
                self.btn_appendix_path.clicked.connect(self.open_appendix)
        except:
            pass
    
    def open_file_dialog(self, file_type=None):
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        dialog.setViewMode(QtWidgets.QFileDialog.Detail)

        file_name = dialog.getOpenFileNames()
        if file_name:
            return file_name
        else:
            QtWidgets.QMessageBox.warning(self, "warning", "Please select file")
        

    def open_directory_dialog(self):
        directory = QtWidgets.QFileDialog()
        directory.setFileMode(QtWidgets.QFileDialog.Directory)
        directory.setViewMode(QtWidgets.QFileDialog.Detail)
        if directory.exec_():
            directory_name = directory.selectedFiles()
            return directory_name
        else:
            QtWidgets.QMessageBox.warning(self, "warning", "Please select folder")
        

    def set_up(self):
        # labal
        self.link_com.info_department = self.lab_info_department
        self.link_com.info_name = self.lab_info_name
        # ComboBox
        self.link_com.user_project = self.cbx_project
        self.link_com.user_type = self.cbx_type        
        # textEdit
        self.link_com.file_describe = self.tedt_file_describe
        self.link_com.feedback = self.tedt_feedback
        # lineEdit
        # self.link_com.material_path = self.ledt_material_path
        self.link_com.file_path = self.ledt_file_path
        self.link_com.screenshot_path = self.ledt_screenshot_path
        # list widget
        # self.link_com.appendix_path = self.lwgt_appendix_path
        # widget
        self.link_com.info_widget_show = self.widget_info
        self.link_com.message_widget_show = self.widget_message
        self.link_com.test_widget_show = self.widget_test
        self.link_com.screen_widget_show = self.widget_screen
        self.link_com.file_widget_show = self.widget_file
        self.link_com.transmit_widget_show = self.widget_transmit
        self.link_com.project_widget_show = self.widget_info_project
        # clicked connect
        self.btn_import_path.clicked.connect(self.link_com.import_path)
        self.btn_public.clicked.connect(self.link_com.public_file)
        self.btn_screenshot.clicked.connect(self.link_com.screen_shot)
        self.btn_playblast.clicked.connect(self.open_playblast)

    def open_playblast(self):
        file_list = self.open_file_dialog()[0]
        if file_list:
            for _file in file_list:
                self.ledt_screenshot_path.setText(_file)

    def open_material(self):
        dir_list = self.open_directory_dialog()
        if dir_list:
            for _dir in dir_list:
                self.ledt_material_path.setText(_dir)
                self.link_com.material_path = self.ledt_material_path

    def open_appendix(self):
        self.lwgt_appendix_path.clear()
        file_lists = self.open_file_dialog()[0]
        if file_lists:
            self.lwgt_appendix_path.addItems(file_lists)
            self.link_com.appendix_path = self.lwgt_appendix_path

    def eventFilter(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.lwgt_appendix_path.selectItems()

def get_win_strat(window_name):
    if pm.window(window_name, query=True, exists=True):
        pm.deleteUI(window_name)
    if pm.windowPref(window_name, query=True, exists=True):
        pm.windowPref(window_name, remove=True)

def show_ui():
    get_win_strat(NAME)
    win = LinkCgtwUi(parent=maya_main_window)
    win.show()
    # dock_able_widget_ui(restore=False)

if __name__ == "__main__":
    show_ui()