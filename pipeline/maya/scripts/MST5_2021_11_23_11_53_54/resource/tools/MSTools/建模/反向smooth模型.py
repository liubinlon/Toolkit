# -*- coding: GBK -*-

import pymel.core as pmc
import maya.cmds as cmds
import maya.mel as mel


def smoothReduce():
    sel=cmds.ls(sl=True)
    if sel:
        pointNum=cmds.polyEvaluate(v=True)
        vertexId = sel[0]+'.vtx[{}]'.format(str(pointNum))
        lastEdgeGroup=cmds.polyListComponentConversion(vertexId,fv=True,te=True)[0]
        cmds.select(lastEdgeGroup)

        while 1:
            calcu = cmds.ls(sl=True)
            cmds.SelectEdgeLoopSp()
            edge = cmds.ls(sl=True,fl=True)
            edges = [int(ii.split('[')[1].split(']')[0]) for ii in edge]
            cmds.polySelect(er=edges,en=2)
            pp = cmds.ls(sl=True)
            if pp == calcu:
                break
        cmds.polyDelEdge( cv=True )
    else:
        cmds.warning('not selected!')
    



windowName = 'smoothReduce_WindowName' # 自定义
if cmds.window(windowName,ex=True):  
    cmds.deleteUI(windowName)
        
cmds.window(windowName,title="模型反向smooth工具") # 自定义
cmds.rowColumnLayout(numberOfColumns=1,adj=True)

cmds.text(l='')
cmds.text(fn="boldLabelFont",l='选择需要反向smooth的模型')
cmds.text(l='')
cmds.text(fn="boldLabelFont",l='记得删历史')
cmds.text(l='')
cmds.text(fn="boldLabelFont",l='再执行，行就行，不行就算了') # 自定义

cmds.text(l='')



cmds.button(l="反向Smooth！！",c="smoothReduce()") # 自定义

cmds.text(l='')
cmds.setParent('..')
cmds.showWindow(windowName)