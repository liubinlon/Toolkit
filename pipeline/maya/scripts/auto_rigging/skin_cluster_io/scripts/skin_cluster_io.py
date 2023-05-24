#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
'''
   File    :   skin_cluster__io.py
   Time    :   2023/05/01 12:22:18
   Author  :   Liu ZhenBao
   Version :   1.0
   Contact :   3305510092@qq.com
   Desc    :   None
'''
############################################################################

# import the libraries needed by this script here
import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as omAPI
import maya.api.OpenMayaAnim as omaAPI
import maya.OpenMayaAnim as oma
import maya.OpenMaya as om

import numpy as np
import json

import time
import sys
import os
import inspect

script_path = os.path.abspath(inspect.getsourcefile(lambda: 0))
dir = r"{0}".format(script_path)
if dir not in sys.path:
    sys.path.insert(dir)
    
from commonly_operation import CommonlyOperation
print("test")
# here put the class script
class DataIO:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def get_legend_array_from_data(data):
        return 
    
    @staticmethod
    def get_data_item(data, item, legend_array=None):
        return 
    
    @staticmethod
    def set_data_items(data, item_data_array):
        return 
    
class SkinClusterIO:
    def __init__(self) -> None:
        self.DataIO                 = DataIO()
        self.name                   = ''
        self.type                   = 'skinCluster'
        self.weights_non_zero_array = list()
        self.weighta_array          = list()
        self.inf_map_array          = list()
        self.vert_split_array       = list()
        self.inf_array              = list()
        self.skinning_method        = 1
        self.normalize_weights      = 1
        self.geometry               = None
        self.blend_weights          = list()
        self.vtx_count              = 0
        self.envelop                = 1
        self.use_components         = 0
        self.deform_user_normals    = 1
    
    def get_data(self, skin_cluster):
        # get the MFnSkinCluster for skinCluster
        sel_lst = om.MSelectionList()
        sel_lst.add(skin_cluster)
        cluster_node = om.MObject()
        sel_lst.getDependNode(0, cluster_node)
        skin_fn = oma.MFnSkinCluster(cluster_node)
        
        # get components
        fn_set = om.MFnSet(skin_fn.deformerSet())
        members = om.MSelectionList()
        fn_set.getMembers(members, False)
        dag_path = om.MDagPath()
        components = om.MObject()
        members.getDagPath(0, dag_path, components)
        
        # get mesh
        geometry = cmds.skinCluster(skin_cluster, q=1, geometry=1)[0]
        
        # get vtxID_array
        vtx_id_array = list(range(0, len(cmds.ls("{}.vtx[*]".format(geometry), fl=1))))
        
        # get skin
        sel_lst = omAPI.MSelectionList()
        sel_lst.add(mel.eval("findRelatedSkinCluster %s" % geometry))
        skin_path = sel_lst.getDependNode(0)
        
        # get mesh
        sel_lst = omAPI.MSelectionList()
        sel_lst.add(geometry)
        mesh_path = sel_lst.getDagPath(0)
        
        # get vtxs
        fn_skin_cluster = omaAPI.MFnSkinCluster(skin_path)
        fn_vtx_comp = omAPI.MFnSingleIndexedComponent()
        vtx_components = fn_vtx_comp.create(omAPI.MFn.kMeshVertComponent)
        fn_vtx_comp.addElement(vtx_id_array)

        # get weights/infs
        d_weights, inf_count = fn_skin_cluster.getWeights(mesh_path, vtx_components)
        weights_array = np.array(list(d_weights), dtype="float64")
        inf_array = [dp.partialPathName() for dp in fn_skin_cluster.influenceObjects()]
        
        # convert to weights_non_zero_array
        weights_non_zero_array, inf_map_array, vert_split_array = self.components_weight_data(weights_array, inf_count)
        
        # gather blend weights
        blend_weights_marray = om.MDoubleArray()
        skin_fn.getBlendWeights(dag_path, components, blend_weights_marray)
        
        # set data to self vars
        self.name                   = skin_cluster
        self.weights_non_zero_array = np.array(weights_non_zero_array)
        self.inf_map_array          = np.array(inf_map_array)
        self.vert_split_array       = np.array(vert_split_array)
        self.inf_array              = np.array(inf_array)
        self.geometry               = geometry
        self.blend_weights          = np.array(blend_weights_marray)
        self.vtx_count              = len(vert_split_array)-1

        # get attrs
        self.envelop             = cmds.getAttr("{}.envelope".format(skin_cluster))
        self.skinning_method     = cmds.getAttr("{}.skinningMethon".format(skin_cluster))
        self.use_components      = cmds.getAttr("{}.useComponents".format(skin_cluster))
        self.normalize_weights   = cmds.getAttr("{}.normalizeWeights".format(skin_cluster))
        self.deform_user_normals = cmds.getAttr("{}.deformUserNormals".format(skin_cluster))
        
        return True

    def save(self, node=None, dir_path=None):
        # get selection
        if not node:
            node = cmds.ls(sl=1)
            if not node:
                cmds.error("Select Something!")
                return False
            else:
                node = node[0]
        # get skinCluster
        skin_cluster_node = mel.eval("findRelatedSkinCluster " + node)
        if not cmds.objExists(skin_cluster_node):
            return False
        # get file path
        if not dir_path:
            start_dir = cmds.workspace(q=1, rd=True)
            dir_path = cmds.fileDialog2(cap="Save skinweights", ds=2, fm=3, dir=start_dir, ff="*.npy", okc="Select")
        # file save path
        skin_cluster_node = "skin_cluster_{}".format(node)
        file_path = "{0}/{1}.npy".format(dir_path, skin_cluster_node)
        # get strat time
        time_start = time.time()
        # get data
        self.get_data(skin_cluster_node)
       
        # time end
        time_end = time.time()
        time_elapsed = time_end-time_start
        
        # construce data array
        legend = ()
        data = list()
        
        # write data
        np.save(file_path, data)
        
        return True
 
    def load(self, node=None, dir_path=None):
        # get selection
        if not node:
            node = cmds.ls(sl=1)
            if not node:
                cmds.error("Select Something!")
                return False
            else:
                node = node[0]
        # get file path
        if not dir_path:
            start_dir = cmds.workspace(q=1, rd=True)
            dir_path = cmds.fileDialog2(cap="Save skinweights", ds=2, fm=1, dir=start_dir, ff="*.npy", okc="Select")
        # file save path
        skin_cluster_node = "skin_cluster_{}".format(node)
        file_path = "{0}/{1}.npy".format(dir_path, skin_cluster_node)
        # check if skinCluster exists
        if not os.path.exists(file_path):
            cmds.error("skincluster for node not found on -- {}".format(skin_cluster_node))
            return False
        # unbind current skinCluster
        skin_cluster_node = mel.eval("findRelatedSkinCluster" + node)
        if cmds.objExists(skin_cluster_node):
            mel.eval("skinCluster -e -ub " + skin_cluster_node)
        
        # read data
        data = np.load(file_path)
        
        # bind skin
        for inf in self.inf_array:
            if not cmds.objExists(inf):
                cmds.select(cl=True)
                cmds.joint(n=inf)
        skin_cluster_node = "skin_cluster_{}".format(node)
        skin_cluster_node = cmds.skinCluster(self.inf_array, node, n=skin_cluster_node, tsb=1)[0]
        
        # set data
        self.set_data(skin_cluster_node)
        return True
     
    def set_data(self, skin_cluster):
        # get the MFnSkinCluster for skinCluster
        sel_lst = om.MSelectionList()
        sel_lst.add(skin_cluster)
        cluster_node = om.MObject()
        sel_lst.getDependNode(0, cluster_node)
        skin_fn = oma.MFnSkinCluster(cluster_node)
        
        # get components
        fn_set = om.MFnSet(skin_fn.deformerSet())
        members = om.MSelectionList()
        fn_set.getMembers(members, False)
        dag_path = om.MDagPath()
        components = om.MObject()
        members.getDagPath(0, dag_path, components)
        
        # set infs
        influence_paths = om.MDagPathArray()
        inf_count = skin_fn.influenceObjects(influence_paths)
        influence_array = [influence_paths[i].partialPathName() for i in range(influence_paths)]
        
        # change the order in set(i, i)
        influence_indices = om.MIntArray(inf_count)
        [influence_indices.set(i, i) for i in range(inf_count)]
        
        # set data
        skin_fn.setWeights(dag_path, components, influence_indices, weights_marray, False)
        skin_fn.setBlendWeights(dag_path, components, blend_weights_marray)
        
        # set attrs of skinCluster
        cmds.setAttr("{}.envelope".format(skin_cluster), self.envelop)
        cmds.setAttr("{}.skinningMethon".format(skin_cluster), self.skinning_method)
        cmds.setAttr("{}.useComponents".format(skin_cluster), self.use_components)
        cmds.setAttr("{}.normalizeWeights".format(skin_cluster), self.normalize_weights)
        cmds.setAttr("{}.deformUserNormals".format(skin_cluster), self.deform_user_normals)
        
        # name
        cmds.rename(skin_cluster, self.name)
        
        return True
           
    def compress_weight_data(self, weights_array, inf_count):
        return True
        
