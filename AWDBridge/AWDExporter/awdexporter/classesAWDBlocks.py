# different classes for different types of awd-blocks, all inheriting from the "BaseBlock"-class
# these classes are used for storing awd-block-data
# a BaseBlock-Class has a function called "writeBinary" wich will wirte out the binary Data of a Block.
# the "writeBinary" functions are all called by "workerHelpers.py function exportAllData"

import c4d
import struct



class BaseBlock(object):# baseclass for all blocks - not to be instanced directly
    def __init__(self,blockID=0,nameSpace=0,blockType=0):
        self.blockID = blockID
        self.saveBlockID = 0
        self.nameSpace = nameSpace
        self.blockType = blockType
        self.blockFlags= 0
        self.blockSize= 0
        self.isSkinned=False
        self.dataParentBlockID=-1
        self.saveColorTextureID= -1
        self.tagForExport = False # part of a workarround
        self.isReordered = False
        self.objectSettings= 0

    def writeBinary(self,exportData):
        outputBits=struct.pack("< I",self.saveBlockID)
        outputBits+=struct.pack("< B",self.nameSpace)
        outputBits+=struct.pack("< B",self.blockType)
        outputBits+=struct.pack("< B",self.blockFlags)
        if exportData.debug==True:
            print "_"
            print "Exported Block:     BlockID= "+str(self.saveBlockID)+" NameSpcae= "+str(self.nameSpace)+" blockType= "+str(self.blockType) 
        return outputBits


class BaseSceneContainerBlock(BaseBlock):# baseclass for sceneObjects - not to be instanced directly 
    
    def __init__(self,blockID=0,nameSpace=0,sceneObject=None,blockType=0):
        super(BaseSceneContainerBlock, self ).__init__(blockID,nameSpace,blockType)
        self.sceneObject=sceneObject
        self.dataParentBlockID=0
        self.dataMatrix=c4d.Matrix()

    def writeBinary(self,exportData):
        baseBlockBytes=super(BaseSceneContainerBlock, self).writeBinary(exportData)
        outputBits=struct.pack("< I",self.dataParentBlockID)
        outputBits+=struct.pack("< f",self.dataMatrix.v1.x)+struct.pack("< f",self.dataMatrix.v1.y)+struct.pack("< f",self.dataMatrix.v1.z)
        outputBits+=struct.pack("< f",self.dataMatrix.v2.x)+struct.pack("< f",self.dataMatrix.v2.y)+struct.pack("< f",self.dataMatrix.v2.z)
        outputBits+=struct.pack("< f",self.dataMatrix.v3.x)+struct.pack("< f",self.dataMatrix.v3.y)+struct.pack("< f",self.dataMatrix.v3.z)
        outputBits+=struct.pack("< f",self.dataMatrix.off.x*exportData.scale)+struct.pack("< f",self.dataMatrix.off.y*exportData.scale)+struct.pack("< f",self.dataMatrix.off.z*exportData.scale)
        outputBits+=struct.pack("< H",len (self.name))+str(self.name)
        if exportData.debug==True:
            print "ParentBlockID= "+str(self.dataParentBlockID)
        return baseBlockBytes, outputBits

class TriangleGeometrieBlock(BaseBlock):
    def __init__(self,blockID=0,nameSpace=0,sceneObject=None):
        super(TriangleGeometrieBlock, self ).__init__(blockID,nameSpace,1)
        self.sceneObject = sceneObject
        c4d.documents.GetActiveDocument().SetActiveObject(sceneObject)
        self.copiedMesh = self.sceneObject.GetClone()
        c4d.documents.GetActiveDocument().InsertObject(self.copiedMesh,sceneObject.GetUp(),sceneObject)
        c4d.documents.GetActiveDocument().SetActiveObject(self.copiedMesh)   
        c4d.CallCommand(14048)
        c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
        c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
        c4d.EventAdd(c4d.EVENT_ANIMATE)
        self.isSkinned=False
        self.polygonObject = None
        self.allJointIndexe = []
        self.allJointWeights = []
        self.numJoints = []
        self.indexDics = []
        self.maxJointIndex = []
        self.jointTranslater = []
        self.minJointIndex = []
        self.SubmeshPointCount = []
        self.SubmeshTrisCount = []
        #self.copiedMesh = None
        self.pointsUsed = []
        self.pointsUsed = []
        self.weightTag=None

        self.saveLookUpName = "testName"
        self.saveGeometryProps = []
        self.saveSubMeshes = []
        self.saveUserAttributes = []

    def writeBinary(self,exportData):
        baseBlockBytes=super(TriangleGeometrieBlock, self).writeBinary(exportData)
        triangleGeometrieBlockBytes=struct.pack("< H",len(self.saveLookUpName))+str(self.saveLookUpName)
        triangleGeometrieBlockBytes+=struct.pack("< H",len(self.saveSubMeshes))
        triangleGeometrieBlockBytes+=struct.pack("< I",len(self.saveGeometryProps))
        if exportData.debug==True:
            print "SubMeshes Length = "+str(len(self.saveSubMeshes))
        subMeshCount=0
        while subMeshCount<len(self.saveSubMeshes):
            subMeshBlockBytes=self.saveSubMeshes[subMeshCount].writeBinary(exportData)
            triangleGeometrieBlockBytes+=struct.pack("< I",int(len(subMeshBlockBytes)-8))+subMeshBlockBytes
            subMeshCount+=1
        triangleGeometrieBlockBytes+=struct.pack("< I",len(self.saveUserAttributes))
        return baseBlockBytes+struct.pack("< I",len(triangleGeometrieBlockBytes))+triangleGeometrieBlockBytes


