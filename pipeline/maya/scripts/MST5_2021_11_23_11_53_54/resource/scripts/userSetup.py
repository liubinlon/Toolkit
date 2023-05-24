#coding:gbk
import maya.cmds as mayaCmds
import pymel.core as pmc
import ConfigParser
import maya.mel as mel
import sys,toolkit_system


theInstallPath = mayaCmds.moduleInfo(mn='MS_Toolkit',p=True)





def getConfigFromKey(filePath,selection,key):
    getValue = ''
    config_raw = ConfigParser.RawConfigParser()
    config_raw.read(filePath)
    getValue = config_raw.get(selection, key)
    return getValue
    
def is_chinese(string):
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True

    return False
    
progamName = 'MS_Toolkit'



def buildButton_MS_Toolkit(progamName):
    
    try:
        theConfigPath = 'C:/JBY_soft/MS_Toolkit/theConfig.inf'  #此路径为个人配置文件，请勿修改
        getAllBag = eval(getConfigFromKey(theConfigPath,'general', 'paths'))
        for oneBag in getAllBag:
            if not is_chinese(oneBag):
                if oneBag+'MST_DATA/scripts' not in sys.path:
                    sys.path.append(oneBag+'MST_DATA/scripts')
                
                
                try:   
                    getAllPath = mel.eval('getenv("MAYA_SCRIPT_PATH")')
                    getList = getAllPath.split(';')
                
                    if oneBag+'MST_DATA/scripts' not in getAllPath:
                        mel.eval('putenv "MAYA_SCRIPT_PATH" "'+oneBag+'MST_DATA/scripts'+';'+getAllPath+'"')
                    
                    getAllPath = mel.eval('getenv("MAYA_PLUG_IN_PATH")')
                    getList = getAllPath.split(';')
                    if oneBag+'MST_DATA/plug-ins' not in getAllPath:
                        mel.eval('putenv "MAYA_PLUG_IN_PATH" "'+oneBag+'MST_DATA/plug-ins'+';'+getAllPath+'"')
                    
                    getAllPath = mel.eval('getenv("XBMLANGPATH")')
                    getList = getAllPath.split(';')
                    if oneBag+'MST_DATA/icons' not in getAllPath:
                        mel.eval('putenv "XBMLANGPATH" "'+oneBag+'MST_DATA/icons'+';'+getAllPath+'"')

                except:
                    try:
                                
                        getAllPath = str(mel.eval('getenv("MAYA_SCRIPT_PATH")'))
                        getList = getAllPath.split(';')
                        theScriptSTR = str(oneBag+'MST_DATA/scripts')
                        if theScriptSTR not in getAllPath:
                            mel.eval('putenv "MAYA_SCRIPT_PATH" "'+theScriptSTR+';'+getAllPath+'"')
                        
                        getAllPath =  str(mel.eval('getenv("MAYA_PLUG_IN_PATH")'))
                        getList = getAllPath.split(';')
                        thePlugSTR = str(oneBag+'MST_DATA/plug-ins')
                        if thePlugSTR not in getAllPath:
                            mel.eval('putenv "MAYA_PLUG_IN_PATH" "'+thePlugSTR+';'+getAllPath+'"')
                        
                        getAllPath = str(mel.eval('getenv("XBMLANGPATH")'))
                        getList = getAllPath.split(';')
                        theXbmSTR = str(oneBag+'MST_DATA/icons')
                        if theXbmSTR not in getAllPath:
                            mel.eval('putenv "XBMLANGPATH" "'+theXbmSTR+';'+getAllPath+'"')
                        
                                
                    except:mayaCmds.warning(u'[字符串]环境变量添加失败，可能是某插件的env编码与工具盒冲突，盒内部分工具的使用可能受到影响，请查阅【工具盒刷不出的解决办法.zip】')
                        
    except:mayaCmds.warning(u'环境变量添加失败，可能是某插件的env编码与工具盒冲突，盒内部分工具的使用可能受到影响，请查阅【工具盒刷不出的解决办法.zip】')          
    
       
    getProgramPath = mayaCmds.moduleInfo(mn='MS_Toolkit',p=True)
    getScriptDir = getProgramPath+'/scripts'
    if getScriptDir not in sys.path:
        sys.path.append(getScriptDir)
    if mayaCmds.iconTextButton(progamName,ex=True):
        mayaCmds.deleteUI(progamName)
    if mayaCmds.menu('MayaWindow|劲爆羊工具盒5_0',ex=True):
        mayaCmds.deleteUI('MayaWindow|劲爆羊工具盒5_0')
    mayaCmds.iconTextButton(progamName,i=getProgramPath+'/icons/button.png',c='execfile(unicode(\''+getScriptDir+'\'+\'/start.py\'))',stp='python',hi=getProgramPath+'/icons/button_hover.png',p=mayaCmds.iconTextButton('statusFieldButton',q=True,p=True))

    MainMayaWindow = pmc.language.melGlobals['gMainWindow']
    try: 
        customMenu = pmc.menu(u'劲爆羊工具盒5.0', parent=MainMayaWindow)
        pmc.menuItem(label=u"启动工具盒", command='execfile(unicode(\''+getScriptDir+'\'+\'/start.py\'))', parent=customMenu)
    except:pass
    toolkit_system.startCar(theInstallPath + '/scripts/KSN.pyd')

if not pmc.about(batch=True):
    pmc.general.evalDeferred('buildButton_MS_Toolkit(\''+progamName+'\')')

