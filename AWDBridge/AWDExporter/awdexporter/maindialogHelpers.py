
# some classes tio help with the dialog management 

import c4d
from awdexporter import ids    


def InitValues(mainDialog): 
        
    mainDialog.awdExporterData = c4d.plugins.GetWorldPluginData(ids.PLUGINID)
    if mainDialog.awdExporterData:

        if mainDialog.awdExporterData[ids.SCALE_DATA]:
            mainDialog.scale = mainDialog.awdExporterData[ids.SCALE_DATA]
        if mainDialog.awdExporterData[ids.UNUSEDMATERIALS_DATA]:
            mainDialog.unusedMats = mainDialog.awdExporterData[ids.UNUSEDMATERIALS_DATA]
        if mainDialog.awdExporterData[ids.SELECTEDONLY_DATA]:
            mainDialog.selectedOnly = mainDialog.awdExporterData[ids.SELECTEDONLY_DATA]
        if mainDialog.awdExporterData[ids.STREAMING_DATA]:
            mainDialog.streaming = mainDialog.awdExporterData[ids.STREAMING_DATA]
        if mainDialog.awdExporterData[ids.COMPRESSDATA_DATA]:
            mainDialog.compressData = mainDialog.awdExporterData[ids.COMPRESSDATA_DATA]
        if mainDialog.awdExporterData[ids.DEBUG_DATA]:
            mainDialog.debug = mainDialog.awdExporterData[ids.DEBUG_DATA]
        if mainDialog.awdExporterData[ids.CLOSE_DATA]:
            mainDialog.closeAfter = mainDialog.awdExporterData[ids.CLOSE_DATA]

        if mainDialog.awdExporterData[ids.TEXTURES_DATA]:
            mainDialog.textures = mainDialog.awdExporterData[ids.TEXTURES_DATA]
        if mainDialog.awdExporterData[ids.COPYTEXTURES_DATA]:
            mainDialog.copyTextures = mainDialog.awdExporterData[ids.COPYTEXTURES_DATA]
        if mainDialog.awdExporterData[ids.TEXTURESURL_DATA]:
            mainDialog.texturesURL = mainDialog.awdExporterData[ids.TEXTURESURL_DATA]

        if mainDialog.awdExporterData[ids.ANIMATION_DATA]:
            mainDialog.animationBool = mainDialog.awdExporterData[ids.ANIMATION_DATA]
        if mainDialog.awdExporterData[ids.RANGE_DATA]:
            mainDialog.animationRange = mainDialog.awdExporterData[ids.RANGE_DATA]
        if mainDialog.awdExporterData[ids.FIRSTFRAME_DATA]:
            mainDialog.firstFrame = mainDialog.awdExporterData[ids.FIRSTFRAME_DATA]
        if mainDialog.awdExporterData[ids.LASTFRAME_DATA]:
            mainDialog.lastFrame = mainDialog.awdExporterData[ids.LASTFRAME_DATA]
    else:
        mainDialog.awdExporterData = c4d.BaseContainer()
    setUI(mainDialog)
    return True   

