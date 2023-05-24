#coding:utf-8

_mbPATHTOPSDEXE = ""
_mbCONTIONOUSPATH = True

"""
Author: Buliarca Cristian (buliarca@yahoo.com)
Copyright (C) 2013 Buliarca Cristian
http://buliarca.blog124.fc2.com/

Version: 1.0.0

Function:
    this script takes the selected edges, faces and objects and create a path and
    selection into your Photoshop opend document
    

    To install it you need to copy the script : "edgeToPSSelection.py"
    in maya user scripts directory:
        "c:/Users/_your user name_/Documents/maya/2011/scripts/"

    and use this python command to run it:
try:
    reload(edgeToPSSelection)
except:
    import edgeToPSSelection as edgeToPSSelection

    If you want to have it on your shelf just create a shelf button with the above command.

    Use and/or modify at your own risk.

"""
import os
import subprocess
import time

import tempfile
import maya.cmds as cmds

def progress(step1):
    if(cmds.window(MBScriptWinEdgToPSDProgressWindow, q=True, ex = True) ):
        cmds.progressBar(progressControl, edit=True, progress=step1+1)

def setMaxVal(val):
    if(cmds.window(MBScriptWinEdgToPSDProgressWindow, q=True, ex = True) ):
        if val ==0:
            val = 1
        cmds.progressBar(progressControl, edit=True, maxValue=val)

def delProgWin():
    if(cmds.window(MBScriptWinEdgToPSDProgressWindow, q=True, ex = True) ):
        cmds.deleteUI( MBScriptWinEdgToPSDProgressWindow, window=True )

def changeMessageTo(newText):
    if(cmds.window(MBScriptWinEdgToPSDProgressWindow, q=True, ex = True) ):
        cmds.text(mbText, edit=True, label = newText)  

# end of the progress window functions 

