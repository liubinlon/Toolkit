#coding:GBK
u'''
#################################
#
#  HolyPipe 红鲸影视 版权所有
#
#################################

红鲤动画|红鲸影视 的“普天同庆”Maya病毒 查杀工具。
针对.ma文件进行批量查杀。
请从红鲤动画官网下载本代码的最新版本运行
http://www.honglianimation.com/res/pttq.zip

此工具更详细的说明，请见红鲤动画公众号文章：
https://mp.weixin.qq.com/s/0Wxru1Flyxn2XRwofETM5A
'''

__version__ = '20200623.0'

import sys, os, subprocess, json,time,datetime, glob, tempfile
import getpass, platform
import shutil
from stat import ST_ATIME,ST_CTIME,ST_MTIME
__gui__ = 'missing'
try:
    from PySide2 import QtWidgets as qw,  QtCore
    __gui__ = 'PySide2'
except:
    from PySide import QtGui as qw, QtCore
    __gui__ = 'PySide'


#region scan core
#directory 需要扫描的路径//nas/data/PipePrjWork/putiantongqing/最后以斜线结尾
#tryFix 1是修复，0是不修复
#recursion 1是递归，0是不递归
#logPath 扫描"//nas/data/PipePrjWork/putiantongqing/pan_yao.txt"
#skipLog 0是断点续扫，1是重新扫描
def Scanner_ErrorFile_Main(directory,tryFix,recursion,logPath,skipLog, 
                                                uiInfoCallback=lambda info:None, 
                                                uiAddVirusCallback=lambda filePath:None):
    #若重新扫描，删掉log，后改为不删log
    #if skipLog == 1 and os.path.isfile(logPath):
    #    os.remove(logPath)
    timeNow = datetime.datetime.now()
    timeNowStr = timeNow.strftime("%Y-%m-%d %H:%M:%S")
    writeLog(logPath,timeNowStr+',scann Folder Path:'+directory+'\n')
    allMa = []
    errFileList = []
    if recursion:#递归扫描文件夹里的所有ma，并直接扫描，以免服务器根目录递归过程报错无法断点续扫
        ScanFilesFromFolder(directory,logPath,skipLog,prefix=None,postfix='.ma',  tryFix=tryFix,
                                    uiInfoCallback=uiInfoCallback,
                                    uiAddVirusCallback=uiAddVirusCallback)
    else:#非递归扫描文件夹里的所有ma
        getAllFile = os.listdir(directory)
        #断点续扫，读取log里记录的扫过的文件路径信息
        logInfo = ''
        if skipLog == 0 and os.path.isfile(logPath):
            f = open(logPath,'r')
            logInfo = f.read()
            f.close()
        for mm in getAllFile:
            #若扫描过，则跳过
            if skipLog == 0 and logInfo and logInfo.count(directory+mm):
                print(directory+mm+' is already scann\n')
                continue
            if mm.endswith('.ma'):
                allMa.append(directory+mm)
        #根据扫描出来的ma文件列表，进行下一步处理
        for i,mm in enumerate(allMa):
            uiInfoCallback('scaning (%i/%i): %s'%(i, len(allMa), mm))
            isErrorFile = DoScanFile(mm,tryFix,logPath,skipLog)
            if isErrorFile:
                errFileList.append(mm)
                uiAddVirusCallback(mm)
        return errFileList

