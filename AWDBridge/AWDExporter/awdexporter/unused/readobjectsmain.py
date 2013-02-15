import c4d
from c4d import documents

from awdexporter import ids


def read_selected_object(self,cur_obj,objSettings,lights_Dic):
    obj_xml=dom.Element("Dape_obj")#create a new XML-Node
    attributes_xml=dom.Element("Attributes")#create a new XML-Node
    obj_xml.setAttribute("visible",str(cur_obj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR]))#set XML-Node-Attribute "name"
    obj_xml.setAttribute("name",cur_obj.GetName())#set XML-Node-Attribute "name"
    obj_xml.appendChild(attributes_xml)
    self.read_standart_tags(cur_obj,attributes_xml)
    if cur_obj.GetTag(1027939):
        print str(cur_obj.GetTag(1027939)[c4d.COA_SENDCALL])
    supported_object=self.check_for_supported_type(cur_obj,obj_xml)#check if object is of supported type, execute parsing function and append data to XML       
    if supported_object==False:#if objects type not supported:
        obj_xml.setAttribute("type","NULL")#all unsupported and unknown objects are converted to nulls
    lightStr=""
    if cur_obj.GetType() != 5102:
        obj_xml.setAttribute("lights",lightStr)
        if len(lights_Dic)>0:
            lightStr=""
        for light in lights_Dic:
            if light[1]==True:
                isInlist=light[2].get(cur_obj.GetName(),-1) 
                if isInlist==-1:
                    lightStr+=str(light[0])+"#"
                if light[1]==False:
                    isInlist=light[2].get(cur_obj.GetName(),-1) 
                if isInlist>=0:
                    lightStr+=str(light[0])+"#"

        obj_xml.setAttribute("lights",lightStr)
    print str(cur_obj.GetName())+"   -   "+lightStr
    
    if len(cur_obj.GetChildren())>0:
        for k in cur_obj.GetChildren():
            obj_xml2=self.read_selected_object(k,objSettings,lights_Dic)
            obj_xml.appendChild(obj_xml2)
    self.applymatrix_to_xml(cur_obj,obj_xml)#set XML-Node-Attribute "matrix" as raw matrix (16 x float) - its the objects local matrix
    return obj_xml
    
    #end of function read_object()  ----------<<<<<<<<<<<<<<
def check_and_read_morphParams(self,cur_obj=None,obj_xml=None):  
    if cur_obj.GetType() == 5101:
        self.read_spline(cur_obj,obj_xml)
    
    if cur_obj.GetType() == 5168:
        self.read_plane(cur_obj,obj_xml)
    
    if cur_obj.GetType() == 5162:
        self.read_cone(cur_obj,obj_xml);
     
    if cur_obj.GetType() == 5170:
        self.read_cylinder(cur_obj,obj_xml); 
    
    if cur_obj.GetType() == 5160:
        self.read_sphere(cur_obj,obj_xml);
    
    if cur_obj.GetType() == 5159:
        self.read_cube(cur_obj,obj_xml)   
    
    if cur_obj.GetType() == 1019362:
        self.read_joint(cur_obj,obj_xml);
    
    if cur_obj.GetType() == 5102:
        self.read_light(cur_obj,obj_xml);
    
    if cur_obj.GetType() == 5103:
        self.read_cam(cur_obj,obj_xml); 
    
    


def read_standart_tags(self,cur_obj=None,cur_xml=None):
    all_tags=cur_obj.GetTags()
    for tag in all_tags:
        print str(tag.GetType())
        if tag.GetType()==1024237:
            if tag.GetMode()==1:
                self.read_morphtag_single(cur_obj,tag,cur_xml,cur_obj)
            if tag.GetType()==1001149:
            xml_xpressotag=dom.Element("XpressoTag")
            xml_xpressotag.setAttribute("name",str(tag.GetName()))
            xml_xpressotag.setAttribute("type",str(tag.GetName()))
            cur_xml.appendChild(xml_xpressotag)
            #print "Xpresso "+str(cur_obj.GetTag(1001149).GetName())+"   "+str(len(cur_obj.GetTag(1001149).GetNodeMaster().GetRoot().GetChildren()))
            #for s in cur_obj.GetTag(1001149).GetNodeMaster().GetRoot().GetChildren():
                #pass#print len(s.GetOutPorts())
                #print s.GetOwnerID()
                #print s.GetName()

