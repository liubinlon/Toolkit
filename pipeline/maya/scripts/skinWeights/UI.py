import maya.cmds as mc

import skinWeights.loadSkinWeights as loadSkinWeights
reload(loadSkinWeights)


def do():
    if mc.window("SkinWeightlUI", q = 1, ex = 1):
	    mc.deleteUI("SkinWeightlUI", window = 1) 
    window = mc.window("SkinWeightlUI",title="SkinWeightlUI", s = 1,wh = [100,500])
    mc.columnLayout( adj=True )
    
    mc.separator( style='none',h=20 )
    mc.button( h = 30, l = "Export Skin Weight", c = lambda *arg:loadSkinWeights.storeSkinWeight(), bgc = [0.675, 0.663, 0.843])
    mc.separator( style='none',h=20 )
    mc.button( h = 30, l = "Import Skin Weight", c = lambda *arg:loadSkinWeights.writeSkinWeight(), bgc = [0.675, 0.663, 0.843])
    mc.separator( style='none',h=20 )
    mc.setParent("..");
    mc.showWindow( window )
       
do() 
