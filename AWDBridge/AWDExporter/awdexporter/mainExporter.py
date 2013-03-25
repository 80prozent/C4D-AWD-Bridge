# functions running in mainthread of c4d

import c4d
from c4d import documents

from awdexporter import ids
from awdexporter import classMainScene
from awdexporter import classesHelper
from awdexporter import classesAWDBlocks
from awdexporter import mainHelpers
from awdexporter import mainSkeletonReader
from awdexporter import maindialogHelpers
from awdexporter import mainParseObjectToAWDBlock
from awdexporter import mainMaterials

# called by "maindialog.Command()" to start the export-process
def startExport(mainDialog,doc):
    maindialogHelpers.enableAll(mainDialog,False)               # disable the all GUI-elements, so the user can not change anything while exporting    
    exportData=classMainScene.mainScene(doc,mainDialog)         # create a new "mainScene". this class will store all the data collected for export
    export(exportData)                                          # execute the export function 
    exportData.allStatusLength=2+(10*int(exportData.animationCounter))+(10*len(exportData.allMeshObjects))# used to calculate the progress-bar
    exportData.allStatus=1                                      # used to calculate the progress-bar
    exportData.status=1                                         # used to calculate the progress-bar
    mainHelpers.updateCanvas(mainDialog,exportData)             # update the progress-bar
    mainSkeletonReader.createSkeletonBlocks(exportData.objList,exportData,mainDialog) 
    exportData.status=2  
    mainHelpers.updateCanvas(mainDialog,exportData)
    return exportData         

# called by "maindialog.Timer()" to end the exportprocess when background-Thread has finished
def endExport(mainDialog,exportData):        
    mainHelpers.deleteCopiedMeshes(exportData.allMeshObjects)
    if len(exportData.AWDerrorObjects)>0:  
        newMessage=c4d.plugins.GeLoadString(ids.ERRORMESSAGE)+"\n"
        for errorMessage in exportData.AWDerrorObjects:
            newMessage+=c4d.plugins.GeLoadString(errorMessage.errorID)
            if errorMessage.errorData!=None:
                newMessage+="\n\n"+str(c4d.plugins.GeLoadString(ids.ERRORMESSAGEOBJ))+" = "+str(errorMessage.errorData)
        c4d.gui.MessageDialog(newMessage)
        if mainDialog.GetBool(ids.CBOX_CLOSEAFTEREXPORT) == True:  
            exportData=None
            c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
            c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
            c4d.EventAdd(c4d.EVENT_ANIMATE) 
            mainDialog.Close()
            return True  
        exportData=None
        c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
        c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
        c4d.EventAdd(c4d.EVENT_ANIMATE) 
        return True  
    if len(exportData.AWDwarningObjects)>0:  
        newMessage=c4d.plugins.GeLoadString(ids.WARNINGMESSAGE)+"\n"
        for errorMessage in exportData.AWDwarningObjects:
            newMessage+=c4d.plugins.GeLoadString(errorMessage.errorID)
            if errorMessage.errorData!=None:
                newMessage+="AWDWarningObject: "+str(errorMessage.errorData)
        print "Warning "+str(newMessage)
        if mainDialog.GetBool(ids.CBOX_CLOSEAFTEREXPORT) == True:  
            exportData=None
            c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
            c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
            c4d.EventAdd(c4d.EVENT_ANIMATE) 
            mainDialog.Close()    
            return True  
    if mainDialog.GetBool(ids.CBOX_CLOSEAFTEREXPORT) == True and exportData.cancel!=True:  
        exportData=None
        c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
        c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
        c4d.EventAdd(c4d.EVENT_ANIMATE) 
        mainDialog.Close()
        return True  
    exportData=None
    c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
    c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
    c4d.EventAdd(c4d.EVENT_ANIMATE) 
    maindialogHelpers.enableAll(mainDialog,True)
    print c4d.plugins.GeLoadString(ids.SUCCESSMESSAGE)
    mainHelpers.updateCanvas(mainDialog,exportData)
    c4d.EventAdd(c4d.EVENT_ANIMATE) 
    mainDialog.SetTimer(0)            
      