class PrimitiveGeometrieBlock(BaseBlock):
    def __init__(self):
        self.name = "undefined"
    def writeBinary(self,exportData):
        baseBlockBytes=super(PrimitiveGeometrieBlock, self).writeBinary(exportData)
        return baseBlockBytes+struct.pack("< I",0)


class ContainerBlock(BaseSceneContainerBlock):
    
    def __init__(self,blockID=0,nameSpace=0,sceneObject=None):
        super(ContainerBlock, self ).__init__(blockID,nameSpace,sceneObject,22)

    def writeBinary(self,exportData):
        baseBlockBytes,sceneBlockBytes=super(ContainerBlock, self).writeBinary(exportData)
        sceneBlockBytes+=struct.pack("< I",0)
        sceneBlockBytes+=struct.pack("< I",0)
        return baseBlockBytes+struct.pack("< I",len(sceneBlockBytes))+sceneBlockBytes
    
class MeshInstanceBlock(BaseSceneContainerBlock):
    def __init__(self,blockID=0,nameSpace=0,geoBlockID=None,sceneObject=None):
        super(MeshInstanceBlock, self ).__init__(blockID,nameSpace,sceneObject,23)
        self.geoBlockID=geoBlockID
        self.geoObj=None
        self.saveMaterials=[]
        self.saveMaterials2=[]
    def writeBinary(self,exportData):
        baseBlockBytes,sceneBlockBytes=super(MeshInstanceBlock, self).writeBinary(exportData)
        sceneBlockBytes+=struct.pack("< I",self.geoBlockID)
        if exportData.debug==True:
            print "MeshInstance GeometryID = "+str(self.geoBlockID)+" Materials = "+str(self.saveMaterials2)
        sceneBlockBytes+=struct.pack("< H",len(self.saveMaterials2))
        for mat in self.saveMaterials2:
            sceneBlockBytes+=struct.pack("< I",int(mat))
        
        sceneBlockBytes+=struct.pack("< I",0)
        sceneBlockBytes+=struct.pack("< I",0)
        return baseBlockBytes+struct.pack("< I",len(sceneBlockBytes))+sceneBlockBytes

