# some helper-functions for the part of the export process running in the c4d-mainthread

import c4d
import os
from awdexporter import ids
from awdexporter import classesHelper
from awdexporter import classesAWDBlocks

# this class is called by the "mainExporter.py" 
def createAllUsedMaterialBlocks(exportData,exportUnusedMats,objList):
    if exportUnusedMats==True:
        for mat in exportData.allc4dMaterials:
            if str(mat.GetTypeName())!="Mat":
                newWarning=classesHelper.AWDerrorObject(ids.WARNINGMESSAGE1,mat.GetName())
                exportData.AWDwarningObjects.append(newWarning)
            if str(mat.GetTypeName())=="Mat":
                exportData.allUsedc4dMaterials.append(mat.GetName())
            
    if exportUnusedMats==False:
        usedMatsDic={}
        for object in objList:
            checkObjForUsedMaterials(exportData,object,usedMatsDic)
        usedMatsDic=None
    for mat in exportData.allUsedc4dMaterials:
        if(exportData.allMaterials[int(mat)][c4d.MATERIAL_COLOR_SHADER]):
            createSingleTextureBlock(exportData,str(exportData.allMaterials[int(mat)][c4d.MATERIAL_COLOR_SHADER][c4d.BITMAPSHADER_FILENAME]))
        if(exportData.allMaterials[int(mat)][c4d.MATERIAL_DIFFUSION_SHADER]):
            createSingleTextureBlock(exportData,str(exportData.allMaterials[int(mat)][c4d.MATERIAL_DIFFUSION_SHADER][c4d.BITMAPSHADER_FILENAME]))
            
    for mat in exportData.allUsedc4dMaterials:
        createMaterialBlock(exportData,int(mat),False)
        
        
def createMaterialBlock(exportData,materialID,colormat):
    if int(materialID)>=0:
        material=exportData.allMaterials[int(materialID)]
        exportData.allMaterialsBlockIDS[int(materialID)]=exportData.idCounter
        newAWDBlock=classesAWDBlocks.StandartMaterialBlock(exportData.idCounter,0,colormat)
        exportData.IDsToAWDBlocksDic[str(exportData.idCounter)]=newAWDBlock
        exportData.allAWDBlocks.append(newAWDBlock)
        exportData.allMatBlocks.append(newAWDBlock)
        exportData.MaterialsToAWDBlocksDic[str(material)]=newAWDBlock 
        newAWDBlock.tagForExport=True 
        newAWDBlock.saveLookUpName=exportData.allMaterialsNames[int(material.GetName())]
        if material[c4d.MATERIAL_USE_COLOR]==True:
            colorVec=material[c4d.MATERIAL_COLOR_COLOR]
            newAWDBlock.matColor=[colorVec.z*255,colorVec.y*255,colorVec.x*255,0]
            newAWDBlock.saveMatProps.append(1)
            if material[c4d.MATERIAL_USE_TRANSPARENCY]==True:
                newAWDBlock.matAlpha=1.0-material[c4d.MATERIAL_TRANSPARENCY_BRIGHTNESS]
                newAWDBlock.saveMatProps.append(10)
                
            if(material[c4d.MATERIAL_COLOR_SHADER]):
                colorTexBlock=exportData.texturePathToAWDBlocksDic.get(str(material[c4d.MATERIAL_COLOR_SHADER][c4d.BITMAPSHADER_FILENAME]),None)
                if colorTexBlock!=None:
                    newAWDBlock.saveMatType=2
                    newAWDBlock.saveMatProps.append(2)
                    newAWDBlock.saveColorTextureID=colorTexBlock.blockID
        #print "material build: awdBlockid= "+str(material[c4d.MATERIAL_TRANSPARENCY_BRIGHTNESS])
        exportData.idCounter+=1

