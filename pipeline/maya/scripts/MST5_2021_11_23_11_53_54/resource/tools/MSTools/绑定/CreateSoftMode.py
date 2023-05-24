# -*- coding:utf8 -*-

import maya.cmds as mc
import maya.api.OpenMaya as om


def createSoftMode(*args):

    def sofModeMesh(point, transform, mesh, *args):
        ctrl, cntr, locShape, grp = createContral(mc.textField(textField, tx=1, q=1)) 

        transform = om.MFnTransform(om.MGlobal.getSelectionListByName(transform).getDagPath(0))                
        mesh = om.MFnMesh(om.MGlobal.getSelectionListByName(mesh).getDagPath(0))

        point, normal, other = mesh.getClosestPointAndNormal(point)
        position = transform.translation(4)
        position += om.MVector(point.x, point.y, point.z)
        quat = om.MVector(0.0, 0.0, 1.0).rotateTo(normal)
        
        grp = om.MFnTransform(om.MGlobal.getSelectionListByName(grp).getDagPath(0))
        grp.setTranslation(position, 4)
        grp.setRotation(quat, 4)

        softMod = mc.softMod(mesh.fullPathName(), wn=(ctrl, ctrl), n=ctrl.replace("MoveCtrl", "SpftMod"))[0]
        scaleMult = mc.createNode("multiplyDivide", n=ctrl.replace("MoveCtrl", "ScaleMult"))

        mc.connectAttr("%s.radius" %ctrl, "%s.input1X" %scaleMult, f=1)
        mc.connectAttr("%s.scaleValue" %ctrl, "%s.input2X" %scaleMult, f=1)
        mc.connectAttr("%s.outputX" %scaleMult, "%s.falloffRadius" %softMod, f=1)
        mc.connectAttr("%s.parentInverseMatrix[0]" %ctrl, "%s.bindPreMatrix" %softMod, f=1)
        mc.connectAttr("%s.worldPosition[0]" %locShape, "%s.falloffCenter" %softMod, f=1)

        mc.select(cl=1)

    sel = mc.ls(sl=1)
    if len(sel) != 0:
        mcSel = sel[0].split(".", 1)[0]
        mcSelType = mc.objectType(mcSel)
        if mcSelType == "transform":
            shape = mc.listRelatives(mcSel, c=1, s=1, typ="mesh")
            if len(shape) != 0:
                point = getCenterPosition(mc.xform(sel, q=True, t=1, wd=1))
                sofModeMesh(point, mcSel, shape[0])
        elif mcSelType == "mesh":
            transform = mc.listRelatives(mcSel, p=1, typ="transform")[0]
            point = getCenterPosition(mc.xform(transform, q=True, t=1, wd=1))
            sofModeMesh(point, transform, mcSel)
        elif mcSelType == "nurbsSurface":
            mc.warning("The current version does not support Surface!!!  Plase Select Vertex, Edge, Face or Object from Mesh!!!")
        else:
            mc.warning("Plase Select Vertex, Edge, Face or Object!!!")
    else:
        mc.warning("Plase Select Vertex, Edge, Face or Object!!!")
    

def createContral(name, *args):
    grp  = mc.group(em=1, n="%s_SoftMode_Grp" %name)
    cntr = mc.circle(nr=(0, 0, 1), c=(0, 0, 0), r=2.5, ch=0, n="%s_SoftMode_MoveCenter" %name)[0]
    ctrl = mc.curve(d=1, k=[0, 1, 2, 3, 4, 5, 6, 7],
                    p=[(0, 0, -2), (0, 0, 2), (0, 0, 0), (2, 0, 0), (-2, 0, 0), (0, 0, 0), (0, 2, 0), (0, -2, 0)])
    ctrl = mc.rename(ctrl, "%s_SoftMode_MoveCtrl" %name)
    
    cntrShape = mc.listRelatives(cntr, s=1, type="nurbsCurve")[0]
    ctrlShape = mc.listRelatives(ctrl, s=1, type="nurbsCurve")[0]

    loc = mc.spaceLocator(n="%s_SoftMode_MoveLoc" %name)[0]
    locShape = mc.listRelatives(loc, type="locator")[0]
    
    mc.parent(locShape, cntr, r=1, s=1)
    mc.delete(loc)

    mc.parent(cntr, grp)
    mc.parent(ctrl, cntr)

    mc.setAttr("%s.visibility" %locShape, 0)
    mc.setAttr("%s.lineWidth" %cntrShape, 2)
    mc.setAttr("%s.overrideEnabled" %cntrShape, 1)
    mc.setAttr("%s.overrideColor" %cntrShape, 6)
    mc.setAttr("%s.lineWidth" %ctrlShape, 2)
    mc.setAttr("%s.overrideEnabled" %ctrlShape, 1)
    mc.setAttr("%s.overrideColor" %ctrlShape, 17)

    mc.addAttr(ctrl, ln="radius", at="double", min=0, dv=1, k=1)
    mc.addAttr(ctrl, ln="scaleValue", at="double", dv=1, k=1)

    return [ctrl, cntr, locShape, grp]


def getCenterPosition(list, *args):
    x = y = z = 0
    seg = len(list) / 3
    for i in range(seg):
        x += list[i*3]
        y += list[i*3+1]
        z += list[i*3+2]    
    return om.MPoint(x/seg, y/seg, z/seg)


def showWindow(*args):
    global CSM_Window
    global textField
    CSM_Window = "CSM_Window"   
    if mc.window(CSM_Window, ex=1):
        mc.deleteUI(CSM_Window, wnd=1)
    
    CSM_Window = mc.window(CSM_Window, title="Create Soft Mode Window", width=400)
    mc.columnLayout(adjustableColumn=True)
    mc.text(u"\n 请选择任意点，线或面，或是选择单个物体!!! \n \n 下面输入名字，不要重复命名!!! \n")
    textField = mc.textField("name", tx="name")
    mc.button(label=u"创建软选择控制器", c=createSoftMode)
    mc.showWindow(CSM_Window)


showWindow()