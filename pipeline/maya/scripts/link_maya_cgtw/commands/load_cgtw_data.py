#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
'''
   File    :   load_cgtw_data.py
   Time    :   2022/12/07 10:12:21
   Author  :   Liu ZhenBao
   Version :   1.0
   Contact :   3305510092@qq.com
   Desc    :   根据资产名字和环节获取对应的项目数据库, 并获取环节需要的不同数据
'''
############################################################################

# import the libraries needed by this script here
import os
import sys

cgtw_dir = r"C:/CgTeamWork_v6/bin/base"
file_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

if dir not in sys.path:
    sys.path += [cgtw_dir, file_dir]

import cgtw2
# here put the class script

class LoadCgData:
    def __init__(self):
        self._data_dict = dict()
        self.m_tw = cgtw2.tw()
    
    def split_tab(self, _tab):
        """
            对数据库获得的数据进行拆分
        """
        if _tab:
            _tab_str = _tab.split(".")
        return _tab_str[-1]
    
    def get_user_data(self):
        """
            获取登录用户所在的组、用户名, 添加到字典self._data_dict
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