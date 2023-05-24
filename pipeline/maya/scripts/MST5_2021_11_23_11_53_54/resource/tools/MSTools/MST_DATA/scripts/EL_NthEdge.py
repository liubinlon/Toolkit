'''
EL_NthEdge v1.0
Author: Erik Lehmann
Copyright (c) 2019 Erik Lehmann
Email: contact(at)eriklehmann.com
'''

import maya.cmds as mc
import maya.mel as mm
from functools import partial

class MainClassElNthEdge:    

    def __init__(self):
        self.elNthEdgeWinID = "elNthEdgeWin"
        self.elNthEdgeGreen = (0.3, 0.50, 0.40)
        self.elNthEdgeGrey = (0.3, 0.3, 0.3)
        
        self.elNthEdgeMayaVersion = mc.about(q=True, v=True)
        if '2018' in self.elNthEdgeMayaVersion or '2019' in self.elNthEdgeMayaVersion:
            self.elNthEdgeArrowUp = 'moveUVUp.png'
            self.elNthEdgeArrowDown = 'moveUVDown.png'
        elif '2017' in self.elNthEdgeMayaVersion:
            self.elNthEdgeArrowUp = 'nodeGrapherArrowUp.png'
            self.elNthEdgeArrowDown = 'nodeGrapherArrowDown.png'
        else:
            self.elNthEdgeArrowUp = 'arrowUp.png'
            self.elNthEdgeArrowDown = 'arrowDown.png'
        
        self.elNthEdgeUI()

    def elNthEdgeUI(self, _=False):    

        if (mc.window(self.elNthEdgeWinID, exists=True)):
            mc.deleteUI(self.elNthEdgeWinID, wnd=True)
            mc.windowPref(self.elNthEdgeWinID, r=True)

        mc.window(self.elNthEdgeWinID, s=False, tlb=True, t="EL Nth Edge v1.0")
        mc.columnLayout(adj=True)

        mc.rowLayout(nc=4)
        mc.text(l='', w=156, h=20)
                     
        mc.symbolButton(image='%s' % self.elNthEdgeArrowUp, w=25, h=25, 
        c=lambda *_:self.elNthEdgeCollapseTabs(elNthEdgeCollapseTabsVal=True, elNthEdgeTabWinSize=50))
        
        mc.symbolButton(image='%s' % self.elNthEdgeArrowDown, w=25, h=25, 
        c=lambda *_:self.elNthEdgeCollapseTabs(elNthEdgeCollapseTabsVal=False, elNthEdgeTabWinSize=118))
        
        mc.symbolButton(image='nodeGrapherModeAllLarge.png', w=25, h=25,
        c=lambda *_:ElNthEdgeAboutClass())
        
        mc.setParent(top=True) 

        self.elNthEdgeNthEFL = mc.frameLayout(l="Nth Edge", la="top", bgc=self.elNthEdgeGrey, cll=True, cl=False, 
        cc=partial(self.elNthEdgeResWin, elNthEdgeClValue=68), ec=partial(self.elNthEdgeResWin, elNthEdgeClValue=(-68)))
        mc.columnLayout(adj=True)

        mc.rowLayout(nc=4)
        mc.text(' Type :', al='left', w=40)
        mc.radioCollection()
        self.elNthEdgeNthLoopRB = mc.radioButton(l="Loop", w=60, h=30, select=True)
        self.elNthEdgeNthRingRB = mc.radioButton(l="Ring", w=60, h=30)
        self.elNthEdgeNthBorderRB = mc.radioButton(l="Border", w=70, h=30)
        mc.setParent('..')

        mc.rowLayout(nc=4)
        mc.text(l=' Select every', al='left', h=30, w=70)
        self.elNthEdgeNthInput = mc.intField(value=2, h=30, w=50, min=1, max=999)
        mc.text(l='edge', al='center', h=30, w=40)
        mc.button(l="Apply", bgc=self.elNthEdgeGreen, h=30, w=68, c = self.elNthEdgeNthEdge)    
        mc.setParent(top=True)    

        mc.showWindow(self.elNthEdgeWinID)
        mc.window(self.elNthEdgeWinID, e=True, w=240, h=118)

    def elNthEdgeResWin(self, elNthEdgeClValue, _=False):
        elNthEdgeWinSize = mc.window(self.elNthEdgeWinID, q=True, h=True)
        mc.window(self.elNthEdgeWinID, e=True, h=(elNthEdgeWinSize-elNthEdgeClValue))

    def elNthEdgeCollapseTabs(self, elNthEdgeCollapseTabsVal, elNthEdgeTabWinSize, _=False):
        mc.frameLayout(self.elNthEdgeNthEFL, e=True, cl=elNthEdgeCollapseTabsVal)
        mc.window(self.elNthEdgeWinID, e=True, h=elNthEdgeTabWinSize)
       
    def elNthEdgeNthEdge(self, _=False):
        if mc.radioButton(self.elNthEdgeNthLoopRB, q=True, sl=True):
            elNthEdgeNthEdgeType = 'edgeLoop'
        if mc.radioButton(self.elNthEdgeNthRingRB, q=True, sl=True):
            elNthEdgeNthEdgeType = 'edgeRing'
        if mc.radioButton(self.elNthEdgeNthBorderRB, q=True, sl=True):
            elNthEdgeNthEdgeType = 'edgeBorder'
        
        elNthEdgeNthEdgeValue = mc.intField(self.elNthEdgeNthInput, q=True, v=True)

        mm.eval('polySelectEdgesEveryN "%s" %s;' % (elNthEdgeNthEdgeType, elNthEdgeNthEdgeValue))

