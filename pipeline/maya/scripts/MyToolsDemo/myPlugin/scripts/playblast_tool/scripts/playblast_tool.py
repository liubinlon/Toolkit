#!/user/bin/env python
# -*- coding: utf-8 -*-
# Author: Zhenbao Liu
# QQ: 3305510092
# Time: 2021/07/25 12:48:38

'''
File_name: playblast_tool.py
plase enter description
'''
try:
    from PySide import QtGui as QtWidgets
    from PySide import QtCore
    from PySide import QtGui 
except:
    from PySide2 import QtWidgets as QtWidgets
    from PySide2 import QtCore
    from PySide2 import QtGui 
#bulit_in modules
import os
import sys
import getpass
#maya modules
import maya.cmds as cmds
import pymel.core as pymel
import maya.OpenMayaUI as omui


class Playblast:
    def __init__(self):
        self.let_ainfile = None
        self.let_playfile = None
        self.let_start = None
        self.let_end = None
        self.let_height = None
        self.let_width = None
        self.let_suffix = None
        
    def getfilename(self, full_path=None, dir_path=None):
        if full_path:
            if dir_path:
                return str(pymel.sceneName().dirname())
            return str(pymel.sceneName().abspath())
        return str(pymel.sceneName().basename()).split(".")[0]

    def get_user_name(self):
        return getpass.getuser()
            
    def get_camera(self):
        return str(cmds.lookThru(q=True))

    def get_focal_length(self):
        camera_name = self.get_camera()
        return int(cmds.getAttr(camera_name + ".focalLength"))

    def get_time(self):
        get_currentTime = cmds.currentTime(q=True)
        return get_currentTime

    def get_current_fps(self, *args):
        format_list = {'film': 24, 'game': 15, 'pal': 25, 'ntsc': 30, 'show': 48, 'palf': 50, 'ntscf': 60}
        fpsString = cmds.currentUnit(query=True, t=True)
        try:
            return format_list[fpsString]
        except:
            return False

    def get_proj_size(self):
        if cmds.objExists('defaultResolution'):
            width = cmds.getAttr('defaultResolution.w')
            height = cmds.getAttr('defaultResolution.h')
            return str(width) + '*' + str(height)
        else:
            return '000'
        
    def setup_filename(self, directory_path=None):
        if directory_path:
            return "{0}/{1}.{2}".format(directory_path, self.getfilename(), self.get_output_type())
        return "{0}/{1}.{2}".format(self.getfilename(full_path=True, dir_path=True), self.getfilename(), "mov")

    def get_timeslider_data(self):
        return [str(pymel.playbackOptions(min=True, query=True)), str(pymel.playbackOptions(max=True, query=True))]

    def open_file_dialog(self, pathdata):
        directory = QtWidgets.QFileDialog()
        directory.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        directory.setNameFilter("MayaFile (*.ma *.mb)")
        directory.setViewMode(QtWidgets.QFileDialog.Detail)
        if directory.exec_():
            directory_name = directory.selectedFiles()
            directory_new_name = directory_name[0]
            # print(file_name)
            pathdata.setText(directory_new_name)
            # print (type(file_name[0]))
            folder_name = os.path.basename(directory_new_name)
        else:
            QtWidgets.QMessageBox.warning(self, "warning", "Please select folder")
        return directory_new_name, folder_name
    
    def open_directory_dialog(self, pathdata):
        directory = QtWidgets.QFileDialog()
        directory.setFileMode(QtWidgets.QFileDialog.Directory)        
        directory.setViewMode(QtWidgets.QFileDialog.Detail)
        if directory.exec_():
            directory_name = directory.selectedFiles()[0]
            directory_new_name = self.setup_filename(directory_path=directory_name)
            # print(file_name)
            pathdata.setText(directory_new_name)
            # print (type(file_name[0]))
            folder_name = os.path.basename(directory_new_name)
        else:
            QtWidgets.QMessageBox.warning(self, "warning", "Please select folder")
        return directory_new_name, folder_name
         
    def selected_file(self):
        return self.open_file_dialog(self.let_ainfile) 
       
    def open_save_path(self):
        return self.open_directory_dialog(self.let_playfile)
    
    def make_file_exists(self):
        exists_dict = {"Yes": True, "Close": False}
        file_name = self.setup_filename()
        message_string = "File '{0}' exists. Overwrite?".format(file_name)
        if not os.path.isfile(file_name):
            return True
        exists_string = cmds.confirmDialog(title='Playblast Error: File Exists', message=message_string, button=['Yes', 'Close'], defaultButton='Yes', cancelButton='No')
        return exists_dict[exists_string]
    
    def run_playblast(self):
        width_height_data = [int(self.get_width_data()), int(self.get_height_data())]
        output_name =self.setup_filename()
        start_time = self.get_start_data()
        end_time = self.get_end_data()
        output_type = self.get_output_type()
        type_dict = {"mov": "qt", "avi": "avi"}
        if not self.make_file_exists():
            return
        cmds.playblast(format=type_dict[output_type], filename=output_name, sequenceTime=False, forceOverwrite=True, clearCache=1, viewer=True, 
                       showOrnaments=False, compression="H.264", percent=50, widthHeight=width_height_data , startTime=start_time, endTime=end_time)
    
    def get_ain_file(self):
        if not self.let_ainfile:
            return 
        return self.let_ainfile.text()
           
    def get_play_path(self):
        if not self.let_playfile:
            return        
        return self.let_playfile.text()
    
    def get_start_data(self):
        if not self.let_start:
            return
        return self.let_start.text()
    
    def get_end_data(self):
        if not self.let_end:
            return
        return self.let_end.text()
    
    def get_height_data(self):
        if not self.let_height:
            return 
        return self.let_height.text()
    
    def get_width_data(self):
        if not self.let_width:
            return 
        return self.let_width.text()
    
    def get_output_type(self):
        if not self.let_suffix:
            return
        return self.let_suffix.text()