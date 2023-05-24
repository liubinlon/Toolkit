##############################################################
#import skinWeights

#skinWeights.storeSkinWeight()
#skinWeights.writeSkinWeight()


#######################################################################################################
import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import maya.cmds as mc
import maya.mel as mel
import time
import cPickle as pickle
import re

# poly mesh and skinCluster name
#shapeName = 'pPlane1'
#skinClusterNode = 'skinCluster6'


def SkinCluster(shapeName):
    SkinClusterInfo = {}
    #SkinClusterInfo['shapeName'] = shapeName
    skinClusterNode = findRelatedSkinCluster(shapeName)
    
    skinFn = getSkinFn(skinClusterNode)
    
    SkinClusterInfo['envelope'] = mc.getAttr(skinClusterNode+'.envelope')
    SkinClusterInfo['skinningMethod'] = mc.getAttr(skinClusterNode+'.skinningMethod')
    SkinClusterInfo['useComponents'] = mc.getAttr(skinClusterNode+'.useComponents')
    SkinClusterInfo['normalizeWeights'] = mc.getAttr(skinClusterNode+'.normalizeWeights')
    SkinClusterInfo['deformUserNormals'] = mc.getAttr(skinClusterNode+'.deformUserNormals')
    
    SkinClusterInfo['infJnts'] = getInfs(skinFn)
    SkinClusterInfo['weights'] = getSkinWeightInfo(skinFn)
    SkinClusterInfo['blendWeights'] = getblendWeights(skinClusterNode)
    return SkinClusterInfo
        
        

#SkinClusterInfo = SkinCluster(selObj)
#SkinClusterInfo.weights
#SkinClusterInfo.skinCluster




def findRelatedSkinCluster(shapeName):
     return mel.eval('findRelatedSkinCluster("%s")'%shapeName)
     
def getblendWeights(skinClusterNode):
    blendWeights = {}
    indexs = mc.getAttr(skinClusterNode+'.blendWeights',mi=True)
    if indexs:
        values = mc.getAttr(skinClusterNode+'.blendWeights')[0]
        for i in xrange(len(indexs)):
            blendWeights[indexs[i]] = values[i]
    return blendWeights
    
    
def getInfs(skinFn):
    infs = {}
    # create a dictionary whose key is the MPlug indice id and 
    # whose value is the influence list id
    infDags = OpenMaya.MDagPathArray()
    skinFn.influenceObjects(infDags)
    for x in xrange(infDags.length()):
    	infPath = infDags[x].partialPathName()
    	infId = int(skinFn.indexForInfluenceObject(infDags[x]))
    	#infs.append(infPath)
    	infs[infId]= infPath
    return infs     

def getSkinFn(skinClusterNode):
    skinFn = None
    if skinClusterNode:
        # get the MFnSkinCluster for clusterName
        selList = OpenMaya.MSelectionList()
        selList.add(skinClusterNode)
        clusterNode = OpenMaya.MObject()
        selList.getDependNode(0, clusterNode)
        skinFn = OpenMayaAnim.MFnSkinCluster(clusterNode)
        
        # get the MDagPath for all influence    
    return skinFn
#skinFn = getSkinFn(skinClusterNode)
def getSkinWeightInfo(skinFn):
    weights = {}
    #shapeName = 'pPlane1'
    #skinClusterNode = 'skinCluster3'
    # get the MPlug for the weightList and weights attributes
    wlPlug = skinFn.findPlug('weightList')
    wPlug = skinFn.findPlug('weights')
    wlAttr = wlPlug.attribute()
    wAttr = wPlug.attribute()
    wInfIds = OpenMaya.MIntArray()
    
    # the weights are stored in dictionary, the key is the vertId, 
    # the value is another dictionary whose key is the influence id and 
    # value is the weight for that influence
    infs = getInfs(skinFn)
    for vId in xrange(wlPlug.numElements()):
    	vWeights = {}
    	
    	# tell the weights attribute which vertex id it represents
    	wPlug.selectAncestorLogicalIndex(vId, wlAttr)
    	
    	# get the indice of all non-zero weights for this vert
    	wPlug.getExistingArrayAttributeIndices(wInfIds)
    
    	# create a copy of the current wPlug
    	infPlug = OpenMaya.MPlug(wPlug)
    	
    	# 
    	
    	for infId in wInfIds:
    		# tell the infPlug it represents the current influence id
    		#infId = 0
    		infPlug.selectAncestorLogicalIndex(infId, wAttr)
    		
    		# add this influence and its weight to this verts weights
    		try:
    			vWeights[infs[infId]] = infPlug.asDouble()
    		except KeyError:
    			# assumes a removed influence
    			pass
    	weights[vId] = vWeights
    return weights 
