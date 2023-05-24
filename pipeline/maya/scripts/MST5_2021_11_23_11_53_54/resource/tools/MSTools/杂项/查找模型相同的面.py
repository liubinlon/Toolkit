import struct, pymel.core 
import maya.OpenMaya as OpenMaya 
import maya.cmds as mc

aaa = mc.ls(sl = True)
dagpath  = pymel.core.PyNode(aaa[0]).__apiobject__() 
iterator = OpenMaya.MItMeshPolygon(dagpath) 


selection = OpenMaya.MSelectionList() 
md5_lst = list() 
while not iterator.isDone(): 
    center = iterator.center() 
    md5 = struct.pack('dddd', round(center.x, 4), round(center.y, 4), round(center.z, 4), round(center.w, 4)).encode('hex') 

    if md5 in md5_lst: 
        selection.add(dagpath, iterator.currentItem()) 

    md5_lst.append(md5) 
    iterator.next() 


OpenMaya.MGlobal.setActiveSelectionList(selection)