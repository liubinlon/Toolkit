#coding=utf-8
"""
Load ui file
"""

from PySide2.QtUiTools import QUiLoader
import PySide2.QtCore as QtCore


def ui_loader(ui_file, css_name=None):
    lodager = QUiLoader()
    _ui = QtCore.QFile(ui_file)
    _ui.open(QtCore.QFile.ReadOnly)
    _window = loader.load(_ui)
    if css_name:
        with open(css_name, "r") as css_file:
            style_sheet = css_file.read()
        _window.setStyleSheet(style_sheet)
    return _window