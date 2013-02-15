import c4d
from c4d import documents

from awdexporter import ids

 
def read_extrudeNurbs(self,cur_obj=None,obj_xml=None):        
    
    obj_xml.setAttribute("moveX",str( cur_obj[c4d.EXTRUDEOBJECT_MOVE].x))#set XML-Node-Attribute "name"
    obj_xml.setAttribute("moveY",str( cur_obj[c4d.EXTRUDEOBJECT_MOVE].y))#set XML-Node-Attribute "name"
    obj_xml.setAttribute("moveZ",str( cur_obj[c4d.EXTRUDEOBJECT_MOVE].z))#set XML-Node-Attribute "name"
    obj_xml.setAttribute("sub",str( cur_obj[c4d.EXTRUDEOBJECT_SUB]))#set XML-Node-Attribute "name"
    obj_xml.setAttribute("isosub",str( cur_obj[c4d.EXTRUDEOBJECT_ISOPARM]))#set XML-Node-Attribute "name"
    obj_xml.setAttribute("flipNormals",str( cur_obj[c4d.EXTRUDEOBJECT_FLIPNORMALS]))#set XML-Node-Attribute "name"
    obj_xml.setAttribute("hierarchical",str( cur_obj[c4d.EXTRUDEOBJECT_HIERARCHIC]))#set XML-Node-Attribute "name"
    
    
    
def read_joint(self,cur_obj=None,obj_xml=None):
    #dist = (p1.__mul__(p2))
    obj_xml.setAttribute("WeightTagIndex",str(cur_obj.GetWeightTag()))
    #if cur_obj.GetUp().GetType()!=1019362:            
    #obj_xml.setAttribute("type2","RootJOINT")

def read_cam(self,cur_obj=None,obj_xml=None):
    obj_xml.setAttribute("enable","0")
    obj_xml.setAttribute("fl",str(cur_obj[c4d.CAMERA_FOCUS]))
    obj_xml.setAttribute("fov_hor",str((cur_obj[c4d.CAMERAOBJECT_FOV]/3.14159265359)*180))
    obj_xml.setAttribute("fov_ver",str((cur_obj[c4d.CAMERAOBJECT_FOV_VERTICAL]/3.14159265359)*180))
    
   
    
def read_light(self,cur_obj=None,obj_xml=None):
    obj_xml.setAttribute("innerVisibleRadius",str(cur_obj[c4d.LIGHT_VISIBILITY_INNERDISTANCE]))
    obj_xml.setAttribute("outerVisibleRadius",str(cur_obj[c4d.LIGHT_VISIBILITY_OUTERDISTANCE]))
    obj_xml.setAttribute("brightness",str(cur_obj[c4d.LIGHT_BRIGHTNESS]))
    color_ar= str(cur_obj[c4d.LIGHT_COLOR].x)+"#"+str(cur_obj[c4d.LIGHT_COLOR].y)+"#"+str(cur_obj[c4d.LIGHT_COLOR].z)
    obj_xml.setAttribute("lightColor",color_ar)
    lightType=str(cur_obj[c4d.LIGHT_TYPE])
    if cur_obj[c4d.LIGHT_TYPE]==0:
        lightType="Point"
    if cur_obj[c4d.LIGHT_TYPE]==3:
        lightType="Directional"
    obj_xml.setAttribute("lightTyp",lightType)
       
    
def read_cone(self,cur_obj=None,obj_xml=None):
    obj_xml.setAttribute("TopRadius",str(cur_obj[c4d.PRIM_CONE_TRAD]))
    obj_xml.setAttribute("BottomRadius",str(cur_obj[c4d.PRIM_CONE_BRAD]))
    obj_xml.setAttribute("Height",str(cur_obj[c4d.PRIM_CONE_HEIGHT]))
    obj_xml.setAttribute("HSub",str(cur_obj[c4d.PRIM_CONE_HSUB]))
    obj_xml.setAttribute("RSub",str(cur_obj[c4d.PRIM_CONE_SEG]))
    axis=self.read_axis_orientation_combobox(cur_obj[c4d.PRIM_AXIS])
    obj_xml.setAttribute("axis",axis)
    self.get_tex_def(cur_obj,obj_xml) 

