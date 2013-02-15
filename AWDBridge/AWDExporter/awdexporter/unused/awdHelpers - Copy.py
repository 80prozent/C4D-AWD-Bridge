import c4d
from c4d import documents

from awdexporter import ids
from awdexporter import awdMeshReader

def getObjectsMaterials(curObj):
    allSelections=[]    
    for selectionTag in curObj.GetTags(): 
        if selectionTag.GetType()==5673:
            allSelections.append(awdMeshReader.PolySelection(selectionTag.GetName(),selectionTag.GetBaseSelect().GetAll(len(curObj.GetAllPolygons())))) 
    materials=[]
    selections=[]
    for tag in curObj.GetTags():
        if tag.GetType()==5616:# Texture tag gefunden:
            if str(tag[c4d.TEXTURETAG_RESTRICTION])!="None" or str(tag[c4d.TEXTURETAG_RESTRICTION])!="":
                for selection in allSelections: 
                    if str(tag[c4d.TEXTURETAG_RESTRICTION])==selection.name:
                        materials.append(tag.GetMaterial())
                        selections.append(selection)
            if str(tag[c4d.TEXTURETAG_RESTRICTION])=="None" or str(tag[c4d.TEXTURETAG_RESTRICTION])=="":
                materials=[tag.GetMaterial()]
                selections=[None]
    returnMaterials=[]
    matCounter=0
    while matCounter<len(materials):
        oneMaterial=[]
        if str(materials[matCounter].GetTypeName())!="Mat":
            pass
        if str(materials[matCounter].GetTypeName())=="Mat":
            oneMaterial.append(materials[matCounter])
            oneMaterial.append(selections[matCounter])
        matCounter+=1
        returnMaterials.append(oneMaterial)
    return returnMaterials

def read_axis_orientation_combobox(axis_idx):
    axis=""
    if axis_idx==0:
        axis="+X"
    if axis_idx==1:
        axis="-X"
    if axis_idx==2:
        axis="+Y"
    if axis_idx==3:
        axis="-Y"
    if axis_idx==4:
        axis="+Z"
    if axis_idx==5:
        axis="-Z"
    return axis

def applymatrix_to_xml(cur_obj=None,obj_xml=None):
    matrixlocal = cur_obj.GetMl()
    matrix=str(matrixlocal.v1.x)+","+str(matrixlocal.v1.y)+","+str(matrixlocal.v1.z)+",0,"
    matrix+=str(matrixlocal.v2.x)+","+str(matrixlocal.v2.y)+","+str(matrixlocal.v2.z)+",0,"
    matrix+=str(matrixlocal.v3.x)+","+str(matrixlocal.v3.y)+","+str(matrixlocal.v3.z)+",0,"
    matrix+=str(matrixlocal.off.x)+","+str(matrixlocal.off.y)+","+str(matrixlocal.off.z)+",1"
    obj_xml.setAttribute("matrix",matrix)
    rel_pos=cur_obj.GetRelPos()
    rel_scale=cur_obj.GetRelScale()
    rel_rot=cur_obj.GetRelRot()
    obj_xml.setAttribute("posx",str(rel_pos.x)) 
    obj_xml.setAttribute("posy",str(rel_pos.y)) 
    obj_xml.setAttribute("posz",str(rel_pos.z))
    obj_xml.setAttribute("scalex",str(rel_scale.x)) 
    obj_xml.setAttribute("scaley",str(rel_scale.y)) 
    obj_xml.setAttribute("scalez",str(rel_scale.z)) 
    obj_xml.setAttribute("rotx",str(((rel_rot.x/3.14159265359)*180))) 
    obj_xml.setAttribute("roty",str(((rel_rot.y/3.14159265359)*180)))
    obj_xml.setAttribute("rotz",str(((rel_rot.z/3.14159265359)*180)))    

def get_tex_def(cur_obj=None,obj_xml=None):
    for i in cur_obj.GetTags():
       if i.GetType()==5616:# Texture tag gefunden:
            xml_tex=dom.Element("texTag")
            xml_tex.setAttribute("name",str(i.GetMaterial().GetName())) 
            xml_tex.setAttribute("selection",str(i[c4d.TEXTURETAG_RESTRICTION])) 
            obj_xml.appendChild(xml_tex) 

def resetAllObjects(objList=None):
    for cur_obj in objList:
        if cur_obj.GetTag(1024237):#	reset morphtags
            all_tags=cur_obj.GetTags()#get all tags applied to object
            for morphtag in all_tags:#do for each tag:
                if morphtag.GetType()==1024237:#do if the tag is a morphtag
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
        resetAllObjects(cur_obj.GetChildren())