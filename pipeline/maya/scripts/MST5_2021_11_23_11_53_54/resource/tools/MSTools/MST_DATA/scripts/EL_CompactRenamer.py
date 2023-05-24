'''
EL_CompactRenamer v1.0
Author: Erik Lehmann
Copyright (c) 2019 Erik Lehmann
Email: contact(at)eriklehmann.com
'''

import maya.cmds as mc
import sys
from functools import partial

class MainClassCompactRen:

    def __init__(self):
        self.compactRenWinID = "compactRenWin"

        self.compactRenGreen = (0.3, 0.50, 0.40)
        self.compactRenDark = (0.18, 0.18, 0.18)

        self.compactRenUI()

    def compactRenUI(self, _=False):
                                   
        if (mc.window(self.compactRenWinID, exists=True)):
            mc.deleteUI(self.compactRenWinID, wnd=True)
            mc.windowPref(self.compactRenWinID, r=True)
            

        mc.window(self.compactRenWinID, s=False, tlb=True, t="EL Compact Renamer v1.0")
        compactRenMCL = mc.columnLayout(adj=True)
        
        mc.rowLayout(nc=1)
        mc.text(h=2, l="")
        mc.setParent('..')
        
        mc.rowLayout(nc=6)
        mc.text(w=1, l="")
        mc.textField("tFcR_Prefix", height=30, width=60, pht="Prefix")
        
        mc.textField("tFcR_Name", height=30, width=140, pht="Name")
        
        mc.textField("tFcR_Suffix", height=30, width=60, pht="Suffix")

        self.compactRenBtn = mc.button(l="R", c=self.compactRenCall, bgc=self.compactRenGreen, ebg=False, height=28, width=30,
        ann="LMB: Rename objects // RMB: Option menu")
        
        mc.popupMenu(p = self.compactRenBtn)
        
        mc.menuItem(d=True, dl='Rename')
        self.compactRenOptionRBC = mc.radioMenuItemCollection()
        self.compactRenOptionRBA = mc.menuItem(rb=True, cl=self.compactRenOptionRBC, l='All')
        self.compactRenOptionRBP = mc.menuItem(rb=False, cl=self.compactRenOptionRBC, l='Prefix')
        self.compactRenOptionRBN = mc.menuItem(rb=False, cl=self.compactRenOptionRBC, l='Name')
        self.compactRenOptionRBS = mc.menuItem(rb=False, cl=self.compactRenOptionRBC, l='Suffix')
        
        mc.menuItem(d=True, dl='Options')
        self.compactRenOptionRBSR = mc.menuItem(rb=False, l='Search \ Replace')
        
        mc.menuItem(d=True, dl='Padding')
        self.compactRenPadRBC = mc.radioMenuItemCollection()
        mc.menuItem("compactRenPadRB1", rb=False, cl=self.compactRenPadRBC, l='1')
        mc.menuItem("compactRenPadRB2", rb=False, cl=self.compactRenPadRBC, l='2')
        mc.menuItem("compactRenPadRB3", rb=True, cl=self.compactRenPadRBC, l='3')

        mc.symbolButton(image='nodeGrapherModeAllLarge.png', w=25, h=25, c=lambda *_:CompactRenAboutClass())
        
        mc.setParent(top=True)
        
        mc.showWindow(self.compactRenWinID)
        mc.window(self.compactRenWinID, e=True, width=330, h=42)
    
    def compactRenCall(self, _=False):
        if mc.menuItem(self.compactRenOptionRBA, q=True, rb=True):
            self.compactRenName()
            self.compactRenPrefix() 
            self.compactRenSuffix()   
        if mc.menuItem(self.compactRenOptionRBP, q=True, rb=True):
            self.compactRenPrefix() 
        if mc.menuItem(self.compactRenOptionRBN, q=True, rb=True):
            self.compactRenName()
        if mc.menuItem(self.compactRenOptionRBS, q=True, rb=True):
            self.compactRenSuffix()
        if mc.menuItem(self.compactRenOptionRBSR, q=True, rb=True):
            self.compactRenSeaRep()
    
    def compactRenReorder(self, compactRenList, _=False):
        sorted(compactRenList)
        for i in reversed(compactRenList):
            try:
                mc.reorder(i, front=True)
            except:
                pass
    
    def compactRenName(self, _=False):
        compactRenNameText = mc.textField("tFcR_Name", q=True, tx=True)
        if compactRenNameText == "":
            mc.warning("Please enter a name")
        else:  
            compactRenList = mc.ls(sl=True)
            compactRenStartValue = 1
            compactRenStepValue = 1
                    
            compactRenPlaceholderList = []
            compactRenTempList = []
            
            for i in range(1,4):
                 if mc.menuItem("compactRenPadRB%s" % i, q=True, rb=True):
                     compactRenPadding = str(i)
          
            if len(compactRenList) == 1:
                mc.rename(compactRenList[0], '%s' % compactRenNameText)
            
            else:
                compactRenTempStartValue = compactRenStartValue
                
                for i in compactRenList:
                    compactRenTempPadValue = ("%%0%si" % compactRenPadding.replace(" ", "")) % int(compactRenTempStartValue)
                    compactRenTempNewName = mc.rename(i, 'compactRenTempText%s' % ( compactRenTempPadValue))
                    compactRenTempStartValue += 1
                    compactRenPlaceholderList.append(compactRenTempNewName)
                    
                for i in compactRenPlaceholderList:
                    compactRenPadValue = ("%%0%si" % compactRenPadding.replace(" ", "")) % int(compactRenStartValue)
                    compactRenNewName = mc.rename(i, '%s%s' % (compactRenNameText, compactRenPadValue))
                    compactRenStartValue += compactRenStepValue
                    compactRenTempList.append(compactRenNewName)
                       
            self.compactRenReorder(compactRenTempList)
    
    def compactRenPrefix(self, _=False):
        compactRenPreText = mc.textField("tFcR_Prefix", q=True, text=True)
        if compactRenPreText == "":
            mc.warning("Please enter a prefix")
        else:
            compactRenList = mc.ls(sl=True, fl=True)
            
            compactRenPlaceholderList = []
            compactRenTempList = []
            
            if len(compactRenList) == 0:
                print "Select Object(s)."
                
            else:
                for i in compactRenList:
                    compactRenLine = i.split('|')[-1]
                    compactRenTempNewName = mc.rename(i, 'compactRenPreTempText_%s' % (compactRenLine))
                    compactRenPlaceholderList.append(compactRenTempNewName)
                    
                for i in compactRenPlaceholderList:
                    compactRenNewName = i.replace('compactRenPreTempText_', "%s" % compactRenPreText)
                    mc.rename(i, '%s' % compactRenNewName) 
                    compactRenTempList.append(compactRenNewName)
    
    def compactRenSuffix(self, _=False):
        compactRenSufText = mc.textField("tFcR_Suffix", q=True, text=True)
        if compactRenSufText == "":
            mc.warning("Please enter a suffix")
        else:
            compactRenList = mc.ls(sl=True)
            
            compactRenPlaceholderList = []
            compactRenTempList = []
            
            if len(compactRenList) == 0:
                print "Select Object(s)."
            else:
                for i in compactRenList:
                    compactRenLine = i.split('|')[-1]
                    compactRenTempNewName = mc.rename(i, '%s_compactRenSufTempText' % (compactRenLine))
                    compactRenPlaceholderList.append(compactRenTempNewName)
                    
                for i in compactRenPlaceholderList:
                    compactRenNewName = i.replace('_compactRenSufTempText', "%s" % compactRenSufText)
                    mc.rename(i, '%s' % compactRenNewName) 
                    compactRenTempList.append(compactRenNewName)

    def compactRenSeaRep(self, _=False):
        compactRenSearchValue = mc.textField("tFcR_Prefix", q=True, tx=True)
        compactRenReplaceValue = mc.textField("tFcR_Suffix", q=True, tx=True)
        compactRenList = mc.ls(sl=True)
        
        try:
            for i in compactRenList:
                if "%s" % compactRenSearchValue in i:
                    compactRenLine = i.split('|')[-1]
                    compactRenNewText = compactRenLine.replace("%s" % compactRenSearchValue, "%s" % compactRenReplaceValue)
                    mc.rename(i, '%s' % compactRenNewText)     
            sys.exit()
            
        except:
            sys.exit() 

