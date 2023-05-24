# -*- coding: GBK -*-
#####################
'''
~ pythonVersion - 2.7.11 
~ for maya2017/2018
~ win7/10 - 64
~ by 劲爆羊厂长 2018/10/13 
'''
#####################

setZRenderVersion = 'v1.18' 

import maya.cmds as cmds
from PySide2.QtWidgets import QApplication,QLabel,QMessageBox,QProgressBar,QPlainTextEdit,QWidget,QHBoxLayout,QVBoxLayout,QPushButton
from PySide2.QtCore import Qt
from PySide2.QtGui import QTextCursor
import os,re
try:
    if not cmds.pluginInfo("mtoa",q=True,l=True):
        cmds.loadPlugin( "mtoa", qt=True)
except:cmds.warning(u'没加载arnold渲染器?')
if cmds.pluginInfo("mtoa",q=True,l=True):
    from arnold import AiBegin,AiASSWrite,AiNodeSetStr,AiMsgSetConsoleFlags,AI_LOG_ALL,AiASSLoad,AI_NODE_ALL,AiUniverseGetNodeIterator,AiNodeIteratorFinished,AiNodeIteratorGetNext,AiNodeIs,AiNodeGetStr,AiNodeIteratorDestroy,AiEnd

def getMayaWindow():
    return QApplication.activeWindow()

class CheckTheScene_UI(QWidget):
    def __init__(self,parent=getMayaWindow()):
        super(CheckTheScene_UI,self).__init__(parent)

        theFont_ZCheck = u"微软雅黑"
        theColorGray = 'rgb(110,110,110)'
        theColorBlack = 'rgb(40,40,40)'

        self.Style =     """          
                                QWidget
                                {
                                    background:"""+theColorBlack+"""	;
                                    outline:none;  
                                }
                                
                                QProgressBar 
                                {
                                    border: 2px solid """+theColorGray+""";
                                    text-align: center;
                                    padding: 1px;
                                    border-radius: 6px;
                                    background-color:rgb(20,20,23); 
                                    width: 5px;
                                    height:25px;
                                    color:rgb(200,200,200);
                                }

                                QProgressBar::chunk 
                                {
                                    background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0,
                                    stop: 0 #CC6600,
                                    stop: 0.4999 #CC6600,
                                    stop: 0.8 #CC6600,
                                    stop: 1 #FF9900);
                                    border-radius: 6px;
                                    border: 2px solid """+theColorGray+""";
                                }
                                
                                QLabel
                                {
                                    font-family: """+theFont_ZCheck+""";
                                    font-size:13px;
                                    color:"""+theColorGray+""";    
                                }
                                
                                QPushButton
                                {
                                    font-family: """+theFont_ZCheck+""";
                                    font-size:13px;
                                    color:"""+theColorGray+""";
                                    border-radius: 3px;
                                    border: 1px solid """+theColorGray+""";
                                }
                                
                                
                                QPushButton:hover
                                {      
                                    background-color:rgb(220,120,0)   ;
                                }
                                
                                
                                QPlainTextEdit
                                {
                                    font-family: """+theFont_ZCheck+""";
                                    font-size:15px;
                                    border: 1px solid """+theColorGray+""";
                                    margin-top: 10px;
                                    border-radius: 3px;
                                }
                                
               
                                    
                                   
                            """
        self.theHelpOfZCheck = u"""说明：\n
        ~ 此工具用于 : 1、maya场景诊断 2、给别人擦屁股时甩锅\n
        ~ 甩锅时记得要小声逼逼这句话：“他妈的这么毒的场景你给我渲出来试试？”\n
        ~ 讲究的是一个有理有据有血有肉，动之以情晓之以理，令人不得不服\n
        ~ 也可以顺便拿检测结果羞辱一下上游环节的制作习惯\n
        ~ 更多工具请访问  http://blog.sina.com.cn/matthew0326
        """
        self.setParent(getMayaWindow()) 
        self.setWindowFlags(Qt.Window)
        self.setStyleSheet(self.Style)  
        self.clearScene = ClearScene(self)
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(u'场景诊断工具 '+setZRenderVersion)
        self.setMinimumSize(500,750)
        self.MainVLayout = QVBoxLayout()
        self.MainVLayout.setSpacing(1)
        self.setLayout(self.MainVLayout)
        self.doc = QLabel(self.theHelpOfZCheck)
        self.doc.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.MainVLayout.addWidget(self.doc)
        self.theMainPlain = QPlainTextEdit()
        self.theMainPlain.setPlaceholderText(u'请开始诊断 ...')
        self.theMainPlain.setReadOnly(True)
        self.MainVLayout.addWidget(self.theMainPlain)
        self.pbr = QProgressBar()
        self.pbr.setFixedHeight(15)
        self.MainVLayout.addWidget(self.pbr)
        self.StartCheckButton = QPushButton(u'开始诊断')
        self.StartCheckButton.clicked.connect(self.startCheck)
        self.MainVLayout.addWidget(self.StartCheckButton)
        self.clearLayout = QHBoxLayout()
        self.MainVLayout.addLayout(self.clearLayout)
        self.buttonDeleteNameSpace = QPushButton(u'删除所有空间名')
        self.buttonDeleteNameSpace.setFixedWidth(120)
        self.buttonDeleteNameSpace.clicked.connect(self.clearScene.ifDeleteNameSpace)
        self.buttonDeleteUnknown = QPushButton(u'删除所有未知节点')
        self.buttonDeleteUnknown.setFixedWidth(120)
        self.buttonDeleteUnknown.clicked.connect(self.clearScene.ifDeleteUnknown)
        self.clearLayout.addWidget(self.buttonDeleteNameSpace)
        self.clearLayout.addWidget(self.buttonDeleteUnknown)
        self.show()
        
    def startCheck(self):
        self.StartCheckButton.setText(u'努力诊断中...')
        self.pbr.setValue(17)
        self.Check = CheckTheScene(self)
        self.StartCheckButton.setText(u'开始诊断')
    
    

        
