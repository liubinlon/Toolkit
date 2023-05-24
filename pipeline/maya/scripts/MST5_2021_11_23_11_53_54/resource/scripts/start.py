import subprocess,os,sys
import maya.cmds as mayaCmds

theInstallPath = mayaCmds.moduleInfo(mn='MS_Toolkit',p=True)

getScriptDir = theInstallPath+'/scripts/'
if getScriptDir not in sys.path:
    sys.path.insert(0,getScriptDir)
import toolkit_system
toolkit_system.startCar(theInstallPath+'/scripts/MST5.pyd')
