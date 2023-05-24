# 导出表情数据
import maya.cmds as cmds
import json
import re

def get_time_and_data(out_file, attr_list):
    result = dict()
    time_start = int(cmds.playbackOptions(query=True, min=True))
    time_end = int(cmds.playbackOptions(query=True, max=True))
        
    for attr in attr_list:
        con_dict = list()        
        for time in range(time_start, time_end+1):
            cmds.currentTime(time)                                    
            node_data = cmds.getAttr(attr)
            con_dict.append((time, node_data))
        if attr.index(":"):
            result[attr.split(":")[-1]] = con_dict
        else:
            result[attr] = con_dict
        
    with open(out_file, 'w') as f:
        f.write(json.dumps(result, indent=4))
    
if __name__ == '__main__':
    attr_list = ["blendColors1.blender", "body_BS.s04_02_f1121"]
    out_file = cmds.fileDialog2(fileFilter='*.json', caption='Save Animation To ...')
    if out_file and len(out_file) == 1:
        get_time_and_data(out_file[0], attr_list)
       