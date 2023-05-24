#-*- coding: utf-8 -*-
import PySide2.QtWidgets as QtWidgets
from PySide2 import QtCore, QtGui

import maya.cmds as cmds


def jointNaming(obj, alias, objNumb):
    objStr = str(obj)
    objName = objStr.split('_')
    strName = objName[0]
    longName = len(strName)

    for i in range(longName):
        if str(strName)[i].isdigit():
            numberLocation = i
            objStr = strName[:numberLocation]
            newName = objStr + alias + str(objNumb)
        else:
            newName = strName + alias

    objName[0] = newName
    objNewName = "_".join(objName)
    return objNewName

def addJoint(startJoint, partsNumber):
    endJoint = cmds.listRelatives(startJoint, type = "joint")
    rad = cmds.getAttr(startJoint + ".radius")
    fpos = cmds.xform(startJoint, q = 1, ws = 1, t = 1)
    spos = cmds.xform(endJoint, q = 1, ws = 1, t = 1)  
    for i in range(partsNumber):
        newJoint = cmds.insertJoint(startJoint)
        jointNewName = cmds.rename(newJoint, jointNaming(newJoint, "Part", (partsNumber - i)))
        newpos0 = spos[0] + (((fpos[0] - spos[0]) / (partsNumber + 1)) * (i + 1))
        newpos1 = spos[1] + (((fpos[1] - spos[1]) / (partsNumber + 1)) * (i + 1))
        newpos2 = spos[2] + (((fpos[2] - spos[2]) / (partsNumber + 1)) * (i + 1))
        cmds.joint(jointNewName, e = True, co = 1, position = (newpos0, newpos1, newpos2))
        cmds.setAttr(jointNewName + ".radius", rad)
    