#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
'''
   File    :   __init__.py
   Time    :   2022/12/14 10:39:02
   Author  :   Liu ZhenBao
   Version :   1.0
   Contact :   3305510092@qq.com
   Desc    :   None
'''
############################################################################

# import the libraries needed by this script here
from pxr import tf
from pxr.Usdviewq.plugin import PluginContainer


def printMessage(usdviewApi):
    print("Hello, Worlld ")
# here put the class script
class TutorialPluginContainer(PluginContainer):
    def registerPlugins(self, plugRegistry, usdviewApi):
        self._printMessage = plugRegistry.registerCommandPlugin(
            "TutorialPluginContainer.printMessage",
            "Print Message",
            printMessage
            )
    
    def configureView(self, plugRegistry, plugUIBuilder):
        tutMenu = plugUIBuilder.findOrCreateMenu("Tutorial")
        tutMenu.addItem(self._printMessage)

tf.Type.Define(TutorialPluginContainer)
