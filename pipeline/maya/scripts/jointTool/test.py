#-*- coding: utf-8 -*-


# import maya.cmds as cmds

obj = "Main"
objGrp = cmds.lsitRelatives(obj, parent = True)
objList = cmds.listRelatives(obj, noIntermediate = True)
objList.pop(0)
ctrl = cmds.circle(nr = [0 , 1, 0], sw = 360, r = 1, d = 3, ut = 0, tol = 0.01, s = 8, ch = True,  name = obj + "End")[0]
cmds.parent(objList, ctrl)
cmds.parent(ctrl, obj)
# drivergrp = cmds.group(empty=True, name = each + "DriverGrp")
# animgrp = cmds.group(drivergrp, name = each + "AnimGrp")

# cmds.delete(cmds.parentConstraint(each, animgrp)[0])
# cmds.parent(each, drivergrp)
