# functions running in the c4d-main-thread

# some functions to convert skeleton-animations from c4d to awd2-data

import c4d
from c4d import documents

from awdexporter import ids
from awdexporter import classesAWDBlocks

   
def createSkeletonBlocks(objList,exportData,mainDialog):
    for object in objList:
        if object.GetType()==c4d.Ojoint and object.GetTag(1028937)!=None:
            if object.GetTag(1028937)[1010]==True:
                buildSkeleton(exportData,object)
        if object.GetType()==c4d.Ojoint and object.GetTag(1028938)!=None:
            if object.GetTag(1028938)[1010]==True:   
                buildSkeletonAnimation(exportData,object,mainDialog)
        if len(object.GetChildren())>0:
            createSkeletonBlocks(object.GetChildren(),exportData,mainDialog)

def buildSkeletonAnimation(exportData,curObj,mainDialog):   
    #print "Build Skeleton Animation ###################"
    minFrame=curObj.GetTag(1028938)[1013]
    maxFrame=curObj.GetTag(1028938)[1014]
    curFrame=minFrame
    durationList=[]
    idList=[]
    track=curObj.GetFirstCTrack()
    if track==None:
        durationList.append(1*c4d.documents.GetActiveDocument().GetFps())
        idList.append(buildSkeletonPose(exportData,curObj,c4d.BaseTime((curFrame*c4d.documents.GetActiveDocument().GetFps())/1000)))
        buildSkeletonAnimationBlock(exportData,curObj,durationList,idList)
        return 
    curve=track.GetCurve()
    keyCounter=0
    while keyCounter<curve.GetKeyCount():  
        key=curve.GetKey(keyCounter)    
        exportData.allStatus+=float(10/float(curve.GetKeyCount()))
        mainDialog.updateCanvas()
        if key.GetTime().GetFrame(c4d.documents.GetActiveDocument().GetFps())>=minFrame and key.GetTime().GetFrame(c4d.documents.GetActiveDocument().GetFps())<=maxFrame:
            if (keyCounter+1)<curve.GetKeyCount():
                durationList.append(float(curve.GetKey(keyCounter+1).GetTime().Get())-float(key.GetTime().Get()))
            if (keyCounter+1)>=curve.GetKeyCount():
                durationList.append(1*c4d.documents.GetActiveDocument().GetFps())
            idList.append(buildSkeletonPose(exportData,curObj,key.GetTime()))
        keyCounter+=1
    buildSkeletonAnimationBlock(exportData,curObj,durationList,idList)



def buildSkeletonAnimationBlock(exportData,curObj,durationList,idList):   
    newAWDBlock=classesAWDBlocks.SkeletonAnimationBlock(exportData.idCounter,0,curObj.GetTag(1028938)[1011],len(durationList))
    exportData.IDsToAWDBlocksDic[str(exportData.idCounter)]=newAWDBlock
    exportData.allAWDBlocks.append(newAWDBlock)
    newAWDBlock.name=curObj.GetTag(1028938)[1011]
    newAWDBlock.tagForExport=True
    newAWDBlock.framesDurationsList=durationList
    newAWDBlock.framesIDSList=idList
    #print "sgsgsgsgsg "+str(len(idList))
    exportData.idCounter+=1
    exportData.allSkeletonAnimations.append(newAWDBlock)

def buildSkeletonPose(exportData,curObj,curTime):   
    newAWDBlock=classesAWDBlocks.SkeletonPoseBlock(exportData.idCounter,0,curObj.GetTag(1028938)[1011])
    exportData.IDsToAWDBlocksDic[str(exportData.idCounter)]=newAWDBlock
    exportData.allAWDBlocks.append(newAWDBlock)
    newAWDBlock.name=curObj.GetTag(1028938)[1011]
    exportData.idCounter+=1
    newAWDBlock.tagForExport=True
    c4d.documents.GetActiveDocument().SetTime(curTime)# set original Time
    c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
    c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
    c4d.EventAdd(c4d.EVENT_ANIMATE)
    newAWDBlock.transformations=[]
    buildJointTransform([curObj],newAWDBlock.transformations)
    return newAWDBlock.blockID
    #
def buildJointTransform(curObjList,jointTransforms):   
    for curObj in curObjList:
        jointTransforms.append(curObj.GetMl())
        if len(curObj.GetChildren())>0:
            buildJointTransform(curObj.GetChildren(),jointTransforms)

def buildSkeleton(exportData,curObj):
    newAWDBlock=classesAWDBlocks.SkeletonBlock(exportData.idCounter,0,curObj.GetTag(1028937)[1011],curObj)
    exportData.IDsToAWDBlocksDic[str(exportData.idCounter)]=newAWDBlock
    exportData.allAWDBlocks.append(newAWDBlock)
    exportData.allSkeletonBlocks.append(newAWDBlock)
    newAWDBlock.name=curObj.GetTag(1028937)[1011]
    newAWDBlock.tagForExport=True
    exportData.idCounter+=1
    buildSkeletonJoint([curObj],newAWDBlock.saveJointList,0,exportData,newAWDBlock)
        
    #newAWDBlock.dataParentBlockID=0
    #if curObj.GetUp():
    #	newAWDBlock.dataParentBlockID=int(curObj.GetUp().GetName())
    #curObj.SetName(str(exportData.idCounter))
    #exportData.idCounter+=1

def buildSkeletonJoint(jointObjs,jointList,parentID,exportData,newAWDBlock): 
    for jointObj in jointObjs:
        parentID2=parentID
        exportData.jointIDstoSkeletonBlocks[str(jointObj.GetName())]=newAWDBlock
        newJoint=classesAWDBlocks.jointBlock((len(jointList)+1),parentID2,jointObj)
        exportData.jointIDstoJointBlocks[str(jointObj.GetName())]=newJoint
        parentID2=(len(jointList)+1)
        newJoint.lookUpName=exportData.IDsToAWDBlocksDic[jointObj.GetName()].name
        newJoint.transMatrix=jointObj.GetMg().__invert__()
        jointList.append(newJoint)
        if len(jointObj.GetChildren())>0:
            buildSkeletonJoint(jointObj.GetChildren(),jointList,parentID2,exportData,newAWDBlock)

