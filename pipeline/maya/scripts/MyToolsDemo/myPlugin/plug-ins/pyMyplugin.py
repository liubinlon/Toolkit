#coding = utf-8
#python maya plugin for MyToolsDemo

import sys
import pymel.core as pm
import json
import maya.mel as mel
from maya.api import OpenMaya as om
from maya import cmds


def maya_useNewAPI():
    pass
#
COMMAND_NAME = "MyToolsBox"
# Add main menu
main_window = pm.language.melGlobals["gMainWindow"]

def remove_menu(menuName=COMMAND_NAME, parent=main_window):
    """
    remove menu when plugin unload
    """
    if pm.menu(menuName, label=menuName, q=True, exists=True, parent=parent):
        pm.deleteUI(pm.menu(menuName, label=menuName, edit=True, deleteAllItems=True))


def make_menu(menuName=COMMAND_NAME, parent=main_window):
    """
    make menu when plugin load
    """
    remove_menu(menuName)
    # Load json configuration file
    with open("C:/Users/liubi/Documents/maya/2018/scripts/MyToolsBox.json",'r') as load_f:
        load_dict = json.load(load_f)
    topMenu = cmds.menu(menuName, label=menuName, parent=parent, tearOff=True)
    # Add submenu
    for key, value in load_dict.items():
        pm.menuItem(divider=True, dividerLabel=str(key))
        pm.menuItem(label=str(key), subMenu=True, parent=parent, tearOff=True)
        for label, command in value.items():
            pm.menuItem(label=str(label),command=str(command))
            pm.setParent("..", menu=True)

#Plugin
#--------------------------------------
class MyToolsBox(om.MPxCommand):
    def __init__(self):
        super(MyToolsBox, self).__init__()

    def doIt(self, *args):
        print("starting %s" % COMMAND_NAME)
        # try:
        #     import mytool
        #     reload(mytool)
        #     mytool.main()
        # except Exception as ex:
        #     cmds.error(ex.message())

    @staticmethod
    def creator():
        return MyToolsBox()
    # @classmethod
    # def cmdCreator(cls):
    #     return MyToolsBox()


def initializePlugin(plugin):
    """
    """
    vendor = "My Tools Box"
    version = "2021.01.31"
    plugin_fn = om.MFnPlugin(plugin, kPluginVendor, kPluginVersion)
    try:
        plugin_fn.registerCommand(COMMAND_NAME, MyToolsBox.creator)
        make_menu(menuName=COMMAND_NAME)   
    except:
        sys.stderr.write("Failed to register command: {0}".format(COMMAND_NAME))
        raise

def uninitializePlugin(plugin):
    """
    """
    plugin_fn = om.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterCommand(COMMAND_NAME)
        remove_menu(menuName=COMMAND_NAME)
    except:
        sys.stderr.write("Failed to register command: {0}".format(COMMAND_NAME))
        raise

if __name__ == "__main__":
    plugin_name = "pyMyplugin.py"

    cmds.evalDeferred("if cmds.pluginInfo('{0}', q=True, loaded=True): cmds.unloadPlugin('{0}')".format(plugin_name))
    cmds.evalDeferred("if not cmds.pluginInfo('{0}', q=True, loaded=False): cmds.loadPlugin('{0}')".format(plugin_name))

