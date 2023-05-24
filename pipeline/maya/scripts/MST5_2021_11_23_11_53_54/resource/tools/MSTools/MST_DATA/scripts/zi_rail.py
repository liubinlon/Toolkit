# //                          FILE
# // Associated with ziRail_<version>.mll
# //
# //                          AUTHOR
# //  (contact@vertexture.org)
# //  www.vertexture.org
# //  Please read on the website terms of use and licensing.
# // Tutorials can be found also
# //
# //                          DATE
# //  01/05/2020
# //
# //                          DESCRIPTION
# //      Retopo tool inspired by blender Bsurface
# //
# ////////////////////////////////////////////////////////////////////////////////////*/

from pdb import set_trace as db
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import Qt.QtCompat

import maya.cmds as cmds
from maya.OpenMaya import *
import maya.mel as mel

import zi_wireframe

import zi_UI.zi_RailUI
import zi_Widget.zi_Windows
import zi_UI.ziRessources_rc

import math

help = """

<html><head/><body><p align="center"><img src=":/vertexture/skin/vertexture/logoHs_color.png"/></p><p><br/><br/></p><p><span style=" font-size:10pt; font-weight:600; color:#7e835a;">ziRail </span>creates patch polygons along your strokes. These strokes are drawn directly on a mesh. By doing so, creating polygons become intuitiv. This can be used as a companion tool for retopology tasks. <a href="https://www.vertexture.org/?page_id=1809"><span style=" text-decoration: underline; color:#0000ff;">ziWireframe </span></a>is shipped with it.</p><p><br/></p><p><span style=" font-weight:600; color:#7e835a;">Source</span> - Specify a base mesh. The newly created polygons will be snap on it.</p><p><span style=" font-weight:600; color:#7e835a;">As Reference</span><span style=" font-weight:600;"> - </span>Will set the Source mesh as reference. That is convenient if you need to select the components of a mesh ontop of it</p><p><span style=" font-weight:600; color:#7e835a;">Uspans</span> - Specify the amount of subdivisions along the <span style=" font-weight:600;">U</span> direction of the patch. This can be done before and after the patch creation. It will have no effect if you have created the last patch from existing polygon.</p><p><span style=" font-weight:600; color:#7e835a;">Vspans</span>- Specify the amount of subdivisions along the V direction of the patch. This can be done before and after the patch creation. <br/></p><p><span style=" font-weight:600; color:#7e835a;">Projection distance</span>- ziRail a projection based plug-in. This is the max ray distance searching for the closestPoint. A too high value would reduce performance and cause artefacts.</p><p><span style=" font-weight:600; color:#7e835a;">Bridge Subdivs</span>- When creating a bridge surface, this will set the amount of subdvision.</p><p><br/></p><p><span style=" font-weight:600; color:#7e835a;">Close Strokes</span>- While creating grid you may need to have closed strokes (ie. eyelids).</p><p><span style=" font-weight:600; color:#7e835a;">Tweak Mode</span> - Allows to move the vertices and keep the modification on the surface of the source mesh. You can use wathever modifiers for tweaking. This works on vertices/vertex selection (not edges or faces).You can also use Interactiv tweak with MMB drag.</p><p><span style=" font-weight:600; color:#7e835a;">Relax Brush</span>- The brush manipulators does a basic relax task while snapping on the source mesh.</p><p><span style=" font-weight:600; color:#7e835a;">Freeze Borders </span>- So you can relax while preserving the boundary vertices positions.</p><p><br/></p><p><span style=" font-weight:600; color:#7e835a;">Relax Intensity</span>- The relax brush strength</p><p><span style=" font-weight:600; color:#7e835a;">Relax Radius</span>- The relax brush diameter</p><p><span style=" font-weight:600; color:#7e835a;">Tweak Radius</span>- The tweak brush diameter</p><p><br/></p><p><span style=" font-weight:600; color:#7e835a;">SHADER VIEWPORT UI</span> - Advanced parameters for the mesh display</p><p><span style=" font-weight:600; color:#7e835a;">Toggle</span>- activate/deactivate the custom viewport wich display the wireframe</p><p><br/></p><p><span style=" font-weight:600; color:#7e835a;">Rail Mode</span>- Start drawing the strokes.</p><p>---</p><p align="center"><span style=" font-weight:600;">RAIL MODE</span></p><p><span style=" font-weight:600; color:#7e835a;">(DRAW STROKE(s))</span><span style=" font-weight:600;"> LMB + DRAG </span>- On source mesh will draw a stroke. You can repeat the process as much as need to have several strokes. by pressing <span style=" font-weight:600;">ENTER</span>, you will create patches along the strokes. The direction of the strokes has to be consistent so you have a expected result. The strokes are the guides for the resulting patches the polygons in between are interpolated. You may have a better result by reducing the distance between these strokes. You can append polygons from an existing mesh (select it) or from scratch (with an empty selection)</p><p><span style=" font-weight:600; color:#7e835a;">(REDRAW RAIL)</span><span style=" font-weight:600;"> LMB+ CTRL + DRAG </span>- Will modify the last created patch so its fits this stroke. After pressing <span style=" font-weight:600;">ENTER, </span>you can still modify the last line of a patch. For doing so, select a boundary line (explain bellow).</p><p><span style=" font-weight:600; color:#7e835a;">(BORDER RESHAPE)</span><span style=" font-weight:600;"> CTRL + SHIFT + LMB </span>- On a boundary vertex to have an anchor point. Reproduce the same step another boundary vertex to have a boundary line. This boundary line is basically a stroke. Drawing another stroke will create a patch. </p><p><span style=" font-weight:600; color:#7e835a;">(PATCH CREATION FROM PROFILE) </span><span style=" font-weight:600;">LMB + DRAG </span>- With a boundary line selected will create a patch to this stroke ( considered as a profile).</p><p><span style=" font-weight:600; color:#7e835a;">(PATCH CREATION FROM PATH) </span><span style=" font-weight:600;">LMB + SHIFT + DRAG</span> - With a boundary line selected will create a patch along this stroke (considered as a path).</p><p><span style=" font-weight:600; color:#7e835a;">(PATCH CREATION FROM SLICE)</span><span style=" font-weight:600;"> LMB + SHIFT + DRAG </span>- With no line or anchor selected, drag from outside the mesh to draw slices. When ENTER pressed, this will create rails.</p><p><span style=" font-weight:600; color:#7e835a;">(MERGE LOOPS) </span><span style=" font-weight:600;">MMB + SHIFT </span>With a boundary line selected, SHIFT+MMB on a boundary vertex prepare a loop merge. Then press Enter</p><p><span style=" font-weight:600; color:#7e835a;">(POLYBRIDGE LOOPS) </span><span style=" font-weight:600;">MMB + CTRL </span>With a boundary line selected, CTRL+MMB on a boundary vertex to prepare a polyBridge creation. Then press Enter</p><p><span style=" font-weight:600; color:#7e835a;">(MERGE BOUNDARY VERTICES) </span><span style=" font-weight:600;">MMB + CTRL</span>Click on a boundary vertex then another one to merge them</p><p><span style=" font-weight:600; color:#7e835a;">(RELAX BRUSH INTERACTIVE) </span><span style=" font-weight:600; ">MMB + CTRL + SHIFT </span>Same function as the Relax brush but got activated until you release the key combinaison</p><p><span style=" font-weight:600; color:#7e835a;">(TWEAK BRUSH INTERACTIVE) </span><span style=" font-weight:600;">MMB </span>Same function as the Tweak mode but got activated until you release the key combinaison</p><p><span style=" font-weight:600; color:#7e835a;">(VSPAN CHANGE INTERACTIVE) </span><span style=" font-weight:600;">MMB + SHIFT (drag left or right) </span>Change interactively the V amount of span of the last created patch. </p><p>With the MMB and SHIFT hold move left to decrease the value or right to increase. </p><p><br/></p><p><br/></p><p>------------------------------------------------------------</p><p>for more informations and video tutorials, please visit</p><p><a href="www.vertexture.org"><span style=" text-decoration: underline; color:#0000ff;">www.vertexture.org</span></a></p><p align="justify"><span style=" font-weight:600;">MMB+DRAG</span> on whatever widgets to move the window.</p><p align="justify"><span style=" font-weight:600;">RMB+DRAG</span> on whatever widgets to scale up or down the window.</p><p align="justify"><br/><span style=" font-size:7pt;">LMB (Left Mouse Button)</span></p><p align="justify"><span style=" font-size:7pt;">MMB (Middle Mouse Button)</span></p><p align="justify"><span style=" font-size:7pt;">RMB (Right Mouse Button)</span></p><p>&quot;&quot;&quot; </p></body></html>
"""

