#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
'''
   File    :   bath_cloth_com.py
   Time    :   2023/03/18 16:44:28
   Author  :   Liu ZhenBao
   Version :   1.0
   Contact :   3305510092@qq.com
   Desc    :   None
'''
############################################################################

# import the libraries needed by this script here
import os, sys, logging
import maya.standalone
maya.standalone.initialize(name="python")

import maya.mel as mel
import maya.cmds as cmds
import pymel.core as pm

class ClothAssembleCom:
    def __init__(self):
        self.abs_file = None
        self.fbx_file = None
        self.mb_file = None
    
    def re_abs_file(self, file_path, sp_name="abc"):
        type_dict = {"abc": "Alembic", "fbx": "FBX"}
        """
        Args:
            file_path (str, path): 
            sp_name (str, optional): "abc" or "fbx".
        """
        cmds.file(file_path, r=1, type=type_dict(sp_name), namespace=sp_name, force=1)

    
    def copy_skin_weights(self, _mesh, skin_mesh):
        """
            Args: _mesh=带蒙皮的模型， skin_mesh=需要蒙皮的模型
            Return: 需要跟随的骨骼列表
        """
        try:
            skin_node = mel.eval("findRelatedSkinCluster" + _mesh)
            skin_joint = cmds.listConnections("{}.matrix".format(skin_node), type="joint")
            cmds.skinCluster(skin_joint, skin_mesh)
            cmds.copySkinWeights(_mesh, skin_mesh, noMirror=1, surfaceAssociation="closestPoint", influenceAssociation=["closestJoint", "closestBone", "oneToOne"])
        except:
            print("Failed to copy weights: {}".format(_mesh))
        return skin_joint

    def loc_on_mesh(self, _mesh, _jnt_lst):
        """
            Args:
                _mesh: 跟随的模型
                _jnt_lst: 需要跟随的骨骼列表
        """
        for jnt in _jnt_lst:           
            if not cmds.objExists("loc_hair_GP"):
                loc_grp = cmds.group(em=1, name="loc_hair_GP")
                cmds.parent(loc_grp, "Group")
            abs_mesh = pm.PyNode(_mesh)
            shape_node = abs_mesh.getShape()
            po_node = pm.createNode("closestPointOnMesh", name="{}_point_on_mesh".format(jnt))
            pm.connectAttr("{}.outMesh".format(shape_node), "{}.inMesh".format(po_node))
            pm.select(clear=1)
            loc_jnt = pm.joint(name="loc_jnt")
            pm.matchTransform(loc_jnt, jnt)
            pm.connectAttr("{}.t".format(loc_jnt), "{}.inPosition".format(po_node))
            par_v = pm.getAttr("{}.parameterV".format(po_node))
            par_u = pm.getAttr("{}.parameterU".format(po_node))
            pm.delete(po_node, loc_jnt)
            tra_node = pm.createNode("transform", name="{}_follicle".format(jnt), p="loc_hair_GP")
            foll_node = pm.createNode("follicle", name="{}Shape".format(tra_node), p=tra_node)
            pm.connectAttr("{}.outRotate".format(foll_node), "{}.rotate".format(tra_node))
            pm.connectAttr("{}.outTranslate".format(foll_node), "{}.translate".format(tra_node))
            pm.connectAttr("{}.outMesh".format(shape_node), "{}.inputMesh".format(foll_node))
            pm.connectAttr("{}.worldMatrix[0]".format(shape_node), "{}.inputWorldMatrix".format(foll_node))
            pm.setAttr("{}.parameterV".format(foll_node), par_v)
            pm.setAttr("{}.parameterU".format(foll_node), par_u)
            pm.parentConstraint(tra_node, jnt, mo=1, dr=1)

    def main(self, check_maya_file):
        """
        """
        if not os.path.isfile(check_maya_file):
            logging.warning("Failed because Maya file was not found! - {}".format(check_maya_file))
        logging.info("Statr check - {}".format(check_maya_file))
        try:
            cmds.file(check_maya_file, open=True, pmt=False, force=True)
            fx_geo_lst = [_geo for _geo in cmds.listRelatives("FX", ad=1, type="mesh") if "Orig" not in _geo]
            for _geo in fx_geo_lst:
                str_lst = _geo.split("_")
                # 检索渲染模型
                str_lst.remove("grom")
                render_model = "_".join(str_lst)            
                # 添加bs
                cmds.blendShape("abc:{}".format(_geo), _geo, weight=[0, 1])
                # 复制权重
                jiont_lst = self.copy_skin_weights("fbx:{}".format(_geo), render_model)
                # 创建毛囊定位
                self.loc_on_mesh(_geo, jiont_lst)
            
            
            cmds.file(save=1)
        except:
            pass

if __name__ == "__main__":
    return_str = ClothAssembleCom.main(sys.argv[1])