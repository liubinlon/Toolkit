##--------------------------------------------------------------------------
##
## ScriptName : rapidScrews
## Contents   : click to place screws from Libaray
## Author     : Joe Wu
## URL        : http://im3djoe.com
## Since      : 2019/11
## LastUpdate : 2019/12/04 
## Version    : 1.0  First version for public test
##            : 1.01 add vtc lock, screws can lock to target vtx now.
##            : 1.02 imporved vtx lock with slider
##            : 1.03 added subfolder support
##            : 1.04 added random spin
##            : 1.1  rework without normal constraint witch cuase lots of crash
##            : 1.11 remove lock, now use slider to check state,adding depth slider
##            : 1.2  import file via abc to avoid maya crash due to unknow error, eg metalray node ...ect
##            : 1.3  slider update to all in between geo
## Other Note : only test in maya 2019.1 windows enviroment 
##
## Install    : copy and paste script into a python tab in maya script editor
##--------------------------------------------------------------------------

import maya.cmds as mc
import maya.mel as mel
import maya.OpenMaya as oma
import maya.OpenMayaUI as omui
from maya.OpenMaya import MGlobal
import math
import os
import random
import re
from pymel.core.datatypes import Vector, Matrix, Point

meshDirectory = (mc.moduleInfo(mn="MS_Toolkit",p=True))+"/tools/MSTools/MST_DATA/scripts/samples"
 
#global pressFirstTime

def jwMeshPlaceUI():
    global meshDirectory
    global sampleFileChoice
    sampleFileChoice = []
    global SycList
    SycList = []

    if mc.window("jwMeshPlaceUI", exists = True):
        mc.deleteUI("jwMeshPlaceUI")
    jwMeshPlaceUI = mc.window("jwMeshPlaceUI",title = "Rapid Screws v1.3", w=340,mxb = False, s = 1 ,bgc = [0.2, 0.2, 0.2  ])
    mc.columnLayout('topBar', adjustableColumn=0)
    mc.separator(height= 10, style= 'in')
    mc.columnLayout('contCM')
    mc.rowColumnLayout(nc=3,cw=[(1,80),(2,20),(3,250)])
    mc.text(l ='              类型')
    mc.text(l ='')
    mc.radioButtonGrp('meshImportType', nrb=3, sl=1, labelArray3=['网格', '实例化', 'GPU 缓存'], cw = [(1,70),(2,80) ,(3,150)],cc='finishTool()')
    mc.text(l ='')
    mc.setParent( '..' ) 
    
    mc.rowColumnLayout(nc=4 ,cw=[(1,80),(2, 20),(3,250),(4,50)])
    mc.text(l ='             旋转')
    mc.text(l ='')
    mc.floatSliderGrp( 'meshRotSlide' ,w= 250, precision= 1, v = 0, field= 1, min= -180, max= 180,dc='updateRotate()',cc='updateRotate()')
    mc.button('jwResetRot', l= '重置',  c= 'jwMeshResetRot()')
    mc.setParent( '..' ) 
    mc.rowColumnLayout(nc=7 ,cw=[(1,100),(2,50),(3,50),(4,50),(5,50),(6,50),(7,50)])
    mc.text(l ='')
    mc.button('jwRotA', l= "-90", c= 'jwMeshSetRot(-90)')
    mc.button('jwRotB', l= "-45", c= 'jwMeshSetRot( -45)')
    mc.button('jwRotC', l= "-30", c= 'jwMeshSetRot( -30)')
    mc.button('jwRotD', l= "30",  c= 'jwMeshSetRot( 30)')
    mc.button('jwRotE', l= "45",  c= 'jwMeshSetRot( 45)')
    mc.button('jwRotF', l= "90",  c= 'jwMeshSetRot( 90)')
    mc.setParent( '..' ) 
    mc.rowColumnLayout(nc=4 ,cw=[(1,80),(2, 20),(3,250),(4,50)])
    mc.text(l ='      随机旋转')
    mc.text(l ='')
    mc.floatSliderGrp( 'randomRotSlide' ,w= 250, precision = 0, v = 0, field= 1, min= 0, max= 360,dc='updateRotateRandom()',cc='updateRotateRandom()')
    mc.button('jwResetRandomRot', l= '重置',  c= 'jwMeshResetRandomRot()')
    mc.setParent( '..' ) 

    mc.text(l ='')
    mc.rowColumnLayout(nc=4 ,cw=[(1,80),(2,20),(3,250),(4,50)])
    mc.text(l ='             缩放')
    mc.text(l ='')
    mc.floatSliderGrp( 'meshScaleSlide' ,v = 1,  precision= 1, field= 1, min= 0.1, max= 5, dc='updateScale()',cc='updateScale()')
    mc.button('meshScaleReset', l= '重置',  c= 'jwMeshResetScale()')
    mc.setParent( '..' ) 

    mc.rowColumnLayout(nc=4 ,cw=[(1,80),(2, 20),(3,250),(4,50)])
    mc.text(l ='      随机缩放')
    mc.text(l ='')
    mc.floatSliderGrp( 'randomScaleSlide' ,w= 250, precision = 2, v = 0, field= 1, min= 0, max= 1,dc='updateRandomScale()',cc='updateRandomScale()')
    mc.button('jwResetRandomScale', l= '重置',  c= 'jwMeshResetRandomScale()')
    mc.setParent( '..' ) 
    mc.text(l ='')
    mc.rowColumnLayout(nc=4 ,cw=[(1,80),(2,20),(3,250),(4,50)])
    mc.text(l ='      旋转缩放')
    mc.text(l ='')
    mc.floatSliderGrp( 'meshBetweenSlide' ,v = 0,  precision= 0,  field= 1, min= 0, max= 10)
    mc.button('meshBetweenReset', l= '重置',  c= 'jwMeshResetBetween()')
    mc.setParent( '..' ) 
    
    mc.text(l ='')
    mc.rowColumnLayout(nc=4 ,cw=[(1,80),(2,20),(3,250),(4,50)])
    mc.text(l ='             深度')
    mc.text(l ='')
    mc.floatSliderGrp( 'meshDepthSlide' ,v = 0,  precision= 2, field= 1, min= -1, max= 5,dc='updateDepth()',cc='updateDepth()')
    mc.button('meshDepthReset', l= '重置',  c= 'jwMeshResetDepth()')
    mc.setParent( '..' ) 
    
    mc.rowColumnLayout(nc=4 ,cw=[(1,80),(2,20),(3,250),(4,50)])
    mc.text(l ='             吸附')
    mc.text(l ='')
    mc.floatSliderGrp( 'snapVSlider' ,v = 0,  precision= 2, field= 1, min= 0, max= 5)
    mc.button('snapVReset', l= '重置',  c= 'jwMeshResetSnapV()')
    mc.setParent( '..' )  
    
    mc.separator(height= 10, style= 'in')
    mc.scrollLayout('lib')
    mc.frameLayout('请在脚本里面指定库文件',bgc =[0.265, 0.265, 0.265])
    mc.setParent( '..' ) 
    mc.setParent( '..' ) 
    mc.setParent( '..' ) 

    mc.separator(height= 20, style= 'out')
    mc.rowLayout(nc=3 ,cw=[(1,360),(2,45),(3,45)])
    mc.intSliderGrp( 'iconSize', cw3=[100, 40, 250], label = '   每行图标个数         ',  field= 1, min= 1, max= 5, v = 5 ,cc= 'jwfloatResizeIcon()', dc= 'jwfloatResizeIcon()')
    mc.setParent( '..' )
    mc.showWindow(jwMeshPlaceUI)


