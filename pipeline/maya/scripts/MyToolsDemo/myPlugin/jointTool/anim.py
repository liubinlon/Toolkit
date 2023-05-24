# coding=utf-8
# time : 2020/8/10
import maya.cmds as cmds

sel = cmds.ls(sl=True)
t = ":"
for crv in sel:
    s = str(crv).index(t)
    name = crv[:s] + "_anim"
    cmds.file("C:/Users/liuzb/Desktop/anim/%s" % name, force=True,
              options="precision=8;intValue=17;nodeNames=1;verboseUnits=0;whichRange=1;range=0:10;options=keys;hierarchy=none;controlPoints=0;shapes=1;helpPictures=0;useChannelBox=0;copyKeyCmd=-animation objects -option keys -hierarchy none -controlPoints 0 -shape 1",
              typ="animExport", preserveReferences=True, exportSelected=True)
