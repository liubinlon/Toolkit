import re
import os

def is_surface(crv, loc_str):
    """Get selection curve translate number, duplicate curve and create surface"""
    if cmds.getAttr(crv + ".tx"):
        x_num = cmds.getAttr(crv + ".tx")
    elif cmds.getAttr(crv + ".ty"):
        y_num = cmds.getAttr(crv + ".ty")
    else:
        z_num = cmds.getAttr(crv + ".tz")
    new_crv = cmds.duplicate(crv, name = i + "_end")
    if x_num:
        cmds.setAttr(new_crv + ".tx", x_num)
    elif y_num:
        cmds.setAttr(new_crv + ".ty", y_num)
    else:
        cmds.setAttr(new_crv + ".tz", z_num)
    cmds.loft(crv, new_crv, u = False, c = False, ar = True, d = 1, ss = 1, rn = False, po = 0, rsn = True, name = crv + loc_str)
    

def get_crv_point(crv):
    """Get surface points and return"""
    name_data = str(crv)   
#    if re.findall(r"\d+\.?\d*", name_data):
#        str_data = "".join(re.split(r"[^A-Za-z]", name_data))
#        print str_data
#        num_data = "".join(re.findall(r"\d+\.?\d*", name_data))
#        print num_data
#    else:
        
    new_data = name_data + "Shape"
    point_num = len(cmds.getAttr("%s.cv[*][0]" % new_data))      
    return point_num, new_data 

def create_skin_bone(crv, main_crv, u = True):
    """Get curve point, create skin joint"""
    # name_data = str(crv)    
    # if re.findall(r"\d+\.?\d*", name_data):
    #     str_data = "".join(re.split(r"[^A-Za-z]", name_data))
    #     num_data = re.findall(r"\d+\.?\d*", name_data)
    #     new_data = str_data + "Shape" + num_data
    # point_num = len(cmds.getAttr("%s.cv[*][0]" % new_data))
    point_num = get_crv_point(crv)
    isom_node = cmds.createNode("curveFromSurfaceIso", name = crv + "_isom")
    cmds.setAttr(isom_node + ".isoparmValue")
    cmds.setAttr(isom_node + ".relativeValue", 1)
    info_node = cmds.createNode("curveInfo", name = crv + "_info")
    double_node = cmds.createNode("addDoubleLinear", name = crv + "_addDouble")
    multiA_node = cmds.createNode("multiplyDivide", name = crv + "A_multi")
    cmds.setAttr(multiA_node + ".operation", 2)
    multiB_node = cmds.createNode("multiplyDivide", name = crv + "B_multi")
    cmds.setAttr(multiB_node + ".operation", 2)
    cmds.connectAttr(main_crv + ".sx", multiB_node + ".input1X")
    cmds.connectAttr(point_num[1] + ".worldSpace[0]", isom_node + ".inputSurface")
    cmds.connectAttr(isom_node + ".outputCurve", info_node + ".inputCurve")
    cmds.connectAttr(info_node + ".arcLength", multiA_node + ".input1X")
    get_data = cmds.getAttr(multiA_node + ".input1X")
    cmds.setAttr(multiA_node + ".input2X", get_data)
    cmds.connectAttr(multiA_node + ".outputX", multiB_node + ".input2X")
    cmds.connectAttr(multiB_node + ".outputX", double_node + ".input1")
    cmds.setAttr(double_node + ".input2", -1)
    skin_bone_grp = cmds.group(em = True, name = "skin_bone_all_grp")
    new_num = 1.0/(point_num[0] -1)
    for p in range(0, point_num[0]):        
        skin_bone = cmds.joint(name = "%s%s" % (crv, p))
        buf_grp = cmds.group(skin_bone, name = crv + "_buf%s" % p)
        rig_grp = cmds.group(buf_grp, name = crv + "_rig%s" % p, p = skin_bone_grp)
        cmds.addAttr(rig_grp, ln = "parameter", at = "double", dv = 0, max = 1, min = 0)
        cmds.setAttr(rig_grp + ".parameter", keyable = True)
        cmds.setAttr(rig_grp + ".parameter", p * new_num)
        cmds.addAttr(rig_grp, ln = "squash", at = "double", dv = 0)
        cmds.setAttr(rig_grp + ".squash", keyable = True)
        cmds.setAttr(rig_grp + ".squash", 0.1)        
        info_node = cmds.createNode("pointOnSurfaceInfo", name = "%s%s_Info" % (crv, p))
        cmds.connectAttr(point_num[1] + ".worldSpace[0]", info_node + ".inputSurface")
        aim_node = cmds.createNode("aimConstraint", name = crv + "%s_aim" % p)
        multd_node = cmds.createNode("multDoubleLinear", name = crv + "%s_multD" % p)
        addd_node = cmds.shadingNode("addDoubleLinear", asUtility = True, name = crv + "%s_addD" % p)
        cmds.setAttr(addd_node + ".input2", 1)
        cmds.connectAttr(info_node + ".normal", aim_node + ".target[0].targetTranslate")
        cmds.connectAttr(info_node + ".tangentV", aim_node + ".worldUpVector")
        cmds.connectAttr(aim_node + ".constraintRotate", rig_grp + ".rotate")
        cmds.connectAttr(info_node + ".position", rig_grp + ".translate")
        cmds.connectAttr(double_node + ".output", multd_node + ".input1")
        cmds.connectAttr(multd_node + ".output", addd_node + ".input1")
        cmds.connectAttr(addd_node + ".output", rig_grp + ".scaleX")
        cmds.connectAttr(addd_node + ".output", rig_grp + ".scaleY")
        cmds.connectAttr(rig_grp + ".squash", multd_node + ".input2")
        cmds.connectAttr(main_crv + ".s", buf_grp + ".s")
        
        cmds.parent(aim_node, rig_grp)
        if u:
            cmds.setAttr(info_node + ".parameterV", 0.5)
            cmds.connectAttr(rig_grp + ".parameter", info_node + ".parameterU")
        else:
            cmds.connectAttr(rig_grp + ".parameter", info_node + ".parameterV")
            cmds.setAttr(info_node + ".parameterU", 0.5)
        cmds.select(clear = True)

