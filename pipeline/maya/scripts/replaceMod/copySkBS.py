import pymel.core as pm

import maya.cmds as mc
import maya.mel as mel

import math


def CL_listBSindex(bsName):
	attrName = []
	# attr=mc.blendShape(bsName,q=1,weight=1)
	attr = mc.listAttr(bsName, m=True, st="weight")
	# attr=mc.aliasAttr(bsName+".weight[*]", q=True)
	# num=len(attr)

	if not attr:
		return attrName

	for n in attr:
		indexName = bsName + "." + n
		# aa=mc.setAttr(bsName+'.weight['+str(n)+']', 0)
		aa = mc.aliasAttr(indexName, q=1)
		attrName.append(aa)

	return attrName


def CL_findConnections(bsNode, bsIndex):
	connection = []
	if bsIndex != None:
		for a in range(0, len(bsIndex)):
			input = mc.listConnections(bsNode + "." + bsIndex[a], s=True, d=False, plugs=True)
			if input != None:
				connection.append(input[0])
			# print bsNode+"."+bsIndex[a]+" -- connected to -- "+input[0]
			else:
				connection.append("")
				pass
	return connection


def CL_listHistoryNode(objName, type):
	nodes = []
	#allHis = mc.listHistory(objName, pruneDagObjects=1, groupLevels=1, lv=3)
	allHis = mc.listHistory(objName, pruneDagObjects=1)
	#print 'allHis ', allHis
	if not allHis == None:
		for his in allHis:
			try:
				if mc.nodeType(his) == type:
					nodes.append(his)
			except:
				print
				'~~~~'
	return nodes


def CL_copySkinWts(obj1, obj2, deleteExistSkin=True):
	if not mc.objExists(obj1):
		print
		'Not find %s' % obj1
		return
	old_obj = obj1
	# new_obj = obj2

	obj2_name = obj2.split('|')[-1]
	# skin attrs
	skin = CL_listHistoryNode(old_obj, "skinCluster")

	if not skin:
		mc.warning('Object %s not bindSkin' % old_obj)
		return

	sm = mc.getAttr(skin[0] + ".skinningMethod")
	# uc=mc.getAttr(skin+".useComponents")
	# df=mc.getAttr(skin+".deformUserNormals")
	nw = mc.getAttr(skin[0] + ".normalizeWeights")
	maxInf = mc.getAttr(skin[0] + ".maxInfluences")
	mainInf = mc.getAttr(skin[0] + ".maintainMaxInfluences")
	# get influence joints
	inf_joints = mc.skinCluster(skin[0], q=1, inf=1)
	# create skin for new object

	has_skin = CL_listHistoryNode(obj2, "skinCluster")

	if not has_skin:
		has_skin = mc.skinCluster(inf_joints, obj2, n=obj2_name + '_skin', tsb=1,
		                          skinMethod=sm,
		                          normalizeWeights=nw,
		                          maximumInfluences=maxInf,
		                          obeyMaxInfluences=mainInf
		                          )
		print 'create skin 111'

	else:
		if deleteExistSkin:
			mc.skinCluster(obj2, e=True, ub=True)
			has_skin = mc.skinCluster(inf_joints, obj2, n=obj2_name + '_skin', tsb=1,
			                          skinMethod=sm,
			                          normalizeWeights=nw,
			                          maximumInfluences=maxInf,
			                          obeyMaxInfluences=mainInf
			                          )
			print 'create skin 222'
	# copy skin
	mc.copySkinWeights(ss=skin[0], ds=has_skin[0], spa=1, nm=1, sm=1)
	mc.select(obj2)
	mel.eval('removeUnusedInfluences')
	mc.select(cl=True)
	print
	obj2

	return inf_joints


def CL_getSkinInf(obj):
	skin = CL_listHistoryNode(obj, "skinCluster")
	if skin:
		inf = mc.skinCluster(skin, q=1, inf=1)
	return inf


# CL_copyDefToGeo('extra_000_grp|vest_m_000_hi','extra_000_grp|vest_m_000_hi')


def CL_copyDefToGeo(sourceObj, targetObj):
	bsNode = CL_listHistoryNode(sourceObj, "blendShape")
	if bsNode:
		CL_copyBSToGeo(sourceObj, targetObj)
		mc.setAttr('%s.envelope' % bsNode[0], 0)
	if CL_listHistoryNode(sourceObj, "skinCluster"):
		# copy skin
		CL_copySkinWts(sourceObj, targetObj)
	if bsNode:
		mc.setAttr('%s.envelope' % bsNode[0], 1)