class LightBlock(BaseSceneContainerBlock):
    def __init__(self,blockID=0,nameSpace=0,sceneObject=None):
        super(LightBlock, self ).__init__(blockID,nameSpace,sceneObject,41)
        self.name = "undefined"
        self.lightType = 1
        self.lightProps = []
        self.nearRadius = 0.0
        self.farRadius = 0.0
        self.color = []
        self.specIntestity = 0.0
        self.diffuseIntensity = 0.0
        self.castShadows = False
    def writeBinary(self,exportData):
        baseBlockBytes,sceneBlockBytes=super(LightBlock, self).writeBinary(exportData)
        sceneBlockBytes+=struct.pack("< B",self.lightType)
        lightAttributesBytes=str()
        for lightProperty in self.lightProps:
            if lightProperty==1:
                lightAttributesBytes+=struct.pack("< H",lightProperty)
                lightAttributesBytes+=struct.pack("< I",4)
                lightAttributesBytes+=struct.pack("< f",float(self.nearRadius))
            if lightProperty==2:
                lightAttributesBytes+=struct.pack("< H",lightProperty)
                lightAttributesBytes+=struct.pack("< I",4)
                lightAttributesBytes+=struct.pack("< f",float(self.farRadius))
            if lightProperty==3:
                lightAttributesBytes+=struct.pack("< I",4)
                lightAttributesBytes+=struct.pack("< B",int(self.color[0]))
                lightAttributesBytes+=struct.pack("< B",int(self.color[1]))
                lightAttributesBytes+=struct.pack("< B",int(self.color[2]))
                lightAttributesBytes+=struct.pack("< B",int(self.color[3]))
            if lightProperty==4:
                lightAttributesBytes+=struct.pack("< H",lightProperty)
                lightAttributesBytes+=struct.pack("< I",4)
                lightAttributesBytes+=struct.pack("< f",float(self.specIntestity))
            if lightProperty==5:
                lightAttributesBytes+=struct.pack("< H",lightProperty)
                lightAttributesBytes+=struct.pack("< I",4)
                lightAttributesBytes+=struct.pack("< f",float(self.diffuseIntensity))
            if lightProperty==10:
                lightAttributesBytes+=struct.pack("< H",lightProperty)
                lightAttributesBytes+=struct.pack("< I",1)
                lightAttributesBytes+=struct.pack("< B",self.castShadows)

        sceneBlockBytes+=struct.pack("< I",len(lightAttributesBytes))+str(lightAttributesBytes)
        sceneBlockBytes+=struct.pack("< I",0)
        return baseBlockBytes+struct.pack("< I",len(sceneBlockBytes))+sceneBlockBytes

class CameraBlock(BaseSceneContainerBlock):
    def __init__(self):
        self.name = "undefined"
    def writeBinary(self,exportData):
        baseBlockBytes,sceneBlockBytes=super(CameraBlock, self).writeBinary(exportData)
        sceneBlockBytes+=struct.pack("< I",0)
        sceneBlockBytes+=struct.pack("< I",0)
        return baseBlockBytes+struct.pack("< I",len(sceneBlockBytes))+sceneBlockBytes

class StandartMaterialBlock(BaseBlock):
    def __init__(self,blockID=None,nameSpace=None,colorMat=False):
        super(StandartMaterialBlock, self ).__init__(blockID,nameSpace,81)
        self.lookUpName = None
        self.matType = 0
        self.numShadingMethods = 0
        self.materialProperties = None
        self.shaderMethods = []
        self.colorTextureID = None
        self.userAttributes = None
        self.colorMat = colorMat

        self.saveLookUpName = ""
        self.saveMatType = 1
        self.saveShaders = []
        self.saveMatProps = []
        self.saveMatAtts = []
        self.saveColorTextureID = 0
        self.matColor = []
        self.matAlpha = 1.0

    def writeBinary(self,exportData):
        baseBlockBytes=super(StandartMaterialBlock, self).writeBinary(exportData)
        materialBlockBytes=struct.pack("< H",len(self.saveLookUpName))+str(self.saveLookUpName)
        materialBlockBytes+=struct.pack("< B",self.saveMatType)
        materialBlockBytes+=struct.pack("< B",len(self.saveShaders))
        materialBAttributesBytes=str()
        if exportData.debug==True:
            print "Material Color = "+str(int(self.matColor[0]))+" / "+str(int(self.matColor[1]))+" / "+str(int(self.matColor[2]))+" / "+str(int(self.matColor[3]))
            print "Material matAlpha = "+str((self.matAlpha))
        for matProperty in self.saveMatProps:
            if matProperty==1:
                materialBAttributesBytes+=struct.pack("< H",matProperty)
                materialBAttributesBytes+=struct.pack("< I",4)
                materialBAttributesBytes+=struct.pack("< B",int(self.matColor[0]))
                materialBAttributesBytes+=struct.pack("< B",int(self.matColor[1]))
                materialBAttributesBytes+=struct.pack("< B",int(self.matColor[2]))
                materialBAttributesBytes+=struct.pack("< B",int(self.matColor[3]))
            if matProperty==2:
                materialBAttributesBytes+=struct.pack("< H",matProperty)
                materialBAttributesBytes+=struct.pack("< I",4)
                materialBAttributesBytes+=struct.pack("< I",int(self.saveColorTextureID))
            if matProperty==10:
                materialBAttributesBytes+=struct.pack("< H",matProperty)
                materialBAttributesBytes+=struct.pack("< I",4)
                materialBAttributesBytes+=struct.pack("< f",self.matAlpha)
            #materialBAttributesBytes+=struct.pack("< H",matProperty.propID)
            #materialBAttributesBytes+=struct.pack("< H",matProperty.propID)

        materialBlockBytes+=struct.pack("< I",len(materialBAttributesBytes))+str(materialBAttributesBytes)
        #materialBlockBytes+=struct.pack("< I",len(self.saveMatProps))
        #materialBlockBytes+=struct.pack("< I",len(self.saveShaders))
        materialBlockBytes+=struct.pack("< I",len(self.saveMatAtts))
        return baseBlockBytes+struct.pack("< I",len(materialBlockBytes))+materialBlockBytes

