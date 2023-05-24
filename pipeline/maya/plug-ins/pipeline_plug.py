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
def remove_menu(menu_name=kPluginCmdName):
    """
    remove menu when plugin unload
    """
    if pm.menu(menu_name, q=True, exists=True):
        pm.deleteUI(menu_name, menu=True)


def make_menu(menu_name, label, command,):
    """
    make menu when plugin load
    """
    remove_menu(kPluginCmdName)
    pipeline_box = pm.menu(kPluginCmdName, label=kPluginCmdName, parent=main_window, tearOff=True)
    pm.menuItem(divider=True, dividerLabel=menu_name)
    pm.menuItem(label=menu_name, subMenu=True, parent=pipeline_box, tearOff=True)
    pm.menuItem(label=str(label), command=command, sourceType='mel')
    pm.setParent("..", menu=True)
    
def get_menu_data():
    menu_list = list()
    label_list = list()
    command_list = list()
    abs_file = r"D:\\Toolkit\maya\\GenerateToolsBox.py"
    abs_dir = abs_file[:abs_file.rfind("\\")]
    with open("{}/MyToolsBox.json".format(abs_dir), 'r') as load_f:
        load_dict = json.load(load_f)
    for key, value in load_dict.items():
        menu_list.append(key)
        for label, command in value.items():
            label_list.append(label)
            command_list.append(command)
    return menu_list, label_list, command_list



# Plugin class
# ----------------------------------------------------------------------
class PlipelineCom(om.MPxCommand):
    def __init__(self, command_win):
        super(PlipelineCom, self).__init__()
        import command_win
        reload(command_win)

    def doIt(self, args):
        try:
            import self.win
            reload(self.win)
            self.win.main()
        except Exception as ex:
            pm.error(ex.message())

    @staticmethod
    def creator():
        return PlipelineCom()


# Initialize
# ----------------------------------------------------------------------
def initializePlugin(mobject):
    """Initialize the plug-in and add menu"""
    errMsg = u'Failed to register command: %s\n' % kPluginCmdName
    plugin = om.MFnPlugin(mobject, kPluginVendor, kPluginVersion)
    try:
        plugin.registerCommand(kPluginCmdName, PlipelineCom.creator)
        make_menu(menu_name=kPluginCmdName)
        # makeShelf(shelfName=kPluginCmdName)
    except:
        sys.stderr.write(errMsg)
        raise

# Uninitialize
# ----------------------------------------------------------------------
def uninitializePlugin(mobject):
    """Uninitialize the plug-in and delete menu"""
    plugin = om.MFnPlugin(mobject)
    try:
        plugin.deregisterCommand(kPluginCmdName)
        remove_menu(menu_name=kPluginCmdName)
        # removeShelf(shelfName=kPluginCmdName)
    except:
        sys.stderr.write('Failed to unregister command: %s\n' % kPluginCmdName)
        raise