def multiButtonToggle():
    checkState = mc.radioButtonGrp('meshMultiMode',  q =True , sl= True)
    iconLightOff()
    if checkState == 1:
        mc.button('goMultiButton',  e =True , en = False)
        mc.button('multiCleanButton',  e =True , en = False)

    else:
        mc.button('goMultiButton',  e =True , en = True)
        mc.button('multiCleanButton',  e =True , en = True) 
    
    
def screenVisPoly():
    commonList= []
    view = omui.M3dView.active3dView()
    oma.MGlobal.selectFromScreen(0, 0, view.portWidth(), view.portHeight(), oma.MGlobal.kReplaceList)
    objects = oma.MSelectionList()
    sel = oma.MSelectionList()
    oma.MGlobal.getActiveSelectionList(objects)
    #restore selection
    oma.MGlobal.setActiveSelectionList(sel, oma.MGlobal.kReplaceList)
    #return the objects as strings
    fromScreen = []
    objects.getSelectionStrings(fromScreen)
    shapesOnScreen = mc.listRelatives(fromScreen, shapes=True,f=True)
    meshList = mc.ls(type='mesh',l=True)#only polygon
    if len(meshList)>0 and shapesOnScreen is not None:
        commonList = list(set(meshList) & set(shapesOnScreen))
        return commonList
    else:
        commonList = []
    return commonList



def finishTool():
    restoreSelVis()
    #mc.MoveTool()
    mc.select(cl=True)
    iconLightOff()
    
def restoreSelVis():
    mc.modelEditor('modelPanel1', e=True, sel=True)
    mc.modelEditor('modelPanel2', e=True, sel=True)
    mc.modelEditor('modelPanel3', e=True, sel=True)
    mc.modelEditor('modelPanel4', e=True, sel=True)
    
def hideSelVis():
    mc.modelEditor('modelPanel1', e=True, sel=False)
    mc.modelEditor('modelPanel2', e=True, sel=False)
    mc.modelEditor('modelPanel3', e=True, sel=False)
    mc.modelEditor('modelPanel4', e=True, sel=False)  



                
def updateRandomScale():
    randomScale = mc.floatSliderGrp('randomScaleSlide' , q=True, v=True)
    scaleXXX = mc.floatSliderGrp('meshScaleSlide', q=True, v=True)
    global SycList
    if len(SycList)>0:
        for s in SycList:
            if mc.objExists(s):
                if randomScale > 0:
                    randomNumber = random.uniform((scaleXXX-randomScale),(scaleXXX+randomScale))
                    mc.setAttr((s+'.scaleX'),randomNumber)
                    mc.setAttr((s+'.scaleY'),randomNumber)
                    mc.setAttr((s+'.scaleZ'),randomNumber)
                else:
                    mc.setAttr((s+'.scaleX'),scaleXXX)
                    mc.setAttr((s+'.scaleY'),scaleXXX)
                    mc.setAttr((s+'.scaleZ'),scaleXXX)
 
