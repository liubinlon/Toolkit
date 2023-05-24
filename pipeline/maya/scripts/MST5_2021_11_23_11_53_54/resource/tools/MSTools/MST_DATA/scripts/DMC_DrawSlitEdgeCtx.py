# -*- coding: utf-8 -*-
"""
import DMC_DrawSlitEdgeCtx as DSlECtx
DSlECtx.DrawSlitEdgeCtx()
"""
#mayaモジュールのインポート
import maya.mel as mel
import maya.cmds as cmds
import maya.OpenMaya as om
import maya.api.OpenMaya as om2
import maya.api.OpenMayaUI as om2UI
import math


def DrawSlitEdgeCtx():
    if not cmds.contextInfo('DrawSlitEdgeCtx',ex=True):cmds.draggerContext('DrawSlitEdgeCtx',e=False,n='DrawSlitEdgeCtx Tool',i1='pencil.xpm',cursor='default',um='sequence')
    cmds.draggerContext('DrawSlitEdgeCtx',e=True,pressCommand='DSlECtx.DSlE_A()',dragCommand='DSlECtx.DSlE_B()',releaseCommand='DSlECtx.DSlE_C()')
    cmds.draggerContext('DrawSlitEdgeCtx',e=True,helpString=u'SlitCut,Ctrl:not snap,Ctrl+Shift:Snap to Edge,Alt:Snap to Last orner,Shift:Add loop edge')
    cmds.setToolTo('DrawSlitEdgeCtx')
    
def DSlE_A():
    global df_MeshFn
    df_MeshFn=[]
    df_MeshFn[0:0]=[None]
    df_MeshFn[1:1]=[None]
    df_MeshFn[2:2]=[None]
    df_MeshFn[3:3]=[None]

    sel=om2.MGlobal.getActiveSelectionList()
    hl=om.MSelectionList()
    om.MGlobal.getHiliteList(hl)
    sA=[]
    hl.getSelectionStrings(sA)
    for I in sA:sel.add(I)

    for i in range(sel.length()):
        try:dagPath=sel.getDagPath(i)
        except:continue
        if dagPath.hasFn(om2.MFn.kMesh):
            df_MeshFn[3]=cmds.ls(live=1)
            MeshFn=om2.MFnMesh(dagPath)
            df_MeshFn[0]=[MeshFn,MeshFn.autoUniformGridParams()]
            df_MeshFn[2]=MeshFn.fullPathName()
            cmds.select(df_MeshFn[2])
            df_MeshFn[1]=PPinView(df_MeshFn[2])
            cmds.makeLive(df_MeshFn[1])
            cmds.curve(d=1,ws=1,p=om2.MVector(cmds.autoPlace(um=1)))
            cmds.setAttr(".dispCV", 0)
            om.MGlobal.executeCommand('hilite %s' %df_MeshFn[2])
            break

def DSlE_B():
    CV=cmds.filterExpand(sm=9,fp=1)
    if CV:
        wpv=om2.MVector(cmds.autoPlace(um=1))
        curveFn = om2.MFnNurbsCurve(om2.MGlobal.getSelectionListByName(CV[0]).getDagPath(0))
        num=curveFn.numCVs
        if num==1:cmds.curve(CV[0],a=1,ws=1,p=wpv)
        else:
            cvStep=cmds.optionVar(q='df_cvStep')
            wpvh=wpv-om2.MVector(curveFn.cvPosition(num-2,4))
            if wpvh.length()<cvStep:cmds.xform('%s.cv[%s]' %(CV[0],num-1),t=wpv,a=1,ws=1)
            else:cmds.curve(CV[0],a=1,ws=1,p=wpv)
        cmds.refresh(f=1)

