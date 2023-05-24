'''
EL Distribute v1.0
Author: Erik Lehmann
Copyright (c) 2019 Erik Lehmann
Email: contact(at)eriklehmann.com
'''

import maya.cmds as mc
import math
from functools import partial

class MainClassElDistribute:

    def __init__(self):
        self.elDistributeWinID = "elDistributeWin"
        
        self.elDistributeGreen = (0.3, 0.50, 0.40)
        self.elDistributeGrey = (0.3, 0.3, 0.3)

        self.elDistributeDisSpacingAmount = 0.0
        
        self.elDistributeMayaVersion = mc.about(q=True, v=True)
        if '2018' in self.elDistributeMayaVersion or '2019' in self.elDistributeMayaVersion:
            self.elDistributeArrowUp = 'moveUVUp.png'
            self.elDistributeArrowDown = 'moveUVDown.png'
        elif '2017' in self.elDistributeMayaVersion:
            self.elDistributeArrowUp = 'nodeGrapherArrowUp.png'
            self.elDistributeArrowDown = 'nodeGrapherArrowDown.png'
        else:
            self.elDistributeArrowUp = 'arrowUp.png'
            self.elDistributeArrowDown = 'arrowDown.png'
        
        self.elDistributeUI()

    def elDistributeUI(self, _=False):    

        if (mc.window(self.elDistributeWinID, exists=True)):
            mc.deleteUI(self.elDistributeWinID, wnd=True)
            mc.windowPref(self.elDistributeWinID, r=True)

        mc.window(self.elDistributeWinID, s=False, tlb=True, t="EL Distribute v1.0")
        mc.columnLayout(adj=True)

        mc.rowLayout(nc=5)
        mc.text(l='', w=127, h=20)
        
        mc.symbolButton(image='%s' % self.elDistributeArrowUp, w=25, h=25,
        ann='Collapse all tabs', 
        c=lambda *_:self.elDistributeCollapseTabs(elDistributeCollapseTabsVal=True, elDistributeTabWinSize=50))
        
        mc.symbolButton(image='%s' % self.elDistributeArrowDown, w=25, h=25,
        ann='Expand all tabs', 
        c=lambda *_:self.elDistributeCollapseTabs(elDistributeCollapseTabsVal=False, elDistributeTabWinSize=197))
        
        mc.symbolButton(image='nodeGrapherModeAllLarge.png', w=25, h=25,
        ann="Open 'About' window with information about the toolkit", 
        c=lambda *_:ElDistributeAboutClass())
        
        mc.setParent(top=True)

        self.elDistributeUI = mc.frameLayout(l="Distribute", la="top", bgc=self.elDistributeGrey, cll=True, cl=False, 
        cc=partial(self.elDistributeResWin, elDistributeClValue=147), ec=partial(self.elDistributeResWin, elDistributeClValue=(-147)))
        mc.columnLayout(adj=True)
        
        mc.rowLayout(nc=4)
        mc.text(l=" Axis", al="left", w=65, h=30)
        self.elDistributeMethodAxisRBC = mc.radioCollection()
        self.elDistributeMethodAxisRBX = mc.radioButton(sl=True, cl=self.elDistributeMethodAxisRBC, l='X', w=50, h=30)
        self.elDistributeMethodAxisRBY = mc.radioButton(sl=False, cl=self.elDistributeMethodAxisRBC, l='Y', w=50, h=30)
        self.elDistributeMethodAxisRBZ = mc.radioButton(sl=False, cl=self.elDistributeMethodAxisRBC, l='Z', w=50, h=30)
        mc.setParent('..')
        
        mc.rowLayout(nc=4)
        mc.text(l=" Direction", al="left", w=65, h=30)
        self.elDistributeMethodDirRBC = mc.radioCollection()
        self.elDistributeMethodDirRBPo = mc.radioButton(sl=True, cl=self.elDistributeMethodDirRBC, l='Plus', w=50, h=30)
        self.elDistributeMethodDirRBNe = mc.radioButton(sl=False, cl=self.elDistributeMethodDirRBC, l='Minus', w=50, h=30)
        mc.text(l="", al="left", w=15, h=30)
        mc.setParent('..')
        
        mc.rowLayout(nc=2)
        mc.text(l=" Spacing", w = 65, align="left")
        self.elDistributeDisSpacingFF = mc.floatField(min=0, max=100, pre=3, v=self.elDistributeDisSpacingAmount, w=137, h=30)
        mc.setParent('..')
        
        mc.rowLayout(nc=1)
        mc.text(l="", w = 204, h=4, align="left")
        mc.setParent('..')
        
        mc.rowLayout(nc=1)
        self.elDistributeMethodBtn = mc.button(l="Distribute Objects", al="center", bgc=self.elDistributeGreen, w=204, h=40, 
        c = self.elDistributeMethod, ann='LMB: Distribute stacked objects based on their bounding box',)
        mc.setParent(top=True)

        mc.showWindow(self.elDistributeWinID)
        mc.window(self.elDistributeWinID, e=True, w=210, h=197)

    def elDistributeResWin(self, elDistributeClValue, _=False):
        elDistributeWinSize = mc.window(self.elDistributeWinID, q=True, h=True)
        mc.window(self.elDistributeWinID, e=True, h=(elDistributeWinSize-elDistributeClValue))

    def elDistributeCollapseTabs(self, elDistributeCollapseTabsVal, elDistributeTabWinSize, _=False):
        mc.frameLayout(self.elDistributeUI, e=True, cl=elDistributeCollapseTabsVal)
        mc.window(self.elDistributeWinID, e=True, h=elDistributeTabWinSize)

    def elDistributeGetObjectScaleValues(self, elDistributeGetObjScaleInput, _=False):
        elDistributeGetScaleX = mc.getAttr("%s.scaleX" % elDistributeGetObjScaleInput)
        elDistributeGetScaleY = mc.getAttr("%s.scaleY" % elDistributeGetObjScaleInput)
        elDistributeGetScaleZ = mc.getAttr("%s.scaleZ" % elDistributeGetObjScaleInput)
        elDistributeObjScaleValues = [elDistributeGetScaleX, elDistributeGetScaleY, elDistributeGetScaleZ]
        return elDistributeObjScaleValues

    def elDistributeGetBoundingBox(self, elDistributeGetBBInput, _=False):
        elDistributeGetBBAxisLength = [0,0,0]
        elDistributeGetBBTransformScale = self.elDistributeGetObjectScaleValues(elDistributeGetBBInput)
        
        if self.elDistributeIsGroup(elDistributeGetBBInput) == True:
            elDistributeGetBBObjectBB = mc.exactWorldBoundingBox(elDistributeGetBBInput, ce=True)
            elDistributeGetBBObjectBBMin = elDistributeGetBBObjectBB[0:3]
            elDistributeGetBBObjectBBMax = elDistributeGetBBObjectBB[3:6]
            
            elDistributeGetBBAxisLength[0] = (elDistributeGetBBObjectBBMax[0]-elDistributeGetBBObjectBBMin[0])
            elDistributeGetBBAxisLength[1] = (elDistributeGetBBObjectBBMax[1]-elDistributeGetBBObjectBBMin[1])
            elDistributeGetBBAxisLength[2] = (elDistributeGetBBObjectBBMax[2]-elDistributeGetBBObjectBBMin[2])
            
        else:
            elDistributeBBShape = mc.listRelatives(elDistributeGetBBInput, s=True)
            elDistributeGetBBObjectBBMin = list(mc.getAttr("%s.boundingBoxMin" % elDistributeBBShape[0])[0])
            elDistributeGetBBObjectBBMax = list(mc.getAttr("%s.boundingBoxMax" % elDistributeBBShape[0])[0])
            
            elDistributeGetBBAxisLength[0] = (elDistributeGetBBObjectBBMax[0]-elDistributeGetBBObjectBBMin[0]) * elDistributeGetBBTransformScale[0]
            elDistributeGetBBAxisLength[1] = (elDistributeGetBBObjectBBMax[1]-elDistributeGetBBObjectBBMin[1]) * elDistributeGetBBTransformScale[1]
            elDistributeGetBBAxisLength[2] = (elDistributeGetBBObjectBBMax[2]-elDistributeGetBBObjectBBMin[2]) * elDistributeGetBBTransformScale[2]

        return elDistributeGetBBAxisLength 
        
    
    def elDistributeIsGroup(self, elDistributeIsGroupInput, _=False):
        if not mc.listRelatives(elDistributeIsGroupInput, s = True) and mc.nodeType(elDistributeIsGroupInput) == 'transform':
            return True
        else:
            return False

    def elDistributeMethod(self, _=False):
        
        if mc.radioButton(self.elDistributeMethodDirRBPo, q=True, sl=True):
            elDistributeDisDir = 1
        if mc.radioButton(self.elDistributeMethodDirRBNe, q=True, sl=True):
            elDistributeDisDir = -1
            
        if mc.radioButton(self.elDistributeMethodAxisRBX, q=True, sl=True):
            elDistributeDisPosSelector = 0
        if mc.radioButton(self.elDistributeMethodAxisRBY, q=True, sl=True):
            elDistributeDisPosSelector = 1
        if mc.radioButton(self.elDistributeMethodAxisRBZ, q=True, sl=True):
            elDistributeDisPosSelector = 2
        
        elDistributeDisCurrentSel = mc.ls(sl=True)
        self.elDistributeDisMoveX = 0
        self.elDistributeDisMoveY = 0
        self.elDistributeDisMoveZ = 0
        
        self.elDistributeDisMoveSum = 0
        self.elDistributeDisCheckIter = 1
        self.elDistributeDisPrevLength = 0
        self.elDistributeDisHalfDifference = 0
        
        for i in elDistributeDisCurrentSel:
            print 'Sum %s' % self.elDistributeDisMoveSum
  
            mc.select(i)
            elDistributeDisAxisLength = self.elDistributeGetBoundingBox(i)
            
            if self.elDistributeDisPrevLength == 0 or self.elDistributeDisPrevLength == elDistributeDisAxisLength[elDistributeDisPosSelector]: 
                self.elDistributeDisMoveResult = elDistributeDisAxisLength[elDistributeDisPosSelector]
                
            if self.elDistributeDisPrevLength > 0 and elDistributeDisAxisLength[elDistributeDisPosSelector] > self.elDistributeDisPrevLength:
                self.elDistributeDisHalfDifference = (elDistributeDisAxisLength[elDistributeDisPosSelector] - self.elDistributeDisPrevLength) / 2
                self.elDistributeDisMoveResult = elDistributeDisAxisLength[elDistributeDisPosSelector] + self.elDistributeDisHalfDifference
                
            if self.elDistributeDisPrevLength > 0 and elDistributeDisAxisLength[elDistributeDisPosSelector] < self.elDistributeDisPrevLength:
                self.elDistributeDisHalfDifference = (self.elDistributeDisPrevLength - elDistributeDisAxisLength[elDistributeDisPosSelector]) / -2
                self.elDistributeDisMoveResult = elDistributeDisAxisLength[elDistributeDisPosSelector] + self.elDistributeDisHalfDifference 

            if mc.radioButton(self.elDistributeMethodAxisRBX, q=True, sl=True):
                self.elDistributeDisMoveX = (self.elDistributeDisMoveSum + self.elDistributeDisHalfDifference) * elDistributeDisDir 
            if mc.radioButton(self.elDistributeMethodAxisRBY, q=True, sl=True):
                self.elDistributeDisMoveY = (self.elDistributeDisMoveSum + self.elDistributeDisHalfDifference) * elDistributeDisDir
            if mc.radioButton(self.elDistributeMethodAxisRBZ, q=True, sl=True):
                self.elDistributeDisMoveZ = (self.elDistributeDisMoveSum + self.elDistributeDisHalfDifference) * elDistributeDisDir
            
            self.elDistributeDisSpacingAmount = mc.floatField(self.elDistributeDisSpacingFF, q=True, v=True)
            
            if self.elDistributeDisCheckIter == 1:
                pass
            else:
                mc.move( self.elDistributeDisMoveX, self.elDistributeDisMoveY, self.elDistributeDisMoveZ, os=False, r=True)
            
            self.elDistributeDisMoveSum += self.elDistributeDisMoveResult + self.elDistributeDisSpacingAmount
            self.elDistributeDisCheckIter += 1
            self.elDistributeDisHalfDifference = 0
            self.elDistributeDisPrevLength = elDistributeDisAxisLength[elDistributeDisPosSelector]
            
        mc.select(elDistributeDisCurrentSel)

