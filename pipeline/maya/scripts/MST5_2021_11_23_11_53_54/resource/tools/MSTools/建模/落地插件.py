############################################################################################
'''
Snap To Ground Tool
--------------------------------------------------------------------------------------------
Author: Ryan Nolan
Contact: RyanNolan3D@gmail.com
--------------------------------------------------------------------------------------------
Usage:
Select your ground object and "set surface to snap to"
NOTE: Ground must have some sort of UVs for script to work
Then "Snap objects"
Note: It's recommended to move your objects above the ground. Objects below the ground will
	be ignored
'''
############################################################################################
import maya .cmds as OOO0O0O0OO000OO00 #line:1
import maya .mel as OOO0OOO000OOOOOO0 #line:2
import copy as OOO0OOOOOO0O0O0OO #line:4
import maya .OpenMayaUI as O0O0OOO00000O0O0O #line:5
import maya .OpenMaya as O0O0OO0000O00O00O #line:6
import os as OOO00O000OO0OO00O #line:8
__all__ =[]#line:10
class OOOO00O00OOOO0OO0 ():#line:12
	terrain =""#line:13
	def __init__ (OO0OOO000OO00OO0O ):#line:15
		OO0OOO000OO00OO0O .createWindow ()#line:16
	def SetSurfaceObj (OO0O000O0O00O00OO ,*OO00O0OOO000O0O00 ):#line:18
		OO0O000O0O00O00OO .terrain =OOO0O0O0OO000OO00 .ls (sl =True ,o =True )#line:19
		print (OO0O000O0O00O00OO .terrain )#line:20
		print ("Surface terrain set")#line:21
	def Snap (OOOOOO000O0OOO0O0 ,*OOO00000O0OOOOO00 ):#line:24
		O00OOO000O00O0OOO =OOO0O0O0OO000OO00 .ls (sl =True )#line:25
		OOO0O0O0OO000OO00 .undoInfo (st =False )#line:26
		for O00OO000O0OOOOOO0 in O00OOO000O00O0OOO :#line:28
			O00000OO00O00OOOO =OOO0O0O0OO000OO00 .getAttr (O00OO000O0OOOOOO0 +".translate")#line:30
			OOOOO00O00OOO00O0 =O00OO0OO00000OO00 (OOOOOO000O0OOO0O0 .terrain [0 ],O00000OO00O00OOOO [0 ],[0 ,-1 ,0 ])#line:31
			if OOOOO00O00OOO00O0 !=None :#line:33
				OOO0O0O0OO000OO00 .setAttr ((O00OO000O0OOOOOO0 +".translateY"),OOOOO00O00OOO00O0 ['hit'][1 ])#line:34
		OOO0O0O0OO000OO00 .undoInfo (st =True )#line:36
	def createWindow (O00OO0O0O00O0O000 ):#line:38
		if OOO0O0O0OO000OO00 .window ("SnapToGroundTool",exists =True ):#line:40
			OOO0O0O0OO000OO00 .deleteUI ("SnapToGroundTool")#line:41
		if OOO0O0O0OO000OO00 .windowPref ("SnapToGroundTool",exists =True ):#line:43
			OOO0O0O0OO000OO00 .windowPref ("SnapToGroundTool",remove =True )#line:44
		OOO0O0O0OO000OO00 .window ("SnapToGroundTool",title ="Snap To Ground Tool")#line:46
		OOO0O0O0OO000OO00 .columnLayout (rs =5 )#line:48
		OOO0O0O0OO000OO00 .button (w =200 ,h =30 ,label ="设置吸附表面",c =O00OO0O0O00O0O000 .SetSurfaceObj )#line:49
		OOO0O0O0OO000OO00 .button (w =200 ,h =30 ,label ="设置物体",c =O00OO0O0O00O0O000 .Snap )#line:50
		OOO0O0O0OO000OO00 .showWindow ("SnapToGroundTool")#line:52