def ScanFilesFromFolder(directory,logPath,skipLog,prefix=None,postfix=None, 
                                        uiInfoCallback=lambda info:None, 
                                        uiAddVirusCallback=lambda filePath:None,
                                        tryFix=False):
    files_list=[]
    #logInfo = ''
    #断点续扫，读取log里记录的扫过的文件信息
    #log文件记录方式：True d:/.../aa.ma    tryFix  202006221500    1024L
    fileInLogDic = {}
    alreadyExaminFiles = []
    if skipLog == 0 and os.path.isfile(logPath):
        f = open(logPath,'r')
        lines = f.readlines()
        f.close()
        for mm in range(len(lines)):
            getLineInfo = lines[mm].decode('utf-8').strip().split('\t')
            if len(getLineInfo) == 5:
                fileInLogDic[getLineInfo[2]] = {'virus':getLineInfo[0],'killed':getLineInfo[1],'mtime':getLineInfo[3],'size':getLineInfo[4]}
        alreadyExaminFiles = fileInLogDic.keys()

    def appendScanFile(filePath):
        files_list.append(filePath)
        uiInfoCallback('scaning (%i): %s'%(len(files_list),  filePath))
        isErrorFile = DoScanFile(filePath,tryFix,logPath,skipLog, uiAddVirusCallback=uiAddVirusCallback)

    for root, sub_dirs, files in os.walk(directory):
        uiInfoCallback('gathering files (%i): '% len(files_list)+root+'\\')
        for special_file in files:
            if not special_file.lower().endswith('.ma'):
                continue
            uiInfoCallback('gathering files (%i): '% len(files_list)+os.path.join(root,special_file) )
            if postfix:
                if special_file.endswith(postfix):
                    if alreadyExaminFiles:#非第一次扫描
                        if alreadyExaminFiles.count(os.path.join(root,special_file)):#文件被扫描过
                            if time.strftime("%Y%m%d%H%M%S",time.localtime(os.path.getmtime(os.path.join(root,special_file)))) == fileInLogDic.get(os.path.join(root,special_file)).get('mtime'):#文件修改时间和log里记录的上次扫描时的修改时间一致，即本次扫描和上次扫描比，文件没有改动
                                if fileInLogDic.get(os.path.join(root,special_file)).get('virus') == 'True' and fileInLogDic.get(os.path.join(root,special_file)).get('killed') == 'False':#上次有毒，且只扫没杀，需要重新扫描并杀毒
                                    appendScanFile(os.path.join(root,special_file))
                                else:
                                    continue
                            else:#虽文件扫描过，但文件有修改，需要重新扫描
                                appendScanFile(os.path.join(root,special_file))
                        else:#文件没有被扫描过
                            appendScanFile(os.path.join(root,special_file))
                    else:#第一次扫描
                        appendScanFile(os.path.join(root,special_file))
            elif prefix:
                if special_file.startswith(prefix):
                    if alreadyExaminFiles:#非第一次扫描
                        if alreadyExaminFiles.count(os.path.join(root,special_file)):#文件被扫描过
                            if time.strftime("%Y%m%d%H%M%S",time.localtime(os.path.getmtime(os.path.join(root,special_file)))) == fileInLogDic.get(os.path.join(root,special_file)).get('mtime'):#文件修改时间和log里记录的上次扫描时的修改时间一致，即本次扫描和上次扫描比，文件没有改动
                                if fileInLogDic.get(os.path.join(root,special_file)).get('virus') == 'True' and fileInLogDic.get(os.path.join(root,special_file)).get('killed') == 'False':#上次有毒，且只扫没杀，需要重新扫描并杀毒
                                    appendScanFile(os.path.join(root,special_file))
                                else:
                                    continue
                            else:#虽文件扫描过，但文件有修改，需要重新扫描
                                appendScanFile(os.path.join(root,special_file))
                        else:#文件没有被扫描过
                            appendScanFile(os.path.join(root,special_file))
                    else:#第一次扫描
                        appendScanFile(os.path.join(root,special_file))
            else:
                #若扫描过，则跳过
                if skipLog == 0 and alreadyExaminFiles and alreadyExaminFiles.count(os.path.join(root,special_file)):
                    print(os.path.join(root,special_file)+' is already scanned\n')
                    continue
                appendScanFile(os.path.join(root,special_file))
                if alreadyExaminFiles:#非第一次扫描
                    if alreadyExaminFiles.count(os.path.join(root,special_file)):#文件被扫描过
                        if time.strftime("%Y%m%d%H%M%S",time.localtime(os.path.getmtime(os.path.join(root,special_file)))) == fileInLogDic.get(os.path.join(root,special_file)).get('mtime'):#文件修改时间和log里记录的上次扫描时的修改时间一致，即本次扫描和上次扫描比，文件没有改动
                            if fileInLogDic.get(os.path.join(root,special_file)).get('killed') == False and tryFix:#上次只扫没杀，本次若需要杀毒，需要重新扫描并杀毒
                                appendScanFile(os.path.join(root,special_file))
                            else:
                                continue
                        else:#虽文件扫描过，但文件有修改，需要重新扫描
                            appendScanFile(os.path.join(root,special_file))
                    else:#文件没有被扫描过
                        appendScanFile(os.path.join(root,special_file))
                else:#第一次扫描
                    appendScanFile(os.path.join(root,special_file))
    return files_list

