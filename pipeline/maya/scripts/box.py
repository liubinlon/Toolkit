#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
'''
File    :   box.py
Time    :   2022/11/01 11:55:17
Author  :   ZhenBao Liu
Version :   1.0
Contact :   3305510092@qq.com
Desc    :   None
'''
# import the libraries needed by this script here
import maya.cmds as cmds
import maya.mel as mel
from itertools import product
import logging
import pymel.core as pymel
import os, time

"""
This is toolbox for used daily script collection
"""

"""
添加道具控制器
"""
def prop():
    lst = cmds.ls(sl=True)
    fix_grp = cmds.group(name="Fixed", empty=True, parent=lst[0])
    con = cmds.circle(name="Constrain", ch=False, r=2, nr=(0, 1, 0))[0]
    cmds.setAttr("{}.sx".format(con), keyable=False, lock=True)
    cmds.setAttr("{}.sz".format(con), keyable=False, lock=True)
    cmds.setAttr("{}.sy".format(con), keyable=False, lock=True)
    main = cmds.circle(name="Main", ch=False, r=1, nr=(0, 1, 0))
    mot_grp = cmds.group(name="MotionSystem", empty=True, parent=main[0])
    def_grp = cmds.group(name="DeformationSystem", empty=True, parent=main[0])
    cmds.parent(main, con)
    cmds.parent(con, lst)
"""
整理constraint
"""
def cpnstraint_parent():
    lst = cmds.ls(type=["parentConstraint", "scaleConstraint"])
    for j in lst:
        if cmds.listRelatives(j, parent=True)[0] == "Constraint":
            continue
        try:
            cmds.parent(j, "Constraint")
        except:
            cmds.group(name="Constraint", em=True, p="Fixed")
            cmds.parent(j, "Constraint")
    cmds.setAttr("Constraint.visibility", 0)
    cmds.select(clear=True)
"""
动力学添加FK控制器
"""
def hair_fk():
    lst = cmds.ls(sl=True)
    ik_list = []
    for con in lst:
        con_grp = cmds.listRelatives(con, parent=True)
        parent_node = cmds.listRelatives(con_grp, children=True, type="parentConstraint")
        cmds.delete(parent_node)
        con_jnt = list(set(cmds.listConnections(con, type="joint")))[0]
        cmds.disconnectAttr(con+".rx", con_jnt+".rx")
        cmds.disconnectAttr(con+".ry", con_jnt+".ry")
        cmds.disconnectAttr(con+".rz", con_jnt+".rz")
        cmds.parentConstraint(con, con_jnt, mo=True)
        ik_jnt = cmds.listConnections(con_jnt, source=False, type="joint")
        ik_jnt.sort(key=lambda jnt:len(jnt), reverse=True)
        ik_list.append(ik_jnt[1])
    ikEffector_node = cmds.listRelatives(ik_list[0], allDescendents=True, type="ikEffector")[0]
    ik_handle = cmds.listConnections(ikEffector_node, type="ikHandle")[0]
    curve_node = list(set(cmds.listConnections(ik_handle, type="nurbsCurve")))[0]
    curve_shape = cmds.listRelatives(curve_node, shapes=True)[0]
    info_node = cmds.createNode("curveInfo", name=curve_node+"info")
    mult_A = cmds.createNode("multiplyDivide", name=curve_node+"multA")
    cmds.setAttr(mult_A+".operation", 2)
    mult_B = cmds.createNode("multiplyDivide", name=curve_node+"multB")
    cmds.setAttr(mult_B+".operation", 2)
    cmds.connectAttr(curve_shape+".worldSpace[0]", info_node+".inputCurve")
    cmds.connectAttr(info_node+".arcLength", mult_A+".input1X")
    curve_light = cmds.getAttr(mult_A+".input1X")
    cmds.setAttr(mult_A+".input2X", curve_light)
    cmds.connectAttr(mult_A+".outputX", mult_B+".input1X")
    
    if cmds.objExists("scale_loc"):
        cmds.connectAttr("scale_loc.sx", mult_B+".input2X")
    else:
        loc_grp = cmds.group(name="scale_loc", empty=True, parent="Fixed")
        cmds.parentConstraint("Main", loc_grp, mo=False)
        cmds.scaleConstraint("Main", loc_grp, mo=False)
        cmds.connectAttr("{}.sx".format(loc_grp), mult_B+".input2X")
    
    for jnt in range(len(ik_list)):
        cmds.connectAttr(mult_B+".outputX", ik_list[jnt]+".sx")
        cmds.setAttr(lst[jnt]+".sz", keyable=True, lock=False)
        cmds.setAttr(lst[jnt]+".sy", keyable=True, lock=False)
        cmds.connectAttr(lst[jnt]+".sz", ik_list[jnt]+".sz")
        cmds.connectAttr(lst[jnt]+".sy", ik_list[jnt]+".sy")
        
    cmds.select(clear=True)
