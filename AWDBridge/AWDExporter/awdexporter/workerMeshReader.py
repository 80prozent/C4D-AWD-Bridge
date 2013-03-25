# functions that will run inside the background-worker-thread
# main-functions for mesh-converting

import c4d
from c4d import documents

from awdexporter import ids
from awdexporter import classesAWDBlocks
from awdexporter import workerSubMeshReader
from awdexporter import workerHelpers

# convert all the geometry-blocks from c4d-polygon-object to away3d mesh
def convertMeshes(meshBlockList,exportData,workerthreat):
    for meshBlock in meshBlockList:                     # we check if the user cancelled the process
        if workerthreat.TestBreak():                        # if user cancelled 
            return                                              # and return if he has   
        convertMesh(meshBlock,exportData,workerthreat)      # convert the geometry-block into away3d-mesh-data

# collect all Skeletons that are used by a weighttag in a list
def getUsedSkeletons(cntLength,weightTag,jointIdsToSkeletonsBlocks,curDoc):
    jointCnt=0
    usedSkeletons=[]
    while jointCnt<cntLength:
        curJoint=weightTag.GetJoint(jointCnt,curDoc)
        if curJoint is not None:
            curJointName=curJoint.GetName()
            nextSkeleton=jointIdsToSkeletonsBlocks.get(str(curJointName),None) 
            if nextSkeleton is not None:
                if len(usedSkeletons)==0:
                    usedSkeletons.append(nextSkeleton)
                if len(usedSkeletons)>0:
                    allreadyExists=False
                    for skeleton in usedSkeletons:
                        if skeleton==nextSkeleton:
                            allreadyExists=True
                            break
                    if allreadyExists==False:
                        usedSkeletons.append(nextSkeleton)
        jointCnt+=1
    return usedSkeletons
    
def convertMesh(meshBlock,exportData,workerthreat):
    exportData.doc.SetActiveObject(meshBlock.copiedMesh)
    if not meshBlock.copiedMesh.GetTag(5604): 
        return    
    if not meshBlock.copiedMesh.GetTag(5600):
        return  
    materials=workerHelpers.getObjectsMaterials(meshBlock.copiedMesh)
    matCounter=0   
    while matCounter<len(materials):
        meshBlock.saveSubMeshes.append(classesAWDBlocks.awdSubMesh(materials[matCounter][0],materials[matCounter][1].name,materials[matCounter][1].selectionIndexe,materials[matCounter][2]))
        matCounter+=1
         
    if workerthreat.TestBreak():
        return        
            
    workerSubMeshReader.prepareSubmeshIndexe(meshBlock)       
 
    if workerthreat.TestBreak():
        return

    # if the meshBlock has a WeightTag-applied, we check if the mesh is used by one single skeleton or not.
    weightTag=meshBlock.copiedMesh.GetTag(c4d.Tweights)
    if weightTag is not None:
        jointCount=weightTag.GetJointCount()
        allSkeletons=getUsedSkeletons(jointCount,weightTag,exportData.jointIDstoSkeletonBlocks,exportData.doc)           
        if len(allSkeletons)==0:
            print "Warning - No Joints are bound to a valid Skeleton"
        if len(allSkeletons)>1:
            print "Warning - Not all Joints are bound to the same Skeleton"
        if len(allSkeletons)==1:
            meshBlock.weightTag=weightTag
    if workerthreat.TestBreak():
        return
        
    #morphs=[]    
    #for morphState in allPointAndUvMorpTag:
        #if morphState.morphedObject==cur_mesh:
            #morphs.append(morphState)   
    #for submesh in new_submeshes:
        #for morphState in morphs:
            #submorphVerts=[]
            #submorphUVs=[]
            #submorphActiv=False
            #submorphdata=[submorphVerts,submorphUVs,submorphActiv,morphState.morphName,morphState.tagName,morphState.tagObject]
            #submesh.morphs.append(submorphdata)                
    print ("parse = "+str(meshBlock.sceneObject.GetName()))            
    workerSubMeshReader.collectSubmeshData(meshBlock,exportData,workerthreat)   # parse this object into a awd2-geometry-block
    if workerthreat.TestBreak():                                                # when the user has cancelled the process: 
        return                                                                      # we stop executing and return 
    for subMesh in meshBlock.saveSubMeshes:                                     # for every SubMeshBlock that has been created:
        if workerthreat.TestBreak():                                                # we check if the user cancelled the process
            return                                                                      # and return if he has
        workerSubMeshReader.transformUVS(subMesh)                                   # transform the uvs if needed (to allow for tilling etc)
        if workerthreat.TestBreak():                                                # check if the user cancelled the process
            return                                                                      # and return if he has
        workerSubMeshReader.buildGeometryStreams(subMesh,exportData.scale)          # build the AWD-geometry-streams for all submeshes



          
  
