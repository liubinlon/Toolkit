#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
'''
File    :   link_cg.py
Time    :   2022/06/24 21:53:47
Author  :   ZhenBao Liu
Version :   1.0
Contact :   3305510092@qq.com
Desc    :   None
'''

import sys
import pymel.core as pm
from maya.api import OpenMaya as om
import os
import json


def maya_useNewAPI():
    pass

main_window = pm.language.melGlobals["gMainWindow"]
kPluginCmdName = 'pipeline'
kPluginVendor = '3305510092@qq.com'
kPluginVersion = '2022.06.26'


# Menu and Shelf
# ----------------------------------------------------------------------

def get_menu_data():
    abs_file = r"D:/ToolKit/pipeline/maya/plug/pipeline_plug.py"
    abs_dir = abs_file[:abs_file.rfind("/")]
    with open("{}/pipeline_box.json".format(abs_dir), 'r') as load_f:
        load_dict = json.load(load_f)
    return load_dict

def make_menu(mobject): 
    """
    make menu when plugin load
    """
    remove_menu(kPluginCmdName)
    plugin = om.MFnPlugin(mobject, kPluginVendor, kPluginVersion)
    data_dict = get_menu_data()    
    pipeline_box = pm.menu(kPluginCmdName, label=kPluginCmdName, parent=main_window, tearOff=True)
    for key, value in data_dict.items():
        pm.menuItem(divider=True, dividerLabel=key)
        pm.menuItem(label=key, subMenu=True, parent=pipeline_box, tearOff=True)
        for label, command in value.items():
            pm.menuItem(label=str(label), command=command, sourceType='mel')
            com = PlipelineCom(command)
            plugin.registerCommand(label, com.creator())
            pm.setParent("..", menu=True)

def remove_menu(menu=kPluginCmdName):
    """
    remove menu when plugin unload
    """
    if pm.menu(kPluginCmdName, q=True, exists=True):
        pm.deleteUI(kPluginCmdName, menu=True)
# Plugin class
# ----------------------------------------------------------------------
class PlipelineCom(om.MPxCommand):

    def __init__(self, command_win):
        super(PlipelineCom, self).__init__()
        self.command_win = command_win
    def doIt(self, args):
        import self.command_win
        reload(self.command_win)
        self.command_win.run()

    @staticmethod
    def creator():
        return PlipelineCom(command_win)


# Initialize
# ----------------------------------------------------------------------
def initializePlugin(mobject):
    """Initialize the plug-in and add menu"""
    errMsg = u'Failed to register command: %s\n' % kPluginCmdName   
    try:        
        make_menu(mobject)
    except:
        sys.stderr.write(errMsg)
        raise

# Uninitialize
# ----------------------------------------------------------------------
def uninitializePlugin(mobject):
    """Uninitialize the plug-in and delete menu"""
    plugin = om.MFnPlugin(mobject)
    data_dict = get_menu_data() 
    try:           
        for key, value in data_dict.items():
            for label, command in value.items():
                plugin.deregisterCommand(command)
        remove_menu()
    except:
        sys.stderr.write('Failed to unregister command: %s\n' % kPluginCmdName)
        raise