"""
解锁属性
"""
def unlock_attr():
    lst = cmds.ls(sl=True)
    for o in lst:
        cmds.setAttr("{0}.tx".format(o), lock=False)
        cmds.setAttr("{0}.ty".format(o), lock=False)
        cmds.setAttr("{0}.tz".format(o), lock=False)
        
        cmds.setAttr("{0}.rx".format(o), lock=False)
        cmds.setAttr("{0}.ry".format(o), lock=False)
        cmds.setAttr("{0}.rz".format(o), lock=False)
        
        cmds.setAttr("{0}.sx".format(o), lock=False)
        cmds.setAttr("{0}.sy".format(o), lock=False)
        cmds.setAttr("{0}.sz".format(o), lock=False)
"""
删除显示图层
"""
def delete_disply():
    layer_lst = cmds.listConnections("layerManager", source=True)
    for lay in layer_lst:
        if lay == "defaultLayer":
            continue
        else:
            cmds.delete(lay)
"""
批量copy权重
"""
def copy_skin():
    lst = cmds.ls(sl=True)
    old_mesh = [mesh for mesh in cmds.listRelatives(lst[0], allDescendents=True, typ="mesh") if "Orig" not in mesh]
    new_mesh = cmds.listRelatives(lst[1], allDescendents=True, typ="mesh")
    for old, new in product(old_mesh, new_mesh):
        if old in new:
            try:
                cmds.select(old, r=True)
                cmds.select(new, add=True)
                mel.eval("copySkinNew")
            except:
                pass
"""
清除空间名
"""
def clear_namespace():
    lst = cmds.namespaceInfo(listOnlyNamespaces=True)
    lst.remove("shared")
    lst.remove("UI")
    for str in lst:
        try:
            cmds.namespace(moveNamespace=[str, ":"], f=True)
            cmds.namespace(removeNamespace=str)
            print "delete namespace:{0}".format(str)
        except:
            pass
"""
设置骨骼显示隐藏
"""
def show_bone():
    selection = cmds.ls(sl=True)
    for each in selection:   
        if cmds.nodeType(each) == 'joint' and cmds.getAttr(each + ".drawStyle") == 0:
            cmds.setAttr(each + ".drawStyle", 2)
        else:
            cmds.setAttr(each + ".drawStyle", 0)
"""
隐藏控制器shape
"""
def unshow_shape():
    lst = cmds.ls(sl=True)
    for con in lst:
        con_grp = cmds.listRelatives(con, shapes=True)[0]   
        cmds.setAttr(con_grp+".lodVisibility", 0)
"""
delete uvset
"""
def delete_uv(lst_uv):    
    lst_uv.remove("map1")
    for uv in lst_uv:
        cmds.polyUVSet(delete=True, uvSet=uv)
        str_set.add(uv)
        
def delete_uv():
    logger = logging.getLogger(name="delete uv name")
    logger.setLevel(logging.DEBUG)

    lst_mod = cmds.ls(type="mesh")
    str_set = set()
       
    for mod in lst_mod:
        cmds.select(mod)
        uv_data = cmds.polyUVSet(allUVSets=True, q=True)
        try:
            if (len(uv_data) > 0) and ("map1" in uv_data):
                delete_uv(uv_data)
            elif len(uv_data) > 0:
                cmds.polyUVSet(rename=True, newUVSet="map1", uvSet=uv_data[0])
                new_data = cmds.polyUVSet(allUVSets=True, q=True)
                delete_uv(new_data)
            elif len(uv_data) == 1 and uv_data[0]!="map1":
                cmds.polyUVSet(rename=True, newUVSet="map1", uvSet=uv_data[0])
            else:
                pass
        except:
            pass
            
    logger.info(list(str_set))
"""
保存文件到本地    
"""
def getfilename(full_path=None, dir_path=None):
    if full_path:
        if dir_path:
            return str(pymel.sceneName().dirname())
        return str(pymel.sceneName().abspath())
    return str(pymel.sceneName().basename())

def quet_list(lst):
    print lst
    if not str(lst[-1]).isdigit():
        return lst
    lst.pop(-1)
    print lst
    return lst
    #return list(filter(lambda x: not str(x).isdigit(), lst))

