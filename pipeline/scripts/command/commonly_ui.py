#-*- coding:utf-8 -*-
"""
Load ui file
"""
from PySide2.QtUiTools import QUiLoader
import PySide2.QtCore as QtCore

class CommonlyUi:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def ui_loader(uiFile, css_name = None):
        loader = QUiLoader()
        uifile = QtCore.QFile(uiFile)
        uifile.open(QtCore.QFile.ReadOnly)
        window = loader.load(uifile)
        uifile.close()
        if css_name:
            with open(css_name, 'r') as css_file:
                style_sheet = css_file.read()
            window.setStyleSheet(style_sheet)
        return window