def updateScale():
    scaleXXX = mc.floatSliderGrp('meshScaleSlide', q=True, v=True)
    global SycList
    if len(SycList)>0:
        for s in SycList:
            if mc.objExists(s):
                if mc.objExists(s):
                    mc.setAttr((s+'.scaleX'),scaleXXX)
                    mc.setAttr((s+'.scaleY'),scaleXXX)
                    mc.setAttr((s+'.scaleZ'),scaleXXX)

def updateDepth():
    depthXXX = mc.floatSliderGrp('meshDepthSlide', q=True, v=True)
    global SycList
    if len(SycList)>0:
        for s in SycList:
            if mc.objExists(s):
                mc.setAttr((s+'.translateY'),depthXXX)

def updateRotate():
    rotXXX = mc.floatSliderGrp('meshRotSlide', q=True, v=True)
    global SycList
    if len(SycList)>0:
        for s in SycList:
            if mc.objExists(s):
                mc.setAttr((s+'.rotateY'),rotXXX)

def jwMeshSetRot(angle):
    global SycList
    if len(SycList)>0:
        for s in SycList:
            if mc.objExists(s):
                mc.setAttr((s+'.rotateY'),angle)

def updateRotateRandom():
    randomY = mc.floatSliderGrp( 'randomRotSlide' ,q=1,v=True)
    global SycList
    if len(SycList)>0:
        for s in SycList:
            if mc.objExists(s):
                randomNumber = random.uniform(0,randomY)
                mc.setAttr((s+'.rotateY'),int(randomNumber))

   
def killInitalSample():
    iconLightOff()


def offPressPlace():
    global betweenList
    global betweenList3DPos
    betweenList3DPos = []
    mc.refresh(cv=True,f=True)
    for e in betweenList:
        attList = ['translateX','translateY','translateZ']
        attListRecord =['ptX','ptY','ptZ']
        for a in range(len(attList)):
            attListRecord[a] = mc.getAttr(e +'.'+attList[a])
        pos3D = (attListRecord[0],attListRecord[1],attListRecord[2])
        betweenList3DPos.append(pos3D )
    
def getPosition(SX,SY):
    global betweenListShape
    global checkVisList
    pos = oma.MPoint()
    dir = oma.MVector()
    hitpoint = oma.MFloatPoint()
    omui.M3dView().active3dView().viewToWorld(int(SX), int(SY), pos, dir)
    pos2 = oma.MFloatPoint(pos.x, pos.y, pos.z)
    #current camera
    view = omui.M3dView.active3dView()
    cam = oma.MDagPath()
    view.getCamera(cam)
    camPath = cam.fullPathName()
    
    cameraTrans = mc.listRelatives(camPath,type='transform',p=True)
    cameraPosition = mc.xform(cameraTrans,q=1,ws=1,rp=1)
    
    checkHit = 0
    finalMesh = []
    finalX = []
    finalY = []
    finalZ = []
    
    shortDistance = 10000000000
    distanceBetween = 1000000000
    
    hitFacePtr = oma.MScriptUtil().asIntPtr()
    hitFace = []
    checkList =  list(set(checkVisList)-set(betweenListShape))
    for mesh in checkList:
        selectionList = oma.MSelectionList()
        selectionList.add(mesh)
        dagPath = oma.MDagPath()
        selectionList.getDagPath(0, dagPath)
        fnMesh = oma.MFnMesh(dagPath)
        
        intersection = fnMesh.closestIntersection(
        oma.MFloatPoint(pos2),
        oma.MFloatVector(dir),
        None,
        None,
        False,
        oma.MSpace.kWorld,
        99999,
        False,
        None,
        hitpoint,
        None,
        hitFacePtr,
        None,
        None,
        None)
        
        if intersection:
            x = hitpoint.x
            y = hitpoint.y
            z = hitpoint.z
            distanceBetween = math.sqrt( ((float(cameraPosition[0]) - x)**2)  + ((float(cameraPosition[1]) - y)**2) + ((float(cameraPosition[2]) - z)**2))
            if distanceBetween < shortDistance:
                shortDistance = distanceBetween
                finalMesh = mesh
                finalX = x
                finalY = y
                finalZ = z
                hitFace = oma.MScriptUtil(hitFacePtr).asInt()

    return finalX, finalY, finalZ ,finalMesh ,hitFace
    mc.refresh(cv=True,f=True)

