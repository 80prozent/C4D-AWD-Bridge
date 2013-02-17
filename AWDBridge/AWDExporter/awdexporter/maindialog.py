import c4d
import os
from awdexporter import ids
from awdexporter import workerExporter
from awdexporter import mainHelpers   
from awdexporter import classCanvas
from awdexporter import mainExporter

from awdexporter import maindialogPresets
from awdexporter import maindialogHelpers

workerThread=None
exportData=None
enableObjects=[]
enableStates=[]

class WorkerThread(c4d.threading.C4DThread):    
    def Main(self):
        global exportData
        doc=c4d.documents.GetActiveDocument()
        workerExporter.startWorkerExport(exportData,self)                
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
        self.userarea = classCanvas.Canvas()
        
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
            maindialogHelpers.InitValues(self)     
            return True

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
    def CoreMessage(self, msg, result):
        self.updateCanvas()
        return True


            
    def Timer(self, msg):
        global exportData
        doc=c4d.documents.GetActiveDocument()
        op=doc.GetActiveObject()
        if workerThread.IsRunning():
            self.updateCanvas()
            pass
        if not workerThread.IsRunning():         
            mainHelpers.deleteCopiedMeshes(exportData.allMeshObjects)
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
            maindialogHelpers.enableAll(self,True)
            print c4d.plugins.GeLoadString(ids.SUCCESSMESSAGE)
            self.SetTimer(0)
       
    def printErrors(self):  
        global exportData
        if len(exportData.AWDerrorObjects)>0:  
            maindialogHelpers.enableAll(self,True)
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
            c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
            c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
            c4d.EventAdd(c4d.EVENT_ANIMATE)  
            exportData=None  
            return False   
        return True

    def Command(self, id, msg):  
        global workerThread,exportData
             
        self.updateCanvas()

        if id == ids.BTN_CANCEL:
            workerThread.End()
            self.SetTimer(0)
            exportData=None
            self.updateCanvas()
            maindialogHelpers.enableAll(self,True)
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
            exportData=mainExporter.startExport(self) 
            self.printErrors() 
            if exportData!=None:
                workerThread  = WorkerThread()
                workerThread.Start() 
                self.SetTimer(20)
            if exportData==None:
                self.SetTimer(0)  
              
        if id == ids.CBOX_ANIMATION: 
            self.animationBool=self.GetBool(ids.CBOX_ANIMATION)
            maindialogHelpers.setValues(self)  
            maindialogHelpers.setUI(self)
        if id == ids.LINK_EXTERNTEXTURESPATH: 
            self.texturesURL=self.GetString(ids.LINK_EXTERNTEXTURESPATH)
            maindialogHelpers.setValues(self)
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
            maindialogHelpers.setUI(self)
        if id == ids.COMBO_TEXTURESMODE: 
            maindialogHelpers.setValues(self)   
            maindialogHelpers.setUI(self)
           
        if id == ids.MENU_PRESET_LOAD:   
            exportResult=maindialogPresets.loadPreset(self)  
        maindialogHelpers.setValues(self)     
        if id == ids.MENU_PRESET_SAVE:   
            exportResult=maindialogPresets.savePreset(self) 
              
        #self.setUI()     
        return True  
    
    """
    # called on 'Close()'
    def AskClose(self):
        
        return not c4d.gui.QuestionDialog(c4d.plugins.GeLoadString(ids.STR_ASKCLOSE))
    """       