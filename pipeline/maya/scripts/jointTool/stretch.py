#-*- coding: utf-8 -*-
from PySide2.QtUiTools import QUiLoader
import PySide2.QtCore as QtCore

import maya.cmds as cmds


def CreatJin(RangeNumber, objselection):
    global objCI, TopJoint
    objcurve = objselection[0]
    objShape = "%sShape" % objcurve
    objCI = cmds.createNode("curveInfo", n = '%sInfo' % objselection[0])
    cmds.connectAttr("%s.worldSpace[0]" % objShape, "%s.inputCurve" % objCI)
    getCrvLong = cmds.getAttr("%s.arcLength" % objCI)
    jointLong = getCrvLong / (int(RangeNumber) - 1)
    for i in range(0, int(RangeNumber)):
        cmds.createNode("joint", name = "%s%s_Jin" % (objselection[0], i))
        if i > 0:
            newjoint = ("%s%s_Jin" % (objselection[0], i))
            if newjoint:
                cmds.parent(newjoint, ("%s%s_Jin" % (objselection[0], i - 1)))
                cmds.setAttr("%s.translateX" % newjoint, jointLong)
        else:
            continue
    TopJoint = ("%s%s_Jin" % (objselection[0], 0))
    return TopJoint

# gets joint list
def ListCompJoint(TopJoint, withEndJoints = True):
    ListedJoints = cmds.listRelatives(TopJoint, type = 'joint', ad = True)
    ListedJoints.append(TopJoint)
    ListedJoints.reverse()
    CompleteJoints = ListedJoints[:]
    if not withEndJoints:
        CompleteJoints = [Joint for Joint in ListedJoints if cmds.listRelatives(Joint, c = 1, type = "joint")]
    return CompleteJoints

# selecting joint and curves create ikSplineSolver
def Greateikspline(ListCompJoint, objselection):
    global crv, ikhandle
    objik = ListCompJoint[0], ListCompJoint[-1], objselection[0]
    cmds.select(objik)
    ikhandle = cmds.ikHandle(sol = "ikSplineSolver", ccv = False, scv = False, pcv = False, ns = 3)
    crv = cmds.circle(name = "Stretch_con", c = (0, 0, 0), nr = (0, 1, 0), sw = 360, r = 5, d = 3, ch = -1)
    cmds.setAttr((crv[0] + "Shape") + ".overrideEnabled", 1)
    cmds.setAttr((crv[0] + "Shape") + ".overrideColor", 18)
    attrName = ["twist", "roll", "offset"]
    for attr in attrName:
        cmds.addAttr(crv, longName = "%s" % attr, attributeType = "double", defaultValue = 0)
        cmds.setAttr(crv[0] + (".%s" % attr), keyable = True)
        cmds.connectAttr(crv[0] + ".%s" % attr, ikhandle[0] + ".%s" % attr)
    cmds.select(clear = True)

# create joint scale
def GreateScale(List, objselection):
    cmds.addAttr(crv, longName = "jointscale", attributeType = "double", defaultValue = 1)
    cmds.setAttr(crv[0] + ".jointscale", keyable = True)
    objLen = len(List)
    JinDivide = cmds.createNode('multiplyDivide', n = objselection[0] + 'JinDivide')
    cmds.setAttr("%s.operation" % JinDivide, 2)
    ConDivide = cmds.createNode('multiplyDivide', n = objselection[0] + 'ConDivide')
    # cmds.setAttr("%s.operation" % conToJin, 2)
    # conToJin = cmds.createNode("multiplyDivide", n = objselection[0] + 'conToJin')
    cmds.setAttr("%s.operation" % ConDivide, 2)
    cmds.connectAttr("%s.arcLength" % objCI, "%s.input1X" % JinDivide)
    cmds.connectAttr("%s.outputX" % JinDivide, "%s.input1X" % ConDivide)
    cmds.connectAttr(crv[0] + ".scaleX", ConDivide + ".input2X")
    # cmds.setAttr("%s.input2X" % conToJin, 1)
    CInumber = cmds.getAttr("%s.arcLength" % objCI)
    cmds.setAttr("%s.input2X" % JinDivide, CInumber)
    JinLong = CInumber / (objLen - 1)
    for i in range(1, objLen):
        cmds.setAttr("%s.translateX" % List[i], JinLong)
    for i in range(0, objLen - 1):
        cmds.connectAttr("%s.outputX" % ConDivide, "%s.scaleX" % List[i])

def creatLocator(objselection):
    global crvList
    conlocator = cmds.getAttr("%s.cv[:]" % objselection[0])
    crvList = []
    for i in range(0, len(conlocator)):
        locator = cmds.createNode('transform', n=("%s%d_Lct" % (objselection[0], i)))
        locatorShape = cmds.createNode('locator', n=(locator + "Shape"), p=locator)
        cmds.setAttr(locatorShape + ".lodVisibility", 0)
        cmds.setAttr("%s.translate" % locator, (conlocator[i])[0], (conlocator[i])[1], (conlocator[i])[2])
        cmds.setAttr((locator + "Shape") + ".overrideEnabled", 1)
        cmds.setAttr((locator + "Shape") + ".overrideColor", 17)
        concrv = cmds.circle(name=("%s%d_Con" % (objselection[0], i)), c=(0, 0, 0), nr=(1, 0, 0), sw=360, r=1, d=3, ch=-1)
        crvList.append(concrv[0])
        drivergrp = cmds.group(concrv, name = concrv[0] + "Driver")
        animgrp = cmds.group(drivergrp, name = concrv[0] + "Anim")
        cmds.delete(cmds.parentConstraint(locator, animgrp, weight=True))
        cmds.parent(animgrp, crv)
        cmds.setAttr((concrv[0] + "Shape") + ".overrideEnabled", 1)
        cmds.setAttr((concrv[0] + "Shape") + ".overrideColor", 6)
        cmds.parent(locator, concrv)
        cmds.makeIdentity(locator, apply=True, t=1, r=1, s=1, n=0, pn=1)
        cmds.connectAttr("%s.worldPosition[0]" % (locator + "Shape"), "%s.controlPoints[%d]" % ((objselection[0] + "Shape"), i))

def addSine(objselection):
    cmds.addAttr(crv, longName = "__________", at = "enum", en = "sine:")
    cmds.setAttr("%s.__________" % crv[0], keyable = True)
    cmds.addAttr(crv, ln = "amplitude", at = "double", min = -5, max = 5, dv = 0)
    cmds.setAttr("%s.amplitude" % crv[0], keyable = True)
    cmds.addAttr(crv, longName = "wavelength", at = "double", defaultValue = 2)
    cmds.setAttr("%s.wavelength" % crv[0], keyable=True)
    cmds.addAttr(crv, longName = "sine_offset", at = "double", dv = 0)
    cmds.setAttr("%s.sine_offset" % crv[0], keyable = True)
    crvList.append(objselection[0])
    print crvList
    sine = cmds.nonLinear(crvList, type = "sine")
    newSine = cmds.rename(sine[0], objselection[0] + "Sine")
    attrName = ["amplitude", "wavelength"]
    for attr in attrName:
        cmds.connectAttr("%s.%s" % (crv[0], attr), newSine + ".%s" % attr)
    # cmds.connectAttr("%s.sine_offset" % crv[0], newSine + ".offset")
    cmds.expression(s = "%s.offset = %s.sine_offset * time" % (newSine, crv[0]), o = "default", ae = 1, uc = "all")

def finishing(objselection):
    cmds.group((objselection[0], ikhandle[0]), name=objselection[0] + "setup")
    cmds.parent(TopJoint, crv)