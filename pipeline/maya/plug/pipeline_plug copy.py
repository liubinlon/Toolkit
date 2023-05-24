#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
'''
File    :   pipeline_plug copy.py
Time    :   2022/08/08 11:15:16
Author  :   ZhenBao Liu
Version :   1.0
Contact :   3305510092@qq.com
Desc    :   None
'''
# import the libraries needed by this script here
import sys, math, os, json
import pymel.core as pm
from maya.api import OpenMaya as om

def maya_useNewAPI():
    pass

main_window = pm.language.melGlobals["gMainWindow"]
kPluginCmdName = 'pipeline'
kPluginVendor = '3305510092@qq.com'
kPluginVersion = '2022.06.26'

# here put the class script
class PlipelineCom(om.MPxCommand):

    def __init__(self):
        om.MPxCommand.__init__(self)
    @staticmethod
    def cmdCreator():
        return PlipelineCom()

    def doIt(self, args):
        print "Hello World!"

# Initialize
# ----------------------------------------------------------------------
def initializePlugin(plugin):
    """Initialize the plug-in and add menu"""
    errMsg = u'Failed to register command: %s\n' % kPluginCmdName   
    pluginFn = om.MFnPlugin(plugin)
    try:        
        pluginFn.registerCommand(
            kPluginCmdName, PlipelineCom.cmdCreator
        )
    except:
        sys.stderr.write(errMsg)
        raise

# Uninitialize
# ----------------------------------------------------------------------
def uninitializePlugin(plugin):
    """Uninitialize the plug-in and delete menu"""
    pluginFn = om.MFnPlugin(plugin)
    #data_dict = get_menu_data() 
    try:
        pluginFn.deregisterCommand(kPluginCmdName)
    except:
        sys.stderr.write('Failed to unregister command: %s\n' % kPluginCmdName)
        raise