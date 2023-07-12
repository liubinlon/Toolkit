from PySide2 import QtWidgets, QtCore, QtGui
import os, sys
import subprocess
import inspect
import shutil

# com_path = os.path.abspath(os.path.join(os.path.abspath(inspect.getsourcefile(lambda: 0)), '../../..'))
com_path = os.path.abspath(os.path.join(os.path.abspath(__file__), '../../..'))

if com_path not in sys.path:
    sys.path.append(com_path)
    
from command.commonly_ui import CommonlyUi
from command.commonly_operation import CommonlyOperation

NAME = "Bone rename - v001"

class MSignals(QtCore.QObject):

    finish_signal = QtCore.Signal(str)
    undone_signal = QtCore.Signal(str)
    progress_bar = QtCore.Signal(float)
    
    def __init__(self):
        super().__init__()
    
    def rename_bone(self, file_directory):
        """
            遍历文件夹下的ma文件。
        Args:
            file_directory (url): Chars文件夹绝对路径
        """
        if not file_directory:
            return
        file_lst = self.get_maya_file(file_directory)
        file_number = 100.0/len(file_lst)
        for index, _file in enumerate(file_lst):
            self.progress_bar.emit((index+1)*file_number/2.0)
            cmd = '"c:/Program Files/Autodesk/Maya2020/bin/mayapy.exe" {}/bach/batch_background_renaming/background_renaming_com.py {}'.format(com_path, _file)
            result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = result.communicate()
            output = output.decode("utf-8").strip()
            if "Open file failed" in output:
                self.undone_signal.emit(str(_file))
            elif "Open file succeeded" in output:
                self.finish_signal.emit(str(_file))
            self.progress_bar.emit((index+1)*file_number)
        QtWidgets.QMessageBox.information(self, "information", u"完成!")
                     
    def get_maya_file(self, pro_path):
        lst_maya = list()
        """
            获取目录下的maya文件列表
            return: 返回maya文件列表
        """
        chars_path = os.path.join(pro_path, "Assets/Chars")
        chars_lst = os.listdir(chars_path)
        for c in chars_lst:
            rig_dir = os.path.join(chars_path, c, "Rig")
            if not os.path.isdir(rig_dir):
                continue
            adv_bone = os.path.join(rig_dir, "Beakup_ADV")
            if not os.path.isdir(adv_bone):
                os.mkdir(adv_bone)
            for _file in os.listdir(rig_dir):
                _file_path = os.path.join(rig_dir, _file)
                adv_bone_path = os.path.join(adv_bone, _file)
                if os.path.isdir(_file_path):
                    continue
                shutil.copyfile(_file_path, adv_bone_path)
                if _file_path.endswith(".mb"):
                    lst_maya.append(_file_path)
        return lst_maya
      