def contorllerNaming(obj, alias):
    objStr = str(obj)
    objName = objStr.split('_')
    strName = objName[0]
    longName = len(strName)
    for i in range(longName):
        if str(strName)[i].isdigit():
            numberLocation = i
            objStr = strName[:numberLocation]
            objNumb = strName[numberLocation:]
            newName = objStr + alias + objNumb
        else:
            newName = strName + alias
    objName[0] = newName
    objNewName = "_".join(objName)
    return objNewName

def create_con(bone, o_p):
    """create have group controller"""
    ctrl = cmds.circle(ch = True, nr = (1, 0, 0), name = contorllerNaming(bone, "Con"))
    cmds.setAttr("%s.overrideEnabled" % (ctrl[0] + "Shape"), 1)
    cmds.setAttr("%s.overrideColor" % (ctrl[0] + "Shape"), 18)
    driver_group = cmds.group(ctrl, name = contorllerNaming(bone, "Driver"))
    anim_group = cmds.group(driver_group, name = contorllerNaming(bone, "Anim"), parent = o_p)
    cmds.delete(cmds.pointConstraint(bone, anim_group))
    cmds.delete(cmds.orientConstraint(bone, anim_group))
    cmds.parent(bone, ctrl)
    return ctrl, anim_group

def create_ik_surface(crv):
    pint = get_crv_point(crv)
    new = pint[0]/3
    ik_sureface = cmds.duplicate(crv, name = "ik_surface")
    cmds.rebuildSurface(ik_sureface, rpo = True, rt = 0, end = 1, kr = 0, kcp = False, kc = False, su = new, du = 3, sv = 1, dv =1, tol = 0.01, fr = 0, dir = 2)
    return ik_sureface

def create_ik_bone(info_node, num, data, u = True):
    """create ik control and bone"""
    ik_bone = cmds.joint(name = ("ik_jin%s" % num))
    __ctrl = create_con(ik_bone, info_node)
    hair_shape = cmds.pickWalk(info_node, d = "down")
    cmds.setAttr(hair_shape[0] + ".parameterV", 0.5)
    cmds.setAttr(hair_shape[0] + ".parameterU", data)

def create_fk_bone(num):
    """create fk control and bone"""
    wave_jin = cmds.joint(name = ("FkwaveA%s" % num))
    con_jin = cmds.joint(name = ("Fkcon_jin%s" % num), p = wave_jin)
    __ctrl = create_con(con_jin)
    cmds.connectAttr(__ctrl[0] + ".r", con_jin + ".r")
    cmds.parentConstraint(wave_jin, __ctrl[1], mo = True, weight = 1)
    return wave_jin

def create_fk_sys(crv):
    """"""
    pass

def create_ik_sys(crv):
    pass