"""
Example which builds a .jsx file, sends it to photoshop and then waits for data to be returned. 
Taken from: http://peterhanshawart.blogspot.ro/2014/01/use-python-to-use-javascript-to-get.html
Thank you Pete Hanshaw
"""
# A Mini Python wrapper for the JS commands...
class PhotoshopJSWrapper(object):
    
    def __init__(self):
        # Get the Photoshop exe path from the registry. 
        # self.PS_key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 
        #                               "SOFTWARE\\Adobe\\Photoshop\\60.0")
        # self.PS_APP = _winreg.QueryValueEx(self.PS_key, 'ApplicationPath')[0] + 'Photoshop.exe'     
        self.PS_APP = _mbPATHTOPSDEXE

        # Get the path to the return file. Create it if it doesn't exist.
        self.return_file = tempfile.gettempdir() + os.sep +'ps_temp_ret.txt'
        
        # Ensure the return file exists...
        with open(self.return_file, 'w') as f:
                f.close()  
            
        # Establish the last time the temp file was modified. We use this to listen for changes. 
        self._last_mod_time = os.path.getmtime(self.return_file)         
        
        # Temp file to store the .jsx commands. 
        self.temp_jsx_file = tempfile.gettempdir()+os.sep+"ps_temp_com.jsx"
        
        # This list is used to hold all the strings which eventually become our .jsx file. 
        self._commands = []    
    
    # This group of helper functions are used to build and execute a jsx file.
    def js_new_command_group(self):
        """clean the _commands list. Called before making a new list of commands"""
        self._commands = []

    def js_execute_command(self):
        """Pass the commands to the subprocess module."""
        self._compile_commands()
        shl = False
        if(os.name == 'posix'):
            self.target = 'open -a "' + self.PS_APP +'"' + " " +  '"' + self.temp_jsx_file + '"'
            shl =True
        else:
            self.target = '"' + self.PS_APP +'"' + " " +  '"' + self.temp_jsx_file + '"'
            shl = False
        ret = subprocess.Popen(self.target, shell=shl) 
    
    def _add_command(self, command):
        """add a command to the commands list"""
        self._command_list.append(command)

    def _compile_commands(self):
        with open(self.temp_jsx_file, "wb") as f:
            for command in self._commands:
                f.write(command)
           
    # These are the strings used to build the .jsx file. 
    def js_create_document(self, varName, w, h, docName):
        """
        Javascript command to create a new document. Returns varname as 
        a reference to the jsx variable. 
        """
        self._mode = " NewDocumentMode.RGB" # Hard set, but easy to add as a python var
        self._init_fill = "DocumentFill.WHITE" # Hard set, but easy to add as a python var
        self._PaR = 1.0 # Hard set, but easy to add as a python var
        self._BpC = "BitsPerChannelType.EIGHT" # Hard set, but easy to add as a python var 
        
        self._com = (
            """
            %s = app.documents.add(%s, %s, 72, "%s", %s, %s, %s, %s);
            """ % (varName, w, h, docName, self._mode, self._init_fill, self._PaR, self._BpC)
            )
        self._commands.append(self._com)
        return varName # Return the name we used for the jsx var, we can use this later in the Python code

    def js_write_Paths( self, theArray):
        """
        Javascript command to create paths from the array points. 
        """
        sbpArr0 = 0
        self._com = ("""
            // Save the current preferences;
            var startRulerUnits = app.preferences.rulerUnits;
            var startTypeUnits = app.preferences.typeUnits;
            var startDisplayDialogs = app.displayDialogs;
            // Set Adobe Photoshop CS6 to use pixels and display no dialogs
            app.preferences.rulerUnits = Units.PIXELS;
            app.preferences.typeUnits = TypeUnits.PIXELS;
            app.displayDialogs = DialogModes.NO;
            try{
                var doc = app.activeDocument;
            }catch(e){
                var doc = app.documents.add(1024, 1024, 72, "Selection from Maya");
            }
            
            var theDocW = app.activeDocument.width;
            var theDocH = app.activeDocument.height;
            """)
        changeMessageTo("creating temporary .jsx file")
        progress(0)
        self.js_write_prepath(sbpArr0)
        qs = 0
        qb  = 0
        for a in range(len(theArray)):# writing each subpath
            isTilled = theArray[a]['tilled']
            self.js_write_subpath(sbpArr0, theArray[a], qs, 0, 0)
            if(isTilled[0] == 1):#x tile
                qs = qs + 1
                self.js_write_subpath(sbpArr0, theArray[a], qs, 0, 1)
            if(isTilled[1] == 1):#y tile
                qs = qs + 1
                self.js_write_subpath(sbpArr0, theArray[a], qs, -1, 0)
                if(isTilled[0] == 1):#x tile
                    qs = qs + 1
                    self.js_write_subpath(sbpArr0, theArray[a], qs, -1, 1)
            if(( qb % 999) == 0 and qs != 0):#because there is a limit of 1000 for subpaths in psd jsx
                self.js_write_postpath(sbpArr0)
                qs = -1
                sbpArr0 = sbpArr0 + 1
                self.js_write_prepath(sbpArr0)
            qb = qb + 1
            qs = qs + 1
            progress((98*qb)/len(theArray))
        self.js_write_postpath(sbpArr0)
        self.js_write_selectPath()
        if(sbpArr0 > 0):
            self.js_write_combineLatsXPaths(sbpArr0)
        self._commands.append(self._com)
        delProgWin()

    def js_write_prepath(self, subPathPFX):
        self._com +=(
        """
            var lineSubPathArray_%(sbpArr)s = new Array();
        """%{'sbpArr':subPathPFX}
        )
    def js_write_subpath(self, subPathPFX, thePthArray, n, offsetX, offsetY):
        pointsArray = thePthArray['pos']
        formArray = thePthArray['form']
        ij = 0
        # [{'curve': u'polyToCurve1', 'pos': [[0.905852198600769, 0.707436203956604, 0.0], [0.8157956004142761, 0.8634187579154968, 0.0]. 'form': 0]}
        uv = thePthArray['bigestPos'][0]
        vv = thePthArray['bigestPos'][1]
        self._com += (
        """
        // ===========================================subpath %(nb)s
        var lineArray_%(sbpArr)s_%(nb)s = new Array();
        posVF = %(vposo)s;
        posV = parseInt(%(vposo)s);
        posUF = %(uposo)s;
        posU = parseInt(%(uposo)s);
        """ % {'nb':n, 'uposo':uv, 'vposo':vv, 'sbpArr':subPathPFX}
        )
        for point in pointsArray:
            self._com += (
            """
                var UVvpos = 1-(%(vpos)s);
                UVvpos = 1 - (%(vpos)s - posV);
                if(posVF < 0){
                    UVvpos = -(%(vpos)s + posV);
                }
                var UVupos = (%(upos)s);
                UVupos = (%(upos)s - posU);
                if(posUF < 0){
                    UVupos = 1 + (%(upos)s - posU);
                }
                var thePxV_%(nb)s = (%(ofsX)s*parseInt(theDocH)) + (parseInt((theDocH * UVvpos ) / 1)) ;
                var thePxH_%(nb)s = (%(ofsY)s*parseInt(theDocW)) + (parseInt((theDocW * UVupos) / 1));
                lineArray_%(sbpArr)s_%(nba)s[%(nb)s] = new PathPointInfo;
                lineArray_%(sbpArr)s_%(nba)s[%(nb)s].kind = PointKind.CORNERPOINT;
                lineArray_%(sbpArr)s_%(nba)s[%(nb)s].anchor = Array(thePxH_%(nb)s, thePxV_%(nb)s);
                lineArray_%(sbpArr)s_%(nba)s[%(nb)s].leftDirection = lineArray_%(sbpArr)s_%(nba)s[%(nb)s].anchor;
                lineArray_%(sbpArr)s_%(nba)s[%(nb)s].rightDirection = lineArray_%(sbpArr)s_%(nba)s[%(nb)s].anchor;
            """% {'nb':ij, 'upos': point[0], 'vpos':point[1], 'nba':n, 'ofsX':offsetX, 'ofsY':offsetY, 'sbpArr':subPathPFX}
            )
            ij = ij + 1
        cld = "true"
        if(formArray == 0):
            cld = "false"
        self._com += (
        """
        lineSubPathArray_%(sbpArr)s[%(nb)s] = new SubPathInfo();
        lineSubPathArray_%(sbpArr)s[%(nb)s].operation = ShapeOperation.SHAPEXOR;
        lineSubPathArray_%(sbpArr)s[%(nb)s].closed = %(closed)s;
        lineSubPathArray_%(sbpArr)s[%(nb)s].entireSubPath = lineArray_%(sbpArr)s_%(nb)s;
        """%{'nb':n, 'closed':cld, 'sbpArr':subPathPFX}
        )
    def js_write_postpath(self, subPathPFX):
        self._com +=(
            """
            var suffix = 0;
            for( var i=0; i<app.activeDocument.pathItems.length; i++){
                var pth = app.activeDocument.pathItems[i].name.toString();
                if( pth.search("BCM_MayaSelectedEdges_") != -1 ){
                    var ss = pth.split("BCM_MayaSelectedEdges_");
                    suffix = parseInt(ss[1]) + 1;
                }
            }
            var myPathItem = app.activeDocument.pathItems.add(("BCM_MayaSelectedEdges_"+suffix), lineSubPathArray_%(sbpArr)s);
            """%{'sbpArr':subPathPFX}
        )
    def js_write_selectPath(self):
        self._com +=(
            """            
            // =======================================================select the new path
                var desc264 = new ActionDescriptor();
                    var ref206 = new ActionReference();
                    ref206.putName( charIDToTypeID( "Path" ), ("BCM_MayaSelectedEdges_"+suffix) );
                desc264.putReference( charIDToTypeID( "null" ), ref206 );
            executeAction( charIDToTypeID( "slct" ), desc264, DialogModes.NO );

            // =======================================================make selection from path
            try{
                var idsetd = charIDToTypeID( "setd" );
                    var desc301 = new ActionDescriptor();
                    var idnull = charIDToTypeID( "null" );
                        var ref242 = new ActionReference();
                        var idChnl = charIDToTypeID( "Chnl" );
                        var idfsel = charIDToTypeID( "fsel" );
                        ref242.putProperty( idChnl, idfsel );
                    desc301.putReference( idnull, ref242 );
                    var idT = charIDToTypeID( "T   " );
                        var ref243 = new ActionReference();
                        var idPath = charIDToTypeID( "Path" );
                        var idOrdn = charIDToTypeID( "Ordn" );
                        var idTrgt = charIDToTypeID( "Trgt" );
                        ref243.putEnumerated( idPath, idOrdn, idTrgt );
                    desc301.putReference( idT, ref243 );
                    var idVrsn = charIDToTypeID( "Vrsn" );
                    desc301.putInteger( idVrsn, 1 );
                    var idvectorMaskParams = stringIDToTypeID( "vectorMaskParams" );
                    desc301.putBoolean( idvectorMaskParams, true );
                executeAction( idsetd, desc301, DialogModes.NO );
            }catch(err){}
            // ======================================================= deselect the path
                var desc269 = new ActionDescriptor();
                    var ref212 = new ActionReference();
                    ref212.putClass( charIDToTypeID( "Path" ) );
                desc269.putReference( charIDToTypeID( "null" ), ref212 );
            executeAction( charIDToTypeID( "Dslc" ), desc269, DialogModes.NO );

            // Reset the application preferences

            preferences.rulerUnits = startRulerUnits;
            preferences.typeUnits = startTypeUnits;
            displayDialogs = startDisplayDialogs;

            """
            )
    def js_write_combineLatsXPaths(self, nbToCombine):
            self._com +=(
                """
                kk = app.activeDocument.pathItems.length -1;
                var stp = kk - %(nbx)s;
                while( kk > stp){
                    tcPthN = app.activeDocument.pathItems[kk].name;
                    ttrgPthN = app.activeDocument.pathItems[stp].name;
                    // =======================================================select the new path
                        var desc264 = new ActionDescriptor();
                            var ref206 = new ActionReference();
                            ref206.putName( charIDToTypeID( "Path" ), tcPthN );
                        desc264.putReference( charIDToTypeID( "null" ), ref206 );
                    executeAction( charIDToTypeID( "slct" ), desc264, DialogModes.NO );
                    // =======================================================copy
                    var idcopy = charIDToTypeID( "copy" );
                    executeAction( idcopy, undefined, DialogModes.NO );
                    // =======================================================select the targhet path
                        var desc264 = new ActionDescriptor();
                            var ref206 = new ActionReference();
                            ref206.putName( charIDToTypeID( "Path" ), ttrgPthN );
                        desc264.putReference( charIDToTypeID( "null" ), ref206 );
                    executeAction( charIDToTypeID( "slct" ), desc264, DialogModes.NO );
                    // =======================================================paste the paths
                    var idpast = charIDToTypeID( "past" );
                    executeAction( idpast, undefined, DialogModes.NO );
                    // =======================================================delete the new path
                    var idDlt = charIDToTypeID( "Dlt " );
                        var desc48 = new ActionDescriptor();
                        var idnull = charIDToTypeID( "null" );
                            var ref42 = new ActionReference();
                            ref42.putName( charIDToTypeID( "Path" ), tcPthN );
                        desc48.putReference( idnull, ref42 );
                    executeAction( idDlt, desc48, DialogModes.NO );


                    kk--;
                }
                """%{'nbx':nbToCombine}
            )

    def js_write_data_out(self, returnRequest):
        """ An example of getting a return value"""
        self._com = (
            """
            var retVal = %s; // Ask for some kind of info about something. 
            
            // Write to temp file. 
            var datFile = new File(Folder.temp+"/ps_temp_ret.txt"); 
            datFile.open("w"); 
            datFile.writeln(String(retVal)); // return the data cast as a string.  
            datFile.close();
            """ % (returnRequest)
        )
        self._commands.append(self._com)
        
        
    def read_return(self):
        """Helper function to wait for PS to write some output for us."""
        # Give time for PS to close the file...
        time.sleep(0.1)        
        
        self._updated = False
        while not self._updated:
            self._this_mod_time = os.path.getmtime(self.return_file)
            if str(self._this_mod_time) != str(self._last_mod_time):
                self._last_mod_time = self._this_mod_time
                self._updated = True
        print "Return Detected"
        
        f = open(self.return_file, "r+")
        self._content = f.readlines()
        f.close()      
        self._ret = []
        for item in self._content:
            self._ret.append(str(item.rstrip()))
        return self._ret
    
    
