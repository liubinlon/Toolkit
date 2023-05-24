import maya.cmds as mc
import random

def start():
    
    objSled=mc.ls(sl=1)

    for i in objSled:
        
        lamShader=mc.shadingNode('lambert',asShader=1)
        print lamShader   
        mc.setAttr(lamShader+'.color', random.uniform(0,1), random.uniform(0,1), random.uniform(0,1), type='double3')
        mc.sets(renderable=1 ,noSurfaceShader=1, empty=1, n=lamShader+'SG')
        mc.connectAttr(lamShader+'.outColor', lamShader+'SG.surfaceShader', f=1)
   
        mc.sets(i, e=1, forceElement=lamShader+'SG')