#shapeName = 'pSphere1'    
def setSkinWeight(shapeName,vertexIndexList,SkinClusterInfo):
    
    infJnts = SkinClusterInfo['infJnts'].values()
    for jnt in infJnts:
        if not mc.objExists(jnt):
            print 'Not find jnt %s'%jnt
            return
    
    
    if not findRelatedSkinCluster(shapeName):
        mc.skinCluster(infJnts,shapeName,tsb=True)
    
    skinClusterNode = findRelatedSkinCluster(shapeName)
    #skinFn =  getSkinFn(skinClusterNode)
    jnts = mc.skinCluster(shapeName,q=True,inf=True,)
    for jnt in infJnts:
        if jnt not in jnts:
            try:
                mc.skinCluster(skinClusterNode,edit=True,ai=jnt)
            except:
                 pass
    
    skinFn =  getSkinFn(skinClusterNode)
    infs = getInfs(skinFn)
    # unlock influences used by skincluster
    #infs = mc.skinCluster(skinClusterNode,q=True,inf=True)
    #mc.skinCluster(q=True,inf=True)
    for inf in infs.values():
    	mc.setAttr('%s.liw' % inf)
    
    # normalize needs turned off for the prune to work
    #skinNorm = mc.getAttr('%s.normalizeWeights' % skinClusterNode)
    #if skinNorm != 0:
    #	mc.setAttr('%s.normalizeWeights' % skinClusterNode, 0)
    #mc.skinPercent(skinClusterNode, shapeName, nrm=False, prw=100)
    
    # restore normalize setting
    #if skinNorm != 0:
    #	mc.setAttr('%s.normalizeWeights' % skinClusterNode, skinNorm)
    
    inverseInfs = dict((value,key) for key,value in infs.iteritems())
    
    weights_all = SkinClusterInfo['weights']
    
    if vertexIndexList:
        weights = {}
        for i in vertexIndexList:
            weights[i] = weights_all[i]
    else:
        weights = weights_all
        

    for vertId, weightData in weights.items():
        wlAttr = '%s.weightList[%s]' % (skinClusterNode, vertId)
        oldJntIndexs = mc.getAttr('%s.weightList[%s].weights' % (skinClusterNode, vertId),mi=True)
        if oldJntIndexs:
            for oldJntIndex in oldJntIndexs:
                mc.setAttr(wlAttr + '.weights[%s]' % oldJntIndex, 0)
        for infJnt, infValue in weightData.items():
            wAttr = '.weights[%s]' % inverseInfs[infJnt]
            mc.setAttr(wlAttr + wAttr, infValue)
    	if vertId in SkinClusterInfo['blendWeights'].keys():
    	    mc.setAttr(skinClusterNode+'.blendWeights[%d]'%vertId,SkinClusterInfo['blendWeights'][vertId])
    	else:
    	    mc.setAttr(skinClusterNode+'.blendWeights[%d]'%vertId,0)
    
    mc.setAttr(skinClusterNode+'.envelope',SkinClusterInfo['envelope'])
    mc.setAttr(skinClusterNode+'.skinningMethod',SkinClusterInfo['skinningMethod'])
    mc.setAttr(skinClusterNode+'.useComponents',SkinClusterInfo['useComponents'])
    mc.setAttr(skinClusterNode+'.normalizeWeights',SkinClusterInfo['normalizeWeights'])
    mc.setAttr(skinClusterNode+'.deformUserNormals',SkinClusterInfo['deformUserNormals'])




def isSelectVertex(selObjs):
    mesh = ''
    vertexIndexList = []
    if selObjs:
        selObj = selObjs[0]
        mesh = selObjs[0].split('.')[0]
        if '.vtx[' in selObj:
            vertexIndexList = [int(i.split('.vtx[')[1].replace(']','')) for i in selObjs]
    return mesh,vertexIndexList

def storeSkinWeight():
    selObjs = mc.ls(sl=True)
    
    if selObjs:
        selObj = selObjs[0] 
        singleFilter = ".w (*.w)"
        fileName = mc.fileDialog2(fileFilter=singleFilter, dialogStyle=2)
        if fileName:
            fileName = fileName[0]
            tt = time.time()
            SkinClusterInfo = SkinCluster(selObj)
            print time.time()-tt
            f = open(fileName,'w')
            pickle.dump(SkinClusterInfo,f,protocol=0)
            f.close()
            print time.time()-tt
            

def storeSkinWeight_A(fileName):
    selObjs = mc.ls(sl=True)
    
    if selObjs:
        selObj = selObjs[0] 
        if fileName:
            tt = time.time()
            SkinClusterInfo = SkinCluster(selObj)
            print time.time()-tt
            f = open(fileName,'w')
            pickle.dump(SkinClusterInfo,f,protocol=0)
            f.close()
            print time.time()-tt
            return True
    else:
        return False


