##--------------------------------------------------------------------------
##
## ScriptName : rapidPlace
## Contents   : click to place screws from Libaray
## Author     : Joe Wu
## URL        : http://im3djoe.com
## LastUpdate : 2020/12/02
##			  : create one bezier curve for selected edge loop, smooth edge loop with 2~5 control point and dropoff slider
## Version    : 1.0  First version for public test
## Other Note : test in maya 2020.2 windows
##
## Install    : copy and paste script into a python tab in maya script editor
##--------------------------------------------------------------------------

import maya.cmds as mc
import maya.mel as mel
import math

def arcDeformerUI():
    if mc.window("arcDeformerUI", exists = True):
        mc.deleteUI("arcDeformerUI")
    arcDeformerUI = mc.window("arcDeformerUI",title = "arcDeformer", w=320)
    mc.frameLayout(labelVisible= False)
    mc.text(l ='')
    mc.intSliderGrp('CPSlider', cw3=[80, 30, 180], label = 'Control Point ',  field= 1, min= 2, max= 5, v = 3 )
    mc.floatSliderGrp('dropOffSlider' , label = 'DropOff', v = 1, cw3=[80, 30, 180], field= 1, min= 0.01, max= 10)
    mc.rowColumnLayout(nc=6 ,cw=[(1,20),(2,80),(3,20),(4,75),(5,10),(6,75)])
    mc.text(l ='')
    mc.checkBox('evenSpace', label= "even Space" ,v = 1)
    mc.text(l ='')
    mc.button( l= 'Run',  c= 'arcEdgeLoop()')
    mc.text(l ='')
    mc.button( l= 'Done',  c= 'arcDone()')
    mc.text(l ='')
    mc.setParent( '..' )
    mc.showWindow(arcDeformerUI)


def arcDone():
    global storeEdge
    if mc.objExists('arcCurve'):
        hist = mc.listConnections(mc.listConnections('arcCurveShape',sh=1, d=1 ) ,d=1 ,sh=1)
        mc.delete(hist,ch=1)
        mc.delete('arcCurve*')
    mc.select(storeEdge)
    
def arcEdgeLoop():
    global storeEdge
    selEdge = mc.filterExpand(expand=True ,sm=32)
    storeEdge = selEdge
    if selEdge:
        if mc.objExists('arcCurve'):
            arcDone()
        selMeshForDeformer = mc.ls(sl=1,o=1)
        listVtx = vtxLoopOrder()
        midP = int(len(listVtx)/2)
        mc.move(0.01, 0, 0,selEdge[midP],r=1, cs=1 ,ls=1, wd =1)
        p1 = mc.pointPosition(listVtx[0], w =1)
        p2 = mc.pointPosition(listVtx[midP], w =1)
        p3 = mc.pointPosition(listVtx[-1], w =1)
        newNode = mc.createNode('makeThreePointCircularArc')
        mc.setAttr((newNode + '.pt1'), p1[0],  p1[1] , p1[2])
        mc.setAttr((newNode + '.pt2'), p2[0],  p2[1] , p2[2])
        mc.setAttr((newNode + '.pt3'), p3[0],  p3[1] , p3[2])
        mc.setAttr((newNode + '.d'), 3)
        mc.setAttr((newNode + '.s'), len(listVtx))
        newCurve = mc.createNode('nurbsCurve')
        mc.connectAttr((newNode+'.oc'), (newCurve+'.cr'))
        mc.delete(ch=1)
        transformNode = mc.listRelatives(newCurve, fullPath=True , parent=True )
        if mc.objExists('arcCurve'):
            mc.delete('arcCurve')
        mc.rename(transformNode,'arcCurve')
        uLength =  len(listVtx) 
        totalEdgeLoopLength = 0;
        sum = 0
        Llist = []
        uList = []
        pList = []
        for i in range(len(selEdge)):
            pA = mc.pointPosition(listVtx[i], w =1)
            pB = mc.pointPosition(listVtx[i+1], w =1)
            checkDistance = math.sqrt( ((pA[0] - pB[0])**2)  + ((pA[1] - pB[1])**2)  + ((pA[2] - pB[2])**2) )
            Llist.append(checkDistance)
            totalEdgeLoopLength = totalEdgeLoopLength + checkDistance
        
        goEven = mc.checkBox('evenSpace', q=1 ,v = 1)
        if goEven == 1:
            avg = totalEdgeLoopLength / (len(selEdge))
            for j in range(len(selEdge)-1):
                sum = ((j+1)*avg)
                uList.append(sum) 
        else:
            for j in Llist: 
                sum = sum + j 
                uList.append(sum) 
        for k in uList:
            p = k / totalEdgeLoopLength *uLength
            pList.append(p)
            
        for q in range(len(pList)):
            pp = mc.pointOnCurve("arcCurve" , pr = pList[q], p=1)
            mc.move( pp[0], pp[1], pp[2],listVtx[q+1] , a =True, ws=True)
        mc.delete('arcCurve')
        controlers = 3
        mc.select(selEdge)
        mc.polyToCurve(form=0, degree=3)
        conP = mc.intSliderGrp('CPSlider',q=1 , v = True )
        mc.rebuildCurve(ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s= (conP -1), d=3, tol=0.01)
        mc.nurbsCurveToBezier()
        controlCurve = mc.ls(sl=1)
        mc.delete(ch=1)
        mc.rename("arcCurve")
        deformerNames  = mc.wire( selMeshForDeformer, gw=0, en = 1, ce = 0, li= 0, dds = [(0,1)], dt=1, w = "arcCurve")
        mc.CreateBezierCurveTool()
        mc.setToolTo('moveSuperContext')
        degree = mc.getAttr('arcCurve.degree')
        spans = mc.getAttr('arcCurve.spans')
        numberCVs = degree + spans
        collect = []
        for x in range(int(numberCVs/3)-1):
            g = 'arcCurve.cv[' + str((x+1)*3) + ']'
            collect.append(g)
        mc.select(collect ,r=1)
        cmd = 'doMenuNURBComponentSelection("arcCurve", "controlVertex");'
        mel.eval(cmd)
        mc.connectControl("dropOffSlider", (deformerNames[0]+".dropoffDistance[0]"))

