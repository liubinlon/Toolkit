# -*- coding: utf-8 -*-
"""
author:MoFeioO
time:2020/10/23 15:52
"""
from maya import cmds
import os
import json
import pprint

USERAPPDIR = cmds.internalVar(userAppDir=True)
DIRECTORY = os.path.join(USERAPPDIR, "controllerLibrary")


def create_directory(directory=DIRECTORY):
    """
    Creates the given directory if it doesn't exist already
    Args:
        directory (str): The directory to create
    """
    if not os.path.exists(directory):
        os.mkdir(directory)


class ControllerLibrary(dict):

    def save(self, name, directory=DIRECTORY, **info):
        create_directory(directory)

        path = os.path.join(directory, "{}.ma".format(name))
        info_file = os.path.join(directory, "{}.json".format(name))
        info["name"] = name
        info["path"] = path

        cmds.file(rename=path)

        if cmds.ls(sl=True):
            cmds.file(force=True, type="mayaAscii", exportSelected=True)
        else:
            cmds.file(save=True, type="mayaAscii", force=True)

        with open(info_file, "w") as f:
            json.dump(info, f, indent=4)

        self[name] = info

    def find(self, directory=DIRECTORY):
        self.clear()
        if not os.path.exists(directory):
            return

        files = os.listdir(directory)
        mayaFiles = [f for f in files if f.endswith(".ma")]

        for ma in mayaFiles:
            name, ext = os.path.splitext(ma)
            path = os.path.join(directory, ma)

            info_file = "{0}.json".format(name)
            if info_file in files:
                info_file = os.path.join(directory, info_file)

                with open(info_file, 'r') as f:
                    info = json.load(f)
            else:
                info = {}

            screen_shot = "{}.jpg".format(name)
            if screen_shot in files:
                info["screenshot"] = os.path.join(directory, name)

            info["name"] = name
            info["path"] = path

            self[name] = info


    def load(self, name):
        path = self[name]["path"]
        cmds.file(path, i=True, usingNamespaces=False)

    def save_screenshot(self, name, directory=DIRECTORY):
        path = os.path.join(directory, "{0}.jpg".format(name))
        cmds.viewFit()
        cmds.setAttr("defaultRenderGlobals.imageFormat", 8)
        cmds.playblast(completeFilename=path, forceOverwrite=True, format="image",
                       width=200, height=200, showOrnaments=False, startTime=1, endTime=1, viewer=False)
        return path