def onPressPlace():
    global ctx
    global betweenListShape
    betweenListShape = []
    global SycList
    SycList = []
    global sampleFileChoice
    global selectionPool
    global combineSelPool
    global pressFirstTime
    global betweenFirstTime
    betweenFirstTime = 1
    global screenX,screenY
    global headMesh
    headMesh = []
    global tailMesh
    tailMesh = []
    vpX, vpY, _ = mc.draggerContext(ctx, query=True, anchorPoint=True)
    screenX = vpX
    screenY = vpY
    meshTypeState = mc.radioButtonGrp('meshImportType', q=True , sl=True)
    try:
        if pressFirstTime == 1:
            #check samplePool still item, if yes random select one 
            #multiMode
            newChoice = []
            if len(sampleFileChoice) > 1:
                randomNumber = random.randint(0,(len(sampleFileChoice)-1))
                newChoice = sampleFileChoice[randomNumber]
                sampleFileChoice.remove(newChoice)
                selectionPool.append(newChoice)
                            
            else:
                newChoice = sampleFileChoice[0]
                sampleFileChoice.remove(newChoice)
                selectionPool.append(newChoice)
                pressFirstTime = 0
            
            #combine two list for selection###bug
            combineSelPool = list(set(sampleFileChoice + selectionPool))
            mc.select(newChoice)
        else:
            newNodeA = []
            randomNumber = random.randint(0,(len(combineSelPool)-1))
            newChoiceA = combineSelPool[randomNumber]
            if meshTypeState == 2:
                #only instance mesh not tranform node
                newNodeA = mc.duplicate(newChoiceA,rr=True)
                mc.select(newNodeA)
                mc.pickWalk(d='Down')
                meshNode = mc.ls(sl=True,l=True)
                mc.select(newChoiceA)
                mc.pickWalk(d='Down')
                mc.instance()
                mc.delete(meshNode)
                intNode = mc.ls(sl=True,l=True)
                mc.parent(intNode,newNodeA)
                mc.rename(meshNode[0].split('|')[-1])
                mc.pickWalk(d='up')
            else:
                newNodeA = mc.duplicate(newChoiceA,rr=True)
            mc.select(newNodeA)        

        tempSel = mc.ls(sl=1,type='transform')
        meshNode = mc.listRelatives(tempSel[0],ad=True, typ = 'transform',f=True)
        SycList.append(meshNode[0])
        meshNode = mc.listRelatives(tempSel[0],ad=True, typ = 'transform',f=True)
        myShape = mc.listRelatives(meshNode, shapes=True,f=True)

        wx,wy,wz,hitmesh,hitFace= getPosition(screenX,screenY)
        mc.setAttr((tempSel[0] + '.translateX'), wx)
        mc.setAttr((tempSel[0] + '.translateY'), wy)
        mc.setAttr((tempSel[0] + '.translateZ'), wz)
        hitFaceName = (hitmesh + '.f[' + str(hitFace) +']')
        rx, ry, rz = getFaceAngle(hitFaceName) 
        mc.setAttr((tempSel[0] + '.rotateX'), rx)
        mc.setAttr((tempSel[0] + '.rotateY'), ry)
        mc.setAttr((tempSel[0] + '.rotateZ'), rz)        
        currentScaleX = mc.floatSliderGrp('meshScaleSlide', q=True, v=True)
        currnetRotY =  mc.floatSliderGrp('meshRotSlide', q=True, v=True)
        currentDepth = mc.floatSliderGrp('meshDepthSlide', q=True, v=True)
        mc.setAttr((meshNode[0]+'.scaleX'),currentScaleX)
        mc.setAttr((meshNode[0]+'.scaleY'),currentScaleX)
        mc.setAttr((meshNode[0]+'.scaleZ'),currentScaleX)
        mc.floatSliderGrp('meshScaleSlide', e=True, v = currentScaleX)
        mc.setAttr((meshNode[0]+'.rotateY'),currnetRotY)
        mc.setAttr((meshNode[0]+'.translateY'),currentDepth)
        randomY = mc.floatSliderGrp( 'randomRotSlide' ,q=1,v=True)
        if (randomY > 0):
            randomNumber = random.uniform(0,randomY)
            mc.setAttr((meshNode[0]+'.rotateY'),int(randomNumber))
        silderScale = mc.floatSliderGrp( 'meshScaleSlide' ,q=1,v=True)
        randomScale = mc.floatSliderGrp( 'randomScaleSlide' ,q=1,v=True)
        if (randomScale > 0):
            randomNumber = random.uniform((-1*randomScale),randomScale)
            mc.setAttr((meshNode[0]+'.scaleX'),(randomNumber+silderScale))
            mc.setAttr((meshNode[0]+'.scaleY'),(randomNumber+silderScale))
            mc.setAttr((meshNode[0]+'.scaleZ'),(randomNumber+silderScale))
        mc.select(tempSel)
    except:
        pass
    
    mc.refresh(cv=True,f=True)


        
