# -*- coding: GBK -*-
import maya.cmds as cmds
import maya.OpenMayaUI as omui
import pymel.core as pmc
import shiboken2
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import Qt


__setVersion__ = 'V1.00'

def getMayaWindow():
    return shiboken2.wrapInstance(long(omui.MQtUtil.mainWindow()), QMainWindow)

def replaceConnections(sourceAttr,targetAttr,mode):
    getSourceAttr = pmc.PyNode(sourceAttr)
    getTargetAttr = pmc.PyNode(targetAttr)
    getConnects = getSourceAttr.inputs(p=True)
    if mode == 'output':
        getConnects = getSourceAttr.outputs(p=True)
    getSourceAttr.disconnect()
    if getConnects!=[]:
        try:
            if mode == 'input':
                getConnects[0].connect(getTargetAttr)
            if mode == 'output':
                getTargetAttr.connect(getConnects[0])
        except:
            cmds.warning(sourceAttr+u'链接替换失败')

def createFileTexture():
    tex = pmc.shadingNode('file', asTexture=True, isColorManaged=True)
    
    p2d = pmc.shadingNode('place2dTexture',  asUtility=True)

    tex.filterType.set(0)
    pmc.connectAttr(p2d.outUV, tex.uvCoord)
    pmc.connectAttr(p2d.outUvFilterSize, tex.uvFilterSize)
    pmc.connectAttr(p2d.vertexCameraOne, tex.vertexCameraOne)
    pmc.connectAttr(p2d.vertexUvOne, tex.vertexUvOne)
    pmc.connectAttr(p2d.vertexUvThree, tex.vertexUvThree)
    pmc.connectAttr(p2d.vertexUvTwo, tex.vertexUvTwo)
    pmc.connectAttr(p2d.coverage, tex.coverage)
    pmc.connectAttr(p2d.mirrorU, tex.mirrorU)
    pmc.connectAttr(p2d.mirrorV, tex.mirrorV)
    pmc.connectAttr(p2d.noiseUV, tex.noiseUV)
    pmc.connectAttr(p2d.offset, tex.offset)
    pmc.connectAttr(p2d.repeatUV, tex.repeatUV)
    pmc.connectAttr(p2d.rotateFrame, tex.rotateFrame)
    pmc.connectAttr(p2d.rotateUV, tex.rotateUV)
    pmc.connectAttr(p2d.stagger, tex.stagger)
    pmc.connectAttr(p2d.translateFrame, tex.translateFrame)
    pmc.connectAttr(p2d.wrapU, tex.wrapU)
    pmc.connectAttr(p2d.wrapV, tex.wrapV)
    return tex

def convertShaderAR_to_RS(inputAR):
    needDel = [inputAR]
    getNewRSMat = cmds.shadingNode('RedshiftMaterial',asShader=True,n=getNewName(inputAR,'toRS'))
    replaceConnections(inputAR+'.baseColor',getNewRSMat+'.diffuse_color','input')
    replaceConnections(inputAR+'.metalness',getNewRSMat+'.refl_metalness','input')
    replaceConnections(inputAR+'.specularRoughness',getNewRSMat+'.refl_roughness','input')
    replaceConnections(inputAR+'.outColor',getNewRSMat+'.outColor','output')
    getNormalMap = cmds.listConnections(inputAR+'.normalCamera')
    if getNormalMap :
        try:
            getTheNormalFile = cmds.listConnections(getNormalMap[0]+'.input')
            if getTheNormalFile :
                getFilePath = cmds.getAttr(getTheNormalFile[0]+'.fileTextureName')
                getNewRsNormalMap = cmds.shadingNode('RedshiftNormalMap',asTexture=True)
                cmds.setAttr(getNewRsNormalMap+'.tex0',getFilePath,type='string')
                cmds.connectAttr(getNewRsNormalMap+'.outDisplacementVector',getNewRSMat+'.bump_input',f=True)
        except:cmds.warning(inputAR+u' 在转换过程中法线节点存在异常.')
    cmds.delete(needDel)
    
