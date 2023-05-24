 
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

# poly mesh and skinCluster name
#shapeName = 'pPlane1'
#skinClusterNode = 'skinCluster6'


class SkinCluster():
	def __init__(self,shapeName):
		self.info = {}
		self.info['geometry'] = shapeName
		self.info['skinClusterNode'] = self.findRelatedSkinCluster(shapeName)		
		self.info['envelope'] = mc.getAttr(self.info['skinClusterNode']+'.envelope')
		self.info['skinningMethod'] = mc.getAttr(self.info['skinClusterNode']+'.skinningMethod')
		self.info['useComponents'] = mc.getAttr(self.info['skinClusterNode']+'.useComponents')
		self.info['normalizeWeights'] = mc.getAttr(self.info['skinClusterNode']+'.normalizeWeights')
		self.info['deformUserNormals'] = mc.getAttr(self.info['skinClusterNode']+'.deformUserNormals')
		
		#self.info['jntIndexs'] = mc.getAttr(self.info['skinClusterNode']+'.lw',mi=True)
		
		self.info['infsJnts'] = self.getInfsJnts()
		
		self.info['vertexIndexs'] = mc.getAttr(self.info['skinClusterNode']+'.blendWeights',mi=True)
		self.info['weights'] = self.getSkinWeights()		
		self.info['blendWeights'] = self.getblendWeights()
		
	
	def findRelatedSkinCluster(self,shapeName):
		return mel.eval('findRelatedSkinCluster("%s")'%shapeName)
	
	def getblendWeights(self):
		blendWeights = {}
		indexs = self.info['vertexIndexs']
		if indexs:
			values = mc.getAttr(self.info['skinClusterNode']+'.blendWeights')[0]
			for i in xrange(len(indexs)):
				blendWeights[indexs[i]] = values[i]
		return blendWeights
	
	def getInfsJnts(self):
		infsJnts = {}
		jntIndexs = mc.getAttr(self.info['skinClusterNode']+'.lw',mi=True)
		infList = mc.skinCluster(self.info['skinClusterNode'],q=True,inf=True)
		for i in xrange(len(jntIndexs)):
			infsJnts[jntIndexs[i]] = infList[i]
		return infsJnts
	
	def getSkinWeights(self):
		weights = {}
		tt = time.time()
		vertexIndexs = self.info['vertexIndexs']
		if vertexIndexs:
			for vertexIndex in self.info['vertexIndexs']:
				vertexWeights = {}
				jointIndexs = mc.getAttr(self.info['skinClusterNode']+'.weightList[%d].weights'%(vertexIndex),mi=True)
				for jointIndex in jointIndexs :
					vertexWeights[self.info['infsJnts'][jointIndex]] = mc.getAttr(self.info['skinClusterNode']+'.weightList[%d].weights[%d]'%(vertexIndex,jointIndex),mi=True)
				weights[vertexIndex] = vertexWeights
		
		print time.time()-tt		
		return weights


def setSkinWeight(shapeName,SkinClusterInfo):
    
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
    skinNorm = mc.getAttr('%s.normalizeWeights' % skinClusterNode)
    if skinNorm != 0:
    	mc.setAttr('%s.normalizeWeights' % skinClusterNode, 0)
    mc.skinPercent(skinClusterNode, shapeName, nrm=False, prw=100)
    
    # restore normalize setting
    if skinNorm != 0:
    	mc.setAttr('%s.normalizeWeights' % skinClusterNode, skinNorm)
    inverseInfs = dict((value,key) for key,value in infs.iteritems())
    weights = SkinClusterInfo['weights']
    for vertId, weightData in weights.items():
    	wlAttr = '%s.weightList[%s]' % (skinClusterNode, vertId)
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


def storeSkinWeight():
    selObjs = mc.ls(sl=True)
    
    if selObjs:
        selObj = selObjs[0] 
        #weights = getSkinWeightInfo(selObj)
        singleFilter = ".w (*.w)"
        fileName = mc.fileDialog2(fileFilter=singleFilter, dialogStyle=2)
        if fileName:
            fileName = fileName[0]
            tt = time.time()
            SkinClusterInfo = SkinCluster(selObj)
            f = open(fileName,'w')
            pickle.dump(SkinClusterInfo,f,protocol=0)
            f.close()
            print time.time()-tt


def writeSkinWeight():
    selObjs = mc.ls(sl=True)
    
    if selObjs:
        selObj = selObjs[0]
        singleFilter = ".w (*.w)"
        fileName = mc.fileDialog2(fileFilter=singleFilter, dialogStyle=2,fm=1)
        if fileName:
            fileName = fileName[0]
            f = open(fileName,'r')
            SkinClusterInfo = pickle.load(f)
            f.close()
            tt = time.time()
            setSkinWeight(selObj,SkinClusterInfo)
            print time.time() -tt
    return 'Done!!!'


#storeSkinWeight()
#writeSkinWeight()
    