class CompactRenAboutClass:    

    def __init__(self):
        self.compactRenAboutWinID = "compactRenWinAbout"
        self.compactRenAboutUI()

    def compactRenAboutUI(self, _=False):    


        if (mc.window(self.compactRenAboutWinID, exists=True)):
            mc.deleteUI(self.compactRenAboutWinID, wnd=True)
            mc.windowPref(self.compactRenAboutWinID, r=True)

        mc.window(self.compactRenAboutWinID, s=False, tlb=True, t="About")
        mc.columnLayout(adj=True)
        
        mc.rowLayout(nc=1)
        mc.text(l='', h=10)
        mc.setParent('..')
        
        mc.rowLayout(nc=1)
        mc.text(l='<font color=#3cb777><h3>EL_CompactRenamer v1.0</h3></font>', al='center', w=196, h=20)
        mc.setParent('..')
        mc.rowLayout(nc=1)
        mc.text(l='Author: Erik Lehmann \nCopyright (c) 2019 Erik Lehmann', al='center', w=196, h=40)
        mc.setParent('..')
        
        mc.rowLayout(nc=3)
        mc.text(l='', w=11)
        mc.button(l='Open documentation', ann='Documentation page', w=170, h=30,
        c=lambda *_:self.compactRenAboutOpenBrowser(compactRenAboutSiteCode='Documentation'))
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
        c=lambda *_:self.compactRenAboutOpenBrowser(compactRenAboutSiteCode='Website'))
        mc.button(l='Gumroad', ann="Find more useful resources for Maya on Gumroad.", w=85, h=30, 
        c=lambda *_:self.compactRenAboutOpenBrowser(compactRenAboutSiteCode='Gumroad'))
        mc.text(l='', w=10)
        mc.setParent('..')
        
        mc.rowLayout(nc=4)
        mc.text(l='', w=10)
        mc.button(l='Artstation', ann="Erik Lehmann's Artstation Profile", w=85, h=30,
        c=lambda *_:self.compactRenAboutOpenBrowser(compactRenAboutSiteCode='Artstation'))
        mc.button(l='Facebook', ann='The Art Of Erik Lehmann on Facebook', w=85, h=30,
        c=lambda *_:self.compactRenAboutOpenBrowser(compactRenAboutSiteCode='Facebook'))
        mc.text(l='', w=10)
        mc.setParent(top=True)
        
        mc.showWindow(self.compactRenAboutWinID)
        mc.window(self.compactRenAboutWinID, e=True, w=200, h=290)
        
    def compactRenAboutOpenBrowser(self, compactRenAboutSiteCode, _=False):
        if compactRenAboutSiteCode == 'Documentation':
            mc.launch(web="https://www.eriklehmann.com/documentation")
        elif compactRenAboutSiteCode == 'Website':
            mc.launch(web="http://www.eriklehmann.com/")
        elif compactRenAboutSiteCode == 'Gumroad':
            mc.launch(web="https://gumroad.com/eriklehmann")    
        elif compactRenAboutSiteCode == 'Artstation':
            mc.launch(web="https://www.artstation.com/eriklehmann")
        elif compactRenAboutSiteCode == 'Facebook':
            mc.launch(web="https://www.facebook.com/TheArtOfErikLehmann/")