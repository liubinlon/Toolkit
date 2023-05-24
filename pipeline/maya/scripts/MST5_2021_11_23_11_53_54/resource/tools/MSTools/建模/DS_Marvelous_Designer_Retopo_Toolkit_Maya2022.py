#DS_Marvelous_Designer_Retopo_Toolkit_Maya2022.py
###Author: Derrick Sesson###
###Website: derricksesson.com###
###Release Version: 1.0.0###

from maya import cmds, mel
import random
import maya.OpenMayaUI as omui
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance


def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class FrameLayout(QtWidgets.QGroupBox):
    def __init__(self, parent=None):
        super(FrameLayout, self).__init__(parent)
        self.setCheckable(True)
        self.setChecked(True)


        self.clicked.connect(self.collapse)


    def collapse(self):
        '''
        Toggles the QGroupBox's maximum height to achieve a collapsing effect.
        '''
        parent = self.parent()
        parent_size_hint = parent.minimumSizeHint()
        size_hint = self.minimumSizeHint()

        if self.isChecked():
            self.setMaximumHeight(167777)


            self.resize(self.width(), size_hint.height())
            parent.resize(parent.width(), parent_size_hint.height())

        else:
            self.setMaximumHeight(19)
            self.resize(self.width(), size_hint.height())
            parent.resize(parent.width(), parent_size_hint.height())



