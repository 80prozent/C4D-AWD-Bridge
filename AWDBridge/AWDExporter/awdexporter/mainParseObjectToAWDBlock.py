# functions running in c4d-main-thread
import c4d
from c4d import documents

from awdexporter import ids
from awdexporter import classesAWDBlocks
from awdexporter import mainHelpers

#function check the object-type of a c4d-object and creates a corresponding AWDBlock (see classesAWDBlocks) 
def createSceneBlock(exportData,curObj,tagForExport,returner=True,onlyNullObject=False):  
  
    if onlyNullObject==False:     
        if curObj.GetType() == c4d.Oextrude:
            if len(curObj.GetChildren())==0:
                return False, False
        
        if curObj.GetType() == c4d.Ospline:
            if len(curObj.GetChildren())==0:
                return False, False
        
    
    #####	Primitives
        
        if curObj.GetType() == c4d.Oplane:
            if len(curObj.GetChildren())==0:
                return False, False
        
        if curObj.GetType() == c4d.Ocone:
            if len(curObj.GetChildren())==0:
                return False, False
         
        if curObj.GetType() == c4d.Ocylinder:
            if len(curObj.GetChildren())==0:
                return False, False
        
        if curObj.GetType() == c4d.Osphere:
            if len(curObj.GetChildren())==0:
                return False, False
        
        if curObj.GetType() == c4d.Ocube:
            if len(curObj.GetChildren())==0:
                return False, False
    
        if curObj.GetType() == c4d.Oinstance:
            if curObj[c4d.INSTANCEOBJECT_LINK].GetType()!=c4d.Opolygon:
                print "Instance objects are only allowed to point to Mesh objects"
                if len(curObj.GetChildren())==0:
                    return False, False
            if curObj[c4d.INSTANCEOBJECT_LINK].GetType()==c4d.Opolygon:
                newAWDBlock=classesAWDBlocks.MeshInstanceBlock(exportData.idCounter,0,None,curObj)
                newAWDBlock.geoObj=curObj[c4d.INSTANCEOBJECT_LINK]
                exportData.IDsToAWDBlocksDic[str(exportData.idCounter)]=newAWDBlock
                exportData.allAWDBlocks.append(newAWDBlock)
                exportData.allSceneObjects.append(newAWDBlock)
                newAWDBlock.name=curObj.GetName()
                newAWDBlock.tagForExport=tagForExport
                curObj.SetName(str(exportData.idCounter))
                exportData.idCounter+=1
    
                newAWDBlock.dataParentBlockID=0
                if curObj.GetUp():
                    parentID=exportData.IDsToAWDBlocksDic.get(str(curObj.GetUp().GetName()),None)
                    if parentID!=None:
                        newAWDBlock.dataParentBlockID=int(curObj.GetUp().GetName())
                exportData.unconnectedInstances.append(newAWDBlock)
                return True, True
            
            
    
        if curObj.GetType() == c4d.Opolygon:
        
            newAWDBlock=classesAWDBlocks.TriangleGeometrieBlock(exportData.idCounter,0,curObj)
            exportData.IDsToAWDBlocksDic[str(exportData.idCounter)]=newAWDBlock
            exportData.allAWDBlocks.append(newAWDBlock) 
            exportData.allMeshObjects.append(newAWDBlock)
            newAWDBlock.saveLookUpName=curObj.GetName()
            newAWDBlock.tagForExport=tagForExport
            exportData.idCounter+=1
    
            newAWDBlock=classesAWDBlocks.MeshInstanceBlock(exportData.idCounter,0,exportData.idCounter-1,curObj)
            exportData.IDsToAWDBlocksDic[str(exportData.idCounter)]=newAWDBlock
            exportData.allAWDBlocks.append(newAWDBlock)
            exportData.allSceneObjects.append(newAWDBlock)
            newAWDBlock.name=curObj.GetName() 
            newAWDBlock.tagForExport=tagForExport
            curObj.SetName(str(exportData.idCounter))
            newAWDBlock.dataParentBlockID=0
            if curObj.GetUp():
                parentID=exportData.IDsToAWDBlocksDic.get(str(curObj.GetUp().GetName()),None)
                if parentID!=None:
                    newAWDBlock.dataParentBlockID=int(curObj.GetUp().GetName())
                
                    
            exportData.idCounter+=1
            materials=mainHelpers.getObjectsMaterials(curObj,None,newAWDBlock)
            for mat in materials:
                newAWDBlock.saveMaterials.append(mat[0])
    
        
            return True, True
        
        if curObj.GetType() == c4d.Oskin:
            if len(curObj.GetChildren())==0:
                return False, False
        
        if curObj.GetType() == c4d.Ojoint:
            if curObj.GetTag(1028937):
                skeletonTag=curObj.GetTag(1028937)
    
                if skeletonTag[1010]!=False:
                    print "Found SkeletonTag"
                if skeletonTag[1014]==False:
                    print "Do not export Skeleton as SceneObjects"
                    tagForExport=False
                    returner= True
    
            if curObj.GetTag(1028938):
                skeletonAnimationTag=curObj.GetTag(1028938)
                if skeletonAnimationTag[1010]!=False:
                    exportData.animationCounter+=1
                    print "Build SkeletonAnimation"
                return False, False
    
    
        if curObj.GetType() == c4d.Olight:
            if len(curObj.GetChildren())==0:
                return False, False
        
        if curObj.GetType() == c4d.Ocamera:
            if len(curObj.GetChildren())==0:
                return False, False

    newAWDBlock=classesAWDBlocks.ContainerBlock(exportData.idCounter,0,curObj)
    exportData.IDsToAWDBlocksDic[str(exportData.idCounter)]=newAWDBlock
    exportData.allAWDBlocks.append(newAWDBlock)
    exportData.allSceneObjects.append(newAWDBlock)
    newAWDBlock.name=curObj.GetName()
    newAWDBlock.tagForExport=tagForExport
        
    newAWDBlock.dataParentBlockID=0
    if curObj.GetUp():
        parentID=exportData.IDsToAWDBlocksDic.get(str(curObj.GetUp().GetName()),None)
        if parentID!=None:
            newAWDBlock.dataParentBlockID=int(curObj.GetUp().GetName())
    curObj.SetName(str(exportData.idCounter))
    exportData.idCounter+=1
    
    return returner,tagForExport