import c4d
import os
from awdexporter import ids
from awdexporter import worker
from awdexporter import awdMainClass
from awdexporter import awdSkinningReader   
from awdexporter import awdMeshReader   
from awdexporter import canvas

from xml.dom import minidom
import xml.dom.minidom as dom

SCALE_DATA = 80008
UNUSEDMATERIALS_DATA = 80009
SELECTEDONLY_DATA = 80010
STREAMING_DATA = 80011
COMPRESSDATA_DATA = 80012
DEBUG_DATA = 80013
CLOSE_DATA = 80014

TEXTURES_DATA = 80015
COPYTEXTURES_DATA = 80016
TEXTURESURL_DATA = 80017
FIRSTFRAME_DATA = 80018
LASTFRAME_DATA = 80019
ANIMATION_DATA = 80020
RANGE_DATA = 80021
workerThread=None
exportData=None
enableObjects=[]
enableStates=[]
class MyThread(c4d.threading.C4DThread):    
    def Main(self):
        global exportData
        doc=c4d.documents.GetActiveDocument()
        doc.SetTime(c4d.BaseTime(5, doc.GetFps()))
        worker.export2(exportData,self)                
        c4d.StatusClear()
		
class MainDialog(c4d.gui.GeDialog):
       
    doc = c4d.documents.GetActiveDocument()

    userarea = None
    awdExporterData=None 
    sliderEditor = 1.0
    sliderRender = 1.0
    sliderEditorBool = False
    sliderRenderBool = False

    scale = 1.0
    unusedMats = False
    selectedOnly = False
    streaming = False
    compressData = False
    debug = False
    closeAfter = False

    textures=0
    copyTextures=False
    texturesURL=""
    firstFrame = doc.GetMinTime().GetFrame(doc.GetFps())
    lastFrame = doc.GetMaxTime().GetFrame(doc.GetFps())
    animationBool = False
    animationRange = int(0)
        
    def __init__(self):   
        self.userarea = canvas.Canvas()
        
    def CreateLayout(self):          
        self.MenuFlushAll()
        self.MenuSubBegin(c4d.plugins.GeLoadString(ids.MENU_PRESET))
        self.MenuAddString(ids.MENU_PRESET_LOAD, c4d.plugins.GeLoadString(ids.MENU_PRESET_LOAD))
        self.MenuAddString(ids.MENU_PRESET_SAVE, c4d.plugins.GeLoadString(ids.MENU_PRESET_SAVE))
        self.MenuSubEnd()
        self.MenuSubBegin(c4d.plugins.GeLoadString(ids.MENU_ABOUT))
        self.MenuAddString(ids.MENU_ABOUT_HELP, c4d.plugins.GeLoadString(ids.MENU_ABOUT_HELP))
        self.MenuAddString(ids.MENU_ABOUT_ABOUT, c4d.plugins.GeLoadString(ids.MENU_ABOUT_ABOUT))
        self.MenuSubEnd()
        self.MenuFinished()

        icon2 = c4d.bitmaps.BaseBitmap()
        icon2.InitWith(os.path.join(os.path.dirname(__file__), "res", "pic.jpg"))    
        bc = c4d.BaseContainer()                         
        bc.SetLong(c4d.BITMAPBUTTON_ICONID1, 1390382) 
        bc.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        self.myBitButton=self.AddCustomGui(1390382, c4d.CUSTOMGUI_BITMAPBUTTON, "Bend", c4d.BFH_CENTER | c4d.BFV_CENTER, 32, 32, bc)
        self.myBitButton = c4d.gui.BitmapButtonCustomGui 
        dialogLoadet=self.LoadDialogResource(ids.MAINDIALOG, None, flags= c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT )  
        self.AttachUserArea(self.userarea,
                            ids.MAINDIALOG_USERAREA,
                            c4d.USERAREA_COREMESSAGE)
        self.updateCanvas()
        if dialogLoadet==True:
            self.InitValues()     
            return True

    def InitValues(self): 
        
        self.awdExporterData = c4d.plugins.GetWorldPluginData(ids.PLUGINID)
        if self.awdExporterData:

            if self.awdExporterData[SCALE_DATA]:
                self.scale = self.awdExporterData[SCALE_DATA]
            if self.awdExporterData[UNUSEDMATERIALS_DATA]:
                self.unusedMats = self.awdExporterData[UNUSEDMATERIALS_DATA]
            if self.awdExporterData[SELECTEDONLY_DATA]:
                self.selectedOnly = self.awdExporterData[SELECTEDONLY_DATA]
            if self.awdExporterData[STREAMING_DATA]:
                self.streaming = self.awdExporterData[STREAMING_DATA]
            if self.awdExporterData[COMPRESSDATA_DATA]:
                self.compressData = self.awdExporterData[COMPRESSDATA_DATA]
            if self.awdExporterData[DEBUG_DATA]:
                self.debug = self.awdExporterData[DEBUG_DATA]
            if self.awdExporterData[CLOSE_DATA]:
                self.closeAfter = self.awdExporterData[CLOSE_DATA]

            if self.awdExporterData[TEXTURES_DATA]:
                self.textures = self.awdExporterData[TEXTURES_DATA]
            if self.awdExporterData[COPYTEXTURES_DATA]:
                self.copyTextures = self.awdExporterData[COPYTEXTURES_DATA]
            if self.awdExporterData[TEXTURESURL_DATA]:
                self.texturesURL = self.awdExporterData[TEXTURESURL_DATA]

            if self.awdExporterData[ANIMATION_DATA]:
                self.animationBool = self.awdExporterData[ANIMATION_DATA]
            if self.awdExporterData[RANGE_DATA]:
                self.animationRange = self.awdExporterData[RANGE_DATA]
            if self.awdExporterData[FIRSTFRAME_DATA]:
                self.firstFrame = self.awdExporterData[FIRSTFRAME_DATA]
            if self.awdExporterData[LASTFRAME_DATA]:
                self.lastFrame = self.awdExporterData[LASTFRAME_DATA]
        else:
            self.awdExporterData = c4d.BaseContainer()
        self.setUI()
        return True   

    def CoreMessage(self, msg, result):
        self.updateCanvas()
        return True

    def savePreset(self):
        datei=c4d.storage.SaveDialog(c4d.FILESELECTTYPE_ANYTHING, "save Preset", "set")
        output_xml = dom.Document()
        preset_xml=dom.Element("AWDExporterPreset")
        preset_xml.setAttribute("scale",str(self.scale))
        preset_xml.setAttribute("unusedMats",str(self.unusedMats))
        preset_xml.setAttribute("selectedOnly",str(self.selectedOnly))
        preset_xml.setAttribute("streaming",str(self.streaming))
        preset_xml.setAttribute("compressData",str(self.compressData))
        preset_xml.setAttribute("debug",str(self.debug))
        preset_xml.setAttribute("closeAfter",str(self.closeAfter))
        preset_xml.setAttribute("textures",str(self.textures))
        preset_xml.setAttribute("copyTextures",str(self.copyTextures))
        preset_xml.setAttribute("texturesURL",str(self.texturesURL))
        preset_xml.setAttribute("animationBool",str(self.animationBool))
        preset_xml.setAttribute("animationRange",str(self.animationRange))
        preset_xml.setAttribute("firstFrame",str(self.firstFrame))
        preset_xml.setAttribute("lastFrame",str(self.lastFrame))
        output_xml.appendChild(preset_xml)

        if datei!=None:    
            str_object_xml=output_xml.toprettyxml()  
            f = open(datei, 'wb')
            f.write(str_object_xml)
            f.close()
        return True

    def loadPreset(self):

        datei=c4d.storage.LoadDialog(c4d.FILESELECTTYPE_ANYTHING, "open Preset", c4d.FILESELECT_LOAD,"set")  
        if datei!=None:               
         
            dom1 = dom.parse(datei) 
            if dom1.firstChild.getAttribute("scale"):
                self.scale=float(dom1.firstChild.getAttribute("scale"))
            if dom1.firstChild.getAttribute("unusedMats")=="True":
                self.unusedMats=True
            if dom1.firstChild.getAttribute("selectedOnly")=="True":
                self.selectedOnly=True
            if dom1.firstChild.getAttribute("streaming")=="True":
                self.streaming=True
            if dom1.firstChild.getAttribute("compressData")=="True":
                self.compressData=True
            if dom1.firstChild.getAttribute("debug")=="True":
                self.debug=True
            if dom1.firstChild.getAttribute("closeAfter")=="True":
                self.closeAfter=True
            if dom1.firstChild.getAttribute("textures"):
                self.textures=int(dom1.firstChild.getAttribute("textures"))
            if dom1.firstChild.getAttribute("copyTextures")=="True":
                self.copyTextures=True
            if dom1.firstChild.getAttribute("texturesURL"):
                self.texturesURL=dom1.firstChild.getAttribute("texturesURL")
            if dom1.firstChild.getAttribute("animationBool")=="True":
                self.animationBool=True
            if dom1.firstChild.getAttribute("animationRange"):
                self.animationRange=int(dom1.firstChild.getAttribute("animationRange"))
            if dom1.firstChild.getAttribute("firstFrame"):
                self.firstFrame=float(dom1.firstChild.getAttribute("firstFrame"))
            if dom1.firstChild.getAttribute("lastFrame"):
                self.lastFrame=float(dom1.firstChild.getAttribute("lastFrame"))


        self.setUI()
        return True


    def setUI(self):

        self.SetReal(ids.REAL_SCALE, self.scale, -99999999, 99999999, 1.0, c4d.FORMAT_LONG)
        self.SetBool(ids.CBOX_UNUSEDMATS, self.unusedMats)
        self.SetBool(ids.CBOX_SELECTEDONLY, self.selectedOnly)
        self.SetBool(ids.CBOX_STREAMING, self.streaming)
        self.SetBool(ids.CBOX_COMPRESSED, self.compressData)
        self.SetBool(ids.CBOX_DEBUG, self.debug)
        self.SetBool(ids.CBOX_CLOSEAFTEREXPORT, self.closeAfter)

        self.SetLong(ids.COMBO_TEXTURESMODE, self.textures)
        self.SetBool(ids.CBOX_COPYTEX, self.copyTextures)
        self.SetString(ids.LINK_EXTERNTEXTURESPATH, self.texturesURL)
        self.SetBool(ids.CBOX_ANIMATION, self.animationBool)

        self.SetLong(ids.COMBO_RANGE, self.animationRange)

        self.Enable(ids.REAL_FIRSTFRAME, False)
        self.Enable(ids.REAL_FIRSTFRAME_STR, False)
        self.Enable(ids.REAL_LASTFRAME, False)
        self.Enable(ids.REAL_LASTFRAME_STR, False)
        self.Enable(ids.COMBO_RANGE, False)
        self.Enable(ids.COMBO_RANGE_STR, False)
        self.Enable(ids.LINK_EXTERNTEXTURESPATH_STR, False)
        self.Enable(ids.LINK_EXTERNTEXTURESPATH, False)
        self.Enable(ids.CBOX_COPYTEX, False)

        if self.GetBool(ids.CBOX_COMPRESSED)==True and self.GetBool(ids.CBOX_STREAMING)==True:
            self.SetBool(ids.CBOX_STREAMING,False)
            self.streaming=False

        if self.GetLong(ids.COMBO_TEXTURESMODE)==1:
            self.Enable(ids.LINK_EXTERNTEXTURESPATH_STR, True)
            self.Enable(ids.LINK_EXTERNTEXTURESPATH, True)
            self.Enable(ids.CBOX_COPYTEX, True)

        doc=c4d.documents.GetActiveDocument()
        print self.GetBool(ids.CBOX_ANIMATION)
        if self.GetBool(ids.CBOX_ANIMATION)==True:
            self.Enable(ids.COMBO_RANGE, True)
            self.Enable(ids.COMBO_RANGE_STR, True)
            self.Enable(ids.REAL_LASTFRAME_STR, True)
            self.Enable(ids.REAL_FIRSTFRAME_STR, True)
            if self.GetLong(ids.COMBO_RANGE)==0:
                self.SetReal(ids.REAL_FIRSTFRAME,doc.GetMinTime().GetFrame(doc.GetFps()), doc.GetMinTime().GetFrame(doc.GetFps()), doc.GetMinTime().GetFrame(doc.GetFps()), 1.0, c4d.FORMAT_LONG)
                self.SetReal(ids.REAL_LASTFRAME,doc.GetMaxTime().GetFrame(doc.GetFps()),doc.GetMaxTime().GetFrame(doc.GetFps()), doc.GetMaxTime().GetFrame(doc.GetFps()), 1.0, c4d.FORMAT_LONG)
            if self.GetLong(ids.COMBO_RANGE)==1:
                self.SetReal(ids.REAL_FIRSTFRAME,doc.GetLoopMinTime().GetFrame(doc.GetFps()), doc.GetLoopMinTime().GetFrame(doc.GetFps()), doc.GetLoopMinTime().GetFrame(doc.GetFps()), 1.0, c4d.FORMAT_LONG)
                self.SetReal(ids.REAL_LASTFRAME,doc.GetLoopMaxTime().GetFrame(doc.GetFps()), doc.GetLoopMaxTime().GetFrame(doc.GetFps()), doc.GetLoopMaxTime().GetFrame(doc.GetFps()), 1.0, c4d.FORMAT_LONG)
            if self.GetLong(ids.COMBO_RANGE)==2:
                self.SetReal(ids.REAL_FIRSTFRAME,self.firstFrame, doc.GetMinTime().GetFrame(doc.GetFps()), doc.GetMaxTime().GetFrame(doc.GetFps()), 1.0, c4d.FORMAT_LONG)
                self.SetReal(ids.REAL_LASTFRAME,self.lastFrame, doc.GetMinTime().GetFrame(doc.GetFps()), doc.GetMaxTime().GetFrame(doc.GetFps()), 1.0, c4d.FORMAT_LONG)
                self.Enable(ids.REAL_FIRSTFRAME, True)
                self.Enable(ids.REAL_LASTFRAME, True)
                
                

        return True
    
    
    def setValues(self):

        self.scale=self.GetReal(ids.REAL_SCALE)
        self.awdExporterData.SetReal(SCALE_DATA, self.scale)
        self.unusedMats=self.GetBool(ids.CBOX_UNUSEDMATS)
        self.awdExporterData.SetBool(UNUSEDMATERIALS_DATA, self.unusedMats)
        self.selectedOnly=self.GetBool(ids.CBOX_SELECTEDONLY)
        self.awdExporterData.SetBool(SELECTEDONLY_DATA, self.selectedOnly)
        self.streaming=self.GetBool(ids.CBOX_STREAMING)
        self.awdExporterData.SetBool(STREAMING_DATA, self.streaming)
        self.compressData=self.GetBool(ids.CBOX_COMPRESSED)
        self.awdExporterData.SetBool(COMPRESSDATA_DATA, self.compressData)
        self.debug=self.GetBool(ids.CBOX_DEBUG)
        self.awdExporterData.SetBool(DEBUG_DATA, self.debug)
        self.closeAfter=self.GetBool(ids.CBOX_CLOSEAFTEREXPORT)
        self.awdExporterData.SetBool(CLOSE_DATA, self.closeAfter)
        self.textures=self.GetLong(ids.COMBO_TEXTURESMODE)
        self.awdExporterData.SetLong(TEXTURES_DATA, self.textures)
        self.copyTextures=self.GetBool(ids.CBOX_COPYTEX)
        self.awdExporterData.SetBool(COPYTEXTURES_DATA, self.copyTextures)
        self.texturesURL=self.GetString(ids.LINK_EXTERNTEXTURESPATH)
        self.awdExporterData.SetString(TEXTURESURL_DATA, self.texturesURL)
        self.animationBool=self.GetBool(ids.CBOX_ANIMATION)
        self.awdExporterData.SetBool(ANIMATION_DATA, self.animationBool)
        self.animationRange=self.GetLong(ids.COMBO_RANGE)
        self.awdExporterData.SetLong(RANGE_DATA, self.animationRange)        

        if self.GetLong(ids.COMBO_RANGE)==2:
            self.firstFrame=self.GetReal(ids.REAL_FIRSTFRAME)
            self.lastFrame=self.GetReal(ids.REAL_LASTFRAME)
            self.awdExporterData.SetReal(FIRSTFRAME_DATA, self.firstFrame)
            self.awdExporterData.SetReal(LASTFRAME_DATA, self.lastFrame)  

        c4d.plugins.SetWorldPluginData(ids.PLUGINID, self.awdExporterData)  
	

		
		
    def updateCanvas(self):
        global exportData
        doc=c4d.documents.GetActiveDocument()
        if doc==None:
            statusStr=c4d.plugins.GeLoadString(ids.STATUSMESSAGE)+c4d.plugins.GeLoadString(ids.STATUSMESSAGE1)
            self.userarea.draw([statusStr,0,0])
            return
        if doc!=None:
            if doc.GetDocumentPath()==None or doc.GetDocumentPath()=="":
                statusStr=c4d.plugins.GeLoadString(ids.STATUSMESSAGE)+c4d.plugins.GeLoadString(ids.STATUSMESSAGE1)
                self.userarea.draw([statusStr,0,0])
                return
            if exportData==None:
                statusStr=c4d.plugins.GeLoadString(ids.STATUSMESSAGE)+c4d.plugins.GeLoadString(ids.STATUSMESSAGE2)
                self.userarea.draw([statusStr,0,0])
                return
            if exportData.status==0:
                statusStr=c4d.plugins.GeLoadString(ids.STATUSMESSAGE)+c4d.plugins.GeLoadString(ids.STATUSMESSAGE3)
                self.userarea.draw([statusStr,0,0])
                return
            curPercent=float(float(exportData.allStatus)/float(exportData.allStatusLength))
            c4d.StatusSetBar(curPercent)
            if exportData.status==1:
                statusStr=c4d.plugins.GeLoadString(ids.STATUSMESSAGE)+c4d.plugins.GeLoadString(ids.STATUSMESSAGE4)+"  "+str(int(curPercent*100))+" %"
                self.userarea.draw([statusStr,curPercent,0])                   
                return
            if exportData.status==2:
                statusStr=c4d.plugins.GeLoadString(ids.STATUSMESSAGE)+c4d.plugins.GeLoadString(ids.STATUSMESSAGE5)+"  "+str(int(curPercent*100))+" %"
                self.userarea.draw([statusStr,curPercent,float(exportData.subStatus)])
                return
            if exportData.status==3:
                statusStr=c4d.plugins.GeLoadString(ids.STATUSMESSAGE)+c4d.plugins.GeLoadString(ids.STATUSMESSAGE6)+"  "+str(int(curPercent*100))+" %"
                self.userarea.draw([statusStr,curPercent,0])
                return
            
    def enableAll(self, enableBool):
        self.Enable(ids.CBOX_SELECTEDONLY, enableBool)
        self.Enable(ids.CBOX_UNUSEDMATS, enableBool)
        self.Enable(ids.CBOX_CLOSEAFTEREXPORT, enableBool)
        self.Enable(ids.CBOX_COMPRESSED, enableBool)
        self.Enable(ids.CBOX_ANIMATION, enableBool)
        self.Enable(ids.CBOX_OBJECTCOLORS, enableBool)
        self.Enable(ids.BTN_EXPORT, enableBool)
        
        if enableBool==False:
            self.Enable(ids.BTN_CANCEL, True)
        self.Enable(ids.CBOX_EXPORTMATERIALS, enableBool)
        self.Enable(ids.CBOX_STREAMING, enableBool)
        self.Enable(ids.CBOX_DEBUG, enableBool)
        self.Enable(ids.CBOX_COPYTEX, enableBool)
        self.Enable(ids.COMBO_TEXTURESMODE, enableBool)
        self.Enable(ids.COMBO_TEXTURESMODE_STR, enableBool)
        self.Enable(ids.COMBO_RANGE, enableBool)
        self.Enable(ids.COMBO_RANGE_STR, enableBool)
        self.Enable(ids.LINK_EXTERNTEXTURESPATH, enableBool)
        self.Enable(ids.LINK_EXTERNTEXTURESPATH_STR, enableBool)
        self.Enable(ids.REAL_SCALE, enableBool)
        self.Enable(ids.REAL_FIRSTFRAME, enableBool)
        self.Enable(ids.REAL_LASTFRAME, enableBool)
        self.Enable(ids.REAL_SCALE_STR, enableBool)
        self.Enable(ids.REAL_FIRSTFRAME_STR, enableBool)
        self.Enable(ids.REAL_LASTFRAME_STR, enableBool)
        if enableBool==True:
            self.Enable(ids.BTN_CANCEL, False)
            self.setUI()
      

            
    def Timer(self, msg):
        global exportData
        doc=c4d.documents.GetActiveDocument()
        op=doc.GetActiveObject()
        if workerThread.IsRunning():
            self.updateCanvas()
            pass
        if not workerThread.IsRunning():            
            awdMeshReader.deleteCopiedMeshes(exportData.allMeshObjects)
            if len(exportData.AWDerrorObjects)>0:  
                newMessage=c4d.plugins.GeLoadString(ids.ERRORMESSAGE)+"\n"
                for errorMessage in exportData.AWDerrorObjects:
                    newMessage+=c4d.plugins.GeLoadString(errorMessage.errorID)
                    if errorMessage.errorData!=None:
                        newMessage+="\n\n"+str(c4d.plugins.GeLoadString(ids.ERRORMESSAGEOBJ))+" = "+str(errorMessage.errorData)
                c4d.gui.MessageDialog(newMessage)
                if self.GetBool(ids.CBOX_CLOSEAFTEREXPORT) == True:  
                    exportData=None
                    c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
                    c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
                    c4d.EventAdd(c4d.EVENT_ANIMATE) 
                    self.Close()
                    return True  
                exportData=None
                c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
                c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
                c4d.EventAdd(c4d.EVENT_ANIMATE) 
                return True  
            if len(exportData.AWDwarningObjects)>0:  
                newMessage=c4d.plugins.GeLoadString(ids.WARNINGMESSAGE)+"\n"
                for errorMessage in exportData.AWDwarningObjects:
                    newMessage+=c4d.plugins.GeLoadString(errorMessage.errorID)
                    if errorMessage.errorData!=None:
                        newMessage+="AWDWarningObject: "+str(errorMessage.errorData)
                print "Warning "+str(newMessage)
                if self.GetBool(ids.CBOX_CLOSEAFTEREXPORT) == True:  
                    exportData=None
                    c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
                    c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
                    c4d.EventAdd(c4d.EVENT_ANIMATE) 
                    self.Close()    
                    return True  
            if self.GetBool(ids.CBOX_CLOSEAFTEREXPORT) == True and exportData.cancel!=True:  
                exportData=None
                c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
                c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
                c4d.EventAdd(c4d.EVENT_ANIMATE) 
                self.Close()
                return True  
            exportData=None
            c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
            c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
            c4d.EventAdd(c4d.EVENT_ANIMATE) 
            self.enableAll(True)
            self.SetTimer(0)
    def Command(self, id, msg):  
        global workerThread,exportData
             
        self.updateCanvas()

        if id == ids.BTN_CANCEL:
            workerThread.End()
            self.SetTimer(0)
            exportData=None
            self.updateCanvas()
            self.enableAll(True)
            return True
        if id == ids.BTN_EXPORT:
            doc=c4d.documents.GetActiveDocument()
            if doc==None:
                newMessage=c4d.plugins.GeLoadString(ids.STATUSMESSAGE1)
                c4d.gui.MessageDialog(newMessage)
                return True
            if doc.GetDocumentPath()==None or doc.GetDocumentPath()=="":
                newMessage=c4d.plugins.GeLoadString(ids.STATUSMESSAGE1)
                c4d.gui.MessageDialog(newMessage)
                return True
            self.enableAll(False)
        
            doc=c4d.documents.GetActiveDocument()
            exportData=awdMainClass.mainScene(doc.GetDocumentName(),self,doc.GetFps())#empty list to collect the objects that should be exportet

            worker.export(exportData) 
            exportData.allStatusLength=2+(10*int(exportData.animationCounter))+(10*len(exportData.allMeshObjects))
            exportData.allStatus=1
            exportData.status=1
            self.updateCanvas()
            awdSkinningReader.createSkeletonBlocks(exportData.objList,exportData,self) 
            exportData.status=2  
            self.updateCanvas()
            if len(exportData.AWDerrorObjects)>0:  
                self.enableAll(True)
                newMessage=c4d.plugins.GeLoadString(ids.ERRORMESSAGE)+"\n"
                for errorMessage in exportData.AWDerrorObjects:
                    newMessage+=c4d.plugins.GeLoadString(errorMessage.errorID)
                    if errorMessage.errorData!=None:
                        newMessage+="\n\n"+str(c4d.plugins.GeLoadString(ids.ERRORMESSAGEOBJ))+" = "+str(errorMessage.errorData)
                c4d.gui.MessageDialog(newMessage)
                exportData=None
                if self.GetBool(ids.CBOX_CLOSEAFTEREXPORT) == True:  
                    exportData=None
                    c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
                    c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
                    c4d.EventAdd(c4d.EVENT_ANIMATE) 
                    self.Close()
                    return True  
                c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
                c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
                c4d.EventAdd(c4d.EVENT_ANIMATE) 
                return True               
            workerThread  = MyThread()
            workerThread.Start()
            self.SetTimer(20)
              
        if id == ids.CBOX_ANIMATION: 
            self.animationBool=self.GetBool(ids.CBOX_ANIMATION)
            self.setValues()  
            self.setUI()
        if id == ids.LINK_EXTERNTEXTURESPATH: 
            self.texturesURL=self.GetString(ids.LINK_EXTERNTEXTURESPATH)
            self.setValues()
        if id == ids.CBOX_STREAMING: 
            self.streaming=self.GetBool(ids.CBOX_STREAMING)
            if self.streaming==True:
                self.SetBool(ids.CBOX_COMPRESSED,False)
                self.compressData=False
        if id == ids.CBOX_COMPRESSED: 
            self.streaming=self.GetBool(ids.CBOX_COMPRESSED)
            if self.compressData==True:
                self.SetBool(ids.CBOX_STREAMING,False)
                self.streaming=False
        if id == ids.COMBO_RANGE: 
            self.animationRange=self.GetLong(ids.COMBO_RANGE)
            self.setUI()
        if id == ids.COMBO_TEXTURESMODE: 
            self.setValues()   
            self.setUI()
           
        if id == ids.MENU_PRESET_LOAD:   
            exportResult=self.loadPreset()  
        self.setValues()     
        if id == ids.MENU_PRESET_SAVE:   
            exportResult=self.savePreset() 
              
        #self.setUI()     
        return True  
    
    """
    # called on 'Close()'
    def AskClose(self):
        
        return not c4d.gui.QuestionDialog(c4d.plugins.GeLoadString(ids.STR_ASKCLOSE))
    """       