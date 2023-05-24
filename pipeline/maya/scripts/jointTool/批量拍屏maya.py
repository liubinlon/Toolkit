import maya.cmds as cmds
import maya.mel as mel
import os 
import pymel.core as pm


dir = r"D:\rig\test"

def get_timeslider_time():
    return [int(pm.playbackOptions(ast=True, query=True)), int(pm.playbackOptions(min=True, query=True)),\
    int(pm.playbackOptions(max=True, query=True)),int(pm.playbackOptions(aet=True, query=True))]

time = get_timeslider_time()

def getFile(dir,suffix):
    suffix = suffix
    newname = []
    res = []
    for root, directory, files in os.walk(dir):
        for filename in files:
            name, suf = os.path.splitext(filename)
            if suf == suffix:
                res.append(os.path.join(root, filename))
                newname.append(os.path.join(root, name))
    return res, newname
    
filelist = getFile(dir, ".ma")
newfile = filelist[0]    

for num in range(len(newfile)):
    namestr = newfile[num]
    cmds.file("%s" % namestr, f = True, options = "v=0;", ignoreVersion = True, typ = "mayaAscii", o = True)
    cmds.playblast(format = "qt", filename = "%s.mov" % filelist[1][num], forceOverwrite = True, sequenceTime = 0, clearCache = 0, viewer = 1, showOrnaments = 1, fp = 4, percent = 100, compression = "H.264", quality = 100)   