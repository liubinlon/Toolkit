import maya.cmds
mllName = 'wire.py'
if not maya.cmds.pluginInfo(mllName, q=True, loaded=True):
    maya.cmds.loadPlugin(mllName)