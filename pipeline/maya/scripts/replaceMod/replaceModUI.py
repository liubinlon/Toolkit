# replace mod UI 
##################################################################
# import sys 
# path = '/ibrix3/WHD/editorial/reference/Department_Ref/Rigging/luzy/script'
# if path not in sys.path:
#	sys.path.append(path)
# import manageCloth.replaceModUI as replaceModUI
# reload(replaceModUI)
# AAA = replaceModUI.do()
####################################################################

import maya.cmds as mc

import copySkBS as copySkBS
reload(copySkBS)

from skinWeights import loadSkinWeights
reload(loadSkinWeights)

class do():
	def __init__(self):
		self.window = 'ReplaceModUI'
		self.AllradioButton = 'AllradioButton'
		self.OneToOneradioButton = 'OneToOneradioButton'
		self.PrefixNametextFieldGrp = 'PrefixNametextFieldGrp'

		if mc.window(self.window, q=True, ex=True):
			mc.deleteUI(self.window)
		mc.window(self.window, s=True, wh=[100, 100], title='ReplaceModUI', mxb=False, mnb=True)
		mc.columnLayout(adj=True)

		mc.rowColumnLayout(nc=3, cw=[(1, 150), (2, 50), (3, 80)])
		mc.radioCollection()
		mc.text(l='                    Replace Type:')
		mc.radioButton(self.AllradioButton, l='ALL', )
		mc.radioButton(self.OneToOneradioButton, sl=True, l='One To One')
		mc.setParent('..')
		mc.separator(st='in', w=380)
		mc.textFieldButtonGrp(self.PrefixNametextFieldGrp, l='Prefix :', tx='AAA_', bl='Add_Prefix',
		                      bc=lambda *arg: self.Add_PrefixCmd(), en=0)
		# mc.separator(st='in',w=380)
		# mc.button(l='Copy SkinWeight And reConnect Blendshape',bgc=[.6,.5,.3],w=390,h=30,c=lambda *arg: self.copyBodyCmd())


		mc.separator(st='in', w=380, h=10)
		self.deSK = mc.checkBox(label='Delete Exists skin node on target')


		mc.separator(st='in', w=380, h=10)
		mc.button(l='Copy SkinWeight And Blendshape', bgc=[.2, .5, .4], w=390, h=40, c=lambda *arg: self.batchCopyCmd())
		mc.separator(st='none', w=380, h=10)
		mc.button(l='Copy SkinWeight', bgc=[.2, .5, .4], w=390, h=30, c=lambda *arg: self.batchCopy_skin_Cmd())
		mc.separator(st='none', w=380, h=10)
		mc.button(l='Copy Blendshape', bgc=[.2, .5, .4], w=390, h=30, c=lambda *arg: self.batchCopy_BS_Cmd())

		mc.separator(st='none', w=380, h=10)
		mc.button(l='Reconnect deformer', bgc=[.5, .3, .3], w=390, h=30, c=lambda *arg: self.batch_Reconnect_deformer_Cmd())

		mc.separator( style='in',h=20 )
		mc.button( h = 30, l = "Export Skin Weight", c = lambda *arg:loadSkinWeights.storeSkinWeight(), bgc = [0.675, 0.663, 0.843])
		mc.separator( style='none',h=10 )
		mc.button( h = 30, l = "Import Skin Weight", c = lambda *arg:loadSkinWeights.writeSkinWeight(), bgc = [0.675, 0.663, 0.843])
		mc.separator( style='none',h=20 )

		mc.radioButton(self.AllradioButton, e=True,
		               cc=lambda *arg: mc.textFieldGrp(self.PrefixNametextFieldGrp, e=True, en=1))
		mc.radioButton(self.OneToOneradioButton, e=True,
		               cc=lambda *arg: mc.textFieldGrp(self.PrefixNametextFieldGrp, e=True, en=0))
		mc.showWindow(self.window)

	def copyBodyCmd(self):
		selObj = mc.ls(sl=True)
		if mc.radioButton(self.AllradioButton, q=True, sl=True):
			prefixName = mc.textFieldGrp(self.PrefixNametextFieldGrp, q=True, text=True)
			for obj in selObj:
				if mc.objExists(prefixName + obj):
					copySkBS.CL_reConnectBlendshape(prefixName + obj, obj)
					deleteExistSkin  = mc.checkBox(self.deSK,q=1,v=1)
					copySkBS.CL_copySkinWts(prefixName + obj, obj,deleteExistSkin=deleteExistSkin)

					self.reconnectVis(prefixName + obj, obj)
		else:
			if len(selObj) >= 2:
				for obj in selObj[1::]:
					copySkBS.CL_reConnectBlendshape(selObj[0], obj)
					deleteExistSkin = mc.checkBox(self.deSK, q=1, v=1)
					copySkBS.CL_copySkinWts(selObj[0], obj,deleteExistSkin=deleteExistSkin)
					self.reconnectVis(selObj[0], obj)

	def batchCopy_skin_Cmd(self):
		selObj = mc.ls(sl=True)
		if mc.radioButton(self.AllradioButton, q=True, sl=True):
			prefixName = mc.textFieldGrp(self.PrefixNametextFieldGrp, q=True, text=True)
			for obj in selObj:
				sourceObj = prefixName + obj.split('|')[-1]

				if mc.objExists(sourceObj):
					# self.replaceConstraint(sourceObj,obj)
					deleteExistSkin = mc.checkBox(self.deSK, q=1, v=1)
					copySkBS.CL_copySkinWts(sourceObj, obj,deleteExistSkin=deleteExistSkin)
					self.reconnectVis(sourceObj, obj)
		else:
			if len(selObj) >= 2:
				for obj in selObj[1::]:
					# self.replaceConstraint(selObj[0],obj)
					deleteExistSkin = mc.checkBox(self.deSK, q=1, v=1)
					copySkBS.CL_copySkinWts(selObj[0], obj,deleteExistSkin=deleteExistSkin)
					self.reconnectVis(selObj[0], obj)

	def batchCopy_BS_Cmd(self):
		selObj = mc.ls(sl=True)
		if mc.radioButton(self.AllradioButton, q=True, sl=True):
			prefixName = mc.textFieldGrp(self.PrefixNametextFieldGrp, q=True, text=True)
			for obj in selObj:
				sourceObj = prefixName + obj.split('|')[-1]

				if mc.objExists(sourceObj):
					# self.replaceConstraint(sourceObj,obj)
					copySkBS.CL_copyBSToGeo(sourceObj, obj)

					self.reconnectVis(sourceObj, obj)
		else:
			if len(selObj) >= 2:
				for obj in selObj[1::]:
					# self.replaceConstraint(selObj[0],obj)
					copySkBS.CL_copyBSToGeo(selObj[0], obj)
					self.reconnectVis(selObj[0], obj)


	def batch_Reconnect_deformer_Cmd(self):
		selObj = mc.ls(sl=True)
		if mc.radioButton(self.AllradioButton, q=True, sl=True):
			prefixName = mc.textFieldGrp(self.PrefixNametextFieldGrp, q=True, text=True)
			for obj in selObj:
				sourceObj = prefixName + obj.split('|')[-1]

				if mc.objExists(sourceObj):
					# self.replaceConstraint(sourceObj,obj)
					copySkBS.batchReconnectDeformer(sourceObj, obj)

					self.reconnectVis(sourceObj, obj)
		else:
			if len(selObj) >= 2:
				for obj in selObj[1::]:
					# self.replaceConstraint(selObj[0],obj)
					copySkBS.batchReconnectDeformer(selObj[0], obj)
					self.reconnectVis(selObj[0], obj)


	def batchCopyCmd(self):
		selObj = mc.ls(sl=True)
		if mc.radioButton(self.AllradioButton, q=True, sl=True):
			prefixName = mc.textFieldGrp(self.PrefixNametextFieldGrp, q=True, text=True)
			for obj in selObj:
				sourceObj = prefixName + obj.split('|')[-1]

				if mc.objExists(sourceObj):
					self.replaceConstraint(sourceObj, obj)
					copySkBS.CL_copyDefToGeo(sourceObj, obj)
					self.reconnectVis(sourceObj, obj)
		else:
			if len(selObj) >= 2:
				for obj in selObj[1::]:
					self.replaceConstraint(selObj[0], obj)
					copySkBS.CL_copyDefToGeo(selObj[0], obj)
					self.reconnectVis(selObj[0], obj)

	def reconnectVis(self, source=None, target=None):
		if mc.objExists(source):
			print
			'Not find %s' % source
			return
		oldConnectAttr = mc.listConnections('%s.v' % source, s=True, d=False, p=True)
		if oldConnectAttr:
			mc.connectAttr(oldConnectAttr[0], '%s.v' % target)

	def replaceConstraint(self, source=True, aim=True):
		constraintFuncs = [mc.pointConstraint, mc.orientConstraint, mc.aimConstraint, mc.parentConstraint,
		                   mc.scaleConstraint]
		for consFun in constraintFuncs:
			tls = consFun(source, q=1, tl=1)
			if tls:
				consFun(tls, aim, mo=1, w=1)

	def Add_PrefixCmd(self):

		selObjs = mc.ls(sl=True)
		prefixName = mc.textFieldGrp(self.PrefixNametextFieldGrp, q=True, text=True)
		for selObj in selObjs:
			allChild = [selObj]
			allChild_B = mc.listRelatives(selObj, ad=True, typ='transform', f=True)
			if allChild_B:
				allChild = allChild_B + allChild

			for child in allChild:
				oldName = child.split('|')[-1]
				if oldName:
					mc.rename(child, prefixName + oldName)
		pass











