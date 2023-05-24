#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
'''
   File    :   commonly_operation.py
   Time    :   2022/12/02 16:59:20
   Author  :   Liu ZhenBao
   Version :   1.0
   Contact :   3305510092@qq.com
   Desc    :   None
'''
############################################################################
# import the libraries needed by this script here
import json
import os


# here put the class script
class CommonlyOperation:
    """
        This funtion class that manlpulates file
    """
    @staticmethod
    def replace_file_extension(file_path, extension):
        """
            input: save_path = 文件的绝对路径或带扩展的文件名, extension = 新的扩展类型(os:"json")
            return: 修改后的文件的绝对路径或带扩展的文件名
        """
        path_part = list(os.path.splitext(file_path))
        path_part[-1] = extension
        return ".".join(path_part)
    
    @staticmethod
    def get_json_data(json_abs):
        """
            input: json_abs = json文件的绝对路径
            return: 读取的json数据
        """
        with open(json_abs, "r") as load_f:
            return json.load(load_f)

    @staticmethod
    def save_json_data(json_abs, json_dict):
        """
            input: json_abs = json文件的绝对路径, json_dict = 字典数据
            function: 保存json文件
        """
        with open(json_abs, 'w') as file:
            file.write(json.dumps(json_dict, separators=(",", ": "), indent=4))
    
    @staticmethod
    def change_json_data(_dict, old_key, new_key):
        """
            input: _dict = 需要修改的字典, old_key = 旧的key值, new_key = 新的key值
            return: 新的字典
        """
        attr_lst = ["submit", "submit_tex"]
        dict_data = CommonlyOperation.get_json_data(_dict)
        dict_data[new_key] = dict_data.pop(old_key)
        for _attr in attr_lst:
            if _attr in dict_data[new_key]:
                dict_data[new_key][_attr] = dict_data[new_key][_attr].replace(old_key, "history/{}".format(new_key))
        CommonlyOperation.save_json_data(_dict, dict_data)
    