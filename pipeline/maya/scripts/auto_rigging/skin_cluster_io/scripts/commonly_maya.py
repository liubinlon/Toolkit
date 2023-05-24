#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
'''
   File    :   commonly_maya.py
   Time    :   2022/12/02 16:58:58
   Author  :   Liu ZhenBao
   Version :   1.0
   Contact :   3305510092@qq.com
   Desc    :   None
'''
############################################################################
# import the libraries needed by this script here
import os
import md5
from StringIO import StringIO
import maya.cmds as cmds
import maya.OpenMaya as om
import pymel.core as pm

# here put the class script
class CommonlyMaya:
    """
    This is maya to cgtw link functional class
    """
    @staticmethod
    def my_get_shape_node(obj):
        """
            input: 输入obj
            return: 如果有shape返回shape节点, 否则返回这个节点
        """
        shape_node = cmds.listRelatives(obj, shapes=1)
        if shape_node and len(shape_node) > 1:
            return shape_node[0]
        elif shape_node and len(shape_node) == 1:
            return shape_node
        else:
            return obj
   
    @staticmethod
    def my_get_hierarchy(obj, _type):
        """
            input: obj=, _type = 物体类型
            return: _type类型的物体列表
        """
        if _type == "joint":        
            hierarchy_node = cmds.listRelatives(obj, ad=1, type=_type)
            hierarchy_node.reverse()
        elif [mesh for mesh in cmds.listRelatives(obj, ad=1, type=_type) if "Shape" in mesh]:
            hierarchy_node = [cmds.listRelatives(mesh, p=1)[0] for mesh in cmds.listRelatives(obj, ad=1, type=_type) if "Shape" in mesh]
        else:
            hierarchy_node = [mesh for mesh in cmds.listRelatives(obj, ad=1, type=_type)]                                    
        return hierarchy_node
    
    @staticmethod
    def my_get_animation_time():
        """
            return: 当前时间区间
        """
        time_start = int(cmds.playbackOptions(query=True, min=True))
        time_end = int(cmds.playbackOptions(query=True, max=True))
        return time_start, time_end
    
    @staticmethod
    def my_get_current_fps():
        """
            return: 帧速率
        """
        format_list = {'film': 24, 'game': 15, 'pal': 25, 'ntsc': 30, 'show': 48, 'palf': 50, 'ntscf': 60}
        fpsString = cmds.currentUnit(query=True, t=True)
        try:
            return format_list[fpsString]
        except:
            return False
    
    @staticmethod
    def my_create_bon_list(parent_bon=None, _bon=None):
        """
            input: parent_bon = 父骨骼,  _bon=
            function: 递归
            return: 复制的骨骼名字
        """
        _parent_bon = cmds.duplicate(_bon, name="Anim_{}".format(_bon), po=1)
        if cmds.xform(q=1, wd=1):
            cmds.parent(_parent_bon, w=1)
        if parent_bon:
            cmds.parent(_parent_bon, parent_bon)
            children_bon = cmds.listRelatives(_bon, c=1, type="joint")
        if children_bon:
            CommonlyMaya.create_bon_list(parent_bon=_parent_bon, _bon=children_bon[0])
        return _parent_bon

    @staticmethod
    def my_rename_file(_file, file_name=None, dir_path=None, max_version=None):
        """
            input: _file = 文件绝对路径, file_name = 新的文件名, dir_path = 新路径, max_version = 版本号
            return: 带版本号文件名, 带路径文件名, 新文件名
        """
        file_name_str_list = _file.rsplit(".", 1)
        if len(file_name_str_list) > 1:
            old_file_name, extension_name = file_name_str_list
            if file_name:
                if max_version:
                    if dir_path:
                        return os.path.join(dir_path, "{0}_{1}.{2}".format(file_name, max_version,extension_name))
                    return "{0}_{1}.{2}".format(file_name, max_version, extension_name)
                elif dir_path:
                    return os.path.join(dir_path, "{0}.{1}".format(file_name, extension_name)) 
                return "{0}.{1}".format(file_name, extension_name)                             
        else:
            if file_name:
                if max_version:
                    if dir_path:
                        return os.path.join(dir_path, "{0}_{1}".format(file_name, max_version))
                    return "{0}_{1}".format(file_name, max_version)
                elif dir_path:
                    return os.path.join(dir_path, "{0}".format(file_name)) 
                return "{0}".format(file_name)

    @staticmethod
    def my_get_hierarchy_tree(_parent, _tree):
        """
            input: _parent = group, _tree = dict()       
            function: 递归, 生成字典树
        """
        geo_lst = [mesh for mesh in cmds.listRelatives(_parent, c=1) if "Shape" not in mesh]   
        if geo_lst:
            grp_lst = [grp for grp in geo_lst if cmds.nodeType(CommonlyMaya.get_shape_node(grp)) != "mesh"]
            try:
                _tree.update({_parent: {_mesh: CommonlyMaya.get_geo_points(_mesh) for _mesh in geo_lst if cmds.nodeType(CommonlyMaya.get_shape_node(_mesh)) == "mesh"}})
            except:
                _tree.update({_parent: None})
            for _grp in grp_lst:
                CommonlyMaya.get_hierarchy_tree(_grp, _tree[_parent])
        
    @staticmethod
    def my_get_geo_points(geo):
        """
            input: 输入mesh
            return: 点与面的关系
        """
        points_info = StringIO()
        geo_node = pm.PyNode(geo)
        face_id = om.MIntArray()
        iter = om.MItMeshVertex(geo_node.__apiobject__())       
        while not iter.isDone():
            iter.getConnectedFaces(face_id)
            points_info.write(str(iter.index()))
            points_info.write(" ")
            points_info.write(" ".join([str(i) for i in face_id]))
            points_info.write("\n")
            iter.next()        
        return md5.new(points_info.getvalue()).hexdigest()
    
    @staticmethod
    def my_add_attr_data(obj, attr, _data):
        """
            input: obj = 添加的物体, attr = 属性名字, _data = 属性的数据
            funtional: 添加字符串属性, 并添加参数
        """
        cmds.addAttr(obj, longName=attr, dataType="string")
        cmds.setAttr("{0}.{1}".format(obj, attr), _data, type="string")
    
    @staticmethod
    def ma_get_file_name(full_path=None, dir_path=None):
        """
            根据需求返回关于制作文件的字符串
        """
        if full_path:
            if dir_path:
                return str(pm.sceneName().dirname())
            return str(pm.sceneName().abspath())
        return str(pm.sceneName().basename())