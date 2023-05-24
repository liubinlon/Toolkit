#-*- coding: utf-8 -*-
import maya.cmds as cmds
import re

from contorllerShape import*
from renaming import contorllerNaming

def getEdgeNum(edgeName):
    SplitStr = edgeName.split(".")
    EdgesValues = re.findall(r"\d+\.?\d*",str(SplitStr[1]))
    return int(EdgesValues[0])

def getSelctionObjectName(Selection):
    ObjStr = Selection[0]
    SplitStr = ObjStr.split(".")
    return SplitStr[0]

def RivetLocator(Selection):
    global ObjJoint,ObjLocation

    selObjName = getSelctionObjectName(Selection)
    e1 = getEdgeNum(Selection[0])
    e2 = getEdgeNum(Selection[1])

    nameCFME1 = cmds.createNode('curveFromMeshEdge', n="rivetCurveFromMeshEdge1")
    cmds.setAttr("%s.ihi" % nameCFME1, 1)
    cmds.setAttr("%s.ei[0]" % nameCFME1, e1)
    nameCFME2 = cmds.createNode('curveFromMeshEdge', n="rivetCurveFromMeshEdge2")
    cmds.setAttr("%s.ihi" % nameCFME2, 1)
    cmds.setAttr("%s.ei[0]" % nameCFME2, e2)
    
    nameLoft = cmds.createNode('loft', n="rivetLoft1")
    cmds.setAttr("%s.u" % nameLoft, True)
    cmds.setAttr("%s.rsn" % nameLoft, True)

    namePOSI = cmds.createNode('pointOnSurfaceInfo', n="rivetPointOnSurfaceInfo1")
    cmds.setAttr("%s.turnOnPercentage" % namePOSI, 1)
    cmds.setAttr("%s.parameterU" % namePOSI, 0.5)
    cmds.setAttr("%s.parameterV" % namePOSI, 0.5)
		
    cmds.connectAttr((nameLoft + ".os"), (namePOSI + ".is"), f=1)
    cmds.connectAttr((nameCFME1 + ".oc"), (nameLoft + ".ic[0]"))
    cmds.connectAttr((nameCFME2 + ".oc"), (nameLoft + ".ic[1]"))
    cmds.connectAttr((selObjName + ".w"), (nameCFME1 + ".im"))
    cmds.connectAttr((selObjName + ".w"), (nameCFME2 + ".im"))
    
    ObjLocation = cmds.createNode('transform', n="RivetLocator1")
    cratlocator = cmds.createNode('locator', n=(ObjLocation + "Shape"), p=ObjLocation)
    cmds.setAttr(cratlocator + ".lodVisibility", 0)

    ObjJoint = cmds.createNode("joint", name="%sJnt%s" % (selObjName, e1))
    cmds.parent(ObjJoint, ObjLocation)

    nameAC = cmds.createNode('aimConstraint', p=ObjLocation, n=(ObjLocation + "_rivetAimConstraint1"))

    cmds.setAttr("%s.tg[0].tw" % nameAC, 1)
    cmds.setAttr("%s.a" % nameAC, 0, 1, 0, type="double3")
    cmds.setAttr("%s.u" % nameAC, 0, 0, 1, type="double3")
    cmds.setAttr("%s.v" % nameAC, k=False)
    cmds.setAttr("%s.tx" % nameAC, k=False)
    cmds.setAttr("%s.ty" % nameAC, k=False)
    cmds.setAttr("%s.tz" % nameAC, k=False)
    cmds.setAttr("%s.rx" % nameAC, k=False)
    cmds.setAttr("%s.ry" % nameAC, k=False)
    cmds.setAttr("%s.rz" % nameAC, k=False)
    cmds.setAttr("%s.sx" % nameAC, k=False)
    cmds.setAttr("%s.sy" % nameAC, k=False)
    cmds.setAttr("%s.sz" % nameAC, k=False)
    
    cmds.connectAttr((namePOSI + ".position"), (ObjLocation + ".translate"))
    cmds.connectAttr((namePOSI + ".n"), (nameAC + ".tg[0].tt"))
    cmds.connectAttr((namePOSI + ".tv"), (nameAC + ".wu"))
    cmds.connectAttr((nameAC + ".crx"), (ObjLocation + ".rx"))
    cmds.connectAttr((nameAC + ".cry"), (ObjLocation + ".ry"))
    cmds.connectAttr((nameAC + ".crz"), (ObjLocation + ".rz"))

    cmds.select(ObjLocation, r = 1)
    return ObjLocation

def addContorller():
    conShape = ball()
    newConShape = cmds.rename(conShape, ObjLocation)
    drivergrp = cmds.group(newConShape, name = contorllerNaming(newConShape, "Driver"))
    animgrp = cmds.group(drivergrp, name = contorllerNaming(newConShape, "Anim"))
    cmds.delete(cmds.parentConstraint(ObjJoint, animgrp)[0])
    cmds.parent(animgrp, ObjLocation)
    cmds.parent(ObjJoint, newConShape)
    jingrp = cmds.group(ObjJoint, name = contorllerNaming(ObjJoint, "grp"))
    cmds.parent(jingrp, w = True)
    cmds.connectAttr(newConShape + ".translate", ObjJoint + ".translate")
    cmds.connectAttr(newConShape + ".rotate", ObjJoint + ".rotate")
    cmds.connectAttr(newConShape + ".scale", ObjJoint + ".scale")


def runRivetLocator():
    Selection = cmds.filterExpand(sm=32)
    if len(Selection) == 2:
        RivetLocator(Selection)