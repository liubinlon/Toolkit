import maya.cmds
try:
    maya.cmds.loadPlugin("hairStripsGen.py")
except:pass
maya.cmds.hairStripsGen()

