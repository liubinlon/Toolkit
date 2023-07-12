#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
'''
   File    :   background_renaming_com.py
   Time    :   2023/05/26 10:46:15
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
import inspect

import maya.mel as mel
import maya.cmds as cmds
import pymel.core as pm
from maya import OpenMaya as om
import shutil
# here put the class script
abs_file = os.path.dirname(os.path.abspath(inspect.getsourcefile(lambda: 0)))

def get_time_side():
    """
        获取当前文件的开始时间和结束时间
    Returns:
        list: time 
    """
    return [int(pm.playbackOptions(query=True, min=True)), int(pm.playbackOptions(query=True, max=True))]


def export_fbx_file(fbx_file, anim=False):
    """
        设置fbx导出选项，导出fbx
    Args:
        fbx_file (string): 保存文件的绝对路径
        anim (bool, optional): True，bake动画，导出动画骨骼和控制器， 默认导出绑定fbx
    """
    mel.eval('FBXProperty Export|AdvOptGrp|AxisConvGrp|UpAxis -v "Y";')
    mel.eval('FBXExportSmoothingGroups -v true')
    mel.eval('FBXExportSmoothMesh -v true')
    mel.eval('FBXExportReferencedAssetsContent -v true')
    mel.eval('FBXExportInputConnections -v 0')
    mel.eval('FBXExportIncludeChildren  -v 1')
    if anim:
        (startFrame, endFrame) = get_time_side()
        mel.eval('FBXProperty Export|IncludeGrp|Animation -v true;')
        mel.eval('FBXProperty Export|IncludeGrp|Animation|BakeComplexAnimation -v true;')
        mel.eval('FBXProperty Export|IncludeGrp|Animation|BakeComplexAnimation|BakeFrameStart -v %s;' %startFrame)
        mel.eval('FBXProperty Export|IncludeGrp|Animation|BakeComplexAnimation|BakeFrameEnd -v %s;' %endFrame)
    else:
        mel.eval('FBXProperty Export|IncludeGrp|Animation -v false;')            
    try:
        cmds.file(fbx_file, f=True, options="v=0;", exportSelected=1, typ="FBX export", pr=True, es=True)
    except:
        pm.mel.FBXExport(f=fbx_file, s=True)
    else:
        om.MGlobal.displayError(u'存储Lamber的UE的Fbx文件异常!')

def main(check_maya_file):
    fbx_file = check_maya_file.replace(".mb", ".fbx")
    data_file = fbx_file.replace("Assets/Chars", "Data/Assets/Chars")
    fbx_data_file = data_file.replace("\\Rig", "")
    if not os.path.isfile(check_maya_file):
        logging.warning("Failed because Maya file was not found! - {}".format(check_maya_file))
    logging.info("Statr check - {}".format(check_maya_file))
    try:
        cmds.file(check_maya_file, open=True, pmt=False, force=True)
        mel_file = os.path.join(abs_file, "asExportRenameToUnreal.mel")
        mel.eval('source "%s"' % mel_file.replace("\\", "/"))
        cmds.file(save=1)
        cmds.parent("Geometry", "DeformationSystem", w=1)
        cmds.select("Geometry","DeformationSystem", hi=1)
        export_fbx_file(fbx_file)
        print("Open file succeeded")
        if os.path.isfile(fbx_data_file):
            print(fbx_data_file)
            breakup_fbx = list(os.path.split(fbx_data_file))
            breakup_fbx.insert(1, "Beakup_ADV")
            breakup_dir = os.path.join(breakup_fbx[0], breakup_fbx[1])
            if not os.path.isdir(breakup_dir):
                os.mkdir(breakup_dir)
            move_fbx = os.path.join(breakup_dir, breakup_fbx[2])
            shutil.move(fbx_data_file, move_fbx)
        shutil.copyfile(fbx_file, fbx_data_file)    
        logging.warning("Open file succeeded - {}".format(check_maya_file))
    except:
        print("Open file failed")
        logging.warning("Open file failed - {}".format(check_maya_file))

if __name__ == "__main__":
    main(sys.argv[1])