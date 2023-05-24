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

def re_abs_file(file_path_list, sp_name="fbx"):
    type_dict = {
        "abc": "Alembic",
        "fbx": "FBX",
        "ma": "mayaAscii",
        "mb": "mayaBinary"
        }
    """
    Args:
        file_path (str, path): 
        sp_name (str, optional): "abc" or "fbx".
    """
    for file_path in list(file_path_list):        
        if os.path.exists(file_path):
            logging.info(u"Reference file - {}".format(file_path))
            cmds.file(file_path, r=1, type=type_dict[sp_name], namespace=sp_name, force=1)
        else:
            continue
    import_all_reference()

def operating_namespace(clear=None):   
    lst = cmds.namespaceInfo(listOnlyNamespaces=True)
    lst.remove("shared")
    lst.remove("UI")    
    if clear:
        for str in lst:
            try:
                logging.info(u"Clear namespace - {}".format(lst))
                cmds.namespace(moveNamespace=[str, ":"], f=True)
                cmds.namespace(removeNamespace=str)
            except:
                pass
    else:
        return lst
        
def clear_extra_part():
    def_list = ['persp', 'top', 'front', 'side', 'Group']
    top_level = cmds.ls(assemblies=True)
    cmds.delete(list(set(top_level).difference(set(def_list))))

def import_all_reference():
    """
    """
    file_lst = cmds.file(q=1, reference=1)
    for _file in file_lst:
        logging.info(u"import reference file - {}".format(_file))
        cmds.file(_file, importReference=1)

def copy_skin_weights(_mesh, skin_mesh):
    """
        Args: _mesh=带蒙皮的模型， skin_mesh=需要蒙皮的模型
        Return: 需要跟随的骨骼列表

    """
    logging.info(u"Start copying weights - {}".format(_mesh))
    if pm.objExists(_mesh) and pm.objExists(skin_mesh):
        pm.delete(skin_mesh, ch=1)
        cmds.select(_mesh)
        cmds.RemoveUnusedInfluences()
        cmds.select(_mesh)
        cmds.RemoveUnusedInfluences()
        skin_node = pm.listHistory(_mesh, type="skinCluster")[0]
        joint_skin = pm.skinCluster(skin_node, query=True, inf=True)
        pm.skinCluster(joint_skin, skin_mesh, toSelectedBones=1)
        pm.copySkinWeights(_mesh, skin_mesh, noMirror=1, surfaceAssociation="closestPoint", influenceAssociation=["closestJoint", "closestBone", "oneToOne"])
        return joint_skin
    else:
        logging.info(u"Failed to copy weights - {0}>{1}".format(_mesh, skin_mesh))
        
def loc_on_mesh(_mesh, _jnt_lst, point_word=False):
    """
        Args:
            _mesh: 跟随的模型
            _jnt_lst: 需要跟随的骨骼列表
    """
    logging.info(u"Create positioning follicles - {}".format(_mesh))
    for jnt in _jnt_lst:           
        if not cmds.objExists("loc_hair_GP"):
            loc_grp = pm.group(em=1, name="loc_hair_GP")
            pm.setAttr("{}.v".format(loc_grp), 0)
            pm.parent(loc_grp, "Group")
        #abs_mesh = pm.PyNode(_mesh)
        #shape_node = abs_mesh.getShape()
        shape_node = pm.PyNode(_mesh)
        po_node = pm.createNode("closestPointOnMesh", name="{}_point_on_mesh".format(jnt))
        pm.connectAttr("{}.outMesh".format(shape_node), "{}.inMesh".format(po_node))
        pm.select(clear=1)
        loc_jnt = pm.joint(name="loc_jnt")
        if point_word:
            vertex_world = get_closest_vertex(jnt, _mesh)
            pm.xform(loc_jnt, translation=vertex_world)
        else:
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
        pm.parentConstraint(tra_node, jnt, mo=1)

def tidy_file(cloth_joint=None):
    logging.info(u"Organize files - {}".format(">^_^<"))
    if cloth_joint:
        if not pm.objExists("cloth_root"):
            pm.parent(cloth_joint, "fbx:root")
            pm.rename("fbx:root", "cloth_root")
            pm.setAttr("cloth_root.visibility", 0)
            pm.parent("cloth_root", "DeformationSystem")
        elif pm.objExists("cloth_root"):
             pm.parent(cloth_joint, "cloth_root")
    operating_namespace(clear=True)
    clear_extra_part()

def get_closest_vertex(joint, mesh):
    joint_position = cmds.xform(joint, query=True, translation=True, worldSpace=True)
    vertices = cmds.ls('%s.vtx[*]' % mesh, flatten=True)
    min_distance = sys.float_info.max

    for vertex in vertices:
        vertex_position = cmds.pointPosition(vertex, world=True)
        distance = (
            (joint_position[0] - vertex_position[0]) ** 2 +
            (joint_position[1] - vertex_position[1]) ** 2 +
            (joint_position[2] - vertex_position[2]) ** 2
        ) ** 0.5

        if distance < min_distance:
            min_distance = distance
            vertex_world = vertex_position
    return vertex_world
    
def get_con_jnt():
    zore_hair = [hair for hair in cmds.listRelatives("loc_hair_GP") if cmds.xform(hair, query=True, translation=True, worldSpace=True) == [0, 0, 0]]
    if zore_hair:        
        jnt_lst = list()
        for foll in zore_hair:
            parent_node = list(set(cmds.listConnections(foll, type="parentConstraint")))[0]
            jnt_lst.append(list(set(cmds.listConnections(parent_node, type="joint")))[0])
        cmds.delete(zore_hair)
        return jnt_lst

def get_recent_point(mesh):
    jnt_lst = get_con_jnt()
    if jnt_lst:
        loc_on_mesh(mesh, jnt_lst, point_word=True)

def get_exists_model(_model):
    """_summary_
    """
    _model += "Shape"
    namespace_lst = operating_namespace()
    for space in namespace_lst:    
        if cmds.objExists("{0}:{1}".format(space, _model)):  
            return "{0}:{1}".format(space, _model)

def main(check_maya_file, fbx_list):
    if not os.path.isfile(check_maya_file):
        logging.warning("Failed because Maya file was not found! - {}".format(check_maya_file))
    logging.info(u"Start operation - {}".format(check_maya_file))
    try:
        cmds.file(check_maya_file, open=True, pmt=False, force=True)
        if fbx_list:
            re_abs_file(fbx_list)
        import_all_reference()
        cloth_joint = list()
        cfx_geo_lst = [_geo for _geo in cmds.listRelatives("CFX_TEMP", ad=1, type="mesh") if "Orig" not in _geo]
        for _geo in cfx_geo_lst:
            trasm_node = cmds.listRelatives(_geo, parent=True)[0]
            str_lst = trasm_node.split("_")
            # 检索渲染模型
            remove_lst = ["CfxTemp", "cfx", "mod"]
            str_lst = list(set(str_lst).difference(set(remove_lst)))
            str_lst.append("Geo")
            render_model = "_".join(str_lst)
            # 复制权重
            if get_exists_model(trasm_node):
                joint_lst = copy_skin_weights(get_exists_model(trasm_node), render_model)
                print(joint_lst)
                if joint_lst: 
                    cloth_joint.extend(joint_lst)
                    # 创建毛囊定位
                    loc_on_mesh(_geo, joint_lst)
                    get_recent_point(_geo)    
        tidy_file(cloth_joint)
        cmds.file(save=1)
        logging.info(u"Finish - {}".format(">>^_^<<"))
    except:
        logging.info(u"Execution error - {}".format(check_maya_file))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])