class ElNthEdgeAboutClass:    

    def __init__(self):
        self.elNthEdgeAboutWinID = "elNthEdgeWinAbout"
        self.elNthEdgeAboutUI()

    def elNthEdgeAboutUI(self, _=False):    

        if (mc.window(self.elNthEdgeAboutWinID, exists=True)):
            mc.deleteUI(self.elNthEdgeAboutWinID, wnd=True)
            mc.windowPref(self.elNthEdgeAboutWinID, r=True)

        mc.window(self.elNthEdgeAboutWinID, s=False, tlb=True, t="About")
        mc.columnLayout(adj=True)

        mc.rowLayout(nc=1)
        mc.text(l='', h=10)
        mc.setParent('..')
        
        mc.rowLayout(nc=1)
        mc.text(l='<font color=#3cb777><h3>EL_NthEdge v1.0</h3></font>', al='center', w=196, h=20)
        mc.setParent('..')
        mc.rowLayout(nc=1)
        mc.text(l='Author: Erik Lehmann \nCopyright (c) 2019 Erik Lehmann', al='center', w=196, h=40)
        mc.setParent('..')
        
        mc.rowLayout(nc=3)
        mc.text(l='', w=11)
        mc.button(l='Open documentation', ann='Documentation page', w=170, h=30,
        c=lambda *_:self.elNthEdgeAboutOpenBrowser(elNthEdgeAboutSiteCode='Documentation'))
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
        c=lambda *_:self.elNthEdgeAboutOpenBrowser(elNthEdgeAboutSiteCode='Website'))
        mc.button(l='Gumroad', ann="Find more useful resources for Maya on Gumroad.", w=85, h=30, 
        c=lambda *_:self.elNthEdgeAboutOpenBrowser(elNthEdgeAboutSiteCode='Gumroad'))
        mc.text(l='', w=10)
        mc.setParent('..')
        
        mc.rowLayout(nc=4)
        mc.text(l='', w=10)
        mc.button(l='Artstation', ann="Erik Lehmann's Artstation Profile", w=85, h=30,
        c=lambda *_:self.elNthEdgeAboutOpenBrowser(elNthEdgeAboutSiteCode='Artstation'))
        mc.button(l='Facebook', ann='The Art Of Erik Lehmann on Facebook', w=85, h=30,
        c=lambda *_:self.elNthEdgeAboutOpenBrowser(elNthEdgeAboutSiteCode='Facebook'))
        mc.text(l='', w=10)
        mc.setParent(top=True)

        mc.showWindow(self.elNthEdgeAboutWinID)
        mc.window(self.elNthEdgeAboutWinID, e=True, w=200, h=290)
  
    def elNthEdgeAboutOpenBrowser(self, elNthEdgeAboutSiteCode, _=False):
        if elNthEdgeAboutSiteCode == 'Documentation':
            mc.launch(web="https://www.eriklehmann.com/documentation")
        elif elNthEdgeAboutSiteCode == 'Website':
            mc.launch(web="http://www.eriklehmann.com/")
        elif elNthEdgeAboutSiteCode == 'Gumroad':
            mc.launch(web="https://gumroad.com/eriklehmann")    
        elif elNthEdgeAboutSiteCode == 'Artstation':
            mc.launch(web="https://www.artstation.com/eriklehmann")
        elif elNthEdgeAboutSiteCode == 'Facebook':
            mc.launch(web="https://www.facebook.com/TheArtOfErikLehmann/")