#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Time     : 2019/3/23 21:59
# Email    : spirit_az@foxmail.com
# File    : skirtRig
__author__ = 'ChenLiang.Miao'

import itertools
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
import os, inspect

# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
import pymel.core as pm

import createCtrl
import SkirtRexistsUI as exUI

# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
reload(createCtrl)
reload(exUI)


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
def getShape(transform):
    for each in pm.PyNode(transform).getShapes():
        if not each.intermediateObject.get():
            return each
    return False


def getModulesPath(moudle):
    '''
    return dir for imported moudle..
    '''
    moduleFile = inspect.getfile(moudle)
    modulePath = os.path.dirname(moduleFile)
    return modulePath


def getScriptPath():
    '''
    return dir path for used script..
    '''
    scriptPath = getModulesPath(inspect.currentframe().f_back)
    return scriptPath


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
maya_win = exUI.GetMayaMainWindow()
__abs_path__ = getScriptPath().replace('\\', '/')
main_win_name = 'Skirt Rig'
scriptVersion = 'v1.5'


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #


def icon_path(in_name):
    # return in_name
    return os.path.join(os.path.dirname(__abs_path__), 'icons', in_name).replace('\\', '/')


def getUIPath():
    return os.path.join(__abs_path__, 'UI/ui_SkirtRig.ui').replace('\\', '/')


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
windowClss, baseClass = exUI.loadUi(getUIPath())


class skirtUI(windowClss, baseClass):
    def __init__(self, parent=maya_win):
        super(skirtUI, self).__init__(parent)
        self.setupUi(self)

        self._bt_clicked()

    def _bt_clicked(self):
        self.pushButton_surface.clicked.connect(self.pushButton_surface_clicked)
        self.pushButton_buildCtrl.clicked.connect(self.pushButton_buildCtrl_clicked)

    def pushButton_surface_clicked(self):
        basedOnType = 'nurbsSurface' if self.radioButton_surface.isChecked() else 'mesh'
        sel = pm.ls(sl=True)
        if not sel:
            self.lineEdit_surface.clear()
            self.lineEdit_surface.setText('')
        else:
            shape = sel[0].getShape()
            if shape.type() != basedOnType:
                self.lineEdit_surface.clear()
            else:
                self.lineEdit_surface.setText(sel[0].name())

    def pushButton_buildCtrl_clicked(self):
        isSurface = self.radioButton_surface.isChecked()
        surfaceTrans = str(self.lineEdit_surface.text())
        shape = getShape(surfaceTrans)
        atr, array = self.getUV()
        endEffector = self.checkBox_endEffector.isChecked()
        # create ctrl
        createCtrl.skirtBuildCtrl(shape, atr, array, endEffector=endEffector, isSurface=isSurface)

    def getUV(self):
        isClose = self.checkBox_isClose.isChecked()
        isV = self.radioButton_V.isChecked()

        uNumber = self.spinBox_U.value()
        vNumber = self.spinBox_V.value()

        uOffset = 1.00 / (uNumber - 1) if (uNumber - 1) else 1
        vOffset = 1.00 / (vNumber - 1) if (vNumber - 1) else 1

        uList = [each * uOffset for each in range(uNumber)]
        vList = [each * vOffset for each in range(vNumber)]
        if isClose:
            if isV:
                vOffset = 1.00 / vNumber
                vList = [each * vOffset for each in range(vNumber)]
            else:
                uOffset = 1.00 / uNumber
                uList = [each * uOffset for each in range(uNumber)]

        if uNumber == 1:
            uList = [0.5]

        if vNumber == 1:
            vList = [0.5]

        vList.reverse()
        uList.reverse()

        isU, atr = True, ['parameterU', 'parameterV'] if self.radioButton_surface.isChecked() else ['parameterU', 'parameterV']
        if isV:
            isU, atr = False, ['parameterV', 'parameterU'] if self.radioButton_surface.isChecked() else ['parameterV', 'parameterU']

        pList = [uList, vList]
        if not isU:
            pList = [vList, uList]

        newList = list()
        tempList = list(itertools.product(*pList))
        u = 0
        for i in range(len(pList[0])):
            nList = list()
            for k in range(len(pList[1])):
                nList.append(tempList[u])
                u += 1
            newList.append(nList)
        return atr, newList


def show():
    if exUI.Raise(main_win_name):
        exUI.deleteUI(main_win_name)

    ui = skirtUI()  # type: exUI.QMainWindow
    ui.setObjectName(main_win_name)
    ui.setWindowTitle('{0} {1}'.format(main_win_name, scriptVersion))
    ui.setWindowIcon(exUI.QIcon(icon_path('MCL.png')))
    ui.show()