def writeSkinWeight_A(fileName):
    selObjs = mc.ls(sl=True,fl=True)
    
    if selObjs:
        #selObj = selObjs[0]
        mesh,vertexIndexList = isSelectVertex(selObjs)
        singleFilter = ".w (*.w)"
        if fileName:
            f = open(fileName,'r')
            SkinClusterInfo = pickle.load(f)
            f.close()
            tt = time.time()
            setSkinWeight(mesh,vertexIndexList,SkinClusterInfo)
            print time.time() -tt
    return 'Done!!!'


def writeSkinWeight():
    selObjs = mc.ls(sl=True,fl=True)
    
    if selObjs:
        #selObj = selObjs[0]
        mesh,vertexIndexList = isSelectVertex(selObjs)
        singleFilter = ".w (*.w)"
        fileName = mc.fileDialog2(fileFilter=singleFilter, dialogStyle=2,fm=1)
        if fileName:
            fileName = fileName[0]
            f = open(fileName,'r')
            SkinClusterInfo = pickle.load(f)
            f.close()
            tt = time.time()
            setSkinWeight(mesh,vertexIndexList,SkinClusterInfo)
            print time.time() -tt
    return 'Done!!!'

def batchStoreSkinweight():
    pass
def batchWriteSkinweight():
    pass


def moveFinWeightToBendy():
    selObjs = mc.ls(sl=True,fl=True)
    
    if selObjs:
        #selObj = selObjs[0]
        mesh,vertexIndexList = isSelectVertex(selObjs)
        singleFilter = ".w (*.w)"
        fileName = mc.fileDialog2(fileFilter=singleFilter, dialogStyle=2,fm=1)
        if fileName:
            
            
            fileName = fileName[0]
            f = open(fileName,'r')
            SkinClusterInfo = pickle.load(f)
            f.close()
            
            selJnt = [u'R_armA_finB_1_skn_jnt',
            u'R_armA_finB_2_skn_jnt',
            u'R_armA_finB_3_skn_jnt',
            u'R_armA_finB_4_skn_jnt',
            u'R_armA_finC_1_skn_jnt',
            u'R_armA_finC_2_skn_jnt',
            u'R_armA_finC_3_skn_jnt',
            u'R_armA_finC_4_skn_jnt',
            u'R_armA_finD_1_skn_jnt',
            u'R_armA_finD_2_skn_jnt',
            u'R_armA_finD_3_skn_jnt',
            u'R_armA_finD_4_skn_jnt',
            u'R_armA_finE_1_skn_jnt',
            u'R_armA_finE_2_skn_jnt',
            u'R_armA_finE_3_skn_jnt',
            u'R_armA_finE_4_skn_jnt',
            u'L_armA_finB_1_skn_jnt',
            u'L_armA_finB_2_skn_jnt',
            u'L_armA_finB_3_skn_jnt',
            u'L_armA_finB_4_skn_jnt',
            u'L_armA_finC_1_skn_jnt',
            u'L_armA_finC_2_skn_jnt',
            u'L_armA_finC_3_skn_jnt',
            u'L_armA_finC_4_skn_jnt',
            u'L_armA_finD_1_skn_jnt',
            u'L_armA_finD_2_skn_jnt',
            u'L_armA_finD_3_skn_jnt',
            u'L_armA_finD_4_skn_jnt',
            u'L_armA_finE_1_skn_jnt',
            u'L_armA_finE_2_skn_jnt',
            u'L_armA_finE_3_skn_jnt',
            u'L_armA_finE_4_skn_jnt']

            for i in SkinClusterInfo['weights'].keys():
                for j in SkinClusterInfo['weights'][i].keys():
                    if j in selJnt:
                        aaa = ''
                        aaa = re.search('_\d_',j).group()
                        new = j.replace(aaa,'_bendy'+aaa)

                        SkinClusterInfo['weights'][i][new] = SkinClusterInfo['weights'][i][j]
                        del SkinClusterInfo['weights'][i][j]

            for i in SkinClusterInfo['infJnts'].keys():
                if SkinClusterInfo['infJnts'][i] in selJnt:
                    print SkinClusterInfo['infJnts'][i]
                    aaa = ''
                    aaa = re.search('_\d_',SkinClusterInfo['infJnts'][i]).group()
                    new = SkinClusterInfo['infJnts'][i].replace(aaa,'_bendy'+aaa)
                    SkinClusterInfo['infJnts'][i] = new
                    print SkinClusterInfo['infJnts'][i]
            tt = time.time()
            setSkinWeight(mesh,vertexIndexList,SkinClusterInfo)
            print time.time() -tt
    return 'Done!!!'
    


#storeSkinWeight()
#writeSkinWeight()
    