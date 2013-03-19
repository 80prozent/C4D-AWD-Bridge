# functions that will run inside the background-worker-thread
# more-functions for mesh-converting 

import c4d
from c4d import documents

from awdexporter import ids
from awdexporter import classesAWDBlocks
    
def prepareSubmeshIndexe(meshBlock):
    unselectedIndexe=[]   
    count=len(meshBlock.copiedMesh.GetAllPolygons()) 
    hasUnselectedPolys=False
    for index in xrange(count): 
        foundIndex=0
        subMeshCount=1
        while subMeshCount <len(meshBlock.saveSubMeshes):
            if foundIndex==1:
                meshBlock.saveSubMeshes[subMeshCount].selectionIndexe[index]=0
            if foundIndex==0:
                if meshBlock.saveSubMeshes[subMeshCount].selectionIndexe[index]==1:
                    foundIndex=1
                    unselectedIndexe.append(0)
            subMeshCount+=1
        if foundIndex==0:
            hasUnselectedPolys=True
            unselectedIndexe.append(1) 
    meshBlock.saveSubMeshes[0].selectionIndexe=unselectedIndexe
    if hasUnselectedPolys==False:
        #print "delete first submesh"
        meshBlock.saveSubMeshes.pop(0)
    return   
           
#checks if a vert/uv - combination allready exists in the uniquePool or in the uniquePoolMorphed of the given Submesh.
def buildSharedPoint(faceStyle,meshBlock,curMesh,curPoint,curUV,curSubMesh,pointNr,normal,normalf,anglelimit,useAngle,isEdgeBreak):
                    
        
    checkerstring=str(curPoint)
    if curUV!=None:
        checkerstring+="#"+str(curUV)
    checkerstring2=checkerstring+str(0)
    pointIndex=-1
    pointMorphedIndex=-1
            
    if meshBlock.pointsUsed[pointNr]==True:#if the c4d point hasent been used yet, we take a shortcut and can skip all the next...
        if isEdgeBreak==1:# the point is on a edge break, so we need do make shure its parsed as a new point
            phongbreaknr1=0
            allkeyslength=len(curSubMesh.uniquePoolDict)
            while phongbreaknr1<allkeyslength:
                checkerstring2=checkerstring+str(phongbreaknr1)
                pointIndex2=curSubMesh.uniquePoolDict.get(checkerstring2,-1)  
                if pointIndex2 ==-1:
                    phongbreaknr=phongbreaknr1
                    break
                phongbreaknr1+=1
                    
        if isEdgeBreak==0:#the point is not on a edge break, so we need to find all points that are sharing this position and calculate the angle between there face normals.  
            pointIndex=curSubMesh.uniquePoolDict.get(checkerstring2,-1)  
            if pointIndex>=0:
                if useAngle==True:
                    angle=c4d.utils.VectorAngle(curSubMesh.faceNormal[pointIndex].GetNormalized(), normalf.GetNormalized())
                    if angle>=anglelimit:
                        allkeyslength=len(curSubMesh.uniquePoolDict)
                        phongbreaknr=1
                        while phongbreaknr<allkeyslength:
                            checkerstring2=checkerstring+str(phongbreaknr)
                            pointIndex=curSubMesh.uniquePoolDict.get(checkerstring2,-1)  
                            if pointIndex ==-1:
                                break
                            if pointIndex >= 0:
                                if useAngle==True:
                                    angle=c4d.utils.VectorAngle(curSubMesh.faceNormal[pointIndex].GetNormalized(), normalf.GetNormalized())
                                    if angle<anglelimit:
                                       phongbreaknr=allkeyslength
                            phongbreaknr+=1
                                        
                                        
                                    
        #if pointIndex==-1:
        #    if checkerstring in curSubMesh.uniquePoolMorphed:
        #        pointMorphedIndex=curSubMesh.uniquePoolMorphed.index(checkerstring)   
                 
    #if pointMorphedIndex>=0:
    #    curSubMesh.indexBuffer.append(pointIndex) 
    if pointIndex>=0:
        if str(faceStyle)=="tri":
            curSubMesh.indexBuffer.append(pointIndex)        
        if str(faceStyle)=="quad":
            curSubMesh.quadBuffer.append(pointIndex)
        #curSubMesh.indexBufferMorphed.append("p")   
                
    if pointIndex==-1 and pointMorphedIndex==-1:
        meshBlock.pointsUsed[pointNr]=True   
        buildPoint(faceStyle,meshBlock,curMesh,curSubMesh,curPoint,pointNr,curUV,normal,normalf,checkerstring2)

                         
