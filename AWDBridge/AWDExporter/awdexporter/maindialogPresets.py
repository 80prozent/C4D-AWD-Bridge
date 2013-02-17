# classes to load and save a preset for the dialog

import c4d
from awdexporter import ids

from xml.dom import minidom
import xml.dom.minidom as dom

def savePreset(mainDialog):
    datei=c4d.storage.SaveDialog(c4d.FILESELECTTYPE_ANYTHING, "save Preset", "set")
    output_xml = dom.Document()
    preset_xml=dom.Element("AWDExporterPreset")
    preset_xml.setAttribute("scale",str(mainDialog.scale))
    preset_xml.setAttribute("unusedMats",str(mainDialog.unusedMats))
    preset_xml.setAttribute("selectedOnly",str(mainDialog.selectedOnly))
    preset_xml.setAttribute("streaming",str(mainDialog.streaming))
    preset_xml.setAttribute("compressData",str(mainDialog.compressData))
    preset_xml.setAttribute("debug",str(mainDialog.debug))
    preset_xml.setAttribute("closeAfter",str(mainDialog.closeAfter))
    preset_xml.setAttribute("textures",str(mainDialog.textures))
    preset_xml.setAttribute("copyTextures",str(mainDialog.copyTextures))
    preset_xml.setAttribute("texturesURL",str(mainDialog.texturesURL))
    preset_xml.setAttribute("animationBool",str(mainDialog.animationBool))
    preset_xml.setAttribute("animationRange",str(mainDialog.animationRange))
    preset_xml.setAttribute("firstFrame",str(mainDialog.firstFrame))
    preset_xml.setAttribute("lastFrame",str(mainDialog.lastFrame))
    output_xml.appendChild(preset_xml)
    if datei!=None:    
        str_object_xml=output_xml.toprettyxml()  
        f = open(datei, 'wb')
        f.write(str_object_xml)
        f.close()
    return True

def loadPreset(mainDialog):

    datei=c4d.storage.LoadDialog(c4d.FILESELECTTYPE_ANYTHING, "open Preset", c4d.FILESELECT_LOAD,"set")  
    if datei!=None:               
        dom1 = dom.parse(datei) 
        if dom1.firstChild.getAttribute("scale"):
            mainDialog.scale=float(dom1.firstChild.getAttribute("scale"))
        if dom1.firstChild.getAttribute("unusedMats")=="True":
            mainDialog.unusedMats=True
        if dom1.firstChild.getAttribute("selectedOnly")=="True":
            mainDialog.selectedOnly=True
        if dom1.firstChild.getAttribute("streaming")=="True":
            mainDialog.streaming=True
        if dom1.firstChild.getAttribute("compressData")=="True":
            mainDialog.compressData=True
        if dom1.firstChild.getAttribute("debug")=="True":
            mainDialog.debug=True
        if dom1.firstChild.getAttribute("closeAfter")=="True":
            mainDialog.closeAfter=True
        if dom1.firstChild.getAttribute("textures"):
            mainDialog.textures=int(dom1.firstChild.getAttribute("textures"))
        if dom1.firstChild.getAttribute("copyTextures")=="True":
            mainDialog.copyTextures=True
        if dom1.firstChild.getAttribute("texturesURL"):
            mainDialog.texturesURL=dom1.firstChild.getAttribute("texturesURL")
        if dom1.firstChild.getAttribute("animationBool")=="True":
            mainDialog.animationBool=True
        if dom1.firstChild.getAttribute("animationRange"):
            mainDialog.animationRange=int(dom1.firstChild.getAttribute("animationRange"))
        if dom1.firstChild.getAttribute("firstFrame"):
            mainDialog.firstFrame=float(dom1.firstChild.getAttribute("firstFrame"))
        if dom1.firstChild.getAttribute("lastFrame"):
            mainDialog.lastFrame=float(dom1.firstChild.getAttribute("lastFrame"))


    mainDialogHelper.setUI(mainDialog)
    return True
        
 
  