# An interface to actually call those commands. 
class PhotoshopJSInterface(object):
    
    def __init__(self):
        
        self.psCom = PhotoshopJSWrapper()

    def js_write_Paths(self,theArray):
        self.psCom.js_new_command_group() # Clears the command list. 
        self.psCom.js_write_Paths(theArray)
        self.psCom.js_execute_command()


#functions to be called in Maya that gets the edges info.....    
def getUVPos1( continousPath0 ):
    try:
        if(cmds.window(MBScriptWinEdgToPSDProgressWindow, q=True, ex=True) ):
            delProgWin()
    except :
        pass
    global MBScriptWinEdgToPSDProgressWindow
    MBScriptWinEdgToPSDProgressWindow = cmds.window(title="Exporting edges to paths for Photoshop") #the progress window
    cmds.columnLayout(adjustableColumn=True)
    global mbText
    mbText = cmds.text( label='  Step 1 of 2  ', align='center' )
    global progressControl
    progressControl = cmds.progressBar(maxValue=100, width=400, isInterruptable = True)
    cmds.showWindow( MBScriptWinEdgToPSDProgressWindow )

    retArray = getUVsPos0( continousPath0 )
    return retArray

def getUVsPos0( continousPath ):#this is the function that gets the edges infos....
    import maya.cmds as cmds
    import maya.mel as mel
    import time
    import math
    
    curves = []
    gProg = 0
    progress(0)
    changeMessageTo("Please wait!")

    selSplitOb = splitSelections()
    progress(10)
    gProg = 10

    for objS in selSplitOb:
        #-=================================================
        # these are just for the progress bar
        stepProg0 = 10/len(selSplitOb)#preparing selections
        stepProg1 = 5/len(selSplitOb)#flatten uvs
        stepProg2 = 35/len(selSplitOb)#split edges by shells
        stepProg3 = 20/len(selSplitOb)#create curves
        stepProg4 = 10/len(selSplitOb)#create list to write
        # these are just for the progress bar... end
        #-=================================================

        sel = objS['sel']
        sel = cmds.ls(sel, fl=True)
        selMesh = objS['mesh']
        selTrs = objS['transform']

        #duplicate the object unparent, freeze transforms, transfer the user's selection
        transferSelSet = cmds.sets(sel, name="forTransferSelection")
        selTrsDup = cmds.duplicate(selTrs)
        con2 = cmds.listConnections( transferSelSet, connections=True, type="mesh" )
        myConn2 = ""
        for c in range(len(con2)):
            if(con2[c] == selTrs):
                myConn2 = con2[c - 1]
                break
        plg2 = cmds.listConnections( myConn2 , plugs=True )
        cmds.disconnectAttr (plg2[0], myConn2)
        try:
            cmds.parent(selTrsDup, w=True)
        except:
            pass
        cmds.makeIdentity (selTrsDup, apply=True, t=True, r=True, s=True, n=False)#freeze transform
        sel = cmds.sets(transferSelSet, q=True)
        sel = cmds.ls(sel, fl=True)
        selTrs = selTrsDup
        selTrs = selTrs[0]
        selMesh = cmds.listRelatives(selTrs, s=True)
        selMesh = selMesh[0]
        cmds.delete(transferSelSet)

        selTE = cmds.polyListComponentConversion(sel, ff=True, te=True)#if the selection is face 
        selTE = cmds.ls(selTE, fl=True)
        stp0 = 4
        #-=================================================
        progress(gProg +( stepProg0/stp0))
        gProg = gProg +(stepProg0/stp0)
        #-=================================================
        if( len(selTE) > 0):# this means that there are faces selected
            theSelSet = cmds.sets(sel, name="TempBCMSelectionSet")
            if( objS['allF'] == False):#crashes maya when tryng to delete an polyChipOff done on the entire object
                polyChpOff = cmds.polyChipOff( sel, dup=True , ltz=1)
        else:
            theSelSet = cmds.sets(sel, name="TempBCMSelectionSet")
            toFaces = cmds.polyListComponentConversion(sel, tf=True)
            toFaces = cmds.ls(toFaces, fl=True)
            if( objS['allF'] == False):
                polyChpOff = cmds.polyChipOff( toFaces, dup=True , ltz=1)
        setMembers = cmds.sets(theSelSet, q=True)
        setMembers = cmds.ls(setMembers, fl=True)
        #-=================================================
        progress(gProg +( stepProg0/stp0))
        gProg = gProg +(stepProg0/stp0)
        #-=================================================
        cmds.select(setMembers, r=True)
        if( objS['allF'] == False):
            cmds.select(sel, tgl=True)
        theNewEdg = cmds.ls(sl=True, fl=True)
        theNewEdgSet = cmds.sets(theNewEdg, name="TempBCMNewSet2")
        #-=================================================
        progress(gProg +( stepProg0/stp0))
        gProg = gProg +(stepProg0/stp0)
        #-=================================================
        theNewFaces = cmds.polyListComponentConversion(theNewEdg, tf=True)
        theNewFaces = cmds.ls(theNewFaces, fl=True)
        polySpltVtx = cmds.polySplitVertex(theNewFaces)
        #-=================================================
        progress(gProg +( stepProg0/stp0))
        gProg = gProg +(stepProg0/stp0)
        #-=================================================
        theNewVerts = cmds.polyListComponentConversion(theNewFaces, tv=True)
        theNewVerts = cmds.ls(theNewVerts, fl=True)
        
        gProg = gProg + stepProg0

        changeMessageTo("flattening selected faces to UV's positions")
        #create a plane that will be used to transferAttributes in UV space so the geometry will folow the UVs
        pbXMin = -20
        pbXMax = 20
        pbYMin = -20
        pbYMax = 20

        pbBigX = pbXMax - pbXMin
        if(pbBigX == 0):
            pbBigX = pbXMax
        pbBigY = pbYMax - pbYMin
        if(pbBigY == 0):
            pbBigY = pbYMax
        planeFUV = cmds.polyPlane(w=pbBigX, h=pbBigY, sx=1, sy=1, ax=(0,0,1), cuv=1, ch=True)
        cmds.makeIdentity (planeFUV[0], apply=True, t=True, r=True, s=True, n=False)#freeze transform
        cmds.polyEditUV ((("%s.map[1]" % planeFUV[0]),("%s.map[3]" % planeFUV[0])), v=0, u=pbXMax - 1 ) #xmax
        cmds.polyEditUV ((("%s.map[0]" % planeFUV[0]),("%s.map[2]" % planeFUV[0])), v=0, u=pbXMin) #xmin
        cmds.polyEditUV ((("%s.map[2]" % planeFUV[0]),("%s.map[3]" % planeFUV[0])), u=0, v=pbYMax - 1 ) #ymax
        cmds.polyEditUV ((("%s.map[0]" % planeFUV[0]),("%s.map[1]" % planeFUV[0])), u=0, v=pbYMin ) #ymin
        cUVset = cmds.polyUVSet( selTrs, currentUVSet=True, q=True)
        trnsAtr = cmds.transferAttributes(planeFUV[0], theNewVerts, transferPositions=True,transferNormals=False, transferUVs=False, transferColors=False, sampleSpace=3, sourceUvSpace=cUVset[0], searchMethod=3,  flipUVs=False, colorBorders=True)
        progress(gProg + stepProg1)
        gProg = gProg + stepProg1
        
        polyMrgVtx = cmds.polyMergeVertex( theNewVerts, d=0.0001 )
        polyMrgUV = cmds.polyMergeUV(theNewVerts, d=0.0001)
        
        #cleanup the overlapped uv's
        cmds.select(selTrs, r=True)
        mel.eval('polyCleanupArgList 3 { "0","1","1","0","0","0","0","0","0","1e-005","0","1e-005","0","1e-005","0","-2","1" };')

        if( len(selTE) > 0):# this means that there is a face selected
            theNewEdg2 = cmds.sets(theNewEdgSet, q=True)
            theNewEdg2 = cmds.ls(theNewEdg2, fl=True)
            theNewEdg2 = cmds.polyListComponentConversion(theNewEdg2, te=True)
            theNewEdg2In = cmds.polyListComponentConversion(theNewEdg2, te=True, internal=True)
            theNewEdg2In = cmds.ls(theNewEdg2In, fl=True)
            theNewEdg2 = cmds.ls(theNewEdg2, fl=True)
            cmds.select(theNewEdg2, r=True)
            cmds.selectType(allComponents=False, ocm=True, polymeshEdge=True)
            cmds.polySelectConstraint(mode=2, bo=True, sh=False, cr=False)
            theNewEdg2 = cmds.ls(sl=True, fl=True)
            cmds.polySelectConstraint(mode=0, bo=False, sh=False, cr=False)
            cmds.selectType(allComponents=False, ocm=True, fc=True)
        else:
            theNewEdg2 = cmds.sets(theNewEdgSet, q=True)
            theNewEdg2 = cmds.ls(theNewEdg2, fl=True)
            cmds.select(theNewEdg2, r=True)
        
        if(continousPath == True):
            shellList = []
            iprog2 = 0
            changeMessageTo("separating edges to shells")
            prAll2 = len(theNewEdg2)
            #create a list with shells edges
            while (len(theNewEdg2) > 0):
                myEdg = theNewEdg2[0]
                cmds.select(myEdg,r=True)
                mel.eval("polyConvertToShell;")
                shell = cmds.ls(sl=True, fl=True)
                shellEdg = intersect(theNewEdg2, shell)
                shellList.append(shellEdg)
                progress(gProg+(((prAll2-len(theNewEdg2))*stepProg2)/ prAll2))
                iprog2 = iprog2 + 1
                # cmds.sets(shellEdg, name=("TempBCMShell_%s" %iprog2))#just for debug
                cmds.select(theNewEdg2, r=True)
                cmds.select(shellEdg, tgl=True)
                theNewEdg2 = cmds.ls(sl=True, fl=True)

            gProg = gProg + stepProg2
            
            iprog = 0
            changeMessageTo("creating curves from edges")
            prAll3 = len(shellList)
            for shellE in shellList:
                cmds.select(shellE, r=True)
                cmds.polyToCurve(form=2, degree=1, ch=False)
                theCrv = cmds.ls(sl=True, fl=True)
                cvSPN = cmds.getAttr("%s.spans" %theCrv[0])
                curves.append(theCrv[0])
                zq = 0
                shlLenE = len(shellE)
                if(len(shellE) != cvSPN ):#if there are more edges than the spans of the curve created
                    cmds.select(shellE, r=True)
                    while ( len(shellE) > cvSPN):
                        if(zq > (shlLenE-1)):#just to be sure it won't go forever
                            break
                        jk = 0
                        cvSPN0 = cmds.getAttr("%s.spans" %curves[-1])#get the spans of the last curve created
                        cvFORM = cmds.getAttr("%s.form" %curves[-1])#get the form of the last curve created
                        for i in range(cvSPN0):#for each span of the last created curve
                            # getting the closest 2 verteces for the 2cv's of each span to see wich 
                            # edge was already used to create the curve by creating 2 nodes closestPointOnMesh
                            cvj = ("%s.cv[%s]" %(curves[-1], jk))
                            cvj2 = ("%s.cv[%s]" %(curves[-1], jk + 1))
                            if(cvFORM != 0 and jk == cvSPN0-1):#if the curve is not closed and the loop is at the last itteration
                                cvj2 = ("%s.cv[%s]" %(curves[-1], 0))
                            cvjPos = cmds.xform(cvj, q=True, t=True, ws=True)
                            cvjPos2 = cmds.xform(cvj2, q=True, t=True, ws=True)
                            CPOM = cmds.createNode('closestPointOnMesh')
                            cmds.connectAttr(("%s.worldMesh" %selMesh),("%s.inMesh" %CPOM), f=True)
                            cmds.setAttr(("%s.inPosition " %CPOM), cvjPos[0], cvjPos[1], cvjPos[2])
                            CPOM2 = cmds.createNode('closestPointOnMesh')
                            cmds.connectAttr(("%s.worldMesh" %selMesh),("%s.inMesh" %CPOM2), f=True)
                            cmds.setAttr(("%s.inPosition " %CPOM2), cvjPos2[0], cvjPos2[1], cvjPos2[2])
                            clVtxIDX = cmds.getAttr("%s.closestVertexIndex" %CPOM)# the vertex that alerady has a curve
                            clVtxIDX2 = cmds.getAttr("%s.closestVertexIndex" %CPOM2)# the second vertex that alerady has a curve
                            dirtVtx = ("%s.vtx[%s]" %(selTrs, clVtxIDX))
                            dirtVtx2 = ("%s.vtx[%s]" %(selTrs, clVtxIDX2))
                            dirtEdg = cmds.polyListComponentConversion([dirtVtx, dirtVtx2], te=True, internal=True)
                            dirtEdg = cmds.ls(dirtEdg, fl=True)
                            shellE = removeIntersect(shellE, dirtEdg)
                            cmds.delete((CPOM, CPOM2))
                            # cmds.sets(dirtEdg, name=("TempBCMDirtEdg_%s" %jk))#just for debug
                            jk = jk + 1
                        cmds.select(shellE, r=True)
                        cmds.polyToCurve(form=2, degree=1,ch=False)
                        theCrv = cmds.ls(sl=True, fl=True)
                        cvSPN = cmds.getAttr("%s.spans" %theCrv[0])
                        cvSPN0 = cmds.getAttr("%s.spans" %theCrv[0])
                        curves.append(theCrv[0])
                        zq = zq + 1
                iprog = iprog + 1
                progress(gProg+((stepProg3*iprog)/prAll3))

            cmds.delete((theSelSet,theNewEdgSet))
            cmds.delete(selTrs)
            cmds.delete(planeFUV[0])

            gProg = gProg + stepProg3
            changeMessageTo("creating list with cv's positions")
            thePaths = []
            iprog4 = 0
            prAll4 = len(curves)
            for crv in curves:
                mbForm = cmds.getAttr("%s.form" %crv)
                pthInfo = {'curve':crv,'form':mbForm, 'pos':[], 'tilled':[0,0], 'bigestPos':[0,0]}
                nbSpans = cmds.getAttr("%s.spans" %crv)
                tilledX = 0
                tilledY = 0
                lastPosX = 0
                lastPosY = 0
                bigX = 0
                bigY = 0
                for i in range(nbSpans + 1):
                    cv = ("%s.cv[%s]" %(crv, i))
                    if(mbForm == 2 or mbForm == 1):
                       if i == nbSpans:
                        cv = ("%s.cv[%s]" %(crv, 0))            
                    cvPos = cmds.xform(cv, q=True, t=True)
                    if (i != 0):
                        if(lastPosX != math.ceil(cvPos[0])):
                            tilledX = 1
                        if(lastPosY != math.ceil(cvPos[1])):
                            tilledY = 1
                        if(cvPos[0] > bigX):
                            bigX = cvPos[0]
                        if(cvPos[1] > bigY):
                            bigY = cvPos[1]
                    if( i== 0):
                        bigX = cvPos[0]
                        bigY = cvPos[1]
                    lastPosX = math.ceil(cvPos[0])
                    lastPosY = math.ceil(cvPos[1])
                    pthInfo['pos'].append(cvPos)
                    pthInfo['tilled'] = [tilledX, tilledY]
                    pthInfo['bigestPos'] = [bigX, bigY]
                thePaths.append(pthInfo)
                iprog4 = iprog4 + 1
                progress(gProg+((stepProg4*iprog4)/prAll4))

            
        else:#if you don't want an continous path in PSd...this should be faster but you can't do a selection in PSD
        # you can only use the paths to make a brush stroke
            ii = 0
            thePaths = []
            iprog4 = 0
            prAll4 = len(theNewEdg2)
            for edg in theNewEdg2:
                pthInfo = {'curve':edg,'form':0, 'pos':[], 'tilled':[0,0], 'bigestPos':[0,0]}
                tilledX = 0
                tilledY = 0
                lastPosX = 0
                lastPosY = 0
                bigX = 0
                bigY = 0
                cvs = cmds.polyListComponentConversion(edg, tv=True)
                cvs = cmds.ls(cvs, fl=True)
                cv1Pos = cmds.xform(cvs[0], q=True, t=True)
                cv2Pos = cmds.xform(cvs[1], q=True, t=True)
                if(math.ceil(cv1Pos[0]) != math.ceil(cv2Pos[0])):
                    tilledX = 1
                if(math.ceil(cv1Pos[1]) != math.ceil(cv2Pos[1])):
                    tilledY = 1
                if(cv1Pos[0] > cv2Pos[0]):
                    bigX = cv1Pos[0]
                else:
                    bigX = cv2Pos[0]
                if(cv1Pos[1] > cv2Pos[1]):
                    bigX = cv1Pos[1]
                else:
                    bigX = cv2Pos[1]

                pthInfo['pos'].append(cv1Pos)
                pthInfo['pos'].append(cv2Pos)
                pthInfo['tilled'] = [tilledX, tilledY]
                pthInfo['bigestPos'] = [bigX, bigY]
                thePaths.append(pthInfo)
                ii = ii + 1
                iprog4 = iprog4 + 1
                progress(gProg+(((stepProg2+stepProg3+stepProg4)*iprog4)/prAll4))
            cmds.delete((theSelSet,theNewEdgSet))
            cmds.delete(selTrs)
            cmds.delete(planeFUV[0])
    

    if(len(curves)> 0):
        cmds.delete(curves)
    print thePaths
    if(len(mbSSELECTIE) > 0):
        cmds.select(mbSSELECTIE, r=True)
    if(len(mbSHIGLUMIN) > 0):
        cmds.hilite(mbSHIGLUMIN, r=True)
    return thePaths