def DoScanFile(maPath,tryFix,logPath,skipLog, uiAddVirusCallback=lambda filePath:None):
    try:
        print('scanning: %s'%maPath)
        maPath = LongLongFile(maPath)
        errFile = 0
        f = open(maPath,'r')
        lines = f.readlines()
        lenLines = len(lines)
        errLine = []
        for mm in range(lenLines):
            if lines[mm].count('createNode script -n "'):
                #fopen  fprint  fclose同时出现，判断为带毒
                isFopen = 0
                isFprint = 0
                isFclose = 0
                #print '-------------start---------------'
                errLine.append(mm)
                tt = mm + 1
                while not lines[tt].startswith('createNode ') and not lines[tt].startswith('select ') and not lines[tt].startswith('select ') and not lines[tt].startswith('connectAttr ') :
                    isError = IsHaveKeyword(lines[tt])
                    if isError:
                        errFile = 1
                    if lines[tt].count('fopen'):
                        isFopen = 1
                    if lines[tt].count('fprint'):
                        isFprint = 1
                    if lines[tt].count('fclose'):
                        isFclose = 1
                    errLine.append(tt)
                    tt = tt + 1
                    if tt>=lenLines:
                        break
                if errFile == 0:
                    if isFopen == 1 and isFprint == 1 and isFclose == 1:
                        print('have fopen  fprint  fclose')
                        errFile = 1
        f.close()
        if tryFix and errFile:
            if errLine:
                #修复前先备份为后缀.putiantongqing
                copyFrom = maPath
                copyTo = maPath+'.putiantongqing'
                shutil.copy(copyFrom,copyTo)
                file_stat = os.stat(copyFrom)
                os.utime(copyTo, (file_stat[ST_CTIME], file_stat[ST_MTIME]))
                #os.remove(maPath)
                with open(maPath, "w",) as f:
                    for mm in range(len(lines)):
                        if errLine.count(mm):
                            continue
                        else:
                            f.write(lines[mm])
                f.close()
        #写入log
        #获取ma文件的修改时间和大小，写入log
        tryFixInfo = 'False'
        if tryFix:
            tryFixInfo = 'True'
        mTime= time.strftime("%Y%m%d%H%M%S",time.localtime(os.path.getmtime(maPath)))
        fileSize = os.path.getsize(maPath)
        if errFile:
            writeLog(logPath,'True\t'+tryFixInfo+'\t'+maPath+'\t'+str(mTime)+'\t'+str(fileSize)+'\n')
        else:
            writeLog(logPath,'False\t'+tryFixInfo+'\t'+maPath+'\t'+str(mTime)+'\t'+str(fileSize)+'\n')
        if errFile:
            uiAddVirusCallback(maPath)
        return errFile
    except:
        message = traceException(makeError=0)
        writeLog(logPath+'.except',maPath+'\n'+message+'\n')

def IsHaveKeyword(lineInfo):
    keyWord = ['UI_Mel_Configuration_think',
                   'UI_Mel_Configuration_think_a',
                   'UI_Mel_Configuration_think_b',
                   'autoUpdateAttrEd_SelectSystem',
                   'autoUpdatcAttrEd',
                   'autoUpdatoAttrEnd',
                   'fuck_All_U',
                   '$PuTianTongQing']
    for mm in keyWord:
        if lineInfo.count(mm):
            return 1
    return 0

def writeLog(logPath,infoStr):
    f = open(logPath, 'a')
    f.write(infoStr.encode('utf-8'))
    f.close()

