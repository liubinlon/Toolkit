# -*- coding:GBK -*- 
import os,shutil,codecs
import maya.cmds as cmds
import pymel.core as pmc
global getPlace


def writeNewFileCodeUTF(path,string):
    file = codecs.open(path,'w','utf-8')
    file.write(string)
    file.close    

def copyTreeToPath(sourceFolder,targetPath):
    targetPath = targetPath.decode('gbk')
    sourceFolder = sourceFolder.decode('gbk')
    getAllFiles = []
    getAllDirs = []
    for root, dirs, files in os.walk(sourceFolder, topdown=False):
        for name in files:
            getAllFiles.append(os.path.join(root, name).replace('\\','/'))
        for name in dirs:
            getAllDirs.append(os.path.join(root, name).replace('\\','/'))

    for one in getAllDirs:
        getPathTarget = targetPath+one.replace(sourceFolder,'')
        
        cmds.sysFile(getPathTarget,md=True)
    allNum = getAllFiles.__len__()
    
    for i,one in enumerate(getAllFiles):
        getPathTarget = targetPath+one.replace(sourceFolder,'')
        try:
            cmds.sysFile(one,copy=getPathTarget)
        except:pass


class DeployTool():
    def __init__(self):
        pass

    def startDeploy(self,getPlace):
        getLibDir = getPlace+'/resource/'
        getProgramName = 'MS_Toolkit'
        getScriptDir = cmds.internalVar(userScriptDir=True)
        getMayaModDir = getScriptDir.rsplit('/',3)[0]+'/'
        getAimDir = 'C:/JBY_soft/'+getProgramName+'/'

        cmds.sysFile(getAimDir,md=True)
        cmds.sysFile(getMayaModDir + 'modules',md=True)
        getModText = '+ '+getProgramName+' 5.0 '+getAimDir
        writeNewFileCodeUTF(getMayaModDir + 'modules/'+getProgramName+'.mod',getModText)
        copyTreeToPath(getLibDir,getAimDir)

        if cmds.iconTextButton(getProgramName,ex=True):
            cmds.deleteUI(getProgramName)
        cmds.iconTextButton(getProgramName,hi=getAimDir+'icons/button_hover.png',i=getAimDir+'icons/button.png',c='execfile(\''+getAimDir+'scripts'+'/start.py\')',stp='python',p=cmds.iconTextButton('statusFieldButton',q=True,p=True))
        execfile(unicode(getAimDir+'scripts/start.py'))
        

        
        MainMayaWindow = pmc.language.melGlobals['gMainWindow']
        try: 
            if cmds.menu('MayaWindow|�����򹤾ߺ�5_0',ex=True):
                cmds.deleteUI('MayaWindow|�����򹤾ߺ�5_0')
            customMenu = pmc.menu(u'�����򹤾ߺ�5.0', parent=MainMayaWindow)
            pmc.menuItem(label=u"�������ߺ�", command='execfile(\''+getAimDir+'scripts'+'/start.py\')', parent=customMenu)
        except:pass
        
if __name__ == '__main__':
    getVersionMayaGlobal =int (cmds .about (version =True ))
    if getVersionMayaGlobal>2016: 
        startDeploy = DeployTool()
        theProgWin = cmds.progressWindow(title='���ڰ�װ',
                        progress=0,
                        isInterruptable=True )
        cmds.progressWindow(theProgWin,endProgress=1)
        startDeploy.startDeploy(getPlace)
    
    if getVersionMayaGlobal<=2016: 
        cmds.warning(u'��֧��2016�Լ����Ͱ汾��maya')