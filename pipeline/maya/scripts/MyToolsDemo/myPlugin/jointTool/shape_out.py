import maya.cmds as cmds


sacv = cmds.ls(sl=1)
shape = cmds.listRelatives(sacv, shapes = True,f = 1)
new_curs = []
for i in shape:
    s = i.split('|')
    new_cur = s[-1].replace('Shape','') + '_f'
    cmds.group(em = 1, n = new_cur)
    cmds.parent(i, new_cur, add = 1, s = 1)
    new_curs.append(new_cur)
cmds.delete(sacv)
for i in new_curs:
    cmds.rename(i, i.replace('_f', ''))