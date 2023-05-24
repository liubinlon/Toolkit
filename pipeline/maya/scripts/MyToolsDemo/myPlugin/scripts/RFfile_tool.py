#coding=utf-8
import os
import sys

from PySide2.QtCore import Qt, QMetaObject
import PySide2.QtWidgets as QtWidgets
from PySide2 import QtCore, QtGui

path = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
Dir = r"{0}".format(path)
if Dir not in sys.path:
    sys.path.append(Dir)

from uiLoader.FU import uiLoader
from jointTool.RFfile import RFfile

class RFfile_tool(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super(RFfile_tool, self).__init__(parent)        

        if parent:
            self.setWindowFlags(parent.windowFlags())
        
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle(u"RFfile_tool")
        self.resize(800, 420)
        
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        # self.initSize(0.2)    
        # self.raise_()
        self.initInstance() 
        self.setIcon()
        self.initUI()
        # self.setStyleSheet("""{background-color: rgb(56, 56, 56);border-top-right-radius:5px;border-bottom-right-radius:5px;border-top-left-radius:5px;border-bottom-left-radius:5px;}""")
        # self.set_sheet()

        mainlayout = QtWidgets.QGridLayout()
        mainlayout.addWidget(self.mainWidget)
        mainlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mainlayout)
        self.setCentralWidget(self.mainWidget)
        QMetaObject.connectSlotsByName(mainlayout)

    def setIcon(self):
        app_icon = QtGui.QIcon(r"{0}/icons/logo.png".format(path))
        self.setWindowIcon(app_icon)

    # def set_sheet(self):
    # #     # self.QtGui.setBrush(QtGui.QColor(255, 0, 0, 127))
    #     self.setStyleSheet("""
    #         background-color:rgb(93, 93, 93);
    #         border-top-right-radius:2px;
    #         border-bottom-right-radius:2px;
    #         border-top-left-radius:2px;
    #         border-bottom-left-radius:2px;
    #     """)

    def initSize(self, rate):
        desktop = QtWidgets.QApplication.desktop()
        self.screenWidth = desktop.width() * rate
        self.screenHeight = desktop.height() * rate
        self.resize(self.screenWidth, self.screenHeight)

    def initInstance(self):
        """Initialize the command script"""        
        self.RFfile = RFfile()

    def initUI(self):
        """Read ui file, bind command to the ui and load"""
        path = os.path.split(os.path.dirname(__file__))[0]
        uiFile = (r"{0}/uifile/RFfile.ui".format(path))
        self.mainWidget = uiLoader(uiFile)

        btn_import_excel_modle = self.mainWidget.findChild(QtWidgets.QPushButton, "btn_excel_import")
        redata = btn_import_excel_modle.clicked.connect(self.RFfile.import_file)

        btn_file_path_modle = self.mainWidget.findChild(QtWidgets.QPushButton, "btn_open_file_path")
        btn_file_path_modle.clicked.connect(self.RFfile.open_file_path)

        btn_old_path_modle = self.mainWidget.findChild(QtWidgets.QPushButton, "btn_old_file")
        btn_old_path_modle.clicked.connect(self.RFfile.open_old_file)

        btn_new_path_modle = self.mainWidget.findChild(QtWidgets.QPushButton, "btn_new_file")
        btn_new_path_modle.clicked.connect(self.RFfile.open_new_file)

        btn_run_reference_modle = self.mainWidget.findChild(QtWidgets.QPushButton, "btn_reference")
        btn_run_reference_modle.clicked.connect(self.RFfile.run_reference)
        
        # pbr_line_modle = self.mainWidget.findChild(QtWidgets.QProgressBar, "pbr_line")
        self.RFfile.cbb_display_mod = self.mainWidget.findChild(QtWidgets.QComboBox, "cbb_displaymod")
        self.RFfile.cbb_display_dir = self.mainWidget.findChild(QtWidgets.QComboBox, "cbb_displaydir")
        # item_list = self.RFfile.cbx_display_mod()
        # cbx_displaymod_modle.addItems(item_list)

        self.RFfile.let_excle_file = self.mainWidget.findChild(QtWidgets.QLineEdit, "let_excel")
        self.RFfile.let_file_path = self.mainWidget.findChild(QtWidgets.QLineEdit, "let_path")
        self.RFfile.let_new_file = self.mainWidget.findChild(QtWidgets.QLineEdit, "let_newfilename")
        self.RFfile.let_old_file = self.mainWidget.findChild(QtWidgets.QLineEdit, "let_oldfilename")
        self.RFfile.lsv_file_list = self.mainWidget.findChild(QtWidgets.QTextBrowser, "tbr_filelist")
        # self.RFfile.lsv_file_list.Flow(QtWidgets.QListView.TopToBottom)


def main():
    app = QtWidgets.QApplication([])
    win = RFfile_tool()
    win.show()
    sys.exit(app.exec_())
    
    # # try:
    # #     win.close()
    # # except:
    # #     pass
    # #     # win.show()
    # win = RFfile_tool()
    # win.show()

if __name__ == "__main__":
    main()