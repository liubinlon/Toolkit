#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# author: ZhenBao Liu
# time: 2021/4/4
import os, sys
import pymel.core as pm
import json
"""
load 
"""


def add_menu():
    # Get maya main window
    main_window = pm.language.melGlobals["gMainWindow"]
    menu_obj = "MyToolsBox"
    menu_label = "My Tools Box"

    # Load json configuration file
    with open("C:/Users/liubi/Documents/maya/2018/scripts/MyToolsBox.json", 'r') as load_f:
        load_dict = json.load(load_f)

    # Determine the menu status
    if pm.menu(menu_obj, label=menu_label, exists=True, parent=main_window):
        pm.deleteUI(pm.menu(menu_obj, label=menu_label, edit=True, deleteAllItems=True))
    # Add main menu
    my_tools_box = pm.menu(menu_obj, label=menu_label, parent=main_window, tearOff=True)
    # Add submenu
    for key, value in load_dict.items():
        pm.menuItem(divider=True, dividerLabel=str(key))
        pm.menuItem(label=str(key), subMenu=True, parent=my_tools_box, tearOff=True)
        for label, command in value.items():
            print "execfile(./{0})".format(str(command))
            pm.menuItem(label=str(label), command="execfile(./{0})".format(str(command)))
            pm.setParent("..", menu=True)


if __name__ == "__main__":
    add_menu()