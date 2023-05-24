#-*- coding: utf-8 -*-

import os
import sys

import logging
logging.raiseExceptions = False

path = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]

Dir = r"{0}".format(path)
if Dir not in sys.path:
    sys.path.append(Dir)

import PySide2.QtCore as QtCore

import maya.api.OpenMaya as om
import maya.cmds as cmds

from renaming import contorllerNaming
from PartJoint import addJoint
from stretch import*
from contorllerShape import*
from RivetLocator import*

class btnjnt:
    def __init__(self):
        self.addPartValue = None
        self.stretchJointValue = None
        self.modelName = None
        self.contorllerScaleValue = None
        self.contorllerName = None
        self.addsineValue = None
        self.addtensileValue = None
        self.addContorller = None

    def addpart(self):
        partsNumber = self.getAddPartValue()
        startJoint = cmds.ls(sl = True)
        print partsNumber

        addJoint(startJoint[0], partsNumber)

    def stretch(self):
        RangeNumber = self.getStretchValue()
        checkSine = self.getSineValue()
        checkTensile = self.getTensileValue()
        objselection = cmds.ls(sl=True)

        print RangeNumber
        if len(objselection) == 0:
            cmds.confirmDialog(title='Notice!', message='Please Select One of Object!')
            return
        if checkSine == checkTensile and checkSine == True:
            Objlist = ListCompJoint(CreatJin(RangeNumber, objselection))
            Greateikspline(Objlist, objselection)
            creatLocator(objselection)
            GreateScale(Objlist, objselection)
            addSine(objselection)
            finishing(objselection)
        elif checkSine != checkTensile and checkTensile == True:
            Objlist = ListCompJoint(CreatJin(RangeNumber, objselection))
            Greateikspline(Objlist, objselection)
            creatLocator(objselection)
            GreateScale(Objlist, objselection)
            finishing(objselection)
            # addSine(objselection)
        elif checkSine != checkTensile and checkSine == True:
            Objlist = ListCompJoint(CreatJin(RangeNumber, objselection))
            Greateikspline(Objlist, objselection)
            creatLocator(objselection)
            # GreateScale(Objlist, objselection)
            addSine(objselection)
            finishing(objselection)
        else:
            Objlist = ListCompJoint(CreatJin(RangeNumber, objselection))
            Greateikspline(Objlist, objselection)
            creatLocator(objselection)
            finishing(objselection)

    #Create motion complement bones
    def motionJoint(self):
        string = self.getModelName()

        print string

    def sendToMotionBuilder(self):
        cmds.SendAsNewSceneMotionBuilder()

    #create FK contorller
    def fkContorller(self):
        print "fkContorller"
        selection = cmds.ls(sl = True)
        for i in range(0, len(selection)):
            ctrl = cmds.circle(ch = True, nr = (1, 0, 0), name = contorllerNaming(selection[i], "Con"))
            cmds.setAttr("%s.overrideEnabled" % (ctrl[0] + "Shape"), 1)
            cmds.setAttr("%s.overrideColor" % (ctrl[0] + "Shape"), 18)
            driver_group = cmds.group(ctrl, name = contorllerNaming(selection[i], "Driver"))
            anim_group = cmds.group(driver_group, name = contorllerNaming(selection[i], "Anim"))
            cmds.delete(cmds.pointConstraint(selection[i], anim_group))
            cmds.delete(cmds.orientConstraint(selection[i], anim_group))
            cmds.parentConstraint(ctrl, selection[i], weight = True)

    #set contorller size
    def contorllerScale(self):
        scaleValue = self.getcontorllerScale()
        print scaleValue
        selection = cmds.ls(sl = True)
        for i in selection:
            contorllerCV = cmds.select(i + ".cv[:]")
            cmds.scale(scaleValue, scaleValue, scaleValue, contorllerCV, absolute=True)
            cmds.select(i)

    #set contorller color
    def blue(self):
        selection = cmds.ls(sl=True)

        for each in selection:
            cmds.setAttr((each + "Shape") + ".overrideEnabled", 1)
            cmds.setAttr((each + "Shape") + ".overrideColor", 6)


    def red(self):
        selection = cmds.ls(sl=True)

        for each in selection:
            cmds.setAttr((each + "Shape") + ".overrideEnabled", 1)
            cmds.setAttr((each + "Shape") + ".overrideColor", 13)
        print "red"

    def yellow(self):
        selection = cmds.ls(sl=True)

        for each in selection:
            cmds.setAttr((each + "Shape") + ".overrideEnabled", 1)
            cmds.setAttr((each + "Shape") + ".overrideColor", 17)
        print "yellow"

    def skyblue(self):
        selection = cmds.ls(sl=True)

        for each in selection:
            cmds.setAttr((each + "Shape") + ".overrideEnabled", 1)
            cmds.setAttr((each + "Shape") + ".overrideColor", 18)

        print "skbyle"

    def darkred(self):
        selection = cmds.ls(sl=True)

        for each in selection:
            cmds.setAttr((each + "Shape") + ".overrideEnabled", 1)
            cmds.setAttr((each + "Shape") + ".overrideColor", 4)

    def green(self):
        selection = cmds.ls(sl=True)

        for each in selection:
            cmds.setAttr((each + "Shape") + ".overrideEnabled", 1)
            cmds.setAttr((each + "Shape") + ".overrideColor", 14)

    def darkblue(self):
        selection = cmds.ls(sl=True)

        for each in selection:
            cmds.setAttr((each + "Shape") + ".overrideEnabled", 1)
            cmds.setAttr((each + "Shape") + ".overrideColor", 15)

    def white(self):
        selection = cmds.ls(sl=True)

        for each in selection:
            cmds.setAttr((each + "Shape") + ".overrideEnabled", 1)
            cmds.setAttr((each + "Shape") + ".overrideColor", 16)
    def cubeShape(self):
        name = self.getcontorllerName()
        selection = cmds.ls(sl=True)
        print name
        crv = cube()
        newcrv = cmds.rename(crv, contorllerNaming(name, "Con"))
        driver_group = cmds.group(newcrv, name = contorllerNaming(name, "Driver"))
        anim_group = cmds.group(driver_group, name = contorllerNaming(name, "Anim"))
        for i in selection:
            if len(selection):
                objrotate = cmds.xform(i, rotation = True, worldSpace = True, q = True)
                objtranslate = cmds.xform(i, worldSpace = True, q= True, t = True)
                cmds.setAttr("%s.t" % anim_group, objtranslate[0], objtranslate[1], objtranslate[2])
                cmds.setAttr("%s.r" % anim_group, objrotate[0], objtranslate[1], objrotate[2])
            else:
                continue

    def ballShape(self):
        selection = cmds.ls(sl=True)
        name = self.getcontorllerName()
        print name
        crv = ball()
        newcrv = cmds.rename(crv, contorllerNaming(name, "Con"))
        driver_group = cmds.group(newcrv, name=contorllerNaming(name, "Driver"))
        anim_group = cmds.group(driver_group, name=contorllerNaming(name, "Anim"))
        for i in selection:
            if len(selection):
                objrotate = cmds.xform(i, rotation = True, worldSpace = True, q = True)
                objtranslate = cmds.xform(i, worldSpace = True, q= True, t = True)
                cmds.setAttr("%s.t" % anim_group, objtranslate[0], objtranslate[1], objtranslate[2])
                cmds.setAttr("%s.r" % anim_group, objrotate[0], objtranslate[1], objrotate[2])
            else:
                continue
    
    def laceShape(self):
        selection = cmds.ls(sl=True)
        name = self.getcontorllerName()
        print name
        crv = lace()
        newcrv = cmds.rename(crv, contorllerNaming(name, "Con"))
        driver_group = cmds.group(newcrv, name=contorllerNaming(name, "Driver"))
        anim_group = cmds.group(driver_group, name=contorllerNaming(name, "Anim"))
        for i in selection:
            if len(selection):
                objrotate = cmds.xform(i, rotation = True, worldSpace = True, q = True)
                objtranslate = cmds.xform(i, worldSpace = True, q= True, t = True)
                cmds.setAttr("%s.t" % anim_group, objtranslate[0], objtranslate[1], objtranslate[2])
                cmds.setAttr("%s.r" % anim_group, objrotate[0], objtranslate[1], objrotate[2])
            else:
                continue
                
    #add FK contorller follow for ADV plugin
    def addFkFollow(self):
        print "follow"
        selection = cmds.ls(sl=True)
        for con in range(0, len(selection)):
            if selection[con] == "FKShoulder_L":
                cmds.addAttr(longName="Follow", attributeType="double", min=0.0, max=10.0, dv=10.0)
                cmds.setAttr("%s.Follow" % selection[con], keyable=True)
                creatgroup = cmds.group(empty=True, name="FKfollowShoulder_L")
                cmds.delete(cmds.parentConstraint(selection[con], creatgroup, weight=True))
                piv = cmds.xform("FKOffsetScapula_L", q=True, ws=True, t=True)
                cmds.xform(creatgroup, ws=True, piv=piv)
                poin = cmds.pointConstraint("FKXScapula_L", creatgroup, weight=True)
                orien = cmds.orientConstraint(creatgroup, "FKOffsetShoulder_L", weight=True)
                setrange = cmds.createNode("setRange", name="FKShoulder_LSetRangeFollow")
                cmds.setAttr("%s.valueX" % setrange, 10)
                cmds.setAttr("%s.minX" % setrange, 1)
                cmds.setAttr("%s.oldMaxX" % setrange, 10)
                cmds.connectAttr("%s.Follow" % selection[con], "%s.valueX" % setrange)
                cmds.connectAttr("%s.outValueX" % setrange, "%s.FKXScapula_LW0" % poin[0])
                cmds.connectAttr("%s.outValueX" % setrange, "%s.FKfollowShoulder_LW0" % orien[0])
                cmds.parent(creatgroup, 'FKSystem')
            elif selection[con] == "FKShoulder_R":
                cmds.addAttr(longName="Follow", attributeType="double", min=0.0, max=10.0, dv=10.0)
                cmds.setAttr("%s.Follow" % selection[con], keyable=True)
                creatgroup = cmds.group(empty=True, name="FKfollowShoulder_R")
                cmds.delete(cmds.parentConstraint(selection[con], creatgroup, weight=True))
                piv = cmds.xform("FKOffsetScapula_R", q=True, ws=True, t=True)
                cmds.xform(creatgroup, ws=True, piv=piv)
                poin = cmds.pointConstraint("FKXScapula_R", creatgroup, weight=True)
                orien = cmds.orientConstraint(creatgroup, "FKOffsetShoulder_R", weight=True)
                setrange = cmds.createNode("setRange", name="FKShoulder_RSetRangeFollow")
                cmds.setAttr("%s.valueX" % setrange, 10)
                cmds.setAttr("%s.minX" % setrange, 1)
                cmds.setAttr("%s.oldMaxX" % setrange, 10)
                cmds.connectAttr("%s.Follow" % selection[con], "%s.valueX" % setrange)
                cmds.connectAttr("%s.outValueX" % setrange, "%s.FKXScapula_RW0" % poin[0])
                cmds.connectAttr("%s.outValueX" % setrange, "%s.FKfollowShoulder_RW0" % orien[0])
                cmds.parent(creatgroup, 'FKSystem')
            elif selection[con] == "FKHip_R":
                cmds.addAttr(longName="Follow", attributeType="double", min=0.0, max=10.0, dv=10.0)
                cmds.setAttr("%s.Follow" % selection[con], keyable=True)
                creatgroup = cmds.group(empty=True, name="FKfollowHip_R")
                cmds.delete(cmds.parentConstraint(selection[con], creatgroup, weight=True))
                piv = cmds.xform("HipSwinger_M", q=True, ws=True, t=True)
                cmds.xform(creatgroup, ws=True, piv=piv)
                poin = cmds.pointConstraint("HipSwinger_M", creatgroup, weight=True)
                orien = cmds.orientConstraint(creatgroup, "FKOffsetHip_R", weight=True)
                setrange = cmds.createNode("setRange", name="FKHip_RSetRangeFollow")
                cmds.setAttr("%s.valueX" % setrange, 10)
                cmds.setAttr("%s.minX" % setrange, 1)
                cmds.setAttr("%s.oldMaxX" % setrange, 10)
                cmds.connectAttr("%s.Follow" % selection[con], "%s.valueX" % setrange)
                cmds.connectAttr("%s.outValueX" % setrange, "%s.HipSwinger_MW0" % poin[0])
                cmds.connectAttr("%s.outValueX" % setrange, "%s.FKfollowHip_RW0" % orien[0])
                cmds.parent(creatgroup, 'FKSystem')
            elif selection[con] == "FKHip_L":
                cmds.addAttr(longName="Follow", attributeType="double", min=0.0, max=10.0, dv=10.0)
                cmds.setAttr("%s.Follow" % selection[con], keyable=True)
                creatgroup = cmds.group(empty=True, name="FKfollowHip_L")
                cmds.delete(cmds.parentConstraint(selection[con], creatgroup, weight=True))
                piv = cmds.xform("HipSwinger_M", q=True, ws=True, t=True)
                cmds.xform(creatgroup, ws=True, piv=piv)
                poin = cmds.pointConstraint("HipSwinger_M", creatgroup, weight=True)
                orien = cmds.orientConstraint(creatgroup, "FKOffsetHip_L", weight=True)
                setrange = cmds.createNode("setRange", name="FKHip_LSetRangeFollow")
                cmds.setAttr("%s.valueX" % setrange, 10)
                cmds.setAttr("%s.minX" % setrange, 1)
                cmds.setAttr("%s.oldMaxX" % setrange, 10)
                cmds.connectAttr("%s.Follow" % selection[con], "%s.valueX" % setrange)
                cmds.connectAttr("%s.outValueX" % setrange, "%s.HipSwinger_MW0" % poin[0])
                cmds.connectAttr("%s.outValueX" % setrange, "%s.FKfollowHip_LW0" % orien[0])
                cmds.parent(creatgroup, 'FKSystem')
            else:
                continue
        cmds.select(clear=True)

    #creat a contorller named "tun"
    def importTun(self):
        print "tun"
        points = [(-0.497288, -1.5, 0), (-0.497288, 1.5, 0), (0.502712, 1.498922, 0), (0.502712, -0.500014, 0),
                  (-1.497288, -0.5, 0), (-1.497288, 0.5, 0), (1.502712, 0.5, 0), (1.502712, -0.5, 0),
                  (0.502712, -0.500388, 0),
                  (0.502712, -1.5, 0), (-0.497288, -1.499974, 0),
                  (0, 0, 0)]
        crv = cmds.curve(d=True, p=points, name='Tun')
        cmds.select("%s.cv[12]" % crv)
        cmds.delete()

        cmds.setAttr("%s.overrideEnabled" % crv, 1)
        cmds.setAttr("%s.overrideColor" % crv, 17)

        cmds.setAttr("%s.tx" % crv, lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.ty" % crv, lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.tz" % crv, lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.rx" % crv, lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.ry" % crv, lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.rz" % crv, lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.sx" % crv, lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.sy" % crv, lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.sz" % crv, lock=True, keyable=False, channelBox=False)
        cmds.setAttr("%s.v" % crv, lock=True, keyable=False, channelBox=False)

        cmds.addAttr(crv, longName = "model", attributeType = "enum", enumName = "High:low:")
        cmds.setAttr("%s.model" % crv, keyable=True)
        cmds.addAttr(crv, longName = "hair", attributeType = "enum", enumName = "off:on:")
        cmds.setAttr("%s.hair" % crv, keyable = True)
        cmds.addAttr(crv, longName = "face", attributeType = "enum", enumName = "off:on:")
        cmds.setAttr("%s.face" % crv, keyable = True)
        cmds.addAttr(crv, longName = "cloth", attributeType = "enum", enumName = "one:two:three:")
        cmds.setAttr("%s.cloth" % crv, keyable = True)
        cmds.addAttr(crv, longName = "weapons", attributeType = "enum", enumName = "off:on:")
        cmds.setAttr("%s.weapons" % crv, keyable = True)
        cmds.addAttr(crv, longName = "hairSystem", attributeType = "enum", enumName = "off:Static:dynamicFolliclesOnly:AllFollicles")
        cmds.setAttr("%s.hairSystem" % crv, keyable = True)

        cmds.group(crv, empty=False, name="%s_Grp" % crv)

    #add ADV plugin hisfist
    def addHisFist(self):
        print"hisfist"
        cmds.select(['Fingers_R', 'Fingers_L'])
        selection = cmds.ls(sl=True)
        for con in selection:
            cmds.addAttr(con, ln="hisFist", at='double', min=0, max=10, dv=0)
            cmds.setAttr(con + ".hisFist", keyable=True)
            cmds.select(clear=True)

    #creat driven key
    def key(self):
        print "key"
        selection = cmds.ls(sl=True)
        hisList = ['IndexFinger3', 'IndexFinger2', 'IndexFinger1', 'MiddleFinger3',
                   'MiddleFinger2', 'MiddleFinger1', 'RingFinger3', 'RingFinger2',
                   'RingFinger1', 'PinkyFinger3', 'PinkyFinger2', 'PinkyFinger1',
                   'ThumbFinger3', 'ThumbFinger2', 'ThumbFinger1']
        if selection[0] == "Fingers_R":
            for i in hisList:
                FKExtraobj = "FK" + i + "_R"
                getTvalue = cmds.getAttr(FKExtraobj + ".translate")
                getRvalue = cmds.getAttr(FKExtraobj + ".rotate")
                cmds.setAttr(selection[0] + ".hisFist", 10)
                objtranslate = "FKExtra" + i + "_R" + ".translate"
                objrotate = "FKExtra" + i + "_R" + ".rotate"
                cmds.setAttr(objtranslate, getTvalue[0][0], getTvalue[0][1], getTvalue[0][2])
                cmds.setAttr(objtranslate, getRvalue[0][0], getRvalue[0][1], getRvalue[0][2])
                cmds.setDrivenKeyframe(objtranslate, cd=selection[0] + ".hisFist")
                cmds.setDrivenKeyframe(objrotate, cd=selection[0] + ".hisFist")
                cmds.setAttr(selection[0] + ".hisFist", 0)
                cmds.setAttr(objtranslate, 0, 0, 0)
                cmds.setAttr(objrotate, 0, 0, 0)
                cmds.setDrivenKeyframe(objtranslate, cd=selection[0] + ".hisFist")
                cmds.setDrivenKeyframe(objrotate, cd=selection[0] + ".hisFist")
        elif selection[0] == "Fingers_L":
            for i in hisList:
                FKExtraobj = "FK" + i + "_L"
                getTvalue = cmds.getAttr(FKExtraobj + ".translate")
                getRvalue = cmds.getAttr(FKExtraobj + ".rotate")
                cmds.setAttr(selection[0] + ".hisFist", 10)
                objtranslate = "FKExtra" + i + "_L" + ".translate"
                objrotate = "FKExtra" + i + "_L" + ".rotate"
                cmds.setAttr(objtranslate, getTvalue[0][0], getTvalue[0][1], getTvalue[0][2])
                cmds.setAttr(objtranslate, getRvalue[0][0], getRvalue[0][1], getRvalue[0][2])
                cmds.setDrivenKeyframe(objtranslate, cd=selection[0] + ".hisFist")
                cmds.setDrivenKeyframe(objrotate, cd=selection[0] + ".hisFist")
                cmds.setAttr(selection[0] + ".hisFist", 0)
                cmds.setAttr(objtranslate, 0, 0, 0)
                cmds.setAttr(objrotate, 0, 0, 0)
                cmds.setDrivenKeyframe(objtranslate, cd=selection[0] + ".hisFist")
                cmds.setDrivenKeyframe(objrotate, cd=selection[0] + ".hisFist")

    # Translate to zero
    def translateToZero(self):
        selection = cmds.ls(sl = True)
        for i in selection:
            tx = cmds.getAttr(i + ".tx", lock=True)
            ty = cmds.getAttr(i + ".ty", lock=True)
            tz = cmds.getAttr(i + ".tz", lock=True)
            if (tx == ty == tz) and (not tx):
                cmds.setAttr(i + ".t", 0, 0, 0)
            elif (tx == ty != tz) and (not tx):
                cmds.setAttr(i + ".ty", 0)
                cmds.setAttr(i + ".tx", 0)
            elif (tx != ty == tz) and (not tx):
                cmds.setAttr(i + ".tx", 0)
            elif (tx == tz != ty) and (not ty):
                cmds.setAttr(i + ".ty", 0)
            elif (tx != ty == tz) and (not tz):
                cmds.setAttr(i + ".ty", 0)
                cmds.setAttr(i + ".tz", 0)
            elif (tx == ty != tz) and (not tz):
                cmds.setAttr(i + ".tz", 0)
            elif (tx == tz != ty) and (not tx):
                cmds.setAttr(i + ".tx", 0)
                cmds.setAttr(i + ".tz", 0)
            elif (tx == tz != ty) and (not tx):
                cmds.setAttr(i + ".tx", 0)
                cmds.setAttr(i + ".tz", 0)
            continue

    # Rotate to zero
    def rotateToZero(self):
        selection = cmds.ls(sl = True)
        for i in selection:
            rx = cmds.getAttr(i + ".rx", lock=True)
            ry = cmds.getAttr(i + ".ry", lock=True)
            rz = cmds.getAttr(i + ".rz", lock=True)
            if (rx == ry == rz) and (not rx):
                cmds.setAttr(i + ".r", 0, 0, 0)
            elif (rx == ry != rz) and (not rx):
                cmds.setAttr(i + ".ry", 0)
                cmds.setAttr(i + ".rx", 0)
            elif (rx != ry == rz) and (not rx):
                cmds.setAttr(i + ".rx", 0)
            elif (rx == rz != ry) and (not ry):
                cmds.setAttr(i + ".ry", 0)
            elif (rx != ry == rz) and (not rz):
                cmds.setAttr(i + ".ry", 0)
                cmds.setAttr(i + ".rz", 0)
            elif (rx == ry != rz) and (not rz):
                cmds.setAttr(i + ".rz", 0)
            elif (rx == rz != ry) and (not rx):
                cmds.setAttr(i + ".rx", 0)
                cmds.setAttr(i + ".rz", 0)
            elif (rx == rz != ry) and (not rx):
                cmds.setAttr(i + ".rx", 0)
                cmds.setAttr(i + ".rz", 0)
            continue
    
    def jobRivetLocator(self):
        if self.addContorllerValue() == True:
            runRivetLocator()
            addContorller()
        else:
            runRivetLocator()

    # get enter number
    def getcontorllerName(self):
        if not self.contorllerName:
            return
        return self.contorllerName.text()

    def getcontorllerScale(self):
        if not self.contorllerScaleValue:
            return
        return self.contorllerScaleValue.value()

    def getAddPartValue(self):
        if not self.addPartValue:
            return
        return self.addPartValue.value()

    def getStretchValue(self):
        if not self.stretchJointValue:
            return
        return self.stretchJointValue.value()

    def getModelName(self):
        if not self.modelName:
            return
        return self.modelName.text()

    def getSineValue(self):
        if not self.addsineValue:
            return
        if self.addsineValue.checkState() == QtCore.Qt.CheckState.Checked:
            return True
        else:
            return False

    def getTensileValue(self):
        if not self.addtensileValue:
            return
        if self.addtensileValue.checkState() == QtCore.Qt.CheckState.Checked:
            return True
        else:
            return False

    def addContorllerValue(self):
        if not self.addContorller:
            return
        if self.addContorller.checkState() == QtCore.Qt.CheckState.Checked:
            return True
        else:
            return False