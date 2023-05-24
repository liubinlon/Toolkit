from PySide2 import QtWidgets, QtUiTools, QtCore
from threading import Thread
import os, sys

path = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
abs_dir = r"{0}".format(path)
if abs_dir not in sys.path:
    sys.path.append(abs_dir)

NAME = "Bone rename - v001"

class MSignals(object):
    """_summary_

    Args:
        object (_type_): _description_
    """
    QtCore.Signal(QtWidgets.QPlainTextEdit, QtWidgets.QProgressBar, str, int)


class BoneRename(object):
    """
        后台对maya绑定文件骨骼进行ue命名转换, 最终适配ue骨骼重定向, 并导出fbx文件, 将原有文件进行备份
    """
    def __init__(self):
        self.ui_file = self.load_ui_file("./background_renaming.ui")
    
    def load_ui_file(self, ui_file, css_name=None):
        """
            读取ui文件
        """
        lodager = QtUiTools.QUiLoader()
        _ui = QtCore.QFile(ui_file)
        _ui.open(QtCore.QFile.ReadOnly)
        _window = lodager.load(_ui)
        if css_name:
            with open(css_name, "r") as css_file:
                style_sheet = css_file.read()
            _window.setStyleSheet(style_sheet)
        return _window

    def stuff_ui(self):
        """
            
        """
        pass
    
    def get_maya_file(self):
        lst_maya = list()
        """
            获取目录下的maya文件列表
            return: 返回maya文件列表
        """
        return lst_maya
    
    def rename_bone(self):
        """
            获取文件中的骨骼层级, 按照ue骨骼的的名字进行命名
            并保存文件, 导出fbx文件
        """
    
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    win = BoneRename()
    win.show()
    sys.exit(app.exec_())