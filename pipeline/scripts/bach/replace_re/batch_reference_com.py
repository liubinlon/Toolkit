#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
'''
File    :   batch_reference_com.py
Time    :   2022/11/04 16:41:12
Author  :   ZhenBao Liu
Version :   1.0
Contact :   3305510092@qq.com
Desc    :   None
'''
# import the libraries needed by this script here
import os
import re
import sys
import shutil
import codecs
import time
import threading
import logging
# path = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
# Dir = r"{0}".format(path)
# if Dir not in sys.path:
#     sys.path.append(Dir)

# here put the class script
class ReplaceReferenceCom:
    def __init__(self):
        self.ani_file = None
        self.old_file = None
        self.new_file = None

    def load_file_data(self, latestfile=None, filte=None, new_file_list=None):
        pattern = re.compile('".*?"')
        utf_latestfile = unicode(latestfile, "utf-8")
        with codecs.open(utf_latestfile, "rb", "gbk") as old_file:
            a_lines = old_file.readlines()
            b_lines = a_lines[:]
            for num, line in enumerate(a_lines):   
                if line.count("requires"):
                    break
                if pattern.findall(line):
                    old_ref = pattern.findall(line)[-1][1:-1]
                    if not filte:
                        new_file = self.get_file_name(old_ref, new_file_list)
                        if new_file:
                            b_lines[num] = line.replace(old_ref, new_file)
                    elif old_ref == filte:
                        b_lines[num] = line.replace(filte, new_file_list)
                    else:
                        continue
        with codecs.open(utf_latestfile, "w", "gbk") as new_file:
            for line in b_lines:
                new_file.write(line)
        
        logging.info(f"替换完成文件 - {utf_latestfile}")

    def run_reference(self):
        ani_list = self.get_ani_file_list()
        old_list = self.get_old_file_list()
        new_list = self.get_new_file_list()
        if old_list:            
            for f in ani_list:
                self.load_file_data(latestfile=f, filte=old_list[0], new_file_list=new_list[0])
        else:
            for f in ani_list:
                self.load_file_data(latestfile=f, new_file_list=new_list)

    def get_file_name(self, file_path, file_list):
        for new_file in file_list:
            ma_name = os.path.split(new_file)[-1]
            if str(ma_name) in file_path:
                return new_file


    def get_ani_file_list(self):
        if not self.ani_file:
            return
        item_list = list()
        _count = self.ani_file.count()
        for c in range(_count):
            item_list.append(self.ani_file.item(c).text())  
        return item_list
    
    def get_old_file_list(self):
        if not self.old_file:
            return
        item_list = list()
        _count = self.old_file.count()
        for c in range(_count):
            item_list.append(self.old_file.item(c).text())  
        return item_list
    
    def get_new_file_list(self):
        if not self.new_file:
            return
        item_list = list()
        _count = self.new_file.count()
        for c in range(_count):
            item_list.append(self.new_file.item(c).text())  
        return item_list