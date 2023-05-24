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
"""
    Batch cloth - V001
    组装hdn的fbx骨骼到maya cfx文件, 复制权重,
"""
"""
    Batch cloth - V002
    添加了边缘骨骼判断和毛囊重新定位
"""
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

NAME = u"Batch cloth - V002"

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

                if local_file.endswith((".mb", ".ma",".fbx")):
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
        self.widget_main = QtWidgets.QWidget(self)
        self.lay_main = QtWidgets.QHBoxLayout(self.widget_main)
        self.stuff_ui()
        self.setCentralWidget(self.widget_main)

    def stuff_ui(self):
        self.setObjectName(NAME)
        self.setWindowTitle(NAME)
        self.resize(1000, 500)        
        app_icon = QtGui.QIcon(f"{path}/icons/cloth.png")
        self.setWindowIcon(app_icon)

        lay_fbx_file = QtWidgets.QVBoxLayout()
        lab_fbx_file = QtWidgets.QLabel(u"  fbx文件")
        self.lwt_fbx_file = UseListWidget()
        lay_fbx_file.addWidget(lab_fbx_file)
        lay_fbx_file.addWidget(self.lwt_fbx_file)
        self.lay_main.addLayout(lay_fbx_file)


        lay_maya_file = QtWidgets.QVBoxLayout()
        lab_new_file = QtWidgets.QLabel(u"  maya文件")
        self.lwt_maya_file =  UseListWidget()
        lay_maya_file.addWidget(lab_new_file)
        lay_maya_file.addWidget(self.lwt_maya_file)
        self.lay_main.addLayout(lay_maya_file)

        lay_btn_assemble = QtWidgets.QVBoxLayout()
        self.btn_output_assemble = QtWidgets.QPushButton(QtGui.QIcon(f"{path}/icons/batch_cloth.png"), " ")
        self.btn_output_assemble.setIconSize(QtCore.QSize(60, 60))
        self.btn_output_assemble.setFlat(True)
        lay_btn_assemble.addWidget(self.btn_output_assemble)
        self.lay_main.addLayout(lay_btn_assemble)

        self.btn_output_assemble.clicked.connect(self.assemble_cloth)
    
    def assemble_cloth(self):
        if self.get_maya_path_list():
            for abs_file in self.get_maya_path_list():         
                com_panfu = f"c:"
                com_cd = f"cd c:/Program Files/Autodesk/Maya2020/bin"
                com_run = f"mayapy {abs_dir}/batch_cloth/batch_cloth_com.py {abs_file} {self.get_fbx_path_list()}"
                cd_mayapy = subprocess.Popen(com_panfu+"&"+com_cd+"&"+com_run, stdout=subprocess.PIPE, shell=True)
                # out, err = cd_mayapy.communicate()
                # exitcode = cd_mayapy.returncode
                # cd_mayapy.wait()
                cd_mayapy = subprocess.check_output(com_panfu+"&"+com_cd+"&"+com_run, shell=True)
                out_text = cd_mayapy.decode("utf-8")
        else:
            self.pop_ups()

    def pop_ups(self):
        #self.mgx_pop_ups = QtWidgets.QMessageBox.warning(self, u"提示", u"请选择一个组!", QtWidgets.QMessageBox.Yes, QMessageBox.Yes)
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle(u"提示")
        msg_box.setText(u" 请拖入需要合并的文件")
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes)
        btn_yes = msg_box.button(QtWidgets.QMessageBox.Yes)
        btn_yes.setText(u"确认")
        msg_box.exec_()

    def get_maya_path_list(self):
        file_path_list = list()
        count_number = self.lwt_maya_file.count()
        if count_number > 0:
            for _count in range(count_number):
                file_path_list.append(self.lwt_maya_file.item(_count).text())
        return file_path_list
    
    def get_fbx_path_list(self):
        file_path_str = ""
        count_number = self.lwt_fbx_file.count()
        if count_number > 0:
            for _count in range(count_number):
                file_path_str += f"{self.lwt_fbx_file.item(_count).text()} "
        return file_path_str
    
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    win = BatchCloth()
    win.show()
    sys.exit(app.exec_())
    