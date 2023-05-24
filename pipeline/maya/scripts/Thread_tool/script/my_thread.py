#!/user/bin/env python
# -*- coding: utf-8 -*-
# Author: Zhenbao Liu
# QQ: 3305510092
# Time: 2021/07/06 22:39:35

'''
File_name: thread.py
This is a script to rename objects
'''
try:
    from PySide import QtGui as QtWidgets
    from PySide import QtCore
    from PySide import QtGui 
except:
    from PySide2 import QtWidgets as QtWidgets
    from PySide2 import QtCore
    from PySide2 import QtGui 

import maya.cmds as cmds
import pymel.core as pymel
import string


class ThreadScript:
    def __init__(self):
        self.add_lin_prefix = None
        self.add_lin_suffix = None
        self.replace_lin_find = None
        self.replace_lin_replace = None
        self.add_button_group = None
        self.replace_button_group = None
        self.rename_button_group = None
        self.rename_item_group = None
        self.rename_lin_object = None
        self.rename_suffix_widget = None
        self.rdb_case_switch = None
        self.auto_textedit = None
    
    def get_select_hierarchy(self, sel_obj):
        children_lst = [ch for ch in cmds.listRelatives(sel_obj, allDescendents=True, fullPath=True) if "Shape" not in ch]
        children_lst.append(sel_obj)
        complete_children = children_lst[:]
        list_length = len(complete_children)              
        return complete_children, list_length
    
    def change_string(self, obj_str, prefix_str, suffix_str, index=0, replace=False):
        if obj_str.split("|"):
            obj_str = obj_str.split("|")[-1]
        if replace:
            return obj_str.replace(str(prefix_str), str(suffix_str))
        str_data = obj_str.split("_")
        str_data.insert(index, prefix_str)
        str_data.append(suffix_str)            
        new_str_list = filter(None, str_data)
        new_str = '_'.join(new_str_list)
        return new_str
        
    def seleced_list(self):
        return [sel for sel in cmds.ls(sl=True)]
            
    def add_prefix_suffix(self):
        for sel in self.seleced_list():
            if self.get_add_group() == "Hierarchy" and (self.get_prefix_str() or self.get_suffix_str()):
                list_string_data, list_length = self.get_select_hierarchy(sel)
                for ch in range(list_length):
                    hie_string = self.change_string(list_string_data[ch-list_length], self.get_prefix_str(), self.get_suffix_str())
                    cmds.rename(list_string_data[ch], hie_string)
            elif self.get_add_group() == "Selected" and (self.get_prefix_str() or self.get_suffix_str()):
                new_string = self.change_string(sel, self.get_prefix_str(), self.get_suffix_str())
                cmds.rename(sel, new_string)
            else:
                cmds.warning("Plase enter prefix or suffix")
       
    def _replace(self):
        for sel in self.seleced_list():
            if self.get_replace_group() == "Hierarchy":
                list_string_data, list_length = self.get_select_hierarchy(sel)
                for ch in range(list_length):
                    hie_string = self.change_string(list_string_data[ch-list_length], self.get_find_str(), self.get_replace_str(), replace=True)
                    cmds.rename(list_string_data[ch], hie_string)                    
            elif self.get_replace_group() == "Selected":
                new_string = self.change_string(sel, self.get_find_str(), self.get_replace_str(), replace=True)
                cmds.rename(sel, new_string)
            else:
                cmds.warning("Plase enter find and replace")
            
    def get_word(self, _index):
        word_list = [word for word in string.lowercase]
        return word_list[_index]

    def switch_first_string(self, sel, object_string, suffix, string=True):
        if string:
            if self.get_switch_value():
                new_name = "".join([object_string, suffix.capitalize()])
                cmds.rename(sel, new_name)
            else:
                new_name = "".join([object_string, suffix])
                cmds.rename(sel, new_name)
        else:
            new_name = "".join([object_string, str(suffix)])
            cmds.rename(sel, new_name)
    
    def _rename(self):
        object_string = self.get_object_name()
        for v, sel in enumerate(self.seleced_list()):
            list_string_data, list_length = self.get_select_hierarchy(sel)
            if self.get_item_group() == "a-z":
                if self.get_rename_group() == "Selected":                              
                    self.switch_first_string(sel, object_string, self.get_word(v))
                else:
                    for s_index in range(list_length):
                        self.switch_first_string(list_string_data[s_index-list_length], object_string, self.get_word(list_length-s_index-1))
            elif self.get_item_group() == "0-9":
                if self.get_rename_group() == "Selected":                              
                    self.switch_first_string(sel, object_string, string=False)
                else:
                    for n_index in range(list_length):
                        self.switch_first_string(list_string_data[n_index-list_length], object_string, list_length-n_index-1, string=False)           
            else:
                text_list = self.get_auto_textedit().split("\n")
                text_list.reverse()
                if self.get_rename_group() == "Selected":                              
                    self.switch_first_string(sel, object_string, text_list[v])
                else:
                    for i_index, i_value in enumerate(text_list):
                        print (i_index, i_value)
                        self.switch_first_string(list_string_data[i_index-list_length], object_string, i_value)
    # Get user enter string
    def get_prefix_str(self):
        if not self.add_lin_prefix:
            return
        return self.add_lin_prefix.text()
    
    def get_suffix_str(self):
        if not self.add_lin_suffix:
            return
        return self.add_lin_suffix.text()
    
    def get_find_str(self):
        if not self.replace_lin_find:
            return
        return self.replace_lin_find.text()
    
    def get_replace_str(self):
        if not self.replace_lin_replace:
            return
        return self.replace_lin_replace.text()
    
    def get_object_name(self):
        if not self.rename_lin_object:
            return
        return self.rename_lin_object.text()
    
    def get_switch_value(self):
        if self.rdb_case_switch.checkState() == QtCore.Qt.CheckState.Checked:
            return True
        return False
    
    def get_add_group(self):
        return self.add_button_group.checkedButton().text()
    
    def get_replace_group(self):
        return self.replace_button_group.checkedButton().text()
    
    def get_rename_group(self):
        return self.rename_button_group.checkedButton().text()
    
    def get_item_group(self):
        return self.rename_item_group.checkedButton().text()
    
    def get_auto_textedit(self):
        if not self.auto_textedit:
            return
        return self.auto_textedit.toPlainText()