def buildPoint(faceStyle,meshBlock,curMesh,curSubMesh,curPoint,pointNr,curUv,curNormal=None,curNormalf=None,checkerstring=None):
                     
    ismorph=False
    #morphCounter=0
    #while morphCounter<len(morphes):
        #morphedPoint=morphes[morphCounter].morphedPoints[pointNr]
        #if curPoint.x!=morphedPoint.x or curPoint.y!=morphedPoint.y or curPoint.z!=morphedPoint.z:
            #relativeMorph=str(len(curSubMesh.vertexBufferMorphed))+"#"
            #relativeMorph+=str(curPoint.x-morphedPoint.x)+"#"
            #relativeMorph+=str(curPoint.y-morphedPoint.y)+"#"
            #relativeMorph+=str(curPoint.z-morphedPoint.z)
            #curSubMesh.morphs[morphCounter][2]=True
            #curSubMesh.morphs[morphCounter][0].append(relativeMorph)
            #ismorph=True
        #morphCounter+=1
    weights=None
    joints=None
    if curMesh.GetTag(c4d.Tweights):#if the mesh is skinned:
        jointcounter=0
        weights=[]  
        joints=[] 
        jointCount=curMesh.GetTag(c4d.Tweights).GetJointCount()
        while jointcounter<jointCount:   
            newWeight=curMesh.GetTag(c4d.Tweights).GetWeight(jointcounter,pointNr)
            if newWeight>0:
                newIndex=meshBlock.jointTranslater[jointcounter]
                if newIndex>=0:
                    weights.append(newWeight)
                    joints.append(newIndex) 
                ismorph=False
            jointcounter+=1      
    if ismorph==False:
        if str(faceStyle)=="tri":
            curSubMesh.indexBuffer.append(len(curSubMesh.vertexBuffer))        
        if str(faceStyle)=="quad":
            curSubMesh.quadBuffer.append(len(curSubMesh.vertexBuffer))

        if checkerstring is not None:
            curSubMesh.uniquePoolDict[checkerstring]=len(curSubMesh.vertexBuffer)
        #curSubMesh.indexBufferMorphed.append("p") 
        curSubMesh.vertexBuffer.append(curPoint) 
        #curSubMesh.sharedvertexBuffer.append(-1) faceStyle
        if curUv is not None:
            curSubMesh.uvBuffer.append(curUv)
        if curNormal is not None:
            curSubMesh.normalBuffer.append(curNormal)
        if curNormalf is not None:
            curSubMesh.faceNormal.append(curNormalf)
        if weights is not None:
            curSubMesh.weightsBuffer.append(weights)
        if joints!= None:
            curSubMesh.jointidxBuffer.append(joints)



"""

        if ismorph==True:
            curSubMesh.indexBuffer.append(len(curSubMesh.vertexBufferMorphed))
            curSubMesh.indexBufferMorphed.append("m")  
            curSubMesh.vertexBufferMorphed.append(curPoint) 
            curSubMesh.sharedvertexBufferMorphed.append(-1) 
            if curUV != None:
                curSubMesh.uvBufferMorphed.append(curUV)
            curSubMesh.uniquePoolMorphed.append(checkerstring)
            curSubMesh.weightsBuffer.append(weights)
            curSubMesh.jointidxBuffer.append(joints) 
"""  
                        

