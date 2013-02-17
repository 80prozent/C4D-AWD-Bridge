# some helper-functions for the part of the export process running in the c4d-mainthread

import c4d
from awdexporter import ids
from awdexporter import classesHelper

def deleteCopiedMeshes(meshBlockList):
    for meshBlock in meshBlockList:            
        meshBlock.copiedMesh.Remove()
		
		
		
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

def resetAllObjects(objList=None):
    for curObj in objList:
        if curObj.GetTag(c4d.Tweights):#	reset morphtags
            c4d.documents.GetActiveDocument().SetActiveObject(curObj)
            c4d.CallCommand(1019937)
            c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
            c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
            c4d.documents.GetActiveDocument().SetTime(c4d.documents.GetActiveDocument().GetTime())
            c4d.EventAdd(c4d.EVENT_ANIMATE)
        if curObj.GetTag(c4d.Tposemorph):#	reset morphtags
            all_tags=curObj.GetTags()#get all tags applied to object
            for morphtag in all_tags:#do for each tag:
                if morphtag.GetType()==c4d.Tposemorph:#do if the tag is a morphtag
                    if morphtag.GetMode()==1:#do if the tag is in animation-mode:
                        c4d.documents.GetActiveDocument().SetTime(c4d.BaseTime(0, c4d.documents.GetActiveDocument().GetFps()))
                        c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
                        c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
                        c4d.documents.GetActiveDocument().SetTime(c4d.documents.GetActiveDocument().GetTime())
                        c4d.EventAdd(c4d.EVENT_ANIMATE)
                        for track in morphtag.GetCTracks():
                            curve = track.GetCurve()
                            if curve.GetKeyCount()==0:
                               print "skipped morphpose"
                            if curve.GetKeyCount()>0:
                               curve.GetKey(0).SetValue(curve,0.0)
        resetAllObjects(curObj.GetChildren())