def convertShaderRS_to_AR(inputRS):
    needDel = [inputRS]
    getNewARMat = cmds.shadingNode('aiStandardSurface',asShader=True,n=getNewName(inputRS,'toAR'))
    cmds.setAttr(getNewARMat+'.base',1)
    replaceConnections(inputRS+'.diffuse_color',getNewARMat+'.baseColor','input')
    replaceConnections(inputRS+'.refl_metalness',getNewARMat+'.metalness','input')
    replaceConnections(inputRS+'.refl_roughness',getNewARMat+'.specularRoughness','input')
    replaceConnections(inputRS+'.outColor',getNewARMat+'.outColor','output')
    getNormalMap = cmds.listConnections(inputRS+'.bump_input')
    if getNormalMap:
        try:
            getFilePath = cmds.getAttr(getNormalMap[0]+'.tex0')
            getNewFileNode = createFileTexture()
            getNewNormalMap = cmds.shadingNode('aiNormalMap',asTexture=True)
            cmds.setAttr(getNewNormalMap+'.invertY',1)
            cmds.setAttr(getNewFileNode+'.fileTextureName',getFilePath,type='string')
            cmds.connectAttr(getNewFileNode+'.outColor',getNewNormalMap+'.input',f=True)
            cmds.connectAttr(getNewNormalMap+'.outValue',getNewARMat+'.normalCamera',f=True)
        except:cmds.warning(inputRS+u' 在转换过程中法线节点存在异常.')

    cmds.delete(needDel)


def getNewName(inputName,target):
    theRenderArr = ['_toRS','_toAR']
    newName = inputName+'_'+target
    if theRenderArr[0] in inputName:
        inputName = inputName.replace(theRenderArr[0],'')
        newName = inputName  + theRenderArr[1] 
    if theRenderArr[1] in inputName:
        inputName = inputName.replace(theRenderArr[1],'')
        newName = inputName  + theRenderArr[0]  

    return newName
    


class AnalysisTheScene():
    def __init__(self):
        self.allNode_AR = []
        self.allNode_RS = []
        
    def updateData(self):
        self.getAllArNodes()
        self.getAllRsNodes()
        
    def getAllRsNodes(self):
        self.allNode_RS = cmds.ls(type='RedshiftMaterial',l=True)

    def getAllArNodes(self):
        self.allNode_AR = cmds.ls(type='aiStandardSurface',l=True)
    
    