class TextureBlock(BaseBlock):
    def __init__(self,blockID=None,nameSpace=None,c4dfilePath=None,saveIsEmbed=0,saveFileName=None):
        super(TextureBlock, self ).__init__(blockID,nameSpace,82)
        self.c4dfilePath = c4dfilePath
        if saveIsEmbed==0:
            self.saveIsEmbed = 1
        if saveIsEmbed==1:
            self.saveIsEmbed = 0

        
        self.saveFileName = saveFileName
        self.saveTextureProps=[]
        self.saveTextureAtts=[]
        self.saveTextureData=None
    def writeBinary(self,exportData):
        baseBlockBytes=super(TextureBlock, self).writeBinary(exportData)
        textureBlockBytes=struct.pack("< H",len(self.saveLookUpName))+str(self.saveLookUpName)
        textureBlockBytes+=struct.pack("< B",self.saveIsEmbed)
        if self.saveIsEmbed==0:
            textureData=str(self.saveFileName)
            textureBlockBytes+=struct.pack("< I",len(textureData))+textureData
        if self.saveIsEmbed==1 or self.saveIsEmbed==2:
            textureBlockBytes+=struct.pack("< I",len(self.saveTextureData))+self.saveTextureData

        textureBlockBytes+=struct.pack("< I",len(self.saveTextureProps))
        textureBlockBytes+=struct.pack("< I",len(self.saveTextureAtts))
        #print "external texture2"
        return baseBlockBytes+struct.pack("< I",int(len(textureBlockBytes)))+textureBlockBytes

class CubeTextureBlock(BaseBlock):
    def __init__(self):
        self.isSkinned=False
        self.polygonObject = None
        self.sceneObject = None
    def writeBinary(self,exportData):
        baseBlockBytes=super(CubeTextureBlock, self).writeBinary(exportData)
        return baseBlockBytes+struct.pack("< I",0)

class jointBlock(object):
    def __init__(self,jointID,parentID,jointObj):
        self.jointID=jointID
        self.parentID = parentID
        self.jointObj = jointObj
        self.transMatrix = c4d.Matrix()
        self.lookUpName = "None"

class SkeletonBlock(BaseBlock):
    def __init__(self,blockID=None,nameSpace=None,skeletonName=None,skeletonRoot=None):
        super(SkeletonBlock, self ).__init__(blockID,nameSpace,101)
        self.skeletonName = skeletonName
        self.numJoints = 0
        self.skeletonRoot = skeletonRoot   
        self.jointList=[]   
        self.hasRetargetTag=None   
        self.tPoseObject=None   
        self.refObject=None   
        self.saveJointList=[]   
    def writeBinary(self,exportData):
        baseBlockBytes=super(SkeletonBlock, self).writeBinary(exportData)
        skeletonBlockBytes=struct.pack("< H",len(self.skeletonName))+str(self.skeletonName)
        skeletonBlockBytes+=struct.pack("< H",len(self.saveJointList))
        skeletonBlockBytes+=struct.pack("< I",0)
        for joint in self.saveJointList:
            skeletonBlockBytes+=struct.pack("< H",joint.jointID)
            skeletonBlockBytes+=struct.pack("< H",joint.parentID)
            skeletonBlockBytes+=struct.pack("< H",len(joint.lookUpName))+str(joint.lookUpName)
            skeletonBlockBytes+=struct.pack("< f",joint.transMatrix.v1.x)+struct.pack("< f",joint.transMatrix.v1.y)+struct.pack("< f",joint.transMatrix.v1.z)
            skeletonBlockBytes+=struct.pack("< f",joint.transMatrix.v2.x)+struct.pack("< f",joint.transMatrix.v2.y)+struct.pack("< f",joint.transMatrix.v2.z)
            skeletonBlockBytes+=struct.pack("< f",joint.transMatrix.v3.x)+struct.pack("< f",joint.transMatrix.v3.y)+struct.pack("< f",joint.transMatrix.v3.z)
            skeletonBlockBytes+=struct.pack("< f",joint.transMatrix.off.x*exportData.scale)+struct.pack("< f",joint.transMatrix.off.y*exportData.scale)+struct.pack("< f",joint.transMatrix.off.z*exportData.scale)
            skeletonBlockBytes+=struct.pack("< I",0)
            skeletonBlockBytes+=struct.pack("< I",0)
        skeletonBlockBytes+=struct.pack("< I",0)
        return baseBlockBytes+struct.pack("< I",len(skeletonBlockBytes))+skeletonBlockBytes