def intersect(a, b):
    return list(set(a) & set(b))

def removeIntersect(a, b):
    return list(set(a) - set(b))

def bcmSetAllConnectionsToHasNoEffectTill( myShape, myTransform,  StopNode ):# a script to delete all the nodes to a certain point is not used anymore
    ssh = myShape
    allConnNodes = []
    fc = bcmGetInConnectionPy(ssh, myTransform)
    allConnNodes.append(fc)
    while (fc != ""):
        fc = bcmGetInConnectionPy(fc,myTransform)
        if( fc != ""):
            allConnNodes.append(fc)
    sstop = False
    print (allConnNodes)
    for node in allConnNodes:
        if(sstop == True):
            break
        if(node == StopNode):
            sstop = True
        cmds.delete(node)

def bcmGetInConnectionPy(tobject, myTransform):
    myFirstConn = ""
    if(cmds.nodeType(tobject) == "transferAttributes"):
        tr = cmds.listRelatives(myTransform, shapes=True)
        allConn = cmds.listConnections (tr[-1], p=True )
    else:    
        allConn = cmds.listConnections (tobject, p=True )
        
    for j in range(len(allConn)):
        if(cmds.nodeType(allConn[j]) != "groupParts"):
            temp = allConn[j].split(".")
            if( temp[1] == "outputGeometry" or temp[1] == "output" or temp[1] == "outputGeometry[0]"):
                myFirstConn = temp[0]
    return myFirstConn