def DSlE_C():
    global df_MeshFn
    try:
        sel = om2.MSelectionList()
        for I in cmds.filterExpand(sm=9,fp=1):sel.add(I)
        DagPath=sel.getDagPath(0)
        curveFn0=om2.MFnNurbsCurve(DagPath)
        numCVs=curveFn0.numCVs
        if numCVs==1:cmds.delete(om2.MFnDagNode(curveFn0.parent(0)).fullPathName())
        else:
            CameraFn=om2.MFnCamera(om2UI.M3dView().active3dView().getCamera())
            Ortho=CameraFn.isOrtho()
            vDV=CameraFn.viewDirection(4)
            WP=curveFn0.cvPositions(4)
            curveFn0N=curveFn0.fullPathName()
            DCV=[]
            Pcv=[]
            Ecv=[]
            if Ortho:
                for i in xrange(numCVs):
                    RP=df_MeshFn[0][0].closestIntersection(om2.MFloatPoint(WP[i]),om2.MFloatVector(vDV),4,10000,False,accelParams=df_MeshFn[0][1],tolerance=0.001)
                    if RP[2]>-1:
                        WP[i]=RP[0]
                        Pcv+=[i]
                    else:Ecv+=[i]
                for i in Ecv:
                    if i+1 in Pcv :WP[i]=WP[i+1]+(WP[i+1]-WP[i+2])
                    elif i-1 in Pcv :WP[i]=WP[i-1]+(WP[i-1]-WP[i-2])
                    else:DCV+=['%s.cv[%s]' %(curveFn0N,i)]
            else:
                camP=CameraFn.eyePoint(4)
                for i in xrange(numCVs):
                    RP=df_MeshFn[0][0].closestIntersection(om2.MFloatPoint(camP),om2.MFloatVector(WP[i]-camP),4,10000,False,accelParams=df_MeshFn[0][1],tolerance=0.001)
                    if RP[2]>-1:
                        WP[i]=RP[0]
                        Pcv+=[i]
                    else:Ecv+=[i]
                for i in Ecv:
                    if i+1 in Pcv :WP[i]=WP[i+1]+(WP[i+1]-WP[i+2])
                    elif i-1 in Pcv :WP[i]=WP[i-1]+(WP[i-1]-WP[i-2])
                    else:DCV+=['%s.cv[%s]' %(curveFn0N,i)]
            curveFn0.setCVPositions(WP,4)
            curveFn0.updateCurve()
            if DCV:cmds.delete(DCV)
            DCV=[]
            curveFn0=om2.MFnNurbsCurve(DagPath)
            WP=curveFn0.cvPositions(4)
            numCVs=curveFn0.numCVs
            si=-1
            for i in xrange(1,numCVs-1):
                RP=df_MeshFn[0][0].closestIntersection(om2.MFloatPoint(WP[i]),om2.MFloatVector(vDV),4,0.001,True,accelParams=df_MeshFn[0][1],tolerance=0.001)
                if RP[2]==-1:
                    if si!=i-1:
                        DCV+=['%s.cv[%s]' %(curveFn0N,i)]
                        si=i
            if DCV:
                selcp = om2.MSelectionList()
                for I in DCV:selcp.add(I)
                dagPath,mCmp = selcp.getComponent(0)
                curveFn = om2.MFnNurbsCurve(dagPath)
                curveN=curveFn.fullPathName()
                cvid = om2.MFnSingleIndexedComponent(mCmp).getElements()
                knots=curveFn.knots()
                dcp=['%s.u[%s]' %(curveN,knots[J])for J in cvid]
                dcs =cmds.detachCurve(dcp,ch=False,cos=True,rpo=True)
                selCV = om2.MSelectionList()
                for I in dcs:selCV.add(I)
                for j in range(selCV.length()):
                    try:dagPath = selCV.getDagPath(j)
                    except:continue
                    curveFn = om2.MFnNurbsCurve(dagPath)
                    curveFn.updateCurve()
                cmds.dgdirty(selCV.getSelectionStrings(),a=1)
                om2.MGlobal.setActiveSelectionList(selCV)
                cmds.hilite(df_MeshFn[2])
    except:pass
    if df_MeshFn[1]:cmds.delete(df_MeshFn[1])
    if df_MeshFn[3]:cmds.makeLive(df_MeshFn[3])
    if df_MeshFn[2]:cmds.hilite(df_MeshFn[2])
    mod=cmds.getModifiers()
    if mod==5:Split_by_CV(mod=0,snapP=5)
    elif mod==4:Split_by_CV(mod=0,snapP=4)
    else:Split_by_CV(mod=mod,snapP=0)
    del df_MeshFn

