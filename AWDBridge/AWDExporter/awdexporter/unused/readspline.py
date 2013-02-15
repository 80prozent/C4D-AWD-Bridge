import c4d
from c4d import documents

from awdexporter import ids

 
def read_one_spline_seqment(self,cur_obj,obj_xml):
    xml_spline_seq=dom.Element("SplineSegment") 
    xml_spline_seq.setAttribute("name","Segment1")
    spline_str=""
    tangent_str=""        
    pointcounter=0
    while pointcounter<len(cur_obj.GetAllPoints()):            
        spline_str+=str(cur_obj.GetAllPoints()[pointcounter].x)
        spline_str+=","+str(cur_obj.GetAllPoints()[pointcounter].y)
        spline_str+=","+str(cur_obj.GetAllPoints()[pointcounter].z)+"#"
        if cur_obj.GetTangentCount()>0:
            tangent_data=cur_obj.GetTangent(pointcounter)
            tangent1=tangent_data["vl"]
            tangent2=tangent_data["vr"]
            tangent_str+=str(tangent1.x)+","
            tangent_str+=str(tangent1.y)+","
            tangent_str+=str(tangent1.z)+","
            tangent_str+=str(tangent2.x)+","
            tangent_str+=str(tangent2.y)+","
            tangent_str+=str(tangent2.z)+"#"
        pointcounter+=1
    xml_spline_seq.setAttribute("data",spline_str)#set XML-Node-Attribute "name"
    xml_spline_seq.setAttribute("tangentData", tangent_str)#set XML-Node-Attribute "name"
    obj_xml.appendChild(xml_spline_seq)

def read_all_spline_seqments(self,cur_obj,obj_xml):
    segmentcount=0    
    segmentcount2=0        
    pointcounter=0
    while segmentcount<cur_obj.GetSegmentCount(): 
        segment = cur_obj.GetSegment(segmentcount)
        segmentcount2+=segment["cnt"]
        xml_spline_seq=dom.Element("SplineSegment") 
        xml_spline_seq.setAttribute("name","Segment"+str(segmentcount))
        spline_str=""
        tangent_str=""  
        while pointcounter<segmentcount2:            
            spline_str+=str(cur_obj.GetAllPoints()[pointcounter].x)
            spline_str+=","+str(cur_obj.GetAllPoints()[pointcounter].y)
            spline_str+=","+str(cur_obj.GetAllPoints()[pointcounter].z)+"#"
            if cur_obj.GetTangentCount()>0:
                tangent_data=cur_obj.GetTangent(pointcounter)
                tangent1=tangent_data["vl"]
                tangent2=tangent_data["vr"]
                tangent_str+=str(tangent1.x)+","
                tangent_str+=str(tangent1.y)+","
                tangent_str+=str(tangent1.z)+","
                tangent_str+=str(tangent2.x)+","
                tangent_str+=str(tangent2.y)+","
                tangent_str+=str(tangent2.z)+"#"
            pointcounter+=1
        xml_spline_seq.setAttribute("data",spline_str)#set XML-Node-Attribute "name"
        xml_spline_seq.setAttribute("tangentData", tangent_str)#set XML-Node-Attribute "name"
        xml_spline_seq.setAttribute("spline_closed",str(segment["closed"]))#set XML-Node-Attribute "name"
        obj_xml.appendChild(xml_spline_seq)
        segmentcount+=1

def read_spline(self,cur_obj=None,obj_xml=None):
    typofspline=""
    if cur_obj[c4d.SPLINEOBJECT_TYPE]==0:
        typofspline="Linear"
    if cur_obj[c4d.SPLINEOBJECT_TYPE]==1:
        typofspline="Cubic"
    if cur_obj[c4d.SPLINEOBJECT_TYPE]==2:
        typofspline="Akima"
    if cur_obj[c4d.SPLINEOBJECT_TYPE]==3:
        typofspline="B-Spline"
    if cur_obj[c4d.SPLINEOBJECT_TYPE]==4:
        typofspline="Bezier"
    obj_xml.setAttribute("typ_of_spline",typofspline)#set XML-Node-Attribute "name"
    obj_xml.setAttribute("closed",str(cur_obj[c4d.SPLINEOBJECT_CLOSED]))#set XML-Node-Attribute "name"
    
    interpolate=""
    if cur_obj[c4d.SPLINEOBJECT_INTERPOLATION]==0:
        interpolate="None"
    if cur_obj[c4d.SPLINEOBJECT_INTERPOLATION]==1:
        interpolate="Natural"
    if cur_obj[c4d.SPLINEOBJECT_INTERPOLATION]==2:
        interpolate="Uniform"
    if cur_obj[c4d.SPLINEOBJECT_INTERPOLATION]==3:
        interpolate="Adaptive"
    if cur_obj[c4d.SPLINEOBJECT_INTERPOLATION]==4:
        interpolate="Subdivided"
    obj_xml.setAttribute("spline_interpolate",interpolate)#set XML-Node-Attribute "name"
    obj_xml.setAttribute("spline_number",str(cur_obj[c4d.SPLINEOBJECT_SUB]))#set XML-Node-Attribute "name"
    obj_xml.setAttribute("spline_angle",str(cur_obj[c4d.SPLINEOBJECT_ANGLE]))#set XML-Node-Attribute "name"
    obj_xml.setAttribute("spline_maxlength",str(cur_obj[c4d.SPLINEOBJECT_MAXIMUMLENGTH]))#set XML-Node-Attribute "name"

            if cur_obj.GetSegmentCount()==0:
                read_one_spline_seqment(cur_obj,obj_xml)
            if cur_obj.GetSegmentCount()>0:
                read_all_spline_seqments(cur_obj,obj_xml)
    
    

			