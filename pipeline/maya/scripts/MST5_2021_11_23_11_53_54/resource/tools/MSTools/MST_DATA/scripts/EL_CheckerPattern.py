'''
EL Checker Pattern v2.0
Author: Erik Lehmann 
v2.0 by JBY QQ179454962
Copyright (c) 2019 Erik Lehmann
Email: contact(at)eriklehmann.com
'''

import maya.cmds as mc
import math
from functools import partial
import os, sys

class MainClassElCheckerPattern:    

    def __init__(self):
        self.elCheckerPatternWinID = "elCheckerPatternWin"
        self.elCheckerPatternLayoutSizeWinID = "elCheckerPatternLayoutArrangeSizeWin"
        self.elCheckerPatternCPscriptPath = os.path.dirname(os.path.realpath(__file__))+'/allUVs/'
        
        self.elCheckerPatternGreen = (0.3, 0.50, 0.40)
        self.elCheckerPatternGrey = (0.3, 0.3, 0.3)
        
        self.elCheckerPatternMayaVersion = mc.about(q=True, v=True)
        if '2018' in self.elCheckerPatternMayaVersion or '2019' in self.elCheckerPatternMayaVersion:
            self.elCheckerPatternArrowUp = 'moveUVUp.png'
            self.elCheckerPatternArrowDown = 'moveUVDown.png'
        elif '2017' in self.elCheckerPatternMayaVersion:
            self.elCheckerPatternArrowUp = 'nodeGrapherArrowUp.png'
            self.elCheckerPatternArrowDown = 'nodeGrapherArrowDown.png'
        else:
            self.elCheckerPatternArrowUp = 'arrowUp.png'
            self.elCheckerPatternArrowDown = 'arrowDown.png'
        
        self.elCheckerPatternUI()

    def elCheckerPatternUI(self, _=False):    


        if (mc.window(self.elCheckerPatternWinID, exists=True)):
            mc.deleteUI(self.elCheckerPatternWinID, wnd=True)
            mc.windowPref(self.elCheckerPatternWinID, r=True)

        mc.window(self.elCheckerPatternWinID, s=False, tlb=True, t="EL Checker Pattern v2.0")
        mc.columnLayout(adj=True)

        mc.rowLayout(nc=6)
        mc.text(l='', w=145, h=20)
                     
        mc.symbolButton(image='%s' % self.elCheckerPatternArrowUp, w=25, h=25,
        ann='Collapse all tabs', 
        c=lambda *_:self.elCheckerPatternCollapseTabs(elCheckerPatternCollapseTabsVal=True, elCheckerPatternTabWinSize=50))
        
        mc.symbolButton(image='%s' % self.elCheckerPatternArrowDown, w=25, h=25,
        ann='Expand all tabs', 
        c=lambda *_:self.elCheckerPatternCollapseTabs(elCheckerPatternCollapseTabsVal=False, elCheckerPatternTabWinSize=150))
        
        mc.symbolButton(image='nodeGrapherModeAllLarge.png', w=25, h=25,
        ann="Open 'About' window with information about the toolkit", 
        c=lambda *_:ElCheckerPatternAboutClass())
        
        mc.setParent(top=True)

        self.elCheckerPatternTMUVCP = mc.frameLayout(l="Checker Pattern", bgc=self.elCheckerPatternGrey, cll=True, cl=False, 
        cc=partial(self.elCheckerPatternResWin, elCheckerPatternClValue=99), ec=partial(self.elCheckerPatternResWin, elCheckerPatternClValue=(-99)))
        mc.columnLayout(adj=True)
        
        mc.rowLayout(nc=2)
        mc.button(l="Create / Del", w=110, h=30, bgc=self.elCheckerPatternGreen, ann='LMB: Create Shader // MMB: Delete Shader',
        c = self.elCheckerPatternCPcreateShader, dgc = lambda *_:self.elCheckerPatternCPdeleteShader() )
        
        mc.button(l="Un / Assign", w=110, h=30, ann='LMB: Assign Shader // MMB: Unassign Shader', 
        c = self.elCheckerPatternCPassignShader, dgc = lambda *_:self.elCheckerPatternCPremoveShader())
        

        mc.setParent('..')
        self.theAllPicsMenu = mc.optionMenu( label='Textures', changeCommand=self.MST_changeTexture,h=30)
        theAllPics = mc.getFileList (fld = self.elCheckerPatternCPscriptPath,fs='*.png')

        for one in theAllPics:
            mc.menuItem( label=one)

        mc.rowLayout(nc=3)
        mc.button(l='1 K', w=73, h=30, c = self.elCheckerPatternCPset1K, ann='Set texture map size to 1K')
        mc.button(l='2 K', w=73, h=30, c = self.elCheckerPatternCPset2K, ann='Set texture map size to 2K')
        mc.button(l='4 K', w=72, h=30, c = self.elCheckerPatternCPset4K, ann='Set texture map size to 4K')
        mc.setParent('..')
        
        mc.rowLayout(nc=3)
        mc.button(l='8 K', w=73, h=30, c = self.elCheckerPatternCPset8K, ann='Set texture map size to 8K')
        mc.button(l='16 K', w=73, h=30, c = self.elCheckerPatternCPset16K, ann='Set texture map size to 16K')
        mc.button(l='32 K', w=72, h=30, c = self.elCheckerPatternCPset32K, ann='Set texture map size to 32K')
        mc.setParent(top=True)

        mc.showWindow(self.elCheckerPatternWinID)
        mc.window(self.elCheckerPatternWinID, e=True, w=228, h=180)
    
    def MST_changeTexture(self,*args):
        getTexName = mc.optionMenu(self.theAllPicsMenu,q=True,v=True)
        getNowFullPath = mc.getAttr("MAT_checkerPatternTex.fileTextureName")
        getOldTexList = os.path.split(getNowFullPath)
        if getOldTexList:
            getOldTex = getOldTexList[-1]
            getOldDir = getOldTexList[0]
            mc.setAttr("MAT_checkerPatternTex.fileTextureName", getOldDir+'/'+getTexName, type='string')
        
    
    def elCheckerPatternResWin(self, elCheckerPatternClValue, _=False):
        elCheckerPatternWinSize = mc.window(self.elCheckerPatternWinID, q=True, h=True)
        mc.window(self.elCheckerPatternWinID, e=True, h=(elCheckerPatternWinSize-elCheckerPatternClValue))
    
    
    def elCheckerPatternCollapseTabs(self, elCheckerPatternCollapseTabsVal, elCheckerPatternTabWinSize, _=False):
        mc.frameLayout(self.elCheckerPatternTMUVCP, e=True, cl=elCheckerPatternCollapseTabsVal)
        mc.window(self.elCheckerPatternWinID, e=True, h=elCheckerPatternTabWinSize)
       
    def elCheckerPatternCPcreateShader(self, _=False):

        elCheckerPatternCPshader = mc.shadingNode('surfaceShader', asShader=True, n="MAT_checkerPattern")
        elCheckerPatternCPfileNode = mc.shadingNode('file', asTexture=True, n="MAT_checkerPatternTex")
        elCheckerPatternCPnode = mc.shadingNode('place2dTexture', asUtility=True, n="MAT_checkerPattern_place2D")
        elCheckerPatternCPSG = mc.sets(r=True, nss=True, em=True, n="MAT_checkerPatternSG")

        mc.connectAttr(elCheckerPatternCPshader + '.outColor', elCheckerPatternCPSG + '.surfaceShader', f=True)
        mc.connectAttr(elCheckerPatternCPfileNode + '.outColor', elCheckerPatternCPshader + '.outColor', f=True)
        
        mc.connectAttr(elCheckerPatternCPnode + ".coverage", elCheckerPatternCPfileNode + ".coverage", f=True)
        mc.connectAttr(elCheckerPatternCPnode + ".translateFrame", elCheckerPatternCPfileNode + ".translateFrame", f=True)
        mc.connectAttr(elCheckerPatternCPnode + ".rotateFrame", elCheckerPatternCPfileNode + ".rotateFrame", f=True)
        mc.connectAttr(elCheckerPatternCPnode + ".mirrorU", elCheckerPatternCPfileNode + ".mirrorU", f=True)
        mc.connectAttr(elCheckerPatternCPnode + ".mirrorV", elCheckerPatternCPfileNode + ".mirrorV", f=True)
        mc.connectAttr(elCheckerPatternCPnode + ".stagger", elCheckerPatternCPfileNode + ".stagger", f=True)
        mc.connectAttr(elCheckerPatternCPnode + ".wrapU", elCheckerPatternCPfileNode + ".wrapU", f=True)
        mc.connectAttr(elCheckerPatternCPnode + ".wrapV", elCheckerPatternCPfileNode + ".wrapV", f=True)
        mc.connectAttr(elCheckerPatternCPnode + ".repeatUV", elCheckerPatternCPfileNode + ".repeatUV", f=True) 
        mc.connectAttr(elCheckerPatternCPnode + ".offset", elCheckerPatternCPfileNode + ".offset", f=True)
        mc.connectAttr(elCheckerPatternCPnode + ".rotateUV", elCheckerPatternCPfileNode + ".rotateUV", f=True)
        mc.connectAttr(elCheckerPatternCPnode + ".noiseUV", elCheckerPatternCPfileNode + ".noiseUV", f=True) 
        mc.connectAttr(elCheckerPatternCPnode + ".vertexUvOne", elCheckerPatternCPfileNode + ".vertexUvOne", f=True)
        mc.connectAttr(elCheckerPatternCPnode + ".vertexUvTwo", elCheckerPatternCPfileNode + ".vertexUvTwo", f=True)
        mc.connectAttr(elCheckerPatternCPnode + ".vertexUvThree", elCheckerPatternCPfileNode + ".vertexUvThree", f=True)
        mc.connectAttr(elCheckerPatternCPnode + ".vertexCameraOne", elCheckerPatternCPfileNode + ".vertexCameraOne", f=True)
        mc.connectAttr(elCheckerPatternCPnode + ".outUV", elCheckerPatternCPfileNode + ".uv", f=True)
        mc.connectAttr(elCheckerPatternCPnode + ".outUvFilterSize", elCheckerPatternCPfileNode + ".uvFilterSize", f=True)
        
        

                        
        
        elCheckerPatternCPtexturePath = self.elCheckerPatternCPscriptPath + 'UVCheckerMap01-1024.png'

        mc.setAttr("MAT_checkerPatternTex.fileTextureName", elCheckerPatternCPtexturePath, type='string')

    def elCheckerPatternCPassignShader(self, _=False):
        mc.sets(e=True, fe='MAT_checkerPatternSG')

    def elCheckerPatternCPremoveShader(self, _=False):
        mc.sets(e=True, fe='initialShadingGroup')

    def elCheckerPatternCPdeleteShader(self, _=False):
        mc.hyperShade(objects="MAT_checkerPattern")
        mc.sets(e=True, fe='initialShadingGroup')
        mc.select('MAT_checkerPattern', 'MAT_checkerPatternTex', 'MAT_checkerPattern_place2D', 'MAT_checkerPatternSG', r=True, ne=True)
        mc.delete()

    def elCheckerPatternCPset1K(self, _=False):
        mc.setAttr("MAT_checkerPattern_place2D.repeatU", 1)
        mc.setAttr("MAT_checkerPattern_place2D.repeatV", 1)

    def elCheckerPatternCPset2K(self, _=False):
        mc.setAttr("MAT_checkerPattern_place2D.repeatU", 2)
        mc.setAttr("MAT_checkerPattern_place2D.repeatV", 2)

    def elCheckerPatternCPset4K(self, _=False):
        mc.setAttr("MAT_checkerPattern_place2D.repeatU", 4)
        mc.setAttr("MAT_checkerPattern_place2D.repeatV", 4)

    def elCheckerPatternCPset8K(self, _=False):
        mc.setAttr("MAT_checkerPattern_place2D.repeatU", 8)
        mc.setAttr("MAT_checkerPattern_place2D.repeatV", 8)

    def elCheckerPatternCPset16K(self, _=False):
        mc.setAttr("MAT_checkerPattern_place2D.repeatU", 16)
        mc.setAttr("MAT_checkerPattern_place2D.repeatV", 16)

    def elCheckerPatternCPset32K(self, _=False):
        mc.setAttr("MAT_checkerPattern_place2D.repeatU", 32)
        mc.setAttr("MAT_checkerPattern_place2D.repeatV", 32)

