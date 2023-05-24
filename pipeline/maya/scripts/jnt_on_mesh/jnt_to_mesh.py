#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
'''
File    :   jnt_to_mesh.py
Time    :   2022/07/01 09:51:20
Author  :   ZhenBao Liu
Version :   1.0
Contact :   3305510092@qq.com
Desc    :   None
'''
# import the libraries needed by this script here
import pymel.core as pm
# here put the class script


def loc_on_mesh(_mesh, _loc):
    abs_mesh = pm.PyNode(_mesh)
    shape_node = abs_mesh.getShape()
    po_node = pm.createNode("closestPointOnMesh", name="{}_point_on_mesh".format(_loc))
    pm.connectAttr("{}.outMesh".format(shape_node), "{}.inMesh".format(po_node))
    pm.select(clear=1)
    loc_jnt = pm.joint(name="loc_jnt")
    pm.matchTransform(loc_jnt, _loc)
    pm.connectAttr("{}.t".format(loc_jnt), "{}.inPosition".format(po_node))
    par_v = pm.getAttr("{}.parameterV".format(po_node))
    par_u = pm.getAttr("{}.parameterU".format(po_node))
    pm.delete(po_node, loc_jnt)
    tra_node = pm.createNode("transform", name="{}_follicle".format(_loc))
    foll_node = pm.createNode("follicle", name="{}Shape".format(tra_node), p=tra_node)
    pm.connectAttr("{}.outRotate".format(foll_node), "{}.rotate".format(tra_node))
    pm.connectAttr("{}.outTranslate".format(foll_node), "{}.translate".format(tra_node))
    pm.connectAttr("{}.outMesh".format(shape_node), "{}.inputMesh".format(foll_node))
    pm.connectAttr("{}.worldMatrix[0]".format(shape_node), "{}.inputWorldMatrix".format(foll_node))
    pm.setAttr("{}.parameterV".format(foll_node), par_v)
    pm.setAttr("{}.parameterU".format(foll_node), par_u)
    pm.parentConstraint(tra_node, _loc, mo=1)

lst = pm.ls(sl=1)
_mesh = lst.pop(0)
for jnt in lst:
    loc_on_mesh(_mesh, jnt)