class ClearScene():
    def __init__(self,win):
        self.win=win
        
    def deleteNameSpace(self):
        for i in range(5):
            self.discusRef()
            
    def ifDeleteNameSpace(self):     
        reply = QMessageBox.question(self.win, u'警告', u'是否删掉所有空间名?',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.deleteNameSpace() 
                   
    def discusRef(self):
        getAll_ref = cmds.file(q=True,r=True,sharedReferenceFile=True)
        try:
            for oneR in getAll_ref:
                cmds.file(oneR,ir=True)
        except:
            pass
        getAllNS = cmds.namespaceInfo(r=True,listOnlyNamespaces=True)
        for oneNS in getAllNS:
            if oneNS != 'UI' and oneNS != 'shared':
                try:
                    cmds.namespace(mergeNamespaceWithRoot=True,removeNamespace=oneNS)
                    self.win.theMainPlain.moveCursor(QTextCursor.End)
                    self.win.theMainPlain.insertPlainText(u'已经干掉空间名：'+oneNS+' \n')
                except:
                    pass
                    
    def ifDeleteUnknown(self):
        reply = QMessageBox.question(self.win, u'警告', u'是否删掉未知节点?',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.deleteAllUnknown() 
        
    def deleteAllUnknown(self):
        for one in cmds.ls(type='unknown'):
            try:
                cmds.delete(one)
                self.win.theMainPlain.moveCursor(QTextCursor.End)
                self.win.theMainPlain.insertPlainText(u'未知节点：'+one+u' - 已经被删除\n')
            except:
                self.win.theMainPlain.moveCursor(QTextCursor.End)
                self.win.theMainPlain.insertPlainText(one+u' 无法被删除，可能是来自引用文件或者被锁定\n')

            
class CheckTheScene():
    def __init__(self,win):
        self.ifMtoa = int(cmds.pluginInfo("mtoa",q=True,l=True))
        self.ifRedShift = int(cmds.pluginInfo("redshift4maya",q=True,l=True))
        self.win=win
        self.No = u'---未检测到毒性---\n'
        self.levelList = [u' 神话 6星 \n         (给大佬的神级场景整理意识跪了~)',
                          u' 优秀 5星 \n         (哇靠这么优秀的吗?)',
                          u' 良好 4星 \n         (可以了，还可以再优秀一点)',
                          u' 勉强 3星 \n         (在违法的边缘试探.jpg)',
                          u' 略差 2星 \n         (你怎么回事小老弟.jpg)',
                          u' 较差 1星 \n         (乱来了是不是?)',
                          u' 毒瘤 0星 \n         (报复社会是不是?)'] 
        self.level = ''
        self.sameNameTex = {}
        self.win.theMainPlain.clear()
        self.negativeComment = 0 
        
        self.theValueUP(1,0,u'【贴图状态检测】\n')
        self.win.pbr.setValue(21)
        self.value_point = self.negativeComment
        self.checkTexture()
        self.value_checkTexture = str(self.negativeComment - self.value_point) 
        
        self.theValueUP(1,0,u'\n\n【同名节点检测】\n')
        self.win.pbr.setValue(28)
        self.value_point = self.negativeComment
        self.checkSameNameJBY()  
        self.value_checkSameNameJBY = str(self.negativeComment - self.value_point) 

        
        self.theValueUP(1,0,u'\n\n【未知节点检测】\n')
        self.win.pbr.setValue(36)
        self.value_point = self.negativeComment
        self.checkUnknownJBY()
        self.value_checkUnknownJBY = str(self.negativeComment - self.value_point) 

        self.theValueUP(1,0,u'\n\n【双层引用检测】\n')
        self.win.pbr.setValue(41)
        self.value_point = self.negativeComment
        self.checkSubRef()
        self.value_checkSubRef = str(self.negativeComment - self.value_point) 
        
        self.theValueUP(1,0,u'\n\n【物体名字冒号数量检测】\n')
        self.win.pbr.setValue(46)
        self.value_point = self.negativeComment
        self.checkColonTwo()
        self.value_checkColonTwo = str(self.negativeComment - self.value_point) 
        
        self.theValueUP(1,0,u'\n\n【中文工程目录检测】\n')
        self.win.pbr.setValue(55)
        self.value_point = self.negativeComment
        self.checkProjectName()
        self.value_checkProjectName = str(self.negativeComment - self.value_point) 
        
        self.theValueUP(1,0,u'\n\n【中文用户名检测】\n')
        self.win.pbr.setValue(63)
        self.value_point = self.negativeComment
        self.checkUserName()
        self.value_checkUserName = str(self.negativeComment - self.value_point) 
        
        self.theValueUP(1,0,u'\n\n【引用文件中的可怕的非默认渲染层检测】\n')
        self.win.pbr.setValue(71)
        self.value_point = self.negativeComment
        self.checkRefRenLayer()
        self.value_checkRefRenLayer = str(self.negativeComment - self.value_point) 
        
        self.theValueUP(1,0,u'\n\n【引用文件中令人嫌弃的非默认显示层检测】\n')
        self.win.pbr.setValue(74)
        self.value_point = self.negativeComment
        self.checkRefDisLayer()
        self.value_checkRefDisLayer = str(self.negativeComment - self.value_point) 
        
        
        self.theValueUP(1,0,u'\n\n【临时节点检测】\n')
        self.win.pbr.setValue(80)
        self.value_point = self.negativeComment
        self.checkHis()
        self.value_checkHis = str(self.negativeComment - self.value_point) 
       
        
        self.theValueUP(1,0,u'\n\n【以面给材质检测】\n')
        self.win.pbr.setValue(82)
        self.value_point = self.negativeComment
        self.checkFaceMaterial()
        self.value_checkFaceMaterial = str(self.negativeComment - self.value_point) 
        
        self.theValueUP(1,0,u'\n\n【蒙皮的物体检测】\n')
        self.win.pbr.setValue(89)
        self.value_point = self.negativeComment
        self.checkMeshSkinTransform()
        self.value_checkMeshSkinTransform = str(self.negativeComment - self.value_point) 
        
        self.theValueUP(1,0,u'\n\n【场景内相机检测】\n')
        self.win.pbr.setValue(93)
        self.value_point = self.negativeComment
        self.checkPersp()
        self.value_checkPersp = str(self.negativeComment - self.value_point) 
        
        self.theValueUP(1,0,u'\n\n【大纲层级检测】\n')
        self.win.pbr.setValue(98)
        self.value_point = self.negativeComment
        self.checkOutline()
        self.value_checkOutline = str(self.negativeComment - self.value_point) 
        
        self.win.pbr.setValue(100)
        
        self.theValueUP(1,0,u'\n\n||||||||||||||||||||||||||\n\n【毒性指数检测结果】\n'
                            +u'贴图状态 ：'+self.value_checkTexture+'\n'
                            +u'同名节点 : '+self.value_checkSameNameJBY+'\n'
                            +u'未知节点 : '+self.value_checkUnknownJBY+'\n'
                            +u'双层引用 : '+self.value_checkSubRef+'\n'
                            +u'物体名字冒号数量很多 : '+self.value_checkColonTwo+'\n'
                            +u'中文工程目录 : '+self.value_checkProjectName+'\n'
                            +u'中文用户名 : '+self.value_checkUserName+'\n'
                            +u'引用文件中的可怕的非默认渲染层 : '+self.value_checkRefRenLayer+'\n'
                            +u'引用文件中令人嫌弃的非默认显示层 : '+self.value_checkRefDisLayer+'\n'
                            +u'临时节点 : '+self.value_checkHis+'\n'
                            +u'面给材质 : '+self.value_checkFaceMaterial+'\n'
                            +u'蒙皮物体 : '+self.value_checkMeshSkinTransform+'\n'
                            +u'场景相机 : '+self.value_checkPersp+'\n'
                            +u'大纲层级 : '+self.value_checkOutline +'\n'
                            +u'\n\n    ————毒性指数合计 : '+str(self.negativeComment) +'\n')
                            
        if self.negativeComment < 2:
            self.level = self.levelList[0]
        if self.negativeComment >= 2 and self.negativeComment < 20:   
            self.level = self.levelList[1]
        if self.negativeComment >= 20 and self.negativeComment < 150:   
            self.level = self.levelList[2]    
        if self.negativeComment >= 150 and self.negativeComment < 300:   
            self.level = self.levelList[3]    
        if self.negativeComment >= 300 and self.negativeComment < 2000:   
            self.level = self.levelList[4]   
        if self.negativeComment >= 2000 and self.negativeComment < 60000:   
            self.level = self.levelList[5]   
        if self.negativeComment >= 60000 :  
            self.level = self.levelList[6] 
        self.theValueUP(1,0,u'\n       综合评价  ——  '+self.level+'\n')

        self.win.theMainPlain.moveCursor(QTextCursor.End)
        self.win.result = str(self.negativeComment),self.level

    def theValueUP(self,MUL,ADD,STR):
        self.negativeComment = self.negativeComment*MUL+ADD
        self.win.theMainPlain.moveCursor(QTextCursor.End)
        self.win.theMainPlain.insertPlainText(STR)          
    
        
    def checkTexture(self):
        self.getAllPath = []
        ifRight = 0
        if self.ifMtoa:
            getAllNodes = cmds.ls(type='file')+cmds.ls(type='aiImage')
            getAllAss = []
            getAllNodes = cmds.ls(type='aiStandIn')
            for one in getAllNodes:
                getPath = cmds.getAttr(one+'.dso')
                if getPath not in getAllAss and getPath != '':
                    getAllAss.append(getPath)
                 
            for oneProxy in getAllAss:
                AiBegin()
                AiMsgSetConsoleFlags(AI_LOG_ALL)
                AiASSLoad(oneProxy, AI_NODE_ALL)
                iter = AiUniverseGetNodeIterator(AI_NODE_ALL)
                while not AiNodeIteratorFinished(iter):
                    node = AiNodeIteratorGetNext(iter)
                    if AiNodeIs( node, "MayaFile" ):
                     
                        getPath = AiNodeGetStr( node, "filename" )
                        if getPath not in self.getAllPath and getPath != '':
                            self.getAllPath.append(getPath)
                            if not os.path.exists(getPath):
                                self.theValueUP(1,2,u'丢失贴图：【'+oneProxy+' - '+getPath+u'】\n')
                                ifRight = 1
                            if self.checkCHN(getPath):
                                self.theValueUP(1,66,u'中文贴图路径：【'+oneProxy+' - '+getPath+u'】\n')
                                ifRight = 1
                AiNodeIteratorDestroy(iter)
                AiEnd()
                
                
        if self.ifRedShift:
            getAllRs = []
            getAllNodes = cmds.ls(type='RedshiftProxyMesh')
            tm = re.compile('(\\x00\\x00\\x00[A-Za-z]:/.*?\\x00)+')
            tm2 = re.compile('(\\x00\\x00\\x00//[0-9].*?\\x00)+')
            for one in getAllNodes:
                getPath = cmds.getAttr(one+'.fileName')
                if getPath not in getAllRs and getPath != '':
                    getAllRs.append(getPath)
            
            for oneProxy in getAllRs:
                getCon = readFileCode2(oneProxy)
                getResult = tm.findall(getCon)
                getResult2 = tm2.findall(getCon)
                for oneString in getResult :
                    if '\\' not in oneString and oneString != '' and '_map_auto' not in oneString and '/' in oneString: 
                        getPathMap = oneString.split('\x00\x00\x00')[1][:-1]
                        if getPathMap not in self.getAllPath and getPathMap != '':
                            self.getAllPath.append(getPathMap)
                            if not os.path.exists(getPathMap):
                                self.theValueUP(1,2,u'丢失贴图：【'+oneProxy+' - '+getPathMap+u'】\n')
                                ifRight = 1
                            if self.checkCHN(getPathMap):
                                self.theValueUP(1,66,u'中文贴图路径：【'+oneProxy+' - '+getPathMap+u'】\n')
                                ifRight = 1
                for oneString in getResult2 :
                    if '\\' not in oneString and oneString != '' and '_map_auto' not in oneString and '/' in oneString: 
                        getPathMap = oneString.split('\x00\x00\x00')[1][:-1]
                        if getPathMap not in self.getAllPath and getPathMap != '':
                            self.getAllPath.append(getPathMap)
                                
        getAllNodes = cmds.ls(type='file')      
        for one in getAllNodes:
            if cmds.nodeType(one)=='file' or cmds.nodeType(one)=='psdFileTex':
                getPathCom = cmds.getAttr(one+'.computedFileTextureNamePattern')
                if '<UDIM>.' in getPathCom:
                    allFileUdim = []
                    getPathPre = getPathCom.rsplit('.',2)[0]
                    getSplit = getPathCom[getPathPre.__len__():getPathPre.__len__()+1]
                    getDir = os.path.split(getPathPre)[0]
                    
                    getpre = os.path.split(getPathPre)[-1]
                    getExt = os.path.splitext(getPathCom)[-1]
                    
                    tm = re.compile(getpre+getSplit+'\d\d\d\d'+getExt)
                    getAllPP = cmds.getFileList(fld=getDir,fs=getpre+getSplit+'*')
                    if getAllPP:
                        for oneFp in getAllPP:
                            getP = tm.findall(oneFp)
                            if getP != []:
                                getPath = getDir+'/'+getP[0]
                                if getPath not in self.getAllPath and getPath != '':
                                    self.getAllPath.append(getPath)
                                    if not os.path.exists(getPath):
                                        self.theValueUP(1,2,u'丢失贴图：【'+one+' - '+getPath+u'】\n')
                                        ifRight = 1
                                    if self.checkCHN(getPath):
                                        self.theValueUP(1,87,u'中文贴图路径：【'+one+' - '+getPath+u'】\n')
                                        ifRight = 1

                if '<UDIM>.' not in getPathCom:
                    getPath = cmds.getAttr(one+'.fileTextureName')
                    if getPath not in self.getAllPath and getPath != '':
                        self.getAllPath.append(getPath)
                        if not os.path.exists(getPath):
                            self.theValueUP(1,2,u'丢失贴图：【'+one+' - '+getPath+u'】\n')
                            ifRight = 1
                        if self.checkCHN(getPath):
                            self.theValueUP(1,87,u'中文贴图路径：【'+one+' - '+getPath+u'】\n')
                            ifRight = 1
            if cmds.nodeType(one)=='aiImage':
                getPath = cmds.getAttr(one+'.filename')
                if getPath not in self.getAllPath and getPath != '':
                    self.getAllPath.append(getPath)
                    if not os.path.exists(getPath):
                        self.theValueUP(1,2,u'丢失贴图：【'+one+' - '+getPath+u'】\n')
                        ifRight = 1
                    if self.checkCHN(getPath):
                        self.theValueUP(1,87,u'中文贴图路径：【'+one+' - '+getPath+u'】\n')
                        ifRight = 1
        if ifRight == 0:
            self.theValueUP(1,0,self.No)
        return self.getAllPath      
    
    def checkMeshSkinTransform(self):
        ifRight = 0
        self.theAllObj = []
        for one in cmds.ls(type='skinCluster'):
            getObj = cmds.listConnections(one+'.outputGeometry')
            
            for oneObj in getObj:
                try:
                    getTr = cmds.getAttr(oneObj+'.translate')
                    getRo = cmds.getAttr(oneObj+'.rotate')
                    getSa = cmds.getAttr(oneObj+'.scale')
                    if getTr != [(0.0, 0.0, 0.0)] or getRo != [(0.0, 0.0, 0.0)] or getSa != [(1.0, 1.0, 1.0)]:
                        if not oneObj in self.theAllObj: 
                            self.theValueUP(1,23,u'未冻结变换的蒙皮物体：【'+oneObj+u'】\n')
                            ifRight = 1
                            self.theAllObj.append(oneObj)
                except:pass        
        if ifRight == 0:
            self.theValueUP(1,0,self.No) 
                           
    def checkOutline(self):
        ifRight = 0
        self.theCountOfParentDag = 0
        for one in cmds.ls(dag=True,type='transform',l=True):
            if not 'persp' in one and not 'top' in one and not 'front' in one and not 'side' in one:
                if len([oneStr for oneStr in one if '|' in oneStr])==1:
                    self.theCountOfParentDag+=1
        if self.theCountOfParentDag > 10:
            self.theValueUP(1,10,u'大纲顶层分组超过10个，可能有些凌乱\n')
            ifRight = 1
        if ifRight == 0:
            self.theValueUP(1,0,self.No)  
               
    def checkRefRenLayer(self):
        ifRight = 0
        for one in cmds.ls(type='renderLayer'):
            if ':' in one and not 'defaultRenderLayer' in one.split(':')[-1]:
                self.theValueUP(1,425,u'引用文件中的非默认渲染层：【'+one+u'】\n')
                ifRight = 1
        if ifRight == 0:
            self.theValueUP(1,0,self.No)
            
    def checkRefDisLayer(self):
        ifRight = 0
        for one in cmds.ls(type='displayLayer'):
            if ':' in one and not 'defaultLayer' in one.split(':')[-1]:
                self.theValueUP(1,75,u'引用文件中的非默认显示层：【'+one+u'】\n')
                ifRight = 1
        if ifRight == 0:
            self.theValueUP(1,0,self.No)   
                             
    def checkFaceMaterial(self):
        ifRight = 0
        self.theAllObj = []
        for one in cmds.ls(type='shadingEngine',l=True):
            if 'initialShadingGroup' not in one and 'initialParticleSE' not in one:
                getTheMesh = cmds.listConnections(one+'.memberWireframeColor')
                if getTheMesh != None:
                    for oneMesh in getTheMesh: 
                        if not oneMesh in self.theAllObj:
                            self.theValueUP(1,29,u'以面给材质的物体：【'+oneMesh+u'】\n')
                            ifRight = 1
        if ifRight == 0:
            self.theValueUP(1,0,self.No)        

    def checkSameNameJBY(self):
        ifRight = 0
        for one in cmds.ls():
            if '|' in one:
                self.theValueUP(1,2,u'同名节点：【'+one+u'】\n')
                ifRight = 1
        if ifRight == 0:
            self.theValueUP(1,0,self.No)
            
    def checkColonTwo(self):
        ifRight = 0
        for one in cmds.ls():
            if len([oneStr for oneStr in one if ':' in oneStr])>1:
                self.theValueUP(1,13,u'名字里一堆冒号影响市容的物体：【'+one+u'】\n')
                ifRight = 1
        if ifRight == 0:
            self.theValueUP(1,0,self.No)
            
    def checkUnknownJBY(self):
        ifRight = 0
        for one in cmds.ls(type='unknown'):
            self.theValueUP(1,6,u'未知节点：'+one+'\n')
            ifRight = 1
        if ifRight == 0:
            self.theValueUP(1,0,self.No)    
                   
    def checkSubRef(self):
        ifRight = 0
        for one in cmds.ls(type='reference'):
            try:
                if cmds.referenceQuery(one,parentNamespace=True) != [u'']:
                    self.theValueUP(1,15,u'双层引用：【'+one+u'】\n')
                    ifRight = 1
            except:pass
        if ifRight == 0:
            self.theValueUP(1,0,self.No)    
            
    def checkProjectName(self):
        ifRight = 0
        getProjectPath = cmds.workspace(q=True,fn=True)
        if self.checkCHN(getProjectPath):
            self.theValueUP(3,359,u'中文工程目录：【'+getProjectPath+u'】\n')
            ifRight = 1
        if ifRight == 0:
            self.theValueUP(1,0,self.No)
            
    def checkUserName(self):
        ifRight = 0
        getUserName = os.path.join(os.path.expandvars("%userprofile%")).split('\\')[-1]
        if self.checkCHN(getUserName):
            self.theValueUP(2,475,u'中文用户名：【'+getUserName+u'】\n')
            ifRight = 1
            
        if ifRight == 0:
            self.theValueUP(1,0,self.No)
            
    def checkPersp(self):
        ifRight = 0
        num = 0
        for one in cmds.listCameras():
            if 'persp' in one:
                num += 1
        if num > 1:
            self.theValueUP(1,43,u'场景内有多个大纲视图中不可见的 persp 相机!\n')
            ifRight = 1
        if ifRight == 0:
            self.theValueUP(1,0,self.No)
            
    def checkHis(self):
        ifRight = 0
        for one in cmds.ls(type='transform'):
            if 'transform' in one or 'null' in one :
                self.theValueUP(1,5,u'疑似临时节点(或未删历史) - 【'+one+u'】\n')
                ifRight = 1
        if ifRight == 0:
            self.theValueUP(1,0,self.No)
            
    def checkCHN(self,string):    
        ifZn=False
        for oneChar in string:
            if '\u' in str(repr(oneChar)):
                ifZn = True
        return ifZn
     
