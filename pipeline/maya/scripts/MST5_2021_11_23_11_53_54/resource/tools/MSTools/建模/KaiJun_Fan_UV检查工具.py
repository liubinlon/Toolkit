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
        
cmds.window(windowName,title="�����������С����")
cmds.rowColumnLayout(numberOfColumns=1)
cmds.text(l='')
cmds.text(fn="boldLabelFont",l='��ѡ��һ��ģ��')
cmds.text(l='')
cmds.text(fn="boldLabelFont",l='���� KaiJun Fan �Ĵ���')

cmds.text(l='')
cmds.text(l='')
cmds.button(l="�ҳ��ص�UV����",c="fkaijun_check_uv_overlapping()")
cmds.text(l='')
cmds.button(l="�ҳ���Խuv���޵���",c="fkaijun_uv_face_cross_quadrant()")
cmds.text(l='')
cmds.setParent('..')
cmds.showWindow(windowName)