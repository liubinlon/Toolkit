#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
'''
File    :   bach_abc_tool.py
Time    :   2022/10/26 00:07:33
Author  :   Liu ZhenBao
Version :   1.0
Contact :   3305510092@qq.com
Desc    :   None
'''
##################################################################
"""
Time: 2020/10/31
Version: 2.0
Desc: 添加文件输出显示框
"""
"""
Time: 2020/11/04
Version: 3.0
Desc: 添加导出不同的文件
"""
# import the libraries needed by this script here
import os, sys, json, re
import logging
import subprocess
from collections import OrderedDict
try:
    from PySide2 import QtWidgets
    from PySide2 import QtCore
    from PySide2 import QtGui
    from PySide2 import QtUiTools
except ImportError:
    from PyQt5 import QtWidgets
    from PyQt5 import QtCore


abs_dir = os.path.dirname(os.path.abspath(__file__))

if abs_dir not in sys.path:
    sys.path+=[abs_dir]

NAME = u"Bach abc - V002"

# here put the class script
class UseListWidget(QtWidgets.QListWidget):  # type: ignore
    def __init__(self, parent=None):
        super(UseListWidget, self).__init__(parent)
        self.setAcceptDrops(True)  # 开启接受拖入事件
        self.setDragEnabled(True)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setContextMenuPolicy(QtGui.Qt.CustomContextMenu)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.customContextMenuRequested.connect(self.right_menu)
        

    def dragEnterEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()
            # super(UseListWidget, self).dragEnterEvent(event)
                        
    def dropEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            event.setDropAction(QtGui.Qt.CopyAction)
            event.accept()
            for _url in mime_data.urls():
                local_file = _url.toLocalFile()
                if local_file.endswith(".ma"):
                    self.addItem(local_file)
        else:
            event.ignore()

    def right_menu(self, pos):
        _menu = QtWidgets.QMenu()  # type: ignore
        menu_remove = _menu.addAction(u"删除")  # type: ignore
        menu_clear = _menu.addAction(u"清空")  # type: ignore
        _action = _menu.exec_(self.mapToGlobal(pos))
               
        if _action == menu_remove:
            for _path in range(len(self.selectedIndexes())-1, -1, -1):
                self.takeItem(self.selectedIndexes()[_path].row())
        elif _action == menu_clear:
            self.clear()
        else:
            pass

class BachCache(QtWidgets.QMainWindow):  # type: ignore
    def __init__(self, parent=None):
        super(BachCache, self).__init__(parent)
        # self.setWindowFlags(QtCore.Qt.Window)
        self.root_directory = os.path.dirname(abs_dir)
        self.stuff_ui()
    
    def stuff_ui(self):
        """
        填充ui
        """
        self.setObjectName(NAME)
        self.setWindowTitle(NAME)
        self.resize(860, 600)
        app_icon = QtGui.QIcon(f"{self.root_directory}/icons/cache.png")
        self.setWindowIcon(app_icon)
        self.widget_main = QtWidgets.QWidget(self)
        lay_main = QtWidgets.QGridLayout(self.widget_main)

        lay_selecte_abc = QtWidgets.QVBoxLayout()
        btn_output_abc = QtWidgets.QPushButton(QtGui.QIcon(f"{self.root_directory}/icons/batch_cache.png"), " ")
        btn_output_abc.setIconSize(QtCore.QSize(60, 60))
        btn_output_abc.setFlat(True)
        btn_output_abc.clicked.connect(self.output_abc)
        # self.rbtn_replace_abc = QtWidgets.QRadioButton(u"Reference")
        # self.rbtn_replace_abc.setChecked(True)
        # self.rbtn_import_abc = QtWidgets.QRadioButton(u"Import")
        spr_selecte_abc = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        
        lay_selecte_abc.addWidget(btn_output_abc)
        # lay_selecte_abc.addWidget(self.rbtn_replace_abc)
        # lay_selecte_abc.addWidget(self.rbtn_import_abc)
        lay_selecte_abc.addItem(spr_selecte_abc)
        lay_main.addLayout(lay_selecte_abc, 0, 0, 1, 1)

        lay_output_abc = QtWidgets.QVBoxLayout()
        self.file_path = UseListWidget()       
        lay_output_abc.addWidget(self.file_path)
        lay_main.addLayout(lay_output_abc, 0, 1, 1, 1)

        lay_hint_file = QtWidgets.QVBoxLayout()
        lab_finish_file = QtWidgets.QLabel(u"完成")
        lab_undone_file = QtWidgets.QLabel(u"未完成")
        
        self.lwgt_finish_file = QtWidgets.QListWidget()        
        self.lwgt_undone_file = QtWidgets.QListWidget() 
        lay_hint_file.addWidget(lab_finish_file)       
        lay_hint_file.addWidget(self.lwgt_finish_file)
        lay_hint_file.addWidget(lab_undone_file)
        lay_hint_file.addWidget(self.lwgt_undone_file)
        lay_main.addLayout(lay_hint_file, 0, 2, 1, 1)
        self.setCentralWidget(self.widget_main)
    
    def output_abc(self):
        finished_file_list = list()
        unfinished_file_list = list()
        if self.get_absolute_path_list():
            for abs_file in self.get_absolute_path_list():
                com_panfu = f"c:"
                com_cd = f"cd c:/Program Files/Autodesk/Maya2018/bin"
                com_run = f"mayapy {abs_dir}/bach_cache_com.py {abs_file}"
                # cd_mayapy = subprocess.Popen(com_panfu+"&"+com_cd+"&"+com_run, stdout=subprocess.PIPE, shell=True)
                # cd_mayapy.wait()
                cd_mayapy = subprocess.check_output(com_panfu+"&"+com_cd+"&"+com_run, shell=True)
                out_text = cd_mayapy.decode("utf-8")
                if "Finished file" in out_text:
                    finished_file_list.append(self.out_file_name(keywords="Finished file", out_text=out_text))                  
                elif "Unfinished file" in out_text:
                    unfinished_file_list.append(self.out_file_name(keywords="Unfinished file", out_text=out_text))
                else:
                    pass
            self.lwgt_finish_file.addItems(list(set(finished_file_list)))
            self.lwgt_undone_file.addItems(list(set(unfinished_file_list)))
        else:
            self.pop_ups()

    def out_file_name(self, keywords=None, out_text=None):
        for _tex in out_text.splitlines():
            if str(keywords) in _tex:
                out_file_str = _tex.split("-")[-1]
                return out_file_str

    def pop_ups(self):
        #self.mgx_pop_ups = QtWidgets.QMessageBox.warning(self, u"提示", u"请选择一个组!", QtWidgets.QMessageBox.Yes, QMessageBox.Yes)
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle(u"提示")
        msg_box.setText(u" 请拖入需要导出abc的.ma文件")
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes)
        btn_yes = msg_box.button(QtWidgets.QMessageBox.Yes)
        btn_yes.setText(u"确认")
        msg_box.exec_()

    def get_absolute_path_list(self):
        file_path_list = list()
        count_number = self.file_path.count()
        if count_number > 0:
            for _count in range(count_number):
                file_path_list.append(self.file_path.item(_count).text())
        return file_path_list
               
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)   
    win = BachCache()
    win.show()
    sys.exit(app.exec_())