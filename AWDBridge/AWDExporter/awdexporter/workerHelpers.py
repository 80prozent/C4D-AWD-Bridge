# functions that will run inside the background-worker-thread

import c4d
import copy
import struct
import os
import zlib
from awdexporter import ids
from awdexporter import classesHelper
from awdexporter import workerReorderBlocks
from awdexporter import classesAWDBlocks

# called by "WorkerExporter.py"
def getAllObjectData(exportData):
    for awdSceneBlock in exportData.allSceneObjects:
        dataMatrix=awdSceneBlock.sceneObject.GetMl()
        if awdSceneBlock.isSkinned==True:
            pass#dataMatrix=c4d.Matrix()
        awdSceneBlock.dataMatrix=dataMatrix
		
# called by "WorkerExporter.py"
# creates the final binary string and saves it to harddisc
def exportAllData(exportData):        
    outputBits=struct.pack('< 3s',exportData.headerMagicString)
    outputBits+=struct.pack('< B',exportData.headerVersionNumberMajor)
    outputBits+=struct.pack('< B',exportData.headerVersionNumberMinor)
    outputBits+=struct.pack('< H',exportData.headerFlagBits)
    outputBits+=struct.pack('< B',exportData.headerCompressionType)
    outputBlocks=str()
    blocksparsed=0
    while blocksparsed<len(exportData.allSaveAWDBlocks):
        outputBlocks+=exportData.allSaveAWDBlocks[blocksparsed].writeBinary(exportData)
        blocksparsed+=1
    if exportData.headerCompressionType==1:
        outputBody = zlib.compress(outputBlocks, 9)
    if exportData.headerCompressionType==0:
        outputBody = outputBlocks
    outputBits+=struct.pack('< I',len(outputBody))
    outputBits+=outputBody
    f = open(exportData.datei, 'wb')
    f.write(outputBits)
    f.close()
    if exportData.openPrefab==True:
        c4d.storage.GeExecuteFile(exportData.datei)
    return
	
def reorderAllBlocks(exportData):

    for awdBlock in exportData.allAWDBlocks:
        workerReorderBlocks.addToExportListMaterials(exportData,awdBlock)
    for awdBlock in exportData.allAWDBlocks:
        workerReorderBlocks.addToExportList(exportData,awdBlock)
    for awdSkeleton in exportData.allSkeletonBlocks:
        workerReorderBlocks.addSkeleton(exportData,awdSkeleton)
    for awdSkeletonAnimation in exportData.allSkeletonAnimations:
        workerReorderBlocks.addSkeletonAnimation(exportData,awdSkeletonAnimation)

def connectInstances(exportData):
    for instanceBlock in exportData.unconnectedInstances:
        geoInstanceID=instanceBlock.sceneObject[c4d.INSTANCEOBJECT_LINK].GetName()
        instanceGeoBlock=exportData.allAWDBlocks[int(geoInstanceID)]        
        if instanceGeoBlock is not None:
            geoBlockID=instanceGeoBlock.geoBlockID
            geoBlock=exportData.allAWDBlocks[int(geoBlockID)]    
            if geoBlock is not None:      
                geoBlock.sceneBlocks.append(instanceBlock)
        instanceBlock.geoBlockID=geoBlockID
        
	
			
# most likely this function will be edited soon, so it this duplicated version makes sense		
def getObjectColorMatBlock(exportData,colorVector):
    newColorVecString="#"+str(colorVector)
    colorMat=exportData.colorMaterials.get(newColorVecString,None)  
    #print str(newColorVecString) + "  /  "+str() 
    if colorMat is not None:
        return colorMat
    newAWDBlock=classesAWDBlocks.StandartMaterialBlock(exportData.idCounter,0,True)
    newAWDBlock.saveLookUpName="Material"
    newAWDBlock.matColor=[colorVector.z*255,colorVector.y*255,colorVector.x*255,0]
    newAWDBlock.saveMatProps.append(1)
    newAWDBlock.isCreated=True
    newAWDBlock.tagForExport=False 
    
    exportData.allAWDBlocks.append(newAWDBlock)
    exportData.allMatBlocks.append(newAWDBlock)
    exportData.colorMaterials[newColorVecString]=newAWDBlock
    #exportData.MaterialsToAWDBlocksDic[str(defaultMaterial)]=newAWDBlock 
    exportData.idCounter+=1
    return newAWDBlock
       


def getAllPolySelections(curObj):
    allSelections=[]                                                                                                                            # we create "allSelections" as new empty List
    for selectionTag in curObj.GetTags():                                                                                                           # do for each tag on the Object:          
        if selectionTag.GetType()==c4d.Tpolygonselection:                                                                                           # if the tag is a Polygon-SelectionTag:
            allSelections.append(classesHelper.PolySelection(selectionTag.GetName(),selectionTag.GetBaseSelect().GetAll(len(curObj.GetAllPolygons())))) # store a new instance of HelperClass "PolySelection" in  "allSelections"                       
    return allSelections
   