class SkeletonPoseBlock(BaseBlock):
    def __init__(self,blockID=None,nameSpace=None,skeletonPoseName=None):
        super(SkeletonPoseBlock, self ).__init__(blockID,nameSpace,102)
        self.skeletonPoseName = skeletonPoseName
        self.numJoints = 0
        self.transformations = []
    def writeBinary(self,exportData):
        baseBlockBytes=super(SkeletonPoseBlock, self).writeBinary(exportData)
        skeletonPoseBlockBytes=struct.pack("< H",len(self.skeletonPoseName))+str(self.skeletonPoseName)
        skeletonPoseBlockBytes+=struct.pack("< H",len(self.transformations))
        skeletonPoseBlockBytes+=struct.pack("< I",0)
        jointcounter=0
        while jointcounter<len(self.transformations):
            self.transformations[jointcounter].Normalize()
            skeletonPoseBlockBytes+=struct.pack("< B",1)
            skeletonPoseBlockBytes+=struct.pack("< f",self.transformations[jointcounter].v1.x)+struct.pack("< f",self.transformations[jointcounter].v1.y)+struct.pack("< f",self.transformations[jointcounter].v1.z)
            skeletonPoseBlockBytes+=struct.pack("< f",self.transformations[jointcounter].v2.x)+struct.pack("< f",self.transformations[jointcounter].v2.y)+struct.pack("< f",self.transformations[jointcounter].v2.z)
            skeletonPoseBlockBytes+=struct.pack("< f",self.transformations[jointcounter].v3.x)+struct.pack("< f",self.transformations[jointcounter].v3.y)+struct.pack("< f",self.transformations[jointcounter].v3.z)
            skeletonPoseBlockBytes+=struct.pack("< f",float(self.transformations[jointcounter].off.x))+struct.pack("< f",float(self.transformations[jointcounter].off.y))+struct.pack("< f",float(self.transformations[jointcounter].off.z))
            jointcounter+=1
        skeletonPoseBlockBytes+=struct.pack("< I",0)
        return baseBlockBytes+struct.pack("< I",len(skeletonPoseBlockBytes))+skeletonPoseBlockBytes

class SkeletonAnimationBlock(BaseBlock):
    def __init__(self,blockID=None,nameSpace=None,skeletonAnimationName=None,skeletonAnimationframes=None):
        super(SkeletonAnimationBlock, self ).__init__(blockID,nameSpace,103)
        self.skeletonAnimationName = skeletonAnimationName
        self.numFrames = skeletonAnimationframes
        self.framesImported = 0
        self.targetSkeletonJointList = []  
        self.framesDurationsList = []  
        self.framesIDSList = []  
        self.framesIDSList2 = []  
    def writeBinary(self,exportData):
        baseBlockBytes=super(SkeletonAnimationBlock, self).writeBinary(exportData)
        skeletonAnimationBlockBytes=struct.pack("< H",len(self.skeletonAnimationName))+str(self.skeletonAnimationName)
        skeletonAnimationBlockBytes+=struct.pack("< H",len(self.framesIDSList2))
        skeletonAnimationBlockBytes+=struct.pack("< I",0)
        frameCounter=0
        while frameCounter<len(self.framesIDSList2):
            skeletonAnimationBlockBytes+=struct.pack("< I",int(self.framesIDSList2[frameCounter]))
            skeletonAnimationBlockBytes+=struct.pack("< H",int((1000*self.framesDurationsList[frameCounter])))
            frameCounter+=1
        skeletonAnimationBlockBytes+=struct.pack("< I",0)
        return baseBlockBytes+struct.pack("< I",len(skeletonAnimationBlockBytes))+skeletonAnimationBlockBytes

