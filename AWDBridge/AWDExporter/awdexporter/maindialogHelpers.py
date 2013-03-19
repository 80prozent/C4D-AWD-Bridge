
# some classes tio help with the dialog management 

import c4d
from awdexporter import ids    


def InitValues(mainDialog): 
        
    mainDialog.awdExporterData = c4d.plugins.GetWorldPluginData(ids.PLUGINID)
    if mainDialog.awdExporterData:

        if mainDialog.awdExporterData[ids.REAL_SCALE]:
            mainDialog.scale = mainDialog.awdExporterData[ids.REAL_SCALE]
        if mainDialog.awdExporterData[ids.CBOX_UNUSEDMATS]:
            mainDialog.unusedMats = mainDialog.awdExporterData[ids.CBOX_UNUSEDMATS]
        if mainDialog.awdExporterData[ids.CBOX_STREAMING]:
            mainDialog.streaming = mainDialog.awdExporterData[ids.CBOX_STREAMING]
        if mainDialog.awdExporterData[ids.CBOX_COMPRESSED]:
            mainDialog.compressData = mainDialog.awdExporterData[ids.CBOX_COMPRESSED]
        if mainDialog.awdExporterData[ids.CBOX_DEBUG]:
            mainDialog.debug = mainDialog.awdExporterData[ids.CBOX_DEBUG]
        if mainDialog.awdExporterData[ids.CBOX_CLOSEAFTEREXPORT]:
            mainDialog.closeAfter = mainDialog.awdExporterData[ids.CBOX_CLOSEAFTEREXPORT]
        if mainDialog.awdExporterData[ids.COMBO_TEXTURESMODE  ]:
            mainDialog.textures = mainDialog.awdExporterData[ids.COMBO_TEXTURESMODE]
        if mainDialog.awdExporterData[ids.CBOX_ANIMATION]:
            mainDialog.animationBool = mainDialog.awdExporterData[ids.CBOX_ANIMATION]
        if mainDialog.awdExporterData[ids.COMBO_RANGE]:
            mainDialog.animationRange = mainDialog.awdExporterData[ids.COMBO_RANGE]
        if mainDialog.awdExporterData[ids.REAL_FIRSTFRAME]:
            mainDialog.firstFrameUser = mainDialog.awdExporterData[ids.REAL_FIRSTFRAME]
        if mainDialog.awdExporterData[ids.REAL_LASTFRAME]:
            mainDialog.lastFrameUser = mainDialog.awdExporterData[ids.REAL_LASTFRAME]
        if mainDialog.awdExporterData[ids.CBOX_OPENPREFAB]:
            mainDialog.openInPreFab = mainDialog.awdExporterData[ids.CBOX_OPENPREFAB]
    else:
        mainDialog.awdExporterData = c4d.BaseContainer()
    setUI(mainDialog)
    return True   