def PPinView(MeshN):
    sel=om2.MGlobal.getActiveSelectionList()
    hl=om.MSelectionList()
    om.MGlobal.getHiliteList(hl)
    
    useDepth=cmds.selectPref(q=1,useDepth=1)
    if not useDepth:om.MGlobal.executeCommand('selectPref -useDepth 1')
    sM =om2.MGlobal.selectionMode()

    om2.MGlobal.setActiveSelectionList(om2.MSelectionList())
    om.MGlobal.executeCommand('hilite %s' %MeshN)

    om2.MGlobal.setSelectionMode(om2.MGlobal.kSelectComponentMode)
    om.MGlobal.executeCommand('selectType -facet true')
    viewPort = om2UI.M3dView.active3dView()
    om.MGlobal.selectFromScreen(0,0,viewPort.portWidth(),viewPort.portHeight(),om.MGlobal.kReplaceList,om.MGlobal.kSurfaceSelectMethod)
    BB=cmds.polyEvaluate(bc=1)
    om2.MGlobal.setActiveSelectionList(sel)
    om.MGlobal.setHiliteList(hl)
    om2.MGlobal.setSelectionMode(sM)
    if not useDepth:om.MGlobal.executeCommand('selectPref -useDepth 0')
    D=om2.MVector([BB[0][1]-BB[0][0],BB[1][1]-BB[1][0],BB[2][1]-BB[2][0]]).length()*20
    if D>0:
        BB=om2.MBoundingBox(om2.MPoint(BB[0][0],BB[1][0],BB[2][0]),om2.MPoint(BB[0][1],BB[1][1],BB[2][1]))
        CameraFn=om2.MFnCamera(om2UI.M3dView().active3dView().getCamera())
        CMatrix=CameraFn.getPath().inclusiveMatrixInverse()
        BB.transformUsing(CMatrix)
        camP=CameraFn.eyePoint(4)
        camV=CameraFn.viewDirection(4)
        PP=camP+camV*BB.max[2]*-1
        TR=cmds.createNode('transform',ss=1)
        om.MGlobal.executeCommand('setAttr %s.v %s' %(TR,0))
        om.MGlobal.executeCommand('setAttr %s.t %s %s %s' %(TR,PP[0],PP[1],PP[2]))
        om.MGlobal.executeCommand('setAttr %s.s %s %s %s' %(TR,D,D,D))
        mesh=cmds.createNode('mesh',ss=1,p=TR)
        pPlane=cmds.createNode('polyPlane',ss=1)
        om.MGlobal.executeCommand('setAttr %s.axis %s %s %s' %(pPlane,camV[0],camV[1],camV[2]))
        om.MGlobal.executeCommand('setAttr %s.subdivisionsWidth %s' %(pPlane,2))
        om.MGlobal.executeCommand('setAttr %s.subdivisionsHeight %s' %(pPlane,2))
        cmds.connectAttr('%s.output' %pPlane, '%s.inMesh' %mesh, f=1)
        cmds.optionVar(floatValue=('df_cvStep', D/10000))
    else:TR=None
    return TR