# this is the main - mesh-parsing function....            
def collectSubmeshData(meshBlock,exportData,workerthreat):
    usePhong=False
    usePhongAngle=False
    useEdgeBreaks=False
    edgebreaks=None
    phoneAngle=-1
    normalData=meshBlock.copiedMesh.CreatePhongNormals()
    normalCounter=0
    phongTag=meshBlock.copiedMesh.GetTag(c4d.Tphong)
    if phongTag is not None:
        usePhong=True
        usePhongAngle=phongTag[c4d.PHONGTAG_PHONG_ANGLELIMIT]
        useEdgeBreaks=phongTag[c4d.PHONGTAG_PHONG_USEEDGES]
        phoneAngle=phongTag[c4d.PHONGTAG_PHONG_ANGLE]
        if useEdgeBreaks==True:
            edgebreaks=meshBlock.copiedMesh.GetPhongBreak()
        
    allOldPoints=meshBlock.copiedMesh.GetAllPoints()
    meshBlock.pointsUsed=[]
    for point in allOldPoints:
        meshBlock.pointsUsed.append(False)
    polys=meshBlock.copiedMesh.GetAllPolygons()
    count=len(polys)
    count2=float(10/float(count))
    for faceIndex in xrange(count):                                     # iterate trough all polygons 
        if workerthreat.TestBreak():                                        # if the user cancelled the export, 
            return                                                              # we return
        exportData.subStatus=float(float(faceIndex)/float(count))           # used to update the progress bar
        exportData.allStatus+=count2                                        # used to update the progress bar
        oldpoints=polys[faceIndex]                                          # store the original point-indicies
        uvTag=meshBlock.copiedMesh.GetTag(c4d.Tuvw)                         # get the first UV-Tag applied to the mesh
        if uvTag is not None:                                               # if a UV-Tag is found,  
            uv = uvTag.GetSlow(faceIndex)                                       # we get the UVs for the Polygon and store them in "uv"
        subcount=0
        for subcount in xrange(len(meshBlock.saveSubMeshes)):            
            if meshBlock.saveSubMeshes[subcount].selectionIndexe[faceIndex]==1:                   
                uva=uvb=uvc=uvd=None
                if meshBlock.copiedMesh.GetTag(5671):
                    uva=uv["a"]
                    uvb=uv["b"]
                    uvc=uv["c"]
                    uvd=uv["d"]              
                normala=normalb=normalc=normald=None
                
                faceStyle="tri"
                if oldpoints.c!=oldpoints.d:
                    if (str(allOldPoints[oldpoints.c]))!=(str(allOldPoints[oldpoints.d])):
                        faceStyle="quad"
                    if (str(allOldPoints[oldpoints.c]))==(str(allOldPoints[oldpoints.d])):
                        if meshBlock.copiedMesh.GetTag(5671):
                            if str(uvc)!=str(uvd):
                                faceStyle="quad"
                                
                            
                if usePhong==True:
                    normalf=None
                    if usePhongAngle==True:
                        edge1=allOldPoints[oldpoints.a].__sub__(allOldPoints[oldpoints.c])
                        edge2=allOldPoints[oldpoints.b].__sub__(allOldPoints[oldpoints.d])
                        normalf=edge1.Cross(edge2)
                    normala=normalData[normalCounter]
                    normalCounter+=1
                    normalb=normalData[normalCounter]
                    normalCounter+=1
                    normalc=normalData[normalCounter]
                    normalCounter+=1
                    normald=normalData[normalCounter]
                    normalCounter+=1
                                   
                    isEdgeBreakA=isEdgeBreakB=isEdgeBreakC=isEdgeBreakD=isEdgeBreakD=isEdgeBreakA1=isEdgeBreakB1=isEdgeBreakC1=isEdgeBreakD1=0
                    if edgebreaks!=None:
                        isEdgeBreakA1=edgebreaks.IsSelected(4*faceIndex)
                        isEdgeBreakB1=edgebreaks.IsSelected(4*faceIndex+1)
                        isEdgeBreakC1=edgebreaks.IsSelected(4*faceIndex+3)
                          
                        if isEdgeBreakA1==True and isEdgeBreakB1==True:
                            isEdgeBreakA=1    
                        if isEdgeBreakA1==True and isEdgeBreakB1==True:
                            isEdgeBreakB=1
                        if isEdgeBreakB1==True and isEdgeBreakC1==True:
                            isEdgeBreakB=1    
                        if isEdgeBreakB1==True and isEdgeBreakC1==True:
                            isEdgeBreakC=1
                            
                        if str(faceStyle)=="tri":
                            if isEdgeBreakA1==True and isEdgeBreakC1==True:
                                isEdgeBreakA=1
                            if isEdgeBreakA1==True and isEdgeBreakC1==True:
                                isEdgeBreakC=1
                                
                        if str(faceStyle)=="quad":
                            isEdgeBreakD1=edgebreaks.IsSelected(4*faceIndex+4)
                            if isEdgeBreakA1==True and isEdgeBreakD1==True:
                                isEdgeBreakA=1
                            if isEdgeBreakD1==True and isEdgeBreakC1==True:
                                isEdgeBreakC=1
                            if isEdgeBreakD1==True and isEdgeBreakA1==True:
                                isEdgeBreakD=1
                            if isEdgeBreakD1==True and isEdgeBreakC1==True:
                                isEdgeBreakD=1
                                
                        buildSharedPoint(faceStyle,meshBlock,meshBlock.copiedMesh,allOldPoints[oldpoints.a],uva,meshBlock.saveSubMeshes[subcount],oldpoints.a,normala,normalf,phoneAngle,usePhongAngle,isEdgeBreakA)
                        buildSharedPoint(faceStyle,meshBlock,meshBlock.copiedMesh,allOldPoints[oldpoints.b],uvb,meshBlock.saveSubMeshes[subcount],oldpoints.b,normalb,normalf,phoneAngle,usePhongAngle,isEdgeBreakB)
                        buildSharedPoint(faceStyle,meshBlock,meshBlock.copiedMesh,allOldPoints[oldpoints.c],uvc,meshBlock.saveSubMeshes[subcount],oldpoints.c,normalc,normalf,phoneAngle,usePhongAngle,isEdgeBreakC)
                        if str(faceStyle)=="quad":
                            buildSharedPoint(faceStyle,meshBlock,meshBlock.copiedMesh,allOldPoints[oldpoints.d],uvd,meshBlock.saveSubMeshes[subcount],oldpoints.d,normald,normalf,phoneAngle,usePhongAngle,isEdgeBreakD)
                
                if usePhong==False:
                    buildPoint(faceStyle,meshBlock,meshBlock.copiedMesh,meshBlock.saveSubMeshes[subcount],allOldPoints[oldpoints.a],oldpoints.a,uva)
                    buildPoint(faceStyle,meshBlock,meshBlock.copiedMesh,meshBlock.saveSubMeshes[subcount],allOldPoints[oldpoints.b],oldpoints.b,uvb)
                    buildPoint(faceStyle,meshBlock,meshBlock.copiedMesh,meshBlock.saveSubMeshes[subcount],allOldPoints[oldpoints.c],oldpoints.c,uvc)
                    if str(faceStyle)=="quad":
                        buildPoint(faceStyle,meshBlock,meshBlock.copiedMesh,meshBlock.saveSubMeshes[subcount],allOldPoints[oldpoints.d],oldpoints.d,uvd)
                subcount=len(meshBlock.saveSubMeshes)       
            subcount+=1
    exportData.subStatus=0
    
    
