#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
   File    :   add_adv_control.py
   Time    :   2023/08/25 16:11:45
   Author  :   Liu ZhenBao
   Version :   1.0
   Contact :   3305510092@qq.com
   Desc    :   None
'''
############################################################################

# import the libraries needed by this script here

import maya.cmds as cmds
import maya.mel as mel
import os, sys, inspect
script_location = 
if sys.path():
   pass

# here put the funciton script
def add_adv_control():
   scale = cmds.getAttr("FaceFitSkeleton.faceScale")
   adv_file = r'{}/asToMetaHuman.ma'.format(script_location)
   hide_objs = [
      "ctrlBoxOffset", 
      "ctrlBox2Offset", 
      "EyeBrowRegion1_RShape", 
      "EyeBrowRegion1_LShape",
      "EyeRegion1_RShape", 
      "EyeRegion1_LShape", 
      "Eye1_RShape", 
      "Eye1_LShape", 
      "NoseRegion1_MShape", 
      "LipRegion1_MShape",
      "upperFace1_MShape", 
      "middleFace1_MShape", 
      "lowerFace1_MShape", 
      "upperTeeth1_MShape", 
      "lowerTeeth1_MShape",
      "Tongue11_MShape", 
      "Tongue21_MShape",
      "Tongue31_MShape"
      ]
   
   # 导入adv面部控制器      
   if cmds.file(adv_file, q=1, ex=1):
      cmds.error(u'文件:"{}" 没有找到'.format(adv_file))
   # 删除场景中的mehahuman_contorl_toggle控制器    
   if cmds.objExists("GRP_faceGUI"):
      cmds.delete("GRP_faceGUI", "adv_contorl_toggle")
      return
   
   cmds.circle(n="adv_contorl_toggle", c=(0, 0, 0), nr=(0, 0, 1), sw=360, r=scale/30.0, d=3, ut=0, tol=0.000393701, s=8, ch=0)
   cmds.rotate(0, 0, 110, "adv_contorl_toggle.cv[1]", "adv_contorl_toggle.cv[3]", "adv_contorl_toggle.cv[5]", "adv_contorl_toggle.cv[7]", r=1, p=(0, 0, 0), os=True)
   cmds.rotate(0, 0, 11.7, "adv_contorl_toggle.cv[0:99]", r=1, p=(0, 0, 0), os=1)
   cmds.setAttr("adv_contorl_toggle.overrideEnabled", 1)
   cmds.setAttr("adv_contorl_toggle.overrideColor", 13)
   pos1 = cmds.xform("ctrlBoxShape.cv[3]", q=True, ws=True, t=True)
   cmds.xform("adv_contorl_toggle", ws=1, t=(pos1[0], pos1[1], pos1[2]))
   cmds.parent("adv_contorl_toggle", "ControlsSetup")
   cmds.lock_attr("adv_contorl_toggle", 1, 1, 1, 1)
   cmds.addAttr("adv_contorl_toggle", k=1, ln="MetaHumanControlPanelVis", at="bool", dv=1)
   cmds.createNode("reverse", n="MetaHumanControlPanelVisReverse")
   cmds.connectAttr("adv_contorl_toggle.MetaHumanControlPanelVis", "MetaHumanControlPanelVisReverse.inputX")
   for index, _obj in enumerate(hide_objs):
      if cmds.objExists(_obj):
         cmds.connectAttr("MetaHumanControlPanelVisReverse.outputX", "{}.v".format(_obj))
   
   cmds.file(adv_file, rpr="as_import", i=1)
   print("GRP_faceGUI", "ControlsSetup")
   cmds.connectAttr("adv_contorl_toggle.MetaHumanControlPanelVis", "GRP_faceGUI.v")
   cmds.as_align("GRP_faceGUI", "ctrlBox", 1, 0, 0, 0)
   cmds.as_align("FRM_faceGUI", "ctrlBox", 1, 0, 0, 0)
   
   pos1 = cmds.xform("ctrlBoxShape.cv[1]", q=1, ws=1, t=1)
   pos2 = cmds.xform("ctrlBoxShape.cv[3]", q=1, ws=1, t=1)
   s = (pos1[1],-pos2[1])/32.0
   cmds.setAttr("FRM_faceGUI.s", s, s, s, type="float3")
   cmds.setAttr("GRP_faceGUI.tx", pos1*1.1)
   cmds.setAttr("GRP_faceGUI.ty", pos1*-0.6)
   
   if cmds.objExists("CTRL_faceGUIShape"):
      cmds.delete("CTRL_faceGUIShape")
   
   temp_string = cmds.listRelatives("FRM_faceGUI", ad=1, type="mesh")
   
   for _temp in temp_string:
      if cmds.getAttr("{}.overrideDisplayType".format(_temp)) == 2:
         cmds.sets(_temp, e=1, forceElement="asBlackSG")
      else:
         cmds.sets(_temp, e=1, forceElement="asGreen2SG")
   
def ds_sdk(driver, driven, driver_value, driven_value):
   strat_value = 0
   if mel.eval('gmatch %s "*[.]s[x-z]"' % driven) 
   
      
   
   
def lock_attr():
   pass
   
def go_to_pose():
   pass

def as_align(object, align_to_object, translate, rotate, joine_orient, rotate_order):
   """_summary_

   Args:
       object (string): _description_
       align_to_object (string): _description_
       translate (bool): _description_
       rotate (bool): _description_
       joine_orient (bool): _description_
       rotate_order (bool): _description_
   """
   parents = cmds.listRelatives(object, p=1)
   cmds.parent(object, align_to_object)
   temp_string = cmds.listRelatives(object, p=1)[0]
   
   if temp_string != align_to_object:
      generated_xform = temp_string
   
   if translate:
      cmds.xform(object, os=1, t=(0, 0, 0))
      if generated_xform != "":
         cmds.xform(generated_xform, os=1, t=(0, 0, 0))
   
   if rotate_order:
      cmds.setAttr("{}.rotateOrder".format(object), cmds.getAttr("{}.rotateOrder".format(align_to_object)))
   
   if rotate:
      cmds.xform(object, os=1, ro=(0, 0, 0))
      if generated_xform != "":
         cmds.xform(generated_xform, os=1, rp=(0, 0 , 0))
         
   if joine_orient and  rotate:
      cmds.setAttr("{}.jointOrient".format(object), 0, 0, 0, type="float3")
   
   if cmds.objExists(parents):
      cmds.parent(object, parents)
   else:
      cmds.parent(object, w=1)
      