def read_cylinder(self,cur_obj=None,obj_xml=None):
    obj_xml.setAttribute("radius",str(cur_obj[c4d.PRIM_CYLINDER_RADIUS]))#set XML-Node-Attribute "name"
    obj_xml.setAttribute("height",str(cur_obj[c4d.PRIM_CYLINDER_HEIGHT]))#set XML-Node-Attribute "name"
    obj_xml.setAttribute("hsub",str(cur_obj[c4d.PRIM_CYLINDER_HSUB]))#set XML-Node-Attribute "name"
    obj_xml.setAttribute("rsub",str(cur_obj[c4d.PRIM_CYLINDER_SEG]))#set XML-Node-Attribute "name"
    axis=self.read_axis_orientation_combobox(cur_obj[c4d.PRIM_AXIS])
    obj_xml.setAttribute("axis",axis)
    self.get_tex_def(cur_obj,obj_xml)

def read_sphere(self,cur_obj=None,obj_xml=None):
    obj_xml.setAttribute("radius",str(cur_obj[c4d.PRIM_SPHERE_RAD]))#set XML-Node-Attribute "name"
    obj_xml.setAttribute("sub",str(cur_obj[c4d.PRIM_SPHERE_SUB]))#set XML-Node-Attribute "name"
    self.get_tex_def(cur_obj,obj_xml) 
    
def read_null(self,cur_obj=None,obj_xml=None): 
    self.get_tex_def(cur_obj,obj_xml)
        
def read_plane(self,cur_obj=None,obj_xml=None): 
    obj_xml.setAttribute("width",str(cur_obj[c4d.PRIM_PLANE_WIDTH]))
    obj_xml.setAttribute("height",str(cur_obj[c4d.PRIM_PLANE_HEIGHT]))
    obj_xml.setAttribute("wsub",str(cur_obj[c4d.PRIM_PLANE_SUBW]))
    obj_xml.setAttribute("hsub",str(cur_obj[c4d.PRIM_PLANE_SUBH]))
    axis=self.read_axis_orientation_combobox(cur_obj[c4d.PRIM_AXIS])
    obj_xml.setAttribute("axis",axis)
    self.get_tex_def(cur_obj,obj_xml)

    
def read_user_data(self,cur_mesh=None):
    count=0
    for id, bc in cur_mesh.GetUserDataContainer():
        if bc.GetId()==1:#userdataGruppe
            print "userdatagruppegefunden   "+str(bc.GetString(c4d.DESC_NAME))
        if bc.GetId()==19:#float
            print "float gefunden  "+str(bc.GetString(c4d.DESC_NAME))+"  "+str(cur_mesh[id])
        if bc.GetId()==400006001:#boole
            print "boole gefunden  "+str(bc.GetString(c4d.DESC_NAME))+"  "+str(cur_mesh[id])
        #print bc.GetId()
        count+=1    
        #for index, value in bc:
               #print "Index: %i, Value: %s", index, str(value)
    
        for z in bc:
            eins=0#print z
          
def read_shape(self,cur_mesh=None,cur_xml=None):
    xml_verts=dom.Element("Verts") 
    if cur_mesh.GetTag(5600):#"Vertices-Tag", this Tag is not shown in c4d ObjectManager, but every Polygon-Object should own it 
        pass    #print "Vertices found:"+str(cur_mesh.GetTag(5600).GetDataCount())
        points_export=""
        for i in cur_mesh.GetAllPoints():
            points_export+=str(i.x)+","+str(i.y)+","+str(i.z)+","
        xml_verts.setAttribute("count",str(len(cur_mesh.GetAllPoints())))#set XML-Node-Attribute "name"
            xml_verts.setAttribute("name","Points")  
            xml_verts.setAttribute("data",points_export)  
            cur_xml.appendChild(xml_verts)
def read_cube(self,cur_obj=None,obj_xml=None): 
    obj_xml.setAttribute("type","CUBE")  
    obj_xml.setAttribute("sizeX",str(cur_obj[c4d.PRIM_CUBE_LEN].x))
    obj_xml.setAttribute("sizeY",str(cur_obj[c4d.PRIM_CUBE_LEN].y))
    obj_xml.setAttribute("sizeZ",str(cur_obj[c4d.PRIM_CUBE_LEN].z)) 
    obj_xml.setAttribute("subx",str(cur_obj[c4d.PRIM_CUBE_SUBX])) 
    obj_xml.setAttribute("suby",str(cur_obj[c4d.PRIM_CUBE_SUBY]))
    obj_xml.setAttribute("subz",str(cur_obj[c4d.PRIM_CUBE_SUBZ]))
    self.get_tex_def(cur_obj,obj_xml)