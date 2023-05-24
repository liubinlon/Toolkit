#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
'''
   File    :   bach_usd_com.py
   Time    :   2022/12/13 11:38:39
   Author  :   Liu ZhenBao
   Version :   1.0
   Contact :   3305510092@qq.com
   Desc    :   None
'''
############################################################################

# import the libraries needed by this script here

# here put the class script
import maya.cmds as cmds
import ufe
from pxr import Usd
import mayaUsd as uLib
import os 
import sys
import subprocess
if ufe.GlobalSelection.get().empty():
    cmds.error("Select any ufe item under (and including) gateway node")

ufe_item = ufe.GlobalSelection().get().back()
ufe_path_gateway = ufe.Path(ufe_item.path().segments[0])
stage = uLib.ufe.getStage(str(ufe_path_gateway))
sdfLayer = stage.GetRootLayer()
mayaVer = int(cmds.about(q=True, majorVersion=True))
if mayaVer == 2022:
    maya_py = os.path.join(os.environ["MAYA_LOCATION"], "bin", "mayapy{ver}".format(ver="" if sys.version_info.major == 3 else "2"))
else:
    maya_py = os.path.join(os.environ["MAYA_LOCATION"], "bin", "mayapy")

usd_view_path = os.path.join(os.environ["USD_LOCATION"], "bin", "usdview")

try:
    import OpenGL
except:
    subprocess.check_call(maya_py, "-m", "pip", "install", "PyOpenGL==3.1.0")

CREATE_NO_WINDOW = 0x08000000
subprocess.Popen([maya_py, usd_view_path, sdfLayer.realpath], creationflags=subprocess.CREATE_NO_WINDOW)