# -*- coding: GBK -*-

import maya.cmds as cmds
from random import sample

def sel_Bfb():
    selold=cmds.ls(sl=True,fl=True)
    num=cmds.intSliderGrp("sdbfbslider",q=True,v=True)
    selnum=num*len(selold)/100
    if selnum >= len(selold):
        cmds.warning(u'�����������ѡ��ĸ����������������������')
        return ''
    selnew=sample(selold,selnum)
    cmds.select(selnew,r=True)
    
def sel_num():
    selold=cmds.ls(sl=True,fl=True)
    selnum=cmds.intSliderGrp("sdnumslider",q=True,v=True)
    if selnum >= len(selold):
        cmds.warning(u'�����������ѡ��ĸ����������������������')
        return ''
    selnew=sample(selold,selnum)
    cmds.select(selnew,r=True)
    
def sel_Bfb_Job():
    global selbfbjob
    selbfbjob=cmds.scriptJob(e=('SelectionChanged','sel_Bfb()'), parent="random_select_xj")
def sel_Num_Job():
    global selnumjon
    selnumjon=cmds.scriptJob(e=('SelectionChanged','sel_num()'), parent="random_select_xj")
def Del_Bfb_Job():
    global selbfbjob
    try:
        cmds.scriptJob(k=selbfbjob,f=True)
    except:
        cmds.warning('�ر�ʧ�ܣ�û�п�������ʹ�ô���')
def Del_Num_Job():
    global selnumjon
    try:
        cmds.scriptJob(k=selnumjon,f=True)
    except:
        cmds.warning('�ر�ʧ�ܣ�û�п�������ʹ�ô���')
def Help_Message():
    cmds.window(title="Help_Made:С��", wh=(400,170))
    cmds.columnLayout( adjustableColumn=True )
    cmds.text( label='�ýű���Ҫ�����Ƕ�ѡ��ĵ㡢�ߡ��桢��������������ɸѡ\n\n�޸��ˣ�ʹ�ú�ģ��û��ѡ�С�ѡ�к���ֱ�����߳��־���bug\n' )
    cmds.text(bgc=(0.5,0.5,0),label='ע��' )
    cmds.text( label='\nѡ�к���ֱ�����߳��־���\n���нű�help�˵��µ�clean\n\nmade vs��С��\nQQ��1181434685' )
    cmds.showWindow()
def Button_Color(but_on,but_off,On_or_Off):
    if On_or_Off=='On':
        cmds.button(but_on,e=1,bgc=(0,1,0))
        cmds.button(but_off,e=1,bgc=(0,0,0))
    elif On_or_Off=='Off':
        cmds.button(but_on,e=1,bgc=(0,0,0))
        cmds.button(but_off,e=1,bgc=(1,0,0))
window = cmds.window("random_select_xj", title="���ѡ��", iconName='Short Name', widthHeight=(300, 220) ,menuBar=True)
cmds.menu( label='Help', helpMenu=True )
cmds.menuItem( label='Message',i='advancedSettings.png',c='Help_Message()')
cmds.menuItem( label='Clean',i='activeSelectedAnimLayer.png',c='cmds.scriptJob(ka=True)')
cmds.columnLayout( adjustableColumn=True )
tabs = cmds.tabLayout()
#-------------------------------------
child1=cmds.columnLayout( adjustableColumn=True )
cmds.text(l="ѡȡ��Ҫ�������ɸѡ�ĵ㡢�ߡ��桢�������塣\n\n����Ҫ���ѡȡ����İٷֱ���")
cmds.intSliderGrp ("sdbfbslider",f=1,maxValue=100,minValue=0,cc='cmds.intSliderGrp("zdbfbslider",e=True,value=cmds.intSliderGrp("sdbfbslider",q=True,v=True))')
cmds.button( label='Apply', c='sel_Bfb()')
cmds.text(l="\n����Ҫ���ѡȡ����ĸ���")
cmds.intSliderGrp ("sdnumslider",f=1,maxValue=99999999,minValue=0,cc='cmds.intSliderGrp("zdnumslider",e=True,value=cmds.intSliderGrp("sdnumslider",q=True,v=True))')
cmds.button( label='Apply', c='sel_num()')
cmds.setParent( '..' )

#-------------------------------------
child2=cmds.columnLayout( adjustableColumn=True )
cmds.text(l="ѡȡ��Ҫ�������ɸѡ�ĵ㡢�ߡ��桢�������塣\n\n����Ҫ���ѡȡ����İٷֱ���")
cmds.intSliderGrp ("zdbfbslider",f=1,maxValue=100,minValue=0,cc='cmds.intSliderGrp("sdbfbslider",e=True,value=cmds.intSliderGrp("zdbfbslider",q=True,v=True))')
cmds.rowLayout(nc=2)
cmds.button('buton1', label='����',w=150,bgc=(0,0,0), c='sel_Bfb_Job()\nButton_Color("buton1","butoff1","On")')
cmds.button('butoff1', label='�ر�',w=150,bgc=(0,0,0), c='Del_Bfb_Job()\nButton_Color("buton1","butoff1","Off")')
cmds.setParent( '..' )
cmds.text(l="\n����Ҫ���ѡȡ����ĸ���")
cmds.intSliderGrp ("zdnumslider",f=1,maxValue=99999999,minValue=0,cc='cmds.intSliderGrp("sdnumslider",e=True,value=cmds.intSliderGrp("zdnumslider",q=True,v=True))')
cmds.rowLayout(nc=2)
cmds.button('buton2', label='����',w=150,bgc=(0,0,0), c='sel_Num_Job()\nButton_Color("buton2","butoff2","On")')
cmds.button('butoff2', label='�ر�',w=150,bgc=(0,0,0), c='Del_Num_Job()\nButton_Color("buton2","butoff2","Off")')
cmds.setParent( '..' )
cmds.setParent( '..' )
#-------------------------------------
cmds.tabLayout( tabs, edit=True, tabLabel=((child1, '�ֶ�'), (child2, '�Զ�')) )
cmds.setParent( '..' )

cmds.showWindow( window )