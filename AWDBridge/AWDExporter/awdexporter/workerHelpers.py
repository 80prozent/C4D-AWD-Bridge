# functions that will run inside the background-worker-thread

import c4d
import copy
import struct
import os
import zlib
from awdexporter import ids
from awdexporter import classesHelper

# called by "WorkerExporter.py"
def getAllObjectData(exportData):
    for awdSceneBlock in exportData.allSceneObjects:
        awdSceneBlock.dataMatrix=awdSceneBlock.sceneObject.GetMl()
		
# called by "WorkerExporter.py"
# creates the final binary string and saves it to harddisc
def exportAllData(exportData):        
    datei=c4d.storage.SaveDialog(c4d.FILESELECTTYPE_ANYTHING, "save as *.AWD", "awd")
    if datei==None:     
        exportData.cancel=True
        return
    if datei!=None:     
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
        f = open(datei, 'wb')
        f.write(outputBits)
        f.close()
    return
	
def reorderAllBlocks(exportData):
    for awdBlock in exportData.allAWDBlocks:
        exportData.addToExportList(awdBlock)
    for awdSkeleton in exportData.allSkeletonBlocks:
        exportData.addSkeleton(awdSkeleton)
    for awdSkeletonAnimation in exportData.allSkeletonAnimations:
        exportData.addSkeletonAnimation(awdSkeletonAnimation)

def connectInstances(exportData):
    for instanceBlock in exportData.unconnectedInstances:
        geoInstanceID=instanceBlock.sceneObject[c4d.INSTANCEOBJECT_LINK].GetName()
        instanceSceneBlock=exportData.IDsToAWDBlocksDic.get(str(geoInstanceID),None)
        instanceBlock.geoBlockID=instanceSceneBlock.geoBlockID
        if instanceSceneBlock.hasTexture==True:
            materials=getObjectsMaterials(instanceSceneBlock.sceneObject)
        if instanceSceneBlock.hasTexture==False:
            allSelections=[] 
            for selectionTag in instanceSceneBlock.sceneObject.GetTags(): 
                if selectionTag.GetType()==c4d.Tpolygonselection:
                    allSelections.append(mainHelpers.PolySelection(selectionTag.GetName(),selectionTag.GetBaseSelect().GetAll(len(instanceSceneBlock.sceneObject.GetAllPolygons())))) 
            materials=mainHelpers.getObjectsMaterials(instanceBlock.sceneObject,allSelections)
        for mat in materials:
            instanceBlock.saveMaterials.append(mat[0])
	
			
			
# this is basically the same function as found in "mainHelpers", 
# but since it is run by the worker-thread i duplicated it in here.
# most likely this function will be edited soon, so it this duplicated version makes sense		
def getObjectsMaterials(curObj,allSelections=None,polygonObjectBlock=None,exportData=None):
    if allSelections==None:    
        allSelections=[] 
        for selectionTag in curObj.GetTags(): 
            if selectionTag.GetType()==c4d.Tpolygonselection:
                allSelections.append(classesHelper.PolySelection(selectionTag.GetName(),selectionTag.GetBaseSelect().GetAll(len(curObj.GetAllPolygons())))) 
    materials=[]
    selections=[]
    textureTags=[]
    foundTexturetag=False
    for tag in curObj.GetTags():
        if tag.GetType()==c4d.Ttexture:# Texture tag gefunden:
            foundTexturetag=True
            if str(tag[c4d.TEXTURETAG_RESTRICTION])!="None" or str(tag[c4d.TEXTURETAG_RESTRICTION])!="" or str(tag[c4d.TEXTURETAG_RESTRICTION])!=None:
                for selection in allSelections: 
                    if str(tag[c4d.TEXTURETAG_RESTRICTION])==selection.name:
                        if tag.GetMaterial()!= None:
                            if len(materials)==0:
                                materials.append(str(0))
                                selections=[classesHelper.PolySelection("Base",[])]
                                textureTags=[None]
                            if str(tag.GetMaterial().GetTypeName())!="Mat":
                                if exportData!=None:
                                    newWarning=AWDerrorObject(ids.WARNINGMESSAGE1,tag.GetMaterial().GetName())
                                    exportData.AWDwarningObjects.append(newWarning)
                                materials.append(str(0))
                                selections.append(selection)    
                                textureTags.append(None)    
                            if str(tag.GetMaterial().GetTypeName())=="Mat":
                                materials.append(tag.GetMaterial().GetName())
                                selections.append(selection)  
                                textureTags.append(tag)                          
            if str(tag[c4d.TEXTURETAG_RESTRICTION])=="None" or str(tag[c4d.TEXTURETAG_RESTRICTION])=="" or str(tag[c4d.TEXTURETAG_RESTRICTION])==None:
                if tag.GetMaterial()!= None:
                    if str(tag.GetMaterial().GetTypeName())!="Mat":
                        if exportData!=None:
                            newWarning=AWDerrorObject(ids.WARNINGMESSAGE1,tag.GetMaterial().GetName())
                            exportData.AWDwarningObjects.append(newWarning)
                        materials=[str(0)]
                        selections=[classesHelper.PolySelection("Base",[])]
                        textureTags=[None]
                    if str(tag.GetMaterial().GetTypeName())=="Mat":
                        materials=[tag.GetMaterial().GetName()]
                        selections=[classesHelper.PolySelection("Base",[])]
                        textureTags.append(tag)
    if foundTexturetag==False and polygonObjectBlock!=None:
        polygonObjectBlock.hasTexture=False
    returnMats=[]
    matCounter=0
    while matCounter<len(materials):
        newMaterialsSelectionCombo=[materials[matCounter],selections[matCounter],textureTags[matCounter]]
        returnMats.append(newMaterialsSelectionCombo)
        matCounter+=1
    if foundTexturetag==False and curObj.GetUp()!=None:
        returnMats=getObjectsMaterials(curObj.GetUp(),allSelections,None,exportData)
    if foundTexturetag==False and curObj.GetUp()==None:
        newMaterialsSelectionCombo=[0,classesHelper.PolySelection("Base",[]),None]
        returnMats.append(newMaterialsSelectionCombo)
    return returnMats