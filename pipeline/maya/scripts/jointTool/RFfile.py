# coding=utf-8
import os
import re
import sys
import shutil
import codecs
import pathlib2
import time
import threading

try:
    from PySide.QtCore import Qt
    import PySide.QtWidgets as QtWidgets
    from PySide import QtCore, QtGui
except:
    from PySide2.QtCore import Qt
    import PySide2.QtWidgets as QtWidgets
    from PySide2 import QtCore, QtGui

path = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
Dir = r"{0}".format(path)
if Dir not in sys.path:
    sys.path.append(Dir)


class RFfile:
    def __init__(self):
        self.let_excle_file = None
        self.let_file_path = None
        self.let_old_file = None
        self.let_new_file = None
        self.cbx_file_backup = None
        self.cbb_display_mod = None
        self.cbb_display_dir = None
        self.lsv_file_list = None

    def open_file_dialog(self, pathdata):
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        dialog.setViewMode(QtWidgets.QFileDialog.Detail)
        if dialog.exec_():
            file_name = (dialog.selectedFiles())[0]
            pathdata.setText(file_name)
            # return file_name
        else:
            QtWidgets.QMessageBox.warning(self, "warning", "Please select directory")
        return file_name

    def open_directory_dialog(self, pathdata):
        directory = QtWidgets.QFileDialog()
        directory.setFileMode(QtWidgets.QFileDialog.Directory)
        directory.setViewMode(QtWidgets.QFileDialog.Detail)
        if directory.exec_():
            directory_name = directory.selectedFiles()
            directory_new_name = directory_name[0]
            # print(file_name)
            pathdata.setText(directory_new_name)
            # print (type(file_name[0]))
            folder_name = os.path.basename(directory_new_name)
        else:
            QtWidgets.QMessageBox.warning(self, "warning", "Please select folder")
        return directory_new_name, folder_name

    def import_file(self, path_data):
        # global file_list
        path_data = self.open_file_dialog(self.let_excle_file)
        f = open(path_data)
        self.list_view("lens file: "+path_data)
        self.file_list = f.readlines()
        for num in range(len(self.file_list)):
            self.file_list[num] = "%06d" % int(self.file_list[num].rstrip())
        # return self.file_list 

    def get_folder_directory(self, path):
        directory_list = []
        path_data = pathlib2.Path(path)
        for entry in path_data.iterdir():
            if entry.is_dir():
                if bool(re.search(r"\d", entry.name)) and re.findall("\d+", entry.name)[0] in self.file_list:
                    directory_list.append(entry.name)
        # print(directory_list)    
        return directory_list

    # def is_sub_string(self, substrlist, filetype):

    # flag = True
    # for substr in substrlist:
    #     if not(substr in filetype):
    #         flag = False
    # return flag

    def get_file_list(self, findpath):
        # filelsit = []
        filename = os.listdir(findpath)
        for i in filename:
            if os.path.splitext(i)[1] == ".ma" or os.path.splitext(i)[1] == ".mb":
                if filename:
                    filename.sort(key=lambda fn: os.path.getmtime(findpath+"/"+fn) if not os.path.isdir(
                        findpath + "/" + fn) else 0)
                    file_str = os.path.join(findpath, filename[-1])
                    file_str = file_str.replace("\\", "/")
                else:
                    QtWidgets.QMessageBox.warning(self, "warning", "Empty folder")
                    break
                    # file_str = print("directory not folder")
                    # break

        # if (len(filename) > 0):
        #     for fn in filename:
        #         if (len(flagstr) > 0):
        #             if self.is_sub_string(flagstr, fn):
        #                 fullfilename = os.path.join(findpath, fn)
        #                 filelsit.append(fullfilename)
        #         else:
        #             fullfilename = os.path.join(findpath, fn)
        # #             filelsit.append(fullfilename)
        # if len(filelsit) > 0:
        #     filelsit.sort(key=lambda fn : os.path.getmtime(findpath+"/"+fn) if not os.path.isdir(findpath+"/"+fn) else 0)
        #     file_str = os.path.join(findpath, filelsit[-1])
        #     # file_new.replace("\\", "/")
        return file_str

    def load_file_data(self, latestfile, filte, new_file_name):
        pattern = re.compile('".*?"')
        # progressBar = QProgressDialog()
        with codecs.open(latestfile, "rb", "gbk") as old_file:
            a_lines = old_file.readlines()
            b_lines = a_lines[:]
        for num, line in enumerate(a_lines):
            if line.count("requires"):
                break
            if pattern.findall(line):
                old_ref = pattern.findall(line)[-1][1:-1]
                if old_ref == filte:
                    # insertPos = old_ref.rfind(".")
                    new_ref = new_file_name
                    b_lines[num] = line.replace(filte, new_ref)
        with codecs.open(latestfile, "w", "gbk") as new_file:
            for line in b_lines:
                new_file.write(line)

    def open_file_path(self):
        # global complete_list
        """
        open the shot path to work
        """
        ani = self.get_display_mod()
        work = self.get_display_dir()
        self.complete_list = []
        directory_path = self.open_directory_dialog(self.let_file_path)
        self.folder_list = self.get_folder_directory(directory_path[0])
        self.list_view("Project directory: " + self.let_file_path.text())
        for f in self.folder_list:
            pathstr = ("%s/%s/%s/%s" % (directory_path[0], f, ani, work))
            latest_file = self.get_file_list(pathstr)
            self.complete_list.append(latest_file)

        # directory_data = os.path.split(os.path.dirname(directory_path))
        # print(directory_data)
        # print("open_file_path")
        # return complete_list

    def open_old_file(self):
        # global old_file_name
        """get old file path and name"""

        self.old_file_name = self.open_file_dialog(self.let_old_file)
        self.list_view("Old file: " + self.old_file_name)
        # return old_file_name

    def open_new_file(self):
        # global new_file_name
        """get new file path and name"""
        self.new_file_name = self.open_file_dialog(self.let_new_file)
        self.list_view("Now file: " + self.new_file_name)
        # return new_file_name

    # def cbx_display_mod(self):
    #     def_folder = self.get_folder_directory(Dir)
    #     if self.folder_list:
    #         return self.folder_list
    #         # return self.folder_list
    #     else:
    #         return def_folder        
    #         # return self.get_folder_directory(Dir)

    # def show_dialog(self, time_num):
    #     num = int(time_num)
    #     progress = QtWidgets.QProgressDialog(my_code, self)
    #     progress.setWindowTitle("请稍等")
    #     progress.setLabelText("正在替换...")
    #     progress.setConcelButtonText("取消")
    #     progress.setMinimumDuration(5)
    #     progress.setWindowModality(Qt.WindowModal)
    #     progress.setRange(0, num)

    #     for i in range(num):
    #         progress.setValue(i)
    #         if progress.wasCanceled():
    #             QtWidgets.QMessageBox.warning(self, "提示", "操作失败")
    #             break

    #     progress.setValue(num)
    #     QtWidgets.QMessageBox.information(self, "提示", "操作成功")

    # def run(self):
    #     for f in self.complete_list:
    #         time_num = len(self.complete_list)
    #         self.load_file_data(f, self.old_file_name, self.new_file_name)
    #     return time_num

    def list_view(self, item):
        # model = QtGui.QStandardItemModel()
        # new_item = QtGui.QStandardItem(item)
        # new_item = QtGui.QStandardItemModel.setItem(numb, new_item)
        # model.appendRow(new_item)
        # if setmodel == True:
        self.lsv_file_list.append(item)

    def run_reference(self):
        self.list_view("Please wait a moment....")
        # directory_path = self.open_directory_dialog(self.let_file_path)
        # folder_name = self.get_folder_directory(directory_path[0])
        # latest_file = self.open_file_path(directory_path, folder_name)
        # old_ref = self.open_old_file()
        # new_ref = self.open_new_file()

        for f in self.complete_list:
            self.list_view("Executable files: " + f)
            self.list_view("-------------------")
            self.load_file_data(f, self.old_file_name, self.new_file_name)
            # time_num = len(self.complete_list)
            # thread1 = threading.Thread(traget = self.show_dialog, args = (time_num,))
            # thread2 = threading.Thread(traget = self.load_file_data, args = (f, self.old_file_name, self.new_file_name,))
            # thread1.start()
            # thread2.start()
        self.list_view("Complete!!!")
        """replaced file"""

    def run_rander(self):
        """exec rander"""
        print("run_reference")

    def get_excel_file(self):
        if not self.let_excle_file:
            return
        return self.let_excle_file.text()

    def get_file_path(self):
        if not self.let_file_path:
            return
        return self.let_file_path.text()

    def get_old_file(self):
        if not self.let_old_file:
            return
        return self.let_old_file.text()

    def get_new_file(self):
        if not self.let_new_file:
            return
        return self.let_new_file.text()

    def get_file_backup(self):
        if not self.cbx_file_backup:
            return
        if self.cbx_file_backup.checkState() == QtCore.Qt.CheckState.Checked:
            return True
        else:
            return False

    def get_display_mod(self):
        if not self.cbb_display_mod:
            return
        return self.cbb_display_mod.currentText()

    def get_display_dir(self):
        if not self.cbb_display_dir:
            return
        return self.cbb_display_dir.currentText()

    # def main(self):
    #     import_file()
    #     open_file_path()
    #     open_new_file()
    #     run_reference()
    #     run_rander()

# if __name__ == "__main__":
#     obj = RFfile()
#     obj.main()
