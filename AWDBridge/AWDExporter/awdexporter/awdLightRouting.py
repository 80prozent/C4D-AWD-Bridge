import c4d
from c4d import documents

from awdexporter import ids

class LightRouter(Object):
    def __init__(self):
        self.name = "undefined"
def read_light_routing(self,curObj=None,exportData.light_dic=None):
    lightType="unsupported"
    if curObj[c4d.LIGHT_TYPE]==0:
        lightType="Point"
    if curObj[c4d.LIGHT_TYPE]==3:
        lightType="Directional"
    if lightType!="unsupported":
        objCount=0
        lightObjectDic={}
        ex_or_included=True
        if curObj[c4d.LIGHT_EXCLUSION_MODE]==0:
            ex_or_included=False
        if curObj[c4d.LIGHT_EXCLUSION_MODE]==1:
            ex_or_included=True
        while objCount < curObj[c4d.LIGHT_EXCLUSION_LIST].GetObjectCount():
            if curObj[c4d.LIGHT_EXCLUSION_LIST].ObjectFromIndex(documents.GetActiveDocument(),objCount):
                lightObjectDic[str(curObj[c4d.LIGHT_EXCLUSION_LIST].ObjectFromIndex(documents.GetActiveDocument(),objCount).GetName())]=0
                if curObj[c4d.LIGHT_EXCLUSION_LIST].GetFlags(objCount)>7:
                    for child1 in curObj[c4d.LIGHT_EXCLUSION_LIST].ObjectFromIndex(documents.GetActiveDocument(),objCount).GetChildren():
                        self.read_light_routing_recursiv(child1,lightObjectDic,ex_or_included)
            objCount+=1
            newlightObject=[]
            newlightObject.append(curObj.GetName())
            newlightObject.append(ex_or_included)
            newlightObject.append(lightObjectDic)
            light_dic.append(newlightObject)
    
def read_light_routing_recursiv(self,curObj=None,light_dic=None,ex_or_included=None):
    light_dic[str(curObj.GetName())]=ex_or_included
    for child in curObj.GetChildren():
        self.read_light_routing_recursiv(child,light_dic)   