class BoneRename(QtWidgets.QMainWindow):
    break_thread = QtCore.Signal(str)
    """
        后台对maya绑定文件骨骼进行ue命名转换, 最终适配ue骨骼重定向, 并导出fbx文件, 将原有文件进行备份
    """
    def __init__(self, parent=None):
        super(BoneRename, self).__init__(parent)
        self.ui_file = CommonlyUi.ui_loader("{}/bach/batch_background_renaming/background_renaming.ui".format(com_path))       
        self.output_data = dict()
        self.stuff_ui()
        self.set_thread()
       
    def stuff_ui(self):
        """
            对ui文件进行编辑, 链接按钮相关函数
        """
        self.setObjectName(NAME)
        self.setWindowTitle(NAME)
        self.resize(800, 600)
        app_icon = QtGui.QIcon(f"{com_path}/icons/renaming_logo.png")
        self.setWindowIcon(app_icon)
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.addWidget(self.ui_file)
        self.setLayout(main_layout)
        self.setCentralWidget(self.ui_file)
        # 按钮链接功能
        self.ui_file.btn_open.clicked.connect(self._open)
        self.ui_file.btn_output_data.clicked.connect(self.save_data)
        self.ui_file.btn_run.clicked.connect(self.start_thread)
        self.ui_file.btn_clear_data.clicked.connect(self.clear_data)
    
    def set_thread(self):
        """
            创建新的进程
        """
        self.thread1 = QtCore.QThread(self)  # 创建一个线程
        self.range_thread = MSignals()  # 实例化线程类
        self.range_thread.moveToThread(self.thread1)  # 将类移动到线程中运行
        # 线程数据传回信号，用add_item函数处理
        self.range_thread.undone_signal.connect(self.updata_undone)
        self.range_thread.finish_signal.connect(self.updata_finish)
        self.range_thread.progress_bar.connect(self.updata_progre)
        self.break_thread.connect(self.range_thread.rename_bone)
    
    def start_thread(self):
        self.thread1.start()
        self.break_thread.emit(self.get_file_directory())
        
        
    def updata_undone(self, str):
        self.ui_file.ptet_undone.appendPlainText(str)
    
    def updata_finish(self, str):
        self.ui_file.ptet_finish.appendPlainText(str)
        
    def updata_progre(self, num):
        self.ui_file.progress_bar.setValue(num)

       
    def directory_dilog(self, path_data):
        """
            打开文本框
        """
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        dialog.setViewMode(QtWidgets.QFileDialog.Detail)
        if dialog.exec_():
            file_name = (dialog.selectedFiles())[0]
            path_data.setText(file_name)
            return file_name
        else:
            QtWidgets.QMessageBox.warning(self, "warning", "Please select directory")
    
    def file_dilog(self):
        """
            打开文本框
        """
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        dialog.setViewMode(QtWidgets.QFileDialog.Detail)
        fileName = dialog.getSaveFileName(self,u"保存文件", os.getcwd(), filter="*.json")[0]
        return fileName
    
    def _open(self):
        """
            打开项目文件夹
        """
        self.directory_dilog(self.ui_file.let_file_directory)
        
    def save_data(self):
        """
            保存数据为json文件
        """
        out_put_dic = dict()
        file_name = self.file_dilog()
        if self.get_finish_signal():
            out_put_dic["finish"] = [_text for _text in self.ui_file.ptet_finish.toPlainText().split("\n")]         
        if self.get_undone_signal():
            out_put_dic["undone"] = [_text for _text in self.ui_file.ptet_undone.toPlainText().split("\n")]
        CommonlyOperation.save_json_data(file_name, out_put_dic)
       
    def get_finish_data(self):
        """
            获取完成的文件路径符串
        Returns:
            string: 字符串
        """
        if not self.ui_file.ptet_finish.text():
            return
        return self.ui_file.ptet_finish.text()
    
    def get_finish_signal(self):
        """
            判断finish信号
        Returns:
            _type_: bool
        """
        if self.ui_file.cbox_finish.checkState() == QtCore.Qt.CheckState.Checked:
            return True
        return False
    
    def get_undone_signal(self):
        """
            判断undone信号
        Returns:
            _type_: bool
        """
        if self.ui_file.cbox_undone.checkState() == QtCore.Qt.CheckState.Checked:
            return True
        return False
    
    def clear_data(self):
        """
            删除显示栏显示的文字, 归零进度条
        """
        self.ui_file.ptet_undone.clear()
        self.ui_file.ptet_finish.clear()
        self.ui_file.progress_bar.setValue(0)
        
        
    def get_undone_data(self):
        """
            获取未完成的文件路径符串
        Returns:
            string: 字符串
        """
        if not self.ui_file.ptet_undone.text():
            return
        return self.ui_file.ptet_undone.text()
    
    def get_file_directory(self):
        """
            获取路径
        Returns:
            string: 如果存在返回工作路径，默认返回当前电脑用户路径
        """
        if not self.ui_file.let_file_directory.text():
            return os.environ["HOME"]
        return self.ui_file.let_file_directory.text()
       
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    win = BoneRename()
    win.show()
    sys.exit(app.exec_())