def setUI(mainDialog):
    mainDialog.SetReal(ids.REAL_SCALE, mainDialog.scale, -99999999, 99999999, 1.0, c4d.FORMAT_LONG)
    mainDialog.SetBool(ids.CBOX_UNUSEDMATS, mainDialog.unusedMats)
    mainDialog.SetBool(ids.CBOX_SELECTEDONLY, mainDialog.selectedOnly)
    mainDialog.SetBool(ids.CBOX_STREAMING, mainDialog.streaming)
    mainDialog.SetBool(ids.CBOX_COMPRESSED, mainDialog.compressData)
    mainDialog.SetBool(ids.CBOX_DEBUG, mainDialog.debug)
    mainDialog.SetBool(ids.CBOX_CLOSEAFTEREXPORT, mainDialog.closeAfter)

    mainDialog.SetLong(ids.COMBO_TEXTURESMODE, mainDialog.textures)
    mainDialog.SetBool(ids.CBOX_COPYTEX, mainDialog.copyTextures)
    mainDialog.SetString(ids.LINK_EXTERNTEXTURESPATH, mainDialog.texturesURL)
    mainDialog.SetBool(ids.CBOX_ANIMATION, mainDialog.animationBool)
    mainDialog.SetLong(ids.COMBO_RANGE, mainDialog.animationRange)

    mainDialog.Enable(ids.REAL_FIRSTFRAME, False)
    mainDialog.Enable(ids.REAL_FIRSTFRAME_STR, False)
    mainDialog.Enable(ids.REAL_LASTFRAME, False)
    mainDialog.Enable(ids.REAL_LASTFRAME_STR, False)
    mainDialog.Enable(ids.COMBO_RANGE, False)
    mainDialog.Enable(ids.COMBO_RANGE_STR, False)
    mainDialog.Enable(ids.LINK_EXTERNTEXTURESPATH_STR, False)
    mainDialog.Enable(ids.LINK_EXTERNTEXTURESPATH, False)
    mainDialog.Enable(ids.CBOX_COPYTEX, False)

    if mainDialog.GetBool(ids.CBOX_COMPRESSED)==True and mainDialog.GetBool(ids.CBOX_STREAMING)==True:
        mainDialog.SetBool(ids.CBOX_STREAMING,False)
        mainDialog.streaming=False

    if mainDialog.GetLong(ids.COMBO_TEXTURESMODE)==1:
        mainDialog.Enable(ids.LINK_EXTERNTEXTURESPATH_STR, True)
        mainDialog.Enable(ids.LINK_EXTERNTEXTURESPATH, True)
        mainDialog.Enable(ids.CBOX_COPYTEX, True)

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
            mainDialog.SetReal(ids.REAL_FIRSTFRAME,mainDialog.firstFrame, doc.GetMinTime().GetFrame(doc.GetFps()), doc.GetMaxTime().GetFrame(doc.GetFps()), 1.0, c4d.FORMAT_LONG)
            mainDialog.SetReal(ids.REAL_LASTFRAME,mainDialog.lastFrame, doc.GetMinTime().GetFrame(doc.GetFps()), doc.GetMaxTime().GetFrame(doc.GetFps()), 1.0, c4d.FORMAT_LONG)
            mainDialog.Enable(ids.REAL_FIRSTFRAME, True)
            mainDialog.Enable(ids.REAL_LASTFRAME, True)
    return True
    
    
