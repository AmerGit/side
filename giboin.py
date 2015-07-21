from maya import OpenMaya, cmds

import random

def getPoints(percentage):
    mSelectionList = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getActiveSelectionList(mSelectionList)
    # get dependency node to item
    dagPath = OpenMaya.MDagPath()
    mSelectionList.getDagPath(0, dagPath)
    # get shapeNode
    dagPath.extendToShape()
    # create function set to operate on it
    meshFunctionSet = OpenMaya.MFnMesh(dagPath.node())
    # get limit
    vertexCount = meshFunctionSet.numVertices()
    limit = vertexCount*percentage/100
    
    
    randomList = random.sample(range(vertexCount), limit)
    for item in randomList:
        cmds.select('%s.vtx[%d]'%(dagPath, item)
    
getPoints(20)
