import pymel.core as pm
import maya.mel as mel

def resetSkin():
    selObj = pm.ls(sl=True)
    if selObj:
        for obj in selObj:
            skinNmae = mel.eval('findRelatedSkinCluster("%s")'%obj)
            if skinNmae:
                skinPN = pm.PyNode(skinNmae)
                #skinPN = pm.PyNode('EyeBrowSC')
                infs = skinPN.getInfluence()
                indexs = skinPN.lockWeights.get(mi=True)
                for i,jnt in zip(indexs,infs):
                    skinPN.bindPreMatrix[i].set(jnt.worldInverseMatrix[0].get(),type='matrix')

resetSkin()