__version__ = 0.85
__tool__ = "ziRail"
__author__ = "VERTEXTURE"

NAMEPLUGS = ["ziRail", "ziWireframeViewport"]
ATTRSNAP = "zisnap"
VERBOSE = False


class Options(object):

    attrMT = 'zi_mergThreshold'
    attrD = 'zi_distancesnap'
    attrDep = 'ziCutDp'
    attrU = 'zi_uspan'
    attrV = 'zi_vspan'
    attrB = 'zi_bdiv'

    attrInt = 'zi_railIntens'
    attrRad = 'zi_railRadius'
    attrFrz = 'zi_railFreeze'
    attrTwR = 'zi_railTweakR'

    def __init__(self):
        self._source = None
        self.numjob = int()

        # -- has to be lower than 1000 to display the helpers correctly
        if self.getAttribute(self.attrDep, 990) > 1000:
            cmds.optionVar(fv=[self.attrDep, 990])
            cmds.warning("Depth Priory was higher than 1000")

    def getAttribute(self, attr, default):

        if cmds.optionVar(exists=attr):
            return cmds.optionVar(q=attr)

        return default

    def clearAttrs(self):

        map(lambda x: cmds.optionVar(remove=x), [self.attrMT,
                                                 self.attrD,
                                                 self.attrU,
                                                 self.attrV,
                                                 self.attrB,
                                                 self.attrInt,
                                                 self.attrRad,
                                                 self.attrFrz,
                                                 self.attrTwR])

    # GETTER

    @property
    def numjob(self):
        return self._numjob

    @property
    def source(self):
        return self._source

    @source.setter
    def sourceShape(self, shape):
        self._source = shape

    @property
    def mergeThreshold(self):
        return self.getAttribute(self.attrMT, 0.001)

    @property
    def distance(self):
        return self.getAttribute(self.attrD, 100)

    @property
    def u(self):
        return self.getAttribute(self.attrU, 5)

    @property
    def v(self):
        return self.getAttribute(self.attrV, 5)

    @property
    def bdiv(self):
        return self.getAttribute(self.attrB, 1)

    @property
    def intensity(self):
        return self.getAttribute(self.attrInt, 50)

    @property
    def radius(self):
        return self.getAttribute(self.attrRad, 50)

    @property
    def freeze(self):
        return self.getAttribute(self.attrFrz, 1)

    @property
    def tweakR(self):
        return self.getAttribute(self.attrTwR, 50)

    # SETTER
    @v.setter
    def v(self, value):
        cmds.optionVar(iv=[self.attrV, value])

    @u.setter
    def u(self, value):
        cmds.optionVar(iv=[self.attrU, value])

    @bdiv.setter
    def bdiv(self, value):
        cmds.optionVar(iv=[self.attrB, value])

    @mergeThreshold.setter
    def mergeThreshold(self, value):
        cmds.optionVar(fv=[self.attrMT, value])

    @distance.setter
    def distance(self, value):
        cmds.optionVar(fv=[self.attrD, value])

    @numjob.setter
    def numjob(self, value):
        self._numjob = value

    @intensity.setter
    def intensity(self, value):
        cmds.optionVar(fv=[self.attrInt, value])

    @radius.setter
    def radius(self, value):
        cmds.optionVar(fv=[self.attrRad, value])

    @freeze.setter
    def freeze(self, value):
        cmds.optionVar(iv=[self.attrFrz, value])

    @tweakR.setter
    def tweakR(self, value):
        cmds.optionVar(iv=[self.attrTwR, value])