# i think this function is not ok. 
def transformUVS(subMesh):
    if subMesh.textureTag!=None:
        if len(subMesh.uvBuffer)>0:
            repeat=subMesh.textureTag[c4d.TEXTURETAG_TILE]
            scaleU=subMesh.textureTag[c4d.TEXTURETAG_TILESX]
            scaleV=subMesh.textureTag[c4d.TEXTURETAG_TILESY]
            if subMesh.textureTag[c4d.TEXTURETAG_REPETITIONX]>0 or subMesh.textureTag[c4d.TEXTURETAG_REPETITIONY]>0:
                repeat=False
                scaleU=scaleU
                scaleV=scaleV
            for uv in subMesh.uvBuffer:
                uv.x=(uv.x)-(subMesh.textureTag[c4d.TEXTURETAG_OFFSETX])
                uv.y=(uv.y)-(subMesh.textureTag[c4d.TEXTURETAG_OFFSETY])
                if subMesh.textureTag[c4d.TEXTURETAG_REPETITIONX]>0 or subMesh.textureTag[c4d.TEXTURETAG_REPETITIONY]>0:
                    uv.x=uv.x*scaleU
                    if subMesh.textureTag[c4d.TEXTURETAG_REPETITIONX]==0:
                        while uv.x>1:
                            uv.x-=1
                    if subMesh.textureTag[c4d.TEXTURETAG_REPETITIONX]>0:
                        repXCounter=1
                        repSeamlessXCounter=0
                        while repXCounter<subMesh.textureTag[c4d.TEXTURETAG_REPETITIONX]:
                            
                            if uv.x>repXCounter and uv.x<(repXCounter+1):
                                repSeamlessXCounter+=1
                                uv.x-=repXCounter
                                if repSeamlessXCounter==1:
									repSeamlessXCounter=-1
									uv.x=(uv.x*-1)+1
                            repXCounter+=1
                        if uv.x>repXCounter:
                            uv.x=1
							
                    uv.y=uv.y*scaleV
                    if subMesh.textureTag[c4d.TEXTURETAG_REPETITIONY]==0:
                        while uv.y>1:
                            uv.y-=1
                    if subMesh.textureTag[c4d.TEXTURETAG_REPETITIONY]>0:
                        repYCounter=1
                        repSeamlessYCounter=0
                        while repYCounter<subMesh.textureTag[c4d.TEXTURETAG_REPETITIONY]:
                            
                            if uv.y>repYCounter and uv.y<(repYCounter+1):
                                repSeamlessYCounter+=1
                                uv.y-=repYCounter
                                if repSeamlessYCounter==1:
									repSeamlessYCounter=-1
									uv.y=(uv.y*-1)+1
                            repYCounter+=1
                        if uv.y>repXCounter:
                            uv.y=1
        #print "texuretag repeat = "+str(repeat)+" scaleU = "+str(scaleU)+" scaleV = "+str(scaleV)    
        #build all the geometryStreams (the geometry-streams contain the data still as python-list, and will be parsed into binary