def onDragPlace():
    global ctx
    global pressFirstTime
    global betweenFirstTime
    global screenX,screenY
    global betweenList
    global betweenListShape
    global checkVisList
    global combineSelPool
    global SycList
    global headMesh
    global tailMesh
    global lastPanelActive
    lastPanelActive = mc.getPanel(underPointer=True)

    currentSX = 0
    currnetSY = 0
    goStrightLine = mc.floatSliderGrp('meshBetweenSlide', q=True, v=True)
    randomY = mc.floatSliderGrp( 'randomRotSlide' ,q=1,v=True)
    meshTypeState = mc.radioButtonGrp('meshImportType', q=True , sl=True)
    
    selSample = []
    selSample = mc.ls(sl=True,fl=True,l=True)
    headMesh = selSample[0]
    if len(selSample)>0:
        if (goStrightLine > 0):
            if betweenFirstTime == 1:
                #need to give one sample to first position           
                attList = ['translateX','translateY','translateZ','rotateX','rotateY','rotateZ','scaleX','scaleY','scaleZ']
                attListRecord =['ptX','ptY','ptZ','prX','prY','prZ','psX','psY','psZ']
                for a in range(len(attList)):
                    attListRecord[a] = mc.getAttr(selSample[0]+'.'+attList[a])
                #pick up sample if multiMode
                if len(combineSelPool)>1:
                        randomNumber = random.randint(0,(len(combineSelPool)-1))
                        mc.select(combineSelPool[randomNumber])
                else:
                    mc.select(selSample[0])
                keepItMesh = mc.ls(sl=1,fl=1)
                #make a copy
                if meshTypeState == 2:
                    #only instance mesh not tranform node
                    newKeepNode = mc.duplicate(keepItMesh[0],rr=True)
                    mc.select(newKeepNode)
                    mc.pickWalk(d='Down')
                    meshKeepNode = mc.ls(sl=True,l=True)
                    mc.select(keepItMesh[0])
                    mc.pickWalk(d='Down')
                    mc.instance()
                    mc.delete(meshKeepNode)
                    intKeepNode = mc.ls(sl=True,l=True)
                    mc.parent(intKeepNode,newKeepNode)
                    intKeepNode = mc.ls(sl=True,l=True)
                    mc.rename(meshKeepNode[0].split('|')[-1])
                    mc.pickWalk(d='up')
                else:
                    mc.duplicate(keepItMesh[0])
                #restore position
                checkKeepNode = mc.ls(sl=1,fl=1)
                for b in range(len(attList)):
                    mc.setAttr((checkKeepNode[0]+'.'+attList[b]),attListRecord[b]) 
                checkKeepNodeChild = mc.listRelatives(checkKeepNode[0],ad=True, typ = 'transform',f=True)
                SycList.append(checkKeepNodeChild[0])
                
                meshNodeA = mc.listRelatives(selSample[0],ad=True, typ = 'transform',f=True)
                SycList.append(meshNodeA[0])
                if randomY > 0:
                    randomNumber = random.uniform(0,randomY)
                    mc.setAttr((meshNodeA[0]+'.rotateY'),int(randomNumber))
                
                tailMesh = checkKeepNode[0]
                betweenList = []
                betweenListShape = []
                #get in between element
                for i in range(int(goStrightLine)):
                    if len(combineSelPool)>1:
                        randomNumber = random.randint(0,(len(combineSelPool)-1))
                        mc.select(combineSelPool[randomNumber])
                    else:
                        mc.select(selSample[0])
                    
                    newBetweenDulpi = mc.ls(sl=True,fl=True,l=True)
                    if meshTypeState == 2:
                        #only instance mesh not tranform node
                        newNode = mc.duplicate(newBetweenDulpi[0],rr=True)
                        mc.select(newNode)
                        mc.pickWalk(d='Down')
                        meshNode = mc.ls(sl=True,l=True)
                        mc.select(newBetweenDulpi[0])
                        mc.pickWalk(d='Down')
                        mc.instance()
                        mc.delete(meshNode)
                        intNode = mc.ls(sl=True,l=True)
                        mc.parent(intNode,newNode)
                        intNode = mc.ls(sl=True,l=True)
                        mc.rename(meshNode[0].split('|')[-1])
                        mc.pickWalk(d='up')
                    else:
                        mc.duplicate(newBetweenDulpi[0])
                    
                    selBetween = mc.ls(sl=True,fl=True,l=True)
                    meshNodeB = mc.listRelatives(selBetween[0],ad=True, typ = 'transform',f=True)

                    if randomY > 0:
                        randomNumber = random.uniform(0,randomY)
                        mc.setAttr((meshNodeB[0]+'.rotateY'),int(randomNumber))
                    
                    silderScale = mc.floatSliderGrp( 'meshScaleSlide' ,q=1,v=True)
                    randomScale = mc.floatSliderGrp( 'randomScaleSlide' ,q=1,v=True)
                    if (randomScale > 0):
                        randomNumber = random.uniform((-1*randomScale),randomScale)
                        mc.setAttr((meshNodeB[0]+'.scaleX'),(randomNumber+silderScale))
                        mc.setAttr((meshNodeB[0]+'.scaleY'),(randomNumber+silderScale))
                        mc.setAttr((meshNodeB[0]+'.scaleZ'),(randomNumber+silderScale))
                    SycList.append(meshNodeB[0])
                    betweenShape = mc.listRelatives(selBetween[0], fullPath=True ,ad=True)
                    betweenList.append(selBetween[0])
                    betweenListShape.append(betweenShape[0])
                    betweenFirstTime = 0
        else:
            betweenListShape = []

        modifiers = mc.getModifiers()
        if (modifiers == 4):
            #print 'ctrl Press'
            if len(SycList)>0:
                for s in SycList:
                    sY = mc.getAttr(s + '.rotateY')
                    mc.setAttr((s+'.rotateY'),(sY + 1))
            mc.refresh(f=True)
            
        elif(modifiers == 1):
            #print 'shift selSample'
            if len(SycList)>0:
                for s in SycList:
                    sY = mc.getAttr(s + '.rotateY')
                    mc.setAttr((s+'.rotateY'),(sY - 1))
            mc.refresh(cv=True,f=True)
        else:
            vpX, vpY, _ = mc.draggerContext(ctx, query=True, dragPoint=True)
            currentSX = vpX
            currentSY = vpY
            pos = oma.MPoint()
            dir = oma.MVector()
            hitpoint = oma.MFloatPoint()
            omui.M3dView().active3dView().viewToWorld(int(vpX), int(vpY), pos, dir)
            pos2 = oma.MFloatPoint(pos.x, pos.y, pos.z)
            
            #current camera
            view = omui.M3dView.active3dView()
            cam = oma.MDagPath()
            view.getCamera(cam)
            camPath = cam.fullPathName()
            
            cameraTrans = mc.listRelatives(camPath,type='transform',p=True)
            cameraPosition = mc.xform(cameraTrans,q=1,ws=1,rp=1)
            
            checkHit = 0
            finalMesh = []
            finalX = 0
            finalY = 0
            finalZ = 0
            shortDistance = 10000000000
            distanceBetween = 1000000000
           

            meshNode = mc.listRelatives(selSample, fullPath=True ,ad=True)
            myShape = mc.listRelatives(meshNode, shapes=True,f=True)
            if myShape == None:#gpu
                checkList =  list(set(checkVisList))
            else:
                checkList =  list(set(checkVisList)-set(myShape)-set(betweenListShape))
            
            hitFacePtr = oma.MScriptUtil().asIntPtr()
            hitFace = []
            for mesh in checkList:
  
                selectionList = oma.MSelectionList()
                selectionList.add(mesh)
                dagPath = oma.MDagPath()
                selectionList.getDagPath(0, dagPath)
                fnMesh = oma.MFnMesh(dagPath)
               
                intersection = fnMesh.closestIntersection(
                oma.MFloatPoint(pos2),
                oma.MFloatVector(dir),
                None,
                None,
                False,
                oma.MSpace.kWorld,
                99999,
                False,
                None,
                hitpoint,
                None,
                hitFacePtr,
                None,
                None,
                None)
                
                if intersection:
                    x = hitpoint.x
                    y = hitpoint.y
                    z = hitpoint.z
                    distanceBetween = math.sqrt( ((float(cameraPosition[0]) - x)**2)  + ((float(cameraPosition[1]) - y)**2) + ((float(cameraPosition[2]) - z)**2))
                    if distanceBetween < shortDistance:
                        shortDistance = distanceBetween
                        finalMesh = mesh
                        hitFace = oma.MScriptUtil(hitFacePtr).asInt()
                        finalX = x
                        finalY = y
                        finalZ = z
                    
                    mc.setAttr((selSample[0] + '.translateX'), finalX)
                    mc.setAttr((selSample[0] + '.translateY'), finalY)
                    mc.setAttr((selSample[0] + '.translateZ'), finalZ)
                    hitFaceName = (finalMesh + '.f[' + str(hitFace) +']')
                    rx, ry, rz = getFaceAngle(hitFaceName) 
                    mc.setAttr((selSample[0] + '.rotateX'), rx)
                    mc.setAttr((selSample[0] + '.rotateY'), ry)
                    mc.setAttr((selSample[0] + '.rotateZ'), rz)
                    lockVtxCheck = mc.floatSliderGrp('snapVSlider', q=True, v=True)
                    if (lockVtxCheck > 0):
                        cvX = 0
                        cvY = 0
                        cvZ = 0
                        shortDistanceCheck = 10000
                        checkCVDistance = 10000
                        mostCloseDist = lockVtxCheck
                        hitFaceName = (finalMesh + '.f[' + str(hitFace) +']')
                        cvList = (mc.polyInfo(hitFaceName , fv=True )[0]).split(':')[-1].split('    ')
                        cvList = [x for x in cvList if x.strip()]
                        mostCloseCVPoint = []
                        for v in cvList:
                            checkNumber = ''.join([n for n in v.split('|')[-1] if n.isdigit()]) 
                            if len(checkNumber) > 0:
                                cvPoint = (finalMesh + '.vtx[' + str(checkNumber) +']')
                                cvPosition = mc.pointPosition(cvPoint)
                                checkCVDistance = math.sqrt( ((float(cvPosition[0]) - finalX)**2)  + ((float(cvPosition[1]) - finalY)**2) + ((float(cvPosition[2]) - finalZ)**2))
                                if checkCVDistance < shortDistanceCheck:
                                    shortDistanceCheck = checkCVDistance
                                    cvX = float(cvPosition[0])
                                    cvY = float(cvPosition[1])
                                    cvZ = float(cvPosition[2])
                                    mostCloseCVPoint = cvPoint
                        if shortDistanceCheck < mostCloseDist:
                            mc.setAttr((selSample[0] + '.translateX'), cvX)
                            mc.setAttr((selSample[0] + '.translateY'), cvY)
                            mc.setAttr((selSample[0] + '.translateZ'), cvZ)
                            #get average normal angle from suround faces
                            rX,rY,rZ = avgVertexNormalAngle(cvPoint)
                            mc.setAttr(selSample[0]+'.rotateX', rX)
                            mc.setAttr(selSample[0]+'.rotateY', rY)
                            mc.setAttr(selSample[0]+'.rotateZ', rZ)

                    # caculate new inBetween position        
                    for a in range(int(goStrightLine)):
                        disX = (screenX - currentSX)/(goStrightLine+1)
                        disY = (screenY - currentSY)/(goStrightLine+1)
                        nextX = 0
                        nextY = 0
                        nextX =   screenX -(disX*(a+1))
                        nextY =   screenY -(disY*(a+1)) 
                        wx,wy,wz,hitmesh,hitFace = getPosition(nextX,nextY)

                        if wx != []:
                            mc.setAttr((betweenList[a] + '.translateX'), wx)
                            mc.setAttr((betweenList[a] + '.translateY'), wy)
                            mc.setAttr((betweenList[a] + '.translateZ'), wz)
                            hitFaceName = (hitmesh + '.f[' + str(hitFace) +']')
                            rx, ry, rz = getFaceAngle(hitFaceName) 
                            mc.setAttr((betweenList[a] + '.rotateX'), rx)
                            mc.setAttr((betweenList[a] + '.rotateY'), ry)
                            mc.setAttr((betweenList[a] + '.rotateZ'), rz)
                 
        
        
        mc.select(selSample[0])
        updateDepth()
        updateScale()
        mc.refresh(cv=True,f=True)

