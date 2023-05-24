#-*- coding: utf-8 -*-
import os
import sys
import maya.cmds as cmds

def contorllerNaming(obj, alias):
    objStr = str(obj)
    objName = objStr.split('_')
    strName = objName[0]
    longName = len(strName)

    for i in range(longName):
        if str(strName)[i].isdigit():
            numberLocation = i
            objStr = strName[:numberLocation]
            objNumb = strName[numberLocation:]
            newName = objStr + alias + objNumb
        else:
            newName = strName + alias

    objName[0] = newName
    objNewName = "_".join(objName)
    return objNewName