class ConvertMaterial_UI(QTabWidget):
    def __init__(self):
        super(ConvertMaterial_UI,self).__init__()
        self.setParent(getMayaWindow()) 
        self.setMinimumSize(700,500)
        self.setWindowFlags(Qt.Window)
        self.AllData = AnalysisTheScene()
        self.__initUI__()
        self.updateAllData()
        self.colorStyleLow =" rgb(70,70,70)"
        self.colorStyle = "rgb(170,170,170)"
        self.colorStyleHigh ="#0099FF"
        self.colorStyleBlack = "rgb(60,60,60)"
        self.style = '''
                QTabWidget:pane
                            {
                                border-top:1px solid '''+self.colorStyle+''';
                                
                                
                            }
                QTabBar:tab
                            {
                              
                                
                                font-size:13px;
                                max-width:220px;
                                width:120px;
                                min-height:25px;
                            }
                QTabBar:tab:selected,QTabBar:tab:hover
                            {
                                color : '''+self.colorStyleHigh+''';
                                border-color:'''+self.colorStyleHigh+''';
             
                            }
                QTreeView:focus { border: none; }
                QTreeView{outline:none;selection-background-color: transparent;}
                QTreeView:item
                            {
                                
                                background: '''+self.colorStyleBlack+''';
                                shadow : rgb(9, 10, 12);
                                border: 1px solid ;
                                border-radius: 6px;
                                padding-top : 0px;
                                padding-bottom : 0px;
                                padding-left : 10px;
                                padding-right : 10px;
                                color : '''+self.colorStyle+''';
                                font-family:Roman times;
                                font-size:14px;
                                height : 20px;
                                width : 60px;
                            }


                QTreeView:item:selected
                            {
                              
                                shadow : '''+self.colorStyleHigh+''';
                                border: 1px solid ;
                                background-color:rgb(45,45,45);
                                border-radius: 8px;
                                padding-top : 0px;
                                font-size:13px;
                                padding-bottom : 0px;
                                padding-left : 5px;
                                padding-right : 0px;
                                color : '''+self.colorStyleHigh+''';
                                border-color:'''+self.colorStyleHigh+''';
                                height : 27px;
                                width : 60px;
                              
                            }
                QLineEdit
                            {
                                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgb(53, 57, 60), stop:1 rgb(33, 34, 36));
                                padding-top : 0px;
                                padding-bottom : 0px;
                                padding-left : 10px;
                                padding-right : 10px;
                                color : '''+self.colorStyle+''';
                                font-size:13px;
                                height : 20px;
                                width : 60px;
                            }
                QPushButton
                            {
                                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgb(53, 57, 60), stop:1 rgb(33, 34, 36));
                                shadow : rgb(9, 10, 12);
                                border: 2px solid rgb(9, 10, 12);
                                border-radius: 10px;
                                padding-top : 0px;
                                padding-bottom : 0px;
                                padding-left : 10px;
                                padding-right : 10px;
                                color : '''+self.colorStyle+''';
                                font-size:14px;
                                height : 20px;
                                width : 60px;
                            }
                QLabel,QListWidget{
                                outline:none;
                                shadow : rgb(9, 10, 12);
                                border: 0px solid rgb(9, 10, 12);
                                border-radius: 10px;
                                padding-top : 0px;
                                padding-bottom : 0px;
                                padding-left : 10px;
                                padding-right : 10px;
                                color : '''+self.colorStyle+''';
                                font-size:20px;
                                height : 20px;
                                width : 60px;
                            }
                 QListWidget::item:selected   
                            {
                                background:black; color:'''+self.colorStyleHigh+''';
                            }
                QPushButton:disabled
                            {
                                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgb(53, 57, 60), stop:1 rgb(33, 34, 36));
                                shadow : rgb(9, 10, 12);
                                border: 2px solid rgb(9, 10, 12);
                                border-radius: 10px;
                                padding-top : 0px;
                                padding-bottom : 0px;
                                padding-left : 10px;
                                padding-right : 10px;
                                color : '''+self.colorStyleLow+''';

                                height : 20px;
                                width : 60px;
                            }
                QPushButton:hover
                            {
                                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgb(53, 57, 60), stop:1 rgb(33, 34, 36));
                                shadow : '''+self.colorStyleHigh+''';
                                border: 2px solid rgb(9, 10, 12);
                                border-radius: 10px;
                                padding-top : 0px;
                                font-size:13px;
                                padding-bottom : 0px;
                                padding-left : 10px;
                                padding-right : 10px;
                                color : '''+self.colorStyleHigh+''';
                                border-color:'''+self.colorStyleHigh+''';
                                height : 27px;
                                width : 60px;
                            }
                QProgressBar
                            {
                                border:2px solid grey;
                                border-radius:5px;
                            }
                QProgressBar::chunk 
                            {
                                background-color:'''+self.colorStyle+''';
                                width:10px;
                                margin:0.5px;
                            }
                QProgressBar
                            {
                                border:2px solid grey;
                                border-radius:10px;
                                text-align: center;
                            }     
                    '''
        self.setStyleSheet(self.style)
        
    def __initUI__(self):
        self.setWindowTitle(u'RS-AR材质转换 ' + __setVersion__)
        self.mainLayout = QVBoxLayout()
        self.subLayout = QHBoxLayout()
        

        self.mainLayout.addLayout(self.subLayout)
        self.listWidget_AR = QListWidget(self)
        self.listWidget_RS = QListWidget(self)

        self.listWidget_AR.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidget_RS.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.changeButtonLayout = QVBoxLayout()
        self.leftLayout = QVBoxLayout()
        self.leftLayout2 = QHBoxLayout()

        self.leftLayout2.setAlignment(Qt.AlignCenter)
        self.leftLayout.addLayout(self.leftLayout2)
        self.rightLayout = QVBoxLayout()
        self.rightLayout2 = QHBoxLayout()
        self.rightLayout2.setAlignment(Qt.AlignCenter)
        self.rightLayout.addLayout(self.rightLayout2)
        self.leftLabel = QLabel(u'Arnold材质球')
        self.rightLabel = QLabel(u'RedShift材质球')
        self.leftButtonSelAll = QPushButton(u'全选')
        self.leftButtonSelAll.clicked.connect(self.leftSelectAll)
        self.rightButtonSelAll = QPushButton(u'全选')
        self.rightButtonSelAll.clicked.connect(self.rightSelectAll)
        self.leftLayout2.addWidget(self.leftLabel )
        self.leftLayout2.addWidget(self.leftButtonSelAll)
        self.leftLayout.addWidget(self.listWidget_AR)
        self.rightLayout2.addWidget(self.rightLabel )
        self.rightLayout2.addWidget(self.rightButtonSelAll)
        self.rightLayout.addWidget(self.listWidget_RS)

        self.button_AR_RS = QPushButton(u'====>')
        self.button_RS_AR = QPushButton(u'<====')
        self.button_AR_RS.clicked.connect(self.startConvert_AR_RS)
        self.button_RS_AR.clicked.connect(self.startConvert_RS_AR)
        
        self.changeButtonLayout.addWidget(self.button_AR_RS)
        self.changeButtonLayout.addWidget(self.button_RS_AR)

        self.subLayout.addLayout(self.leftLayout)
        self.subLayout.addLayout(self.changeButtonLayout)

        self.subLayout.addLayout(self.rightLayout)
        self.pbar = QProgressBar()
        self.pbar.setVisible(False)
        self.pbar.setTextVisible(False)
        self.pbar.setMaximumHeight(10)
        self.mainLayout.addWidget(self.pbar)
        self.setLayout(self.mainLayout)
        
        self.show()
        
    def updateAllData(self):
        self.AllData.updateData()
        self.listWidget_AR.clear()
        for oneNode in self.AllData.allNode_AR:
            itemAR = QListWidgetItem(oneNode)
            self.listWidget_AR.addItem(itemAR)
        self.listWidget_RS.clear()
        for oneNode in self.AllData.allNode_RS:
            itemRS = QListWidgetItem(oneNode)
            self.listWidget_RS.addItem(itemRS)
    
    def leftSelectAll(self):
        self.listWidget_AR.selectAll()

    def rightSelectAll(self):
        self.listWidget_RS.selectAll()
        
        
    def startConvert_AR_RS(self):
        self.pbar.setVisible(True)
        allMat = [oneItem.text() for oneItem in self.listWidget_AR.selectedItems()]
        allNum = allMat.__len__()
        for i,one in enumerate(allMat):
            if cmds.objExists(one):
                convertShaderAR_to_RS(one)
                self.pbar.setValue((i+1)*100/allNum)
        self.updateAllData()
        self.pbar.setVisible(False)
                
    def startConvert_RS_AR(self):
        self.pbar.setVisible(True)
        allMat = [oneItem.text() for oneItem in self.listWidget_RS.selectedItems()]
        allNum = allMat.__len__()
        for i,one in enumerate(allMat):
            if cmds.objExists(one):
                convertShaderRS_to_AR(one)
                self.pbar.setValue((i+1)*100/allNum)
        self.updateAllData()
        self.pbar.setVisible(False)
    
    