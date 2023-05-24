#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = 'miaoChenLiang'

# --+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+--#
import xml
import cStringIO
import maya.OpenMayaUI as mui

from GUIImport import *


# --+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+--#

def GetMayaLayout(layoutString):
    ptr = mui.MQtUtil.findLayout(layoutString)
    if ptr:
        return wrapInstance(long(ptr))


def GetWindow(windowName):
    ptr = mui.MQtUtil.findWindow(windowName)
    if ptr:
        return wrapInstance(long(ptr))


def GetFullName(qObj):
    pointer = sip.unwrapinstance(qObj)
    if type(pointer) == long:
        windowString = mui.MQtUtil.fullName(pointer)
        if windowString:
            return windowString
        else:
            return ''
    else:
        return GetQtWidget(qObj.objectName(), LongName=True)[-1]


def wrapInstance(widget):
    if isinstance(widget, basestring):
        widget = mui.MQtUtil.findWindow(widget)
    if USE_PYQT_MODULE:
        return sip.wrapinstance(long(widget), QObject)
    else:
        return shiboken.wrapInstance(long(widget), QWidget)


def GetMayaMainWindow():
    maya_window = mui.MQtUtil.mainWindow()
    return wrapInstance(maya_window)


def GetQtWidget(QWidgetName, LongName=False):
    RootName = str(GetMayaMainWindow().objectName())
    Name = QWidgetName.split('|')[-1]
    for w in QApplication.topLevelWidgets():
        try:
            if w.objectName() == Name:
                if LongName:
                    return w, '|' + '|'.join([RootName, QWidgetName])
                else:
                    return w
        except:
            pass

    try:
        for w in QApplication.topLevelWidgets():
            for c in w.children():
                if c.objectName() == Name:
                    if LongName:
                        return c, '|' + '|'.join([str(w.objectName()), str(c.objectName())])
                    else:
                        return c

    except:
        pass


def UIExists(Name, AsBool=True):
    QObject = GetQtWidget(Name)
    if QObject:
        if AsBool:
            return bool(QObject)
        return QObject
    elif AsBool:
        return False
    else:
        return None


def Raise(Name):
    qobject = GetQtWidget(Name)
    if qobject:
        return qobject
    else:
        return False


def deleteUI(Name):
    qObject = GetQtWidget(Name)
    if USE_PYQT_MODULE:
        sip.delete(qObject)
    else:
        shiboken.delete(qObject)


def loadUi(uiPath):
    '''
    read an ui file, get two classes to return..
    '''
    if USE_PYQT_MODULE:
        form_class, base_class = __pyqtLoadUi(uiPath)
    else:
        form_class, base_class = __pysideLoadUi(uiPath)
    return form_class, base_class


def __pyqtLoadUi(uiPath):
    '''
    read an ui file, use PyQt4 method get two classes to return..
    '''
    return uic.loadUiType(uiPath)


def __pysideLoadUi(uiPath):
    '''
    read an ui file, use PySide method get two classes to return..
    '''
    parsed = xml.etree.ElementTree.parse(uiPath)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text

    with open(uiPath, 'r') as f:
        o = cStringIO.StringIO()
        frame = dict()

        uic.compileUi(f, o, indent=0)

        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame

        form_class = frame['Ui_%s' % form_class]
        base_class = eval(widget_class)

    return form_class, base_class