def O00OO0OO00000OO00 (OOOOO0OO000OOOO00 ,O00OO00OO00O00OO0 ,OO00000OOOO0O000O ,OO00O0000O00O0000 =1000 ):#line:54
    O00000O0OOO0O0OO0 =O0O0OO0000O00O00O .MSelectionList ()#line:56
    O00000O0OOO0O0OO0 .add (OOOOO0OO000OOOO00 )#line:59
    OO0O00OOOOOOOO0O0 =O0O0OO0000O00O00O .MDagPath ()#line:62
    O00000O0OOO0O0OO0 .getDagPath (0 ,OO0O00OOOOOOOO0O0 )#line:66
    OOO0OO0OOO00000O0 =O0O0OO0000O00O00O .MFnMesh (OO0O00OOOOOOOO0O0 )#line:70
    O00OO00OO00O00OO0 =O0O0OO0000O00O00O .MFloatPoint (O00OO00OO00O00OO0 [0 ],O00OO00OO00O00OO0 [1 ],O00OO00OO00O00OO0 [2 ])#line:73
    O000O0000O0O0OOOO =O0O0OO0000O00O00O .MFloatVector (OO00000OOOO0O000O [0 ],OO00000OOOO0O000O [1 ],OO00000OOOO0O000O [2 ])#line:76
    O0O000000OO0OOOOO =O0O0OO0000O00O00O .MFloatPoint ()#line:79
    OOO00OO00OO0O0000 =False #line:81
    OOO0OO0O00O0O00OO =O0O0OO0000O00O00O .MDistance .internalToUI (1000000 )#line:82
    O00OOO0O0000OO000 =False #line:83
    OOOOOO000O0OOOOO0 =None #line:84
    OO000O0O0OOO00000 =None #line:85
    O0O0OOO00O0O0000O =None #line:86
    O0O00OOO000O0000O =None #line:87
    O00000O00O0000000 =None #line:88
    O00O000OOO0000O0O =None #line:89
    O0OOO0O00O00OOOOO =None #line:90
    O00O00O0O0000O00O =None #line:91
    O0O0O000OOO00OOOO =OOO0OO0OOO00000O0 .closestIntersection (O00OO00OO00O00OO0 ,O000O0000O0O0OOOO ,OOOOOO000O0OOOOO0 ,OO000O0O0OOO00000 ,OOO00OO00OO0O0000 ,O0O0OO0000O00O00O .MSpace .kWorld ,OOO0OO0O00O0O00OO ,O00OOO0O0000OO000 ,O0O0OOO00O0O0000O ,O0O000000OO0OOOOO ,O0O00OOO000O0000O ,O00000O00O0000000 ,O00O000OOO0000O0O ,O0OOO0O00O00OOOOO ,O00O00O0O0000O00O )#line:100
    if O0O0O000OOO00OOOO :#line:103
        O00000000O0O0OOO0 =O0O0OO0000O00O00O .MPoint (O0O000000OO0OOOOO )#line:104
        OO000OOO0O0OO000O =[0.0 ,0.0 ]#line:105
        O0O0000OOOOOOOO00 =O0O0OO0000O00O00O .MScriptUtil ()#line:106
        O0O0000OOOOOOOO00 .createFromList (OO000OOO0O0OO000O ,2 )#line:107
        O0OOOOOO0OOOOO0O0 =O0O0000OOOOOOOO00 .asFloat2Ptr ()#line:108
        O0OO000000O00O0O0 =None #line:109
        O0OO0OOO0OO0O0O00 =None #line:110
        OO00OOOOOO0OO00OO =OOO0OO0OOO00000O0 .getUVAtPoint (O00000000O0O0OOO0 ,O0OOOOOO0OOOOO0O0 ,O0O0OO0000O00O00O .MSpace .kWorld )#line:111
        OO0OOOOO0OOOO00O0 =O0O0OO0000O00O00O .MScriptUtil .getFloat2ArrayItem (O0OOOOOO0OOOOO0O0 ,0 ,0 )or False #line:113
        O0OOOO0O0000O0000 =O0O0OO0000O00O00O .MScriptUtil .getFloat2ArrayItem (O0OOOOOO0OOOOO0O0 ,0 ,1 )or False #line:114
        if OO0OOOOO0OOOO00O0 and O0OOOO0O0000O0000 :#line:115
            return {'hit':[O0O000000OO0OOOOO .x ,O0O000000OO0OOOOO .y ,O0O000000OO0OOOOO .z ],'source':[O00OO00OO00O00OO0 .x ,O00OO00OO00O00OO0 .y ,O00OO00OO00O00OO0 .z ],'uv':[OO0OOOOO0OOOO00O0 ,O0OOOO0O0000O0000 ]}#line:116
        else :#line:117
            return {'hit':[O0O000000OO0OOOOO .x ,O0O000000OO0OOOOO .y ,O0O000000OO0OOOOO .z ],'source':[O00OO00OO00O00OO0 .x ,O00OO00OO00O00OO0 .y ,O00OO00OO00O00OO0 .z ],'uv':False }#line:118
    else :#line:119
        return None #line:120
OOOO00O00OOOO0OO0 ()

#===============================================================#
# Obfuscated by Oxyry Python Obfuscator (http://pyob.oxyry.com) #
#===============================================================#