# create the final AWD-GeometryStream-Objects for one SubMeshBlock. 
def buildGeometryStreams(subMesh,scale):

    # create the final AWD-GeometryStream-Object for Point-Data (type=1)
    if len(subMesh.vertexBuffer)>0:
        pointData=[]
        for point in subMesh.vertexBuffer:
            pointData.append(point.x*scale)
            pointData.append(point.y*scale)
            pointData.append(point.z*scale)
        subMesh.saveGeometryStreams.append(classesAWDBlocks.awdGeometryStream(1,pointData))
        
    # create the final AWD-GeometryStream-Object for Normal-Data (type=4)
    if len(subMesh.normalBuffer)>0:
        normalData=[]
        for point in subMesh.normalBuffer:
            normalData.append(point.x)
            normalData.append(point.y)
            normalData.append(point.z)
        subMesh.saveGeometryStreams.append(classesAWDBlocks.awdGeometryStream(4,normalData))
        
    # create the final AWD-GeometryStream-Object for Quad-Index-Data (type=8) - NOT USED BY OFFICIAL AWD2
    if len(subMesh.quadBuffer)>0:
        quadData=[]
        for indexPoint in subMesh.quadBuffer:
            quadData.append(indexPoint)
        subMesh.saveGeometryStreams.append(classesAWDBlocks.awdGeometryStream(8,quadData))
        
    # create the final AWD-GeometryStream-Object for Index-Data (type=2)
    if len(subMesh.indexBuffer)>0:
        indexData=[]
        for indexPoint in subMesh.indexBuffer:
            indexData.append(indexPoint)
        subMesh.saveGeometryStreams.append(classesAWDBlocks.awdGeometryStream(2,indexData))
        
    # create the final AWD-GeometryStream-Object for UV-Data (type=3)
    if len(subMesh.uvBuffer)>0:
        uvData=[]
        for uv in subMesh.uvBuffer:
            uvData.append(uv.x)
            uvData.append(uv.y)
        subMesh.saveGeometryStreams.append(classesAWDBlocks.awdGeometryStream(3,uvData))
        
    # prepare Weight-Data and JointIndex-Data for the final AWD.GeometryStream-Object:
    if len(subMesh.weightsBuffer)>0 and len(subMesh.jointidxBuffer)>0:
        
        # Get the Maximum number of Joints used on one point, and create some lists to store the new weight data:        
        maxJoints=0                     # this will hold the maximum of joints per point, e.g. the length of weights-lists and jointIndex-lists
        subMesh.saveWeightsBuffer=[]    # this will hold a new list of weight for each point of the submesh
        subMesh.saveIndexBuffer=[]      # this will hold a new list of joindIndicies for each point of the submesh
        for weights in subMesh.weightsBuffer:       # for each weightList (same as "for each point of submesh")
            subMesh.saveWeightsBuffer.append([])        # create a new list, that will store all weights for this point later
            subMesh.saveIndexBuffer.append([])          # create a new list, that will store all JointIndicies for this point later
            if len(weights)>maxJoints:                  # if the length of this weight-list is bigger than a previous processed weight-list:
                maxJoints=len(weights)                      # set maxJoints to the length of this weight-list
                
        jointCount=0                                
        while jointCount<maxJoints:                         # do for 0-maxJoints
            bufferCount=0
            while bufferCount<len(subMesh.weightsBuffer):       # do for every list of weights:
                newWeight=float(0.0)
                newIndex=1
                biggestWeight=float(0.0)
                curweightcount=-1
                weightcount=0
                while weightcount<len(subMesh.weightsBuffer[bufferCount]):              # find the biggest weight of the old-weight-list
                    if subMesh.weightsBuffer[bufferCount][weightcount]>=biggestWeight:      # and store it to biggestWeight and curweightcount (weight + jointIndex)
                        biggestWeight=float(subMesh.weightsBuffer[bufferCount][weightcount])
                        curweightcount=weightcount
                    weightcount+=1
                    
                if curweightcount>=0:                                                   # if the curweightcount was set (another weight/joint was found for this list)
                    newIndex=subMesh.jointidxBuffer[bufferCount][curweightcount]            # get the "real" Index of the JointIndex
                    subMesh.weightsBuffer[bufferCount].pop(curweightcount)                  # delete the newly found weight from the old weight-list
                    subMesh.jointidxBuffer[bufferCount].pop(curweightcount)                 # delete the newly found joindindex from the old joindindex-list
                    
                subMesh.saveIndexBuffer[bufferCount].append(newIndex)                   # save the new JointIndex to the new JointIndex-list
                subMesh.saveWeightsBuffer[bufferCount].append(biggestWeight)            # save the new JointIndex to the new JointIndex-list
                bufferCount+=1
            jointCount+=1
            
        bufferCount=0
        while bufferCount<len(subMesh.weightsBuffer):                           # for every weight-list do:
            jointCount=0
            allWeight=0                 # here will store the sum of all weights applied to one point, so we can check if they are == 1.0 as they should
            while jointCount<maxJoints:                                             # iterate trough list (using the maxJoints-value instead of len(weight-list)
                if float(subMesh.saveWeightsBuffer[bufferCount][jointCount])>float(1.0):        # check if this weight alone is bigger than 1.0
                    subMesh.saveWeightsBuffer[bufferCount][jointCount]=float(1.0)                    # and if so, set it back to 1
                if float(subMesh.saveWeightsBuffer[bufferCount][jointCount])<float(0.0):        # check if this weight alone is smaller than 0.0
                    subMesh.saveWeightsBuffer[bufferCount][jointCount]=float(0.0)                    # and if so, set it back to 0.0
                allWeight+=float(subMesh.saveWeightsBuffer[bufferCount][jointCount])            # add this weight to allWeight        
                jointCount+=1
                
            if float(allWeight) == float(0.0):                                      # if the allWeight for this point is 0.0 
                subMesh.saveWeightsBuffer[bufferCount][0]=float(1.0)                    # we set the first weight in the list to 1.0
                allWeight=float(1.0)                                                    # and fix the allWeight to 1.0 so the next calculation will be skipped
            if float(allWeight) != float(1.0):                                      # if the allWeight for this point is not 1.0
                jointCount=0                                                                                
                while jointCount<maxJoints:                                             # for every weight in the list do:                          
                    subMesh.saveWeightsBuffer[bufferCount][jointCount]*=(1/allWeight)       # multiply with 1/allWeight to set the allWeight back to 1
                    jointCount+=1
            bufferCount+=1

        # build final AWD-GeometryStream-Object for JointIndicies (type=6)
        indexData=[]                                # will hold the final weight-list
        for index in subMesh.saveIndexBuffer:
            for index2 in index:
                indexData.append(index2)            
        subMesh.saveGeometryStreams.append(classesAWDBlocks.awdGeometryStream(6,indexData))

        # build final AWD-GeometryStream-Object for Weights (type=7)
        weightData=[]
        for weight in subMesh.saveWeightsBuffer:
            for weight2 in weight:
                weightData.append(weight2)            
        subMesh.saveGeometryStreams.append(classesAWDBlocks.awdGeometryStream(7,weightData))
    
