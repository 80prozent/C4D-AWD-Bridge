# functions running in the c4d-main-thread

# some functions to convert skeleton-animations from c4d to awd2-data

import c4d
from c4d import documents

from awdexporter import ids
from awdexporter import classesAWDBlocks
from awdexporter import mainHelpers
from awdexporter import mainSkeletonHelper

# this is the function that gets called from the "mainExporter"
def createSkeletonBlocks(objList,exportData,mainDialog):
    for object in objList:                                      # for every object do:
        skeletonTag=object.GetTag(1028937)                          # try to find a "SkeletonTag" on this object 
        if skeletonTag is not None:                                 # if a "SkeletonTag" is found:
            if skeletonTag[1010]==True:                                 # if the "SkeletonTag" is enabled for export:
                if skeletonTag[1011] is not None:                           # if the "SkeletonTag"-Name is not None:
                    buildSkeleton(exportData,object)                            # build the skeletonBlock
        skeletonAnimationTag=object.GetTag(1028938)                 # try to find a "SkeletonAnimationTag" on this object  
        if skeletonAnimationTag is not None:                        # if a "SkeletonAnimationTag" is found:
            if skeletonAnimationTag[1010]==True:                        # if the "SkeletonAnimationTag" is enabled for export:
                if skeletonAnimationTag[1011] is not None:                  # if the "SkeletonAnimationTag"-Name is not None:
                    buildSkeletonAnimation(exportData,object,mainDialog)        # build the SkeletonAnimationBlock
        if len(object.GetChildren())>0:                             # if the object has any Children:
            createSkeletonBlocks(object.GetChildren(),exportData,mainDialog)# execute this function again, passing the children as objList


    
# build a new skeletonBlock 
def buildSkeleton(exportData,curObj):
    newAWDBlock=classesAWDBlocks.SkeletonBlock(exportData.idCounter,0,curObj.GetTag(1028937)[1011],curObj)  # create a new block for the skeleton
    exportData.IDsToAWDBlocksDic[str(exportData.idCounter)]=newAWDBlock                                     # add a dictionary-entrance for the skeletonBlock
    exportData.allAWDBlocks.append(newAWDBlock)                                                             # append the SkeletonBlock to the allAwdBlocks-list
    exportData.allSkeletonBlocks.append(newAWDBlock)                                                        # append the SkeletonBlock to the SkeletonBlocks-list    
    newAWDBlock.name=curObj.GetTag(1028937)[1011]                                                           # set the name of the AWDBlock
    newAWDBlock.tagForExport=True                                                                           # tag this AWDBlock for export
    exportData.idCounter+=1                                                                                 # increment the idCounter
    newSkeleton=mainSkeletonHelper.SkeletonHelper(curObj,None,False)                                        # use the skeletonHelper to check if the skeletonBlock is a valid skeleton
    weightTags=newSkeleton.allWeightTags                                                                    # get the weighttags that are using this skeleton from the Skeletonhelper
    if len(weightTags)==0:                                                                                  # if no weightTag is found:
        newWarning=AWDerrorObject(ids.WARNINGMESSAGE1,tag.GetMaterial().GetName())                              # create a Warning that the Skeleton has no valid binding 
        exportData.AWDwarningObjects.append(newWarning)                                                         # append the warning to the warnings-list, so it will get displayed when finished
        
    buildSkeletonJoint([curObj],newAWDBlock.saveJointList,0,exportData,newAWDBlock)                         # build all the skeleton-joint-blokcs (bindingMatrix etc)
    for tag in newSkeleton.expressionTagsToRestore:                                                         # after reading the skeleton positions, we enabl
        tag[c4d.EXPRESSION_ENABLE]=True                                                                         # we enable the expression-tags that have been disabled by the skeletonHelper earlier

#recursive function to create all the jointBlocks for one Skeleton
def buildSkeletonJoint(jointObjs,jointList,parentID,exportData,skeletonBlock): 
    for jointObj in jointObjs:
        newJoint=classesAWDBlocks.jointBlock((len(jointList)+1),parentID,jointObj)          # create a new jointblock
        exportData.jointIDstoSkeletonBlocks[str(jointObj.GetName())]=skeletonBlock          # create a dictionary-entrance in jointIDStoSkeletonBlocks, so we can get the skeleton this joint is used by, by using the joints name 
        exportData.jointIDstoJointBlocks[str(jointObj.GetName())]=newJoint                  # create a dictionary-entrance in jointIDstoJointBlocks, so we can get the joints-index  by using its name
        newJoint.lookUpName=exportData.IDsToAWDBlocksDic[jointObj.GetName()].name           # get the original joint-name

        newJoint.transMatrix=((jointObj.GetMg().__invert__()))                       # set the InversBindMatrix for this Joint        
        jointList.append(newJoint)                                                          # append this joint-block to the skeletonBlocks-jointList
        parentID2=(len(jointList))                                                          # get the parentID to use for the next joints 
        if len(jointObj.GetChildren())>0:                                                   # if the object has any childs:
            buildSkeletonJoint(jointObj.GetChildren(),jointList,parentID2,exportData,skeletonBlock) # execute the function for the childs 