def splitSelections():# this function will organize selections by objects
    global mbSSELECTIE
    global mbSHIGLUMIN
    sel = cmds.ls(sl=True, fl=True)
    mbSSELECTIE = sel
    mbSHIGLUMIN = cmds.ls(hl=True, fl=True)
    fc = cmds.filterExpand( ex=True, sm=34 )#face
    ed = cmds.filterExpand( ex=True, sm=32 )#egde
    pg = cmds.filterExpand( ex=True, sm=12 )#polygon

    ob = cmds.ls(sl=True, fl=True, o=True, shapes=True)

    splitedSelectionsSets = []
    fstSet = cmds.sets(em=True, name="firstSelSet")
    invalidSel = True
    if(fc):
        cmds.sets(fc, include = fstSet)
        invalidSel = False
    if(ed):
        cmds.sets(ed, include = fstSet)
        invalidSel = False 
    if(pg):
        invalidSel = False

    if(invalidSel == True):
        changeMessageTo("You need to have edges, polygons or polygon objects selected!")
        raise Exception("You need to have edges, polygons or polygon objects selected!")
    j = 0
    #split subojects per object
    for mesh in ob:
        dupSet = cmds.duplicate(fstSet, inputConnections=True)
        con = cmds.listConnections( dupSet, connections=True, type="mesh" )
        tr = cmds.listRelatives(mesh, parent=True)
        myConn = ""
        for c in range(len(con)):
            if(con[c] == tr[0]):
                myConn = con[c - 1]
                break
        for d in range(len(con)):
            try:
                plg = cmds.listConnections( con[d] , plugs=True )
                if(myConn != con[d]):
                    cmds.disconnectAttr (plg[0], con[d])
            except:
                pass
        fcc = cmds.sets(dupSet, q=True)
        ss = {'mesh':mesh, 'transform':tr[0], 'sel':fcc, 'allF':False}
        splitedSelectionsSets.append(ss)
        cmds.delete(dupSet)
    
    #split objects
    if(pg):
        for ot in pg:
            shp = cmds.listRelatives(ot, shapes=True)
            allFc = cmds.polyEvaluate(ot, face=True)
            fcx = ("%s.f[0:%s]" %(ot, allFc-1))
            ss1 = {'mesh':shp[0], 'transform':ot, 'sel':fcx, 'allF':True}
            splitedSelectionsSets.append(ss1)

    cmds.delete(fstSet)
    return splitedSelectionsSets

