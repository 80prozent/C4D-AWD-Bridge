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
        #print "delete first submehs"
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
        while jointcounter<curMesh.GetTag(c4d.Tweights).GetJointCount():    
            if curMesh.GetTag(c4d.Tweights).GetWeight(jointcounter,pointNr)>0:
                weights.append(curMesh.GetTag(c4d.Tweights).GetWeight(jointcounter,pointNr))
                joints.append(meshBlock.jointTranslater[jointcounter]) 
                ismorph=False
            jointcounter+=1      
    if ismorph==False:
        if str(faceStyle)=="tri":
            curSubMesh.indexBuffer.append(len(curSubMesh.vertexBuffer))        
        if str(faceStyle)=="quad":
            curSubMesh.quadBuffer.append(len(curSubMesh.vertexBuffer))

        if checkerstring!= None:
            curSubMesh.uniquePoolDict[checkerstring]=len(curSubMesh.vertexBuffer)
        #curSubMesh.indexBufferMorphed.append("p") 
        curSubMesh.vertexBuffer.append(curPoint) 
        #curSubMesh.sharedvertexBuffer.append(-1) faceStyle
        if curUv!= None:
            curSubMesh.uvBuffer.append(curUv)
        if curNormal!= None:
            curSubMesh.normalBuffer.append(curNormal)
        if curNormalf!= None:
            curSubMesh.faceNormal.append(curNormalf)
        if weights!= None:
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
            curSubMesh.jointidxBuffer.append(joints) """  
                        

            
def collectSubmeshData(meshBlock,exportData,workerthreat):
    usePhong=False
    usePhongAngle=False
    useEdgeBreaks=False
    edgebreaks=None
    phoneAngle=-1
    normalData=meshBlock.copiedMesh.CreatePhongNormals()
    normalCounter=0
    if meshBlock.copiedMesh.GetTag(5612):
        usePhong=True
        usePhongAngle=meshBlock.copiedMesh.GetTag(5612)[c4d.PHONGTAG_PHONG_ANGLELIMIT]
        useEdgeBreaks=meshBlock.copiedMesh.GetTag(5612)[c4d.PHONGTAG_PHONG_USEEDGES]
        phoneAngle=meshBlock.copiedMesh.GetTag(5612)[c4d.PHONGTAG_PHONG_ANGLE]
        if useEdgeBreaks==True:
            edgebreaks=meshBlock.copiedMesh.GetPhongBreak()
        
    allOldPoints=meshBlock.copiedMesh.GetAllPoints()
    meshBlock.pointsUsed=[]
    for point in allOldPoints:
        meshBlock.pointsUsed.append(False)
    polys=meshBlock.copiedMesh.GetAllPolygons()
    count=len(polys)
    count2=float(10/float(count))
    for faceIndex in xrange(count): 
        if workerthreat.TestBreak():
            return
        exportData.subStatus=float(float(faceIndex)/float(count))
        exportData.allStatus+=count2
        oldpoints=polys[faceIndex]
        if meshBlock.copiedMesh.GetTag(5671):
            uv =meshBlock.copiedMesh.GetTag(5671).GetSlow(faceIndex)
        subcount=0
        for subcount in xrange(len(meshBlock.saveSubMeshes)):
            
            if meshBlock.saveSubMeshes[subcount].selectionIndexe[faceIndex]==1:  
                 
                uva=None
                uvb=None
                uvc=None
                uvd=None
                if meshBlock.copiedMesh.GetTag(5671):
                    uva=uv["a"]
                    uvb=uv["b"]
                    uvc=uv["c"]
                    uvd=uv["d"]
                normala=None
                normalb=None
                normalc=None
                normald=None
                
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
                    if str(faceStyle)=="tri":
                        if edgebreaks!=None:
                            isEdgeBreakA1=edgebreaks.IsSelected(4*faceIndex)
                            isEdgeBreakB1=edgebreaks.IsSelected(4*faceIndex+1)
                            isEdgeBreakC1=edgebreaks.IsSelected(4*faceIndex+3)
                            
                            if isEdgeBreakA1==True and isEdgeBreakB1==True:
                                isEdgeBreakA=1
                            if isEdgeBreakA1==True and isEdgeBreakC1==True:
                                isEdgeBreakA=1
    
                            if isEdgeBreakA1==True and isEdgeBreakB1==True:
                                isEdgeBreakB=1
                            if isEdgeBreakB1==True and isEdgeBreakC1==True:
                                isEdgeBreakB=1
    
                            if isEdgeBreakA1==True and isEdgeBreakC1==True:
                                isEdgeBreakC=1
                            if isEdgeBreakB1==True and isEdgeBreakC1==True:
                                isEdgeBreakC=1
                                
                        buildSharedPoint(faceStyle,meshBlock,meshBlock.copiedMesh,allOldPoints[oldpoints.a],uva,meshBlock.saveSubMeshes[subcount],oldpoints.a,normala,normalf,phoneAngle,usePhongAngle,isEdgeBreakA)
                        buildSharedPoint(faceStyle,meshBlock,meshBlock.copiedMesh,allOldPoints[oldpoints.b],uvb,meshBlock.saveSubMeshes[subcount],oldpoints.b,normalb,normalf,phoneAngle,usePhongAngle,isEdgeBreakB)
                        buildSharedPoint(faceStyle,meshBlock,meshBlock.copiedMesh,allOldPoints[oldpoints.c],uvc,meshBlock.saveSubMeshes[subcount],oldpoints.c,normalc,normalf,phoneAngle,usePhongAngle,isEdgeBreakC)
                
                    if str(faceStyle)=="quad":
                        if edgebreaks!=None:
                            isEdgeBreakA1=edgebreaks.IsSelected(4*faceIndex)
                            isEdgeBreakB1=edgebreaks.IsSelected(4*faceIndex+1)
                            isEdgeBreakC1=edgebreaks.IsSelected(4*faceIndex+2)
                            isEdgeBreakD1=edgebreaks.IsSelected(4*faceIndex+3)
                            
                            if isEdgeBreakA1==True and isEdgeBreakB1==True:
                                isEdgeBreakA=1
                            if isEdgeBreakA1==True and isEdgeBreakD1==True:
                                isEdgeBreakA=1
    
                            if isEdgeBreakA1==True and isEdgeBreakB1==True:
                                isEdgeBreakB=1
                            if isEdgeBreakB1==True and isEdgeBreakC1==True:
                                isEdgeBreakB=1
    
                            if isEdgeBreakB1==True and isEdgeBreakC1==True:
                                isEdgeBreakC=1
                            if isEdgeBreakD1==True and isEdgeBreakC1==True:
                                isEdgeBreakC=1
                                
                            if isEdgeBreakD1==True and isEdgeBreakA1==True:
                                isEdgeBreakD=1
                            if isEdgeBreakD1==True and isEdgeBreakC1==True:
                                isEdgeBreakD=1
                                
                        buildSharedPoint(faceStyle,meshBlock,meshBlock.copiedMesh,allOldPoints[oldpoints.a],uva,meshBlock.saveSubMeshes[subcount],oldpoints.a,normala,normalf,phoneAngle,usePhongAngle,isEdgeBreakA)
                        buildSharedPoint(faceStyle,meshBlock,meshBlock.copiedMesh,allOldPoints[oldpoints.b],uvb,meshBlock.saveSubMeshes[subcount],oldpoints.b,normalb,normalf,phoneAngle,usePhongAngle,isEdgeBreakB)
                        buildSharedPoint(faceStyle,meshBlock,meshBlock.copiedMesh,allOldPoints[oldpoints.c],uvc,meshBlock.saveSubMeshes[subcount],oldpoints.c,normalc,normalf,phoneAngle,usePhongAngle,isEdgeBreakC)
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
#checks if a vert/uv - combination allready exists in the uniquePool or in the uniquePoolMorphed of the given Submesh.

                
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
                
def buildGeometryStreams(subMesh,scale):
        
    if len(subMesh.vertexBuffer)>0:
        pointData=[]
        for point in subMesh.vertexBuffer:
            pointData.append(point.x*scale)
            pointData.append(point.y*scale)
            pointData.append(point.z*scale)
        subMesh.saveGeometryStreams.append(classesAWDBlocks.awdGeometryStream(1,pointData))
    if len(subMesh.normalBuffer)>0:
        normalData=[]
        for point in subMesh.normalBuffer:
            normalData.append(point.x)
            normalData.append(point.y)
            normalData.append(point.z)
        subMesh.saveGeometryStreams.append(classesAWDBlocks.awdGeometryStream(4,normalData))
    if len(subMesh.quadBuffer)>0:
        quadData=[]
        for indexPoint in subMesh.quadBuffer:
            quadData.append(indexPoint)
        subMesh.saveGeometryStreams.append(classesAWDBlocks.awdGeometryStream(8,quadData))
    if len(subMesh.indexBuffer)>0:
        indexData=[]
        for indexPoint in subMesh.indexBuffer:
            indexData.append(indexPoint)
        subMesh.saveGeometryStreams.append(classesAWDBlocks.awdGeometryStream(2,indexData))
    if len(subMesh.uvBuffer)>0:
        uvData=[]
        for uv in subMesh.uvBuffer:
            uvData.append(uv.x)
            uvData.append(uv.y)
        subMesh.saveGeometryStreams.append(classesAWDBlocks.awdGeometryStream(3,uvData))
    if len(subMesh.weightsBuffer)>0 and len(subMesh.jointidxBuffer)>0:
        maxJoints=0
        subMesh.saveWeightsBuffer=[]
        subMesh.saveIndexBuffer=[]
        for weights in subMesh.weightsBuffer:
            subMesh.saveWeightsBuffer.append([])
            subMesh.saveIndexBuffer.append([])
            if len(weights)>maxJoints:
                maxJoints=len(weights)
        jointCount=0
        while jointCount<maxJoints:
            bufferCount=0
            while bufferCount<len(subMesh.weightsBuffer):
                newWeight=0
                newIndex=1
                biggestWeight=0
                curweightcount=-1
                weightcount=0
                while weightcount<len(subMesh.weightsBuffer[bufferCount]):
                    if subMesh.weightsBuffer[bufferCount][weightcount]>=biggestWeight:
                        biggestWeight=subMesh.weightsBuffer[bufferCount][weightcount]
                        curweightcount=weightcount
                    weightcount+=1
                if curweightcount>=0:
                    newIndex=subMesh.jointidxBuffer[bufferCount][curweightcount]
                    biggestWeight=biggestWeight
                    subMesh.weightsBuffer[bufferCount].pop(curweightcount)
                    subMesh.jointidxBuffer[bufferCount].pop(curweightcount)
                subMesh.saveIndexBuffer[bufferCount].append(newIndex)
                subMesh.saveWeightsBuffer[bufferCount].append(biggestWeight)
                bufferCount+=1
            jointCount+=1

        bufferCount=0
        while bufferCount<len(subMesh.weightsBuffer):
            jointCount=0
            allWeight=0
            while jointCount<maxJoints:
                if subMesh.saveWeightsBuffer[bufferCount][jointCount]>1:
                    subMesh.saveWeightsBuffer[bufferCount][jointCount]=1
                if subMesh.saveWeightsBuffer[bufferCount][jointCount]<0:
                    subMesh.saveWeightsBuffer[bufferCount][jointCount]=0
                allWeight+=subMesh.saveWeightsBuffer[bufferCount][jointCount]
                jointCount+=1
                
            if allWeight == 0:
                subMesh.saveWeightsBuffer[bufferCount][0]=1
                allWeight=1
            if allWeight != 1:
                jointCount=0
                while jointCount<maxJoints:
                    subMesh.saveWeightsBuffer[bufferCount][jointCount]*=(1/allWeight)
                    jointCount+=1
                

            bufferCount+=1

        indexData=[]
        for index in subMesh.saveIndexBuffer:
            for index2 in index:
                indexData.append(index2)            
        subMesh.saveGeometryStreams.append(classesAWDBlocks.awdGeometryStream(6,indexData))

        weightData=[]
        for weight in subMesh.saveWeightsBuffer:
            for weight2 in weight:
                weightData.append(weight2)
            
        subMesh.saveGeometryStreams.append(classesAWDBlocks.awdGeometryStream(7,weightData))

        #subMesh.saveGeometryStreams.append(classesAWDBlocks.awdGeometryStream(3,uvData))
       
  
    
     
    
