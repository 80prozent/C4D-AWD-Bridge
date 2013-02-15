import c4d
from c4d import documents

from awdexporter import ids
from awdexporter import awdMainClass
from awdexporter import awdBlocks
from awdexporter import awdHelpers
from awdexporter import awdMeshReader
from awdexporter import awdSkinningReader

      
def export(exportData):

    doc=documents.GetActiveDocument()
    objectsToExport=[]#empty list to collect the objects that should be exportet
#exportData.allAnimations.append(myclasses.animation(mainDialog.GetString(ids.STR_ANIMATIONNAME),0,exportData,mainDialog.GetReal(ids.REAL_LASTFRAME),doc.GetFps()))

    exportData.originalActiveObjects=doc.GetActiveObjects(True)
    exportData.originalActiveTags=doc.GetActiveTags()
    exportData.originalActiveMaterials=doc.GetActiveMaterials()
    
    #create MetaDataBlock
    newMetaDataBlock=awdBlocks.MetaDataBlock(exportData.idCounter,0)
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
    newAWDBlock=awdBlocks.StandartMaterialBlock(exportData.idCounter,0)#obj_xml.setAttribute("type","NULL")#set XML-Node-Attribute "name"
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
                newError=awdMainClass.AWDerrorObject(ids.ERRORMESSAGE1,None)
                exportData.AWDerrorObjects.append(newError)
                return exportData
            if exportData.unusedMats==True:
                exportData.allc4dMaterials=doc.GetMaterials()
                if len(exportData.allc4dMaterials)==0:
                    newError=awdMainClass.AWDerrorObject(ids.ERRORMESSAGE1,None)
                    exportData.AWDerrorObjects.append(newError)
                    return exportData
            
    if exportData.selectedOnly==False:
        objectsToExport=doc.GetObjects()
        if len(objectsToExport)==0:
            if exportData.unusedMats==False:
                newError=awdMainClass.AWDerrorObject(ids.ERRORMESSAGE2,None)
                exportData.AWDerrorObjects.append(newError)
                return exportData
            if exportData.unusedMats==True:
                exportData.allc4dMaterials=doc.GetMaterials()
                if len(exportData.allc4dMaterials)==0:
                    newError=awdMainClass.AWDerrorObject(ids.ERRORMESSAGE2,None)
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
    awdHelpers.resetAllObjects(objectsToExport)
        
    exportData.createAllSceneBlocks(objectsToExport,exportData.defaultObjectSettings)
    exportData.objList=objectsToExport
	
	
	
def export2(exportData,workerthreat):
    doc=documents.GetActiveDocument()
    exportData.connectInstances()
    if workerthreat.TestBreak():
        return            
    exportData.getAllObjectData()
    if workerthreat.TestBreak():
        return          
    awdMeshReader.convertMeshes(exportData.allMeshObjects,exportData,workerthreat)
    if workerthreat.TestBreak():
        return          
              
    exportData.status=3
    exportData.reorderAllBlocks()
    if workerthreat.TestBreak():
        return          
    exportData.exportAllData()
    if workerthreat.TestBreak():
        return          
    exportData.allStatus+=1
    matidcounter=1
    for mat in doc.GetMaterials():   
        mat.SetName(str(exportData.allMaterialsNames[matidcounter]))
        matidcounter+=1
    for objBlock in exportData.allSceneObjects:   
        objBlock.sceneObject.SetName(objBlock.name)

    #self.parse_mats(mats_xml,self.GetBool(CBOX_UNUSEDMATS["id"]),used_mat_names)#loop trough all matrials and creates xml
    #self.read_morphtags(copied_op)#loops trough all objects, sets all  morphtags keyvalues to 0          
    #object_eintrag = self.read_selected_object(copied_op,objSettings,lights_Dic)#loop through all objects, creating xml 
    #self.read_hirarchy_morphs(copied_op,object_eintrag)#loop through all objects again, creaing morphstates for children of hirarchy-morphs
    #self.export_meshes(copied_op,object_eintrag,allPointAndUvMorpTag)#parsing the meshes

            #self.export_to_XMLfile(output_xml)
            #doc.SetActiveObject(op)#make the original object activ again
        
        #op.SetEditorMode(c4d.MODE_UNDEF)#make original object visible again
        # if no object is selected we open a c4d.MessageDialog for ErrorNotification:
    #if not(op):    
        #print "No Object selected!\n"
        
      #copied_op.Remove()#remove cloned object  
     
def restoreEverything(exportData,workerthreat):

    firstObj=0# restore the original selection 
    for obj in exportData.originalActiveObjects:
        if firstObj>0:
            doc.SetSelection(obj,c4d.SELECTION_ADD)
        if firstObj==0:
            doc.SetSelection(obj,c4d.SELECTION_NEW)
            firstObj+=1
    for tag in exportData.originalActiveTags:
        doc.SetSelection(tag,c4d.SELECTION_ADD)
    for material in exportData.originalActiveMaterials:
        doc.SetSelection(material,c4d.SELECTION_ADD)
    
    #doc.SetTime(originalTime)# set original Time
    #doc.SetMode(storeEditMode)# set original Editmode

    #objectsToExport=None

    c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
    c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
    c4d.EventAdd(c4d.EVENT_ANIMATE)
    
    c4d.StatusClear()
    
    return exportData
            
      

 