def Split_by_CV(tol=0.001,mod=0,snapP=0):
    hl=om.MSelectionList()
    om.MGlobal.getHiliteList(hl)
    sA=[]
    hl.getSelectionStrings(sA)
    hl2=om2.MSelectionList()
    for I in sA:hl2.add(I)
    dagPathM=None
    for i in range(hl2.length()):
        try:dagPathM = hl2.getDagPath(i)
        except:continue
        if dagPathM.hasFn(om2.MFn.kMesh):break
    hl=sA[0]
    if dagPathM:
        TransformN = om2.MFnTransform(om2.MFnMesh(dagPathM).parent(0)).fullPathName()
        selCV=om2.MGlobal.getActiveSelectionList()
        dCVs=[]
        for j in range(selCV.length()):
            try:dagPath = selCV.getDagPath(j)
            except:continue
            if dagPath.hasFn(om2.MFn.kNurbsCurve):
                dCVs+=[cmds.parent(om2.MFnTransform(dagPath.transform()).fullPathName(),TransformN,r=0)[0]]
        cmds.dgdirty(dCVs,a=1)
        cmds.makeIdentity(dCVs,n=0, s=1, r=1, t=1, apply=True, pn=0)
        cmds.dgdirty(dCVs,a=1)
        cmds.parent(dCVs,w=1)
        om.MGlobal.executeCommand('hilite %s' %hl)
        selCV = om2.MSelectionList()
        for I in dCVs:selCV.add(I)
        for j in range(selCV.length()):
            dagPath = selCV.getDagPath(j)
            curveFn = om2.MFnNurbsCurve(dagPath)
            try:ln=curveFn.numCVs
            except:
                cmds.delete(om2.MFnDagNode(dagPath.transform()).fullPathName())
                continue
            MeshFn = om2.MFnMesh(dagPathM)
            MeshFn.updateSurface()
            ItrP=om2.MItMeshPolygon(dagPathM)
            ItrE=om2.MItMeshEdge(dagPathM)
            VnumO= MeshFn.numVertices
            MLP=MeshFn.getPoints()
            intersector=om2.MMeshIntersector()
            intersector.create(MeshFn.object())

            WP=curveFn.cvPositions()
            WP[0]+=(WP[1]-WP[0])*0.75
            WP[-1]+=(WP[-2]-WP[-1])*0.75
            curveFn.setCVPositions(WP)
            curveFn.updateCurve()
            try:
                curveFn = om2.MFnNurbsCurve(dagPath)
                params=om2.MDoubleArray()
                for i in xrange(ln):params+=[i]
                curveFn.setKnots(params, 0, ln-1)
                u=1.0*tol*(ln-1)
                Us=[]
                FID=intersector.getClosestPoint(curveFn.getPointAtParam(0)).face
                for i in xrange(int(1/tol)):
                    ui=u*i
                    CP=om2.MPoint(intersector.getClosestPoint(curveFn.getPointAtParam(ui)).point)
                    if CP[1]!=FID:
                        FID=CP[1]
                        Us+=[ui]
                FUs=[float(i) for i in xrange(ln)]
                FUs=list(set(FUs+Us))
                FUs.sort()
                FID=-1
                ip=[]
                addID=[]
                rateS=-1
                CVD=WP[int(ln/20)+1]-WP[0]
                for I in FUs:
                    MPOM=intersector.getClosestPoint(curveFn.getPointAtParam(I))
                    CP=[om2.MPoint(MPOM.point),MPOM.face]
                    if CP[1]!=FID or I==ln-1:
                        FID=CP[1]
                        ItrP.setIndex(CP[1])
                        EDs=ItrP.getEdges()
                        magS=[]
                        for II in EDs:
                            ItrE.setIndex(II)
                            id0=ItrE.vertexId(0)
                            id1=ItrE.vertexId(1)
                            AB=(MLP[id1]-MLP[id0]).normal()
                            magS+=[((CP[0]-MLP[id0])^AB).length()]
                        if min(magS)>0.1:continue
                        minID=EDs[magS.index(min(magS))]
                        ItrE.setIndex(minID)
                        id0=ItrE.vertexId(0)
                        id1=ItrE.vertexId(1)
                        AB=(MLP[id1]-MLP[id0])
                        rate=(CP[0]-MLP[id0])*AB.normal()/AB.length()
                        if snapP==5:
                            if rate>0.5:rate=1.0
                            else:rate=0
                        elif snapP==4:
                            if rate>0.98:rate=1.0
                            elif rate<0.02:rate=0
                        elif rateS<0 :
                            if rate>0.85:rate=1.0
                            elif rate<0.15:rate=0
                            rateS=1
                        else:
                            if rate>0.98:rate=1.0
                            elif rate<0.02:rate=0
                        if CVD:
                            if rate==1 or rate==0:pass
                            elif not ItrE.onBoundary():
                                angle =abs(math.degrees(CVD.angle(MLP[id0]-MLP[id1]))-90)
                                if angle>40:continue
                            CVD=None
                        ip+=[(minID, rate)]
                        if rate==1:addID+=[id1]
                        elif rate==0:addID+=[id0]
                if ip[0][0]==ip[1][0]:
                    if len(ip[0])==len(ip[1]):ip.pop(0)
                if ip[-1][0]==ip[-2][0]:
                    if len(ip[-1])==len(ip[-2]):ip.pop(-1)
                if ip[0][0]==ip[-1][0]:
                    if abs(ip[0][1]-ip[-1][1])<0.3:ip[-1]=ip[0]
                if snapP!=4:
                    if ip[-1][1]>0.9:ip[-1]=(ip[-1][0],1.0)
                    elif ip[-1][1]<0.1:ip[-1]=(ip[-1][0],0)
                if mod==1:cmds.polySplit(TransformN, ip=ip,ief=1,sma=180)
                else:cmds.polySplit(TransformN, ip=ip,sma=0)
                VnumA= cmds.polyEvaluate(TransformN,v=1)
                cmds.select(cmds.polyListComponentConversion('%s.vtx[%s:%s]' %(TransformN,VnumO,VnumA),['%s.vtx[%s]' %(TransformN,I) for I in addID],te=1,internal=1),add=1)
                EndVtxS()
                EndVtxS()
                LP=curveFn.cvPosition(ln-1,4)
                cmds.dgdirty(TransformN,a=1)
            except:
                cmds.delete(dCVs[j])
                continue
            cmds.delete(dCVs[j])
            selE = om2.MSelectionList()
            for I in cmds.filterExpand(ex=1,sm=32,fp=1) or []:selE.add(I)
            sel = om2.MSelectionList()
            for I in cmds.polyListComponentConversion(tv=1):sel.add(I)
            for i in range(sel.length()):
                dagPath,mCmp = sel.getComponent(0)
                MeshFn = om2.MFnMesh(dagPath)
                MeshN=MeshFn.fullPathName()
                WP=MeshFn.getPoints(4)
                Vid =om2.MFnSingleIndexedComponent(mCmp).getElements()
                dis=[LP.distanceTo(WP[I]) for I in Vid]
                LviD=Vid[dis.index(min(dis))]
                iterV= om2.MItMeshVertex(dagPath)
                iterV.setIndex(LviD)
                if not iterV.onBoundary():
                    om.MGlobal.executeCommand('select %s.vtx[%s]' %(MeshN,LviD))
                    try:
                        Eids=VTXnPolyEdge()
                        if Eids:
                            nPolySplitEdge(ief=1,CT=False,sma=180)
                            om2.MGlobal.setActiveSelectionList(selE)
                            cmds.select(['%s.e[%s]' %(TransformN,I) for I in Eids],add=1)
                        else:
                            nPolySplitEdge(ief=1,CT=False,sma=180)
                            om2.MGlobal.setActiveSelectionList(selE)
                            VnumA2= cmds.polyEvaluate(TransformN,v=1)
                            cmds.select(cmds.polyListComponentConversion('%s.vtx[%s:%s]' %(TransformN,VnumA,VnumA2),'%s.vtx[%s]' %(TransformN,LviD),te=1,internal=1),add=1)
                    except:om2.MGlobal.setActiveSelectionList(selE)
            if mod==1:
                try:nPolySplitEdge(ief=1,CT=False,sma=180)
                except:pass
            else:
                slitEdgeB()