def CL_reConnectBlendshape(sourceObj, targetObj):
	targetObj_name = targetObj.split('|')[-1]
	bsNodes = CL_listHistoryNode(sourceObj, 'blendShape')

	if bsNodes:
		bsNode = bsNodes[0]
		bs = pm.PyNode(bsNode)
		print bs
		index = bs.weightIndexList()

		target_BS = mc.blendShape(targetObj,foc=True, n=targetObj_name + '_BS', tc=True)[0]

		for i in index:
			aliasAttr = mc.aliasAttr("%s.weight[%s]" % (bsNode, i), q=True)
			value = mc.getAttr('%s.%s' % (bsNode, aliasAttr))
			shape = bs.getTargets(bs.getGeometry()[0], i)[0].getTransform().name()
			mc.blendShape(target_BS, e=True,foc=True, tc=False, t=(targetObj, i, shape, 1))
			mc.setAttr('%s.%s' % (target_BS, shape), value)
			connectAttr = mc.listConnections('%s.%s' % (bsNode, aliasAttr), s=True, d=False, p=True)
			if connectAttr:
				mc.connectAttr(connectAttr[0], '%s.%s' % (target_BS, shape))


def CL_gotBsIndexAndAlias(bsNode):
	result = {}

	if mc.nodeType(bsNode) == 'blendShape':
		index = mc.getAttr('%s.weight' % bsNode, mi=True)
		for i in index:
			aliasAttrName = mc.aliasAttr('%s.w[%d]' % (bsNode, i), q=1)
			result[aliasAttrName] = i

		return result


def CL_getBsConnectedTarget(bsNode, index):
	result = None

	if mc.nodeType(bsNode) == 'blendShape':
		# print bsNode,index
		tar = mc.listConnections(
			'%s.inputTarget[0].inputTargetGroup[%d].inputTargetItem[6000].inputGeomTarget' % (bsNode, index), s=True,
			d=False)
		# tar = bs.getTargets(bs.getGeometry()[0],index)

		if tar:
			result = tar[0]
			return result


def CL_copyBSToGeo(sourceObj, targetObj):
	if CL_listHistoryNode(targetObj, 'blendShape'):
		mc.error('%s already have blendShape ,  plese check!' % targetObj)
		return
	#source_bs = CL_listHistoryNode(sourceObj, 'blendShape')

	temp_geo = mc.duplicate(targetObj, n='TEMPBS_' + targetObj)[0]
	CL_copyBSToGeo_per(sourceObj, temp_geo)
	temp_bs_Nodes = CL_listHistoryNode(temp_geo, 'blendShape')

	if temp_bs_Nodes:
		temp_bs_Node = temp_bs_Nodes[0]
		getUselessTar(temp_bs_Node)
		CL_copyBSToGeo_per(temp_geo, targetObj)

	mc.delete(temp_geo)
	return 'Done'


def CL_copyBSToGeo_per(sourceObj, targetObj):
	targetObj_name = targetObj.split('|')[-1]

	bsNodes = CL_listHistoryNode(sourceObj, 'blendShape')
	if not bsNodes:
		mc.warning('Object %s no blendShape' % sourceObj)
		return
	bsNode = bsNodes[0]
	print
	'bsNode', bsNode

	bsIndex = CL_listBSindex(bsNode)
	print
	bsIndex

	if not bsIndex:
		mc.warning('blendShape %s no target ' % sourceObj)
		return

	shapeList = []
	attrList = []

	attrValue = []

	needDeleteShapeList = []

	# trun on BS
	mc.setAttr(bsNode + ".envelope", 1)
	if bsIndex != None:
		aliasAttrNameWithIndexDict = CL_gotBsIndexAndAlias(bsNode)

		allIndex = CL_listBSindex(bsNode)
		BSindex = []
		for b in range(0, len(bsIndex)):
			BSindex.append(bsIndex[b])
		# print BSindex
		connection = CL_findConnections(bsNode, bsIndex)

		wrapNode = CL_listHistoryNode(targetObj, "wrap")
		if len(wrapNode) == 0:
			mc.select(targetObj, sourceObj)
			mc.CreateWrap(exclusiveBind=1)

		for a in range(0, len(bsIndex)):
			oldValue = mc.getAttr(bsNode + "." + BSindex[a])
			attrValue.append(oldValue)

			input = mc.listConnections(bsNode + "." + BSindex[a], s=True, d=False, plugs=True)
			if input != None:
				mc.disconnectAttr(input[0], bsNode + "." + BSindex[a])

			mc.setAttr(bsNode + "." + BSindex[a], 0)
			mc.setAttr(bsNode + "." + BSindex[a], 1)
			attrName = mc.aliasAttr(bsNode + "." + BSindex[a], q=True)

			realIndex = aliasAttrNameWithIndexDict[attrName]
			newShape = CL_getBsConnectedTarget(bsNode, realIndex)
			if not newShape:
				newShape = mc.duplicate(targetObj, n=targetObj_name + '_' + attrName)[0]
				needDeleteShapeList.append(newShape)

			mc.setAttr(bsNode + "." + BSindex[a], 0)
			mc.select(cl=True)
			# print targetObj,a,newShape
			shapeList.append(newShape)
			# connection.append(input)
			attrList.append(attrName)
		# print a,bsNode+indexName,input,attrName
		# print bsNode+"."+BSindex[a], connection[a]

		targetBS = targetObj_name + "_BS"
		BSnode = CL_listHistoryNode(targetObj, "blendShape")

		if BSnode:
			targetBS = BSnode[0]
		else:
			#print '1111'
			targetBS = mc.blendShape(targetObj,foc=True,sd=1, n=targetObj_name + "_BS", tc=False)[0]
			#targetBS = mc.blendShape(targetObj, foc=True, n=targetObj_name + "_BS", tc=False)[0]


		# print BSnode,targetBS
		for i in range(0, len(shapeList)):
			# add blendshape and re-connect
			mc.blendShape(targetBS, e=True, tc=False, t=(targetObj, i, shapeList[i], 1.0))
			if connection[i] != "":
				# print 	connection[i],targetBS+"."+shapeList[i]
				mc.connectAttr(connection[i], targetBS + "." + shapeList[i], f=True)
				mc.connectAttr(connection[i], bsNode + "." + attrList[i], f=True)

			else:

				mc.setAttr(targetBS + "." + shapeList[i], attrValue[i])

			if shapeList[i] in needDeleteShapeList:
				try:
					mc.aliasAttr(attrList[i], targetBS + "." + shapeList[i])
				except:
					# print targetBS+"."+shapeList[i]
					pass

		# delete wrap
		wrapNode = CL_listHistoryNode(targetObj, "wrap")
		if len(wrapNode) > 0:
			for w in wrapNode:
				mc.delete(w)
				print
				"Delete " + w + " deformer..."

	if needDeleteShapeList:
		mc.delete(needDeleteShapeList)