def setValues(mainDialog):
    mainDialog.scale=mainDialog.GetReal(ids.REAL_SCALE)
    mainDialog.awdExporterData.SetReal(ids.SCALE_DATA, mainDialog.scale)
    mainDialog.unusedMats=mainDialog.GetBool(ids.CBOX_UNUSEDMATS)
    mainDialog.awdExporterData.SetBool(ids.UNUSEDMATERIALS_DATA, mainDialog.unusedMats)
    mainDialog.selectedOnly=mainDialog.GetBool(ids.CBOX_SELECTEDONLY)
    mainDialog.awdExporterData.SetBool(ids.SELECTEDONLY_DATA, mainDialog.selectedOnly)
    mainDialog.streaming=mainDialog.GetBool(ids.CBOX_STREAMING)
    mainDialog.awdExporterData.SetBool(ids.STREAMING_DATA, mainDialog.streaming)
    mainDialog.compressData=mainDialog.GetBool(ids.CBOX_COMPRESSED)
    mainDialog.awdExporterData.SetBool(ids.COMPRESSDATA_DATA, mainDialog.compressData)
    mainDialog.debug=mainDialog.GetBool(ids.CBOX_DEBUG)
    mainDialog.awdExporterData.SetBool(ids.DEBUG_DATA, mainDialog.debug)
    mainDialog.closeAfter=mainDialog.GetBool(ids.CBOX_CLOSEAFTEREXPORT)
    mainDialog.awdExporterData.SetBool(ids.CLOSE_DATA, mainDialog.closeAfter)
    mainDialog.textures=mainDialog.GetLong(ids.COMBO_TEXTURESMODE)
    mainDialog.awdExporterData.SetLong(ids.TEXTURES_DATA, mainDialog.textures)
    mainDialog.copyTextures=mainDialog.GetBool(ids.CBOX_COPYTEX)
    mainDialog.awdExporterData.SetBool(ids.COPYTEXTURES_DATA, mainDialog.copyTextures)
    mainDialog.texturesURL=mainDialog.GetString(ids.LINK_EXTERNTEXTURESPATH)
    mainDialog.awdExporterData.SetString(ids.TEXTURESURL_DATA, mainDialog.texturesURL)
    mainDialog.animationBool=mainDialog.GetBool(ids.CBOX_ANIMATION)
    mainDialog.awdExporterData.SetBool(ids.ANIMATION_DATA, mainDialog.animationBool)
    mainDialog.animationRange=mainDialog.GetLong(ids.COMBO_RANGE)
    mainDialog.awdExporterData.SetLong(ids.RANGE_DATA, mainDialog.animationRange)        

    if mainDialog.GetLong(ids.COMBO_RANGE)==2:
        mainDialog.firstFrame=mainDialog.GetReal(ids.REAL_FIRSTFRAME)
        mainDialog.lastFrame=mainDialog.GetReal(ids.REAL_LASTFRAME)
        mainDialog.awdExporterData.SetReal(ids.FIRSTFRAME_DATA, mainDialog.firstFrame)
        mainDialog.awdExporterData.SetReal(ids.LASTFRAME_DATA, mainDialog.lastFrame)  

    c4d.plugins.SetWorldPluginData(ids.PLUGINID, mainDialog.awdExporterData)  

def enableAll(mainDialog, enableBool):
    mainDialog.Enable(ids.CBOX_SELECTEDONLY, enableBool)
    mainDialog.Enable(ids.CBOX_UNUSEDMATS, enableBool)
    mainDialog.Enable(ids.CBOX_CLOSEAFTEREXPORT, enableBool)
    mainDialog.Enable(ids.CBOX_COMPRESSED, enableBool)
    mainDialog.Enable(ids.CBOX_ANIMATION, enableBool)
    mainDialog.Enable(ids.CBOX_OBJECTCOLORS, enableBool)
    mainDialog.Enable(ids.BTN_EXPORT, enableBool)
        
    if enableBool==False:
        mainDialog.Enable(ids.BTN_CANCEL, True)
    mainDialog.Enable(ids.CBOX_EXPORTMATERIALS, enableBool)
    mainDialog.Enable(ids.CBOX_STREAMING, enableBool)
    mainDialog.Enable(ids.CBOX_DEBUG, enableBool)
    mainDialog.Enable(ids.CBOX_COPYTEX, enableBool)
    mainDialog.Enable(ids.COMBO_TEXTURESMODE, enableBool)
    mainDialog.Enable(ids.COMBO_TEXTURESMODE_STR, enableBool)
    mainDialog.Enable(ids.COMBO_RANGE, enableBool)
    mainDialog.Enable(ids.COMBO_RANGE_STR, enableBool)
    mainDialog.Enable(ids.LINK_EXTERNTEXTURESPATH, enableBool)
    mainDialog.Enable(ids.LINK_EXTERNTEXTURESPATH_STR, enableBool)
    mainDialog.Enable(ids.REAL_SCALE, enableBool)
    mainDialog.Enable(ids.REAL_FIRSTFRAME, enableBool)
    mainDialog.Enable(ids.REAL_LASTFRAME, enableBool)
    mainDialog.Enable(ids.REAL_SCALE_STR, enableBool)
    mainDialog.Enable(ids.REAL_FIRSTFRAME_STR, enableBool)
    mainDialog.Enable(ids.REAL_LASTFRAME_STR, enableBool)
    if enableBool==True:
        mainDialog.Enable(ids.BTN_CANCEL, False)
        setUI(mainDialog)
