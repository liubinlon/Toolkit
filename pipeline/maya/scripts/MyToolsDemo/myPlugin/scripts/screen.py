#bulit_in modules
import os
import sys
import getpass
#maya modules
import maya.cmds as cmds
import pymel.core as pymel
import maya.OpenMayaUI as omui
#pyside2 mmodules
from PySide2 import QtGui, QtWidgets, QtCore


class btn:
    def __init__(self):
        self.filename = None
        self.fonSizeValue = None
        self.widthValue = None
        self.heightValue = None
        # self.lowerleftValue = None
        # self.lowerrightValue = None
        # self.upperleftValue = None
        # self.upperrightValue = None
        self.setcbxformat = None
        self.setfoncolor = None

    def foncolor(self):
        value = self.setfoncolor.currentIndex()
        if value == 3:
            cmds.displayColor("headsUpDisplayLabels", 17, dormant = 1)
            cmds.displayColor("headsUpDisplayValues", 17, dormant = 1)
        elif value == 2:
            cmds.displayColor("headsUpDisplayLabels", 13, dormant = 1)
            cmds.displayColor("headsUpDisplayValues", 13, dormant = 1)
        elif value == 1:
            cmds.displayColor("headsUpDisplayLabels", 6, dormant = 1)
            cmds.displayColor("headsUpDisplayValues", 6, dormant = 1)
        else:
            cmds.displayColor("headsUpDisplayLabels", 16, dormant = 1)
            cmds.displayColor("headsUpDisplayValues", 16, dormant = 1)

    def setformat(self):
        value = self.setcbxformat.currentIndex()
        if value == 2:
            formatstr = "image"
            formatstr1 = "gif"
        elif value == 1:
            formatstr = "avi"
            formatstr1 = "avi"
        else:
            formatstr = "qt"
            formatstr1 = "mov"
        return formatstr,formatstr1

    def autofilename(self):
        filename = self.newfilename()
        if not filename:
            namestr = self.getfilename()
        else:
            namestr = filename
        return namestr

    def getfilename(self, full_path = None, dir_path = None):
        if full_path:
            if dir_path:
                return str(pymel.sceneName().dirname())
            return str(pymel.sceneName().abspath())
        return str(pymel.sceneName().basename()).split(".")[0]
    
    # def get_all_ref_path(self, loaded = None, not_loded = None):
    #     all_ref_path = cmds.ls(references=True)
    #     loaded_ref_path = [p for p in all_ref_path if cmds.referenceQuery(p, il=1)]
    #     if loaded:
    #         return loaded_ref_path
    #     elif not_loded:
    #         return [k for k in all_ref_path if k not in loaded_ref_path]
    #     else:
    #         return all_ref_path

    def remdisplay(self):     
        if cmds.headsUpDisplay(listHeadsUpDisplays = True):
            for i in cmds.headsUpDisplay(listHeadsUpDisplays = True):
                cmds.headsUpDisplay(i, remove = True)

    def get_user_name(self, *args):
        return getpass.getuser()
        
    def get_camera(self, *args):
        return str(cmds.lookThru(q = True))

    def get_focal_length(self, *camera_name):
        camera_name = self.get_camera()
        return int(cmds.getAttr(camera_name + ".focalLength"))

    def get_time(self, *args):
        get_currentTime = cmds.currentTime(q = True)
        return get_currentTime

    def get_current_fps(self, *args):
        format_list = {'film': 24, 'game': 15, 'pal': 25, 'ntsc': 30, 'show': 48, 'palf': 50, 'ntscf': 60}
        fpsString = cmds.currentUnit(query=True, t=True)
        try:
            return format_list[fpsString]
        except:
            return False

    def get_proj_size(self, *args):
        if cmds.objExists('defaultResolution'):
            width = cmds.getAttr('defaultResolution.w')
            height = cmds.getAttr('defaultResolution.h')
            return str(width) + '*' + str(height)
        else:
            return '000'

    def add_Display(self):
        cmds.headsUpDisplay('cameraName', section = 5, block = 4, blockSize = 'small', label = 'camera:', labelFontSize = 'large', dataFontSize = "large",command = self.get_camera, event = 'SelectionChanged', nodeChanges = 'attributeChange')
        cmds.headsUpDisplay('focalLength', section = 6, block = 4, blockSize = 'small', label = 'focal length:', labelFontSize = 'large', dataFontSize = "large", command = self.get_focal_length, attachToRefresh = True)
        cmds.headsUpDisplay('displaySize', section = 9, block = 4, blockSize = 'small', label = 'displaySize:', labelFontSize = 'large', dataFontSize = "large", command = self.get_proj_size, attachToRefresh = True)
        cmds.headsUpDisplay('currentTime', section = 7, block = 4, blockSize = 'small', label = '  ', labelFontSize = 'large', dataFontSize = "large", command = self.get_time, attachToRefresh = True)
        cmds.headsUpDisplay('currentfps', section = 8, block = 4, blockSize = 'small', label = 'fps:', labelFontSize = 'large', dataFontSize = "large", command = self.get_current_fps, attachToRefresh = True)
        
    def get_maya_win(self, module = "mayaUI"):
        prt = omui.MQtUtil.mainWindow()
        if moduel == "Qt":
            import Qt
            if "PyQt" in Qt.__binding__:
                import sip
                import PyQt5.QtCore as QtCore
                main_window = sip.wrapinstance(long(prt), QtCore.QObject)
            elif Qt.__binding__ == "PySide":
                import shiboken
                import PySide.QtGui as QtGui
                main_window = shiboken.wrapinstance(long(prt), QtGui.QWidget)
            else:
                raise ValueError("Qt binding not supported...")
        elif module == "PyQt5":
            import sip
            import PyQt5.QtCore as QtCore
            main_window = sip.wrapinstance(long(prt), QtCore.QObject)
        elif module == "PySide":
            import shiboken
            import PySide.QtGui as QtGui
            main_window = shiboken.wrapinstance(long(prt), QtGui.QWidget)
        elif module == "PySide2":
            import shiboken2
            import PySide2.QtWidgets as QtWidgets
            main_window = shiboken2.wrapinstance(long(prt), QtWidgets.QWidget)
        elif module == "mayaUI":
            main_window = "MayaWindow"
        else:
            raise ValueError('param"module" must be "mayaUI" "PyQt5" "PySide" "PySide2" or "Qt"')

    def get_display_layers(self, get_ref_layers = None,get_normal_layers = None):
        all_layers = list()
        all_layers.extend(
            [k for k in [k for k in cmds.ls(type="displayLayer") if k != "defaultLayer"]])
        ref_layers = [k.encode('utf-8') for k in all_layers if  cmds.referenceQuery(k, inr=1)]
        if get_ref_layers:
            return ref_layers
        elif get_normal_layers:
            return [_ for _ in all_layers if _ not in ref_layers]
        else:
            return all_layers


    
    # def set_information(self):

    #     if self.upperleftValue.isChecked():
    #         return ("upperleftValue")
    #     elif self.upperrightValue.isChecked():
    #         return ("upperrightValue")
    #     elif self.lowerleftValue.isChecked():
    #         return ("lowerleftValue")
    #     else:
    #         return ("lowerrightValue")
    # def setwidth(self):
    #     if not self.getwidthValue():
    #         return int(2048)
    
    # def setheight(self):
    #     if not self.getheightValue():
    #         return int(1152)

    def openFileDialog(self, dir):
        return str(cmds.fileDialog2(dialogStyle=1, fileMode = 3, dir=dir)).split("\'")[1]

    def setwidthValue(self):
        widthValue = self.getwidthValue()
        heightValue = self.getheightValue()
        if widthValue != 0:
            width = widthValue
            heigth = heightValue
        else:
            width = 2048
            height = 1052
        return width, heigth

    def playblast(self):
        print self.setwidthValue()[:]
        # cmds.setAttr('defaultResolution.w', self.setwidthValue()[0])
        # cmds.setAttr('defaultResolution.h', self.setwidthValue()[1])
        # # filename = os.path.basename(__file__)
        # self.remdisplay()
        # self.add_Display()
        # dir_path = str(pymel.sceneName().dirname())
        # newpath = self.openFileDialog(dir_path)
        # for_mat = self.setformat()
        # # filename = os.path.basename(__file__)
        # file_name = self.autofilename()
        # # information = self.set_information()
        # filename = newpath + "/" +file_name + "." + for_mat[1]
        # cmds.playblast(format = for_mat[0], filename = filename, sequenceTime = False, forceOverwrite = True, clearCache = 1, viewer = True, showOrnaments = True, 
        # compression = "H.264", percent = 50, widthHeight = self.setwidthValue())
        

    def newfilename(self):
        if not self.filename:
            return
        return self.filename.text()

    def getfonSizeValue(self):
        if not self.fonSizeValue:
            return
        return self.fonSizeValue.text()

    def getwidthValue(self):
        if not self.widthValue:
            return 
        return self.widthValue.text()

    def getheightValue(self):
        if not self.heightValue:
            return 
        return self.heightValue.value()
    
    # def getlowerleftValue(self):
    #     if not self.lowerleftValue:
    #         return
    #     if self.lowerleftValue.isChecked():
    #         return True
    #     else:return False
   
    # def getlowerrightValue(self):
    #     if not self.lowerrightValue:
    #         return
    #     if self.lowerrightValue.isChecked():
    #         return True
    #     else:return False
    
    # def getupperleftValue(self):
    #     if not self.upperleftValue:
    #         return
    #     if self.upperleftValue.isChecked():
    #         return True
    #     else:return False
    
    # def getupperrightValue(self):
    #     if not self.upperrightValue:
    #         return
    #     if self.upperrightValue.isChecked():
    #         return True
    #     else:return False