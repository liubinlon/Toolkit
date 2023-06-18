import maya.cmds as cmds
import maya.api.OpenMaya as om

def show_prompt_dialog(title, message, icon=None):
    cmds.confirmDialog(title=title, message=message, button=['OK'], defaultButton='OK', cancelButton='OK', dismissString='OK', icon=icon)


def find_nearest_joints(source_joint, target_joint):
    source_list = cmds.listRelatives(source_joint, ad=1, type="joint")
    source_list.append(source_joint)
    target_list = cmds.listRelatives(target_joint, ad=1, type="joint")
    target_list.append(target_joint)
    nearest_pairs = []
    
    for source_joint in source_list:
        closest_joint = None
        closest_distance = float('inf')

        source_pos = cmds.xform(source_joint, query=True, worldSpace=True, translation=True)
        source_pos = om.MVector(source_pos[0], source_pos[1], source_pos[2])

        for target_joint in target_list:
            target_pos = cmds.xform(target_joint, query=True, worldSpace=True, translation=True)
            target_pos = om.MVector(target_pos[0], target_pos[1], target_pos[2])

            distance = (target_pos - source_pos).length()

            if distance < closest_distance:
                closest_distance = distance
                closest_joint = target_joint

        if closest_joint:
            nearest_pairs.append((source_joint, closest_joint))

    return nearest_pairs

try:
    source_joints, target_joints = cmds.ls(sl=1)
    nearest_pairs = find_nearest_joints(source_joints, target_joints)
    
    if nearest_pairs:
        for pair in nearest_pairs:
            source_joint, target_joint = pair
            cmds.parentConstraint(source_joint, target_joint, maintainOffset=True)
            cmds.scaleConstraint(source_joint, target_joint, maintainOffset=True)
        show_prompt_dialog("信息", "约束完成！", "information")
    else:
        show_prompt_dialog("错误", "找不到最近的骨骼对列表！", "critical")
except:
    show_prompt_dialog("提示", "请先选择驱动根骨，再选择被驱动骨骼根骨！", "warning")