def export(exportData):
   
    #create the MetaDataBlock
    newMetaDataBlock=classesAWDBlocks.MetaDataBlock(exportData.idCounter,0)
    exportData.IDsToAWDBlocksDic[str(exportData.idCounter)]=newMetaDataBlock
    exportData.allAWDBlocks.append(newMetaDataBlock)
    newMetaDataBlock.tagForExport=True
    exportData.idCounter+=1
    
    #create Default material (to be applied to objects that have no materials or object-color assigned)
    defaultMaterial=c4d.BaseMaterial(c4d.Mmaterial)
    defaultMaterial.SetName("C4D-DefaultMat")
    defaultMaterial[c4d.MATERIAL_USE_COLOR]=True
    defaultMaterial[c4d.MATERIAL_COLOR_COLOR]=exportData.doc[c4d.DOCUMENT_DEFAULTMATERIAL_COLOR]
    exportData.allMaterialsNames.append(defaultMaterial.GetName())  
    exportData.allMaterialsBlockIDS.append(exportData.idCounter)  
    exportData.allMaterials.append(defaultMaterial)  
    defaultMaterial.SetName("0")  

    newAWDBlock=classesAWDBlocks.StandartMaterialBlock(exportData.idCounter,0)#obj_xml.setAttribute("type","NULL")#set XML-Node-Attribute "name"
    newAWDBlock.saveLookUpName=exportData.allMaterialsNames[int(defaultMaterial.GetName())]
    newAWDBlock.matColor=[defaultMaterial[c4d.MATERIAL_COLOR_COLOR].z*255,defaultMaterial[c4d.MATERIAL_COLOR_COLOR].y*255,defaultMaterial[c4d.MATERIAL_COLOR_COLOR].x*255,0]
    newAWDBlock.saveMatProps.append(1)
    exportData.IDsToAWDBlocksDic[str(exportData.idCounter)]=newAWDBlock
    exportData.allAWDBlocks.append(newAWDBlock)
    exportData.allMatBlocks.append(newAWDBlock)
    exportData.MaterialsToAWDBlocksDic[str(defaultMaterial)]=newAWDBlock 
    newAWDBlock.tagForExport=False 
    exportData.idCounter+=1 

    matidcounter=1
    for mat in exportData.allc4dMaterials:
        exportData.allMaterialsNames.append(mat.GetName())    
        exportData.allMaterialsBlockIDS.append(-1)      
        exportData.allMaterials.append(mat)      
        mat.SetName(str(matidcounter))
        matidcounter+=1

    c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
    c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
    c4d.EventAdd(c4d.EVENT_ANIMATE)          
            
    objectsToExport=exportData.doc.GetObjects()                             # get a list of all objects in the scene
    if len(objectsToExport)==0:                                             # if no object is in the scene:
        if exportData.unusedMats==False:                                        # if no unsued materials should be exported:
            newError=classesHelper.AWDerrorObject(ids.ERRORMESSAGE2,None)           # create a new errorObject
            exportData.AWDerrorObjects.append(newError)                             # append the new errorObject to the errorlist, so it will be displayed at the end of export process 
            return exportData                                                       # return from function
        if exportData.unusedMats==True:                                         # if unused materials should be exported:
            exportData.allc4dMaterials=doc.GetMaterials()                           # get a list of all materials
            if len(exportData.allc4dMaterials)==0:                                  # if no material was found:
                newError=classesHelper.AWDerrorObject(ids.ERRORMESSAGE2,None)           # create a new errorObject
                exportData.AWDerrorObjects.append(newError)                             # append the new errorObject to the errorlist, so it will be displayed at the end of export process 
                return exportData                                                       # return from function

    originalTime=exportData.doc.GetTime()#store the original play position
    storeEditMode=exportData.doc.GetMode()#store the current EditMode
    
    #doc.SetTime(exportData.firstFrame, doc.GetFps())#set play position to 0
    exportData.doc.SetMode(11)#set EditMode to 11 (Model-Mode) - otherwise the triangulate method will only affect the selected polygons!

    c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
    c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
    c4d.EventAdd(c4d.EVENT_ANIMATE)
    
    mainMaterials.createAllUsedMaterialBlocks(exportData, exportData.unusedMats,objectsToExport)
    if len(exportData.AWDerrorObjects)>0:
        return exportData
    #mainHelpers.resetAllObjectsAtBeginning(objectsToExport)
        
    mainParseObjectToAWDBlock.createAllSceneBlocks(exportData,objectsToExport,exportData.defaultObjectSettings)
    exportData.objList=objectsToExport
	
	
 