def set_file_name(current, pre=None):    
    current_str = current.split("_")
    if "TEX" in current_str[-2]:
        current_str[-2] = "RIG"
    now = "_".join(current_str)
    print now
    return now

def set_path_data(_path, pre=None, fix=None):
    now_time = time.localtime()
    now_time_str = time.strftime("%Y%m%d%H%M", now_time)
    data_list = _path.split("/")
    data_list[0] = pre
    new_lst = quet_list(data_list)
    if "MOD" in new_lst[-1]: 
        new_lst[-1] = fix
    new_lst.append(now_time_str)
    new_scenename = "/".join(new_lst)
    return new_scenename  
      
def save_file():    
    old_scenename = getfilename(full_path=True, dir_path=True)
    if not old_scenename:
        cmds.error("请完成文件制作后，再次点击")
    _scenname = set_path_data(old_scenename, pre="D:", fix="RIG")
    if not os.path.isdir(_scenname):
        os.makedirs(_scenname)
    current = getfilename()
    scenname = "{0}/{1}".format(_scenname, set_file_name(current, pre=".ma")) 
    cmds.file(rename=scenname)
    cmds.file(save=True, type='mayaAscii')
"""
批量添加blend
"""
def get_geo_list(obj):
    return [mesh for mesh in cmds.listRelatives(obj, allDescendents=True, typ="mesh") if "Orig" not in mesh]

def add_blend():
    lst = cmds.ls(sl=True)
        
    old_mesh = get_geo_list(lst[0])
    new_mesh = get_geo_list(lst[1])
    
    for old, new in product(old_mesh, new_mesh):
        if old.split(":")[-1] == new.split(":")[-1]:
            old_geo = cmds.listRelatives(old, parent=True)[0]
            new_geo = cmds.listRelatives(new, parent=True)[0]
            cmds.blendShape(old_geo, new_geo, weight=[0, 1])

def list_uniq(on_list):
    return list(set(on_list))

def up_str(str):
    part = str.split("_")
    part.pop(-1)
    new_str = "_".join(part)    
    return new_str
"""
批量替换约束模型
"""
    
def get_mod_dict():
    global data_dict
    data_dict = {}
    lst = cmds.ls(sl=True)      
    for crv in lst:
        try:
            node_lst = list_uniq([up_str(node) for node in cmds.listConnections(crv) if cmds.nodeType(node) == "parentConstraint"])
            data_dict[crv] = node_lst
        except:
            pass
#解析字典，添加约束
def replace_con_mod():
    for key, value in data_dict.items():
        for v in value:
            if cmds.objExists(v):
                try:
                    cmds.parentConstraint(key, v, mo=1)
                    cmds.scaleConstraint(key, v, mo=1)
                    print key, v
                except:
                    pass

def replace_mod():
    if cmds.window('repUI',q=True,ex=True):
        cmds.deleteUI('repUI')
    cmds.windowPref("repUI", ra=True)
    my_window = cmds.window("repUI", title="替换模型", widthHeight=(200, 55), rtf=True, parent="propUI")
    cmds.columnLayout(adjustableColumn=True)
    cmds.button(label="获取控制器模型", command="get_mod_dict()")
    cmds.button(label="替换", command="replace_con_mod()")
    cmds.setParent("..")
    cmds.showWindow(my_window)
"""
This is UI for the toolbox          
"""
def make_ui():
    if cmds.window('propUI',q=True,ex=True):
        cmds.deleteUI('propUI')
    cmds.windowPref('propUI',ra=True)
    my_window = cmds.window("propUI", title="小匣子", widthHeight=(150, 20), rtf=True)
    cmds.columnLayout(adjustableColumn=True)
    cmds.button(label="道具控制器", command="prop()")
    cmds.button(label="层级整理", command="cpnstraint_parent()")
    cmds.button(label="删除多余UV", command="delete_uv()")
    cmds.button(label="hair fk", command="hair_fk()")
    cmds.button(label="解锁属性", command="unlock_attr()")
    cmds.button(label="删除显示层", command="delete_disply()")
    cmds.button(label="批量拷贝权重", command="copy_skin()")
    cmds.button(label="清除空间名", command="clear_namespace()")
    cmds.button(label="骨骼显示隐藏", command="show_bone()")
    cmds.button(label="隐藏shape", command="unshow_shape()")
    cmds.button(label="保存文件到本地", command="save_file()")
    cmds.button(label="批量添加blend", command="add_blend()")
    cmds.button(label="替换模型（约束）", command="replace_mod()")
    cmds.setParent("..")
    cmds.showWindow(my_window)
    
make_ui()