def createSingleTextureBlock(exportData,texturePath):
    if texturePath==None or str(texturePath)=="" or str(texturePath)=="None":
        return
    isInList=exportData.texturePathToAWDBlocksDic.get(str(texturePath),None)
    if isInList==None:
        pathName=os.path.basename(texturePath)
        newAWDBlock=classesAWDBlocks.TextureBlock(exportData.idCounter,0,str(texturePath),exportData.embedTextures,pathName)
        exportData.IDsToAWDBlocksDic[str(exportData.idCounter)]=newAWDBlock
        exportData.allAWDBlocks.append(newAWDBlock)
        exportData.texturePathToAWDBlocksDic[str(texturePath)]=newAWDBlock
        exportData.idCounter+=1
        extensionAr=pathName.split(".")
        extension=extensionAr[(len(extensionAr)-1)]
        filenamecount=0 
        newAWDBlock.saveLookUpName=""
        newAWDBlock.tagForExport=True
        while filenamecount<(len(extensionAr)-1):
            newAWDBlock.saveLookUpName+=extensionAr[filenamecount]
            filenamecount+=1

        if extension!="jpg" and extension!="jpeg" and extension!="JPG" and extension!="JPEG" and extension!="png" and extension!="PNG":
            exportData.AWDerrorObjects.append(classesHelper.AWDerrorObject(ids.ERRORMESSAGE3,texturePath))
            return
        inDocumentPath=texturePath
        try:
            with open(texturePath) as f: pass
        except IOError as e:
            try:
                inDocumentPath=os.path.join(c4d.documents.GetActiveDocument().GetDocumentPath(),texturePath)
                with open(inDocumentPath) as f: pass
            except IOError as e:
                try:
                    inDocumentPath=os.path.join(c4d.documents.GetActiveDocument().GetDocumentPath(),"tex",texturePath)
                    with open(inDocumentPath) as f: pass
                except IOError as e:
                    exportData.AWDerrorObjects.append(classesHelper.AWDerrorObject(ids.ERRORMESSAGE4,inDocumentPath))
                    return
        texturefile=open(str(inDocumentPath),"rb")
        if exportData.embedTextures==0:
            newAWDBlock.saveTextureData=texturefile.read()
        
        texturefile.close()




def checkObjForUsedMaterials(exportData,curObj,usedMatsDic,fromChild=False):
    exporterSettingsTag=curObj.GetTag(1028905)
    useMats=True
    if exporterSettingsTag!=None:
        if exporterSettingsTag[1016]==False and exporterSettingsTag[1016]== True:
            return
        if exporterSettingsTag[1016]==False and exporterSettingsTag[1016]== False:
            useMats=False
    if useMats==True:                
        materials=[]
        if curObj.GetType()==c4d.Oinstance:
            hasTextures=False
            for tag in curObj[c4d.INSTANCEOBJECT_LINK].GetTags():
                if tag.GetType()==c4d.Ttexture:
                    hasTextures=True
            allSelections=[]
            for selectionTag in curObj[c4d.INSTANCEOBJECT_LINK].GetTags():
                if selectionTag.GetType()==c4d.Tpolygonselection:
                    allSelections.append(classesHelper.PolySelection(selectionTag.GetName(),selectionTag.GetBaseSelect().GetAll(len(curObj[c4d.INSTANCEOBJECT_LINK].GetAllPolygons())))) 
                
            if hasTextures==True:
                materials=getObjectsMaterials(curObj[c4d.INSTANCEOBJECT_LINK],None,None,exportData)
            if hasTextures==False:
                materials=getObjectsMaterials(curObj,allSelections,None,exportData)
                
        if curObj.GetType()==c4d.Opolygon or fromChild==True:
            materials=getObjectsMaterials(curObj,None,None,exportData)
            
        for mat in materials:
            matIsinDic=usedMatsDic.get(str(mat[0]),None)
            if matIsinDic==None:
                usedMatsDic[str(mat[0])]=mat[0]
                exportData.allUsedc4dMaterials.append(mat[0])               
                      

    for objChild in curObj.GetChildren():
        checkObjForUsedMaterials(exportData,objChild,usedMatsDic,True)
        
        
            
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