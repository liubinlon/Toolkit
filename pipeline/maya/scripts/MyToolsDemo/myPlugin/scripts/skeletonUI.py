# /maya/
import os, sys


from PySide2 import QtCore, QtGui, QtWidgets
import maya.OpenMayaUI as omui
# from shiboken2 import wrapInstance

from


path = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]

Dir = r"{0}".format(path)

if dir not in sys.path:
    sys.path.append(Dir)


# def get_maya_window():
#     if __name__ == "__main__":
#         maya_par = omui.MQtUtil.mainWindow()
#         maya_window = wrapInstance(long(maya_par), QtWidgets.QMainWindow)
#         return maya_window


class Myskeleton(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Myskeleton, self).__init__(parent)
        self.setWindowTitle(u"skeleton")
        self.resize(330, 560)
        self.initInstance()
        self.initUI()

    def initInstance(self):
        pass

    def initUI(self):
        qtool_box = QtWidgets.QToolBox()
        qtbtn_body = qtool_box
        qtbtn_body.setItemText("body")
        qtbtn_body.setShortcutEnabled(checkable = True, checked = False)


def main():
    global win
    try:
        win.close()
    except:
        pass
    win = Myskeleton()
    win.show()


if __name__ == "__main__":
    main()
