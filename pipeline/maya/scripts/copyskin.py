#!/usr/bin/env python2
# -*- encoding: utf-8 -*-

import maya.cmds as mc
import maya.mel as mm


def start():
            
    if mc.window("copy_skin",ex=True):
        mc.deleteUI("copy_skin")
    mc.window('copy_skin',title=u'拷贝权重到布料简模')
    mc.columnLayout(adjustableColumn=True)
    mc.text(label=u'先选择绑定模型，再加选目标物体，然后点击\'执行\'按钮')
    mc.button(label=u'执行',command='copy_skin_oto()')
    mc.showWindow()

def copy_skin_oto():

    one_one_list=mc.ls(sl=True)
    
    ss_skin = mm.eval("findRelatedSkinCluster "+one_one_list[0])
    
    if ss_skin.split(":")[-1][:4]=="skin":

        get_joint_list=mc.listConnections('%s.matrix'%ss_skin)
        
        ds_skin=mc.skinCluster(get_joint_list,one_one_list[1],tsb=True)
        
        mc.copySkinWeights(ss=ss_skin,ds=ds_skin[0],noMirror=True,surfaceAssociation='closestPoint',ia='oneToOne')
        
    else:
                  
        skin_Cluster = mc.listConnections('%s.inputPolymesh'%ss_skin[0])
        
        get_joint_list=mc.listConnections('%s.matrix'%skin_Cluster[0])
        
        ds_skin=mc.skinCluster(get_joint_list,one_one_list[1],tsb=True)
        
        mc.copySkinWeights(ss=skin_Cluster[0],ds=ds_skin[0],noMirror=True,surfaceAssociation='closestPoint',ia='oneToOne')
    