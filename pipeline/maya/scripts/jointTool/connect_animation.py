# find controller broken animation curve and try go to connection
import maya.cmds as cmds

selection = cmds.ls(sl=True)
anim_list = cmds.ls(type=["animCurveTU", "animCurveTL", "animCurveTA"])


def get_name(name):
    """
    :return:controller name
    """
    namestr = name.split(":")
    return namestr[-1]


for crv in selection:
    name_number = get_name(crv)
    attr_list = cmds.listAttr(crv, keyable=True, unlocked=True)

    attr_number = len(attr_list)

    if attr_number != 0:
        for attr in range(attr_number):
            anim = name_number + "_" + attr_list[attr]

            if anim in anim_list:
                cmds.connectAttr(anim + ".output", crv + ".%s" % attr_list[attr])
    else:
        continue
