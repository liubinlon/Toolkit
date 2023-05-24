###############################################################################
# Name:
#   NormalEditTool
#
#
# Author:
#   Bread   QQ:21788985
#
###############################################################################

# coding: utf-8
import maya.cmds as mc
import maya.OpenMaya as om

qtVersion = mc.about(qtVersion=True)

if qtVersion.startswith("4") or type(qtVersion) not in [str,unicode]:
    from PySide import QtGui
    from PySide import QtCore
    from PySide import QtWidgets
    from PySide import QtUiTools
    
else:
    from PySide2 import QtGui
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    from PySide2 import QtUiTools
    
uifile_path = mc.moduleInfo(mn='MS_Toolkit',p=True)+"/tools/MSTools/MST_DATA/scripts/NormalEditTool_CN.ui"

def loadui(uifile_path):
    uifile = QtCore.QFile(uifile_path)
    print uifile
    uifile.open(QtCore.QFile.ReadOnly)
    uiWindow = QtUiTools.QUiLoader().load(uifile)
    uifile.close()
    print "load ui"
    return uiWindow
def launcher():
    if mc.window("NormalEditTool",e=1,ex=1):
       mc.deleteUI("NormalEditTool",window=True)

class MainWindow():
    
    def __init__(self,parent = None):
        self.ui = loadui(uifile_path)
        #�����ڷ������ϲ�
        self.ui.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.ui.show()
        
        #button
        self.ui.ShowVertexNoraml.clicked.connect(self.ShowVertexNoraml)
        self.ui.LockNoraml.clicked.connect(self.LockNoraml)
        self.ui.UnlockNormal.clicked.connect(self.UnlockNormal)
        self.ui.HardEdge.clicked.connect(self.HardEdge)
        self.ui.SoftEdge.clicked.connect(self.SoftEdge)
        self.ui.ModelTransmit.clicked.connect(self.ModelTransmit)
        self.ui.VertexTransfer.clicked.connect(self.VertexTransfer)
        self.ui.ClearHistory.clicked.connect(self.ClearHistory)
        self.ui.sommthbush.clicked.connect(self.sommthbush)
        self.ui.noramlEdit.clicked.connect(self.noramlEdit)
        self.ui.matchingFace.clicked.connect(self.matchingFace)
        self.ui.matchingFaceS.clicked.connect(self.matchingFaceS)
        self.ui.copyNormal.clicked.connect(self.copyNormal)
        self.ui.pasteNormal.clicked.connect(self.pasteNormal)
        self.ui.averageNormal.clicked.connect(self.averageNormal)
        self.ui.Dot.clicked.connect(self.Dot)
        self.ui.LocatorDot.clicked.connect(self.LocatorDot)
        self.ui.LocatorDot_2.clicked.connect(self.LocatorDot_2)
     
     
        
        self.ui.up.clicked.connect(self.up)
        self.ui.down.clicked.connect(self.down)
        self.ui.left.clicked.connect(self.left)
        self.ui.right.clicked.connect(self.right)
        self.ui.front.clicked.connect(self.front)
        self.ui.back.clicked.connect(self.back)
        
        self.ui.addX1.clicked.connect(self.addX1)
        self.ui.addX5.clicked.connect(self.addX5)
        self.ui.addY1.clicked.connect(self.addY1)
        self.ui.addY5.clicked.connect(self.addY5)
        self.ui.addZ1.clicked.connect(self.addZ1)
        self.ui.addZ5.clicked.connect(self.addZ5)
        self.ui.subX1.clicked.connect(self.subX1)
        self.ui.subX5.clicked.connect(self.subX5)
        self.ui.subY1.clicked.connect(self.subY1)
        self.ui.subY5.clicked.connect(self.subY5)
        self.ui.subZ1.clicked.connect(self.subZ1)
        self.ui.subZ5.clicked.connect(self.subZ5)
        self.ui.mulX1.clicked.connect(self.mulX1)
        self.ui.mulX5.clicked.connect(self.mulX5)
        self.ui.mulY1.clicked.connect(self.mulY1)
        self.ui.mulY5.clicked.connect(self.mulY5)
        self.ui.mulZ1.clicked.connect(self.mulZ1)
        self.ui.mulZ5.clicked.connect(self.mulZ5)
        
        self.ui.cLocator.clicked.connect(self.cLocator)
           
        
        #value
        
        #self.ui.soomthvalue.valueChanged.connect(self.soomthvalue)
        #self.ui.dotvalue.valueChanged.connect(self.dotvalue)
       
        
       

        
    def ShowVertexNoraml(self):
        mc.ToggleVertexNormalDisplay()
        
    def LockNoraml(self):
        mc.polyNormalPerVertex (fn=1)
        
    def UnlockNormal(self):
        mc.polyNormalPerVertex (ufn=1)        
        
    def SoftEdge(self):
        selection = mc.ls(sl=True)  
        mc.polySoftEdge(a=180,ch=1 ,name= "selection")
    
    def HardEdge(self):
        selection = mc.ls(sl=True)  
        mc.polySoftEdge(a=0,ch=1 ,name= "selection")     
           
    def ModelTransmit(self):
        selection = mc.ls(sl=1)
        mc.transferAttributes(selection[0],selection[1],transferNormals=1)
        #mc.polyUnite( selection[0] ,selection[1],n = 'result')
        
    def VertexTransfer(self):
        selection = mc.ls(sl=1)
        mc.transferAttributes(selection[0],selection[1],transferPositions=1)
        
    def ClearHistory(self):
        mc.DeleteHistory
        mc.delete(ch=1)
        
    def sommthbush(self):
        mc.SetMeshSmoothTool()
      
        
    def noramlEdit(self):
        mc.PolygonNormalEditTool()        

    def matchingFace(self):
        mc.polySetToFaceNormal(setUserNormal=True)

    def matchingFaceS(self):
        faces = mc.filterExpand(sm=34, ex=True)
        
        verts = mc.ls((cmds.polyListComponentConversion(faces, ff=True, tv=True)), flatten=True)
        
        normals = [[], [], []]
        
        
        for v in verts:
        
            conFaces = mc.ls(cmds.polyListComponentConversion(v, fv=True, tf=True), flatten=True)
        
            shaFaces = list(set(conFaces).intersection(set(faces)))
        
            faceNorm = mc.polyInfo(shaFaces, fn=True)
        
        
            for normal in faceNorm:
        
        	    label, vertex, x, y, z = normal.split()
        
        	    normals[0].append(float(x))
        
        	    normals[1].append(float(y))
        
        	    normals[2].append(float(z))
        
        
            x_avg = (sum(normals[0]) / len(shaFaces))
        
            y_avg = (sum(normals[1]) / len(shaFaces))
        
            z_avg = (sum(normals[2]) / len(shaFaces))
        
        
            mc.select(v)
        
            mc.polyNormalPerVertex(xyz = (x_avg, y_avg, z_avg))
        
        
            normals[:] = [[], [], []]
        
        
        mc.select(cl=True)

        
    def copyNormal(self):
        vertex =mc.ls(sl=1,fl=1)
        global vertexNormal
        vertexNormal=mc.polyNormalPerVertex(q=1, xyz=1)

    def pasteNormal(self):
        vertex =mc.ls(sl=1,fl=1)
        mc.polyNormalPerVertex(xyz=(vertexNormal[0],vertexNormal[1],vertexNormal[2]))
        

    def averageNormal(self):
        soomv = (self.ui.soomthvalue.value()+1)/10.0 
        
        mc.polyAverageNormal(prenormalize=1,allowZeroNormal=0,postnormalize=1,distance=soomv,replaceNormalXYZ=( 1 ,0 ,0))     
        
    def up(self):
        mc.polyNormalPerVertex(xyz=(0,1,0)) 
              
    def down(self):
        mc.polyNormalPerVertex(xyz=(0,-1,0))       

    def left(self):
        mc.polyNormalPerVertex(xyz=(-1,0,0)) 
        
    def right(self):
        mc.polyNormalPerVertex(xyz=(1,0,0))       
        
    def front(self):
        mc.polyNormalPerVertex(xyz=(0,0,1))       
    
    def back(self):
        mc.polyNormalPerVertex(xyz=(0,0,-1))   
        
    def addX1(self):
        mc.polyNormalPerVertex (fn=1),mc.polyNormalPerVertex( rel=True, x=.1 )        
        
    def addX5(self):
        mc.polyNormalPerVertex (fn=1),mc.polyNormalPerVertex( rel=True, x=.5 )        
        
    def subX1(self):
        mc.polyNormalPerVertex (fn=1),mc.polyNormalPerVertex( rel=True, x=-.1 )        
        
    def subX5(self):
        mc.polyNormalPerVertex (fn=1),mc.polyNormalPerVertex( rel=True, x=-.5 )
        
    def addY1(self):
        mc.polyNormalPerVertex (fn=1),mc.polyNormalPerVertex( rel=True, y=.1 )       
        
    def addY5(self):
        mc.polyNormalPerVertex (fn=1),mc.polyNormalPerVertex( rel=True, y=.5 )       
                
    def subY1(self):
        mc.polyNormalPerVertex (fn=1),mc.polyNormalPerVertex( rel=True, y=-.1 )     
        
    def subY5(self):
        mc.polyNormalPerVertex (fn=1),mc.polyNormalPerVertex( rel=True, y=-.5)     
        
    def addZ1(self):
        mc.polyNormalPerVertex (fn=1),mc.polyNormalPerVertex( rel=True, z=.1 )     
        
    def addZ5(self):
        mc.polyNormalPerVertex (fn=1),mc.polyNormalPerVertex( rel=True, z=.5 )   
        
    def subZ1(self):
        mc.polyNormalPerVertex (fn=1),mc.polyNormalPerVertex( rel=True, z=-.1 )        
        
    def subZ5(self):
        mc.polyNormalPerVertex (fn=1),mc.polyNormalPerVertex( rel=True, z=-.5 ) 
        
        
    def mulX1(self):  
    
        for i in mc.ls(sl=1,fl=1):
            normals = mc.polyNormalPerVertex(i,q=1, xyz=1)
            normals[0]*=1.1
            normals[1]
            normals[2]
            mc.polyNormalPerVertex(i,xyz=(normals[0],normals[1],normals[2]))
                    
    def mulX5(self):  
    
        for i in mc.ls(sl=1,fl=1):
            normals = mc.polyNormalPerVertex(i,q=1, xyz=1)
            normals[0]*=1.5
            normals[1]
            normals[2]
            mc.polyNormalPerVertex(i,xyz=(normals[0],normals[1],normals[2]))        
        
    def mulY1(self):  
    
        for i in mc.ls(sl=1,fl=1):
            normals = mc.polyNormalPerVertex(i,q=1, xyz=1)
            normals[0]
            normals[1]*=1.1
            normals[2]
            mc.polyNormalPerVertex(i,xyz=(normals[0],normals[1],normals[2]))
                    
    def mulY5(self):  
    
        for i in mc.ls(sl=1,fl=1):
            normals = mc.polyNormalPerVertex(i,q=1, xyz=1)
            normals[0]
            normals[1]*=1.5
            normals[2]
            mc.polyNormalPerVertex(i,xyz=(normals[0],normals[1],normals[2]))           
        
    def mulZ1(self):  
    
        for i in mc.ls(sl=1,fl=1):
            normals = mc.polyNormalPerVertex(i,q=1, xyz=1)
            normals[0]
            normals[1]
            normals[2]*=1.1
            mc.polyNormalPerVertex(i,xyz=(normals[0],normals[1],normals[2]))
                    
    def mulZ5(self):  
    
        for i in mc.ls(sl=1,fl=1):
            normals = mc.polyNormalPerVertex(i,q=1, xyz=1)
            normals[0]
            normals[1]
            normals[2]*=1.5
            mc.polyNormalPerVertex(i,xyz=(normals[0],normals[1],normals[2]))           
                     
        
    def cLocator(self):
        
        mc.spaceLocator(n = "Create")
        
        

   
        
        

        
    def Dot(self):
        
        selList = om.MSelectionList()
        selList.add(mc.ls(sl=1,fl=1)[0])
        dagpath = om.MDagPath()
        
        selList.getDagPath(0, dagpath)
        
        mesh = om.MFnMesh(dagpath)
        
        points = om.MFloatPointArray()
        
        mesh.getPoints(points, 4)
        
        center_point = om.MFloatPoint()
        
        for p in range(points.length()):
            center_point.x += points[p].x
            center_point.y += points[p].y
            center_point.z += points[p].z
        
        center_point.x /= points.length()    
        center_point.y /= points.length()
        center_point.z /= points.length()
        
        normal_new = om.MFloatVectorArray()
        
        it_vertex = om.MItMeshVertex(dagpath)
        point_list = mc.filterExpand(sm=31)
        index_list= []
        for point in point_list:
            index = int(point[point.find(".vtx[")+5:-1])
            index_list.append(index)    
        while not it_vertex.isDone():
            
            if it_vertex.index() in index_list:
                position_vertex = it_vertex.position(4)
                mesh.setVertexNormal(om.MVector((position_vertex.x-center_point.x),(position_vertex.y-center_point.y), (position_vertex.z-center_point.z)), it_vertex.index(), 4)
     
            it_vertex.next()
        mesh.updateSurface()
           
    def LocatorDot(self , loc="Create"):
        
        num = (self.ui.dotvalue.value()+1)/100.0
        msel = om.MSelectionList()
        
        om.MGlobal.getActiveSelectionList(msel)  
        
        dagpath = om.MDagPath()
        
        msel.getDagPath(0, dagpath)
        
        mesh = om.MFnMesh(dagpath)
        
        it_vertex = om.MItMeshVertex(dagpath)
        point_to = om.MPoint()
        point_list = mc.filterExpand(sm=31)
        index_list= []
        for point in point_list:
            index = int(point[point.find(".vtx[")+5:-1])
            index_list.append(index)   
             
        print num
        point_to.x, point_to.y, point_to.z = mc.pointPosition( loc, w=1 )
               
        while not it_vertex.isDone():
            if it_vertex.index() in index_list:
                point_vertex = it_vertex.position(4)
                target = om.MVector(point_to - point_vertex)
                target.normalize()
                normal_vertex = om.MVector()
                it_vertex.getNormal(normal_vertex, om.MSpace.kWorld)
                normal_vertex.normalize()
                vector_change = om.MVector(-target - normal_vertex)
                normal_new = normal_vertex + om.MVector(vector_change.x*num, vector_change.y*num, vector_change.z*num)
                mesh.setVertexNormal(normal_new, it_vertex.index(), 4)
            it_vertex.next()    
        mesh.updateSurface() 
              
       
    def LocatorDot_2( self,loc="Create"):
        num = (self.ui.dotvalue.value()+1)/100.0
        
        msel = om.MSelectionList()
        
        om.MGlobal.getActiveSelectionList(msel)  
        
        dagpath = om.MDagPath()
        
        msel.getDagPath(0, dagpath)
        
        mesh = om.MFnMesh(dagpath)
        
        it_vertex = om.MItMeshVertex(dagpath)
        point_to = om.MPoint()
        point_list = mc.filterExpand(sm=31)
        index_list= []
        for point in point_list:
            index = int(point[point.find(".vtx[")+5:-1])
            index_list.append(index)   
        
        point_to.x, point_to.y, point_to.z = mc.pointPosition( loc, w=1 )
        
        while not it_vertex.isDone():
            if it_vertex.index() in index_list:
                point_vertex = it_vertex.position(4)
                target = om.MVector(point_to - point_vertex)
                target.normalize()
                normal_vertex = om.MVector()
                it_vertex.getNormal(normal_vertex, om.MSpace.kWorld)
                normal_vertex.normalize()
                vector_change = om.MVector(target - normal_vertex)
                normal_new = normal_vertex + om.MVector(vector_change.x*num, vector_change.y*num, vector_change.z*num)
                mesh.setVertexNormal(normal_new, it_vertex.index(), 4)
            it_vertex.next()    
        mesh.updateSurface()        
             
if __name__ == "__main__":
    mainWindow = MainWindow()