class Mesh(object):

    def __init__(self):
        pass

    @staticmethod
    def shape(transform):
        """Description
        """
        shapes = cmds.listRelatives(transform[0], shapes=True, type='mesh')
        return shapes[0] if shapes else None

    @staticmethod
    def node(shape, obj):
        """Ensure the zirail and selection network got created

        :Param shape: shape selection
        :Type shape: str()

        :Param obj: the main instanced object
        :Type obj: object()

        """
        nodes = cmds.ls(typ=__tool__)

        if nodes and shape:
            obj.connect(shape, 'outMesh', nodes[0], 'ziRailMesh')

            return nodes[0]

        obj.createStream()
        return Mesh.node(shape, obj)


class Win(zi_Widget.zi_Windows.Frameless,
          QObject,
          zi_UI.zi_RailUI.Ui_MainWindow):

    def __init__(self):
        super(Win, self).__init__()

        self.ctx = ""
        self.setupUi(self)
        self.loadPlugin()

        self.opt = Options()

        # self.setHotkeys()
        self.setConnections()
        self.setIcons()
        self.setWin()
        self.setBackConnections()

        self.show()

    def setWin(self):
        """Set misc preference for the QMainWindow and QWidgets
        """
        title = "%s %s" % (__name__, __version__)
        self.addBar(help, NAMEPLUGS[0])

        self.setWindowTitle(title)

        self.logo.setPixmap(
            self.logo.pixmap()
            .scaledToWidth(90, Qt.QtCore.Qt.SmoothTransformation))

        self.setMinimumSize(225, 450)
        self.setMaximumSize(900, 900)

        # get rid of this feature, obsolete
        self.opt.mergeThreshold = 0.001  # -- force to this value

        map(lambda x: x.setHidden(True), [self.spinLab,
                                          self.mergeTSpin,
                                          self.blankUBtn,
                                          self.blankVBtn
                                          ])

        self.opt.distance = 100  # -- default value for most cases
        self.distanceSpin.setValue(self.opt.distance)
        self.mergeTSpin.setValue(self.opt.mergeThreshold)
        self.freezeBtn.setChecked(self.opt.freeze)
        self.bridgeSpin.setValue(self.opt.bdiv)
        self.Uspin.setValue(self.opt.u)
        self.Vspin.setValue(self.opt.v)

        map(lambda x: x.setEnabled(True), [self.forceSlid,
                                           self.radiusSlid,
                                           self.tweakRadSlid])

        self.butTheme.clicked.emit()
        self.setFocusPolicy(Qt.QtCore.Qt.StrongFocus)

        # --------------------------------------------- set ColorButton widgets
        # --------------------------------------------- set ColorButton widgets

        self.wirefr = zi_wireframe.Win(False)
        self.wirefr.close()
        vars = zi_wireframe.OptVar()

        self.surfaceColor = self.wirefr.createColor("Surface")
        self.pointColor = self.wirefr.createColor("Point")
        self.lineColor = self.wirefr.createColor("Line")

        params = ["Surface Color", "Line Color", "Point Color"]
        self.colorButtons = [self.surfaceColor,
                             self.pointColor, self.lineColor]

        for button, param in zip(self.colorButtons, params):

            button.setObjectName(param)
            button.setTxt(param.split(" ")[0], 50)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            self.colorLayout.addWidget(button)

            if button == self.colorButtons[0]:
                self.wirefr.setColor(button, vars.surfColor)
                button.clicked.connect(
                    lambda: self.defineColor(self.surfaceColor))

            if button == self.colorButtons[1]:
                self.wirefr.setColor(button, vars.pointColor)
                button.clicked.connect(
                    lambda: self.defineColor(self.pointColor))

            if button == self.colorButtons[2]:
                self.wirefr.setColor(button, vars.lineColor)
                button.clicked.connect(
                    lambda: self.defineColor(self.lineColor))

        map(lambda x: x.setMaximumHeight(30), [self.surfaceColor,
                                               self.pointColor,
                                               self.lineColor])

    def resizeEvent(self, event):

        if event.type() == QEvent.Resize:

            if not hasattr(self, 'colorButtons'):
                return

            for button in self.colorButtons:
                button.setFixedWidth(
                    self.width() * (float(1) / self.colorButtons.__len__()))

    def refreshColors(self):
        self.wirefr.setColor(self.surfaceColor, self.wirefr.var.surfColor)
        self.wirefr.setColor(self.pointColor, self.wirefr.var.pointColor)
        self.wirefr.setColor(self.lineColor, self.wirefr.var.lineColor)

    def defineColor(self, wid):
        colors = self.wirefr.getColor(wid)
        self.wirefr.setColor(wid, colors)

        name = wid.objectName()

        for i in xrange(3):

            cmds.optionVar(fv=(zi_wireframe.kColors[name][i], colors[i]))

        cmds.refresh(cv=True, f=True)

    def setBackConnections(self):
        """Check if a ziRail connection already exist to set the source mesh
        """
        node = cmds.ls(typ=__tool__)

        if node:

            meshes = cmds.listConnections('%s.ziRailMesh' % node[0])
            if meshes:
                # -- saving the current selection
                prevSelection = cmds.ls(sl=True)

                cmds.select(meshes[0], replace=True)
                self.pickSrcBtn.clicked.emit()
                self.restoreReferenceState()

                cmds.select(prevSelection, replace=True)

    def setIcons(self):
        """Set QPushButton::QIcon images for UI
        """
        self.viewportBtn.setIcon(QIcon(":render_layeredShader.png"))
        self.closeStrokeBtn.setIcon(QIcon(":attachCurves.png"))

        self.launch.setIcon(QIcon(":birail1Gen.png"))
        self.launch.setIcon(QIcon(":birail1Gen.png"))
        self.relaxBrBtn.setIcon(QIcon(":putty.png"))
        self.freezeBtn.setIcon(QIcon(":Freeze.png"))
        self.tweakBtn.setIcon(QIcon(":Grab.png"))

    def setHotkeys(self):
        """Set hotkeys to speed up the workflow, deactivated for now.
        """
        mayWin = zi_Widget.zi_Windows.getMayaWin()

        self.plus = QShortcut(QKeySequence(Qt.QtCore.Qt.Key_Plus), mayWin)
        self.minus = QShortcut(QKeySequence(Qt.QtCore.Qt.Key_Minus), mayWin)
        self.plus.activated.connect(lambda: self.spansArrow(self.Vspin, 1))
        self.minus.activated.connect(lambda: self.spansArrow(self.Vspin, -1))

    def setConnections(self):
        """Set QSignals and QSlots for QWidgets
        """
        # -- have to be set before the connections
        self.tweakRadSlid.setValue(self.opt.tweakR)
        self.forceSlid.setValue(self.opt.intensity)
        self.radiusSlid.setValue(self.opt.radius)

        # -- QSignals and QSlots setup
        self.pickSrcBtn.clicked.connect(self.pickSource)

        self.blankVBtn.clicked.connect(lambda: self.blank(self.blankVBtn, "v"))
        self.blankUBtn.clicked.connect(lambda: self.blank(self.blankUBtn, "u"))

        self.upUBtn.clicked.connect(lambda: self.spansArrow(self.Uspin, 1))
        self.dnUBtn.clicked.connect(lambda: self.spansArrow(self.Uspin, -1))
        self.upVBtn.clicked.connect(lambda: self.spansArrow(self.Vspin, 1))
        self.dnVBtn.clicked.connect(lambda: self.spansArrow(self.Vspin, -1))

        self.refBox.stateChanged.connect(self.referenceState)

        self.distanceSpin.valueChanged.connect(self.changeDistance)
        self.mergeTSpin.valueChanged.connect(self.changeThreshold)
        self.bridgeSpin.valueChanged.connect(self.changeBridge)

        self.shaderApplyBtn.clicked.connect(self.applyViewport)
        self.viewportBtn.clicked.connect(self.setViewport)

        self.tweakRadSlid.valueChanged.connect(self.setTweakR)
        self.closeStrokeBtn.clicked.connect(self.closeStroke)
        self.radiusSlid.valueChanged.connect(self.relaxBrush)
        self.forceSlid.valueChanged.connect(self.relaxBrush)

        self.Uspin.valueChanged.connect(self.spansChanged)
        self.Vspin.valueChanged.connect(self.spansChanged)

        self.freezeBtn.clicked.connect(self.relaxFreezeBrush)
        self.relaxBrBtn.clicked.connect(self.relaxBrush)
        self.tweakBtn.clicked.connect(self.tweakMode)

        self.launch.clicked.connect(self.launching)

    def closeEvent(self, event):
        self.clearState()

    def clearState(self):
        # -- if already a mesh make sure we restore its state

        if not self.opt.sourceShape:
            return

        if cmds.objExists(self.opt.sourceShape):
            self.setRef(self.opt.sourceShape, False)
            self.setShading(self.opt.sourceShape, True)
            self.refBox.setChecked(False)

    def setTweakR(self):
        """Description
        """
        radius = self.tweakRadSlid.value()
        self.opt.tweakR = radius

    def spansArrow(self, func, incr):
        """Called function for changing spans u or v direction
        :Param func: the method to exec
        :Type func: function obj

        :Param incr: the value to set
        :Type incr: int()
        """
        func.setValue(func.value() + incr)
        func.editingFinished.emit()

    def changeDistance(self):
        """Set distance variable
        """
        self.opt.distance = float(self.distanceSpin.value())

    def changeThreshold(self):
        """Description
        """
        self.opt.mergeThreshold = float(self.mergeTSpin.value())

    def spansChanged(self, dummy):
        """Change the u or v spans sudbdivisions of the last created patch
        """
        if not self.ctx:
            return

        if self.ziRailNode():
            cmds.ziRailCmd(v=int(self.Vspin.value()),
                           u=int(self.Uspin.value()))

            if cmds.contextInfo(self.ctx, exists=True):
                cmds.ziRailContext(self.ctx, e=True, refresh=True)

    def referenceState(self, state):

        bsmesh = self.opt.sourceShape

        if not bsmesh:
            cmds.warning("please set a source mesh first")
            return

        self.setRef(bsmesh, state)

    def setShading(self, bsmesh, state):

        self.setAttribute(bsmesh, "overrideEnabled",
                          True if state is False else False)
        self.setAttribute(bsmesh, "overrideShading", state)

        # res = "deactivated" if state == False else "activated"
        # cmds.warning("%s overridshading is %s" % (bsmesh, res))

    def setRef(self, bsmesh, state):

        if not cmds.objExists(bsmesh):
            return

        overrid = True if state == 2 else False
        self.setAttribute(bsmesh, "overrideEnabled", overrid)
        self.setAttribute(bsmesh, "overrideDisplayType", state)

        # res = "activated" if state == 2 else "deactivated"
        # cmds.warning("%s reference is %s" % (bsmesh, res))

    def setAttribute(self, obj, attr, value):

        if not cmds.objExists(obj):
            return

        if not cmds.getAttr("{}.{}".format(obj, attr), lock=True):
            cmds.setAttr('{}.{}'.format(obj, attr), value)

    def restoreReferenceState(self):

        if not cmds.objExists(self.opt.sourceShape):
            return

        state = cmds.getAttr(
            '{}.overrideDisplayType'.format(self.opt.sourceShape))

        res = True if state == 2 else False
        self.refBox.setChecked(res)

    def getSelection(self):
        """Query the current selection
        """
        sels = cmds.ls(hilite=True) + cmds.ls(sl=True, o=True)

        if not sels:
            cmds.error("please select a mesh")

        shapes = cmds.listRelatives(sels[0], shapes=True)

        if not shapes:
            cmds.error("please select a valid mesh")

        if cmds.nodeType(shapes[0]) == "mesh":
            return shapes[0]

        else:
            cmds.error('cannot retrieves a valid mesh from selection')

    def applyViewport(self):
        """Set the Vertexture viewport
        """
        sel = self.getSelection()

        panels = cmds.getPanel(type="modelPanel")
        for panel in panels or []:

            if self.shaderApplyBtn.isChecked():

                cmd = "setRendererAndOverrideInModelPanel $gViewport2 %s %s"
                mel.eval(cmd % ("VertextureViewport", panel))

                self.setShading(sel, False)
                # self.setAttribute(sel, "overrideEnabled", True)
                # self.setAttribute(sel, "overrideShading", False)

        if not self.shaderApplyBtn.isChecked():
            cmd = "setRendererInModelPanel $gViewport2 %s"
            mel.eval(cmd % (panel))

            self.setShading(sel, True)
            # self.setAttribute(sel, "overrideEnabled", False)
            # self.setAttribute(sel, "overrideShading", True)

    def setViewport(self):
        """Open the viewport UI
        :return : the QMainWindow object
        """
        self.loadPlugin()
        zi_wireframe.main().show()

    def closeStroke(self):
        cmds.ziRailCmd(close=True)

    def tweakMode(self):
        """Description
        """
        self.relaxBrBtn.setChecked(False)

        if self.tweakBtn.isChecked():
            shape = self.getShape()

            # -- no selection then skipp
            if not shape:
                return

            # -- if tweaknode not created yet, create a new one
            node = self.ziTweakNode()
            if not node:
                node = [cmds.createNode("ziTweakNode", ss=True)]

            # -- make the connections of tweak node
            self.attachTweakNode(shape, node[0])

            # -- switch to component mode and move tool
            mel.eval("""setSelectMode components Components;\
                selectType -smp 1 -sme 0 -smf 0 -smu 0 -pv 1\
                 -pe 0 -pf 0 -puv 0; HideManipulators;\
                  setToolTo $gMove """)

        if not self.tweakBtn.isChecked():
            self.detachTweakNode()

    def tweakFunc(self, geoA, geoB):
        """Description

        :Param geoA: the tweakable geo
        :Type geoA: str()

        :Param geoB: the geo where the tweakable geo got snapped
        :Type geoB: str()

        """
        attribute = "%s.%s" % (geoA, ATTRSNAP)
        res = cmds.getAttr(attribute)

        if not res or not cmds.objExists(attribute):
            self.tweakBtn.setChecked(False)

        cmds.ziTweakCmd(tm=geoB)

    def relaxFreezeBrush(self):
        """Freeze border SLOT
        """
        self.relaxBrBtn.setChecked(True)
        self.relaxBrush()

    def relaxBrush(self):
        """Relax CMD
        """
        radius = self.radiusSlid.value() * 5
        itn = self.forceSlid.value() * .0005
        v = True if self.freezeBtn.isChecked() else False

        # -- to restore later or interactiv context
        self.opt.radius = self.radiusSlid.value()
        self.opt.intensity = self.forceSlid.value()
        self.opt.freeze = v

        # -- preserve the tweak node for meshinter optimisation
        if self.ziTweakNode():
            self.detachTweakNode()

        if self.relaxBrBtn.isChecked():
            self.tweakBtn.setChecked(False)

            self.setContext()

            if cmds.contextInfo(self.ctx, exists=True):
                cmds.ziRailContext(self.ctx, e=1, rb=1,
                                   rad=radius, i=itn, fr=v)
                return

    def setMmesh(self):
        """Description
        """
        console("setMMesh")
        if cmds.contextInfo(self.ctx, exists=True):
            cmds.deleteUI(self.ctx)
            console("deteteui setmmesh")

        self.setContext()
        cmds.setToolTo('selectSuperContext')
        cmds.select(clear=True)

    def setContext(self):
        """Description
        """
        if cmds.contextInfo(self.ctx, exists=True):
            cmds.setToolTo(self.ctx)

        else:
            self.ctx = cmds.ziRailContext()
            cmds.setToolTo(self.ctx)

    def blank(self, obj, span):
        """Description
        """
        func = self.disableU if span == "u" else self.disableV
        mode = False if obj.isChecked() else True
        func(mode)

        if span == 'u':
            self.opt.u = 1 if obj.isChecked() else self.Uspin.value()

        if span == 'v':
            self.opt.v = 1 if obj.isChecked() else self.Vspin.value()

    def disableU(self, mode):
        map(lambda x: x.setEnabled(mode), [self.upUBtn,
                                           self.dnUBtn,
                                           self.Uspin])

    def disableV(self, mode):
        map(lambda x: x.setEnabled(mode), [self.upVBtn,
                                           self.dnVBtn,
                                           self.Vspin])

    def changeBridge(self):
        """Description
        """
        self.opt.bdiv = int(self.bridgeSpin.value())

    def launching(self):
        """Launch the main context tool
        """
        if not cmds.constructionHistory(q=True, tgl=True):
            cmds.error("Please activate the construction history")

        Mesh.node(self.opt.source, self)

        if self.pickSrcBtn.text() in cmds.ls(sl=True):
            cmds.select(clear=True)

        nodes = cmds.ls(typ="ziTweakNode")
        self.detachTweakNode()
        map(lambda x: x.setChecked(False), [self.relaxBrBtn, self.tweakBtn])

        self.refreshColors()
        self.setContext()

    def pickSource(self):
        """Specify the source mesh and make its connections
        """
        sels = cmds.ls(sl=True)

        if not sels:
            cmds.error("invalid selection")

        shape = Mesh.shape(sels)

        if not shape:
            cmds.error("invalid selection")

        self.clearState()

        self.opt.sourceShape = shape
        node = Mesh.node(shape, self)

        self.sender().setText(sels[0])
        self.connect(shape, "outMesh", node, "ziRailMesh")

        self.initNodes()
        self.setMmesh()

    def setupNetwork(self):
        """Create the networks connection
        """
        if not self.ziRailNode():
            self.createStream()

    def createStream(self):
        """Create the connection and node if not exist
        """
        sels = cmds.ls(sl=True)

        node = ''
        currentNodes = cmds.ls(typ=__tool__)

        if not currentNodes:
            node = cmds.createNode(__tool__, n='ziRailShape')
        else:
            node = currentNodes[0]

        if not cmds.nodeType(node) == __tool__:
            cmds.delete(node)
            cmds.error("please load the plugin")

        if not self.opt.sourceShape:
            cmds.error("Please specify a source mesh first")

        if not cmds.objExists(self.opt.sourceShape):
            cmds.error("please specify a valid source")

        self.connect(self.opt.sourceShape, 'outMesh', node, 'ziRailMesh')

        console("\"%s\" connected to %s" % (self.opt.sourceShape, node))

        # -- restoring previous selection
        cmds.select(sels, replace=True)

    def initNodes(self):
        """Description
        """
        tweaknode = self.ziTweakNode()

        if tweaknode:
            cmds.delete(tweaknode)

    def ziTweakNode(self):
        """Returns the node of type ziTweakNode in the scene as list or []
        """
        # self.freezeBtn.setChecked(False)
        return cmds.ls(typ="ziTweakNode")

    def detachTweakNode(self):
        """Description
        """
        tweaknode = self.ziTweakNode()
        shape = self.getShape()

        if cmds.objExists(self.opt.sourceShape) and tweaknode and shape:

            self.disconnect(self.opt.sourceShape,
                            'worldMesh[0]', tweaknode[0], 'scanMesh')
            self.disconnect(tweaknode[0], "ziTweakEval", shape, "visibility")
            self.disconnect(shape, "worldMesh[0]", tweaknode[0], "lowMesh")

    def linkJob(self, node1, attr1, node2, attr2, connect):
        """Description

        :Param  node1:
        :Type  node1:

        :Param  attr1:
        :Type  attr1:

        :Param  node2:
        :Type  node2:

        :Param  attr2:
        :Type  attr2:
        """
        console("linkjob: %s.%s  -->> %s.%s" % (node1, attr1, node2, attr2))

        for node in [node1, node2]:

            if not cmds.objExists(node):
                cmds.error("the node %s does not exist" % node)

        male = '.'.join([node1, attr1])
        female = '.'.join([node2, attr2])

        if connect:
            if not cmds.isConnected(male, female):
                cmds.connectAttr(male, female, f=True)

        else:
            if cmds.isConnected(male, female):
                cmds.disconnectAttr(male, female)

    def connect(self, node1, attr1, node2, attr2):
        self.linkJob(node1, attr1, node2, attr2, True)

    def disconnect(self, node1, attr1, node2, attr2):
        self.linkJob(node1, attr1, node2, attr2, False)

    def attachTweakNode(self, shape, node):
        """Set the connections from tweaknode, selections and source
        if tweakNode already exists, reconnect

        :Param shape: the current selection
        :Type shape: str()

        :Param node: the existing tweakNode path or None
        :Type node: str()
        """
        self.connect(self.opt.sourceShape, "worldMesh[0]", node, "scanMesh")
        self.connect(node, "ziTweakEval", shape, "visibility")
        self.connect(shape, "worldMesh[0]", node, "lowMesh")

    def ziRailNode(self):
        """Get a ziRail node or create one if none
        """
        return Mesh.node(self.opt.source, self)

    def getShape(self):
        """Description
        """
        sels = cmds.ls(hl=True) + cmds.ls(sl=True, o=True)
        for sel in sels:
            shapes = cmds.listRelatives(sel, shapes=True)

            if shapes:
                if cmds.nodeType(shapes[0]) == 'mesh':
                    return shapes[0]

    def loadPlugin(self):
        version = cmds.about(v=True)

        for plug in NAMEPLUGS:
            name = "{name}_{ver}".format(name=plug, ver=version)

            if not cmds.pluginInfo(name, q=True, loaded=True):

                try:
                    cmds.loadPlugin(name)
                    console("{} loaded".format(name))
                except:
                    cmds.error("""Cannot load plugin %s please make sure\
                     the *.mll file is in the correct folder,\
                     a video tutorial is on the website""" % name)

    # ----------------------------------------------- hotkey wrappers
    # ----------------------------------------------- hotkey wrappers

    def VspanUp(self):
        self.spansArrow(self.Vspin, 1)

    def VspanDn(self):
        self.spansArrow(self.Vspin, -1)

    def UspanUp(self):
        self.spansArrow(self.Uspin, 1)

    def UspanDn(self):
        self.spansArrow(self.Uspin, -1)

    def closeStrokes(self):
        cmds.ziRailCmd(close=True)

    def relax(self):
        self.relaxBrBtn.setChecked(True)
        self.relaxBrBtn.clicked.emit()

    def railMode(self):
        self.launch.clicked.emit()

    def tweak(self):
        self.tweakBtn.setChecked(True)
        self.tweakBtn.clicked.emit()

    def freezeBorder(self):
        self.freezeBtn.setChecked(not self.freezeBtn.isChecked())
        self.freezeBtn.clicked.emit()