class UVAnimationBlock(BaseBlock):
    def __init__(self):
        self.name = "undefined"
    def writeBinary(self,exportData):
        baseBlockBytes=super(UVAnimationBlock, self).writeBinary(exportData)
        return baseBlockBytes+struct.pack("< I",0)


class NameSpaceBlock(BaseBlock):
    def __init__(self):
        self.name = "undefined"
    def writeBinary(self,exportData):
        baseBlockBytes=super(NameSpaceBlock, self).writeBinary(exportData)
        return baseBlockBytes+struct.pack("< I",0)

class MetaDataBlock(BaseBlock):
    def __init__(self,blockID=0,nameSpace=0):
        super(MetaDataBlock, self ).__init__(blockID,nameSpace,255)
    def writeBinary(self,exportData):
        baseBlockBytes=super(MetaDataBlock, self).writeBinary(exportData)
        return baseBlockBytes+struct.pack("< I",0)
		
		
class BaseAttribute(object):
    def __init__(self):
        tester=0
        tesere=2
        while tester<tesere:
            print tester
            tester+=1
        self.attributeID = 0
        self.attributeValue = None

class awdGeometryStream(object):
    def __init__(self,streamType,streamData):
        self.streamType=streamType
        self.streamTypeName="None"
        self.streamData=streamData
        if streamType==1:#Vertex
            self.streamTypeName="Vertex"
            self.dataType = "f"
            self.dataType2 = 4
        if streamType==2:#Index
            self.streamTypeName="Index"
            self.dataType = "H"
            self.dataType2 = 2
        if streamType==3:#UV
            self.streamTypeName="UV"
            self.dataType = "f"
            self.dataType2 = 4
        if streamType==4:#VertexNormals
            self.streamTypeName="VertexNormals"
            self.dataType = "f"
            self.dataType2 = 4
        if streamType==5:#VertexTangents
            self.streamTypeName="VertexTangents"
            self.dataType = "f"
            self.dataType2 = 4
        if streamType==6:#JointIndex
            self.streamTypeName="JointIndex"
            self.dataType = "H"
            self.dataType2 = 2
        if streamType==7:#JointWeights
            self.streamTypeName="JointWeights"
            self.dataType = "f"
            self.dataType2 = 4
        if streamType==8:#quads - not used by official AWD
            self.streamTypeName="quads"
            self.dataType = "H"
            self.dataType2 = 2

class awdSubMesh(object):
    def __init__(self,materialName,selectionName,selectionIndexe, textureTag):
        self.materialName= materialName
        self.selectionName= selectionName
        self.selectionIndexe= selectionIndexe
        self.textureTag= textureTag

        self.objectSettings= 0
        self.saveSubMeshProps=0
        self.saveGeometryStreams = []
        self.saveUserAttributesList= 0

        self.weightsBuffer= []
        self.jointidxBuffer= []
        self.saveIndexBuffer= []
        self.saveWeightsBuffer= []

        self.vertexBuffer= []
        self.indexBuffer= []
        self.uvBuffer= []
        self.normalBuffer= []
        self.faceNormal= []
        self.quadBuffer= []

        self.uniquePoolDict= {}

    def writeBinary(self,exportData):
        outputBits=struct.pack("< I",self.saveSubMeshProps)
        subMeshCount=0
        outputString="Subemesh '"+str(self.selectionName)+"' streams = "
        while subMeshCount<len(self.saveGeometryStreams):
            if len(self.saveGeometryStreams[subMeshCount].streamData)>0:
            
                outputBits+=struct.pack("< B",self.saveGeometryStreams[subMeshCount].streamType)
                outputBits+=struct.pack("< B",self.saveGeometryStreams[subMeshCount].dataType2)
                streamDataBits=str()
                streamCounter=0
                outputString+=str(self.saveGeometryStreams[subMeshCount].streamTypeName)+" = "+str(len(self.saveGeometryStreams[subMeshCount].streamData))+"  / "
                while streamCounter< len(self.saveGeometryStreams[subMeshCount].streamData):
                    streamDataBits+=struct.pack(str("< "+str(self.saveGeometryStreams[subMeshCount].dataType)),self.saveGeometryStreams[subMeshCount].streamData[streamCounter])
                    streamCounter+=1
                outputBits+=struct.pack("< I",len(streamDataBits))+streamDataBits

            subMeshCount+=1
        if exportData.debug==True:
            print outputString
        outputBits+=struct.pack("< I",self.saveUserAttributesList)
        return outputBits