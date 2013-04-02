# functions that will run inside the background-worker-thread


import c4d
import copy
import struct
import os
import zlib
from awdexporter import ids
from awdexporter import classesHelper

def addSkeleton(exportData,awdSkeleton):
    if awdSkeleton.tagForExport==True:
        awdSkeleton.saveBlockID=len(exportData.allSaveAWDBlocks)
        exportData.allSaveAWDBlocks.append(awdSkeleton)

def addSkeletonPose(exportData,awdSkeletonPose):
    awdSkeletonPose.saveBlockID=len(exportData.allSaveAWDBlocks)
    exportData.allSaveAWDBlocks.append(awdSkeletonPose)
    return awdSkeletonPose.saveBlockID

def addSkeletonAnimation(exportData,awdSkeletonAnimation):
    if awdSkeletonAnimation.tagForExport==True:
        poseCouunt=0
        for pose in awdSkeletonAnimation.framesIDSList:
            skelPoseBlock=exportData.IDsToAWDBlocksDic.get(str(pose),None)
            if skelPoseBlock==None:
                pass#warning
            if skelPoseBlock!=None:
                awdSkeletonAnimation.framesIDSList2.append(addSkeletonPose(exportData,skelPoseBlock))
        awdSkeletonAnimation.saveBlockID=len(exportData.allSaveAWDBlocks)
        exportData.allSaveAWDBlocks.append(awdSkeletonAnimation)

def addToExportListMaterials(exportData,awdBlock):
    if awdBlock.isReordered==True:
        return awdBlock.saveBlockID
    if awdBlock.isReordered==False:
        if awdBlock.tagForExport==True:
            doThis=False
            if awdBlock.blockType==82:#NameSpace
                doThis=True
            if awdBlock.blockType==254:#NameSpace
                doThis=True
            if awdBlock.blockType==255:#metadata
                doThis=True
            if awdBlock.blockType==81:#material
                doThis=True
                if awdBlock.saveMatType==2:
                    textureBlock=exportData.IDsToAWDBlocksDic.get(str(awdBlock.saveColorTextureID),None)
                    if textureBlock is not None:
                        awdBlock.saveColorTextureID=addToExportList(exportData,textureBlock)
            if doThis==True:
                awdBlock.saveBlockID=int(len(exportData.allSaveAWDBlocks))
                awdBlock.isReordered=True
                exportData.allSaveAWDBlocks.append(awdBlock)
                return awdBlock.saveBlockID
    return None
                        
def addToExportList(exportData,awdBlock):
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
                parentBlock=exportData.IDsToAWDBlocksDic.get(str(awdBlock.dataParentBlockID),None)
                if parentBlock is not None:
                    awdBlock.dataParentBlockID=addToExportList(exportData,parentBlock)
                    
            if awdBlock.blockType==23:#meshinstance
                parentBlock=exportData.IDsToAWDBlocksDic.get(str(awdBlock.dataParentBlockID),None)
                if parentBlock is not None:
                    awdBlock.dataParentBlockID=addToExportList(exportData,parentBlock)
                geoBlock=exportData.IDsToAWDBlocksDic.get(str(awdBlock.geoBlockID),None)
                if geoBlock is not None:
                    awdBlock.geoBlockID=addToExportList(exportData,geoBlock)           
                awdBlock.saveMaterials2=[]
                #print str(len(geoBlock.saveSubMeshes))+"   geoBlock.saveSubMeshes"
                for mat in awdBlock.saveMaterials:
                    #print "mat = "+str(int(mat))+"  /  "+str(exportData.allAWDBlocks[int(mat)])
                    matBlockID=addToExportListMaterials(exportData,exportData.allAWDBlocks[int(mat)])
                    #print "matBlockID = "+str(matBlockID)
                    awdBlock.saveMaterials2.append(matBlockID)
                    #print "awdBlock.saveMaterials2 = "+str(awdBlock.saveMaterials2)
                      
            if awdBlock.blockType==41:#light
                parentBlock=exportData.IDsToAWDBlocksDic.get(str(awdBlock.dataParentBlockID),None)
                if parentBlock is not None:
                    awdBlock.dataParentBlockID=addToExportList(exportData,parentBlock)
                    
            if awdBlock.blockType==42:#camera
                parentBlock=exportData.IDsToAWDBlocksDic.get(str(awdBlock.dataParentBlockID),None)
                if parentBlock is not None:
                    awdBlock.dataParentBlockID=addToExportList(exportData,parentBlock)
                    
                            
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
                
            awdBlock.saveBlockID=int(len(exportData.allSaveAWDBlocks))
            awdBlock.isReordered=True
            exportData.allSaveAWDBlocks.append(awdBlock)
            return awdBlock.saveBlockID