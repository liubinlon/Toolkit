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
        self.remove_joint_list = [
            "upperarm_twistCor_01", 
            "thumb_03_side_inn", 
            "index_01_palm", 
            "middle_03_in", 
            "pinky_01_mcp", 
            "wrist_outer", 
            "thumb_03_side_out", 
            "thigh_bck", 
            "pinky_02_bulge", 
            "clavicle_scap", 
            "lowerarm_in", 
            "pinky_02_in", 
            "lowerarm_out", 
            "index_03_in", 
            "upperarm_tricep", 
            "ring_03_bulge", 
            "clavicle_pec", 
            "upperarm_in", 
            "lowerarm_fwd", 
            "middle_02_side_inn", 
            "upperarm_out", 
            "index_metacarpal_slide", 
            "ring_02_dip", 
            "index_01_mcp", 
            "thigh_twistCor_02", 
            "ring_02_bulge", 
            "thigh_twistCor_01", 
            "middle_01_palm", 
            "middle_02_in", 
            "index_02_bulge", 
            "ankle_bck", 
            "index_01_side_inn", 
            "index_01_bulge", 
            "spine_04_latissimus", 
            "pinky_01_bulge", 
            "pinky_01_side_inn", 
            "pinky_01_palm", 
            "middle_01_bulge", 
            "index_02_in", 
            "thigh_fwd_lwr", 
            "pinky_02_dip", 
            "ring_01_bulge", 
            "middle_03_bulge", 
            "calf_kneeBack", 
            "ring_01_side_out", 
            "index_01_palmMid", 
            "ring_01_mcp", 
            "ring_02_side_inn", 
            "clavicle_out", 
            "thumb_03_bulge", 
            "pinky_02_pip", 
            "pinky_02_side_inn", 
            "upperarm_bck", 
            "thumb_02_bulge", 
            "ring_03_in", 
            "thumb_02_side_inn", 
            "index_02_dip", 
            "thigh_out", 
            "pinky_02_side_out", 
            "ring_02_pip", 
            "thigh_bck_lwr", 
            "calf_twistCor_02", 
            "middle_01_palmMid", 
            "middle_02_bulge", 
            "ring_metacarpal_slide", 
            "thumb_02_side_out", 
            "thumb_02_in", 
            "ring_01_palm", 
            "thumb_01_side_out", 
            "thumb_01_side_inn", 
            "calf_knee", 
            "ring_01_palmMid", 
            "ring_02_side_out", 
            "ring_02_in", 
            "middle_01_side_out", 
            "middle_01_side_inn", 
            "lowerarm_bck", 
            "pinky_03_in", 
            "index_02_side_out", 
            "ring_01_side_inn", 
            "middle_02_pip", 
            "thumb_02_mcp", 
            "pinky_03_bulge", 
            "wrist_inner", 
            "thigh_in", 
            "thigh_fwd", 
            "pinky_01_palmMid", 
            "middle_01_mcp", 
            "middle_02_dip", 
            "index_02_side_inn", 
            "middle_02_side_out", 
            "ankle_fwd", 
            "index_02_pip", 
            "index_01_side_out", 
            "middle_metacarpal_slide", 
            "pinky_metacarpal_slide", 
            "pinky_01_side_out", 
            "thumb_03_pip", 
            "upperarm_bicep", 
            "thumb_03_in", 
            "upperarm_fwd", 
            "index_03_bulge"
        ]
        self.zb_default_joint = [
            "root", 
            "pelvis", 
            "spine_01", 
            "spine_02", 
            "spine_03", 
            "spine_04", 
            "spine_05", 
            "neck_01", 
            "neck_02", 
            "head", 
            "FACIAL_C_Neck2Root", 
            "FACIAL_L_12IPV_NeckBackA1", 
            "FACIAL_L_12IPV_NeckBackA2", 
            "FACIAL_C_12IPV_AdamsA2", 
            "FACIAL_C_12IPV_AdamsA1", 
            "FACIAL_R_NeckBackA", 
            "FACIAL_L_12IPV_NeckA5", 
            "FACIAL_R_12IPV_NeckA2", 
            "FACIAL_R_12IPV_NeckA3", 
            "FACIAL_R_12IPV_NeckA1", 
            "FACIAL_R_12IPV_NeckA6", 
            "FACIAL_R_12IPV_NeckA4", 
            "FACIAL_R_12IPV_NeckA5", 
            "FACIAL_L_NeckBackA", 
            "FACIAL_C_NeckBackA", 
            "FACIAL_C_12IPV_NeckBackA1", 
            "FACIAL_C_12IPV_NeckBackA2", 
            "FACIAL_R_12IPV_NeckBackA2", 
            "FACIAL_R_12IPV_NeckBackA1", 
            "FACIAL_L_12IPV_NeckA4", 
            "FACIAL_L_12IPV_NeckA6", 
            "FACIAL_L_12IPV_NeckA1", 
            "FACIAL_L_12IPV_NeckA2", 
            "FACIAL_L_12IPV_NeckA3", 
            "FACIAL_C_AdamsApple", 
            "FACIAL_L_NeckA1", 
            "FACIAL_L_NeckA3", 
            "FACIAL_L_NeckA2", 
            "FACIAL_R_NeckA3", 
            "FACIAL_R_NeckA2", 
            "FACIAL_R_NeckA1", 
            "FACIAL_C_Neck1Root", 
            "FACIAL_L_12IPV_NeckB5", 
            "FACIAL_L_12IPV_NeckB4", 
            "FACIAL_L_12IPV_NeckB7", 
            "FACIAL_L_12IPV_NeckB6", 
            "FACIAL_L_12IPV_NeckB3", 
            "FACIAL_R_12IPV_NeckB6", 
            "FACIAL_R_12IPV_NeckB4", 
            "FACIAL_R_NeckBackB", 
            "FACIAL_C_12IPV_NeckB1", 
            "FACIAL_C_12IPV_NeckB2", 
            "FACIAL_R_12IPV_NeckB5", 
            "FACIAL_R_12IPV_NeckBackB2", 
            "FACIAL_R_12IPV_NeckBackB1", 
            "FACIAL_L_NeckBackB", 
            "FACIAL_C_NeckBackB", 
            "FACIAL_L_NeckB1", 
            "FACIAL_L_NeckB2", 
            "FACIAL_R_NeckB2", 
            "FACIAL_R_NeckB1", 
            "FACIAL_R_12IPV_NeckB7", 
            "FACIAL_R_12IPV_NeckB3", 
            "FACIAL_L_12IPV_NeckBackB1", 
            "FACIAL_L_12IPV_NeckBackB2", 
            "FACIAL_C_12IPV_NeckBackB1", 
            "FACIAL_C_12IPV_NeckBackB2", 
            "FACIAL_C_NeckB", 
            "clavicle_l", 
            "upperarm_l", 
            "upperarm_correctiveRoot_l", 
            "upperarm_bck_l", 
            "upperarm_fwd_l", 
            "upperarm_in_l", 
            "upperarm_out_l", 
            "lowerarm_l", 
            "hand_l", 
            "pinky_metacarpal_l", 
            "pinky_01_l", 
            "pinky_02_l", 
            "pinky_03_l", 
            "pinky_03_bulge_l", 
            "pinky_03_half_l", 
            "pinky_03_in_l", 
            "pinky_02_dip_l", 
            "pinky_02_bulge_l", 
            "pinky_02_side_out_l", 
            "pinky_02_side_inn_l", 
            "pinky_02_half_l", 
            "pinky_02_in_l", 
            "pinky_02_pip_l", 
            "pinky_01_palmMid_l", 
            "pinky_01_bulge_l", 
            "pinky_01_side_out_l", 
            "pinky_01_side_inn_l", 
            "pinky_01_half_l", 
            "pinky_01_mcp_l", 
            "pinky_01_palm_l", 
            "pinky_metacarpal_slide_l", 
            "ring_metacarpal_l", 
            "ring_01_l", 
            "ring_02_l", 
            "ring_03_l", 
            "ring_03_bulge_l", 
            "ring_03_half_l", 
            "ring_02_dip_l", 
            "ring_03_in_l", 
            "ring_02_bulge_l", 
            "ring_02_side_out_l", 
            "ring_02_side_inn_l", 
            "ring_02_half_l", 
            "ring_02_in_l", 
            "ring_02_pip_l", 
            "ring_01_palmMid_l", 
            "ring_01_bulge_l", 
            "ring_01_side_out_l", 
            "ring_01_side_inn_l", 
            "ring_01_half_l", 
            "ring_01_mcp_l", 
            "ring_01_palm_l", 
            "ring_metacarpal_slide_l", 
            "thumb_01_l", 
            "thumb_02_l", 
            "thumb_03_l", 
            "thumb_03_bulge_l", 
            "thumb_03_side_out_l", 
            "thumb_03_side_inn_l", 
            "thumb_03_half_l", 
            "thumb_03_pip_l", 
            "thumb_03_in_l", 
            "thumb_02_bulge_l", 
            "thumb_02_side_out_l", 
            "thumb_02_side_inn_l", 
            "thumb_02_half_l", 
            "thumb_02_in_l", 
            "thumb_02_mcp_l", 
            "thumb_01_side_out_l", 
            "thumb_01_side_inn_l", 
            "middle_metacarpal_l", 
            "middle_01_l", 
            "middle_02_l", 
            "middle_03_l", 
            "middle_03_bulge_l", 
            "middle_03_half_l", 
            "middle_03_in_l", 
            "middle_02_dip_l", 
            "middle_02_bulge_l", 
            "middle_02_side_out_l", 
            "middle_02_side_inn_l", 
            "middle_02_half_l", 
            "middle_02_pip_l", 
            "middle_02_in_l", 
            "middle_01_palmMid_l", 
            "middle_01_bulge_l", 
            "middle_01_side_out_l", 
            "middle_01_side_inn_l", 
            "middle_01_half_l", 
            "middle_01_mcp_l", 
            "middle_01_palm_l", 
            "middle_metacarpal_slide_l", 
            "index_metacarpal_l", 
            "index_01_l", 
            "index_02_l", 
            "index_03_l", 
            "index_03_bulge_l", 
            "index_03_half_l", 
            "index_02_dip_l", 
            "index_03_in_l", 
            "index_02_bulge_l", 
            "index_02_side_out_l", 
            "index_02_side_inn_l", 
            "index_02_half_l", 
            "index_02_in_l", 
            "index_02_pip_l", 
            "index_01_palmMid_l", 
            "index_01_bulge_l", 
            "index_01_side_out_l", 
            "index_01_side_inn_l", 
            "index_01_half_l", 
            "index_01_mcp_l", 
            "index_01_palm_l", 
            "index_metacarpal_slide_l", 
            "wrist_inner_l", 
            "wrist_outer_l", 
            "lowerarm_twist_02_l", 
            "lowerarm_twist_01_l", 
            "lowerarm_correctiveRoot_l", 
            "lowerarm_in_l", 
            "lowerarm_out_l", 
            "lowerarm_fwd_l", 
            "lowerarm_bck_l", 
            "upperarm_twist_01_l", 
            "upperarm_twistCor_01_l", 
            "upperarm_twist_02_l", 
            "upperarm_tricep_l", 
            "upperarm_bicep_l", 
            "upperarm_twistCor_02_l", 
            "clavicle_out_l", 
            "clavicle_scap_l", 
            "clavicle_r", 
            "upperarm_r", 
            "upperarm_correctiveRoot_r", 
            "upperarm_bck_r", 
            "upperarm_in_r", 
            "upperarm_fwd_r", 
            "upperarm_out_r", 
            "lowerarm_r", 
            "hand_r", 
            "pinky_metacarpal_r", 
            "pinky_01_r", 
            "pinky_02_r", 
            "pinky_03_r", 
            "pinky_03_bulge_r", 
            "pinky_03_half_r", 
            "pinky_03_in_r", 
            "pinky_02_dip_r", 
            "pinky_02_bulge_r", 
            "pinky_02_side_out_r", 
            "pinky_02_side_inn_r", 
            "pinky_02_half_r", 
            "pinky_02_in_r", 
            "pinky_02_pip_r", 
            "pinky_01_palmMid_r", 
            "pinky_01_bulge_r", 
            "pinky_01_side_out_r", 
            "pinky_01_side_inn_r", 
            "pinky_01_half_r", 
            "pinky_01_mcp_r", 
            "pinky_01_palm_r", 
            "pinky_metacarpal_slide_r", 
            "ring_metacarpal_r", 
            "ring_01_r", 
            "ring_02_r", 
            "ring_03_r", 
            "ring_03_bulge_r", 
            "ring_03_half_r", 
            "ring_02_dip_r", 
            "ring_03_in_r", 
            "ring_02_bulge_r", 
            "ring_02_side_out_r", 
            "ring_02_side_inn_r", 
            "ring_02_half_r", 
            "ring_02_in_r", 
            "ring_02_pip_r", 
            "ring_01_palmMid_r", 
            "ring_01_bulge_r", 
            "ring_01_side_out_r", 
            "ring_01_side_inn_r", 
            "ring_01_half_r", 
            "ring_01_mcp_r", 
            "ring_01_palm_r", 
            "ring_metacarpal_slide_r", 
            "thumb_01_r", 
            "thumb_02_r", 
            "thumb_03_r", 
            "thumb_03_bulge_r", 
            "thumb_03_side_out_r", 
            "thumb_03_side_inn_r", 
            "thumb_03_half_r", 
            "thumb_03_pip_r", 
            "thumb_03_in_r", 
            "thumb_02_bulge_r", 
            "thumb_02_side_out_r", 
            "thumb_02_side_inn_r", 
            "thumb_02_half_r", 
            "thumb_02_in_r", 
            "thumb_02_mcp_r", 
            "thumb_01_side_out_r", 
            "thumb_01_side_inn_r", 
            "middle_metacarpal_r", 
            "middle_01_r", 
            "middle_02_r", 
            "middle_03_r", 
            "middle_03_bulge_r", 
            "middle_03_half_r", 
            "middle_03_in_r", 
            "middle_02_dip_r", 
            "middle_02_bulge_r", 
            "middle_02_side_out_r", 
            "middle_02_side_inn_r", 
            "middle_02_half_r", 
            "middle_02_pip_r", 
            "middle_02_in_r", 
            "middle_01_palmMid_r", 
            "middle_01_bulge_r", 
            "middle_01_side_out_r", 
            "middle_01_side_inn_r", 
            "middle_01_half_r", 
            "middle_01_mcp_r", 
            "middle_01_palm_r", 
            "middle_metacarpal_slide_r", 
            "index_metacarpal_r", 
            "index_01_r", 
            "index_02_r", 
            "index_03_r", 
            "index_03_bulge_r", 
            "index_03_half_r", 
            "index_02_dip_r", 
            "index_03_in_r", 
            "index_02_bulge_r", 
            "index_02_side_out_r", 
            "index_02_side_inn_r", 
            "index_02_half_r", 
            "index_02_in_r", 
            "index_02_pip_r", 
            "index_01_palmMid_r", 
            "index_01_bulge_r", 
            "index_01_side_out_r", 
            "index_01_side_inn_r", 
            "index_01_half_r", 
            "index_01_mcp_r", 
            "index_01_palm_r", 
            "index_metacarpal_slide_r", 
            "wrist_inner_r", 
            "wrist_outer_r", 
            "lowerarm_twist_02_r", 
            "lowerarm_twist_01_r", 
            "lowerarm_correctiveRoot_r", 
            "lowerarm_out_r", 
            "lowerarm_in_r", 
            "lowerarm_fwd_r", 
            "lowerarm_bck_r", 
            "upperarm_twist_01_r", 
            "upperarm_twistCor_01_r", 
            "upperarm_twist_02_r", 
            "upperarm_tricep_r", 
            "upperarm_bicep_r", 
            "upperarm_twistCor_02_r", 
            "clavicle_out_r", 
            "clavicle_scap_r", 
            "clavicle_pec_r", 
            "spine_04_latissimus_l", 
            "spine_04_latissimus_r", 
            "clavicle_pec_l", 
            "thigh_r", 
            "calf_r", 
            "foot_r", 
            "ball_r", 
            "littletoe_01_r", 
            "littletoe_02_r", 
            "ringtoe_01_r", 
            "ringtoe_02_r", 
            "middletoe_01_r", 
            "middletoe_02_r", 
            "bigtoe_01_r", 
            "bigtoe_02_r", 
            "indextoe_01_r", 
            "indextoe_02_r", 
            "ankle_bck_r", 
            "ankle_fwd_r", 
            "calf_twist_02_r", 
            "calf_twistCor_02_r", 
            "calf_twist_01_r", 
            "calf_correctiveRoot_r", 
            "calf_kneeBack_r", 
            "calf_knee_r", 
            "thigh_twist_01_r", 
            "thigh_twistCor_01_r", 
            "thigh_twist_02_r", 
            "thigh_twistCor_02_r", 
            "thigh_correctiveRoot_r", 
            "thigh_fwd_r", 
            "thigh_bck_r", 
            "thigh_out_r", 
            "thigh_in_r", 
            "thigh_bck_lwr_r", 
            "thigh_fwd_lwr_r", 
            "thigh_l", 
            "calf_l", 
            "foot_l", 
            "ball_l", 
            "indextoe_01_l", 
            "indextoe_02_l", 
            "bigtoe_01_l", 
            "bigtoe_02_l", 
            "littletoe_01_l", 
            "littletoe_02_l", 
            "middletoe_01_l", 
            "middletoe_02_l", 
            "ringtoe_01_l", 
            "ringtoe_02_l", 
            "ankle_bck_l", 
            "ankle_fwd_l", 
            "calf_twist_02_l", 
            "calf_twistCor_02_l", 
            "calf_twist_01_l", 
            "calf_correctiveRoot_l", 
            "calf_kneeBack_l", 
            "calf_knee_l", 
            "thigh_twist_01_l", 
            "thigh_twistCor_01_l", 
            "thigh_twist_02_l", 
            "thigh_twistCor_02_l", 
            "thigh_correctiveRoot_l", 
            "thigh_bck_l", 
            "thigh_fwd_l", 
            "thigh_out_l", 
            "thigh_bck_lwr_l", 
            "thigh_in_l", 
            "thigh_fwd_lwr_l"
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
       
    def edit_ns(self, remove_space=None, add_space=None):
        """
        添加和删除指定的空间命
        Args:
            remove_space (string): 移除的空间命. Defaults to None.
            add_space (string): _description_. Defaults to None.
        """
        if remove_space:
            cmds.namespace(mv=[remove_space, ":"], f=1)
            cmds.namespace(rm=remove_space)
        if add_space:
            cmds.namespace(set=":")
            cmds.namespace(add=add_space)
            
    def get_except_joint(self, root_joint=None):
        """
        移除MH骨骼列表的修型骨骼

        Args:
            root_joint (joint): 根骨骼

        Returns:
            list: 需要bake动画的骨骼列表
        """
        if root_joint:
            return [jnt for jnt in cmds.ls(root_joint, dag=1, ni=1, type="joint") if jnt.split(":")[-1].replace("_r", "").replace("_l", "") not in self.remove_joint_list]

    def zb_other_joint(self, name_space=None):
        if name_space:
            zb_name_space = name_space.replace("MH", "MHZB").replace("Chars", "Props")
            zb_root = "{}:root".format(zb_name_space)
            if cmds.objExists(zb_root):
                other_joint = [jnt.split(":")[-1] for jnt in cmds.ls(zb_root, dag=1, ni=1, type="joint")]
                other_joint = list(set(other_joint).difference(set(self.zb_default_joint)))
                for jnt in other_joint:
                    cmds.parentConstraint("{0}:{1}".format(zb_name_space, jnt), "{0}:{1}".format(name_space, jnt), mo=0)
    
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
            mel.eval('FBXProperty Export|IncludeGrp|Animation -v true;')    
            (startFrame, endFrame) = self.get_time_side() 
            # mel.eval('FBXProperty Export|IncludeGrp|Animation -v true;')
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
            
    def make_bake_results(self, joint_lst, min_frame, max_frame):
        
        cmds.bakeResults(joint_lst,  
                         t=(min_frame-5, max_frame+5),
                         simulation = 1,
                         sampleBy=1,
                         oversamplingRate =1,
                         disableImplicitControl=1,
                         preserveOutsideKeys=1,
                         sparseAnimCurveBake=0,
                         removeBakedAttributeFromLayer=0,
                         removeBakedAnimFromLayer = 0,
                         bakeOnOverrideLayer=0,
                         minimizeRotation = 1,
                         controlPoints=0,
                         shape=1
                         )
    
    def delete_constraint(self, root_joint):
        cmds.delete(cmds.ls(root_joint, 
                            dag=1,
                            type=["parentConstraint", 
                            "scaleConstraint", 
                            "pointConstraint",
                            "orientConstraint"]))

    def out_fbx(self, anim=False):
        """
            默认导出绑定的fbx文件, 带骨骼和蒙皮模型, 输出路径为当前文件路
            anim为1输出骨骼
        Args:
            anim (bool, optional): 是否导出动画fbx, 默认为False.
        Returns:
            _type_: fbx文件绝对路径列表
        """
        body_root = "DHIbody:root"
        copy_lst = list()
        loct_path = self.get_file_data(full_path=1, dir_path=1)
        file_name, fextension = os.path.splitext(self.get_file_data())
        if anim:
            if not cmds.ls("*:DHIbody:root"):
                return copy_lst
            min_frame, max_frame = self.get_time_side()
            for dhi in cmds.ls('*:DHIbody:root'):
                name_space = dhi.split(":")[0]
                newNameSpace = '_'.join(name_space.split("_")[1::])
                self.zb_other_joint(name_space)
                self.edit_ns(remove_space=name_space)
                str_lst = file_name.split("_")[0:3]
                new_file_name = "_".join(str_lst)
                cmds.parent(body_root, "head_grp", w=1)
                # body_joint = self.get_except_joint(body_root)
                # self.make_bake_results(body_joint, min_frame, max_frame)
                # cmds.currentTime(min_frame-5)
                # self.delete_constraint(body_root)
                cmds.select(body_root)
                body_fbx_name = "{0}/{1}_{2}_DHIbody.fbx".format(loct_path, new_file_name, newNameSpace)
                self.export_fbx_file(body_fbx_name, anim=1)
                copy_lst.append(body_fbx_name)
                cmds.select(self.face_con_lst)
                head_fbx_name = "{0}/{1}_{2}_DHIhead.fbx".format(loct_path, new_file_name, newNameSpace)
                self.export_fbx_file(head_fbx_name, anim=1)
                copy_lst.append(head_fbx_name)
                cmds.parent(body_root, "head_grp", "Group")
                self.edit_ns(add_space=name_space)
                for obj in cmds.ls("Group", dag=1, ni=1):
                    if cmds.objExists(obj):
                        cmds.rename(obj, ":{0}:{1}".format(name_space, obj))
                if cmds.namespace(exists="DHIbody"):
                    self.edit_ns(remove_space="DHIbody")
                if cmds.namespace(exists="DHIhead"):
                    self.edit_ns(remove_space="DHIhead")
        else:
            if not cmds.ls("*DHIbody:root"):
                return copy_lst
            self.delete_constraint(body_root)
            self.delete_constraint("DHIhead:spine_04")
            cmds.parent(body_root, "Geometry", w=1)           
            cmds.delete("spine_04_drv", "thigh_r_drv", "thigh_l_drv")
            cmds.parent("DHIhead:spine_04", "spine_03_drv")            
            as_name_lst = ["root_drv", "pelvis_drv", "spine_01_drv", "spine_02_drv", "spine_03_drv"]
            bs_name_lst = ["root", "pelvis", "spine_01", "spine_02", "spine_03"]
            for index, item in enumerate(as_name_lst):
                cmds.rename(item, bs_name_lst[index])
            cmds.parent("root", w=1)
            cmds.select(body_root, hi=1)
            cmds.select("body_GeoGP", add=1)
            body_fbx_name = "{0}/{1}_DHIbody.fbx".format(loct_path, file_name)
            self.export_fbx_file(body_fbx_name)
            copy_lst.append(body_fbx_name)
            # cmds.select(self.face_con_lst)
            cmds.select("root", hi=1)
            cmds.select("head_GeoGP", add=1)
            head_fbx_name = "{0}/{1}_DHIhead.fbx".format(loct_path, file_name)
            self.export_fbx_file(head_fbx_name)
            copy_lst.append(head_fbx_name)
            cmds.file("{0}/{1}".format(loct_path, self.get_file_data()), open=1, f=1)
        return copy_lst
                     
if __name__ == "__main__":
    mh_com = MhOutputFbx()
    copy_file = mh_com.out_fbx(anim=1)
    print(copy_file)