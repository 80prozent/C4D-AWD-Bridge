import c4d
from c4d import documents

from awdexporter import ids

     
    
          
def read_hirarchy_morphs(self,cur_obj=None,cur_xml=None):
    if cur_obj.GetTag(1024237):#only do if object got any morphtag applied
        all_tags=cur_obj.GetTags()#get all tags applied to object
        for morphtag in all_tags:#do for each tag:
            if morphtag.GetType()==1024237:#do if the tag is a morphtag
                if morphtag.GetMode()==1:#do if the tag is in animation-mode:
                    if str(morphtag[c4d.ID_CA_POSE_HIERARCHY])=="1":
                        doc.SetTime(c4d.BaseTime(0, fps))
                        c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
                        c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
                        doc.SetTime(doc.GetTime())
                        c4d.EventAdd(c4d.EVENT_ANIMATE)
                        for track in morphtag.GetCTracks():
                            curve = track.GetCurve()
                            if curve.GetKeyCount()>0:
                                if len(cur_obj.GetChildren())>0:
                                    childcount=1
                                    for k in cur_obj.GetChildren():
                                        self.read_hirarchys_morphs2(k,cur_xml.childNodes[childcount],morphtag.GetName(),cur_obj.GetName(),track.GetName(),morphtag,curve)
                                        childcount+=1
                            curve.GetKey(0).SetValue(curve,0.0)
    if len(cur_obj.GetChildren())>0:
        childcount=1
        for k in cur_obj.GetChildren():
            self.read_hirarchy_morphs(k,cur_xml.childNodes[childcount])
            childcount+=1
    
