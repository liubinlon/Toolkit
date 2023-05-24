#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
'''
File    :   generate_tools_menu.py
Time    :   2022/08/10 12:47:33
Author  :   ZhenBao Liu
Version :   1.0
Contact :   3305510092@qq.com
Desc    :   None
'''
# import the libraries needed by this script here

import inspect
import os
import json
import pymel.core as pm
from maya import mel
# Get maya main window
main_window = pm.language.melGlobals["gMainWindow"]
menu_obj = "MayaToolsBox"
menu_label = "Pileline"
abs_file = os.path.abspath(inspect.getsourcefile(lambda: 0))

# Load json configuration file

abs_dir = abs_file[:abs_file.rfind("\\")]
icons_dir = os.path.abspath(os.path.dirname(abs_dir))

with open("{}/maya_tool_menu.json".format(abs_dir), 'r') as load_f:
    load_dict = json.load(load_f)

# Determine the menu status
def delete_menu(menu_obj):
    if pm.menu(menu_obj, label=menu_label, exists=True, parent=main_window):
        pm.deleteUI(pm.menu(menu_obj, label=menu_label, edit=True, deleteAllItems=True))
# 首字母大写
def auto_capitalize(_string):
    return _string.capitalize()

# Load command
def load_command(command_name):
    if "mel" in command_name:
        mel_function = command_name.split(":")[-1]
        return "mel.eval('{};')".format(mel_function)
    return "import {0}\nreload({0})\n{0}.start()".format(command_name)

def get_icons(_name):
    return "{}/icons/{}.png".format(icons_dir, _name)

# Add submenus
def make_menu():
    delete_menu(menu_obj)
    # Add main menu
    my_tools_box = pm.menu(menu_obj, label=menu_label, parent=main_window, tearOff=True)
    for key, value in load_dict.items():
        pm.menuItem(divider=True, dividerLabel=str(auto_capitalize(key)))
        parent_icon = get_icons(str(key))
        if os.path.exists(parent_icon):
            parent_menu = pm.menuItem(label=str(auto_capitalize(key)), subMenu=True, parent=my_tools_box, tearOff=True, image=parent_icon)
        else:
            parent_menu = pm.menuItem(label=str(auto_capitalize(key)), subMenu=True, parent=my_tools_box, tearOff=True)
        for label, command in value.items():
            label_icon = get_icons(str(label))
            if os.path.exists(label_icon):
                pm.menuItem(label=str(label), command=load_command(command), parent=parent_menu, image=label_icon)
            else:
                pm.menuItem(label=str(label), command=load_command(command), parent=parent_menu)
            pm.setParent("..", menu=True)

if __name__ == "__main__":
    make_menu()