def setUI(mainDialog):
    mainDialog.SetReal(ids.REAL_SCALE, mainDialog.scale, 0.001, 99999999, 1.0, c4d.FORMAT_REAL)
    mainDialog.SetBool(ids.CBOX_UNUSEDMATS, mainDialog.unusedMats)
    mainDialog.SetBool(ids.CBOX_STREAMING, mainDialog.streaming)
    mainDialog.SetBool(ids.CBOX_COMPRESSED, mainDialog.compressData)
    mainDialog.SetBool(ids.CBOX_DEBUG, mainDialog.debug)
    mainDialog.SetBool(ids.CBOX_CLOSEAFTEREXPORT, mainDialog.closeAfter)
    mainDialog.SetBool(ids.CBOX_OPENPREFAB, mainDialog.openInPreFab)
    mainDialog.SetBool(ids.CBOX_ANIMATION, mainDialog.animationBool)

    mainDialog.SetLong(ids.COMBO_TEXTURESMODE, mainDialog.textures)
    mainDialog.SetLong(ids.COMBO_RANGE, mainDialog.animationRange)

    mainDialog.Enable(ids.REAL_FIRSTFRAME, False)
    mainDialog.Enable(ids.REAL_FIRSTFRAME_STR, False)
    mainDialog.Enable(ids.REAL_LASTFRAME, False)
    mainDialog.Enable(ids.REAL_LASTFRAME_STR, False)
    mainDialog.Enable(ids.COMBO_RANGE, False)
    mainDialog.Enable(ids.COMBO_RANGE_STR, False)

    if mainDialog.GetBool(ids.CBOX_COMPRESSED)==True and mainDialog.GetBool(ids.CBOX_STREAMING)==True:
        mainDialog.SetBool(ids.CBOX_STREAMING,False)
        mainDialog.streaming=False


    doc=c4d.documents.GetActiveDocument()
    #print mainDialog.GetBool(ids.CBOX_ANIMATION)
    if mainDialog.GetBool(ids.CBOX_ANIMATION)==True:
        mainDialog.Enable(ids.COMBO_RANGE, True)
        mainDialog.Enable(ids.COMBO_RANGE_STR, True)
        mainDialog.Enable(ids.REAL_LASTFRAME_STR, True)
        mainDialog.Enable(ids.REAL_FIRSTFRAME_STR, True)
        if mainDialog.GetLong(ids.COMBO_RANGE)==0:
            mainDialog.SetReal(ids.REAL_FIRSTFRAME,doc.GetMinTime().GetFrame(doc.GetFps()), doc.GetMinTime().GetFrame(doc.GetFps()), doc.GetMinTime().GetFrame(doc.GetFps()), 1.0, c4d.FORMAT_LONG)
            mainDialog.SetReal(ids.REAL_LASTFRAME,doc.GetMaxTime().GetFrame(doc.GetFps()),doc.GetMaxTime().GetFrame(doc.GetFps()), doc.GetMaxTime().GetFrame(doc.GetFps()), 1.0, c4d.FORMAT_LONG)
        if mainDialog.GetLong(ids.COMBO_RANGE)==1:
            mainDialog.SetReal(ids.REAL_FIRSTFRAME,doc.GetLoopMinTime().GetFrame(doc.GetFps()), doc.GetLoopMinTime().GetFrame(doc.GetFps()), doc.GetLoopMinTime().GetFrame(doc.GetFps()), 1.0, c4d.FORMAT_LONG)
            mainDialog.SetReal(ids.REAL_LASTFRAME,doc.GetLoopMaxTime().GetFrame(doc.GetFps()), doc.GetLoopMaxTime().GetFrame(doc.GetFps()), doc.GetLoopMaxTime().GetFrame(doc.GetFps()), 1.0, c4d.FORMAT_LONG)
        if mainDialog.GetLong(ids.COMBO_RANGE)==2:
            mainDialog.SetReal(ids.REAL_FIRSTFRAME,mainDialog.firstFrameUser, doc.GetMinTime().GetFrame(doc.GetFps()), doc.GetMaxTime().GetFrame(doc.GetFps()), 1.0, c4d.FORMAT_LONG)
            mainDialog.SetReal(ids.REAL_LASTFRAME,mainDialog.lastFrameUser, doc.GetMinTime().GetFrame(doc.GetFps()), doc.GetMaxTime().GetFrame(doc.GetFps()), 1.0, c4d.FORMAT_LONG)
            mainDialog.Enable(ids.REAL_FIRSTFRAME, True)
            mainDialog.Enable(ids.REAL_LASTFRAME, True)
    return True
    
    