# returns a list of materials that are directly applied to the baseGeometry (the polygonObject) 
def getMaterials(curObj,allSelections,inherite):
    returnMats=[]
    for tag in curObj.GetTags():                                        # do for each tag on the Object:  
        if tag.GetType()==c4d.Ttexture:                                     # if the tag is a texture tag:
            foundTexturetag=True                                                # set "foundTexturetag" to True 
            curSelection=tag[c4d.TEXTURETAG_RESTRICTION]                        # get the name of the Polygon-Selection that restricts the Material or None or ""     
            if curSelection is not None and str(curSelection)!=str(""):         # if the name of the Polygon-Selection is not None and not "", the material is restricted by a Selection:
                for selection in allSelections:                                         # for each selection do:
                    if str(tag[c4d.TEXTURETAG_RESTRICTION])==selection.name:                # if this is the selection that is restricting the textureTag: 
                        if tag.GetMaterial() is not None:                                      
                            if len(returnMats)==0:                                                  
                                newMaterialList=[]
                                newMaterialList.append(str(1))                      
                                newMaterialList.append(classesHelper.PolySelection("Base",[]))
                                newMaterialList.append(None)  
                                returnMats.append(newMaterialList)
                            if str(tag.GetMaterial().GetTypeName())!="Mat":                         # if this Materials-type is not a C4d-DefaultMaterial:
                                newWarning=AWDerrorObject(ids.WARNINGMESSAGE1,tag.GetMaterial().GetName())  # create a Warning Object
                                exportData.AWDwarningObjects.append(newWarning)                             
                                newMaterialList=[]
                                newMaterialList.append(str(1))                      
                                newMaterialList.append(selection)
                                newMaterialList.append(None)  
                                returnMats.append(newMaterialList)
                            if str(tag.GetMaterial().GetTypeName())=="Mat":                         
                                newMaterialList=[]
                                newMaterialList.append(tag.GetMaterial().GetName())             
                                newMaterialList.append(selection)
                                newMaterialList.append(tag)  
                                returnMats.append(newMaterialList)
                        break
                                                
            if curSelection is None or str(curSelection)==str(""):              # if the name of the Restriction is None or "", the material is not restricted by any selection:
                if tag.GetMaterial() is not None:                                  
                    if str(tag.GetMaterial().GetTypeName())!="Mat":                     # if this Materials-type is not a C4d-DefaultMaterial: 
                        newWarning=AWDerrorObject(ids.WARNINGMESSAGE1,tag.GetMaterial().GetName()) # create a Warning Object
                        exportData.AWDwarningObjects.append(newWarning)                     
                        newMaterialList=[]
                        newMaterialList.append(str(1))                      
                        newMaterialList.append(classesHelper.PolySelection("Base",[]))
                        newMaterialList.append(None)  
                        returnMats.append(newMaterialList)
                    if str(tag.GetMaterial().GetTypeName())=="Mat":                     # if this Materials-type is a C4d-DefaultMaterial: 
                        newMaterialList=[]
                        newMaterialList.append(tag.GetMaterial().GetName())                      
                        newMaterialList.append(classesHelper.PolySelection("Base",[]))
                        newMaterialList.append(tag)  
                        returnMats=[newMaterialList]
    if inherite==True and len(returnMats)==0:
        parentObj=curObj.GetUp()
        if parentObj is not None:
            returnMats=getMaterials(parentObj,allSelections,True)
    return returnMats
                            
# get the materials applied to a mesh. if the mesh has no texture applied, the function will be executed for its Parent-Object, so we can read out the c4d-materials inheritage			
def getObjectColorMode(curObj,textureBaseMaterial,exportData):
    
    objColorMode=curObj[c4d.ID_BASEOBJECT_USECOLOR]   

    if int(objColorMode)==int(0): # ColorMode = OFF                                                   
        newMaterialList=[]
        newMaterialList.append(str(1))    
        newMaterialList.append(classesHelper.PolySelection("Base",[]))                                      
        newMaterialList.append(None)                                                                        
        if textureBaseMaterial is not None:
            newMaterialList=textureBaseMaterial
        return True, newMaterialList                                                                                 
        
    if int(objColorMode)==int(1): # ColorMode = AUTOMATIC      
        newMaterialList=[]
        newMaterialList.append(str(getObjectColorMatBlock(exportData,curObj[c4d.ID_BASEOBJECT_COLOR]).blockID))    
        newMaterialList.append(classesHelper.PolySelection("Base",[]))                                        
        newMaterialList.append(None)                                                                           
        if textureBaseMaterial is not None:
            newMaterialList=textureBaseMaterial
        return True, newMaterialList    
        
    if int(objColorMode)==int(2): # ColorMode = ON                                               
        newMaterialList=[]                                        
        newMaterialList.append(str(getObjectColorMatBlock(exportData,curObj[c4d.ID_BASEOBJECT_COLOR]).blockID))     
        newMaterialList.append(classesHelper.PolySelection("Base",[]))                                       
        newMaterialList.append(None)
        return False, newMaterialList                                                                                  
        
    if int(objColorMode)==int(3): # ColorMode = LAYER                                                                         
        newMaterialList=[]
        objLayerData=curObj.GetLayerData(exportData.doc)
        if objLayerData is not None:
            newMaterialList.append(str(getObjectColorMatBlock(exportData,objLayerData["color"]).blockID))   
        if objLayerData is None:
            newMaterialList.append(str(1))   
        newMaterialList.append(classesHelper.PolySelection("Base",[]))                                       
        newMaterialList.append(None)           
        return False, newMaterialList                                                                                    