# build a skeletonAnimationBlock
def buildSkeletonAnimation(exportData,curObj,mainDialog):   
    minFrame=mainDialog.GetReal(ids.REAL_FIRSTFRAME)                                                            # get the first frame of the animation range
    maxFrame=mainDialog.GetReal(ids.REAL_LASTFRAME)                                                           # get the last frame of the animation range
    curFrame=minFrame                                                                                           # set the first frame to be the current frame
    durationList=[]                                                                                             # list to store all frame-durations
    idList=[]                                                                                                   # list to store all frame-IDs
    track=curObj.GetFirstCTrack()                                                                               # get the first track of the curObj
    if track==None:                                                                                             # if no track is found
        durationList.append(1*exportData.doc.GetFps())                                                              # set only one duration
        idList.append(buildSkeletonPose(exportData,curObj,c4d.BaseTime((curFrame*exportData.doc.GetFps())/1000)))   # add one skeletonPoseBlock to the idLis
        buildSkeletonAnimationBlock(exportData,curObj,durationList,idList)                                          # create a SkeletonAnimationBlock containing only one Frame
        return                                                                                                      # exit this function
    curve=track.GetCurve()                                                                                 # get the curve for this track
    keyCounter=0   
    keyCount=curve.GetKeyCount()  
    print keyCount                                                                              # get key-Count of the Curve
    lastDuration=0
    lastPose=None
    firstKeyTime=None
    while keyCounter<keyCount:                                                                                  # iterate over the keyCount
        key=curve.GetKey(keyCounter)                                                                            # get a key   
        keyTime=key.GetTime()    
        if firstKeyTime < keyTime:
            firstKeyTime=keyTime
        #exportData.doc.SetTime(curTime)                                                                   # get a key   
        keyTimeInFrame=keyTime.GetFrame(exportData.doc.GetFps())
        exportData.allStatus+=float(10/float(curve.GetKeyCount()))                                                  # used to calculate processbar
        mainHelpers.updateCanvas(mainDialog,exportData)                                                             # update processbar
        # if the keys time is within the range to export:
        if float(keyTimeInFrame)>=float(minFrame) and float(keyTimeInFrame)<=float(maxFrame):
            if (keyCounter+1)<keyCount:# if this is not the last key, we calculate the duration-time like this: durationTime = nextKeyTime - thisKeyTime
                durationList.append(float(curve.GetKey(keyCounter+1).GetTime().Get())-float(keyTime.Get()))
            if (keyCounter+1)>=keyCount:# if this is the last keyframe within the range, we set its duration 
                durationList.append((1000/exportData.doc.GetFps())/1000)#100*(1000/exportData.doc.GetFps()))
            idList.append(buildSkeletonPose(exportData,curObj,keyTime))
        keyCounter+=1
    if firstKeyTime is not None:
        durationList.append((1000/exportData.doc.GetFps())/1000)
        print durationList
        idList.append(buildSkeletonPose(exportData,curObj,firstKeyTime))
    buildSkeletonAnimationBlock(exportData,curObj,durationList,idList)                                          # create the SkeletonAnimationBlock 

def buildSkeletonAnimationBlock(exportData,curObj,durationList,idList):   
    newAWDBlock=classesAWDBlocks.SkeletonAnimationBlock(exportData.idCounter,0,curObj.GetTag(1028938)[1011],len(durationList)) # create a new AWDSkeletonAnimationBlock
    exportData.IDsToAWDBlocksDic[str(exportData.idCounter)]=newAWDBlock
    exportData.allAWDBlocks.append(newAWDBlock)
    newAWDBlock.name=curObj.GetTag(1028938)[1011]
    newAWDBlock.tagForExport=True
    newAWDBlock.framesDurationsList=durationList
    newAWDBlock.framesIDSList=idList
    exportData.idCounter+=1
    exportData.allSkeletonAnimations.append(newAWDBlock)

# creates a new SkeletonPoseBlock - called by "buildSkeletonAnimation()"
def buildSkeletonPose(exportData,curObj,curTime):   
    newAWDBlock=classesAWDBlocks.SkeletonPoseBlock(exportData.idCounter,0,curObj.GetTag(1028938)[1011])
    exportData.IDsToAWDBlocksDic[str(exportData.idCounter)]=newAWDBlock
    exportData.allAWDBlocks.append(newAWDBlock)
    newAWDBlock.name=curObj.GetTag(1028938)[1011]
    exportData.idCounter+=1
    newAWDBlock.tagForExport=True
    print "MatrixOFF= "+str(curObj.GetName())+" / "+str(curTime.Get())
    c4d.documents.SetDocumentTime(exportData.doc, curTime)# set original Time
    c4d.DrawViews( c4d.DRAWFLAGS_FORCEFULLREDRAW|c4d.DRAWFLAGS_NO_THREAD|c4d.DRAWFLAGS_NO_REDUCTION|c4d.DRAWFLAGS_STATICBREAK )
    c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
    c4d.EventAdd(c4d.EVENT_ANIMATE)
    c4d.EventAdd(c4d.EVENT_FORCEREDRAW)
    c4d.DrawViews( c4d.DRAWFLAGS_FORCEFULLREDRAW)
    c4d.GeSyncMessage(c4d.EVMSG_ASYNCEDITORMOVE)
    newAWDBlock.transformations=[]
    buildJointTransform([curObj],newAWDBlock.transformations,exportData,True) # recursive function to get all Joints as JointBlocks
    return newAWDBlock.blockID
    
# saves the skeleton-joint-matricies while playing trough timeline - called by "buildSkeletonPose()"
def buildJointTransform(curObjList,jointTransforms,exportData,firstJoint):   
    for curObj in curObjList:
        if firstJoint==False:
            newMatrix=curObj.GetMl()    
        if firstJoint==True:
            newMatrix=curObj.GetMg()
        newMatrix.off=newMatrix.off*exportData.scale
        print "MatrixOFF= "+str(curObj.GetName())+" / "+str(newMatrix.off)
        jointTransforms.append(newMatrix)
        if len(curObj.GetChildren())>0:
            buildJointTransform(curObj.GetChildren(),jointTransforms,exportData,False)
            
    