def setValues(mainDialog):
    mainDialog.scale=mainDialog.GetReal(ids.REAL_SCALE)
    mainDialog.awdExporterData.SetReal(ids.REAL_SCALE, mainDialog.scale)
    mainDialog.openInPreFab=mainDialog.GetBool(ids.CBOX_OPENPREFAB)
    mainDialog.awdExporterData.SetBool(ids.CBOX_OPENPREFAB, mainDialog.openInPreFab)
    mainDialog.unusedMats=mainDialog.GetBool(ids.CBOX_UNUSEDMATS)
    mainDialog.awdExporterData.SetBool(ids.CBOX_UNUSEDMATS, mainDialog.unusedMats)
    mainDialog.streaming=mainDialog.GetBool(ids.CBOX_STREAMING)
    mainDialog.awdExporterData.SetBool(ids.CBOX_STREAMING, mainDialog.streaming)
    mainDialog.compressData=mainDialog.GetBool(ids.CBOX_COMPRESSED)
    mainDialog.awdExporterData.SetBool(ids.CBOX_COMPRESSED, mainDialog.compressData)
    mainDialog.debug=mainDialog.GetBool(ids.CBOX_DEBUG)
    mainDialog.awdExporterData.SetBool(ids.CBOX_DEBUG, mainDialog.debug)
    mainDialog.closeAfter=mainDialog.GetBool(ids.CBOX_CLOSEAFTEREXPORT)
    mainDialog.awdExporterData.SetBool(ids.CBOX_CLOSEAFTEREXPORT, mainDialog.closeAfter)
    mainDialog.textures=mainDialog.GetLong(ids.COMBO_TEXTURESMODE)
    mainDialog.awdExporterData.SetLong(ids.COMBO_TEXTURESMODE  , mainDialog.textures)
    mainDialog.animationBool=mainDialog.GetBool(ids.CBOX_ANIMATION)
    mainDialog.awdExporterData.SetBool(ids.CBOX_ANIMATION, mainDialog.animationBool)
    mainDialog.animationRange=mainDialog.GetLong(ids.COMBO_RANGE)
    mainDialog.awdExporterData.SetLong(ids.COMBO_RANGE, mainDialog.animationRange)        

    if mainDialog.GetLong(ids.COMBO_RANGE)==2:
        mainDialog.firstFrameUser=mainDialog.GetReal(ids.REAL_FIRSTFRAME)
        mainDialog.lastFrameUser=mainDialog.GetReal(ids.REAL_LASTFRAME)
        mainDialog.awdExporterData.SetReal(ids.REAL_FIRSTFRAME, mainDialog.firstFrameUser)
        mainDialog.awdExporterData.SetReal(ids.REAL_LASTFRAME, mainDialog.lastFrameUser)  

    c4d.plugins.SetWorldPluginData(ids.PLUGINID, mainDialog.awdExporterData)  

def enableAll(mainDialog, enableBool):
    mainDialog.Enable(ids.CBOX_UNUSEDMATS, enableBool)
    mainDialog.Enable(ids.CBOX_CLOSEAFTEREXPORT, enableBool)
    mainDialog.Enable(ids.CBOX_COMPRESSED, enableBool)
    mainDialog.Enable(ids.CBOX_ANIMATION, enableBool)
    mainDialog.Enable(ids.BTN_EXPORT, enableBool)
    mainDialog.Enable(ids.CBOX_OPENPREFAB, enableBool)       
        
    mainDialog.Enable(ids.CBOX_UNUSEDMATS, enableBool)
    mainDialog.Enable(ids.CBOX_STREAMING, enableBool)
    mainDialog.Enable(ids.CBOX_DEBUG, enableBool)
    mainDialog.Enable(ids.COMBO_TEXTURESMODE, enableBool)
    mainDialog.Enable(ids.COMBO_TEXTURESMODE_STR, enableBool)
    mainDialog.Enable(ids.COMBO_RANGE, enableBool)
    mainDialog.Enable(ids.COMBO_RANGE_STR, enableBool)
    mainDialog.Enable(ids.REAL_SCALE, enableBool)
    mainDialog.Enable(ids.REAL_FIRSTFRAME, enableBool)
    mainDialog.Enable(ids.REAL_LASTFRAME, enableBool)
    mainDialog.Enable(ids.REAL_SCALE_STR, enableBool)
    mainDialog.Enable(ids.REAL_FIRSTFRAME_STR, enableBool)
    mainDialog.Enable(ids.REAL_LASTFRAME_STR, enableBool)
    if enableBool==True:
        mainDialog.Enable(ids.BTN_CANCEL, False)
    if enableBool==True:
        mainDialog.Enable(ids.BTN_CANCEL, False)
        setUI(mainDialog)