class DS_MD_Retopo(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(DS_MD_Retopo, self).__init__(parent)

        self.setWindowTitle("Marvelous Designer Retopo Tools")
        self.setWindowFlags((self.windowFlags()
                             ^ QtCore.Qt.WindowContextHelpButtonHint))

        # self.setMaximumHeight(self.height())

        # Create Widgets

        # Create Total Selected CVs Widgets
        total_cvs_label = QtWidgets.QLabel('Total CVs: ')
        self.total_cvs_field = QtWidgets.QLineEdit()
        self.total_cvs_field.setText('0')
        self.total_cvs_field.setEnabled(False)

        self.total_cvs_button = QtWidgets.QPushButton('Get Total Selected CVs')
        self.total_cvs_button.setToolTip("Display Total CVs for one or more curves.")

        # Create Curve Widgets
        self.set_angle_threshold_label = QtWidgets.QLabel('Set Angle Threshold:')
        self.set_angle_threshold_spinbox = QtWidgets.QSpinBox()
        self.set_angle_threshold_spinbox.setMaximumWidth(50)
        self.set_angle_threshold_spinbox.setValue(30)


        self.create_curves_button = QtWidgets.QPushButton('Create Border Curves')
        self.create_curves_button.setMinimumWidth(120)
        self.create_curves_button.setMinimumHeight(40)
        self.create_curves_button.setToolTip("Create curves on the borders of your flat mesh. \nUse the Angle Threshold to define the angle change when a new curve is created.")


        # Create Split/Merge Curve Widgets
        self.split_curve_field = QtWidgets.QLineEdit()
        # self.split_curve_field.setFixedWidth(30)
        self.split_curve_field.setPlaceholderText('CV Index')

        self.split_curve_button = QtWidgets.QPushButton('Split Curve')
        self.split_curve_button.setToolTip('Split curve at given cv index. Use "Inverse Order" to reverse the direction of the index split.')

        self.split_curve_inverse_order_box = QtWidgets.QCheckBox('Inverse Order')

        self.rebuild_curve_button = QtWidgets.QPushButton('Rebuild Curve')
        self.rebuild_curve_button.setToolTip("Rebuild the selected curve or curves to have the given cv count.")
        self.rebuild_curve_field = QtWidgets.QLineEdit()
        self.rebuild_curve_field.setPlaceholderText('CV count')

        self.merge_curve_button = QtWidgets.QPushButton('Merge Curves')
        self.merge_curve_button.setToolTip("Merge two or more selected curves.")


        self.normalize_curve_spacing_button = QtWidgets.QPushButton('Normalize Curve Spacing')
        self.normalize_curve_spacing_button.setToolTip("Creates even spacing between cvs for selected curves.")



        self.create_curve_from_isoparm_button = QtWidgets.QPushButton('Create Curve From Isoparm')
        self.create_curve_from_isoparm_button.setToolTip("Create curves from one or more selected NURBS isoparms.")
        self.create_curve_from_edges_button = QtWidgets.QPushButton('Create Curve From Edges')
        self.create_curve_from_edges_button.setToolTip("Create a curve from the current polygon edgeloop selection.")


        # Create Surface Widgets

        self.create_surface_3_sides_button = QtWidgets.QPushButton('Create Surface (3 Sides)')
        self.create_surface_3_sides_button.setToolTip("Create a NURBS surface from 3 curves. \nSelect a main center curve and it's two sides.")

        self.create_surface_4_sides_button = QtWidgets.QPushButton('Create Surface (4 Sides)')
        self.create_surface_4_sides_button.setToolTip("Create a NURBS surface from 4 curves.")

        self.reverse_surface_direction = QtWidgets.QPushButton('Reverse Surface Direction')
        self.reverse_surface_direction.setToolTip("Reverse NURBS surface normal direction.")

        # Create Split/Merge Surface Widgets

        split_surface_u_label = QtWidgets.QLabel("'U' Isoparm Index:")
        split_surface_v_label = QtWidgets.QLabel("'V' Isoparm Index:")

        self.split_surface_u_field = QtWidgets.QLineEdit()
        self.split_surface_u_field .setFixedWidth(30)
        self.split_surface_u_field .setText('0')

        self.split_surface_v_field = QtWidgets.QLineEdit()
        self.split_surface_v_field .setFixedWidth(30)
        self.split_surface_v_field .setText('0')

        self.split_surface_u_button = QtWidgets.QPushButton("Split Surface 'U'")
        self.split_surface_u_button.setToolTip('Split NURBS surface at given "U" index. Use "Inverse Order" to reverse the direction of the index split.')
        self.split_surface_v_button = QtWidgets.QPushButton("Split Surface 'V'")
        self.split_surface_v_button.setToolTip('Split NURBS surface at given "V" index. Use "Inverse Order" to reverse the direction of the index split.')

        self.split_surface_inverse_order_box = QtWidgets.QCheckBox('Inverse Order')



        # Create Mesh Tool Widgets

        self.convert_to_poly_button = QtWidgets.QPushButton('Convert To Poly')
        self.convert_to_poly_button.setMinimumWidth(120)
        self.convert_to_poly_button.setMinimumHeight(40)
        self.convert_to_poly_button.setToolTip("Convert and merge selected NURBS surfaces to polygon meshes.")

        self.merge_poly_meshes_button = QtWidgets.QPushButton('Merge Poly Meshes')
        self.merge_poly_meshes_button.setToolTip("Merge 2 or more polygon meshes.")


        threshold_label = QtWidgets.QLabel('Threshold:')
        self.threshold_field = QtWidgets.QLineEdit()
        self.threshold_field.setText('0.001')

        self.merge_vertices_button = QtWidgets.QPushButton('Merge Vertices')
        self.merge_vertices_button.setMinimumHeight(30)
        self.merge_vertices_button.setToolTip("Merge Vertices based on distance threshold. Select the whole mesh to merge all verts, or selected specific verts.")

        self.transfer_uvs_button = QtWidgets.QPushButton('Transfer UVs')
        self.transfer_uvs_button.setMinimumHeight(30)
        self.transfer_uvs_button.setToolTip("Select source mesh, then target mesh to transfer uvs.")

        self.relax_vertices_button = QtWidgets.QPushButton('Relax Vertices')
        self.relax_vertices_button.setMinimumHeight(30)
        self.relax_vertices_button.setToolTip("Relax interior vertices, use Relax Loops to define how many times to smooth.")

        self.relax_loop_field = QtWidgets.QLineEdit()
        self.relax_loop_field.setText('1')
        self.relax_loop_field.setMaximumWidth(35)
        self.relax_loop_field.setToolTip("Relax Loops.")

        self.transfer_button = QtWidgets.QPushButton('Transfer')
        self.transfer_button.setToolTip("Select 3d mesh, then 2d mesh, then 2d retopo mesh.\n(Make sure 2d mesh has no overlapping UVs.)")
        self.transfer_button.setMinimumWidth(120)
        self.transfer_button.setMinimumHeight(40)

        self.zipper_button = QtWidgets.QPushButton('Zipper Edge Merge')
        self.zipper_button.setToolTip("Select TWO edges sharing ONE vertex to start zipping.")
        self.zipper_button.setMinimumWidth(120)
        self.zipper_button.setMinimumHeight(40)

        self.zipper_loop_box = QtWidgets.QCheckBox('Loop through\n   edges')
        self.zipper_loop_box.setMinimumWidth(120)
        self.zipper_loop_box.setMinimumHeight(50)
        self.zipper_loop_box.setChecked(True)

        self.zipper_loop_box.setToolTip("Loop through each edge and merge until loop is complete.")


        #   Create Main Window Close Button Widget
        self.close_button = QtWidgets.QPushButton('Close')
        self.close_button.setFixedWidth(60)


        # Create Layouts

        # Create Total CV Layout
        total_cv_layout = QtWidgets.QGridLayout()

        total_cv_layout.addWidget(total_cvs_label,0,0)
        total_cv_layout.addWidget(self.total_cvs_field,0,1)
        total_cv_layout.addWidget(self.total_cvs_button,0,2)

        # Create Curve Layout
        create_curves_layout = QtWidgets.QGridLayout()
        angle_layout = QtWidgets.QHBoxLayout()
        angle_layout.addWidget(self.set_angle_threshold_label, 0)
        angle_layout.addWidget(self.set_angle_threshold_spinbox, 0)

        create_curves_layout.addLayout(angle_layout, 0, 0)
        create_curves_layout.addWidget(self.create_curves_button, 1, 0,1,3)


        # Create Split Curve Layout
        split_curves_layout = QtWidgets.QGridLayout()


        split_curves_layout.addWidget(self.split_curve_field, 0, 0)
        split_curves_layout.addWidget(self.split_curve_button, 0, 1)
        split_curves_layout.addWidget(self.split_curve_inverse_order_box, 0, 2)

        split_curves_layout.addWidget(self.rebuild_curve_field, 1, 0,1,1)
        split_curves_layout.addWidget(self.rebuild_curve_button, 1, 1,1,3)
        split_curves_layout.addWidget(self.merge_curve_button, 2, 0, 1, 4)
        split_curves_layout.addWidget(self.normalize_curve_spacing_button, 3, 0, 1, 4)
        split_curves_layout.addWidget(self.create_curve_from_isoparm_button, 4, 0, 1, 4)
        split_curves_layout.addWidget(self.create_curve_from_edges_button, 5, 0, 1, 4)

        # Create Surface Layout

        create_surface_layout = QtWidgets.QGridLayout()

        create_surface_layout.addWidget(self.create_surface_3_sides_button, 0, 0)
        create_surface_layout.addWidget(self.create_surface_4_sides_button, 1, 0)
        create_surface_layout.addWidget(self.reverse_surface_direction, 2, 0)

        # Split Surface Layout
        split_surface_layout = QtWidgets.QGridLayout()

        split_surface_layout.addWidget(split_surface_u_label, 0, 0)
        split_surface_layout.addWidget(self.split_surface_u_field, 0, 1)
        split_surface_layout.addWidget(self.split_surface_u_button, 0, 2)

        split_surface_layout.addWidget(split_surface_v_label, 1, 0)
        split_surface_layout.addWidget(self.split_surface_v_field, 1, 1)
        split_surface_layout.addWidget(self.split_surface_v_button, 1, 2)
        split_surface_layout.addWidget(self.split_surface_inverse_order_box, 0, 3,2,1)


        # Mesh Tools Layout
        mesh_tools_layout = QtWidgets.QGridLayout()

        mesh_tools_layout.addWidget(self.convert_to_poly_button,0,0,1,5)
        mesh_tools_layout.addWidget(self.merge_poly_meshes_button, 1, 0, 1, 5)
        mesh_tools_layout.addWidget(self.transfer_uvs_button,2,0, 1, 5)
        mesh_tools_layout.addWidget(threshold_label,3,0)
        mesh_tools_layout.addWidget(self.threshold_field,3,1)
        mesh_tools_layout.addWidget(self.merge_vertices_button,3,2)
        mesh_tools_layout.addWidget(self.relax_vertices_button,3,3)
        mesh_tools_layout.addWidget(self.relax_loop_field,3,4)
        mesh_tools_layout.addWidget(self.transfer_button,4,0,1,5)
        mesh_tools_layout.addWidget(self.zipper_button,5,0,2,4)
        mesh_tools_layout.addWidget(self.zipper_loop_box,5,4)

        # Create Main Layout

        main_layout = QtWidgets.QGridLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(4, 4, 4, 4)
        self.setLayout(main_layout)
        # self.tree_widget = QtWidgets.QTreeWidget()

        # groupBoxA = QtWidgets.QGroupBox("Total Selected CVs")
        groupBoxA = FrameLayout("Total Selected CVs")
        groupBoxB = FrameLayout("Create BorderCurves")
        groupBoxC = FrameLayout("Split/Merge Curves")
        groupBoxD = FrameLayout("Create Surfaces")
        groupBoxE = FrameLayout("Split Surfaces")
        groupBoxF = FrameLayout("Mesh Tools")

        groupBoxA.setLayout(total_cv_layout)
        groupBoxB.setLayout(create_curves_layout)
        groupBoxC.setLayout(split_curves_layout)
        groupBoxD.setLayout(create_surface_layout)
        groupBoxE.setLayout(split_surface_layout)
        groupBoxF.setLayout(mesh_tools_layout)

        main_layout.addWidget(groupBoxA,1,0)
        main_layout.addWidget(groupBoxB,2,0)
        main_layout.addWidget(groupBoxC,3,0)
        main_layout.addWidget(groupBoxD,4,0)
        main_layout.addWidget(groupBoxE,5,0)
        main_layout.addWidget(groupBoxF,6,0)

        groupBoxA.setMaximumHeight(groupBoxA.minimumSizeHint().height())


        # Create Connections
        self.total_cvs_button.clicked.connect(self.displayTotalCVs)

        self.create_curves_button.clicked.connect(self.createBorderCurves)
        self.split_curve_button.clicked.connect(self.splitCurve)

        self.rebuild_curve_button.clicked.connect(self.rebuildCurve)
        self.merge_curve_button.clicked.connect(self.mergeCurves)
        self.normalize_curve_spacing_button.clicked.connect(self.normalizeCurves)

        self.create_curve_from_isoparm_button.clicked.connect(self.createCurveFromIso)
        self.create_curve_from_edges_button.clicked.connect(self.createCurveFromEdges)

        self.create_surface_3_sides_button.clicked.connect(self.createSurface3)
        self.create_surface_4_sides_button.clicked.connect(self.createSurface4)
        self.reverse_surface_direction.clicked.connect(self.reverseSurfaceDirection)

        self.split_surface_u_button.clicked.connect(self.splitSurfaceU)
        self.split_surface_v_button.clicked.connect(self.splitSurfaceV)

        self.merge_poly_meshes_button.clicked.connect(self.mergePolyMeshes)

        self.convert_to_poly_button.clicked.connect(self.convertToPoly)

        self.merge_vertices_button.clicked.connect(self.mergeVertices)

        self.transfer_uvs_button.clicked.connect(self.transferUvs)

        self.relax_vertices_button.clicked.connect(self.relaxVertices)

        self.transfer_button.clicked.connect(self.transfer)

        self.zipper_button.clicked.connect(self.zipper)



        self.close_button.clicked.connect(self.close)

    def displayTotalCVs(self):
        '''
        Display CV count for selected curves.
        '''
        total_CVs = 0

        sel = cmds.ls(sl=True)

        for s in sel:
            shape = cmds.listRelatives(s, s=True)[0]

            if cmds.nodeType(shape) == 'nurbsCurve':
                spans = cmds.getAttr('%s.spans'%shape)
                total_CVs += spans


        self.total_cvs_field.setText(str(total_CVs))


    def createBorderCurves(self):
        '''
        Creates border curves for selected geo  based on Angle Threshold.
        '''
        cmds.undoInfo(openChunk=True)

        try:
            meshes = cmds.ls(sl=True)
            angle = self.set_angle_threshold_spinbox.value()

            for geo in meshes:
                cmds.select(geo)
                cmds.ConvertSelectionToEdgePerimeter(geo)
                edges = cmds.ls(sl=True, fl=True)

                edgeLines = []
                counter = 0


                crv_grp = 'crv_GRP'
                nurbs_grp = 'nurbs_GRP'
                poly_grp = 'poly_GRP'


                if not cmds.objExists(crv_grp):
                    crv_grp = cmds.group(n='crv_GRP', em=True)
                if not cmds.objExists(nurbs_grp):
                    nurbs_grp = cmds.group(n='nurbs_GRP', em=True)
                if not cmds.objExists(poly_grp):
                    poly_grp = cmds.group(n='poly_GRP', em=True)

                for edge in edges:
                    if not any(edge in sl for sl in edgeLines):
                        cmds.select(edge)
                        cmds.polySelectConstraint(propagate=4,  m2a=angle)

                        edgeLine = [s for s in cmds.ls(sl=True, fl=True) if s in edges]

                        edgeLines.append([])
                        edgeLines[counter] = edgeLine

                        counter += 1

                for each in edgeLines:
                    r = random.uniform(0.0,1.0)
                    g = random.uniform(0.0,1.0)
                    b = random.uniform(0.0,1.0)

                    cmds.select(each, r=True)

                    crv = cmds.polyToCurve(form=2, degree=1, conformToSmoothMeshPreview=1, ch=False)[0]
                    cmds.xform(crv, cp=True)


                    crvShape = cmds.listRelatives(crv, s=True)[0]
                    spans = cmds.getAttr('%s.spans'%crvShape)

                    annotation = self.create_annotation(crv)


                    self.random_color(crvShape, r,g,b)
                    self.random_color(annotation, r,g,b)

                    cmds.parent(crv, crv_grp)

                    cmds.setAttr('%s.visibility'%geo, 0)
        finally:
            cmds.undoInfo(closeChunk=True)


    def mergeCurves(self):
        '''
        Merges selected curves.
        '''
        cmds.undoInfo(openChunk=True)

        try:
            r = random.uniform(0.0,1.0)
            g = random.uniform(0.0,1.0)
            b = random.uniform(0.0,1.0)

            sel = [s for s in cmds.ls(sl=True, l=True) if cmds.nodeType(cmds.listRelatives(s, s=True, f=True)[0]) == 'nurbsCurve']
            if len(sel) < 2:
                cmds.warning('Please select two or more curves:')
            else:
                parentGRP = sel[-1].split('|')[-2]

                newCRV = cmds.attachCurve(sel, n=sel[-1].split('|')[-1], ch=0, rpo=0, kmk=1, m=1, bb=0.5, bki=0, p=0.1)
                cmds.xform(newCRV, cp=True)
                # cmds.DeleteHistory()
                cmds.delete(sel)

                annotation = self.create_annotation(newCRV)

                self.random_color(cmds.listRelatives(newCRV, s=True)[0], r,g,b)
                self.random_color(annotation, r,g,b)

                cmds.parent(newCRV, parentGRP)
        finally:
            cmds.undoInfo(closeChunk=True)


    def normalizeCurves(self):
        '''
        Rebuild curves for even spacing between CVs
        '''
        cmds.undoInfo(openChunk=True)

        try:
            sel = [s for s in cmds.ls(sl=True, l=True) if cmds.nodeType(cmds.listRelatives(s, s=True, f=True)[0]) == 'nurbsCurve']
            if sel:
                for crv in sel:
                    crv_shape = cmds.listRelatives(crv, s=True) or []
                    if crv_shape:
                        CV_count = cmds.getAttr('{}.spans'.format(crv_shape[0]))
                        cmds.rebuildCurve(crv, ch=0, rpo=1, rt=0, end=1, kr=2, kcp=0, kep=1, kt=0, s=CV_count, d=1, tol=0.01)

                        annotation = [s for s in cmds.listRelatives(crv, ad=True) if cmds.nodeType(s) == 'annotationShape'][0]

                        cmds.setAttr('%s.text'%annotation, str(CV_count), type="string")
                cmds.select(sel)
        finally:
            cmds.undoInfo(closeChunk=True)


    def rebuildCurve(self):
        '''
        Rebuild selected curves based on determined CV count.
        '''
        cmds.undoInfo(openChunk=True)
        try:
            CV_count = self.rebuild_curve_field.text()
            if not CV_count:
                cmds.warning('Please define a cv count.')
            else:
                CV_count = int(CV_count)
                sel = [s for s in cmds.ls(sl=True, l=True) if cmds.nodeType(cmds.listRelatives(s, s=True, f=True)[0]) == 'nurbsCurve']
                for s in sel:
                    cmds.rebuildCurve(s, ch=0, rpo=1, rt=0, end=1, kr=2, kcp=0, kep=1, kt=0, s=CV_count, d=1, tol=0.01)

                    annotation = [s for s in cmds.listRelatives(s, ad=True) if cmds.nodeType(s) == 'annotationShape'][0]

                    cmds.setAttr('%s.text'%annotation, str(CV_count), type="string")
        finally:
            cmds.undoInfo(closeChunk=True)

    def splitCurve(self):
        '''
        Split curve at specified index
        '''
        def split(targetSpan, crvs, reverse):
            if not targetSpan:
                cmds.warning('Please define a cv index to split curve at or select one cv.')
            else:
                if '.cv' in crvs[0]:
                    grp = crvs[0].split('|')[1]
                else:
                    grp = cmds.listRelatives(crvs[0], p=True)
                for crv in crvs:
                    if '.cv' in crvs[0]:
                        crv = cmds.listRelatives(crvs[0].split('.cv')[0], p=True)[0]

                    annotation = [s for s in cmds.listRelatives(crv, ad=True) if cmds.nodeType(s) == 'annotationShape'][0]
                    annotationTransform = cmds.listRelatives(annotation, p=True)[0]
                    cmds.delete(annotation)
                    cmds.delete(annotationTransform)

                    cmds.rebuildCurve(crv, ch=1, rpo=1, rt=0, end=1, kr=2, kcp=1, kep=1, kt=0, s=4, d=1, tol=0.01)

                    crvShape = cmds.listRelatives(crv, s=True)[0]
                    spans = cmds.getAttr('%s.spans'%crvShape)

                    if targetSpan:
                        targetSpan = int(targetSpan)
                        reverseTargetSpan = spans - targetSpan

                    if reverse:
                        detach = cmds.ls(cmds.detachCurve('%s.u[%s]'%(crv, reverseTargetSpan), ch=False, cos=True, rpo=1), l=True)
                    else:
                        detach = cmds.ls(cmds.detachCurve('%s.u[%s]'%(crv, targetSpan), ch=False, cos=True, rpo=1), l=True)


                    if not cmds.listRelatives(detach[0], s=True):
                        detach[0] = cmds.listRelatives(detach[0], p=True, f=True)[0]
                    if not cmds.listRelatives(detach[1], s=True):
                        detach[1] = cmds.listRelatives(detach[1], p=True, f=True)[0]



                    if len(detach[0].split('|')) == 2:
                        newCurveA = cmds.ls(cmds.parent(detach[0], grp),l=True)
                    else:
                        newCurveA = cmds.ls(detach[0],l=True)

                    if len(detach[1].split('|')) == 2:
                        newCurveB = cmds.ls(cmds.parent(detach[1], grp),l=True)
                    else:
                        newCurveB = cmds.ls(detach[1],l=True)


                    cmds.xform(newCurveA, cp=True)
                    cmds.xform(newCurveB, cp=True)

                    cmds.select(newCurveA)
                    annotationA = self.create_annotation(newCurveA)
                    cmds.select(newCurveB)
                    annotationB = self.create_annotation(newCurveB)

                    r = random.uniform(0.0,1.0)
                    g = random.uniform(0.0,1.0)
                    b = random.uniform(0.0,1.0)

                    self.random_color(cmds.listRelatives(newCurveA, s=True)[0], r,g,b)
                    self.random_color(annotationA, r,g,b)

                    r = random.uniform(0.0,1.0)
                    g = random.uniform(0.0,1.0)
                    b = random.uniform(0.0,1.0)

                    self.random_color(cmds.listRelatives(newCurveB, s=True)[0], r,g,b)
                    self.random_color(annotationB, r,g,b)


                    cmds.rebuildCurve(newCurveA, ch=1, rpo=1, rt=0, end=1, kr=2, kcp=1, kep=1, kt=0, s=4, d=1, tol=0.01)
                    cmds.rebuildCurve(newCurveB, ch=1, rpo=1, rt=0, end=1, kr=2, kcp=1, kep=1, kt=0, s=4, d=1, tol=0.01)

        #Execution Code
        cmds.undoInfo(openChunk=True)
        try:
            selected_cv = []
            crvs = cmds.ls(sl=True, l=True, fl=True)
            targetSpan = self.split_curve_field.text() or []
            reverseCheck = self.split_curve_inverse_order_box.isChecked()

            if crvs:
                if any([crv for crv in crvs if '.cv' in crv]):
                    if len(crvs) != 1:
                        cmds.warning('Please only select one CV to split.')
                        targetSpan = []
                    else:
                        targetSpan = crvs[0].split('.cv')[-1][1:-1]
                        reverseCheck = False

                split(targetSpan, crvs, reverseCheck)
        finally:
            cmds.undoInfo(closeChunk=True)

    def createCurveFromIso(self):
        '''
        Create curve from selected Isoparm.
        '''

        cmds.undoInfo(openChunk=True)
        try:
            sel = cmds.ls(sl=True, l=True)

            if sel:
                grp = cmds.listRelatives(sel[0], p=True, f=True)[0].split('|')[1]
                crv_grp = grp.replace('nurbs', 'crv')

                for s in sel:
                    if cmds.nodeType(s) == 'nurbsSurface':
                        r = random.uniform(0.0,1.0)
                        g = random.uniform(0.0,1.0)
                        b = random.uniform(0.0,1.0)

                        nurb = s.split('[')[0]
                        number = int(round(float(s.split('[')[-1][:-1])))

                        iso = '%s[%s]'%(nurb, number)

                        curve = cmds.duplicateCurve(iso, ch=0, rn=0, local=0)[0]
                        cmds.xform(curve, cp=True)

                        annotation = self.create_annotation(curve)

                        self.random_color(cmds.listRelatives(curve, s=True)[0], r,g,b)
                        self.random_color(annotation, r,g,b)
                        cmds.parent(curve, crv_grp)
        finally:
            cmds.undoInfo(closeChunk=True)


    def createCurveFromEdges(self):
        '''
        Create curve from selected polygon Edges.
        '''
        cmds.undoInfo(openChunk=True)
        try:
            sel = cmds.ls(sl=True, l=True)
            if sel:
                if cmds.nodeType(sel[0]) == 'mesh':
                    grp = 'crv_GRP'
                    r = random.uniform(0.0,1.0)
                    g = random.uniform(0.0,1.0)
                    b = random.uniform(0.0,1.0)



                    curve = cmds.polyToCurve(form=2, degree=1, conformToSmoothMeshPreview=1, ch=False)[0]
                    cmds.xform(curve, cp=True)

                    annotation = self.create_annotation(curve)

                    self.random_color(cmds.listRelatives(curve, s=True)[0], r,g,b)
                    self.random_color(annotation, r,g,b)
                    cmds.parent(curve, grp)
        finally:
            cmds.undoInfo(closeChunk=True)


    def createSurface3(self):
        '''
        Create Nurbs Surface based on 3 selected curves.
        '''
        cmds.undoInfo(openChunk=True)
        try:
            sel = [s for s in cmds.ls(sl=True, l=True) if cmds.nodeType(cmds.listRelatives(s, s=True, f=True)[0]) == 'nurbsCurve']
            if sel and len(sel) == 3:
                    grp = cmds.listRelatives(sel[0], p=True, f=True)[0]
                    nurbs_grp = grp.replace('crv', 'nurbs')
                    surface = cmds.singleProfileBirailSurface(sel, ch=0, po=0, tm=1, tp1=0)
                    cmds.rebuildSurface(surface, ch=0, rpo=1, rt=0, end=1, kr=2, kcp=1, kc=0, su=4, du=1, sv=4, dv=1, tol=0.01, fr=0, dir=2)
                    cmds.parent(surface, nurbs_grp)
        finally:
            cmds.undoInfo(closeChunk=True)

    def createSurface4(self):
        '''
        Create Nurbs Surface based on 3 selected curves.
        '''
        cmds.undoInfo(openChunk=True)
        try:
            sel = [s for s in cmds.ls(sl=True, l=True) if cmds.nodeType(cmds.listRelatives(s, s=True)[0]) == 'nurbsCurve']
            if sel and len(sel) == 4:
                grp = cmds.listRelatives(sel[0], p=True, f=True)[0]
                nurbs_grp = grp.replace('crv', 'nurbs')
                surface = cmds.boundary(sel, ch=0, order=0, ep=0, rn=0, po=0, ept=0.01)
                cmds.rebuildSurface(surface, ch=0, rpo=1, rt=0, end=1, kr=2, kcp=1, kc=0, su=4, du=1, sv=4, dv=1, tol=0.01, fr=0, dir=2)
                cmds.parent(surface, nurbs_grp)
        finally:
            cmds.undoInfo(closeChunk=True)


    def reverseSurfaceDirection(self):
        '''
        Reverse Nurbs Surface Normal
        '''
        cmds.undoInfo(openChunk=True)
        try:
            sel = [s for s in cmds.ls(sl=True, l=True) if cmds.nodeType(cmds.listRelatives(s, s=True)[0]) == 'nurbsSurface']

            for s in sel:
                try:
                    cmds.reverseSurface(s, d=0, ch=0, rpo=1)
                    cmds.select(sel)
                except:
                    pass
        finally:
            cmds.undoInfo(closeChunk=True)


    def splitSurfaceU(self):
        '''
        Split Nurbs surface at specified U index.
        '''
        def splitU(index, parameter, sel, reverse):
            if not index and sel:
                cmds.warning('Please define a "U" isoparm index or select one isoparm.')
            else:
                if sel:
                    if '.v' in sel[0] or '.u' in sel[0]:
                        grp = sel[0].split('|')[1]
                    else:
                        grp = cmds.listRelatives(sel[0], p=True, f=True)
                    for s in sel:
                        if '.v' in s or '.u' in s:
                            shape = cmds.listRelatives(sel[0].split('.')[0], s=True, f=True)[0]
                        else:
                            shape = cmds.listRelatives(s, s=True, f=True)[0]

                        if cmds.nodeType(shape) == 'nurbsSurface':
                            uSpans = cmds.getAttr('%s.maxValue%s'%(shape, parameter.upper()))

                            reverseIndex = uSpans - float(index)

                            if index > 0 or '.v' in sel[0] or '.u' in sel[0]:
                                if reverse:
                                    detach = cmds.ls(cmds.detachSurface('%s.%s[%s]'%(shape, parameter, reverseIndex), ch=0, rpo=1), l=True)
                                else:
                                    detach = cmds.ls(cmds.detachSurface('%s.%s[%s]'%(shape, parameter, index), ch=0, rpo=1), l=True)

                                if not cmds.listRelatives(detach[0], s=True):
                                    detach[0] = cmds.listRelatives(detach[0], p=True, f=True)[0]
                                if not cmds.listRelatives(detach[1], s=True):
                                    detach[1] = cmds.listRelatives(detach[1], p=True, f=True)[0]

                                if len(detach[0].split('|')) == 2:
                                    newSurfaceA = cmds.ls(cmds.parent(detach[0], grp),l=True)
                                else:
                                    newSurfaceA = cmds.ls(detach[0],l=True)

                                if len(detach[1].split('|')) == 2:
                                    newSurfaceB = cmds.ls(cmds.parent(detach[1], grp),l=True)
                                else:
                                    newSurfaceB = cmds.ls(detach[1],l=True)



                                cmds.rebuildSurface(newSurfaceA, ch=0, rpo=1, rt=0, end=1, kr=2, kcp=1, kc=0, su=4, du=1, sv=4, dv=1, tol=0.01, fr=0, dir=2)
                                cmds.rebuildSurface(newSurfaceB, ch=0, rpo=1, rt=0, end=1, kr=2, kcp=1, kc=0, su=4, du=1, sv=4, dv=1, tol=0.01, fr=0, dir=2)

        #Execution code
        cmds.undoInfo(openChunk=True)
        try:
            sel = cmds.ls(sl=True, l=True, fl=True)
            parameter = 'u'
            index = self.split_surface_u_field.text()
            reverseCheck = self.split_surface_inverse_order_box.isChecked()

            if sel:
                if any([s for s in sel if '.u' in sel or '.v']):
                    if len(sel) != 1:
                        cmds.warning('Please only select one isoparm to split.')
                        index = []
                    else:
                        if '.v' in sel[0] or '.u' in sel[0]:
                            parameter = sel[0].split('[')[0][-1]
                            index = sel[0].split('.{}'.format(parameter))[-1][1:-1]
                            if '.' in index:
                                index = str(round(float(index)))

                            reverseCheck = False

                splitU(index, parameter, sel, reverseCheck)
        finally:
            cmds.undoInfo(closeChunk=True)

    def splitSurfaceV(self):
        '''
        Split Nurbs surface at specified V index.
        '''
        def splitV(index, parameter, sel, reverse):
            if not index and sel:
                cmds.warning('Please define a "V" isoparm index or select one isoparm.')
            else:
                if sel:
                    if '.v' in sel[0] or '.u' in sel[0]:
                        grp = sel[0].split('|')[1]
                    else:
                        grp = cmds.listRelatives(sel[0], p=True, f=True)
                    for s in sel:
                        if '.v' in s or '.u' in s:
                            shape = cmds.listRelatives(s.split('.')[0], s=True, f=True)[0]
                        else:
                            shape = cmds.listRelatives(s, s=True, f=True)[0]

                        if cmds.nodeType(shape) == 'nurbsSurface':
                            uSpans = cmds.getAttr('%s.maxValue%s'%(shape, parameter.upper()))

                            reverseIndex = uSpans - float(index)

                            if index > 0 or '.v' in sel[0] or '.u' in sel[0]:
                                if reverse:
                                    detach = cmds.ls(cmds.detachSurface('%s.%s[%s]'%(shape, parameter, reverseIndex), ch=0, rpo=1), l=True)
                                else:
                                    detach = cmds.ls(cmds.detachSurface('%s.%s[%s]'%(shape, parameter, index), ch=0, rpo=1), l=True)

                                if not cmds.listRelatives(detach[0], s=True):
                                    detach[0] = cmds.listRelatives(detach[0], p=True, f=True)[0]
                                if not cmds.listRelatives(detach[1], s=True):
                                    detach[1] = cmds.listRelatives(detach[1], p=True, f=True)[0]

                                if len(detach[0].split('|')) == 2:
                                    newSurfaceA = cmds.ls(cmds.parent(detach[0], grp),l=True)
                                else:
                                    newSurfaceA = cmds.ls(detach[0],l=True)

                                if len(detach[1].split('|')) == 2:
                                    newSurfaceB = cmds.ls(cmds.parent(detach[1], grp),l=True)
                                else:
                                    newSurfaceB = cmds.ls(detach[1],l=True)



                                cmds.rebuildSurface(newSurfaceA, ch=0, rpo=1, rt=0, end=1, kr=2, kcp=1, kc=0, su=4, du=1, sv=4, dv=1, tol=0.01, fr=0, dir=2)
                                cmds.rebuildSurface(newSurfaceB, ch=0, rpo=1, rt=0, end=1, kr=2, kcp=1, kc=0, su=4, du=1, sv=4, dv=1, tol=0.01, fr=0, dir=2)

        #Execution code
        cmds.undoInfo(openChunk=True)
        try:
            sel = cmds.ls(sl=True, l=True, fl=True)
            parameter = 'v'
            index = self.split_surface_v_field.text()
            reverseCheck = self.split_surface_inverse_order_box.isChecked()

            if sel:
                if any([s for s in sel if '.u' in sel or '.v']):
                    if len(sel) != 1:
                        cmds.warning('Please only select one isoparm to split.')
                        index = []
                    else:
                        if '.v' in sel[0] or '.u' in sel[0]:
                            parameter = sel[0].split('[')[0][-1]
                            index = sel[0].split('.{}'.format(parameter))[-1][1:-1]
                            if '.' in index:
                                index = str(round(float(index)))

                            reverseCheck = False

                splitV(index, parameter, sel, reverseCheck)
        finally:
            cmds.undoInfo(closeChunk=True)

    def convertToPoly(self):
        '''
        Converts Nurbs surfaces to plygons and merges close vertices if more than 1 surface is converted.
        '''
        cmds.undoInfo(openChunk=True)
        try:
            sel = cmds.ls(sl=True, l=True)

            polys = []

            for s in sel:
                if cmds.nodeType(cmds.listRelatives(s,s=True,f=True)[0]) == 'nurbsSurface':
                    poly = cmds.nurbsToPoly(s, mnd=1, ch=0, f=3, pt=1, pc=200, chr=0.1, ft=0.01, mel=0.001, d=0.1, ut=1, un=3, vt=1, vn=3, uch=0, ucr=0, cht=0.2, es=0, ntr=0, mrt=0, uss=1)[0]
                    polys.append(poly)
                    cmds.setAttr('{}.v'.format(s), 0)

            if not polys:
                cmds.warning('No nurbs surface selected.')
            else:
                if len(polys) > 1:
                    mesh = cmds.polyUnite(polys, ch=0, mergeUVSets=1, centerPivot=True)[0]
                else:
                    mesh = polys[0]
                cmds.polyMergeVertex(mesh, d=0.001, am=1, ch=0)
                cmds.select(mesh, r=True)

                if not cmds.objExists('poly_GRP'):
                    cmds.group(n='poly_GRP', w=True, em=True)
                cmds.parent(mesh, 'poly_GRP')
        finally:
            cmds.undoInfo(closeChunk=True)


    def mergePolyMeshes(self):
        '''
        Merge selected poly meshes and sew close vertices.
        '''
        cmds.undoInfo(openChunk=True)
        try:
            sel = [s for s in cmds.ls(sl=True, l=True) if cmds.nodeType(cmds.listRelatives(s, s=True, f=True)[0]) == 'mesh']

            if not sel:
                cmds.warning('Select 2 or more poly surfaces.')
            else:
                if len(sel) >= 2:
                    if not cmds.objExists('poly_GRP'):
                        cmds.group(n='poly_GRP', w=True, em=True)
                    dupes = cmds.duplicate(sel)
                    mesh = cmds.polyUnite(sel, ch=0, mergeUVSets=1, centerPivot=True)[0]
                    cmds.polyMergeVertex(mesh, d=0.001, am=1, ch=0)
                    cmds.select(mesh, r=True)
                    cmds.parent(mesh, 'poly_GRP')
                    cmds.delete(dupes)
                else:
                    cmds.warning('Select 2 or more poly surfaces.')
        finally:
            cmds.undoInfo(closeChunk=True)


    def mergeVertices(self):
        '''
        Merge Vertices of selected geometry based on threshold.
        '''
        cmds.undoInfo(openChunk=True)
        try:
            threshold = self.threshold_field.text()
            if not threshold:
                cmds.warning('Please define merge distance threshold.')
            else:
                sel = [s for s in cmds.ls(sl=True, l=True) if cmds.nodeType(cmds.listRelatives(s, s=True, ni=True)) == 'mesh']
                if sel:
                    threshold = self.threshold_field.text()

                    cmds.polyMergeVertex(sel, d=threshold, am=1, ch=0)
        finally:
            cmds.undoInfo(closeChunk=True)


    def transferUvs(self):
        '''
        Relax all interior vertices of selected meshes and loop based on the mount of loops defined.
        '''
        cmds.undoInfo(openChunk=True)
        try:
            sel = [s for s in cmds.ls(sl=True, l=True) if cmds.nodeType(cmds.listRelatives(s, s=True)) == 'mesh']
            if len(sel) != 2:
                cmds.warning('Please select a source and a target mesh.')
            else:
                cmds.select(sel[0])
                cmds.select(sel[1], add=True)
                cmds.transferAttributes(transferPositions=0,
                                            transferNormals=0,
                                            transferUVs=1,
                                            sourceUvSet="map1",
                                            targetUvSet="map1",
                                            transferColors=0,
                                            sampleSpace=4,
                                            sourceUvSpace="map1",
                                            targetUvSpace="map1",
                                            searchMethod=3,
                                            flipUVs=0,
                                            colorBorders=1)
        finally:
            cmds.undoInfo(closeChunk=True)


    def relaxVertices(self):
        '''
        Relax all interior vertices of selected meshes and loop based on the mount of loops defined.
        '''
        cmds.undoInfo(openChunk=True)
        try:
            loops = self.relax_loop_field.text()
            if not loops:
                cmds.warning('Please define Relax Loops.')
            else:
                sel = [s for s in cmds.ls(sl=True, l=True) if cmds.nodeType(cmds.listRelatives(s, s=True)) == 'mesh']
                if sel:
                    if cmds.listRelatives(sel, s=True):
                        if len(sel) != 1:
                            cmds.warning('Select vertices or single mesh.')
                        else:
                            verts = '%s.vtx[:]'%sel[0]
                            cmds.select(verts)
                            cmds.ShrinkPolygonSelectionRegion()

                    for i in range(int(loops)):
                        cmds.polyAverageVertex()
                    cmds.select(sel)
        finally:
            cmds.undoInfo(closeChunk=True)


    def transfer(self):
        '''
        Transfer new retopo flat surface to 3d mesh.
        '''
        cmds.undoInfo(openChunk=True)
        try:
            sel = [s for s in cmds.ls(sl=True, l=True) if cmds.nodeType(cmds.listRelatives(s, s=True, ni=True, f=True)[0]) == 'mesh']

            if len(sel) != 3:
                cmds.warning('Select 3d mesh, then 2d mesh, then 2d retopo mesh. Make sure 2d mesh has no overlapping UVs')
            else:
                mesh_3d = sel[0]
                mesh_2d = sel[1]
                mesh_retopo = sel[2]

                #transfer uvs
                cmds.select(mesh_2d)
                cmds.select(mesh_retopo, add=True)
                cmds.transferAttributes(transferPositions=0,
                                        transferNormals=0,
                                        transferUVs=1,sourceUvSet="map1",
                                        targetUvSet="map1",
                                        transferColors=0,
                                        sampleSpace=0,
                                        sourceUvSpace="map1",
                                        targetUvSpace="map1",
                                        searchMethod=3,
                                        flipUVs=0,
                                        colorBorders=1)
                cmds.DeleteHistory(mesh_retopo)


                cmds.select(mesh_2d)
                cmds.select(mesh_3d, add=True)
                cmds.transferAttributes(transferPositions=0,
                                        transferNormals=0,
                                        transferUVs=1,sourceUvSet="map1",
                                        targetUvSet="map1",
                                        transferColors=0,
                                        sampleSpace=4,
                                        sourceUvSpace="map1",
                                        targetUvSpace="map1",
                                        searchMethod=3,
                                        flipUVs=0,
                                        colorBorders=1)
                cmds.DeleteHistory(mesh_3d)

                #transfer position

                dupe = cmds.duplicate(mesh_retopo, n='new_wrapped_mesh')
                dupe = cmds.parent(dupe, w=True)
                cmds.setAttr('{}.v'.format(mesh_retopo), 0)

                cmds.select(mesh_3d)
                cmds.select(dupe, add=True)
                cmds.transferAttributes(transferPositions=1,
                                        transferNormals=0,
                                        transferUVs=1,sourceUvSet="map1",
                                        targetUvSet="map1",
                                        transferColors=0,
                                        sampleSpace=3,
                                        sourceUvSpace="map1",
                                        targetUvSpace="map1",
                                        searchMethod=3,
                                        flipUVs=0,
                                        colorBorders=1)
                cmds.select(dupe)
        finally:
            cmds.undoInfo(closeChunk=True)


    def collapse(self, gBox):
        """ Collapses a QGroupBox """
        # Find out if the state is on or off
        gbState = eval(gBox + '.isChecked()')
        if not gbState:
            eval (gBox + '.setFixedHeight(15)')
                    # Set window Height
            self.setFixedHeight(self.sizeHint().height())

        else:
            oSize = eval(gBox + '.sizeHint()')
            eval(gBox + '.setFixedHeight(oSize.height())')
                    # Set window Height
            self.setFixedHeight(self.sizeHint().height())

    def zipper(self):
        '''
        Zipper button mapping
        '''
        cmds.undoInfo(openChunk=True)
        try:
            checked = self.zipper_loop_box.isChecked()

            if checked:
                run = True
                while run:
                    try:
                        self.en_zipperEdge()
                    except:
                        run=False

            else:
                self.en_zipperEdge()
        finally:
            cmds.undoInfo(closeChunk=True)


    def random_color(self, item, r, g, b):
        '''
        Sets random color override for passed item.
        '''
        cmds.undoInfo(openChunk=True)
        try:
            cmds.setAttr("%s.overrideEnabled"%item,1)
            cmds.setAttr("%s.overrideRGBColors"%item,1)

            cmds.setAttr("%s.overrideColorR"%item, r)
            cmds.setAttr("%s.overrideColorG"%item, g)
            cmds.setAttr("%s.overrideColorB"%item, b)
        finally:
            cmds.undoInfo(closeChunk=True)


    def create_annotation(self, curve):
        '''
        Creates and attaches annotation of passed curve.
        '''
        cmds.undoInfo(openChunk=True)
        try:
            shape = cmds.listRelatives(curve, s=True, f=True)[0]
            curve = cmds.ls(sl=True)
            # shape = cmds.listRelatives(cmds.ls(sl=True), s=True, f=True)[0]
            spans = cmds.getAttr('%s.spans'%shape)

            annotation = cmds.annotate(curve, tx=str(spans))
            annotationTransform = cmds.listRelatives(annotation, p=True, f=True)[0]
            annotationTransform = cmds.ls(cmds.parent(annotationTransform , curve))

            center = cmds.xform(curve, q=True, piv=True)[0:3]
            cmds.xform(annotationTransform, t=(center[0]+1,center[1]+1,center[2]+1))

            return cmds.ls(annotation,l=True)[0]
        finally:
            cmds.undoInfo(closeChunk=True)


    def en_zipperEdge(self):
        '''
        Function to loop through and sew edges. Not my original code, original author Unknown.
        '''
        newEdge = []
        twoEdges = cmds.ls(sl=True,l=True,fl=True)
        #find if 2 edges are selected
        if len(twoEdges) != 2:
            cmds.error("Select TWO edges sharing ONE vertex to start zipping.")
        else:
            cmds.select(twoEdges[0],r=True)
            cmds.ConvertSelectionToVertices()
            edgeOnePoints = cmds.ls(sl=True,l=True,fl=True)
            cmds.select(twoEdges[1],r=True)
            cmds.ConvertSelectionToVertices()
            edgeTwoPoints = cmds.ls(sl=True,l=True,fl=True)
            anyAction = 0
            # goes through and merges vertices if  not on edge point
            if edgeOnePoints[0] == edgeTwoPoints[0]:
                cmds.polyMergeVertex(edgeOnePoints[1], edgeTwoPoints[1],d=10000)
                anyAction =1

            if edgeOnePoints[1] == edgeTwoPoints[1]:
                cmds.polyMergeVertex(edgeOnePoints[0], edgeTwoPoints[0],d=10000)
                anyAction =1

            if edgeOnePoints[0] == edgeTwoPoints[1]:
                cmds.polyMergeVertex(edgeOnePoints[1], edgeTwoPoints[0],d=10000)
                anyAction =1

            if edgeOnePoints[1] == edgeTwoPoints[0]:
                cmds.polyMergeVertex(edgeOnePoints[0], edgeTwoPoints[1],d=10000)
                anyAction =1

            if anyAction == 1:
                newVertex = cmds.ls(sl=True,l=True,fl=True)
                cmds.ConvertSelectionToEdges()
                newEdges = cmds.ls(sl=True,l=True,fl=True)
            cmds.select(cl=True)
            bordEdges = []
            # find if new edges have border
            for edge in newEdges:
                tempString = cmds.polyListComponentConversion(edge,fe=True,tf=True)
                nTemp = cmds.ls(tempString,fl=True,l=True)
                if len(nTemp) == 1:
                    bordEdges.append(edge)
            #check to see if done or not
            if len(bordEdges) == 2:
                cmds.select(bordEdges,r=True)
                cmds.delete(ch=True,all=True)


try:
    md_retopo.deleteLater()
except:
    pass

md_retopo = DS_MD_Retopo()

md_retopo.show()