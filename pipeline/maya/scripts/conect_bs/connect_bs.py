#output bs data
def CL_listBSindex(bsName):
	attrName = []
	# attr=pm.blendShape(bsName,q=1,weight=1)
	attr = pm.listAttr(bsName, m=True, st="weight")
	# attr=pm.aliasAttr(bsName+".weight[*]", q=True)
	# num=len(attr)

	if not attr:
		return attrName

	for n in attr:
		indexName = bsName + "." + n
		# aa=pm.setAttr(bsName+'.weight['+str(n)+']', 0)
		aa = pm.aliasAttr(indexName, q=1)
		attrName.append(aa)

	return attrName
bs_name = "body_BS"
lst_index = CL_listBSindex(bs_name)

def CL_findConnections(bsNode, bsIndex):
    connection = dict()
    if bsIndex:
        for value, item in enumerate(bsIndex):
            bs_attr = bsNode + "." + item            
            try:
                input = pm.listConnections(bs_attr, s=True, d=False, plugs=True)[0]
                connection[str(input)] = str(bs_attr)
            except:
                pass
    return connection

index_dict = CL_findConnections(bs_name, lst_index)
print(index_dict)
import json

with open("D:/ProjectAssets/GB_PV1/Asset/Chars/fengling/fengline_bs.json", 'w') as load_f:
        load_dict = json.dump(index_dict, load_f)

# input bs data

import json
def get_menu_data():
    with open("D:/ProjectAssets/GB_PV1/Asset/Chars/fengling/fengline_bs.json", 'r') as load_f:
        load_dict = json.load(load_f)
    return load_dict
data_dict = get_menu_data()
for key, value in data_dict.items():
    try:
        pm.connectAttr(key, value)
    except:
        pass
# 
import json
attr_dict = dict()
lst = pm.ls(sl=1)
for fol in lst:
    shape_node = fol.getShape()
    to_mesh = pm.listConnections(shape_node, s=1, d=0, c=1, p=1)
    parent_constraint_node = pm.listConnections(fol, t="transform")[0]
    tran_node = pm.listConnections(parent_constraint_node, t="transform")[0]
    attr_dict[fol.name()] = {"constraint": tran_node.name(),
                        "connections": [to_mesh[0][-1].name(), to_mesh[0][0].name(), to_mesh[1][-1].name(), to_mesh[1][0].name()]
                        }
json_str = json.dumps(attr_dict, indent=4)
with open("D:/ProjectAssets/GB_PV1/Asset/Chars/fengling/rig/GB_PV1_Chars_RIG_Fengling-WalkingDress.json", 'w') as load_f:
        load_f.write(json_str)