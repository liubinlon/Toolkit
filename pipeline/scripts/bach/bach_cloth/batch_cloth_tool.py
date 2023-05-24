#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
'''
   File    :   batch_cloth_tool.py
   Time    :   2023/03/19 20:50:07
   Author  :   Liu ZhenBao
   Version :   1.0
   Contact :   3305510092@qq.com
   Desc    :   None
'''
############################################################################
# import the libraries needed by this script here

import os
import sys
import subprocess

from PySide2.QtCore import Qt, QMetaObject
import PySide2.QtWidgets as QtWidgets
from PySide2 import QtCore, QtGui

path = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
abs_dir = r"{0}".format(path)

if abs_dir not in sys.path:
    sys.path.append(abs_dir)

import batch_cloth_com
# reload(batch_cloth_com)

NAME = u"Batch cloth - V001"

# here put the class script
class UseListWidget(QtWidgets.QListWidget):  # type: ignore
    def __init__(self, parent=None):
        super(UseListWidget, self).__init__(parent)
        self.setAcceptDrops(True)  # 开启接受拖入事件
        self.setDragEnabled(True)
        # self.setFixedSize(400, 50)
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
                if local_file.endswith(".mb", "abc", "fbx"):
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

class BatchCloth(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super(BatchCloth, self).__init__(parent)
        self.batch_com = batch_cloth_com.ClothAssembleCom()
        self.widget_main = QtWidgets.QWidget(self)
        self.lay_main = QtWidgets.QHBoxLayout(self.widget_main)
        self.stuff_ui()
        self.setCentralWidget(self.widget_main)

    def stuff_ui(self):
        self.setObjectName(NAME)
        self.setWindowTitle(NAME)
        self.resize(1000, 80)        
        app_icon = QtGui.QIcon(f"{path}/icons/reference.png")
        self.setWindowIcon(app_icon)

        lay_btn_replace = QtWidgets.QVBoxLayout()
        self.btn_output_replace = QtWidgets.QPushButton(QtGui.QIcon(f"{path}/icons/batch_reference.png"), " ")
        self.btn_output_replace.setIconSize(QtCore.QSize(60, 60))
        self.btn_output_replace.setFlat(True)
        self.cbx_auto_replace = QtWidgets.QCheckBox()
        self.cbx_auto_replace.setIcon(QtGui.QIcon(f"{path}/icons/automatch.png"))
        self.cbx_auto_replace.setIconSize(QtCore.QSize(60, 60))
        self.cbx_auto_replace.setChecked(True)
        self.cbx_auto_replace.stateChanged.connect(lambda:self.btn_state(self.cbx_auto_replace))
        lay_btn_replace.addWidget(self.btn_output_replace)
        lay_btn_replace.addWidget(self.cbx_auto_replace)
        self.lay_main.addLayout(lay_btn_replace)

        lay_ani_file = QtWidgets.QVBoxLayout()
        lab_ani_file = QtWidgets.QLabel(u"  动画文件")
        self.lwt_mb_file = UseListWidget()
        lay_ani_file.addWidget(lab_ani_file)
        lay_ani_file.addWidget(self.lwt_mb_file)
        self.lay_main.addLayout(lay_ani_file)
        
        lay_old_file = QtWidgets.QVBoxLayout()
        lab_old_file = QtWidgets.QLabel(u"  旧引用文件")
        self.lwt_abc_file =  UseListWidget()
        self.lwt_abc_file.setDisabled(True)
        lay_old_file.addWidget(lab_old_file)
        lay_old_file.addWidget(self.lwt_abc_file)
        self.lay_main.addLayout(lay_old_file)

        lay_new_file = QtWidgets.QVBoxLayout()
        lab_new_file = QtWidgets.QLabel(u"  新引用文件")
        self.lwt_new_file =  UseListWidget()
        lay_new_file.addWidget(lab_new_file)
        lay_new_file.addWidget(self.lwt_new_file)
        self.lay_main.addLayout(lay_new_file)

        self.batch_com.mb_file = self.lwt_mb_file
        self.batch_com.abs_file = self.lwt_abc_file
        self.batch_com.fbx_file = self.lwt_new_file
        self.btn_output_replace.clicked.connect(self.assemble_cloth)
    
    def assemble_cloth(self):
        if self.get_absolute_path_list():
            for abs_file in self.get_absolute_path_list():
                com_panfu = f"c:"
                com_cd = f"cd c:/Program Files/Autodesk/Maya2018/bin"
                com_run = f"mayapy {abs_dir}/bach_cache_com.py {abs_file}"
                # cd_mayapy = subprocess.Popen(com_panfu+"&"+com_cd+"&"+com_run, stdout=subprocess.PIPE, shell=True)
                # cd_mayapy.wait()
                cd_mayapy = subprocess.check_output(com_panfu+"&"+com_cd+"&"+com_run, shell=True)
                out_text = cd_mayapy.decode("utf-8")
        else:
            self.pop_ups()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    win = BatchCloth()
    win.show()
    sys.exit(app.exec_())
    