import maya.cmds as cmds
from CreasePlus import CreasePlusMain

CreasePlusMain.start()

if not cmds.pluginInfo("CreasePlusNodes", q=True, loaded=True):
    cmds.loadPlugin("CreasePlusNodes.py")