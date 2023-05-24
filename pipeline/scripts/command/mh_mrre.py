import maya.cmds as cmds
from itertools import product

transScale = [-1,-1,-1,1,1,1]
selRoot = cmds.ls(sl=1)
sourceGrps = selRoot + cmds.listRelatives(selRoot, ad=1, type='joint') 
#sourceGrps = selRoot
attrList = ['.tx','.ty','.tz','.rx','.ry','.rz']
for checkGrp in sourceGrps:
    if '_l_' in checkGrp:
        targetGrp = checkGrp.replace('_l_', '_r_')
    else:
        targetGrp = checkGrp.replace('_r_', '_l_')
    for num, attr in enumerate(attrList):
        # attr = attrList[num]
        cons = cmds.listConnections(checkGrp+attr, s=1, d=0)
        if cons:
            continue
        try:
            cmds.setAttr(targetGrp+attr, transScale[num]*cmds.getAttr(checkGrp+attr))
        except:
            pass
    print('------')
    print(checkGrp)
    print(targetGrp)