def LongLongFile(result):
    if len(result)>=260:
        if result[2:3]!='?':
            if result[:2] in ['\\\\','//']:
                result = r'\\?\UNC\%s'%result[2:].replace('/','\\')
            else:
                result = r'\\?\%s'%result.replace('/','\\')
        else:
            result = result.replace('/','\\')
    return result

def traceException(makeError=0):
    import traceback, StringIO
    fp = StringIO.StringIO()
    traceback.print_exc(file=fp)
    message = fp.getvalue()
    if message.split('\n')[-2][0:len('SystemExit')] != 'SystemExit':
        if makeError:
            raise RuntimeError, message
            pass
        else:
            print(message)
            return message
# endregion scan core

# region gui
class VirusOp():
    def __init__(self):
        self.closeExistingWindow()
        self.show_ui()

    def closeExistingWindow(self):
        for qt in qw.QApplication.topLevelWidgets():
            try:
                if qt.windowTitle() == u'Virus Scan Clean':
                    qt.close()
            except:
                pass

    def getFileDialogText(self):
        scanPath = self.inputPathDir.getExistingDirectory()
        self.filePath.setText(scanPath)

    def getLogDialogText(self):
        savePath = self.logDir.getOpenFileName()
        self.logPath.setText(savePath)

    def getFilePath(self):
        curFilePath = self.filePath.text()
        print('scan path is:')
        print(curFilePath)
        print('\n')
        return curFilePath + '\\'

    def getLogPath(self):
        curLogPath = self.logPath.text()
        print('log path is:')
        print(curLogPath)
        print('\n')
        return curLogPath

    def getScanMode(self):
        curMode = self.modeCB.currentText()
        print('scan mode is:')
        print(curMode)
        scanMode = 0
        if curMode == u'重新扫描':
            scanMode = 1
        if curMode == u'断点扫描':
            scanMode = 0
        print(scanMode)
        print('\n')
        return scanMode

    def getCleanState(self):
        curState = self.scanCleanBtn.checkState()
        print('clean state is:')
        print(curState)
        cleanState = 0
        if curState == 0:
            cleanState = 0
        else:
            cleanState = 1
        print(cleanState)
        print('\n')
        return cleanState

    def getWalkState(self):
        curState = self.scanWalkBtn.checkState()
        print('walk state is:')
        print(curState)
        walkState = 0
        if curState == 0:
            walkState = 0
        else:
            walkState = 1
        print(walkState)
        print('\n')
        return walkState

    def addList(self, virusList):
        scanModeParam = self.getScanMode()
        if scanModeParam:
            self.fileList.clear()
        for iFile in virusList:
            self.fileList.addItem(iFile)
        print('finish adding\n')

    def getRefState(self, event):
        refState = 0
        if self.refBtn1.isChecked():
            refState = 0
        if self.refBtn2.isChecked():
            refState = 1
        if self.refBtn3.isChecked():
            refState = 2
        self.query.close()

        subPaths = []
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.LinkAction)
            event.accept()
            for url in event.mimeData().urls():
                filePath = unicode(url.toLocalFile())
                print(filePath)
                if os.path.isfile(filePath) and filePath.lower().endswith('.ma'):
                    subPaths.extend([filePath])
                elif os.path.isdir(filePath):
                    subPaths.extend([x for x in glob.glob(filePath+'/*') if os.path.isfile(x) and x.lower().endswith('.ma')])
        elif event.mimeData().hasText():
            event.setDropAction(QtCore.Qt.LinkAction)
            event.accept()
            for text in event.mimeData().text().splitlines():
                # filePath = text.split('\t')[-1].replace('"','')
                for iPart in text.split('\t'):
                    tempPath = iPart.replace('"','')
                    if os.path.isfile(tempPath) and tempPath.lower().endswith('.ma'):
                        subPaths.extend([tempPath])
                    elif os.path.isdir(tempPath):
                        subPaths.extend([x for x in glob.glob(tempPath+'/*') if os.path.isfile(x) and x.lower().endswith('.ma')])
        
        def recursiveGetRef(fileName, outList=[], cacheDict={}, recursive=True):
            fileName = os.path.expandvars(fileName).replace('\\', '/')
            if not os.path.isfile(fileName):
                return
            if fileName not in cacheDict:
                cacheDict[fileName] = 1
                outList.append(fileName)
                self.fileList.addItem('\t'+fileName)
                qw.QApplication.instance().processEvents()
            curFile = open(u'%s' % fileName, 'rb')
            curLine = curFile.readline()
            while curLine:
                while not curLine.strip().endswith(';'):
                    curLine += curFile.readline()
                if 'file -rdi ' in curLine and '.ma' in curLine:
                    maPath = os.path.expandvars(curLine.split('\"')[-2]).replace('\\', '/')
                    if not os.path.isfile(maPath):
                        maPath = os.path.dirname(fileName)+'/'+os.path.basename(maPath)
                    if not os.path.isfile(maPath):
                        print('Referenc path not accessable: %s'%maPath)
                        curLine = curFile.readline()
                        continue
                    if maPath not in cacheDict:
                        recursiveGetRef(maPath, outList=outList, cacheDict=cacheDict, recursive=True) if recursive else None
                if 'file -r ' in curLine and '.ma' in curLine:
                    maPath = os.path.expandvars(curLine.split('\"')[-2]).replace('\\', '/')
                    if not os.path.isfile(maPath):
                        maPath = os.path.dirname(fileName)+'/'+os.path.basename(maPath)
                    if not os.path.isfile(maPath):
                        curLine = curFile.readline()
                        print('Referenc path not accessable: %s'%maPath)
                        continue
                    
                    if maPath not in cacheDict:
                        recursiveGetRef(maPath, outList=outList, cacheDict=cacheDict, recursive=True) if recursive else None

                if 'requires ' in curLine:
                    break
                curLine = curFile.readline()
            curFile.close()

        listedPathCache = {}
        if refState == 0:
            for iSubPath in sorted(list(set(subPaths))):
                self.fileList.addItem('\t'+iSubPath)
                listedPathCache[iSubPath.split('\t')[-1].replace('\\','/')] = 1

        if refState == 1:
            print(u'one')
            for i, iSubPath in enumerate(subPaths):
                recursiveGetRef(iSubPath, outList=subPaths, cacheDict=listedPathCache, recursive=False)

        if refState == 2:
            print(u'all')
            for i, iSubPath in enumerate(subPaths):
                recursiveGetRef(iSubPath, outList=subPaths, cacheDict=listedPathCache, recursive=True)


    def refQuery(self, event):

        self.query = qw.QDialog()
        self.query.setWindowFlags(QtCore.Qt.Window|QtCore.Qt.WindowStaysOnTopHint)
        self.query.setWindowTitle('Query')

        vLay = qw.QVBoxLayout()
        self.query.setLayout(vLay)

        scanLabel = qw.QLabel(u'扫描Maya文件中的Reference')
        vLay.addWidget(scanLabel)

        hLay = qw.QHBoxLayout()
        vLay.addLayout(hLay)

        self.refBtn1 = qw.QRadioButton(u'不包括Ref')
        self.refBtn1.setChecked(1)
        hLay.addWidget(self.refBtn1)

        self.refBtn2 = qw.QRadioButton(u'包括一层Ref')
        hLay.addWidget(self.refBtn2)

        self.refBtn3 = qw.QRadioButton(u'包含所有Ref')
        hLay.addWidget(self.refBtn3)

        hLayRecovery = qw.QHBoxLayout()
        vLay.addLayout(hLayRecovery)
        hLayRecovery.addStretch()

        recoveryButton = qw.QPushButton(u'   确定   ')
        recoveryButton.clicked.connect(lambda a=1,e=event: self.getRefState(e))
        hLayRecovery.addWidget(recoveryButton)

        vLay.addStretch()
        self.query.exec_()

    def getList(self):
        itemNum = self.fileList.count()
        itemList = []
        self.listDict = {}
        for i in range(itemNum):
            curItem = self.fileList.item(i)
            curItemName = curItem.text()
            itemList.append(curItemName)
            self.listDict[curItemName.split('\t')[-1]] = i
            print(curItemName)
        print(itemList)
        return itemList

    def emptyList(self):
        removeList = self.fileList.selectedItems()
        rows = sorted([self.fileList.row(item) for item in removeList])[::-1]
        for row in rows:
            removedItem = self.fileList.takeItem(row)
            print('removed from list:', removedItem.text())

    def scanList(self):
        print('start to scan list\n')
        itemList = self.getList()
        print(itemList)
        for iMa in itemList:
            print('start cleaning\n')
            print(iMa)
            maPath = iMa.split('\t')[-1]
            DoScanFile(maPath, 1, self.getLogPath(), self.getScanMode(), uiAddVirusCallback=lambda path:self.updateScanned(path))
            print('finish cleaning\n')

    def updateScanned(self,filePath):
        self.fileList.item(self.listDict[filePath]).setText('cleaned\t'+filePath)

    def scanFuc(self):
        print('start to scan')

        filePathParam = self.getFilePath()
        print('scan path is:')
        print(filePathParam)

        logPathParam = self.getLogPath()
        if not os.path.isdir(os.path.dirname(logPathParam)):
            os.makedirs(os.path.dirname(logPathParam))
        print('log path is:')
        print(logPathParam)
        
        scanModeParam = self.getScanMode()
        print('scan mode is:')
        print(scanModeParam)

        cleanStateParam = self.getCleanState()
        print('clean state is:')
        print(cleanStateParam)

        walkStateParam = self.getWalkState()
        print('walk state is:')
        print(walkStateParam)

        print('start to scan and clean\n')
        virusFileList = Scanner_ErrorFile_Main(filePathParam, cleanStateParam, walkStateParam, logPathParam, scanModeParam, 
                                                                uiInfoCallback=lambda info:self.uiInfo(info),
                                                                uiAddVirusCallback=lambda filePath, clean=cleanStateParam:self.fileList.addItem(('virus\t' if not clean else 'cleaned\t')+filePath))
        print(virusFileList)
        print('\n')
        print('finish scanning and cleaning\n')

    def uiInfo(self, info):
        self.infoLabel.setText(info)
        qw.QApplication.instance().processEvents()

    def show_ui(self):

        self.ui = qw.QWidget()
        self.ui.resize(800,500)
        self.ui.setWindowFlags(QtCore.Qt.Window|QtCore.Qt.WindowStaysOnTopHint)
        self.ui.setWindowTitle(u'Virus Scan Clean')

        topLay = qw.QVBoxLayout()
        topLay.setContentsMargins(0,0,0,0)
        self.ui.setLayout(topLay)

        titlebar = qw.QLabel(u'  Hongli Animation    Ver: %s    GUI: %s    '%(__version__, __gui__))
        titlebar.setStyleSheet('background-color:rgb(16,128,196); color:white; font-size:16px')
        titlebar.setFixedHeight(30)
        topLay.addWidget(titlebar)

        mainLay = qw.QVBoxLayout()
        mainLay.setContentsMargins(10,0,10,10)
        topLay.addLayout(mainLay)

        
        inputLabel = qw.QLabel(u'Input Scan Directory:')
        mainLay.addWidget(inputLabel)

        pathLay = qw.QHBoxLayout()
        mainLay.addLayout(pathLay)

        self.filePath = qw.QLineEdit()
        self.filePath.setMinimumWidth(400)
        pathLay.addWidget(self.filePath)

        viewButton = qw.QPushButton(u'    浏览    ')
        pathLay.addWidget(viewButton)
        viewButton.clicked.connect(lambda *args: self.getFileDialogText())

        self.inputPathDir = qw.QFileDialog()

        user = getpass.getuser()
        pc = platform.node()
        print('user is: ' + user)
        print('pc is: ' + pc)
        print('\n')
        defaultLogPath = '//nas/data/PipePrjWork/__UniPipe_Test/PuTianTongQing_logs/%s_%s_virusScan.log' % (user, pc)
        if not os.path.isdir('//nas/data/PipePrjWork/__UniPipe_Test'):
            defaultLogPath = tempfile.gettempdir().replace('\\','/')+'/PuTianTongQing_logs/%s_%s_virusScan.log' % (user, pc)
        print('default log path is: ' + defaultLogPath)
        print('\n')
        
        logLabel = qw.QLabel(u'Scan Log Path:')
        mainLay.addWidget(logLabel)

        logLay = qw.QHBoxLayout()
        mainLay.addLayout(logLay)

        self.logPath = qw.QLineEdit()
        self.logPath.setMinimumWidth(400)
        logLay.addWidget(self.logPath)
        self.logPath.setText(defaultLogPath)

        logButton = qw.QPushButton(u'    浏览    ')
        logLay.addWidget(logButton)
        logButton.clicked.connect(lambda *args: self.getLogDialogText())

        self.logDir = qw.QFileDialog()
        self.logDir.setDirectory('//nas/data/PipePrjWork/__UniPipe_Test')

        modeLay = qw.QHBoxLayout()
        mainLay.addLayout(modeLay)
        modeLay.addStretch()

        modeLabel = qw.QLabel(u'扫描模式: ')
        modeLay.addWidget(modeLabel)

        self.modeCB = qw.QComboBox()
        modeLay.addWidget(self.modeCB)
        self.modeCB.setEditable(0)
        self.modeCB.setMinimumWidth(185)
        self.modeCB.addItem(u'断点扫描')
        self.modeCB.addItem(u'重新扫描')

        stateLay = qw.QHBoxLayout()
        mainLay.addLayout(stateLay)
        stateLay.addStretch()

        self.scanCleanBtn = qw.QCheckBox(u'扫描到病毒直接清除')
        stateLay.addWidget(self.scanCleanBtn)

        self.scanWalkBtn = qw.QCheckBox(u'包含所有子文件夹')
        self.scanWalkBtn.setChecked(1)
        stateLay.addWidget(self.scanWalkBtn)

        confirmLay = qw.QHBoxLayout()
        mainLay.addLayout(confirmLay)

        self.infoLabel = qw.QLabel('')
        confirmLay.addWidget(self.infoLabel)
        confirmLay.addStretch()

        self.scanBtn = qw.QPushButton(u'    扫描文件夾    ')
        self.scanBtn.setStyleSheet('background-color:rgb(20,196,255); color:white; font-size:16px')
        self.scanBtn.clicked.connect(lambda *args: [self.scanBtn.setEnabled(0), self.scanFuc(), self.scanBtn.setEnabled(1)])
        confirmLay.addWidget(self.scanBtn)
        listLabel = qw.QLabel(u'File List:  (可拖入文件或路径来专杀)')
        mainLay.addWidget(listLabel)

        self.fileList = qw.QListWidget()
        self.fileList.setMinimumWidth(400)
        self.fileList.setAcceptDrops(True)
        self.fileList.setSelectionMode(qw.QAbstractItemView.ExtendedSelection)

        def dragEnterEvent(item, e):
            e.accept()

        def dragMoveEvent(item, e):
            e.accept()

        def dropEvent(item, event):
            event.accept()
            self.refQuery(event)

        self.fileList.dragEnterEvent = lambda e: dragEnterEvent(self.fileList, e)
        self.fileList.dragMoveEvent = lambda e: dragMoveEvent(self.fileList, e)
        self.fileList.dropEvent = lambda e: dropEvent(self.fileList, e)

        mainLay.addWidget(self.fileList)


        cleanLay = qw.QHBoxLayout()
        self.emptyBtn = qw.QPushButton(u'   清除列表中选择文件  ')
        self.emptyBtn.clicked.connect(lambda *args: self.emptyList())
        cleanLay.addWidget(self.emptyBtn)

        mainLay.addLayout(cleanLay)
        cleanLay.addStretch()

        self.cleanBtn = qw.QPushButton(u'      扫描列表并清除      ')
        self.cleanBtn.setStyleSheet('background-color:rgb(20,196,255); color:white; font-size:16px')
        self.cleanBtn.clicked.connect(
            lambda *args: [self.cleanBtn.setEnabled(0), self.scanList(), self.cleanBtn.setEnabled(1)])
        cleanLay.addWidget(self.cleanBtn)

        self.ui.show()
# endregion gui

if __name__ == '__main__':
    #app = qw.QApplication([]) if not qw.QApplication.instance() else None
    VirusOp()
    #app.exec_() if app else None