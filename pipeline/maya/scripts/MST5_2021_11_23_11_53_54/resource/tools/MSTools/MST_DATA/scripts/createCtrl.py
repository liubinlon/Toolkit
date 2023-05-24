#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# @Time  : 2019/3/31 0031 0:50
# @File  : createCtrl.py
# @email : spirit_az@foxmail.com
__author__ = 'ChenLiang.Miao'

# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
# import --+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel


# proc function -+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
# function main -+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
def skirtBuildCtrl(surface, atr, array, endEffector=False, isSurface=True):
    """

    :param surface: build by this surface
    :param atr: U or V axis
    :param array: ctrl position by UVShell
    :return:
    """
    locMats = []
    node = pm.PyNode(surface)  # type:
    nodeName = node.name()

    locJntGrpT = pm.group(em=True, name='grp_locJnt_{0}'.format(nodeName))
    ctrlJntGrpT = pm.group(em=True, name='grp_ctrlJnt_{0}'.format(nodeName))
    cCtrlGrpT = pm.group(em=True, name='grp_ctrlC_{0}'.format(nodeName))
    aimConGrpT = pm.group(em=True, name='grp_aimCon_{0}'.format(nodeName))
    DJntGrpT = pm.group(em=True, name='grp_DJnt_{0}'.format(nodeName))
    skJntGrpT = pm.group(em=True, name='grp_skJnt_{0}'.format(nodeName))
    pm.hide(locJntGrpT, ctrlJntGrpT, aimConGrpT, DJntGrpT)
    if not isSurface:
        follicleLocGrpT = pm.group(em=True, name='grp_follicleJnt_{0}'.format(nodeName))
        pm.hide(follicleLocGrpT)

    # create loc jnt
    for (i, U) in enumerate(array):
        locGrp = pm.group(em=True, name='grp_locJnt_{0}_{1}'.format(nodeName, i))
        pm.parent(locGrp, locJntGrpT)
        if not isSurface:
            follicleGrp = pm.group(em=True, name='grp_follicleJnt_{0}_{1}'.format(nodeName, i))
            pm.parent(follicleGrp, follicleLocGrpT)
        locMat = list()
        for (k, V) in enumerate(U):
            cmds.select(clear=True)
            loc = pm.joint(rad=0.6, name='loc_{0}_{1}_{2}'.format(nodeName, i, k))

            if isSurface:
                pointOnSurfaceInfo = pm.createNode('pointOnSurfaceInfo', name='pos_{0}_{1}_{2}'.format(nodeName, i, k))
                node.worldSpace.connect(pointOnSurfaceInfo.inputSurface)
                pointOnSurfaceInfo.turnOnPercentage.set(True)
                pointOnSurfaceInfo.attr(atr[0]).set(V[0])
                pointOnSurfaceInfo.attr(atr[1]).set(V[1])
                pointOnSurfaceInfo.positionX.connect(loc.translateX)
                pointOnSurfaceInfo.positionY.connect(loc.translateY)
                pointOnSurfaceInfo.positionZ.connect(loc.translateZ)
            else:
                fTrans = pm.createNode('transform', name='pos_{0}_{1}_{2}'.format(nodeName, i, k))
                pointOnSurfaceInfo = pm.createNode('follicle', name='%sShape' % fTrans, parent=fTrans)

                pm.parent(fTrans, follicleGrp)

                pointOnSurfaceInfo.outTranslate.connect(fTrans.translate)
                pointOnSurfaceInfo.outRotate.connect(fTrans.rotate)

                pointOnSurfaceInfo.attr(atr[0]).set(V[0])
                pointOnSurfaceInfo.attr(atr[1]).set(V[1])
                pointOnSurfaceInfo.outTranslateX.connect(loc.translateX)
                pointOnSurfaceInfo.outTranslateY.connect(loc.translateY)
                pointOnSurfaceInfo.outTranslateZ.connect(loc.translateZ)

                node.outMesh.connect(pointOnSurfaceInfo.inputMesh)
                node.worldMatrix[0].connect(pointOnSurfaceInfo.inputWorldMatrix)

            pm.parent(loc, locGrp)

            locMat.append(loc)
        locMats.append(locMat)

    # create ctrlIK joint
    ctrlIKJnts = list()
    for (i, locMat) in enumerate(locMats):
        ctrlIKJnt = list()
        for (k, loc) in enumerate(locMat):
            pm.select(clear=True)
            jnt = pm.joint(radius=0.4, name='ctrlIKJnt_{0}_{1}_{2}'.format(nodeName, i, k))
            ctrlIKJnt.append(jnt)
        ctrlIKJnts.append(ctrlIKJnt)

    for (i, jntGrp) in enumerate(ctrlIKJnts):
        cJntGrp = pm.group(em=True, name='grp_ctrlIKJnt_{0}_{1}'.format(nodeName, i))
        pm.parent(cJntGrp, ctrlJntGrpT)
        for (k, jnt) in enumerate(jntGrp):
            if k == 0:
                pm.parent(jnt, cJntGrp)
            else:
                pm.parent(jnt, jntGrp[k - 1])

    # fix orient
    for each in ctrlIKJnts:
        pm.makeIdentity(each[-1], apply=True, t=1, r=1, s=1, n=0, pn=1, jointOrient=1)

    # create ctrl joint
    ctrlJnts = list()
    for (i, locMat) in enumerate(locMats):
        ctrlJnt = list()
        for (k, loc) in enumerate(locMat):
            pm.select(clear=True)
            jnt = pm.joint(radius=0.4, name='ctrlJnt_{0}_{1}_{2}'.format(nodeName, i, k))
            ctrlJnt.append(jnt)
        ctrlJnts.append(ctrlJnt)

    for (i, jntGrp) in enumerate(ctrlJnts):
        cJntGrp = 'grp_ctrlIKJnt_{0}_{1}'.format(nodeName, i)
        pm.parent(cJntGrp, ctrlJntGrpT)
        for (k, jnt) in enumerate(jntGrp):
            if k == 0:
                pm.parent(jnt, cJntGrp)
            else:
                pm.parent(jnt, jntGrp[k - 1])

    # fix orient
    for each in ctrlJnts:
        pm.makeIdentity(each[-1], apply=True, t=1, r=1, s=1, n=0, pn=1, jointOrient=1)

    # create ctrl
    ctrlCs = list()
    for (i, locMat) in enumerate(locMats):
        ctrlC = list()
        length = len(locMat) - 1
        if endEffector:
            length += 1
        for (k, loc) in enumerate(locMat):
            ctrlG = pm.group(em=True, name='grpCtrl_{0}_{1}_{2}'.format(nodeName, i, k))
            if length > k:
                ctrl, _ = pm.circle(name='ctrl_{0}_{1}_{2}'.format(nodeName, i, k))
                pm.parent(ctrl, ctrlG)
            else:
                ctrl = ''
            ctrlC.append((ctrlG, ctrl))
        ctrlCs.append(ctrlC)

    for (i, ctrlGrp) in enumerate(ctrlCs):
        cCtrlGrp = pm.group(em=True, name='grp_ctrlC_{0}_{1}'.format(nodeName, i))
        pm.parent(cCtrlGrp, cCtrlGrpT)
        for (k, ctrl) in enumerate(ctrlGrp):
            if k == 0:
                pm.parent(ctrl[0], cCtrlGrp)
            else:
                pm.parent(ctrl[0], ctrlGrp[k - 1][1])

    for (i, ctrlGrp) in enumerate(ctrlCs):
        for (k, (ctrlG, ctrl)) in enumerate(ctrlGrp):

            IKJnt = ctrlIKJnts[i][k]
            decomposeMatrix = pm.createNode('decomposeMatrix', name='cCDMatrix_{0}_{1}'.format(i, k))
            IKJnt.matrix.connect(decomposeMatrix.inputMatrix)
            decomposeMatrix.outputTranslateX.connect(ctrlG.translateX)
            decomposeMatrix.outputTranslateY.connect(ctrlG.translateY)
            decomposeMatrix.outputTranslateZ.connect(ctrlG.translateZ)
            if endEffector and k == len(ctrlGrp) - 1:
                continue
            decomposeMatrix.outputRotateX.connect(ctrlG.rotateX)
            decomposeMatrix.outputRotateY.connect(ctrlG.rotateY)
            decomposeMatrix.outputRotateZ.connect(ctrlG.rotateZ)
            decomposeMatrix.outputScaleX.connect(ctrlG.scaleX)
            decomposeMatrix.outputScaleY.connect(ctrlG.scaleY)
            decomposeMatrix.outputScaleZ.connect(ctrlG.scaleZ)

    # ctrl ctrl jnt
    for (i, jntGrp) in enumerate(ctrlJnts):
        for (k, jnt) in enumerate(jntGrp):
            ctrlG, ctrl = ctrlCs[i][k]
            multMatrix = pm.createNode('multMatrix', name='cToJMatrix_{0}_{1}'.format(i, k))
            decomposeMatrix = pm.createNode('decomposeMatrix', name='cToJDMatrix_{0}_{1}'.format(i, k))

            ctrl and ctrl.matrix.connect(multMatrix.matrixIn[0])
            ctrlG.matrix.connect(multMatrix.matrixIn[1])

            multMatrix.matrixSum.connect(decomposeMatrix.inputMatrix)

            decomposeMatrix.outputTranslateX.connect(jnt.translateX)
            decomposeMatrix.outputTranslateY.connect(jnt.translateY)
            decomposeMatrix.outputTranslateZ.connect(jnt.translateZ)
            decomposeMatrix.outputRotateX.connect(jnt.rotateX)
            decomposeMatrix.outputRotateY.connect(jnt.rotateY)
            decomposeMatrix.outputRotateZ.connect(jnt.rotateZ)
            decomposeMatrix.outputScaleX.connect(jnt.scaleX)
            decomposeMatrix.outputScaleY.connect(jnt.scaleY)
            decomposeMatrix.outputScaleZ.connect(jnt.scaleZ)

    # create aimConstraint
    for (i, locMat) in enumerate(locMats):
        aimGrp = pm.group(em=True, name='grp_aim_{0}_{1}'.format(nodeName, i))
        pm.parent(aimGrp, aimConGrpT)
        length = len(locMat) - 1
        for (k, loc) in enumerate(locMat):
            pointOnSurfaceInfo = loc.translateX.inputs()[0]

            aimC = pm.createNode('aimConstraint', name='aim_{0}_{1}_{2}'.format(nodeName, i, k))
            aimC.worldUpType.set(3)
            aimC.aimVector.set(1, 0, 0)
            aimC.upVector.set(0, 1, 0)

            mel.eval('connectAttr -f {0}.inverseMatrix {1}.target[0].targetParentMatrix'.format(loc, aimC))
            loc.translateX.connect(aimC.translateX)
            loc.translateY.connect(aimC.translateY)
            loc.translateZ.connect(aimC.translateZ)
            if isSurface:
                pointOnSurfaceInfo.normalizedNormalX.connect(aimC.worldUpVectorX)
                pointOnSurfaceInfo.normalizedNormalY.connect(aimC.worldUpVectorY)
                pointOnSurfaceInfo.normalizedNormalZ.connect(aimC.worldUpVectorZ)
            else:
                pointOnSurfaceInfo.outNormalX.connect(aimC.worldUpVectorX)
                pointOnSurfaceInfo.outNormalY.connect(aimC.worldUpVectorY)
                pointOnSurfaceInfo.outNormalZ.connect(aimC.worldUpVectorZ)

            if k < length:
                locNext = locMat[k + 1]
                mel.eval('connectAttr -f {0}.translateX {1}.target[0].targetTranslateX'.format(locNext, aimC))
                mel.eval('connectAttr -f {0}.translateY {1}.target[0].targetTranslateY'.format(locNext, aimC))
                mel.eval('connectAttr -f {0}.translateZ {1}.target[0].targetTranslateZ'.format(locNext, aimC))
            else:
                if isSurface:

                    mel.eval(
                        'connectAttr -f {0}.tangentUx {1}.target[0].targetTranslateX'.format(pointOnSurfaceInfo, aimC))
                    mel.eval(
                        'connectAttr -f {0}.tangentUy {1}.target[0].targetTranslateY'.format(pointOnSurfaceInfo, aimC))
                    mel.eval(
                        'connectAttr -f {0}.tangentUz {1}.target[0].targetTranslateZ'.format(pointOnSurfaceInfo, aimC))
                else:
                    mel.eval('connectAttr -f {0}.outTangentX {1}.target[0].targetTranslateX'.format(pointOnSurfaceInfo,
                                                                                                    aimC))
                    mel.eval('connectAttr -f {0}.outTangentY {1}.target[0].targetTranslateY'.format(pointOnSurfaceInfo,
                                                                                                    aimC))
                    mel.eval('connectAttr -f {0}.outTangentZ {1}.target[0].targetTranslateZ'.format(pointOnSurfaceInfo,
                                                                                                    aimC))

            aimC.constraintRotateX.connect(aimC.rotateX)
            aimC.constraintRotateY.connect(aimC.rotateY)
            aimC.constraintRotateZ.connect(aimC.rotateZ)

            pm.parent(aimC, aimGrp)
            # pm.delete(tempLoc, tempLoc1)

    # aim to ctrl jnt
    for (i, jntGrp) in enumerate(ctrlIKJnts):
        for (k, jnt) in enumerate(jntGrp):
            multMatrix = pm.createNode('multMatrix', name='cMatrix_{0}_{1}'.format(i, k))
            decomposeMatrix = pm.createNode('decomposeMatrix', name='cDMatrix_{0}_{1}'.format(i, k))
            aimConstraint = pm.PyNode('aim_{0}_{1}_{2}'.format(nodeName, i, k))

            aimConstraint.matrix.connect(multMatrix.matrixIn[0])
            multMatrix.matrixSum.connect(decomposeMatrix.inputMatrix)

            if k > 0:
                aimConstraintNext = pm.PyNode('aim_{0}_{1}_{2}'.format(nodeName, i, k - 1))
                aimConstraintNext.inverseMatrix.connect(multMatrix.matrixIn[1])

            decomposeMatrix.outputTranslateX.connect(jnt.translateX)
            decomposeMatrix.outputTranslateY.connect(jnt.translateY)
            decomposeMatrix.outputTranslateZ.connect(jnt.translateZ)
            decomposeMatrix.outputRotateX.connect(jnt.rotateX)
            decomposeMatrix.outputRotateY.connect(jnt.rotateY)
            decomposeMatrix.outputRotateZ.connect(jnt.rotateZ)
            decomposeMatrix.outputScaleX.connect(jnt.scaleX)
            decomposeMatrix.outputScaleY.connect(jnt.scaleY)
            decomposeMatrix.outputScaleZ.connect(jnt.scaleZ)

    # create drive skin jnt
    ctrlDJnts = list()
    for (i, locMat) in enumerate(locMats):
        ctrlDJnt = list()
        for (k, loc) in enumerate(locMat):
            pm.select(clear=True)
            jnt = pm.joint(radius=0.4, name='ctrlDJnt_{0}_{1}_{2}'.format(nodeName, i, k))
            ctrlDJnt.append(jnt)
        ctrlDJnts.append(ctrlDJnt)

    for (i, jntGrp) in enumerate(ctrlDJnts):
        dJntGrp = pm.group(em=True, name='grp_DJnt_{0}_{1}'.format(nodeName, i))
        pm.parent(dJntGrp, DJntGrpT)
        for (k, jnt) in enumerate(jntGrp):
            if k == 0:
                pm.parent(jnt, dJntGrp)
            else:
                pm.parent(jnt, jntGrp[k - 1])

    for (i, jntGrp) in enumerate(ctrlDJnts):
        for (k, jnt) in enumerate(jntGrp):
            ctrlJnt = ctrlJnts[i][k]
            ctrlJnt.translateX.connect(jnt.translateX)
            ctrlJnt.translateY.connect(jnt.translateY)
            ctrlJnt.translateZ.connect(jnt.translateZ)
            ctrlJnt.rotateX.connect(jnt.rotateX)
            ctrlJnt.rotateY.connect(jnt.rotateY)
            ctrlJnt.rotateZ.connect(jnt.rotateZ)
            ctrlJnt.scaleX.connect(jnt.scaleX)
            ctrlJnt.scaleY.connect(jnt.scaleY)
            ctrlJnt.scaleZ.connect(jnt.scaleZ)

    # create skin skin jnt
    skJnts = list()
    for (i, locMat) in enumerate(locMats):
        skJnt = list()
        for (k, loc) in enumerate(locMat):
            pm.select(clear=True)
            jnt = pm.joint(radius=0.4, name='skJnt_{0}_{1}_{2}'.format(nodeName, i, k))
            skJnt.append(jnt)
        skJnts.append(skJnt)

    for (i, jntGrp) in enumerate(skJnts):
        skJntGrp = pm.group(em=True, name='grp_skJnt_{0}_{1}'.format(nodeName, i))
        pm.parent(skJntGrp, skJntGrpT)
        for (k, jnt) in enumerate(jntGrp):
            if k == 0:
                pm.parent(jnt, skJntGrp)
            else:
                pm.parent(jnt, jntGrp[k - 1])

    for (i, jntGrp) in enumerate(skJnts):
        for (k, jnt) in enumerate(jntGrp):
            dJnt = ctrlDJnts[i][k]
            pm.delete(pm.parentConstraint(dJnt, jnt, mo=False, weight=1))

    for each in skJnts:
        pm.makeIdentity(each[-1], apply=True, t=1, r=1, s=1, n=0, pn=1, jointOrient=1)
        # pm.joint(each[0], e=True, oj='xyz', secondaryAxisOrient='xup', zso=1)
        # pm.makeIdentity(each[-1], apply=True, t=1, r=1, s=1, n=0, pn=1, jointOrient=1)

    for (i, jntGrp) in enumerate(skJnts):
        for (k, jnt) in enumerate(jntGrp):
            dJnt = ctrlDJnts[i][k]
            pm.parentConstraint(dJnt, jnt, mo=True, weight=1)