class ElCheckerPatternAboutClass:    

    def __init__(self):
        self.elCheckerPatternAboutWinID = "elCheckerPatternWinAbout"
        self.elCheckerPatternAboutUI()

    def elCheckerPatternAboutUI(self, _=False):    

        if (mc.window(self.elCheckerPatternAboutWinID, exists=True)):
            mc.deleteUI(self.elCheckerPatternAboutWinID, wnd=True)
            mc.windowPref(self.elCheckerPatternAboutWinID, r=True)


        mc.window(self.elCheckerPatternAboutWinID, s=False, tlb=True, t="About")
        mc.columnLayout(adj=True)

        mc.rowLayout(nc=1)
        mc.text(l='', h=10)
        mc.setParent('..')
        
        mc.rowLayout(nc=1)
        mc.text(l='<font color=#3cb777><h3>EL Checker Pattern v1.0</h3></font>', al='center', w=196, h=20)
        mc.setParent('..')
        mc.rowLayout(nc=1)
        mc.text(l='Author: Erik Lehmann \nCopyright (c) 2019 Erik Lehmann', al='center', w=196, h=40)
        mc.setParent('..')
        
        mc.rowLayout(nc=3)
        mc.text(l='', w=11)
        mc.button(l='Open documentation', ann='Documentation page', w=170, h=30,
        c=lambda *_:self.elCheckerPatternAboutOpenBrowser(elCheckerPatternAboutSiteCode='Documentation'))
        mc.text(l='', w=10)
        mc.setParent('..')
        
        mc.rowLayout(nc=1)
        mc.text(l='<font color=#3cb777><h3>Feedback Or Questions?</h3></font>', al='center', w=196, h=35)
        mc.setParent('..')
        
        mc.rowLayout(nc=3)
        mc.text(l='', w=21)
        mc.textField(tx='contact@eriklehmann.com', ebg=False, ed=False, w=150, h=30)
        mc.text(l='', w=21)
        mc.setParent('..')
        
        mc.rowLayout(nc=1)
        mc.text(l='<font color=#3cb777><h3>More About My Work</h3></font>', al='center', w=196, h=35)
        mc.setParent('..')
        
        mc.rowLayout(nc=4)
        mc.text(l='', w=10)
        mc.button(l='Website', ann='Explore the work of Filmmaker and Build TD Erik Lehmann', w=85, h=30,
        c=lambda *_:self.elCheckerPatternAboutOpenBrowser(elCheckerPatternAboutSiteCode='Website'))
        mc.button(l='Gumroad', ann="Find more useful resources for Maya on Gumroad.", w=85, h=30, 
        c=lambda *_:self.elCheckerPatternAboutOpenBrowser(elCheckerPatternAboutSiteCode='Gumroad'))
        mc.text(l='', w=10)
        mc.setParent('..')
        
        mc.rowLayout(nc=4)
        mc.text(l='', w=10)
        mc.button(l='Artstation', ann="Erik Lehmann's Artstation Profile", w=85, h=30,
        c=lambda *_:self.elCheckerPatternAboutOpenBrowser(elCheckerPatternAboutSiteCode='Artstation'))
        mc.button(l='Facebook', ann='The Art Of Erik Lehmann on Facebook', w=85, h=30,
        c=lambda *_:self.elCheckerPatternAboutOpenBrowser(elCheckerPatternAboutSiteCode='Facebook'))
        mc.text(l='', w=10)
        mc.setParent(top=True)
        
        mc.showWindow(self.elCheckerPatternAboutWinID)
        mc.window(self.elCheckerPatternAboutWinID, e=True, w=200, h=290)
        
    def elCheckerPatternAboutOpenBrowser(self, elCheckerPatternAboutSiteCode, _=False):
        if elCheckerPatternAboutSiteCode == 'Documentation':
            mc.launch(web="https://www.eriklehmann.com/documentation")
        elif elCheckerPatternAboutSiteCode == 'Website':
            mc.launch(web="http://www.eriklehmann.com/")
        elif elCheckerPatternAboutSiteCode == 'Gumroad':
            mc.launch(web="https://gumroad.com/eriklehmann")    
        elif elCheckerPatternAboutSiteCode == 'Artstation':
            mc.launch(web="https://www.artstation.com/eriklehmann")
        elif elCheckerPatternAboutSiteCode == 'Facebook':
            mc.launch(web="https://www.facebook.com/TheArtOfErikLehmann/")
MainClassElCheckerPattern()