def read_hirarchys_morphs2(self,cur_obj=None,cur_xml=None,cur_name=None,cur_objname=None,cur_shapename=None,morphtag=None,curve=None):
     returned_xml=getmorphxml(cur_xml,cur_name,cur_objname);
     morphs_properties=str(morphtag[c4d.ID_CA_POSE_P])
     morphs_properties+="#"+str(morphtag[c4d.ID_CA_POSE_R])
     morphs_properties+="#"+str(morphtag[c4d.ID_CA_POSE_S])
     morphs_properties+="#"+str(morphtag[c4d.ID_CA_POSE_POINTS])
     morphs_properties+="#"+str(morphtag[c4d.ID_CA_POSE_UV])
     morphs_properties+="#"+str(morphtag[c4d.ID_CA_POSE_PARAM])
     morphs_properties+="#"+str(morphtag[c4d.ID_CA_POSE_USERDATA])
     morphs_properties+="#"+str(morphtag[c4d.ID_CA_POSE_HIERARCHY])
     morphs_properties+="#"+str(morphtag[c4d.ID_CA_POSE_MAPS])
     returned_xml.setAttribute("morphedAttributes",morphs_properties) 
     xml_morph=dom.Element("Morph") 

     morphname=str(cur_shapename)
     buildname=morphname.split(" ")
     resultname=str(buildname[0])
     if len(buildname)>2:
         thiscount=1
         while thiscount<(len(buildname)-1):   
             resultname+=" "+str(buildname[thiscount])
             thiscount+=1  
     xml_morph.setAttribute("name",str(resultname)) 
     
     curve.GetKey(0).SetValue(curve,0.0)  
     c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
     c4d.EventAdd(c4d.EVENT_ANIMATE)
     c4d.DrawViews(c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
     oldMatrix=cur_obj.GetMl()
     oldrel_pos=cur_obj.GetRelPos()
     oldrel_scale=cur_obj.GetRelScale()
     oldrel_rot=cur_obj.GetRelRot()
     curve.GetKey(0).SetValue(curve,1.0)  		
     c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
     c4d.EventAdd(c4d.EVENT_ANIMATE)
     c4d.DrawViews(c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
     #read morphstates local matrix:
     if morphtag[c4d.ID_CA_POSE_P]==1 or morphtag[c4d.ID_CA_POSE_S]==1 or morphtag[c4d.ID_CA_POSE_R]==1:
         rel_pos=cur_obj.GetRelPos()
         rel_scale=cur_obj.GetRelScale()
         rel_rot=cur_obj.GetRelRot()
         self.applymatrix_to_xml(cur_obj,xml_morph)
         xml_morph.setAttribute("posx",str(rel_pos.x-oldrel_pos.x)) 
         xml_morph.setAttribute("posy",str(rel_pos.y-oldrel_pos.y)) 
         xml_morph.setAttribute("posz",str(rel_pos.z-oldrel_pos.z))
         xml_morph.setAttribute("scalex",str(rel_scale.x-oldrel_scale.y)) 
         xml_morph.setAttribute("scaley",str(rel_scale.y-oldrel_scale.y)) 
         xml_morph.setAttribute("scalez",str(rel_scale.z-oldrel_scale.z)) 
         xml_morph.setAttribute("rotx",str(((rel_rot.x/3.14159265359)*180)-((oldrel_rot.x/3.14159265359)*180))) 
         xml_morph.setAttribute("roty",str(((rel_rot.y/3.14159265359)*180)-((oldrel_rot.y/3.14159265359)*180))) 
         xml_morph.setAttribute("rotz",str(((rel_rot.z/3.14159265359)*180)-((oldrel_rot.z/3.14159265359)*180)))   
         #read morphstates parameters:
     if morphtag[c4d.ID_CA_POSE_PARAM]==1:
         check_and_read_morphParams(cur_obj,xml_morph)
     if cur_obj.GetType()==5100:
         newPoints=[]
         newUVs=[]
         if morphtag[c4d.ID_CA_POSE_POINTS]==1:
             newPoints=cur_obj.GetAllPoints()
         if morphtag[c4d.ID_CA_POSE_UV]==1:
             newUVs=cur_obj.GetAllPoints()
         if morphtag[c4d.ID_CA_POSE_POINTS]==1 or morphtag[c4d.ID_CA_POSE_UV]==1:
             allPointAndUvMorpTag.append(PointAndUvMorpTag(cur_shapename,morphtag.GetName(),cur_obj,cur_objname,newPoints,newUVs))

     curve.GetKey(0).SetValue(curve,0.0)  
     c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
     c4d.EventAdd(c4d.EVENT_ANIMATE)
     c4d.DrawViews(c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
     returned_xml.appendChild(xml_morph)
     if len(cur_obj.GetChildren())>0:
        childcount=1
        for k in cur_obj.GetChildren():
            self.read_hirarchys_morphs2(k,cur_xml.childNodes[childcount],cur_name,cur_objname,cur_shapename,morphtag,curve)
            childcount+=1

def getmorphxml(self,cur_xml=None,cur_name=None,cur_objname=None):
    returner_xml=dom.Element("MorphTag");
    returner_xml.setAttribute("type","multi")  
    returner_xml.setAttribute("name",cur_name);
    returner_xml.setAttribute("controllerObj",cur_objname);
    returner_bool=False
    for k in cur_xml.childNodes[0].getElementsByTagName('MorphTag'):
        if str(k.attributes["type"].value)=="multi":
            if str(k.attributes["name"].value)==cur_name and str(k.attributes["controllerObj"].value)==cur_objname:
                returner_xml=k
                returner_bool=True
    if returner_bool==False:
        cur_xml.childNodes[0].appendChild(returner_xml)
    return returner_xml
    
    
def read_morphtags(self,cur_obj=None):
    if cur_obj.GetTag(1024237):#only do if object got any morphtag applied
        all_tags=cur_obj.GetTags()#get all tags applied to object
        for morphtag in all_tags:#do for each tag:
            if morphtag.GetType()==1024237:#do if the tag is a morphtag
                if morphtag.GetMode()==1:#do if the tag is in animation-mode:
                    doc.SetTime(c4d.BaseTime(0, fps))
                    c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
                    c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
                    doc.SetTime(doc.GetTime())
                    c4d.EventAdd(c4d.EVENT_ANIMATE)
                    for track in morphtag.GetCTracks():
                        curve = track.GetCurve()
                        if curve.GetKeyCount()>0:
                            curve.GetKey(0).SetValue(curve,0.0)
    if len(cur_obj.GetChildren())>0:
        for k in cur_obj.GetChildren():
            self.read_morphtags(k)

def read_morphtag_single(self,cur_obj,tag,cur_xml,cur_mesh,allPointAndUvMorpTag):
    valid_track=False
    invalid_tracks=[]
    morphnames=[]
    morphnames.append("BaseMesh")
    morph_foundTrack=[]
    morph_foundTrack.append(True)
    xml_morph_ar=[]
    doc=documents.GetActiveDocument()
    xml_morph_tag=dom.Element("MorphTag") 
    xml_morph_tag.setAttribute("type","single")  
    xml_morph_tag.setAttribute("name",str(tag.GetName()))  
    xml_morph_tag.setAttribute("tagObject",str(cur_obj.GetName()))  
    morphs_properties=str(tag[c4d.ID_CA_POSE_P])
    morphs_properties+="#"+str(tag[c4d.ID_CA_POSE_R])
    morphs_properties+="#"+str(tag[c4d.ID_CA_POSE_S])
    morphs_properties+="#"+str(tag[c4d.ID_CA_POSE_POINTS])
    morphs_properties+="#"+str(tag[c4d.ID_CA_POSE_UV])
    morphs_properties+="#"+str(tag[c4d.ID_CA_POSE_PARAM])
    morphs_properties+="#"+str(tag[c4d.ID_CA_POSE_USERDATA])
    morphs_properties+="#"+str(tag[c4d.ID_CA_POSE_HIERARCHY])
    morphs_properties+="#"+str(tag[c4d.ID_CA_POSE_MAPS])
    xml_morph_tag.setAttribute("morphedAttributes",morphs_properties) 
    xml_morph1=dom.Element("MorphTag") 
    xml_morph_ar.append(xml_morph1)
    for morphcount in range(1, tag.GetMorphCount()): 
        morphnames.append(str(tag.GetMorph(morphcount).GetName()))
        morph_foundTrack.append(False)
    c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED) 
    for track in tag.GetCTracks():
        doc.SetTime(c4d.BaseTime(0, fps))
        curve = track.GetCurve()
        if curve.GetKeyCount()>0:
            c4d.DrawViews(c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
            oldMatrix=cur_obj.GetMl()
            oldrel_pos=cur_obj.GetRelPos()
            oldrel_scale=cur_obj.GetRelScale()
            oldrel_rot=cur_obj.GetRelRot()
            curve.GetKey(0).SetValue(curve,1.0)
            c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
            c4d.EventAdd(c4d.EVENT_ANIMATE)
            c4d.DrawViews(c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
            valid_track,morph=find_name(morphnames,morph_foundTrack,track.GetName())
            xml_morph=dom.Element("Morph") 
            xml_morph.setAttribute("name",str(tag.GetMorph(morph).GetName()))          
            if valid_track==False:
                invalid_tracks.append(track.GetName())
            if valid_track==True:
                #read morphstates local matrix:
                if tag[c4d.ID_CA_POSE_P]==1 or tag[c4d.ID_CA_POSE_S]==1 or tag[c4d.ID_CA_POSE_R]==1:
                    rel_pos=cur_obj.GetRelPos()
                    rel_scale=cur_obj.GetRelScale()
                    rel_rot=cur_obj.GetRelRot()
                    self.applymatrix_to_xml(cur_obj,xml_morph)
                    xml_morph.setAttribute("posx",str(rel_pos.x-oldrel_pos.x)) 
                    xml_morph.setAttribute("posy",str(rel_pos.y-oldrel_pos.y)) 
                    xml_morph.setAttribute("posz",str(rel_pos.z-oldrel_pos.z))
                    xml_morph.setAttribute("scalex",str(rel_scale.x-oldrel_scale.x)) 
                    xml_morph.setAttribute("scaley",str(rel_scale.y-oldrel_scale.y)) 
                    xml_morph.setAttribute("scalez",str(rel_scale.z-oldrel_scale.z)) 
                    xml_morph.setAttribute("rotx",str(((rel_rot.x/3.14159265359)*180)-((oldrel_rot.x/3.14159265359)*180))) 
                    xml_morph.setAttribute("roty",str(((rel_rot.y/3.14159265359)*180)-((oldrel_rot.y/3.14159265359)*180))) 
                    xml_morph.setAttribute("rotz",str(((rel_rot.z/3.14159265359)*180)-((oldrel_rot.z/3.14159265359)*180)))   
                #read morphstates parameters:
                if tag[c4d.ID_CA_POSE_PARAM]==1:
                    check_and_read_morphParams(cur_obj,xml_morph)
                if cur_obj.GetType()==5100:
                    newPoints=[]
                    newUVs=[]
                    if tag[c4d.ID_CA_POSE_POINTS]==1:
                        newPoints=cur_obj.GetAllPoints()
                    if tag[c4d.ID_CA_POSE_UV]==1:
                        newUVs=cur_obj.GetAllPoints()
                    if tag[c4d.ID_CA_POSE_POINTS]==1 or tag[c4d.ID_CA_POSE_UV]==1:
                        allPointAndUvMorpTag.append(PointAndUvMorpTag(tag.GetMorph(morph).GetName(),tag.GetName(),cur_obj,cur_obj.GetName(),newPoints,newUVs))
                xml_morph_ar.append(xml_morph)
            curve.GetKey(0).SetValue(curve,0.0)
            c4d.DrawViews(c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
            c4d.EventAdd(c4d.EVENT_ANIMATE)
    c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
    validMorph=True
    for morphcount in range(1, tag.GetMorphCount()):                          
        if morph_foundTrack[morphcount]==False:  
            validMorph=False            
        if morph_foundTrack[morphcount]==True: 
            xml_morph_tag.appendChild(xml_morph_ar[morphcount])
    if validMorph==True:
        cur_xml.appendChild(xml_morph_tag)        
    
    
def readMorphedPoints(self,cur_mesh=None):
    pass
    
                 
def read_morphtag(self,tag,cur_xml,cur_mesh):
    #print "mode = "+str(tag.GetMode())
    #print "mode = "+str(tag[c4d.ID_CA_POSE_P])
    #print "mode = "+str(tag[c4d.ID_CA_POSE_S])
    #print "mode = "+str(tag[c4d.ID_CA_POSE_R])
    #print "mode = "+str(tag[c4d.ID_CA_POSE_POINTS])
    #print "mode = "+str(tag[c4d.ID_CA_POSE_UV])
    #print "mode = "+str(tag[c4d.ID_CA_POSE_PARAM])
    #print "mode = "+str(tag[c4d.ID_CA_POSE_USERDATA])
    #print "mode = "+str(tag[c4d.ID_CA_POSE_HIERARCHY])
    #print "mode = "+str(tag[c4d.ID_CA_POSE_MAPS])
    unit=1
    vertsNum  = cur_mesh.GetPointCount()
    valid_track=False
    invalid_tracks=[]
    morphnames=[]
    morphnames.append("BaseMesh")
    morph_foundTrack=[]
    morph_foundTrack.append(True)
    xml_morph_ar=[]
    xml_morph1=dom.Element("Morph") 
    xml_morph1.setAttribute("name","base")
    xml_morph1.setAttribute("morph_pos",str(tag[c4d.ID_CA_POSE_P]))
    xml_morph1.setAttribute("morph_rot",str(tag[c4d.ID_CA_POSE_R]))
    xml_morph1.setAttribute("morph_scale",str(tag[c4d.ID_CA_POSE_S]))
    xml_morph1.setAttribute("morph_points",str(tag[c4d.ID_CA_POSE_POINTS]))
    xml_morph1.setAttribute("morph_uv",str(tag[c4d.ID_CA_POSE_UV]))
    xml_morph1.setAttribute("morph_uv",str(tag[c4d.ID_CA_POSE_PARAM]))
    xml_morph1.setAttribute("morph_userdata",str(tag[c4d.ID_CA_POSE_USERDATA]))
    xml_morph1.setAttribute("morph_hirarchy",str(tag[c4d.ID_CA_POSE_HIRARCHY]))
    xml_morph1.setAttribute("morph_maps",str(tag[c4d.ID_CA_POSE_MAPS]))
    xml_morph_ar.append(xml_morph1)
    #print op.GetRelPos()
    doc.SetTime(c4d.BaseTime(0, fps))
    c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
    c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
    doc.SetTime(doc.GetTime())
    c4d.EventAdd(c4d.EVENT_ANIMATE)
    for morphcount in range(1, tag.GetMorphCount()): 
        morphnames.append(str(tag.GetMorph(morphcount).GetName()))
        morph_foundTrack.append(False)
        old_key_values=[]
    for track in tag.GetCTracks():#first loop trough all tracks
        curve = track.GetCurve()
        if curve.GetKeyCount()>0:
            old_key_values.append(curve.GetKey(0).GetValue())
            curve.GetKey(0).SetValue(curve,0.0)
    doc.SetTime(c4d.BaseTime(0, fps))
    c4d.DrawViews(c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
    oldc4dvecs = cur_mesh.GetAllPoints()
    old_pos=cur_mesh.GetRelPos()
    old_rot=cur_mesh.GetRelRot()
    old_scale=cur_mesh.GetRelScale()
    c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED) 
    for track in tag.GetCTracks():
        doc.SetTime(c4d.BaseTime(0, fps))
        curve = track.GetCurve()
        if curve.GetKeyCount()>0:
            curve.GetKey(0).SetValue(curve,1.0)
            valid_track,morph=find_name(morphnames,morph_foundTrack,track.GetName())
            #print "morphstate position = "+str(tag.GetMorph(morph).GetFirst()[c4d.ID_CA_POSE_P])
            xml_morph=dom.Element("Morph") 
            xml_morph.setAttribute("name",str(morphnames[morphcount]))
            
            if valid_track==False:
                invalid_tracks.append(track.GetName())
            if valid_track==True:
                c4d.DrawViews(c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
                c4dvecs = cur_mesh.GetAllPoints()
                blendverts = []
                for v in c4dvecs:
                    blendverts.append([v.x*unit,v.z*unit,v.y*unit])
                #code += "Key"+tcs+"verts = " + str(blendverts)+"\n"
                #code += "for v in range(0,"+str(vertsNum)+"):\n\tc4dmesh.verts[v].co.x = Key"+tcs+"verts[v][0]\n\tc4dmesh.verts[v].co.y = Key"+tcs+"verts[v][1]\n\tc4dmesh.verts[v].co.z = Key"+tcs+"verts[v][2]\n"
                #code += "shapeKey = ob.getData().getKey()\n"
                #code += "newIpo = Ipo.New('Key','newIpo')\n"
                #code += "if(shapeKey.ipo == None):   shapeKey.ipo = newIpo\n"
                #code += "if(shapeKey.ipo['Key "+tcs+"'] == None):   shapeKey.ipo.addCurve('Key "+tcs+"')\n"
         
                c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
                new_pos=cur_mesh.GetRelPos()
                new_rot=cur_mesh.GetRelRot()
                new_scale=cur_mesh.GetRelScale()
                self.applymatrix_to_xml(cur_mesh,xml_morph)
                #print "oldvecs = "+str(oldc4dvecs)    
                #print "newvecs = "+ str(c4dvecs)   
                #print "old_pos = "+ str(old_pos)   
                #print "new_pos = "+ str(new_pos) 
                #print "old_rot = "+ str(old_rot)   
                #print "new_rot = "+ str(new_rot) 
                #print "old_scale = "+ str(old_scale)   
                #print "new_scale = "+ str(new_scale) 
                keyCount = curve.GetKeyCount()
                curve.GetKey(0).SetValue(curve,0.0)
                for k in range(0,keyCount):
                    key = curve.GetKey(k)
                    value = key.GetValue()
                    frame = key.GetTime().GetFrame(fps)
                    #code += "shapeKey.ipo['Key "+tcs+"'].append(BezTriple.New("+str(float(frame))+","+str(value)+",0.0))\n"
            xml_morph_ar.append(xml_morph)
            c4d.EventAdd(c4d.EVENT_ANIMATE)
    c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
    value_counter=0
    for track in tag.GetCTracks():
        curve = track.GetCurve()
        if curve.GetKeyCount()>0:
            curve.GetKey(0).SetValue(curve,old_key_values[value_counter])
            value_counter+=1
    invalidmorphs=[]
    for morphcount in range(1, tag.GetMorphCount()):                        
        if morph_foundTrack[morphcount]==True: 
            cur_xml.appendChild(xml_morph_ar[morphcount])
        if morph_foundTrack[morphcount]==False:
            invalidmorphs.append(str(morphnames[morphcount]))
    if len(invalidmorphs)>0:
        invalidemorph_str="Couldnt find anmiation-tracks for this Morphs:\n"
        for inv_morh in invalidmorphs:
            invalidemorph_str+="\n - name = '"+str(inv_morh)+"' expected track: '"+str(inv_morh)+" Strength'\n"
        invalidemorph_str+="make shure a animation-track with the correct expected name exists for each morph you want to have exported\n"
        gui.MessageDialog(str(invalidemorph_str))
    if len(invalidmorphs)>0:
        invalidemorph_str="Couldnt find corresponding morphs for animationtracks:\n"
        for inv_track in invalid_tracks:
            find_name2=inv_track.split(" ")
            namefinder2=str(find_name2[0])
            if len(find_name2)>2:
                thiscount=1
                while thiscount<(len(find_name2)-1):   
                    namefinder2+=" "+str(find_name2[thiscount])
                    thiscount+=1  
                invalidemorph_str+="\n - track = '"+str(inv_track)+"' expected morph: '"+str(namefinder2)+"'\n"
        invalidemorph_str+="make shure a morph with the correct expected name exists for each animation track you want to have exported\n"
        gui.MessageDialog(str(invalidemorph_str))
    
    
    
def find_name(self,m_names,m_found,trackname):
    find_name=trackname.split(" ")
    namefinder2=str(find_name[0])
    if len(find_name)>2:
       thiscount=1
       while thiscount<(len(find_name)-1):   
            namefinder2+=" "+str(find_name[thiscount])
            thiscount+=1    
    namecount=0
    trackvalid=False
    morph=0
    while namecount < len(m_names):
        if m_names[namecount]==namefinder2:
            m_found[namecount]=True
            morph=namecount;
            namecount=len(m_names)
            trackvalid=True
        namecount+=1
    return trackvalid, morph
    

    
    
     