# -----------------------------------------------  DEBUG FUNCTION
# -----------------------------------------------  DEBUG FUNCTION

    @staticmethod
    def loc(pos, name=''):
        grpName = 'locs'
        if not cmds.objExists(grpName):
            cmds.createNode('transform', n=grpName)

        node = cmds.spaceLocator(n=name, p=(pos[0], pos[1], pos[2]))[0]
        cmds.setAttr('%s.localScaleX' % node, 0.1)
        cmds.setAttr('%s.localScaleY' % node, 0.1)
        cmds.setAttr('%s.localScaleZ' % node, 0.1)

        cmds.delete(node, ch=True)
        cmds.xform(node, cpc=True)
        cmds.parent(node, grpName)

    @staticmethod
    def locs(pos, name=""):
        [Win.loc(p, name) for p in pos]

    @staticmethod
    def curv(points, name=""):
        poses = map(lambda x: (x[0], x[1], x[2]), points)
        cmds.curve(d=1, p=poses)


def console(*txt):
    """Description
    """
    if not VERBOSE:
        return

    txt = map(str, txt)
    print("ziRInfo. {:_>50}".format(' '.join(txt)))


# ----------------------------------------------- MAIN FUNCTION

def main():
    global ziRailObj

    try:
        ziRailObj.deleteLater()
    except:
        pass

    ziRailObj = Win()
    return ziRailObj
