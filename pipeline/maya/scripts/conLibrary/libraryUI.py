# -*- coding: utf-8 -*-
"""
author:MoFeioO
time:2020/10/25 11:23
"""
import pprint

from maya import cmds
import controllerLibrary
reload(controllerLibrary)
from PySide2 import QtWidgets, QtCore, QtGui


class ControllerLibraryUI(QtWidgets.QDialog):
    """
    The controllerLibraryUI is a dialog that lets us save and import controllers
    """
    def __init__(self):
        super(ControllerLibraryUI, self).__init__()

        self.setWindowTitle("Controller Library UI")
        # The library variable points to an instance of our controller library
        self.library = controllerLibrary.ControllerLibrary()
        # Every time we create a new instance, we will automatically build our UI and populate it
        self.buildUI()
        self.populate()

    def buildUI(self):
        """This method builds out the UI"""
        # This is the master layout
        layout = QtWidgets.QVBoxLayout(self)
        # This is the child horizontal widget
        save_widget = QtWidgets.QWidget()
        save_layout = QtWidgets.QHBoxLayout(save_widget)
        layout.addWidget(save_widget)

        self.save_name_field = QtWidgets.QLineEdit()
        save_layout.addWidget(self.save_name_field)

        save_btn = QtWidgets.QPushButton("save")
        save_btn.clicked.connect(self.save)
        save_layout.addWidget(save_btn)

        # These are the parameters for our thumbnail size
        size = 64
        buffer = 12
        # This will create a grid list widget to display our controller thumbnails
        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.setViewMode(QtWidgets.QListWidget.IconMode)
        self.list_widget.setIconSize(QtCore.QSize(size, size))
        self.list_widget.setGridSize(QtCore.QSize(size+buffer, size+buffer))
        self.list_widget.setResizeMode(QtWidgets.QListWidget.Adjust)
        layout.addWidget(self.list_widget)

        # This is our child widget that holds all the buttons
        btn_widget = QtWidgets.QWidget()
        btn_layout = QtWidgets.QHBoxLayout(btn_widget)
        layout.addWidget(btn_widget)

        import_btn = QtWidgets.QPushButton("import")
        import_btn.clicked.connect(self.load)
        btn_layout.addWidget(import_btn)

        refresh_btn = QtWidgets.QPushButton("refresh")
        refresh_btn.clicked.connect(self.populate)
        btn_layout.addWidget(refresh_btn)

        close_btn = QtWidgets.QPushButton("close")
        close_btn.clicked.connect(self.close)
        btn_layout.addWidget(close_btn)

    def populate(self):
        """This clears the listWidget and then repopulates it with the contents of our library"""
        self.list_widget.clear()
        self.library.find()

        for name, info in self.library.items():
            item = QtWidgets.QListWidgetItem(name)
            self.list_widget.addItem(item)

            screenshot = info.get("screenshot")
            if screenshot:
                icon = QtGui.QIcon(screenshot)
                item.setIcon(icon)

            item.setToolTip(pprint.pformat(info))

    def save(self):
        """
        This saves the controller with the given file name
        """
        name = self.save_name_field.text()
        if not name.strip():
            cmds.warning("You must give a name")
            return
        self.library.save(name)
        self.library.save_screenshot(name)
        self.populate()
        self.save_name_field.setText(" ")

    def load(self):
        """This loads the currently selected controller"""
        current_item = self.list_widget.currentItem()

        if not current_item:
            return

        name = current_item.text()

        self.library.load(name)

def showUI():
    """
    This shows and return a handle to the ui
    Returns:
        QDialog
    """
    win = ControllerLibraryUI()
    win.show()