def edgToPSD( contPath, PSDPath ):
    PS = PhotoshopJSInterface()
    PS.psCom.PS_APP = PSDPath
    PS.js_write_Paths( getUVPos1(contPath))

def edgToPSDUI():#the UI for the script
    global _mbPATHTOPSDEXE
    global _mbCONTIONOUSPATH

    def mbPsdBrowserSSS(*args):

        filename = cmds.fileDialog2( dialogStyle=1, caption="Browse for Photoshop executable", okCaption="Open",returnFilter=True,fileMode= 1  )
        pathToPsd = filename[0]
        myPyFile = os.path.realpath(__file__)
        inputPyFile = open(myPyFile, "r")
        myPyScriptStr = ""
        ln = 1
        _mbPATHTOPSDEXE = pathToPsd
        for line in inputPyFile:
            if (ln == 1):#rewrite this file's line 828
                line = ("_mbPATHTOPSDEXE = \"%s\"\n" %pathToPsd)
            myPyScriptStr += line
            ln = ln + 1
        inputPyFile.close()
        inputPyFile2 = open(myPyFile, "w")
        inputPyFile2.write(myPyScriptStr)
        inputPyFile2.close()
        cmds.textField(mbStr, edit=True, text=pathToPsd)

    def mbContinousPathSSS(*args):
        myPyFile = os.path.realpath(__file__)
        inputPyFile = open(myPyFile, "r")
        myPyScriptStr = ""
        mbChkValue = cmds.checkBox(mbChk, q=True, v=True)
        _mbCONTIONOUSPATH = mbChkValue
        ln = 1
        for line in inputPyFile:
            if (ln == 2):#rewrite this file's line 828
                line = ("_mbCONTIONOUSPATH = %s\n" %mbChkValue)
            myPyScriptStr += line
            ln = ln + 1
        inputPyFile.close()
        inputPyFile2 = open(myPyFile, "w")
        inputPyFile2.write(myPyScriptStr)
        inputPyFile2.close()
    def execEdgeToPSD(*args):
        vv = (cmds.checkBox(mbChk, q=True, v=True))
        psdv = (cmds.textField(mbStr, q=True, text=True))
        if(psdv == ""):
            mbPsdBrowserSSS()
            psdv = (cmds.textField(mbStr, q=True, text=True))
            edgToPSD(vv, psdv)
        else:
            edgToPSD(vv, psdv)
            # try:
            #     edgToPSD(vv, psdv)
            # except:
            #    print ("Maybe the Photoshop path you specifiyed doesn't exist anymore") 
    try:
        if(cmds.window(MBScriptWinEdgToPSDUi, q=True, ex=True) ):
            cmds.deleteUI( MBScriptWinEdgToPSDUi, window=True )
    except :
        pass

    MBScriptWinEdgToPSDUi = cmds.window(title="Exporting edges to paths for Photoshop options")
    cmds.columnLayout(adjustableColumn=True)
    mbForm = cmds.formLayout(numberOfDivisions = 100)
    mbText = cmds.text( label='  Photoshop path: ', align='left' )
    mbStr = cmds.textField(editable=True, text=_mbPATHTOPSDEXE)
    mbButton = cmds.button( label='Browse', command=mbPsdBrowserSSS)
    mbChkLb = cmds.text( label='  Continous Path: ', align='left' )
    mbChk = cmds.checkBox( v=_mbCONTIONOUSPATH, l='', changeCommand=mbContinousPathSSS)
    mbOkButton = cmds.button( label='Apply', height=40, command = execEdgeToPSD)
    cmds.formLayout( mbForm, edit=True, 
                    attachForm=[
                        (mbText, 'top', 10), 
                        (mbText, 'left', 5), 
                        (mbStr, 'top', 5), 
                        (mbButton, 'top', 5), 
                        (mbButton, 'right', 5),
                        (mbChkLb, 'left', 90),
                        (mbOkButton, 'bottom', 5), 
                        (mbOkButton, 'left', 5), 
                        (mbOkButton, 'right', 5),
                        ],
                    attachControl=[
                        (mbStr, 'left', 5, mbText), 
                        (mbStr, 'right', 5, mbButton),
                        (mbChkLb, 'top', 23, mbStr),
                        (mbChk, 'top', 20, mbStr),
                        (mbChk, 'right', 5, mbButton),
                        (mbOkButton, 'top', 10, mbChk), 
                        (mbOkButton, 'bottom', 10, mbChk),
                        ] 
                    )


    cmds.showWindow( MBScriptWinEdgToPSDUi )

edgToPSDUI()