def EndVtxS():
    selRTS=om2.MSelectionList()
    sel=om2.MGlobal.getActiveSelectionList()
    seled=om2.MSelectionList()
    for I in cmds.filterExpand(sm=32,ex=0) or[]:seled.add(I)
    for i in xrange(seled.length()):
        dagPath,mCmp=seled.getComponent(i)
        AEid =set(om2.MFnSingleIndexedComponent(mCmp).getElements())
        MeshFn=om2.MFnMesh(dagPath)
        MeshN=MeshFn.fullPathName()
        Eiter=om2.MItMeshEdge(dagPath)
        edgeListS=[]
        AEn=len(AEid)
        edgID=[]
        for j in xrange(AEn):
            Eid = [list(AEid)[0]]
            for jj in xrange(AEn):
                EE=False
                for I in Eid:
                    Eiter.setIndex(I)
                    if I in edgID:
                        AE=(AEid & set(list(Eiter.getConnectedEdges())))
                        AE=(AE-set(edgID))
                        if len((AE))==0 :
                            AE=(AEid & set(list(Eiter.getConnectedEdges())))
                            AE=(AE & set(edgID))
                            AEL=list(AE)
                            VidI=set(list(MeshFn.getEdgeVertices(I)))
                            AE=set()
                            for J in AEL:
                                VidJ=set(list(MeshFn.getEdgeVertices(J)))
                                VidJ=list(VidI & VidJ)[0]
                                selvtxJ=om2.MSelectionList()
                                selvtxJ.add('%s.vtx[%s]' %(MeshN,VidJ))
                                if selvtxJ.intersect(selvtx,0).length()==0:AE=set([J])
                    else:AE=(AEid & set(list(Eiter.getConnectedEdges())))
                    if AE:
                        Eid+=list(AE)
                        AEid=(AEid-AE)
                        EE=True
                    else:continue
                if EE:continue
                else:
                    edgeListS+=[['%s.e[%s]' %(MeshN,I) for I in Eid]]
                    if len(Eid)==1:AEid.remove(Eid[0])
                    break
            if len(AEid)==0:break
        for I in edgeListS:
            sel = om2.MSelectionList()
            for J in I:sel.add(J)
            dagPath,mCmp = sel.getComponent(0)
            MeshFn=om2.MFnMesh(dagPath)
            Vid=[]
            for I in om2.MFnSingleIndexedComponent(mCmp).getElements():Vid+=MeshFn.getEdgeVertices(I)
            for J in ['%s.vtx[%s]' %(MeshFn.fullPathName(),I) for I in Vid if Vid.count(I)==1]:selRTS.add(J)
    selRTS.merge(seled, 0)
    om2.MGlobal.setActiveSelectionList(selRTS)
    rate=3
    ED=cmds.filterExpand(sm=[32],ex=0,fp=1) or []
    sel = om2.MSelectionList()
    for I in ED:sel.add(I)
    for i in range(sel.length()):
        dagPath,mCmp = sel.getComponent(i)
        Eid =om2.MFnSingleIndexedComponent(mCmp).getElements()
        iterE= om2.MItMeshEdge(dagPath,mCmp)
        mag=0
        for I in Eid:
            iterE.setIndex(I)
            mag+=iterE.length()
    lim=mag/len(Eid)*rate
    VTX=cmds.filterExpand(sm=[31],ex=0,fp=1) or []
    sel = om2.MSelectionList()
    for I in VTX:sel.add(I)
    for i in range(sel.length()):
        dagPath,mCmp = sel.getComponent(i)
        iterV= om2.MItMeshVertex(dagPath)
        MeshFn = om2.MFnMesh(dagPath)
        MeshN = MeshFn.fullPathName()
        Vid =list(om2.MFnSingleIndexedComponent(mCmp).getElements())
        WP=[MeshFn.getPoint(I,4) for I in Vid]
        num=len(Vid)
        eds=[]
        for j in range(num)[::-1]:
            dis=[WP[j].distanceTo(I) for I in WP]
            dis[j]=lim
            dismin=min(dis)
            if dismin<lim:
                ID=dis.index(dismin)
                NV=[Vid[j],Vid[ID]]
                Vid.pop(ID)
                WP.pop(ID)
                eds+=cmds.polySelect(MeshN,sep=(NV),ass=1) or []
        if eds:
            cmds.select(eds,add=1)
            cmds.select(cmds.polyListComponentConversion(eds,tv=1),d=1)
        VTX=cmds.filterExpand(sm=[31],ex=1,fp=1) or []
        if len(VTX)<3:cmds.select(VTX,d=1)


