import c4d
from c4d import documents

from awdexporter import ids
from awdexporter import objectTypes

 

	#export_bool=True
    #obj_newsDic={}
    #mat_namesDic={}
    #error_objects=[]
    #double_name=""
    #doubled_mats_name=[]
    #unsupportedObjects=[]
    #invatidMorphTags_state=[]
    #invatidMorphTags_names=[]
    #error_objects.append(double_name)
    #error_objects.append(doubled_mats_name)
    ##error_objects.append(unsupportedObjects)
    #error_objects.append(invatidMorphTags_state)
    #export_bool=self.check_for_double_names(curObj,obj_newsDic,used_mat_names,error_objects,lights_Dic)
    #print str(export_bool)     
    #if export_bool==False:#showing error if found double names in objects
    #    gui.MessageDialog("Each Object needs to have a unique Name ! \n This Name was found Double: '"+str(error_objects[0])+"'")
    #if export_bool==True:
    #    doc=documents.GetActiveDocument()
    #    returner=self.check_for_double_mat_names(doc,mat_namesDic,used_mat_names,error_objects)#same as above but for materials
    #    export_bool=returner[0]
    #    any_unused_Mats=returner[1]
    #    if export_bool==False:#showing error if found double names in materials 
    #        gui.MessageDialog("Each Material needs to have a unique Name ! \n This Name was found Double: '"+str(error_objects[1])+"'")
    return #export_bool
    
def check_for_double_names(self,curObj,namesDic,used_mat_names,error_objects,lightDic):
    if curObj.GetType() == 5102:
        self.read_light_routing(curObj,lightDic);
    self.check_standart_tags(curObj,used_mat_names,error_objects)
    returner=True
    pointIndex=namesDic.get(curObj.GetName(),-1) 
    if pointIndex==-1:
        namesDic[str(curObj.GetName())]="1"
        for object_child in curObj.GetChildren():
             returner=self.check_for_double_names(object_child,namesDic,used_mat_names,error_objects,lightDic)
             if returner==False:
                  break
    if pointIndex>=0:
        returner=False
        error_objects[0]=curObj.GetName()
    return returner          
    
    
def check_for_double_mat_names(self,cur_doc,nameDic,mats_used,error_objects):
    #checks if any double named materials exists, and if all materials are used in scene or not.
    all_mats=cur_doc.GetMaterials()
    i=0
    mats_unique=True
    mats_unused=False
    returner=[]
    while i <len(all_mats):
        matnameIndex=nameDic.get(str(all_mats[i].GetName()),-1)
        if matnameIndex==-1:
            nameDic[str(all_mats[i].GetName())]="1"
        if matnameIndex>=0:
            error_objects[1]=all_mats[i].GetName()
            mats_unique=False
            break
        i+=1
    if mats_unique==True:
        if len(mats_used)<len(all_mats):
            mats_unused=True
    returner.append(mats_unique)
    returner.append(mats_unused)
    return returner   
       
def check_standart_tags(self,curObj,used_mat_names,error_objects):
    #global morphTags_in_EditMode,double_named_morphTags,morphTags_with_unlinkedMorphs
    all_tags=curObj.GetTags()
    morphtag_names=[]
    for tag in all_tags:
        if tag.GetType()==5616:# found a Texture-tag:
            # collect all names of found materials in a Dic (every Name is only stored once)
            matnameIndex=used_mat_names.get(str(tag.GetMaterial().GetName()),-1)
            if matnameIndex==-1:
                used_mat_names[str(tag.GetMaterial().GetName())]="1"
        if tag.GetType()==1024237 and tag.GetType()=="Dontdothis":# found a Morph-tag:
            if tag.GetMode()==0:# if morpg-tag is not in animation-state it is not valid:
                morph_error=[]
                morph_error.append("MorphTag must be set to animation!")
                morph_error.append(str(curObj.GetName()))
                morph_error.append(str(tag.GetName()))
                error_objects[3].append(morph_error)
            if tag.GetMode()==1:
                checkname=checkmorphnames(tag.GetName(),morphtag_names)
                if checkname==True:
                    returner=check_morphtag_single(tag,curObj)
                    if returner[0]==False:
                        error_morph3=[curObj.GetName(),tag.GetName(),returner[1]]
                        morphTags_with_unlinkedMorphs.append(error_morph3)
                if checkname==False:
                    morph_error=[]
                    morph_error.append("Each MorphTag needs a unique name!")
                    morph_error.append(str(curObj.GetName()))
                    morph_error.append(str(tag.GetName()))
                    error_objects[3].append(morph_error)
     
    
def checkmorphnames(self,cur_morphname,cur_morphnames):
    return_bool=True
    morphnameIndex=cur_morphnames.get(str(cur_morphname),-1)
    if morphnameIndex==-1:
            cur_morphnames[str(cur_morphname)]="1"
    if morphnameIndex>=0:
            return_bool=False
    return return_bool

 
def check_morphtag_single(self,tag,cur_mesh):
    return_ar=[True,0]
    valid_track=False
    invalid_tracks=[]
    invalid_tracks2=[]
    morphnames={}
    morphnames.append("BaseMorph")
    morph_foundTrack=[]
    morph_foundTrack.append(True)
    for morphcount in range(1, tag.GetMorphCount()): 
        doublenamecheck=checkmorphnames(tag.GetMorph(morphcount).GetName(),morphnames)
        if doublenamecheck==False:
            return_ar=[False,1]
        if doublenamecheck==True:
            morph_foundTrack.append(False)
    if return_ar[0]==True:
        c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED) 
        if len(tag.GetCTracks())!=(len(morphnames)-1):
            return_ar=[False,2]
        if len(tag.GetCTracks())==(len(morphnames)-1):
            tracknames={}
            for track in tag.GetCTracks():
                doublenamecheck=checkmorphnames(track.GetName(),tracknames)
                if doublenamecheck==False:
                    return_ar=[False,3]
                if doublenamecheck==True:
                    curve = track.GetCurve()
                    if curve.GetKeyCount()<=0:
                        return_ar=[False,4]
                    if curve.GetKeyCount()>0:
                        valid_track,morph=find_name(morphnames,morph_foundTrack,track.GetName())
                        if valid_track==False:
                            return_ar=[False,5]
                            invalid_tracks.append(track.GetName())
        if return_ar[0]==True:
            for morphcount in range(1, tag.GetMorphCount()):  
                if morph_foundTrack[morphcount]==False:
                    return_ar=[False,6]
    return return_ar
   