# Name of dragger context

def runIt():
    global ctx
    ctx = 'Click2dTo3dCtx'
    # Delete dragger context if it already exists
    if mc.draggerContext(ctx, exists=True):
        mc.deleteUI(ctx)
    # Create dragger context and set it to the active tool
    mc.draggerContext(ctx, pressCommand = onPressPlace, rc = offPressPlace, dragCommand = onDragPlace, fnz = finishTool, name=ctx, cursor='crossHair',undoMode='step')
    mc.setToolTo(ctx)
    

def goPress(sampleMesh):
    global sampleFileChoice
    if len(sampleFileChoice)>0:
        for s in sampleFileChoice:
            if mc.objExists(str(s)):
                checkStateX = mc.getAttr(s+'.translateX')
                checkStateY = mc.getAttr(s+'.translateY')
                checkStateZ = mc.getAttr(s+'.translateZ')
                if checkStateX == 0 and  checkStateY == 0 and checkStateZ == 0:
                    mc.delete(s)

    global pressFirstTime
    global betweenFirstTime
    global screenX,screenY
    global betweenList
    global betweenListShape
    global checkVisList
    global selectionPool
    global combineSelPool

    screenX = 0
    screenY = 0
    betweenList = []
    betweenListShape = []
    betweenFirstTime = 1
    pressFirstTime = 1
    selectionPool = []
    combineSelPool = []
    checkVisList = screenVisPoly()
    
    iconLightOff()
    sampleName = (sampleMesh.split('/')[-1]).split('.')[0]
    mc.CreateEmptyGroup()
    mc.rename(sampleName + '_offset')
    checkName=mc.ls(sl=True)
    meshTypeState = mc.radioButtonGrp('meshImportType', q=True , sl=True)
    if meshTypeState == 3:#gpu
        cacheName = sampleName
        cachePath = sampleMesh
        cacheNode = mc.createNode('gpuCache',name = cacheName+'Cache')
        mc.setAttr(cacheNode+'.cacheFileName',cachePath,type='string')
        mc.parent(cacheNode,checkName)    
    else:
        command = 'AbcImport -mode import -reparent '+ checkName[0] + ' ' + '"' + sampleMesh + '"' 
        newNode = mel.eval(command)
        mc.xform(ws=1, a=1 ,piv =[0, 0, 0]) 
        mc.pickWalk(d="down")
    
    tempSel = mc.ls(sl=True,type='transform')

    mc.select(tempSel[0])
    
    sampleFileChoice = checkName
    #heightLight Icon

    iconNameCheck = sampleMesh.split('/')[-1].replace('.abc','_png')
    subFolder = sampleMesh.split('/')[-2]
    preIcon = iconNameCheck + '_column|'+subFolder+'_'+ iconNameCheck+'_button'
    cmd = 'mc.symbolButton("'+preIcon+'", e=1, ebg =1, bgc=[0, 0.4, 0.5]) '
    mc.evalDeferred(cmd)
    runIt()
    hideSelVis()