def slitEdgeB():
    cmds.polySplitEdge()
    sel = om2.MSelectionList()
    for I in cmds.filterExpand(sm=32,fp=1) or []:sel.add(I)
    ssd=cmds.softSelect(q=1,ssd=1)
    soft=cmds.softSelect(q=1,softSelectEnabled=1)
    for i in range(sel.length()):
        dagPath,mCmp = sel.getComponent(i)
        MeshFn = om2.MFnMesh(dagPath)
        MeshN=MeshFn.fullPathName()
        WP=MeshFn.getPoints(4)
        Eid =om2.MFnSingleIndexedComponent(mCmp).getElements()
        Vid=[]
        for I in Eid:Vid+=MeshFn.getEdgeVertices(I) 
        Vid=list(set(Vid))
        VWP=[WP[I] for I in Vid]
        SVid=[Vid[j] for j in range(len(VWP)) if VWP.count(VWP[j])==1]
        iterE= om2.MItMeshEdge(dagPath)
        if len(SVid)==1:
            WPO=om2.MPointArray(WP)
            iterP= om2.MItMeshPolygon(dagPath)
            iterV= om2.MItMeshVertex(dagPath)
            Vid=set(Vid)-set(SVid)
            SVid=SVid[0]
            iterV.setIndex(SVid)
            CV=set(iterV.getConnectedVertices()) & Vid
            Vid=Vid - CV
            CV=list(CV)
            OL=WP[CV[0]].distanceTo(WP[SVid])/10.0
            PVTXs=[CV]
            for j in range(len(Vid)):
                CV=[]
                for J in PVTXs[-1]:
                    iterV.setIndex(J)
                    CV+=iterV.getConnectedVertices()
                CV=set(CV) & Vid
                Vid=Vid - CV
                CV=list(CV)
                PVTXs+=[CV]
                if not Vid:break
            Eid=set(Eid)
            OL1=None
            for J in PVTXs[-1:]:
                iterV.setIndex(J[0])
                CE=iterV.getConnectedEdges()
                iterV.setIndex(J[1])
                CE+=iterV.getConnectedEdges()
            CE=set(CE) - Eid
            OLS=[]
            LE=[]
            for J in CE:
                iterE.setIndex(J)
                if iterE.onBoundary():
                    OLS+=[iterE.length()]
                    LE+=[J]
            if OL>min(OLS)*0.5:OL=min(OLS)*0.5
            if len(PVTXs[-1:])==1:OL=OL*0.75
            for J in PVTXs[-1:]:
                iterV.setIndex(J[0])
                CE=list(set(iterV.getConnectedEdges()) & set(LE))
                EV=MeshFn.getEdgeVertices(CE[0])
                DV=((WP[EV[0]]-WP[J[0]])+(WP[EV[1]]-WP[J[0]])).normal()
                WPO[J[0]]=WP[J[0]]+DV*OL
                iterV.setIndex(J[1])
                CE=list(set(iterV.getConnectedEdges()) & set(LE))
                EV=MeshFn.getEdgeVertices(CE[0])
                DV=((WP[EV[0]]-WP[J[1]])+(WP[EV[1]]-WP[J[1]])).normal()
                WPO[J[1]]=WP[J[1]]+DV*OL
            for J in PVTXs[:-1]:
                if not OL1:OL1=OL*0.75
                else:OL1=OL
                iterV.setIndex(J[0])
                CE=set(iterV.getConnectedEdges()) & Eid
                CEVid=[]
                for K in CE:CEVid+=MeshFn.getEdgeVertices(K)
                if CEVid:
                    CEVid=list(set(CEVid)-set([J[0]]))
                    if len(CEVid)>1:
                        tan=(WP[J[0]] - WP[CEVid[0]])+(WP[CEVid[1]] - WP[J[0]])
                    else:
                        tan=(WP[J[0]] - WP[CEVid[0]])
                    tan=tan.normal()
                    CF=iterV.getConnectedFaces()
                    CP=om2.MVector()
                    for K in CF:
                        iterP.setIndex(K)
                        CP+=om2.MVector(iterP.center(4))
                    CP=CP/len(CF)
                    NR=((WP[CEVid[0]]-WP[J[0]]).normal())^((CP-om2.MVector(WP[J[0]])).normal())
                    CPV=CP-om2.MVector(WP[J[0]]) 
                    DV=(tan^NR).normal()
                    if CPV*DV<0:DV*=-1
                    WPO[J[0]]=WP[J[0]]+DV*OL1
                    WPO[J[1]]=WP[J[1]]+DV*OL1*-1
            om.MGlobal.executeCommand('softSelect -e -ssd %s' %(OL))
            om.MGlobal.executeCommand('softSelect -e -softSelectEnabled true')
            om.MGlobal.executeCommand('softSelect -e -ssf 1')
            for J in PVTXs:
                MV=WPO[J[0]]-WP[J[0]]
                MeshFn.setPoint(J[0],WPO[J[0]],4)
                om.MGlobal.executeCommand('select %s.vtx[%s]' %(MeshN,J[0]))
                cmds.move(MV[0], MV[1], MV[2], r=1,xc='surface')
                MV=WPO[J[1]]-WP[J[1]]
                MeshFn.setPoint(J[1],WPO[J[1]],4)
                om.MGlobal.executeCommand('select %s.vtx[%s]' %(MeshN,J[1]))
                cmds.move(MV[0], MV[1], MV[2], r=1,xc='surface')
            MeshFn.setPoints(WPO,4)
            om.MGlobal.executeCommand('softSelect -e -ssd %s' %ssd)
            om.MGlobal.executeCommand('softSelect -e -softSelectEnabled %s' %soft)
            om.MGlobal.executeCommand('select %s.vtx[%s]' %(MeshN,SVid))
            try:nPolySplitEdge(ief=1,sma=0)
            except:pass
            om2.MGlobal.setActiveSelectionList(sel)
        else:
            iterE.setIndex(Eid[0])
            CF=iterE.getConnectedFaces()
            FS=cmds.polySelect(MeshN,ns=1,asSelectString=1,ets=CF[0])
            TE=cmds.ls(cmds.polyListComponentConversion(FS,te=1),fl=1)
            TE=set([int(I.split('[')[1].rstrip(']'))for I in TE])
            Eid=list(set(Eid)-TE)
            if Eid:
                iterE.setIndex(Eid[0])
                CF=iterE.getConnectedFaces()
                FS2=cmds.polySelect(MeshN,ns=1,asSelectString=1,ets=CF[0])
                if len(cmds.ls(FS,fl=1))>len(cmds.ls(FS2,fl=1)):cmds.delete(FS2)
                else:cmds.delete(FS)
                cmds.dgdirty(MeshN,a=1)
                NP=[] 
                selE = om2.MSelectionList()
                for I in cmds.filterExpand(sm=32,fp=1) or []:selE.add(I)
                for j in range(selE.length()):
                    try:dagPath,mCmp = selE.getComponent(j)
                    except:continue
                    if mCmp.hasFn(om2.MFn.kMeshEdgeComponent):
                        iterE= om2.MItMeshEdge(dagPath)
                        iterP= om2.MItMeshPolygon(dagPath)
                        Eid =om2.MFnSingleIndexedComponent(mCmp).getElements()
                        for J in Eid:
                            iterE.setIndex(J)
                            for K in iterE.getConnectedFaces():
                                iterP.setIndex(K)
                                if iterP.numTriangles()>2:NP+=['%s.f[%s]' %(MeshN,K)]
                if NP:
                    cmds.polyTriangulate(NP)
                    cmds.polyQuad(NP)
                    om2.MGlobal.setActiveSelectionList(selE)
    cmds.select(d=1)

