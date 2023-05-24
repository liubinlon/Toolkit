# -*- coding: GBK -*-

from check_core import check_uv_overlapping
from check_core import check_functions
import pymel.core as pmc
import maya.cmds as cmds
import maya.mel as mel

def fkaijun_check_uv_overlapping():
    pmc.select(check_uv_overlapping.main_function(pmc.ls(sl=True)[0].longName()))

def fkaijun_uv_face_cross_quadrant():
    pmc.select(check_functions.uv_face_cross_quadrant(pmc.ls(sl=True)[0].longName()))



windowName = 'theWindow_fkaijun_check_uv'
if cmds.window(windowName,ex=True):  
    cmds.deleteUI(windowName)
        
cmds.window(windowName,title="大肥羊牌贴心小工具")
cmds.rowColumnLayout(numberOfColumns=1)
cmds.text(l='')
cmds.text(fn="boldLabelFont",l='先选择一个模型')
cmds.text(l='')
cmds.text(fn="boldLabelFont",l='嫖自 KaiJun Fan 的代码')

cmds.text(l='')
cmds.text(l='')
cmds.button(l="找出重叠UV的面",c="fkaijun_check_uv_overlapping()")
cmds.text(l='')
cmds.button(l="找出跨越uv象限的面",c="fkaijun_uv_face_cross_quadrant()")
cmds.text(l='')
cmds.setParent('..')
cmds.showWindow(windowName)