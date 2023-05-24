# -*- coding: GBK -*-
import pymel.core as pmc
import maya.cmds as cmds
'''
 选择顺序千万不能错,先选择被复制权重的源模型,再选择所有需要权重的模型或组（有无蒙皮都无所谓）,再执行
 by 劲爆羊 2018/8/7 测试环境 maya2017-update5
'''
class CopyTheWeightJBY():
    def __init__(self):
        pass

    def getAllHistoryNodesByType(self,inputNodes,theType):
        getIter = inputNodes.__iter__()
        getAllNodes = [] 
        while getIter:
            try:
                getAllNodes.extend(getIter.next().listHistory(type=theType))
            except StopIteration:
                break
        return list(set(getAllNodes))

    def createSkinClusterToObjects(self,theSourceSkinNode,theBones,theObjcts):
        getTheObjIter = theObjcts.__iter__()
        while getTheObjIter:
            try:
                getTheSkinClusterNew = ''
                theOBJ = getTheObjIter.next()
                getTheSCs = self.getAllHistoryNodesByType([theOBJ],'skinCluster')
                if getTheSCs:
                    getTheSkinClusterNew = getTheSCs[0]
                else:
                    getTheSkinClusterNew = pmc.skinCluster(theBones, theOBJ,tsb=True)
                pmc.copySkinWeights(ss=theSourceSkinNode,ds=getTheSkinClusterNew,noMirror=True,surfaceAssociation='closestPoint',influenceAssociation=('oneToOne','closestJoint','closestJoint'))
            except StopIteration:
                break

    def getAllChildren(self,theInputs,theOutputs):
        getTheInputsIter = theInputs.__iter__()
        while getTheInputsIter:
            try:
                theItem = getTheInputsIter.next()
                if theItem.getShape():
                    theOutputs.append(theItem)
                getChildren = pmc.listRelatives(theItem,f=True,type='transform',c=True)
                if getChildren:
                    self.getAllChildren(getChildren,theOutputs)
            except StopIteration:
                break
                
    def startCopyWeight(self):            
        getSel = pmc.ls(sl=True)
        getAllBones = self.getAllHistoryNodesByType(getSel[:1],'joint')
        if getAllBones:
            getAllSkinCluster = self.getAllHistoryNodesByType(getSel[:1],'skinCluster')
            getChildren = []
            self.getAllChildren(getSel[1:],getChildren)
            self.createSkinClusterToObjects(getAllSkinCluster[0],getAllBones,getChildren)
        else:
            pmc.warning(u'第一个选择的源物体没有蒙皮！')


class CopyTheWeightJBY_UI(): 
    def __init__(self):
        self.initUI()
        
    def initUI(self):
        if pmc.window('win_copyWeight',ex=True):
            pmc.deleteUI('win_copyWeight')
        pmc.window('win_copyWeight',t=u'羊牌复制权重小工具 v1.00 by劲爆羊 2018/8/7')
        pmc.gridLayout(cwh=(550,60),nc=1)
        pmc.text(l='选择顺序千万不能错\n先选择【被复制权重的源模型】\n再选择【所有需要权重的模型或组（有无蒙皮都无所谓）】\n最后执行以下代码（测试环境 maya2017-update5）')
        pmc.button(l=u'复制',c=self.command_copy)
        pmc.setParent('..')
        pmc.showWindow('win_copyWeight')

    def command_copy(self,*args):
        startCopy = CopyTheWeightJBY()
        startCopy.startCopyWeight()
