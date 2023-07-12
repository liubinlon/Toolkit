#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
'''
File    :   screenshot.py
Time    :   2022/09/12 15:42:08
Author  :   Liu ZhenBao
Version :   1.0
Contact :   3305510092@qq.com
Desc    :   None
'''
# import the libraries needed by this script here
from PySide2.QtWidgets import QDesktopWidget, QWidget, QApplication
from PySide2.QtGui import QPainter, QPen, QBrush, QBitmap
from PySide2.QtCore import Qt, QRect, QPoint

import sys

# here put the class script

class WScreenShot(QWidget):
    def __init__(self, parent=None):
        super(WScreenShot, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet('''background-color:black; ''')
        self.setWindowOpacity(0.6)

        desktop_rect = QDesktopWidget().screenGeometry()
        self.setGeometry(desktop_rect)
        self.setCursor(Qt.CrossCursor)
        self.blackMask = QBitmap(desktop_rect.size())
        self.blackMask.fill(Qt.black)
        self.mask = self.blackMask.copy()
        self.isDrawing = False
        self.start_point = QPoint()
        self.end_point = QPoint()

    def paintEvent(self, event):
        if self.isDrawing:
            self.mask = self.blackMask.copy()
            pp = QPainter(self.mask)
            pen = QPen()
            pen.setStyle(Qt.NoPen)
            pp.setPen(pen)
            brush = QBrush(Qt.white)
            pp.setBrush(brush)
            pp.drawRect(QRect(self.start_point, self.end_point))
            self.setMask(QBitmap(self.mask))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_point = event.pos()
            self.end_point = self.start_point
            self.isDrawing = True

    def mouseMoveEvent(self, event):
        if self.isDrawing:
            self.end_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.end_point = event.pos()
            screenshot = QApplication.primaryScreen().grabWindow(QApplication.desktop().winId())
            rect = QRect(self.start_point, self.end_point)
            outputRegion = screenshot.copy(rect)
            outputRegion.save('d:/sho54t.jpg', format='JPG', quality=100)
            self.close()
            
    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key.Key_Escape:
            self.close()

if __name__ == '__main__':
    win = WScreenShot()
    win.show()