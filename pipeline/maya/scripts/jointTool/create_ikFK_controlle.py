import maya.cmds as cmds
import pymel.core as pm


class Conffirm(object):
    pass


def asMayaVersionAsFloat(args):
    pass


class Skeleton:
    def __init__(self):
        self.currentUnit_Linear = cmds.currentUnit(query=True, fullName=True)
        self.animblending_opt = cmds.optionVar(q="animBlendingOpt")
        self.have_ran_this_version = cmds.optionVar(q="")
    if self.currentUnitLinear != "centimeter":
        if cmds.confirmDialog(title="Conffirm", message="", button=["Ok", "Cancel"], defaultButton="Ok") == "Ok":
            cmds.currentUnit(linear="cm")
    if self.animblending_opt != 1:
        cmds.optionVar(intValue=["animBlendingOpt", 1])
        print "// \'Animation Blending Option\' now switched to On.\n"

    # if repr(asMayaVersionAsFloat) >= 2012:
    #     if cmds.manipMoveContext(query=True, exists=True):
    #         if !catchQuiet

    def bone_list(self, bone):
        """
        @param bone:Get root joint name
        @return: joint list
        """
        list_joint = cmds.listRelatives(bone, type="joint", ad=True)
        list_joint.append(bone)
        list_joint.reverse()
        return list_joint

    def contorllerNaming(self, obj, alias):
        """
        @param alias: object name
        @return: new object name
        """
        global new_name
        obj_str = str(obj)
        obj_name = obj_str.split('_')
        str_name = obj_name[0]
        long_name = len(str_name)

        for i in range(long_name):
            if str(str_name)[i].isdigit():
                number_location = i
                obj_str = str_name[:number_location]
                obj_numb = str_name[number_location:]
                new_name = obj_str + alias + obj_numb
            else:
                new_name = str_name + alias

        obj_name[0] = new_name
        obj_newname = "_".join(obj_name)
        return obj_newname

    def create_ikfk_controlle(self, lst_joint):
        fk_list = []
        ik_list = []
        strat_joint = cmds.duplicate(lst_joint)
        now_joint = self.bone_list(strat_joint)
        for i in now_joint:
            fk_joint = i.replice("Skin", "Fk")
            fk_list.append(fk_joint)
            ik_joint = i.replice("Skin", "Ik")
            ik_list.append(ik_joint)
            cmds.createNode("blendColor", name=i.replice(joint, ))