class ElDistributeAboutClass:    

    def __init__(self):
        self.elDistributeAboutWinID = "elDistributeWinAbout"
        self.elDistributeAboutUI()

    def elDistributeAboutUI(self, _=False):    

        if (mc.window(self.elDistributeAboutWinID, exists=True)):
            mc.deleteUI(self.elDistributeAboutWinID, wnd=True)
            mc.windowPref(self.elDistributeAboutWinID, r=True)


        mc.window(self.elDistributeAboutWinID, s=False, tlb=True, t="About")
        mc.columnLayout(adj=True)

        mc.rowLayout(nc=1)
        mc.text(l='', h=10)
        mc.setParent('..')
        
        mc.rowLayout(nc=1)
        mc.text(l='<font color=#3cb777><h3>EL Distribute v1.0</h3></font>', al='center', w=196, h=20)
        mc.setParent('..')
        mc.rowLayout(nc=1)
        mc.text(l='Author: Erik Lehmann \nCopyright (c) 2019 Erik Lehmann', al='center', w=196, h=40)
        mc.setParent('..')
        
        mc.rowLayout(nc=3)
        mc.text(l='', w=11)
        mc.button(l='Open documentation', ann='Documentation page', w=170, h=30,
        c=lambda *_:self.elDistributeAboutOpenBrowser(elDistributeAboutSiteCode='Documentation'))
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
        c=lambda *_:self.elDistributeAboutOpenBrowser(elDistributeAboutSiteCode='Website'))
        mc.button(l='Gumroad', ann="Find more useful resources for Maya on Gumroad.", w=85, h=30, 
        c=lambda *_:self.elDistributeAboutOpenBrowser(elDistributeAboutSiteCode='Gumroad'))
        mc.text(l='', w=10)
        mc.setParent('..')
        
        mc.rowLayout(nc=4)
        mc.text(l='', w=10)
        mc.button(l='Artstation', ann="Erik Lehmann's Artstation Profile", w=85, h=30,
        c=lambda *_:self.elDistributeAboutOpenBrowser(elDistributeAboutSiteCode='Artstation'))
        mc.button(l='Facebook', ann='The Art Of Erik Lehmann on Facebook', w=85, h=30,
        c=lambda *_:self.elDistributeAboutOpenBrowser(elDistributeAboutSiteCode='Facebook'))
        mc.text(l='', w=10)
        mc.setParent(top=True)

        mc.showWindow(self.elDistributeAboutWinID)
        mc.window(self.elDistributeAboutWinID, e=True, w=200, h=290)
 
    def elDistributeAboutOpenBrowser(self, elDistributeAboutSiteCode, _=False):
        if elDistributeAboutSiteCode == 'Documentation':
            mc.launch(web="https://www.eriklehmann.com/documentation")
        elif elDistributeAboutSiteCode == 'Website':
            mc.launch(web="http://www.eriklehmann.com/")
        elif elDistributeAboutSiteCode == 'Gumroad':
            mc.launch(web="https://gumroad.com/eriklehmann")    
        elif elDistributeAboutSiteCode == 'Artstation':
            mc.launch(web="https://www.artstation.com/eriklehmann")
        elif elDistributeAboutSiteCode == 'Facebook':
            mc.launch(web="https://www.facebook.com/TheArtOfErikLehmann/")