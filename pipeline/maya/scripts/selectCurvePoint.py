from maya import cmds
def start():
    allSel=cmds.ls(selection=True)
    allSelCurve = []
    for sel in allSel:
        shapes_name = cmds.listRelatives(sel, fullPath=True)
        for shapes in shapes_name:
            if cmds.nodeType(shapes) == "nurbsCurve":
                allSelCurve.append(sel)
    cmds.select(clear=True)
    for needCurve in allSelCurve:
        cmds.select(needCurve+".cv[0]",tgl=True)  


    