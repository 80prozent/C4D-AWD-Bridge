import c4d
import copy
import struct
import os
from c4d import documents
import zlib


from c4d import bitmaps, gui, plugins, utils, modules, documents

from awdexporter import ids
from awdexporter import awdC4DObjectsReader
from awdexporter import awdBlocks
from awdexporter import awdMeshReader
from awdexporter import awdHelpers

class AWDerrorObject(object):
    def __init__(self, errorID=None,errorData=None):
        self.errorID=errorID
        self.errorData=errorData

class objectSettings(object):
    def __init__(self):
        pass
class mainScene(object):
    def __init__(self, name=None,mainDialog=None,fps=None):

        self.name = name
        self.animationCounter=0
        self.allStatusLength = 0
        self.allStatus = 0
        self.subStatus = 0
        self.status = 0
        self.exportColorMats = mainDialog.GetBool(ids.CBOX_OBJECTCOLORS)
        self.scale = mainDialog.GetReal(ids.REAL_SCALE)
        self.firstFrame=mainDialog.GetReal(ids.REAL_FIRSTFRAME)
        self.lastFrame=mainDialog.GetReal(ids.REAL_LASTFRAME)
        self.selectedOnly=mainDialog.GetReal(ids.CBOX_SELECTEDONLY)
        self.unusedMats=mainDialog.GetReal(ids.CBOX_UNUSEDMATS) 
        self.debug=mainDialog.GetBool(ids.CBOX_DEBUG)        
        self.embedTextures=mainDialog.GetLong(ids.COMBO_TEXTURESMODE)
        self.copyTextures=mainDialog.GetBool(ids.CBOX_COPYTEX)
        texturesURL=mainDialog.GetString(ids.LINK_EXTERNTEXTURESPATH)
        self.externalFilePath=""
        if texturesURL!=None:
            self.externalFilePath=texturesURL
		
        self.headerMagicString = "AWD"
        self.headerVersionNumberMajor = 0
        self.headerVersionNumberMinor = 0   
        
        self.headerFlagBits=0x0
        if mainDialog.GetBool(ids.CBOX_STREAMING)==True:
            self.headerFlagBits=0x1
			
        self.headerCompressionType=0
        if mainDialog.GetBool(ids.CBOX_COMPRESSED)==True:
            self.headerCompressionType=1
					
        self.IDsToAWDBlocksDic = {}                
        self.texturePathToAWDBlocksDic = {}        
        self.MaterialsToAWDBlocksDic = {}
        self.jointIDstoJointBlocks = {}
        self.jointIDstoSkeletonBlocks = {}
        self.objectsIDsDic = {}
        self.skeletonIDsDic = {}
        self.meshIDsDic = {}
        self.lightsIDsDic = {}
        self.materialsIDsDic = {}
        self.cameraIDsDic = {}
        self.texturesIDsDic = {}   
        self.allObjectsDic = {}
        self.unusedIDsDic = {}   
        self.blockDic = {}    
        self.geoDic = {}    
        self.texDic = {}    
        self.materialsDic = {}   

        self.allMatBlocks = []
        self.originalActiveObjects = []
        self.originalActiveTags = []
        self.originalActiveMaterials = []
        self.objList = []
        self.allSaveAWDBlocks = []
        self.allAWDBlocks = []
        self.allc4dObjects = []
        self.allc4dMaterials = c4d.documents.GetActiveDocument().GetMaterials()
        self.allUsedc4dMaterials = []
        self.AWDerrorObjects = []
        self.AWDwarningObjects = []
        self.errorMessages=[0]
        self.unconnectedInstances = []
        self.allSceneObjects = []
        self.allMeshObjects = []
        self.allSkeletonBlocks = []
        self.allMaterialsNames = []
        self.allMaterialsBlockIDS = []
        self.allMaterials = []
        self.reorderedAWDBlockss = []
        self.settings = []
        self.allSceneObjects = []
        self.allGeometries = []
        self.allSkeletons = []
        self.allSkeletonAnimations = []
        self.allAnimations = []
        self.allLightPickers = []
        self.allTextures = []   
        self.allMaterials = []   
        self.allAnimations = []

        self.saveTexturesEmbed = True
        self.cancel=False
        self.parsingOK=False
		
        self.bodyLength=0
        self.path = ""

        self.idCounter = 0
        self.defaultObjectSettings = 0

        self.texturesExternPathMode = 0  
        self.texturesEmbedPathMode = 0  
        self.texturesExternPath = None  
        self.texturesEmbedPath = None  

    def exportAllData(self):

        
        datei=c4d.storage.SaveDialog(c4d.FILESELECTTYPE_ANYTHING, "save as *.AWD", "awd")
        if datei==None:     
            self.cancel=True
            return
        if datei!=None:     
            outputBits=struct.pack('< 3s',self.headerMagicString)
            outputBits+=struct.pack('< B',self.headerVersionNumberMajor)
            outputBits+=struct.pack('< B',self.headerVersionNumberMinor)
            outputBits+=struct.pack('< H',self.headerFlagBits)
            outputBits+=struct.pack('< B',self.headerCompressionType)
            outputBlocks=str()
            blocksparsed=0
            while blocksparsed<len(self.allSaveAWDBlocks):
                outputBlocks+=self.allSaveAWDBlocks[blocksparsed].writeBinary(self)
                blocksparsed+=1
            if self.headerCompressionType==1:
                outputBody = zlib.compress(outputBlocks, 9)
            if self.headerCompressionType==0:
                outputBody = outputBlocks

            outputBits+=struct.pack('< I',len(outputBody))
            outputBits+=outputBody
            f = open(datei, 'wb')
            f.write(outputBits)
            f.close()
        return

    def connectInstances(self):
        for instanceBlock in self.unconnectedInstances:
            geoInstanceID=instanceBlock.sceneObject[c4d.INSTANCEOBJECT_LINK].GetName()
            instanceSceneBlock=self.IDsToAWDBlocksDic.get(str(geoInstanceID),None)
            instanceBlock.geoBlockID=instanceSceneBlock.geoBlockID
            if instanceSceneBlock.hasTexture==True:
                materials=awdHelpers.getObjectsMaterials(instanceSceneBlock.sceneObject)
            if instanceSceneBlock.hasTexture==False:
                allSelections=[] 
                for selectionTag in instanceSceneBlock.sceneObject.GetTags(): 
                    if selectionTag.GetType()==c4d.Tpolygonselection:
                        allSelections.append(awdHelpers.PolySelection(selectionTag.GetName(),selectionTag.GetBaseSelect().GetAll(len(instanceSceneBlock.sceneObject.GetAllPolygons())))) 
                materials=awdHelpers.getObjectsMaterials(instanceBlock.sceneObject,allSelections)
            for mat in materials:
                instanceBlock.saveMaterials.append(mat[0])

    def getAllObjectData(self):
        for awdSceneBlock in self.allSceneObjects:
            awdSceneBlock.dataMatrix=awdSceneBlock.sceneObject.GetMl()


    def reorderAllBlocks(self):
        for awdBlock in self.allAWDBlocks:
            self.addToExportList(awdBlock)
        for awdSkeleton in self.allSkeletonBlocks:
            self.addSkeleton(awdSkeleton)
        for awdSkeletonAnimation in self.allSkeletonAnimations:
            self.addSkeletonAnimation(awdSkeletonAnimation)
        
    def addSkeleton(self,awdSkeleton):
        if awdSkeleton.tagForExport==True:
            awdSkeleton.saveBlockID=len(self.allSaveAWDBlocks)
            self.allSaveAWDBlocks.append(awdSkeleton)

    def addSkeletonPose(self,awdSkeletonPose):
        awdSkeletonPose.saveBlockID=len(self.allSaveAWDBlocks)
        self.allSaveAWDBlocks.append(awdSkeletonPose)
        return awdSkeletonPose.saveBlockID

    def addSkeletonAnimation(self,awdSkeletonAnimation):
        if awdSkeletonAnimation.tagForExport==True:
            poseCouunt=0
            for pose in awdSkeletonAnimation.framesIDSList:
                skelPoseBlock=self.IDsToAWDBlocksDic.get(str(pose),None)
                if skelPoseBlock==None:
                    pass#warning
                if skelPoseBlock!=None:
                    awdSkeletonAnimation.framesIDSList2.append(self.addSkeletonPose(skelPoseBlock))
            awdSkeletonAnimation.saveBlockID=len(self.allSaveAWDBlocks)
            self.allSaveAWDBlocks.append(awdSkeletonAnimation)

    def addToExportList(self,awdBlock):
        if awdBlock.isReordered==True:
            return awdBlock.saveBlockID
        if awdBlock.isReordered==False:
            if awdBlock.tagForExport==True:
                if awdBlock.blockType==1:
                    pass#triangel
                if awdBlock.blockType==11:
                    pass#primitive
                if awdBlock.blockType==21:
                    pass#scene
                if awdBlock.blockType==22:#container
                    parentBlock=self.IDsToAWDBlocksDic.get(str(awdBlock.dataParentBlockID),None)
                    if parentBlock!=None:
                        awdBlock.dataParentBlockID=self.addToExportList(parentBlock)
                if awdBlock.blockType==23:#meshinstance
                    parentBlock=self.IDsToAWDBlocksDic.get(str(awdBlock.dataParentBlockID),None)
                    if parentBlock!=None:
                        awdBlock.dataParentBlockID=self.addToExportList(parentBlock)
                    geoBlock=self.IDsToAWDBlocksDic.get(str(awdBlock.geoBlockID),None)
                    if geoBlock!=None:
                        awdBlock.geoBlockID=self.addToExportList(geoBlock)                    
                    if len(geoBlock.saveSubMeshes)<len(awdBlock.saveMaterials):
                        awdBlock.saveMaterials.pop(0)
                    awdBlock.saveMaterials2=[]
                    for mat in awdBlock.saveMaterials:
                        matBlockID=int(self.allMaterialsBlockIDS[int(mat)])
                        if int(matBlockID)<0:
                            matBlockID=int(self.allMaterialsBlockIDS[0])
                        matBlock=self.allAWDBlocks[int(matBlockID)]
                        awdBlock.saveMaterials2.append(matBlock.saveBlockID)
                    while len(awdBlock.saveMaterials2)<len(geoBlock.saveSubMeshes):
                        matBlockID=int(self.allMaterialsBlockIDS[0])
                        matBlock=self.allAWDBlocks[int(matBlockID)]
                        awdBlock.saveMaterials2.append(matBlock.saveBlockID)
                        
                if awdBlock.blockType==41:#light
                    parentBlock=self.IDsToAWDBlocksDic.get(str(awdBlock.dataParentBlockID),None)
                    if parentBlock!=None:
                        awdBlock.dataParentBlockID=self.addToExportList(parentBlock)
                if awdBlock.blockType==42:#camera
                    parentBlock=self.IDsToAWDBlocksDic.get(str(awdBlock.dataParentBlockID),None)
                    if parentBlock!=None:
                        awdBlock.dataParentBlockID=self.addToExportList(parentBlock)
                if awdBlock.blockType==81:#material
                    if awdBlock.saveMatType==2:
                        textureBlock=self.IDsToAWDBlocksDic.get(str(awdBlock.saveColorTextureID),None)
                        if textureBlock!=None:
                            awdBlock.saveColorTextureID=self.addToExportList(textureBlock)
                            
                if awdBlock.blockType==82:#texture
                    pass
                if awdBlock.blockType==83:#cubetexture
                    pass
                if awdBlock.blockType==101:#skeleton
                    return 0
                if awdBlock.blockType==102:#skeletonpose
                    return 0
                if awdBlock.blockType==103:#skeletonanimation
                    return 0
                if awdBlock.blockType==121:#uvanimation
                    pass
                if awdBlock.blockType==254:#NameSpace
                    pass
                if awdBlock.blockType==255:#metadata
                    pass
                awdBlock.saveBlockID=int(len(self.allSaveAWDBlocks))
                awdBlock.isReordered=True
                self.allSaveAWDBlocks.append(awdBlock)
                return awdBlock.saveBlockID


    def createMaterialBlock(self,materialID,colormat):
        if int(materialID)>=0:
            material=self.allMaterials[int(materialID)]
            self.allMaterialsBlockIDS[int(materialID)]=self.idCounter
            newAWDBlock=awdBlocks.StandartMaterialBlock(self.idCounter,0,colormat)
            self.IDsToAWDBlocksDic[str(self.idCounter)]=newAWDBlock
            self.allAWDBlocks.append(newAWDBlock)
            self.allMatBlocks.append(newAWDBlock)
            self.MaterialsToAWDBlocksDic[str(material)]=newAWDBlock 
            newAWDBlock.tagForExport=True 
            newAWDBlock.saveLookUpName=self.allMaterialsNames[int(material.GetName())]
            if material[c4d.MATERIAL_USE_COLOR]==True:
                colorVec=material[c4d.MATERIAL_COLOR_COLOR]
                newAWDBlock.matColor=[colorVec.z*255,colorVec.y*255,colorVec.x*255,0]
                newAWDBlock.saveMatProps.append(1)
                if material[c4d.MATERIAL_USE_TRANSPARENCY]==True:
                    newAWDBlock.matAlpha=1.0-material[c4d.MATERIAL_TRANSPARENCY_BRIGHTNESS]
                    newAWDBlock.saveMatProps.append(10)
                    
                if(material[c4d.MATERIAL_COLOR_SHADER]):
                    colorTexBlock=self.texturePathToAWDBlocksDic.get(str(material[c4d.MATERIAL_COLOR_SHADER][c4d.BITMAPSHADER_FILENAME]),None)
                    if colorTexBlock!=None:
                        newAWDBlock.saveMatType=2
                        newAWDBlock.saveMatProps.append(2)
                        newAWDBlock.saveColorTextureID=colorTexBlock.blockID
            print "material build: awdBlockid= "+str(material[c4d.MATERIAL_TRANSPARENCY_BRIGHTNESS])
            self.idCounter+=1

    def createSingleTextureBlock(self,texturePath):
        if texturePath==None or str(texturePath)=="" or str(texturePath)=="None":
            return
        isInList=self.texturePathToAWDBlocksDic.get(str(texturePath),None)
        if isInList==None:
            pathName=os.path.basename(texturePath)
            newAWDBlock=awdBlocks.TextureBlock(self.idCounter,0,str(texturePath),self.embedTextures,pathName)
            self.IDsToAWDBlocksDic[str(self.idCounter)]=newAWDBlock
            self.allAWDBlocks.append(newAWDBlock)
            self.texturePathToAWDBlocksDic[str(texturePath)]=newAWDBlock
            self.idCounter+=1
            extensionAr=pathName.split(".")
            extension=extensionAr[(len(extensionAr)-1)]
            filenamecount=0 
            newAWDBlock.saveLookUpName=""
            newAWDBlock.tagForExport=True
            while filenamecount<(len(extensionAr)-1):
                newAWDBlock.saveLookUpName+=extensionAr[filenamecount]
                filenamecount+=1

            if extension!="jpg" and extension!="jpeg" and extension!="JPG" and extension!="JPEG" and extension!="png" and extension!="PNG":
                self.AWDerrorObjects.append(AWDerrorObject(ids.ERRORMESSAGE3,texturePath))
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
                        self.AWDerrorObjects.append(AWDerrorObject(ids.ERRORMESSAGE4,inDocumentPath))
                        return
            texturefile=open(str(inDocumentPath),"rb")
            if self.embedTextures==0:
                newAWDBlock.saveTextureData=texturefile.read()
            
            texturefile.close()

    def createAllUsedTextureAndMaterialBlocks(self,exportUnusedMats,objList):
        if exportUnusedMats==True:
            for mat in self.allc4dMaterials:
                if str(mat.GetTypeName())!="Mat":
                    newWarning=AWDerrorObject(ids.WARNINGMESSAGE1,mat.GetName())
                    self.AWDwarningObjects.append(newWarning)
                if str(mat.GetTypeName())=="Mat":
                    self.allUsedc4dMaterials.append(mat)
            
        if exportUnusedMats==False:
            usedMatsDic={}
            for object in objList:
                self.checkObjForUsedMaterials(object,usedMatsDic)
            usedMatsDic=None
        for mat in self.allUsedc4dMaterials:
            if(self.allMaterials[int(mat)][c4d.MATERIAL_COLOR_SHADER]):
                self.createSingleTextureBlock(str(self.allMaterials[int(mat)][c4d.MATERIAL_COLOR_SHADER][c4d.BITMAPSHADER_FILENAME]))
            if(self.allMaterials[int(mat)][c4d.MATERIAL_DIFFUSION_SHADER]):
                self.createSingleTextureBlock(str(self.allMaterials[int(mat)][c4d.MATERIAL_DIFFUSION_SHADER][c4d.BITMAPSHADER_FILENAME]))
            
        for mat in self.allUsedc4dMaterials:
            self.createMaterialBlock(mat,False)


    def checkObjForUsedMaterials(self,curObj,usedMatsDic,fromChild=False):
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
                        allSelections.append(awdHelpers.PolySelection(selectionTag.GetName(),selectionTag.GetBaseSelect().GetAll(len(curObj[c4d.INSTANCEOBJECT_LINK].GetAllPolygons())))) 
                
                if hasTextures==True:
                    materials=awdHelpers.getObjectsMaterials(curObj[c4d.INSTANCEOBJECT_LINK],None,None,self)
                if hasTextures==False:
                    materials=awdHelpers.getObjectsMaterials(curObj,allSelections,None,self)
                
            if curObj.GetType()==c4d.Opolygon or fromChild==True:
                materials=awdHelpers.getObjectsMaterials(curObj,None,None,self)
            
            for mat in materials:
                matIsinDic=usedMatsDic.get(str(mat[0]),None)
                if matIsinDic==None:
                    usedMatsDic[str(mat[0])]=mat[0]
                    self.allUsedc4dMaterials.append(mat[0])               
                      

        for objChild in curObj.GetChildren():
            self.checkObjForUsedMaterials(objChild,usedMatsDic,True)
            
    def createAllSceneBlocks(self,objList,parentExportSettings=None,tagForExport=True,returner=True):
        for object in objList:
            exporterSettingsTag=object.GetTag(1028905)
            thisExporterSettings=parentExportSettings
            exportThisObj=True
            returnerAR=[False,False]
            if exporterSettingsTag==None:
                returnerAR=awdC4DObjectsReader.createSceneBlock(self,object,tagForExport,returner,False)
                
            if exporterSettingsTag!=None:
                if exporterSettingsTag[1014]==False and exporterSettingsTag[1016]== True:
                    pass
                if exporterSettingsTag[1014]==True and exporterSettingsTag[1016]== True:
                    returnerAR=awdC4DObjectsReader.createSceneBlock(self,object,tagForExport,returner,False)
                if exporterSettingsTag[1014]==True and exporterSettingsTag[1016]== False:
                    returnerAR=awdC4DObjectsReader.createSceneBlock(self,object,tagForExport,returner,False)
                if exporterSettingsTag[1014]==False and exporterSettingsTag[1016]== False:
                    returnerAR=awdC4DObjectsReader.createSceneBlock(self,object,tagForExport,returner,True)
            if returnerAR[0]==True:
                self.createAllSceneBlocks(object.GetChildren(),thisExporterSettings,returnerAR[1],returnerAR[0])
                                