def mag(a, b, c):
	return math.pow(a * a + b * b + c * c, 0.5)


def getUselessTar(BS=None):
	outIndecies = []

	allITGs = mc.getAttr(BS + '.it[0].itg', mi=1)

	# i=0

	for i in allITGs:
		bsData = mc.getAttr('%s.it[0].itg[%s].iti[6000].ipt' % (BS, i))

		if bsData:
			lenV = []
			for each in bsData:
				lv = mag(*each[0:3])
				lenV.append(lv)
			maxV = max(lenV)
			# print i ,maxV
			if maxV < 0.01:
				outIndecies.append(i)

		else:
			outIndecies.append(i)

	for kk in outIndecies:
		mel.eval('blendShapeDeleteTargetGroup %s %s' % (BS, kk))
	# mc.setAttr('%s.it[0].itg[%s].iti[6000].ict'%( BS,kk) , type = 'componentList' , *[0])
	# mc.setAttr('%s.it[0].itg[%s].iti[6000].ipt'% (BS,kk), type = 'pointArray' , *[0])

	# source = mc.listConnections('%s.w[%s]'%( BS,kk ) , s = 1 , d = 0 , p = 1)
	# if source:
	#	mc.disconnectAttr(source[0] , '%s.w[%d]'%(BS,kk))

	return outIndecies


# getUselessTar('tshirtDriver_m_000_low_BS')


def batchSet():
	selObj = mc.ls(sl=True)
	for i in selObj:
		bs = CL_listHistoryNode(i, 'blendShape')
		for j in bs:
			getUselessTar(j)

def getOrigmesh(obj=None):
	orig = None
	obj = pm.PyNode(obj)
	shapes = obj.getShapes(ni=0)
	if not shapes:
		return None
	for shape in shapes:
		if 'Orig' in shape.name():
			outputs = shape.worldMesh[0].outputs()
			if outputs:
				return shape



def batchReconnectDeformer(source=None,target=None):
	source = pm.PyNode(source)
	target = pm.PyNode(target)
	sourceOrig = getOrigmesh(source)

	if not sourceOrig:
		print 'not find Orig mesh'
		return
	defomerIn = sourceOrig.worldMesh[0].outputs(p=1)[0]
	defomerOut = source.getShape().inMesh.inputs(p=1)[0]

	#1. create orig mesh
	targetShape = target.getShape()
	tarOrig = pm.createNode('mesh',name=targetShape+'Orig',p=target)
	tarOrig.intermediateObject.set(1)
	targetShape.outMesh >> tarOrig.inMesh

	tarOrig.worldMesh[0] >> defomerIn
	defomerOut >> targetShape.inMesh
	tarOrig.inMesh.disconnect()
	print 'transfer {} --> {}'.format(source, target)
	pass