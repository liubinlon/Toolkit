import pymel.core as pmc
 
def getSelectedChannels():
    channelBox = pmc.mel.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')	
    attrs = pmc.channelBox(channelBox, q=1, sma=1)
    if not attrs:
        return []
    return attrs
 
 
def setDefaultsBySelect():
    sel = pmc.ls(sl=1)
    for node in sel:
        if getSelectedChannels() == []:
            for attr in node.listAnimatable():
                pAttr = attr.partition('.')[2]
                defaultValue = pmc.attributeQuery(pAttr, node=node, ld=1)[0]
                attr.set(defaultValue)
        else: 
            for attr in getSelectedChannels():
                defaultValue = pmc.attributeQuery(attr, node=node, ld=1)[0]
                pmc.setAttr(node+"."+attr, defaultValue)
                
setDefaultsBySelect()