def vtxLoopOrder():
    selEdges = mc.ls(sl=1,fl=1)
    shapeNode = mc.listRelatives(selEdges[0], fullPath=True , parent=True )
    transformNode = mc.listRelatives(shapeNode[0], fullPath=True , parent=True )
    edgeNumberList = []
    for a in selEdges:
        checkNumber = ((a.split('.')[1]).split('\n')[0]).split(' ')
        for c in checkNumber:
            findNumber = ''.join([n for n in c.split('|')[-1] if n.isdigit()])
            if findNumber:
                edgeNumberList.append(findNumber)
    getNumber = []
    for s in selEdges:
        evlist = mc.polyInfo(s,ev=True)
        checkNumber = ((evlist[0].split(':')[1]).split('\n')[0]).split(' ')
        for c in checkNumber:
            findNumber = ''.join([n for n in c.split('|')[-1] if n.isdigit()])
            if findNumber:
                getNumber.append(findNumber)
    dup = set([x for x in getNumber if getNumber.count(x) > 1])
    getHeadTail = list(set(getNumber) - dup)
    vftOrder = []
    vftOrder.append(getHeadTail[0])
    count = 0
    while len(dup)> 0 and count < 100:
        checkVtx = transformNode[0]+'.vtx['+ vftOrder[-1] + ']'
        velist = mc.polyInfo(checkVtx,ve=True)
        getNumber = []
        checkNumber = ((velist[0].split(':')[1]).split('\n')[0]).split(' ')
        for c in checkNumber:
            findNumber = ''.join([n for n in c.split('|')[-1] if n.isdigit()])
            if findNumber:
                getNumber.append(findNumber)
        findNextEdge = []
        for g in getNumber:
            if g in edgeNumberList:
                findNextEdge = g
        edgeNumberList.remove(findNextEdge)
        checkVtx = transformNode[0]+'.e['+ findNextEdge + ']'
        findVtx = mc.polyInfo(checkVtx,ev=True)
        getNumber = []
        checkNumber = ((findVtx[0].split(':')[1]).split('\n')[0]).split(' ')
        for c in checkNumber:
            findNumber = ''.join([n for n in c.split('|')[-1] if n.isdigit()])
            if findNumber:
                getNumber.append(findNumber)
        gotNextVtx = []
        for g in getNumber:
            if g in dup:
                gotNextVtx = g
        dup.remove(gotNextVtx)
        vftOrder.append(gotNextVtx)
        count +=  1
    vftOrder.append(getHeadTail[1])
    finalList = []
    for v in vftOrder:
        finalList.append(transformNode[0]+'.vtx['+ v + ']' )
    return finalList
arcDeformerUI()