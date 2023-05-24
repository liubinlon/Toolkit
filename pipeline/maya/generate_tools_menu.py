import os
import json
import pymel.core as pm

# Get maya main window
main_window = pm.language.melGlobals["gMainWindow"]
menu_obj = "MayaToolsBox"
menu_label = "MayaToolsBox"
abs_file = r"D:\\Toolkit\maya\\generate_tools_menu.py"
# Load json configuration file
# menu_lst_json = os.path.abspath(os.path.dirname(__file__))
abs_dir = abs_file[:abs_file.rfind("\\")]
with open("{}/maya_tool_menu.json".format(abs_dir), 'r') as load_f:
    load_dict = json.load(load_f)

# Determine the menu status
if pm.menu(menu_obj, label=menu_label, exists=True, parent=main_window):
    pm.deleteUI(pm.menu(menu_obj, label=menu_label, edit=True, deleteAllItems=True))
# Add main menu
my_tools_box = pm.menu(menu_obj, label=menu_label, parent=main_window, tearOff=True)

# Load command
def load_command(command_name):
    return "python(\"import {0};reload({0});{0}.start()\")".format(str(command_name))   
# Add submenus
def make_menu():
    for key, value in load_dict.items():
        pm.menuItem(divider=True, dividerLabel=str(key))
        pm.menuItem(label=str(key), subMenu=True, parent=my_tools_box, tearOff=True)
        for label, command in value.items():
            pm.menuItem(label=str(label), command=load_command(command))
            pm.setParent("..", menu=True)