#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
'''
File    :   cmd_test.py
Time    :   2022/10/20 18:15:48
Author  :   ZhenBao Liu
Version :   1.0
Contact :   3305510092@qq.com
Desc    :   None
'''
import os, sys, time, logging, json
from collections import OrderedDict
import maya.standalone
maya.standalone.initialize(name="python")

import maya.mel as mel
import maya.cmds as cmds
import pymel.core as pm


def get_animation_time():
    time_start = int(cmds.playbackOptions(query=True, min=True))
    time_end = int(cmds.playbackOptions(query=True, max=True))
    return time_start, time_end

def get_file_name(full_path=None, dir_path=None):
    """
        根据需求返回关于制作文件的字符串
    """
    if full_path:
        if dir_path:
            return str(pm.sceneName().dirname())
        return str(pm.sceneName().abspath())
    return str(pm.sceneName().basename())

def get_check_file_name(check_file):
    return os.path.split(check_maya_file)[-1]

def get_ani_cam_name():
    lst = pm.ls(cameras=True)
    for ass in lst:
        if "ANI" in ass.name():
            return ass.getParent()

def main(check_maya_file):
    """
    """
    file_name = os.path.split(check_maya_file)[-1]
    if not os.path.isfile(check_maya_file):
        logging.warning("Failed because Maya file was not found! - {}".format(check_maya_file))
    logging.info("Statr check - {}".format(check_maya_file))
    try:
        cmds.file(check_maya_file, open=True, pmt=False, force=True)
        time_start, time_end = get_animation_time()
        logging.info("Get animation time - start:{} end:{}".format(time_start, time_end))
        dir_path = get_file_name(full_path=True, dir_path=True)
        reference_node = cmds.file(query=True, reference=True)
        for ref_file in reference_node:
            rn_node = cmds.referenceQuery(ref_file, referenceNode=True)
            name_space = cmds.referenceQuery(rn_node, namespace=True, shortName=True)    
            object_name = "{}:Geometry".format(name_space)
            if cmds.objExists(object_name):
                parent_node = cmds.listRelatives(object_name, ap=1, f=1)[0]
                parent_name = parent_node.split("|")[1]
                root_str = "{}|{}".format(parent_node, object_name)
                abc_file_name = "{}_{}".format(get_ani_cam_name(), parent_name.split(":")[-1])
                abc_path = "{}/{}.abc".format(dir_path, abc_file_name)
                cmd_str = 'AbcExport -j "-frameRange {} {} -uvWrite -worldSpace -writeVisibility -autoSubd -dataFormat ogawa -root {} -file {}";'.format(time_start, time_end, root_str, abc_path)
                mel.eval(cmd_str)
                logging.info("Ouput abc file - {}".format(abc_file_name))
                return "Finished file - {}".format(file_name) 
    except:
        logging.warning("Open file failed - {}".format(check_maya_file))
        return "Unfinished file - {}".format(file_name) 

if __name__ == "__main__":
    return_str = main(sys.argv[1])
    print(return_str)