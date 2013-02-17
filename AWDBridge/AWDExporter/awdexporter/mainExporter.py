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

# first function called by "maindialog.py" to start the exportprocess
def startExport(mainDialog):
    doc=c4d.documents.GetActiveDocument()
    if doc==None:
        newMessage=c4d.plugins.GeLoadString(ids.STATUSMESSAGE1)
        c4d.gui.MessageDialog(newMessage)
        return True
    if doc.GetDocumentPath()==None or doc.GetDocumentPath()=="":
        newMessage=c4d.plugins.GeLoadString(ids.STATUSMESSAGE1)
        c4d.gui.MessageDialog(newMessage)
        return True
    maindialogHelpers.enableAll(mainDialog,False)
    
    doc=c4d.documents.GetActiveDocument()
    exportData=classMainScene.mainScene(doc.GetDocumentName(),mainDialog,doc.GetFps())#empty list to collect the objects that should be exportet

    export(exportData) 
    exportData.allStatusLength=2+(10*int(exportData.animationCounter))+(10*len(exportData.allMeshObjects))
    exportData.allStatus=1
    exportData.status=1
    mainDialog.updateCanvas()
    mainSkeletonReader.createSkeletonBlocks(exportData.objList,exportData,mainDialog) 
    exportData.status=2  
    mainDialog.updateCanvas()
    if len(exportData.AWDerrorObjects)>0:  
        maindialogHelpers.enableAll(mainDialog,True)
        newMessage=c4d.plugins.GeLoadString(ids.ERRORMESSAGE)+"\n"
        for errorMessage in exportData.AWDerrorObjects:
            newMessage+=c4d.plugins.GeLoadString(errorMessage.errorID)
            if errorMessage.errorData!=None:
                newMessage+="\n\n"+str(c4d.plugins.GeLoadString(ids.ERRORMESSAGEOBJ))+" = "+str(errorMessage.errorData)
        c4d.gui.MessageDialog(newMessage)
        exportData=None
        if mainDialog.GetBool(ids.CBOX_CLOSEAFTEREXPORT) == True:  
            exportData=None
            c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
            c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
            c4d.EventAdd(c4d.EVENT_ANIMATE) 
            mainDialog.Close()
            exportData=None  
            return exportData
        c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
        c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
        c4d.EventAdd(c4d.EVENT_ANIMATE)  
        exportData=None  
        return exportData  
    return exportData         
              
      
def export(exportData):

    doc=documents.GetActiveDocument()
    objectsToExport=[]#empty list to collect the objects that should be exportet
#exportData.allAnimations.append(myclasses.animation(mainDialog.GetString(ids.STR_ANIMATIONNAME),0,exportData,mainDialog.GetReal(ids.REAL_LASTFRAME),doc.GetFps()))

    exportData.originalActiveObjects=doc.GetActiveObjects(True)
    exportData.originalActiveTags=doc.GetActiveTags()
    exportData.originalActiveMaterials=doc.GetActiveMaterials()
    
    #create MetaDataBlock
    newMetaDataBlock=classesAWDBlocks.MetaDataBlock(exportData.idCounter,0)
    exportData.IDsToAWDBlocksDic[str(exportData.idCounter)]=newMetaDataBlock
    exportData.allAWDBlocks.append(newMetaDataBlock)
    newMetaDataBlock.tagForExport=True
    exportData.idCounter+=1
    
    #create Default material (workarround, to be able to handle submeshes without materials)
    defaultMaterial=c4d.BaseMaterial(c4d.Mmaterial)
    defaultMaterial.SetName("C4D-DefaultMat")
    defaultMaterial[c4d.MATERIAL_USE_COLOR]=True
    defaultMaterial[c4d.MATERIAL_COLOR_COLOR]=c4d.documents.GetActiveDocument()[c4d.DOCUMENT_DEFAULTMATERIAL_COLOR]
    exportData.allMaterialsNames.append(defaultMaterial.GetName())  
    exportData.allMaterialsBlockIDS.append(exportData.idCounter)  
    exportData.allMaterials.append(defaultMaterial)  
    defaultMaterial.SetName("0")  

    #create Default material Block (workarround, to be able to handle submeshes without materials)
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
    for mat in doc.GetMaterials():
        exportData.allMaterialsNames.append(mat.GetName())    
        exportData.allMaterialsBlockIDS.append(-1)      
        exportData.allMaterials.append(mat)      
        mat.SetName(str(matidcounter))
        matidcounter+=1

    c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
    c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
    c4d.EventAdd(c4d.EVENT_ANIMATE)            
    if exportData.selectedOnly==True:
        objectsToExport=doc.GetActiveObjects(False)
        if len(objectsToExport)==0:
            if exportData.unusedMats==False:
                newError=classesHelper.AWDerrorObject(ids.ERRORMESSAGE1,None)
                exportData.AWDerrorObjects.append(newError)
                return exportData
            if exportData.unusedMats==True:
                exportData.allc4dMaterials=doc.GetMaterials()
                if len(exportData.allc4dMaterials)==0:
                    newError=classesHelper.AWDerrorObject(ids.ERRORMESSAGE1,None)
                    exportData.AWDerrorObjects.append(newError)
                    return exportData
            
    if exportData.selectedOnly==False:
        objectsToExport=doc.GetObjects()
        if len(objectsToExport)==0:
            if exportData.unusedMats==False:
                newError=classesHelper.AWDerrorObject(ids.ERRORMESSAGE2,None)
                exportData.AWDerrorObjects.append(newError)
                return exportData
            if exportData.unusedMats==True:
                exportData.allc4dMaterials=doc.GetMaterials()
                if len(exportData.allc4dMaterials)==0:
                    newError=classesHelper.AWDerrorObject(ids.ERRORMESSAGE2,None)
                    exportData.AWDerrorObjects.append(newError)
                    return exportData

    originalTime=doc.GetTime()#store the original play position
    storeEditMode=doc.GetMode()#store the current EditMode
    #doc.SetTime(exportData.firstFrame, doc.GetFps())#set play position to 0
    doc.SetMode(11)#set EditMode to 11 (Model-Mode) - otherwise the triangulate method only affects the selected polygons!

    c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
    c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
    c4d.EventAdd(c4d.EVENT_ANIMATE)
    
    #allPointAndUvMorpTag=[]
    #c4d.CallCommand(13957) # Clear Console
    #allObjectsDic=defaultdict(list)
    #c4d.EventAdd(c4d.EVENT_ANIMATE)#send event to update
    #c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)#send event to update

    exportData.createAllUsedTextureAndMaterialBlocks(exportData.unusedMats,objectsToExport)
    if len(exportData.AWDerrorObjects)>0:
        return exportData
    mainHelpers.resetAllObjects(objectsToExport)
        
    exportData.createAllSceneBlocks(objectsToExport,exportData.defaultObjectSettings)
    exportData.objList=objectsToExport
	
	
 