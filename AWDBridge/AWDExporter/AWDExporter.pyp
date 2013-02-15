"""
Cinema4D AWD exporter 2012 by 80prozent[a]differentdesign.de

This Plugin exports c4d Scenes to away3d using the awd2 file format

enjoy


"""


import os
import sys
import c4d

folder = os.path.dirname(__file__)
if folder not in sys.path:
    sys.path.insert(0, folder)
    
import c4d
    
from awdexporter import ids
from awdexporter import cmddata
from awdexporter import maindialog

maindialog.__res__ = __res__

if __name__ == "__main__":

    iconID = 1390382
    icon2 = c4d.bitmaps.BaseBitmap()
    icon2.InitWith(os.path.join(os.path.dirname(__file__), "res", "exporterPic.png"))
    c4d.gui.RegisterIcon(iconID,icon2)

    icon = c4d.bitmaps.BaseBitmap()
    icon.InitWith(os.path.join(os.path.dirname(__file__), "res", "icon.tif"))
    
    title = c4d.plugins.GeLoadString(ids.STR_TITLE)
        
    c4d.plugins.RegisterCommandPlugin(ids.PLUGINID, title, 0, icon, title, cmddata.CMDData())