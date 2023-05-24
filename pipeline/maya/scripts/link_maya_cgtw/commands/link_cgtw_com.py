#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
   File    :   link_cgtw_com.py
   Time    :   2022/12/02 16:58:34
   Author  :   Liu ZhenBao
   Version :   1.0
   Contact :   3305510092@qq.com
   Desc    :   None
'''
############################################################################
# import the libraries needed by this script here
import sys
import os
import subprocess
import shutil
import time
import re
import maya.OpenMaya as om
import pymel.core as pm
import maya.cmds as cmds
from PySide2.QtWidgets import QApplication
from collections import OrderedDict
# Add cgtw path
cgtw_dir = r"C:/CgTeamWork_v6/bin/base"
file_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

if dir not in sys.path:
    sys.path += [cgtw_dir, file_dir]

import cgtw2
from commonly_maya import CommonlyMaya
from commonly_operation import CommonlyOperation
# reload(commonly_used)

# here put the class script
class LinkCgtwCom:
    """
        根据资产名字和模块, 进行数据库比对, 如果是当前艺术家的任务, 获取资产所需服务器数据, 根据命名规则重新命名文件,  提交工程文件和审核文件
    """
    def __init__(self):
        # label      
        self.info_department = None
        self.info_name = None
        # combo box
        self.user_project = None
        self.user_type = None
        # line edit
        self.file_path = None
        self.screenshot_path = None
        self.material_path = None
        # list widget
        self.appendix_path = None
        # text edit
        self.file_describe = None
        self.feedback = None
        # widget display
        self.info_widget_show = None
        self.message_widget_show = None
        self.test_widget_show = None
        self.screen_widget_show = None
        self.file_widget_show = None
        self.transmit_widget_show = None
        self.project_widget_show = None

        self.m_tw = cgtw2.tw()
        self.maya_cmd = CommonlyMaya()
        self.operation_cmd = CommonlyOperation
        self._data_dict = dict()
        self.get_user_data()        
        self.get_project_data()
        self.get_comparison_information()
    """
        获取当前cgtw登录用户的信息
    """
    def split_tab(self, _tab):
        """
            对数据库获得的数据拆分字符串
        """
        if _tab:
            _tab_str = _tab.split(".")
        return _tab_str[-1]
        
    def get_user_data(self):
        """
            获取登录用户所在组和用户名, 并添加到字典self._data_dict
        """
        m_id = self.m_tw.login.account_id()
        field_sign_list = ["account.name", "account.department"]

        user_data = self.m_tw.info.get("public", "account", [m_id], field_sign_list=field_sign_list)
        self._data_dict["personal"] = {self.split_tab(_data): user_data[0][_data] for _data in field_sign_list}
        
    def get_project_data(self):
        """
            获取所有项目的名字, 数据库, 并添加到字典self._data_dict
        """
        project_field_sign_list=['project.database', 'project.entity']
        project_id = self.m_tw.info.get_id("public", "project", filter_list=[])
        project_data = self.m_tw.info.get("public", "project", project_id, field_sign_list=project_field_sign_list)
        self._data_dict["project"] ={pro["project.database"]: pro["project.entity"] for pro in project_data}

    def get_comparison_information(self):
        """
            根据大纲资产的名字和模块, 获取数据库的信息。
            return: 数据库,  id, work路径, 文件名字, 版本号
        """
        comparison_information = dict()
        lst = cmds.ls(assemblies=True)
        def_cam = ['persp', 'top', 'front', 'side']
        try:    
            camre_node = [node for node in list(set(lst).difference(set(def_cam))) if cmds.nodeType(cmds.listRelatives(node, shapes=1)) == "camera"][0]
            seq_entity, shot_entity, task_entity = camre_node.split("_")
            comparison_information["asset_entity"] = "{}_{}".format(seq_entity, shot_entity)
            comparison_information["task_entity"] = task_entity
            basedata_list = [basedata for basedata in self.get_dict_data("project", key=True) if "proj_gba" not in basedata]
            use_name = self.get_dict_data("personal", index="name")
            for basedata in basedata_list:    
                asset_id_list = self.m_tw.task.get_id(db=basedata, module='shot', filter_list=[['seq.entity','=',seq_entity],'and',["shot.entity","=", shot_entity],'and',['task.entity','=',task_entity]])                
                if asset_id_list:
                    comparison_information["module"] = 'shot'
                    task_artist = self.m_tw.task.get(db=basedata, module="shot", id_list=asset_id_list,  field_sign_list=["task.artist"])[0]
                    if use_name in task_artist["task.artist"]:
                        work_filebox_data = self.m_tw.task.get_sign_filebox(db=basedata, module='shot', id=asset_id_list[0], filebox_sign='88')
                        comparison_information["work_path"] = work_filebox_data["path"]
                        comparison_information["work_file_name"] = work_filebox_data["rule"][0]      
                        comparison_information["file_name"] = comparison_information["work_file_name"]
                        comparison_information["basedata"] = basedata
                        comparison_information["asset_id_list"] = asset_id_list
                        self._data_dict["comparison_information"] = comparison_information
                    else:
                        pass
        except: 
            grp_node = list(set(lst).difference(set(def_cam)))
            if grp_node:
                asset_entity,  task_entity = grp_node[0].rsplit("_", 1)
                comparison_information["asset_entity"] = asset_entity
                comparison_information["task_entity"] = task_entity
                basedata_list = self.get_dict_data("project", key=True)
                use_name = self.get_dict_data("personal", index="name")
                for basedata in basedata_list:
                    asset_id_list = self.m_tw.task.get_id(db=basedata, module="asset", filter_list=[["asset.entity", "=", asset_entity], "and", ["task.entity", "=", task_entity]])                    
                    if asset_id_list:
                        comparison_information["module"] = 'asset'
                        task_artist = self.m_tw.task.get(db=basedata, module="asset", id_list=asset_id_list, field_sign_list=["task.artist"])[0]
                        if use_name in task_artist["task.artist"]:
                            work_filebox_data = self.m_tw.task.get_sign_filebox(db=basedata, module='asset', id=asset_id_list[0], filebox_sign='88')
                            comparison_information["work_path"] = work_filebox_data["path"]
                            comparison_information["work_file_name"] = work_filebox_data["rule"][0]  
                            comparison_information["file_name"] = comparison_information["work_file_name"].replace("*****", "")
                            comparison_information["basedata"] = basedata
                            comparison_information["asset_id_list"] = asset_id_list
                            self._data_dict["comparison_information"] = comparison_information
                        else:
                            pass
        else:
            return "assm_list - {}".format(lst)

    def get_dict_data(self, basedata, key=None, value=None, index=None):
        """
            拆分字典
            return: 对应参数
        """
        basedata_dict = self._data_dict[basedata]
        if key:
            return [key for key, value in basedata_dict.items()]
        if value:
            return [value for key, value in basedata_dict.items()]
        if index:
            return basedata_dict[index]

    def public_file(self):
        """
            增加版本文件, 提交新文件
        """
        version_png = None
        tex_file = None
        local_work_path = self.get_work_path()
        current_work_file = os.path.split(local_work_path)
        _db = self._data_dict["comparison_information"]["basedata"]
        _id = self._data_dict["comparison_information"]["asset_id_list"]
        work_path = self._data_dict["comparison_information"]["work_path"]
        note = self.get_file_describe()
        png_path = os.path.split(self.get_screen_path())
        file_name_str = self._data_dict["comparison_information"]["file_name"]
        file_name = file_name_str.split("*")[0]
        if file_name_str.count("#") > 0:
            count_number = file_name_str.count("#")
            version_png = self.find_new_file(work_path.replace("work", "check"), self.get_screen_path(), file_name, count_number)[-1]
            local_png_path = self.maya_cmd._rename_file(png_path[-1], file_name=file_name, dir_path=png_path[0], max_version=version_png) 
            history_path = work_path
        else:
            local_png_path = self.maya_cmd._rename_file(png_path[-1], file_name=file_name_str, dir_path=png_path[0])
            history_path = os.path.join(work_path, "history")
        # 提交材质文件夹
        if self.get_material_path():
            self.feedback.append("<font color=\"#00ff00\">"+u"上传材质文件>>>"+"</font>")
            local_material_path = self.get_material_path()
            current_material_path = os.path.split(local_material_path)
            work_material_path = self.maya_cmd._rename_file(current_material_path[-1], file_name=file_name_str, dir_path=work_path.replace("work", "Texture"))
            material_history_path = history_path.replace("work", "Texture")
            tex_file = self.judgment_file(work_material_path, material_history_path, current_material_path, file_name_str, local_material_path)
        # 提交fbx或abc文件
        if self.get_appendix_path():           
            appendix_list = self.get_appendix_path()
            out_file_lst = list()
            for local_appendix_path in appendix_list:
                current_appendix_path = os.path.split(local_appendix_path)
                if local_appendix_path.endswith(".abc"):
                    self.feedback.append("<font color=\"#00ff00\">"+u"上传abc文件>>>"+"</font>")
                    cache_path = work_path.replace("work", "cache")
                    appendix_abc_file = self.maya_cmd._rename_file(current_appendix_path[-1], file_name=current_appendix_path[-1].split(".")[0], dir_path=cache_path)
                    abc_path = self.judgment_file(appendix_abc_file, os.path.join(cache_path, "history"), current_appendix_path, file_name, local_appendix_path, count_number)
                    out_file_lst.append(abc_path)                
                elif local_appendix_path.endswith(".fbx"):
                    self.feedback.append("<font color=\"#00ff00\">"+u"上传fbx文件>>>"+"</font>")
                    appendix_fbx_path = self.maya_cmd._rename_file(current_appendix_path[-1], file_name=file_name_str, dir_path=work_path)                  
                    fbx_path = self.judgment_file(appendix_fbx_path, history_path, current_appendix_path, file_name_str, local_appendix_path)
                    out_file_lst.append(fbx_path)
                else:
                    pass
            self.super_animation_tree(local_png_path, "{0}_{1}".format(self._data_dict["comparison_information"]["asset_entity"], self._data_dict["comparison_information"]["task_entity"]), local_work_path, save_path, output_lst=out_file_lst)
        # 提交工程文件
        self.feedback.append("<font color=\"#00ff00\">"+u"上传工程文件>>>"+"</font>")
        if version_png:
            work_ma_file = self.maya_cmd._rename_file(current_work_file[-1], file_name=file_name, dir_path=work_path, max_version="v{}".format("1".zfill(count_number)))
            save_path = self.judgment_file(work_ma_file, history_path, current_work_file, file_name, local_work_path, count_number)
            self.feedback.append("<font color=\"#00ff00\">"+u"保存文件>>>"+"</font>")
            cmds.file(save=True)
            self.super_animation_tree(local_png_path, "{0}_{1}".format(self._data_dict["comparison_information"]["asset_entity"], self._data_dict["comparison_information"]["task_entity"]), local_work_path, save_path)
        else:
            work_ma_file = self.maya_cmd._rename_file(current_work_file[-1], file_name=file_name, dir_path=work_path)  
            save_path = self.judgment_file(work_ma_file, history_path, current_work_file, file_name_str, local_work_path)
            self.super_geometry_tree(file_name, local_work_path, save_path, tex_file=tex_file)        
        # 上传审核文件
        shutil.move(os.path.join(png_path[0], png_path[-1]), local_png_path)
        self.feedback.append("<font color=\"#00ff00\">"+u"上传审核文件>>>"+"</font>")
        self.m_tw.task.submit(db=_db, module=self._data_dict["comparison_information"]["module"], id=_id[0], path_list=[local_png_path], note=note, submit_type='review')
        os.unlink(local_png_path)
        self.info_widget_show.setEnabled(False)
        self.project_widget_show.setEnabled(False)
        self.test_widget_show.setEnabled(False)
        self.screen_widget_show.setEnabled(False)
        self.file_widget_show.setEnabled(False)
        self.transmit_widget_show.setEnabled(False)
        self.feedback.append("<font color=\"#00ff00\">"+u"上传完成^_^"+"</font>")

    def judgment_file(self, work_file, history_path, current_file, file_name_str, local_file_path, _fill=2):
        """
            funtional: 迭代版本
            return: 工程文件和带版本号的文件
        """
        # 文件迭代版本
        if os.path.isfile(local_file_path):
            if os.path.isfile(work_file):
                if history_path in work_file:
                    version_file_name = self.find_new_file(history_path, current_file[-1], file_name_str, _fill= _fill)[0]
                    shutil.copy(local_file_path, version_file_name)
                    return version_file_name
                else:
                    if not os.path.isdir(history_path):
                        os.mkdir(history_path)
                    version_file_name = self.find_new_file(history_path, current_file[-1], file_name_str, _fill= _fill)[0]
                    work_json = work_file.replace(".ma", ".json")
                    version_json_name = version_file_name.replace(".ma", ".json")
                    self.operation_cmd.change_json_data(work_json, os.path.split(os.path.splitext(work_json)[0])[-1], os.path.split(os.path.splitext(version_json_name)[0])[-1])
                    shutil.move(work_file, version_file_name)
                    shutil.move(work_json, version_json_name)
                    shutil.copy(local_file_path, work_file)
                    return work_file
            else:
                shutil.copy(local_file_path, work_file)
                return work_file
        # 文件夹迭代版本
        if os.path.isdir(local_file_path):
            if os.path.isdir(work_file):
                if not os.path.isdir(history_path):
                    os.mkdir(history_path)
                version_file_name = self.find_new_file(history_path, current_file[-1], file_name_str, _fill= _fill)[0]
                work_json = work_file + ".json"
                version_json_name = self.find_new_file(history_path, work_json, file_name_str, _fill= _fill)[0]
                # self.operation_cmd.change_json_data(self.operation_cmd.get_json_data(work_json), os.path.split(os.path.splitext(work_json)[0])[-1], os.path.split(os.path.splitext(version_json_name)[0])[-1])
                shutil.move(work_file, version_file_name)
                # shutil.move(work_json, version_json_name)
                shutil.copytree(local_file_path, work_file)
                return work_file
            else:
                shutil.copytree(local_file_path, work_file)
                return work_file

    def find_new_file(self, dir_path, current_file, file_name_str, _fill):
        """
            function: 查找history里的最新文件版本
            return: 带版本号的文件绝对路径
        """
        file_lists = os.listdir(dir_path)
        if not file_lists:
            version_str = "v{}".format("1".zfill(_fill))
            return self.maya_cmd._rename_file(current_file, file_name=file_name_str, max_version=version_str, dir_path=dir_path), version_str
        file_lists.sort(key=lambda fn: os.path.getmtime("{0}/{1}".format(dir, fn)) if os.path.isfile("{0}/{1}".format(dir, fn)) else False)
        history_file_version = file_lists[-1].split(".")[0]
        version_str = "v{}".format(str(int(re.findall(r"\d+", history_file_version)[-1])+1).zfill(_fill))
        file_version_name = self.maya_cmd._rename_file(file_lists[-1], file_name=file_name_str, max_version=version_str)
        return os.path.join(dir_path, file_version_name), version_str 
            
    def super_geometry_tree(self, file_name, local_file, save_path, tex_file=None):
        """
            input: file_name = 角色文件名, save_path = json保存的文件路径
            output: 关于资产模型层级的json文件
        """
        _tree = dict()
        if cmds.ls(sl=True):
            grp_lst = cmds.ls(sl=True)
        else:
            grp_lst = ["Geometry"]
        for grp in grp_lst:
            self.maya_cmd.get_hierarchy_tree(grp, _tree)
        _tree["local"] = local_file
        _tree["submit"] = save_path
        _tree["submit_tex"] = tex_file
        result = {file_name: _tree}
        if save_path.endswith(".ma") or save_path.endswith(".fbx"):           
            self.operation_cmd.save_json_data(self.operation_cmd.replace_file_extension(save_path, "json"), result)

    def super_animation_tree(self, playblast_path, cam_name, local_file, save_path, output_lst=None):
        """
            input: playblast_path = 拍屏的路径, cam_name = 镜头相机名, local_file = 本地文件位置, save_path=当前提交文件的绝对路径, 
            output: 关于镜头动画信息的json文件
        """
        animation_data = dict()
        time_start, time_end = self.maya_cmd.get_animation_time()
        current_fps = self.maya_cmd.get_current_fps()
        result = OrderedDict([
            ("camera", cam_name),
            ("start", time_start),
            ("end", time_end),
            ("fps", current_fps),
            ("local", local_file),
            ("submit", save_path),
            ("video", os.path.split(playblast_path)[-1]),
            ("output", output_lst)
        ])
        animation_data[os.path.split(save_path)[-1].split(".")[0]] = result
        if save_path.endswith(".ma") or save_path.endswith(".fbx"):
            self.operation_cmd.save_json_data(self.operation_cmd.replace_file_extension(save_path, "json"), animation_data)

    def screen_shot(self):
        """
            拍屏, 并保存图片
        """
        if self.get_screen_path():
            try:
                os.unlink(self.get_screen_path())
            except:
                pass
        self.time_data = time.strftime("%Y%m%d%H%M%S", time.localtime())
        file_dir_str = file_dir.replace("\\", "/")
        clipboard = QApplication.clipboard()
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            grab = subprocess.Popen('rundll32.exe {}/PrScrn.dll PrScrn'.format(file_dir_str), startupinfo=startupinfo)
        else:
            startupinfo = None
        grab.wait() 
        dataImage = clipboard.pixmap()
        png_file_name = "D:\{}.png".format(self.time_data)
        self.screenshot_path.setText(png_file_name)
        dataImage.save(png_file_name)

    def import_path(self):
        """
            将制作文件写入对应的文本框
        """
        self.file_path.setText(self.make_file_path())

    def make_file_path(self):
        """
            return: 返回制作文件的绝对路径
        """
        dir_path = self.maya_cmd.get_file_name(full_path=True, dir_path=True)
        file_name = self.maya_cmd.get_file_name()
        abs_path = os.path.join(dir_path, file_name)
        if abs_path:
            return abs_path

    def get_file_describe(self):
        if not self.file_describe:
            return
        return self.file_describe.toPlainText()

    def get_screen_path(self):
        if not self.screenshot_path:
            return
        return self.screenshot_path.text()
    
    def get_work_path(self):
        if not self.file_path:
            return
        return self.file_path.text()

    def get_material_path(self):
        if not self.material_path:
            return
        return self.material_path.text()
    
    def get_appendix_path(self):
        if not self.appendix_path:
            return
        item_list = list()
        _count = self.appendix_path.count()
        for c in range(_count):
            item_list.append(self.appendix_path.item(c).text())  
        return item_list