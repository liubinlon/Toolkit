# SelectBadGeo v1.1
# License: MIT Licence (See LICENSE.txt or https://choosealicense.com/licenses/mit/)
# Copyright (c) 2017 Erik Lehmann
# Date: 01/16/18
#
# Description: 
#	Select Triangles, Quads, N-Gons, Concave, Hole, Lamina and Non Manifold geometry.
# 
# How to use:
#	1. Select object(s).
#	2. Choose geometry type.
#
# Installation: 
# 	1. 	Copy BadGeo.py to '\Users\[USER]\Documents\maya\[MAYAVERSION]\prefs\scripts'
# 	2. 	Launch / Restart Maya
#	3.	Type into 'Script Editor' (Python tab) and execute:
#       import SelectBadGeo as BG
#       MCBG = BG.MainClassBadGeo()
#       MCBG.badGeoUI()
                          

import maya.cmds as cmds
import maya.mel as mel

class MainClassBadGeo:
    	
    def __init__(self):
        self.bG_output = ""      
                
    def badGeoUI(self):

        # C H E C K  W I N D O W
        
        if (cmds.window("bGWin", exists=True)):
        	cmds.deleteUI("bGWin", wnd=True)
        	cmds.windowPref("bGWin", r=True)        	            
            
        # C R E A T E  U I
                
        cmds.window("bGWin", s=False, tlb=True, rtf=True, t="Select Bad Geometry", w = 145)
        cmds.columnLayout(adj=True)
        
     
        # B A D  G E O M E T R Y
        		
        cmds.frameLayout(label=("Geometry Type"), bgc=(0.3, 0.3, 0.3), collapsable=False, collapse=False, w=120)
                    
        cmds.columnLayout(adj=True)
        
        cmds.button(label="Triangles", h=25, c = self.bGTriangles)
        cmds.button(label="Quads", h=25, c = self.bGQuads)
        cmds.button(label="N-Gons", h=25, c = self.bGNGons)
        cmds.button(label="Concave", h=25, c = self.bGConcave)
        cmds.button(label="Lamina", h=25, c = self.bGLamina)
        cmds.button(label="Holes", h=25, c = self.bGHole)
        cmds.button(label="Non-Manifold", h=25, c = self.bGNonM)
        
               
        cmds.setParent("..")
        cmds.setParent("..")
        
        
        # O U T P U T
        
        cmds.frameLayout(label='Output', bgc=(0.3, 0.3, 0.3), collapsable=False, collapse=True)
                
        self.bG_output = cmds.textField(h = 25, bgc=(0.16, 0.16, 0.16), en = True, ed=False)
        
        cmds.setParent("..")
        cmds.setParent("..")

               
        # S H O W  W I N D O W
        
        cmds.showWindow("bGWin")
        
	
	# M E T H O D S
	
	# T R I A N G L E S

    def bGTriangles(self, _=False):
        bGsel = cmds.ls(sl = True) 
        
        # Change to Component mode to retain object highlighting for better visibility               
        cmds.selectMode(q=True, co=True)

        # Select Object/s and Run Script to highlight Triangles
        cmds.polySelectConstraint(m=3 ,t = 0x0008, sz=1)
        cmds.polySelectConstraint(dis=True)
      
        # Update Textfield  
        bGPolys = cmds.polyEvaluate(fc=True)
        
        try:
            cmds.textField(self.bG_output, e=True, tx=("%s Triangle(s)" % int(bGPolys)))        
        except:
            cmds.textField(self.bG_output, e=True, tx=("Nothing is selected."))
                
     
    # Q U A D S
        
    def bGQuads(self, _=False):
        bGsel = cmds.ls(sl = True)
        
        cmds.selectMode(q=True, co=True)
        
        cmds.polySelectConstraint(m=3 ,t = 0x0008, sz=2)
        cmds.polySelectConstraint(dis=True)
        
        bGPolys = cmds.polyEvaluate(fc=True)
        
        try:
            cmds.textField(self.bG_output, e=True, tx=("%s Quad(s)" % int(bGPolys)))
        except:
            cmds.textField(self.bG_output, e=True, tx=("Nothing is selected."))

    
    # N - G O N S
        
    def bGNGons(self, _=False):
        bGsel = cmds.ls(sl = True) 
        
        cmds.selectMode(q=True, co=True)
        
        cmds.polySelectConstraint(m=3 ,t = 0x0008, sz=3)
        cmds.polySelectConstraint(dis=True)
        
        bGPolys = cmds.polyEvaluate(fc=True)
        
        try:
            cmds.textField(self.bG_output, e=True, tx=("%s N-Gon(s)" % int(bGPolys)))
        except:
            cmds.textField(self.bG_output, e=True, tx=("Nothing is selected."))

    # C O N C A V E
        
    def bGConcave(self, _=False):
        
        bGsel = cmds.ls(sl = True) 
        
        cmds.selectMode(q=True, co=True)
        
        cmds.polySelectConstraint(m=3 ,t = 0x0008, c=1)
        cmds.polySelectConstraint(dis=True)
        
        bGPolys = cmds.polyEvaluate(fc=True)
        
        try:
            cmds.textField(self.bG_output, e=True, tx=("%s Concave(s)" % int(bGPolys)))
        except:
            cmds.textField(self.bG_output, e=True, tx=("Nothing is selected."))
    
    # L A M I N A
        
    def bGLamina(self, _=False):
        bGsel = cmds.ls(sl = True) 
        
        cmds.selectMode(q=True, co=True)

        p = cmds.polyInfo(lf=True)

        if p == None:
            bGPolys = 0
            cmds.select(d=True) 
        else:
            cmds.select(p)
            bGPolys = cmds.polyEvaluate(fc=True)
                   
        try:
            cmds.textField(self.bG_output, e=True, tx=("%s Lamina" % int(bGPolys)))
        except:
            cmds.textField(self.bG_output, e=True, tx=("Nothing is selected."))
    
    # H O L E S
        
    def bGHole(self, _=False):
        bGsel = cmds.ls(sl = True) 
        
        cmds.selectMode(q=True, co=True)
        
        cmds.polySelectConstraint(m=3 ,t = 0x0008, h=1)
        cmds.polySelectConstraint(dis=True)
        
        bGPolys = cmds.polyEvaluate(fc=True)
       
        
        try:
            cmds.textField(self.bG_output, e=True, tx=("%s Hole(s)" % int(bGPolys)))
        except:
            cmds.textField(self.bG_output, e=True, tx=("Nothing is selected."))

    # N O N - M A N I F O L D
        
    def bGNonM(self, _=False):
        bGsel = cmds.ls(sl = True) 
                
        cmds.selectMode(q=True, co=True)
        
        bGPolys = mel.eval('polyCleanupArgList 4 { "0","2","1","0","0","0","0","0","0","1e-005","0","1e-005","0","1e-005","0","1","0","0" };')
        
        bGCount = 0
        
        for i in bGPolys:
            bGCount = bGCount + 1
            
        cmds.select(bGPolys)
        
        try:
            cmds.textField(self.bG_output, e=True, tx=("%s Non-Manifold(s)" % bGCount))
        except:
            cmds.textField(self.bG_output, e=True, tx=("Nothing is selected."))
          
        
        
#MCBG = MainClassBadGeo()
#MCBG.badGeoUI()