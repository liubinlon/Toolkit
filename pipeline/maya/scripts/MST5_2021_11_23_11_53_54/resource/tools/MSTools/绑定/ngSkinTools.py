#coding:gbk

import maya.cmds as mayaCmds
thePath = mayaCmds.moduleInfo(mn='MS_Toolkit',p=True)+'/tools/MSTools/MST_DATA/plug-ins/'+mayaCmds.about(v=True)
if not mayaCmds.pluginInfo("ngSkinTools",q=True,l=True):
    try:
        mayaCmds.loadPlugin(thePath+'/ngSkinTools')
    except:mayaCmds.warning(u'λ�� ' +thePath+u' δ���� ngSkinTools.mll ')
from ngSkinTools.ui.mainwindow import MainWindow
MainWindow.open()

