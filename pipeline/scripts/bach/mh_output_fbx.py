#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
'''
   File    :   luonan_output_fbx.py
   Time    :   2023/04/26 16:10:02
   Author  :   Liu ZhenBao
   Version :   1.0
   Contact :   3305510092@qq.com
   Desc    :   None
'''
############################################################################
"""
import debugpy

#overwrite the default python executable
maya_location = os.path.join(os.environ.get("MAYA_LOCATION"), "bin", "mayapy.exe")
debugpy.configure({'python': maya_location})

# 5678 is the default attach port in the VS Code debug configurations. Unless a host and port are specified, host defaults to 127.0.0.1
debugpy.listen(5678)
print("Waiting for debugger attach")
debugpy.wait_for_client()
debugpy.breakpoint()
print('break on this line')

"""

# import the libraries needed by this script here
import pymel.core as pm
import maya.mel as mel
from maya import OpenMaya as om
import maya.cmds as cmds
import os

# here put the class script
class MhOutputFbx:
    def __init__(self):
        # mh表情控制器列表
        self.face_con_lst = [
            'CTRL_L_mouth_stretch',
            'CTRL_R_mouth_cornerDepress',
            'CTRL_R_mouth_lowerLipDepress',
            'CTRL_L_mouth_lowerLipDepress',
            'CTRL_L_mouth_suckBlow',
            'CTRL_R_mouth_stretch',
            'CTRL_L_mouth_cornerPull',
            'CTRL_R_mouth_sharpCornerPull',
            'CTRL_L_mouth_dimple',
            'CTRL_R_mouth_dimple',
            'CTRL_L_mouth_cornerDepress',
            'CTRL_R_mouth_cornerPull',
            'CTRL_R_nose_wrinkleUpper',
            'CTRL_L_nose_wrinkleUpper',
            'CTRL_L_mouth_upperLipRaise',
            'CTRL_R_mouth_upperLipRaise',
            'CTRL_L_mouth_sharpCornerPull',
            'CTRL_C_mouth',
            'CTRL_R_eye_lidPress',
            'CTRL_L_eye_lidPress',
            'CTRL_R_ear_up',
            'CTRL_L_nose',
            'CTRL_R_nose',
            'CTRL_L_ear_up',
            'CTRL_L_eye_blink',
            'CTRL_R_eye_cheekRaise',
            'CTRL_L_eye_pupil',
            'CTRL_R_eye_pupil',
            'CTRL_C_eye_parallelLook',
            'CTRL_R_eye_blink',
            'CTRL_R_mouth_purseD',
            'CTRL_L_mouth_purseD',
            'CTRL_L_mouth_towardsU',
            'CTRL_R_mouth_towardsU',
            'CTRL_L_mouth_towardsD',
            'CTRL_R_mouth_towardsD',
            'CTRL_L_mouth_stretchLipsClose',
            'CTRL_R_mouth_suckBlow',
            'CTRL_L_mouth_purseU',
            'CTRL_R_mouth_purseU',
            'CTRL_R_mouth_stretchLipsClose',
            'CTRL_L_brow_raiseIn',
            'CTRL_R_brow_raiseIn',
            'CTRL_R_eye_faceScrunch',
            'CTRL_C_teethD',
            'CTRL_C_teeth_fwdBackU',
            'CTRL_C_teeth_fwdBackD',
            'CTRL_C_teethU',
            'CTRL_R_mouth_lipsRollD',
            'CTRL_L_eye_faceScrunch',
            'CTRL_L_nose_nasolabialDeepen',
            'CTRL_R_nose_nasolabialDeepen',
            'CTRL_L_mouth_thicknessD',
            'CTRL_R_mouth_thicknessU',
            'CTRL_L_mouth_lipsRollU',
            'CTRL_R_mouth_lipsRollU',
            'CTRL_L_mouth_lipsRollD',
            'CTRL_R_mouth_thicknessD',
            'CTRL_L_mouth_lipsTogetherU',
            'CTRL_L_mouth_lipsTogetherD',
            'CTRL_R_mouth_lipsTogetherD',
            'CTRL_L_mouth_pressU',
            'CTRL_R_mouth_lipsTogetherU',
            'CTRL_L_mouth_funnelD',
            'CTRL_R_mouth_funnelD',
            'CTRL_L_mouth_funnelU',
            'CTRL_R_mouth_funnelU',
            'CTRL_L_mouth_lipsPressU',
            'CTRL_R_mouth_lipsPressU',
            'CTRL_R_mouth_lipsBlow',
            'CTRL_R_mouth_tightenU',
            'CTRL_L_mouth_tightenD',
            'CTRL_R_mouth_tightenD',
            'CTRL_L_mouth_tightenU',
            'CTRL_R_mouth_pressU',
            'CTRL_L_mouth_lipsBlow',
            'CTRL_L_mouth_pressD',
            'CTRL_R_mouth_pressD',
            'CTRL_R_mouth_corner',
            'CTRL_L_mouth_corner',
            'CTRL_R_eye_eyelidU',
            'CTRL_L_eye_eyelidD',
            'CTRL_R_eye_eyelidD',
            'CTRL_L_eye_eyelidU',
            'CTRL_R_mouth_lipsTowardsTeethD',
            'CTRL_L_mouth_lipsTowardsTeethD',
            'CTRL_R_eyelashes_tweakerIn',
            'CTRL_L_eyelashes_tweakerOut',
            'CTRL_R_eyelashes_tweakerOut',
            'CTRL_L_eyelashes_tweakerIn',
            'CTRL_C_mouth_lipShiftU',
            'CTRL_L_mouth_lipsTowardsTeethU',
            'CTRL_R_mouth_lipsTowardsTeethU',
            'CTRL_C_mouth_lipShiftD',
            'CTRL_faceGUIfollowHead',
            'CTRL_eyesAimFollowHead',
            'CTRL_R_mouth_cornerSharpnessU',
            'CTRL_L_mouth_cornerSharpnessU',
            'CTRL_R_mouth_cornerSharpnessD',
            'CTRL_L_mouth_thicknessU',
            'CTRL_L_mouth_cornerSharpnessD',
            'CTRL_L_mouth_pushPullU',
            'CTRL_L_mouth_pushPullD',
            'CTRL_R_mouth_pushPullD',
            'CTRL_R_mouth_pushPullU',
            'CTRL_C_eye',
            'CTRL_L_eye_squintInner',
            'CTRL_R_eye_squintInner',
            'CTRL_L_eye_cheekRaise',
            'CTRL_L_eye',
            'CTRL_R_eye',
            'CTRL_L_brow_raiseOut',
            'CTRL_R_brow_down',
            'CTRL_L_brow_lateral',
            'CTRL_R_brow_lateral',
            'CTRL_R_brow_raiseOut',
            'CTRL_L_brow_down',
            'CTRL_C_mouth_stickyU',
            'CTRL_R_mouth_stickyInnerU',
            'CTRL_L_mouth_stickyOuterU',
            'CTRL_R_mouth_stickyOuterD',
            'CTRL_R_mouth_stickyInnerD',
            'CTRL_C_mouth_stickyD',
            'CTRL_L_mouth_stickyInnerU',
            'CTRL_R_mouth_lipBiteU',
            'CTRL_L_mouth_lipBiteU',
            'CTRL_R_mouth_lipBiteD',
            'CTRL_R_mouth_stickyOuterU',
            'CTRL_L_mouth_lipBiteD',
            'CTRL_R_jaw_ChinRaiseU',
            'CTRL_L_jaw_ChinRaiseU',
            'CTRL_R_jaw_ChinRaiseD',
            'CTRL_L_jaw_chinCompress',
            'CTRL_R_jaw_chinCompress',
            'CTRL_L_jaw_ChinRaiseD',
            'CTRL_C_tongue_inOut',
            'CTRL_C_tongue_press',
            'CTRL_C_tongue_tip',
            'CTRL_C_tongue_narrowWide',
            'CTRL_C_tongue_roll',
            'CTRL_L_mouth_stickyInnerD',
            'CTRL_R_mouth_lipSticky',
            'CTRL_C_tongue',
            'CTRL_L_mouth_stickyOuterD',
            'CTRL_L_mouth_lipSticky',
            'CTRL_neck_throatUpDown',
            'CTRL_lookAtSwitch',
            'CTRL_rigLogicSwitch',
            'CTRL_R_neck_stretch',
            'CTRL_R_neck_mastoidContract',
            'CTRL_neck_digastricUpDown',
            'CTRL_neck_throatExhaleInhale',
            'CTRL_C_neck_swallow',
            'CTRL_L_neck_mastoidContract',
            'CTRL_L_jaw_clench',
            'CTRL_C_jaw',
            'CTRL_C_jaw_fwdBack',
            'CTRL_C_jaw_openExtreme',
            'CTRL_L_neck_stretch',
            'CTRL_R_jaw_clench',
            'CTRL_R_eyeAim',
            'CTRL_L_eyeAim',
            'CTRL_convergenceSwitch',
            'CTRL_C_eyesAim'
        ] 
        
    def get_file_data(self, full_path=False, dir_path=False):
        """
            获取当前文件工作路径，文件命，文件绝对路径
        Args:
            full_path (bool, optional):  True，返回当前文件绝对路径，默认False
            dir_path (bool, optional): full_path=True, dir_path=True, 返回文件所在文件夹，默认False
        Returns:
            string: 根据标签返回文件信息，默认返回带扩展的文件名
        """
        if full_path:
            if dir_path:
                return str(pm.sceneName().dirname())
            return str(pm.sceneName().abspath())
        return str(pm.sceneName().basename())
    
    def get_time_side(self):
        """
            获取当前文件的开始时间和结束时间
        Returns:
            list: time 
        """
        return [int(pm.playbackOptions(query=True, min=True)), int(pm.playbackOptions(query=True, max=True))]

    def get_file_name(self, abs_path):
        """
            获取不带扩展的文件名
        Args:
            abs_path (path): 文件的绝对路径
        Returns:
            string: 文件名
        """
        return os.path.splitext(os.path.split(abs_path)[-1])[0]
       
    def get_ref_ns(self, keywords):
        """
            查找文件里的所有引用文件，导入存在关键字的文件，删除空间命
        Args:
            keywords (string): 关键字

        Returns:
            list: 资产类型和名字
        """
        for ref in cmds.file(q=True, r=True):
            ref_node = cmds.referenceQuery(ref, referenceNode=True)
            if keywords in ref and cmds.referenceQuery(ref_node, il=True):
                name_space = cmds.referenceQuery(ref, ns=True)
                file_name = self.get_file_name(ref)
                cmds.file(ref, ir=1)
                print(name_space)
                cmds.namespace(mv=[name_space, ":"], f=1)
                cmds.namespace(rm=name_space)
                return file_name.split("_")[1:3]

    def export_fbx_file(self, fbx_file, anim=False):
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
            (startFrame, endFrame) = self.get_time_side()
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

    def out_fbx(self, ch_name="MH", anim=False):
        """
            默认导出绑定的fbx文件, 带骨骼和蒙皮模型, 输出路径为当前文件路
            anim为1输出骨骼
        Args:
            ch_name (str, optional): 检索的关键字，默认为"MH".
            anim (bool, optional): 是否导出动画fbx, 默认为False.

        Returns:
            _type_: fbx文件绝对路径列表
        """
        copy_lst = list()
        loct_path = self.get_file_data(full_path=1, dir_path=1)
        file_name, fextension = os.path.splitext(self.get_file_data())        
        if anim:
            str_lst = file_name.split("_")[0:3]
            # 导入引用文件
            ch_str = self.get_ref_ns(ch_name)
            cmds.parent("DHIbody:root", "head_grp", w=1)
            cmds.select("DHIbody:root", hi=1)
            str_lst.extend(ch_str)           
            new_file_str = "_".join(str_lst)
            body_fbx_name = "{0}/{1}_DHIbody.fbx".format(loct_path, new_file_str)
            self.export_fbx_file(body_fbx_name, anim=1)
            copy_lst.append(body_fbx_name)
            cmds.select(self.face_con_lst)
            head_fbx_name = "{0}/{1}_DHIhead.fbx".format(loct_path, new_file_str)
            self.export_fbx_file(head_fbx_name, anim=1)
            copy_lst.append(head_fbx_name)        
        else:
            cmds.parent("DHIbody:root", "Geometry", w=1)           
            cmds.delete("spine_04_drv", "thigh_r_drv", "thigh_l_drv")
            cmds.parent("DHIhead:spine_04", "spine_03_drv")            
            as_name_lst = ["root_drv", "pelvis_drv", "spine_01_drv", "spine_02_drv", "spine_03_drv"]
            bs_name_lst = ["root", "pelvis", "spine_01", "spine_02", "spine_03"]
            for index, item in enumerate(as_name_lst):
                cmds.rename(item, bs_name_lst[index])
            cmds.parent("root", w=1)
            cmds.select("DHIbody:root", hi=1)
            cmds.select("body_GeoGP", add=1)
            body_fbx_name = "{0}/{1}_DHIbody.fbx".format(loct_path, file_name)
            self.export_fbx_file(body_fbx_name)
            copy_lst.append(body_fbx_name)
            cmds.select(self.face_con_lst)
            cmds.select("root", hi=1)
            cmds.select("head_GeoGP", add=1)
            head_fbx_name = "{0}/{1}_DHIhead.fbx".format(loct_path, file_name)
            self.export_fbx_file(head_fbx_name)
            copy_lst.append(head_fbx_name)
        cmds.file("{0}/{1}".format(loct_path, self.get_file_data()), open=1, f=1)
        return copy_lst
                     
if __name__ == "__main__":
    mh_com = MhOutputFbx()
    copy_file = mh_com.out_fbx()
    print(copy_file)