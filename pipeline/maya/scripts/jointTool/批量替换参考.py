# import maya.cmds as cmds
# from pySide2 import QtCore, QtWidgets, QtGui
# path = "W:\gchd\ase\character\warrior\rig\check\gchd_rig_warrior_liuzhenbao.ma"
# newpath = eval(repr(path).replace("\\", "/"))
# selectlist = cmds.ls(sl = True)
# for i in selectlist:
#     cmds.file(newpath, loadReference = str(i), options = "v=0;")
# point


class Point:

    def __init__(self, xx, yy, zz, ww=1):
        self.x = xx
        self.y = yy
        self.z = zz
        self.w = ww

    def __getitem__(self, item):
        return [self.x, self.y, self.z, self.w][item]

class Vceter:

    def __init__(self, xx, yy, zz, ww=1):
        self.x = xx
        self.y = yy
        self.z = zz
        self.w = ww

    def __sub__(self, other):
        return [other - self.x, other - self.y, other - self.z, other - self.w]

    def __getitem__(self, item):
        return [self.x, self.y, self.z, self.w][item]