class SkinClusterIoJson:
    def __init__(self) -> None:
        self.CommonlyOperation = CommonlyOperation()
    
    def save(self, node=None, dir_path=None):
        if not node:
            node = cmds.ls(sl=1)
            if not node:
                cmds.error("Select Something!")
                return False
            else:
                node = node[0]
       
        skin_cluster_node = mel.eval("findRelatedSkinCluster" + node)
        if not cmds.objExists(skin_cluster_node):
            return False
        
        if not dir_path:
            start_dir = cmds.workspace(q=1, rd=True)
            dir_path = cmds.fileDialog2(cap="Save skinweights", ds=2, fm=3, dir=start_dir, okc="Select")
        # file save path
        skin_cluster_node = "skin_cluster_{}".format(node)
        file_path = "{0}/{1}".format(dir_path, skin_cluster_node)
        # get strat time
        time_start = time.time()
        # get skin weights about the current bone chain
        data = dict()
        shape_node = cmds.listRelatives(node, c=True)[0]
        vtr_array = ["{0}.vtx[{1}]".format(shape_node, v) for v in cmds.getAttr("{}.vrts".format(shape_node), mi=True)]
        for vtx in vtr_array:
            inf_array = cmds.skinPercent(skin_cluster_node, vtx, transform=None, q=1)
            weights = cmds.skinPercent(skin_cluster_node, vtx, q=1, v=1)
            data[vtx] = zip(inf_array, weights)
        
        time_end = time.time()
        time_elapsed = time_end-time_start
        
        self.CommonlyOperation.save_json_data(file_path, data)
        # with open(file_path, 'w') as fh:
        #     json.dump(data, fh, 0)
        #     # fh.close()
        
        return True

    def load(self, node=None, dir_path=None):
        if not node:
            node = cmds.ls(sl=1)
            if not node:
                cmds.error("Select Something!")
                return False
            else:
                node = node[0]
                
        if not dir_path:
            start_dir = cmds.workspace(q=1, rd=True)
            dir_path = cmds.fileDialog2(cap="Load skinweights", ds=2, fm=1, dir=start_dir, okc="Select")
        
        skin_cluster_node = "skin_cluster_{}".format(node)
        file_path = "{0}/{1}".format(dir_path, skin_cluster_node)
        
        if not os.path.exists(file_path):
            cmds.error("skincluster for node not found on -- {}".format(skin_cluster_node))
            return False

        skin_cluster_node = mel.eval("findRelatedSkinCluster" + node)
        if cmds.objExists(skin_cluster_node):
            mel.eval("skinCluster -e -ub " + skin_cluster_node)
        
        data = self.CommonlyOperation.get_json_data(file_path)
        
        inf_array = [inf[0] for inf in data[data.keys()[0]]]
        for inf in inf_array:
            if not cmds.objExists(inf):
                cmds.select(cl=1)
                cmds.joint(n=inf)
        
        skin_cluster_node = "skin_cluster_{}".format(node)
        skin_cluster_node = cmds.skinCluster(inf_array, node, n=skin_cluster_node, tsb=1)
        
        [cmds.skinPercent(skin_cluster_node, vtx, tv=data[vtx], zri=1) for vtx in data.keys()]        
        return True
