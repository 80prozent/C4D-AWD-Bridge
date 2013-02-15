import c4d
from c4d import documents

from awdexporter import ids
from awdexporter import awdBlocks
from awdexporter import awdSubMeshReader
from awdexporter import awdHelpers

   
def deleteCopiedMeshes(meshBlockList):
    for meshBlock in meshBlockList:
            
        meshBlock.copiedMesh.Remove()
		
def convertMeshes(meshBlockList,exportData,workerthreat):
    for meshBlock in meshBlockList:
        #exportData.allStatus+=10
        if workerthreat.TestBreak():
            return
           
        convertMesh(meshBlock,exportData,workerthreat)

def convertMesh(meshBlock,exportData,workerthreat):
    doc=documents.GetActiveDocument()
    doc.SetActiveObject(meshBlock.copiedMesh)
    if not meshBlock.copiedMesh.GetTag(5604): 
        return    
    if not meshBlock.copiedMesh.GetTag(5600):
        return  
    materials=awdHelpers.getObjectsMaterials(meshBlock.copiedMesh)
    matCounter=0   
    while matCounter<len(materials):
        meshBlock.saveSubMeshes.append(awdBlocks.awdSubMesh(materials[matCounter][0],materials[matCounter][1].name,materials[matCounter][1].selectionIndexe,materials[matCounter][2]))
        matCounter+=1

         
    if workerthreat.TestBreak():
        return
        
            
    awdSubMeshReader.prepareSubmeshIndexe(meshBlock)       
 
    if workerthreat.TestBreak():
        return

    #if i.GetType()==5701:                  
        #print "Kantenselektion : "
    #if i.GetType()==5674:
        #print "Punktselektion : "        

    if meshBlock.copiedMesh.GetTag(c4d.Tweights)!=None:
        firstSkeleton=exportData.jointIDstoSkeletonBlocks.get(str(meshBlock.copiedMesh.GetTag(c4d.Tweights).GetJoint(0,doc).GetName()),None)        
        noValidSkeleton=False
        if firstSkeleton!=None:
            firstSkeletonName=exportData.jointIDstoSkeletonBlocks[str(meshBlock.copiedMesh.GetTag(c4d.Tweights).GetJoint(0,doc).GetName())].name
            jointcounter=0 
            meshBlock.jointTranslater=[]
            while jointcounter<meshBlock.copiedMesh.GetTag(c4d.Tweights).GetJointCount():
                curJoint=meshBlock.copiedMesh.GetTag(c4d.Tweights).GetJoint(jointcounter,doc)
                if exportData.jointIDstoSkeletonBlocks.get(str(curJoint.GetName()),None)==None:
                    noValidSkeleton=True
                    break
                if exportData.jointIDstoSkeletonBlocks.get(str(curJoint.GetName()),None)!=None:
                    if firstSkeletonName!=exportData.jointIDstoSkeletonBlocks[str(curJoint.GetName())].name:
                        noValidSkeleton=True
                        break
                meshBlock.jointTranslater.append(exportData.jointIDstoJointBlocks[str(curJoint.GetName())].jointID-1)
                jointcounter+=1
            if noValidSkeleton==False:
                pass#print "Skeleton FOund: "+str(firstSkeletonName)
        if firstSkeleton==None or noValidSkeleton==True:
            jointcounter=0
            meshBlock.jointTranslater=[]
            while jointcounter<meshBlock.copiedMesh.GetTag(c4d.Tweights).GetJointCount():
                meshBlock.jointTranslater.append(jointcounter)
                jointcounter+=1
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
                
    awdSubMeshReader.collectSubmeshData(meshBlock,exportData,workerthreat)
    if workerthreat.TestBreak():
        return
    for subMesh in meshBlock.saveSubMeshes:
        if workerthreat.TestBreak():
            return
        awdSubMeshReader.transformUVS(subMesh)
        if workerthreat.TestBreak():
            return
        awdSubMeshReader.buildGeometryStreams(subMesh,exportData.scale)
    
    #meshBlock.copiedMesh.Remove()



          
  