def avgVertexNormalAngle(vertexName):
    shapeNode = mc.listRelatives(vertexName, fullPath=True , parent=True )
    transformNode = mc.listRelatives(shapeNode[0], fullPath=True , parent=True )
    faceList = (mc.polyInfo(vertexName , vf=True )[0]).split(':')[-1].split('    ')
    faceList = [x for x in faceList if x.strip()]
    getMeAngle=[]
    sumX = 0
    sumY = 0
    sumZ = 0
    for f in faceList:
        checkNumber = ''.join([n for n in f.split('|')[-1] if n.isdigit()]) 
        if len(checkNumber) > 0:
            rx, ry, rz = getFaceAngle((transformNode[0] + '.f[' + str(checkNumber) +']'))
            sumX = sumX + rx
            sumY = sumY + ry
            sumZ = sumZ + rz
    avgX =  sumX /len(faceList)
    avgY =  sumY /len(faceList)
    avgZ =  sumZ /len(faceList)
    return avgX, avgY, avgZ
        
def getFaceAngle(faceName):
    shapeNode = mc.listRelatives(faceName, fullPath=True , parent=True )
    transformNode = mc.listRelatives(shapeNode[0], fullPath=True , parent=True )
    obj_matrix = Matrix(mc.xform(transformNode, query=True, worldSpace=True, matrix=True))
    face_normals_text = mc.polyInfo(faceName, faceNormals=True)[0]
    face_normals = [float(digit) for digit in re.findall(r'-?\d*\.\d*', face_normals_text)]
    v = Vector(face_normals) * obj_matrix
    if max(abs(v[0]), abs(v[1]), abs(v[2])) == -v[1]:
        pass
        #print face, v #if reverse, need to rotate another 180 degree
    upvector = oma.MVector (0,1,0)
    getHitNormal = v
    quat = oma.MQuaternion(upvector, getHitNormal)
    quatAsEuler = oma.MEulerRotation()
    quatAsEuler = quat.asEulerRotation()
    rx, ry, rz = math.degrees(quatAsEuler.x), math.degrees(quatAsEuler.y), math.degrees(quatAsEuler.z)
    return rx, ry, rz