def nPolySplitEdge(ief=1,CT=False,sma=180):
    sel=om2.MGlobal.getActiveSelectionList()
    for i in range(sel.length()):
        try:dagPath,mCmp = sel.getComponent(i)
        except:continue
        NE=[]
        SV=-1
        if mCmp.hasFn(om2.MFn.kMeshVertComponent):
            MeshFn=om2.MFnMesh(dagPath)
            MeshN=MeshFn.fullPathName()
            numEdges=MeshFn.numEdges
            iterE= om2.MItMeshEdge(dagPath,mCmp)
            iterV= om2.MItMeshVertex(dagPath)
            iterP= om2.MItMeshPolygon(dagPath)
            Vid =om2.MFnSingleIndexedComponent(mCmp).getElements()
            PID=[]
            for I in Vid:
                iterV.setIndex(I)
                CF=[]
                for J in iterV.getConnectedFaces():
                    iterP.setIndex(J)
                    if iterP.numTriangles()==3:CF=[J]
                if CF:
                    iterP.setIndex(CF[0])
                    PID+=[CF[0]]
                    CE=iterV.getConnectedEdges()
                    PE=iterP.getEdges()
                    CE=list(set(CE)&set(PE))
                    NE+=[CE[0]]
                    iterE.setIndex(CE[1])
                    mag1=iterE.length()
                    iterE.setIndex(CE[0])
                    mag0=iterE.length()
                    if I==iterE.vertexId(0):
                        sp=0
                        mp=mag1/(mag0+mag1)
                        SV=I
                    else:
                        sp=1
                        mp=mag0/(mag0+mag1)
                        SV=iterE.vertexId(1)
                    CV=iterV.getConnectedVertices()
                    CE=[]
                    for J in CV:
                        iterV.setIndex(J)
                        CE+=iterV.getConnectedEdges()
                    NE+=list(set(PE)-set(CE))
                    break
        elif mCmp.hasFn(om2.MFn.kMeshEdgeComponent):
            MeshFn = om2.MFnMesh(dagPath)
            MeshN = MeshFn.fullPathName()
            numEdges = MeshFn.numEdges
            iterE= om2.MItMeshEdge(dagPath,mCmp)
            iterV= om2.MItMeshVertex(dagPath)
            iterP= om2.MItMeshPolygon(dagPath)
            Eid =om2.MFnSingleIndexedComponent(mCmp).getElements()
            Vid=[]
            for I in Eid:Vid+=list(MeshFn.getEdgeVertices(I))
            Vid =[I for I in set(Vid) if Vid.count(I)==1]
            EF=[]
            for I in Eid:
                iterE.setIndex(I)
                EF+=iterE.getConnectedFaces()
            EF=set(EF)
            PID=[]
            for I in Vid:
                iterV.setIndex(I)
                CF=iterV.getConnectedFaces()
                CF=list(set(CF)-EF)
                if len(CF)==1:
                    iterP.setIndex(CF[0])
                    if iterP.numTriangles()==3:
                        PID+=[CF[0]]
                        CE=iterV.getConnectedEdges()
                        CE=list(set(CE)-set(Eid))
                        NE+=[CE[0]]
                        iterE.setIndex(CE[1])
                        mag1=iterE.length()
                        iterE.setIndex(CE[0])
                        mag0=iterE.length()
                        if I==iterE.vertexId(0):
                            sp=0
                            mp=mag1/(mag0+mag1)
                            SV=I
                        else:
                            sp=1
                            mp=mag0/(mag0+mag1)
                            SV=iterE.vertexId(1)
                        PE=iterP.getEdges()
                        CV=iterV.getConnectedVertices()
                        CE=[]
                        for J in CV:
                            iterV.setIndex(J)
                            CE+=iterV.getConnectedEdges()
                        NE+=list(set(PE)-set(CE))
                        break
        SVP=MeshFn.getPoint(SV,4)
        if NE:
            if CT:mp=0.5
            lp=mp
            mps=[sp]
            for j in xrange(numEdges):
                iterE.setIndex(NE[-1])
                vtx0=iterE.point(0,4)
                vtx1=iterE.point(1,4)
                EV=vtx1-vtx0
                if SVP.distanceTo(vtx0+EV*mp)>SVP.distanceTo(vtx1+EV*mp*-1):mps+=[1.0-mp]
                else:mps+=[mp]
                CF=iterE.getConnectedFaces()
                CF=list(set(CF)-set(PID))
                if len(CF)==1:
                    iterP.setIndex(CF[0])
                    PID+=[CF[0]]
                    if iterP.numTriangles()==2:
                        SVP=vtx0+EV*mps[-1]
                        PE=iterP.getEdges()
                        CE=iterE.getConnectedEdges()
                        NE+=list(set(PE)-set(CE+NE))
                    elif iterP.numTriangles()==1:
                        PE=iterP.getEdges()
                        Le=list(set(PE)-set(NE))
                        iterE.setIndex(Le[0])
                        if iterE.vertexId(0) in list(MeshFn.getEdgeVertices(NE[-1])):lp=1
                        else:lp=0
                        NE+=[Le[0]]
                        mps+=[lp]
                        break
                    else:break
                else:break
            ip=[(NE[i],mps[i]) for i in range(len(NE))]
            cmds.polySplit(MeshN,s=1,sma=sma,ief=ief,ip=ip)


def VTXnPolyEdge():
    sel = om2.MSelectionList()
    for I in cmds.filterExpand(ex=0,sm=31,fp=1) or []:sel.add(I)
    for i in range(sel.length()):
        dagPath,mCmp = sel.getComponent(i)
        MeshFn=om2.MFnMesh(dagPath)
        iterV= om2.MItMeshVertex(dagPath)
        iterP= om2.MItMeshPolygon(dagPath)
        Vid =om2.MFnSingleIndexedComponent(mCmp).getElements()
        Vid0=Vid[0]
        iterV.setIndex(Vid0)
        CF=[]
        for J in iterV.getConnectedFaces():
            iterP.setIndex(J)
            if iterP.numTriangles()>=3:CF+=[J]
        CE=[]
        if len(CF)==2:
            for J in CF:
                iterP.setIndex(J)
                CE+=iterP.getEdges()
            CE=list(set([J for J in CE if CE.count(J)>1]))
        if CE:
            CE=cmds.polySelect(el=CE[0],ns=1)
            return CE