def jwMeshResetRot():
    mc.floatSliderGrp('meshRotSlide' ,e =1, v = 0)
    global SycList
    if len(SycList)>0:
        for s in SycList:
            if mc.objExists(s):
                mc.setAttr((s+'.rotateY'),0)

def jwMeshResetScale():
    mc.floatSliderGrp('meshScaleSlide' ,e =1, v = 1)
    global SycList
    if len(SycList)>0:
        for s in SycList:
            if mc.objExists(s):
                mc.setAttr((s+'.scaleX'),1)
                mc.setAttr((s+'.scaleY'),1)
                mc.setAttr((s+'.scaleZ'),1)

def jwMeshResetDepth():
    mc.floatSliderGrp('meshDepthSlide' ,e =1, v = 0)
    global SycList
    if len(SycList)>0:
        for s in SycList:
            if mc.objExists(s):
                mc.setAttr((s+'.translateY'),0)

def jwMeshResetBetween():
    mc.floatSliderGrp('meshBetweenSlide' ,e =1, v = 0)

def jwMeshResetSnapV():
    mc.floatSliderGrp('snapVSlider' ,e =1, v = 0)

def jwMeshResetRandomRot():
    mc.floatSliderGrp('randomRotSlide' ,e =1, v = 0)
    global SycList
    if len(SycList)>0:
        for s in SycList:
            if mc.objExists(s):
                mc.setAttr((s+'.rotateY'),0)
    

def jwMeshResetRandomScale():
    mc.floatSliderGrp('randomScaleSlide' ,e =1, v = 0)
    updateRandomScale()
    

def jwMeshResetBetweenRandom():
    mc.floatSliderGrp('meshBetweenRandomSlide' ,e =1, v = 0)
    updateBetweenRandom()

def jwfloatResizeIcon():
    global meshDirectory
    checkDir = os.path.isdir(meshDirectory)    
    if checkDir == True :
        subFolder = mc.getFileList(folder = meshDirectory)
        mc.deleteUI('lib')
        mc.setParent('contCM')
        mc.scrollLayout('lib', h= 506)
        for s in subFolder:
            checkSubDir = os.path.isdir(meshDirectory+'/'+s)   
            if checkSubDir == True:
                iconsCollection = []
                iconPath = []
                rowNumber = mc.intSliderGrp('iconSize' ,q=1, v=1 )
                wide =  (420.0 /rowNumber)
                high = (wide*1.3)
                mc.frameLayout('s + FL', label= s ,cll = True,cc ='iconLightOff()')
                mc.gridLayout('libIcons', numberOfColumns = rowNumber, cellWidthHeight = [wide, high])
                iconsCollection = mc.getFileList(folder = (meshDirectory+'/'+s) , filespec = '*.png')
                for i in iconsCollection:
                    iconPath = meshDirectory + '/'+ s + '/' + i;
                    mc.columnLayout((i + '_column'), h = wide)
                    samplePath = iconPath.replace('png','abc')
                    runCmd = 'goPress("' + samplePath + '")'
                    mc.symbolButton((s +'_' + i + '_button'),  w = wide, h = wide, image = iconPath, c = runCmd)
                    mc.text(w = wide, al = 'center', l = i.replace('.png',''))
                    mc.setParent( '..' )
                mc.setParent( '..' )
                mc.setParent( '..' )
            else:
                pass  
    else:
        print 'Directory does not exist!!!'

def iconLightOff():
    getList = collectFullIconList()
    for g in getList:
        try:    
            mc.symbolButton(g , e = True, ebg = 0, bgc=[0, 0.4, 0.5])
        except:
            pass

def collectFullIconList():
    global meshDirectory;
    fullIconList = []
    checkDir = os.path.isdir(meshDirectory)    
    if checkDir == True :
        subFolder = mc.getFileList(folder = meshDirectory)
        for s in subFolder:
            checkSubDir = os.path.isdir(meshDirectory+'/'+s)   
            if checkSubDir == True:
                iconsCollection = []
                iconPath = []
                iconsCollection = mc.getFileList(folder = (meshDirectory+'/'+s) , filespec = '*.png')
                for i in iconsCollection:
                    iconPath = meshDirectory + '/'+ s + '/' + i;
                    iconNameCheck = iconPath.split('/')[-1].replace('.','_')
                    subFolder = iconPath.split('/')[-2]
                    preIcon = iconNameCheck + '_column|'+subFolder+'_'+ iconNameCheck+'_button'
                    fullIconList.append(preIcon)
    return fullIconList

def whatIsOn():
    global meshDirectory;
    getList = collectFullIconList()
    iconOnList = []
    
    for g in getList:
        iconState = mc.symbolButton(g, q=True, bgc=True)
        if iconState[1]>0:
            #get file path
            subFolder = g.split('|')[-1].split('_')[0]
            asset = g.split('|'+subFolder + '_')[-1].replace('_png_button','.abc')
            path = meshDirectory + subFolder +'/' + asset
            iconOnList.append(path)
    return iconOnList


    


jwMeshPlaceUI() 
jwfloatResizeIcon()   
