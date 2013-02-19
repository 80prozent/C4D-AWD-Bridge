#AWD Skeleton Tag (c) 2013 80prozent[a]differentdesign.de

from c4d import gui, bitmaps

import c4d
import c4d.documents
from c4d import *
from c4d import plugins, bitmaps, utils
import os, math

PLUGIN_ID = 1028937    #ID for the tag

AWDSKELETON_EXPORT              = 1010
AWDSKELETON_NAME                = 1011
AWDSKELETON_EXPORTSCENEOBJECTS  = 1014
AWDSKELETON_WRONOBJECTTYPE      = 1013

# +++++++++++++++ The plugin tag ++++++++++++++++++++++++++++++

class AWDSkeletonTagXpression(plugins.TagData):

    def Init(self,node):
        bc = node.GetDataInstance()# Reads the tag's container and opens a copy.
        bc.SetBool(AWDSKELETON_EXPORT,True)#children
        bc.SetBool(AWDSKELETON_EXPORTSCENEOBJECTS,True)#children
        bc.SetString(AWDSKELETON_NAME ,"")
        node.SetData(bc)
        return True
       
    def Draw(self, tag, op, bd, bh):        
        if op.GetType()!=Ojoint:
            tag.Remove()
            c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
            c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
            c4d.EventAdd(c4d.EVENT_ANIMATE)
        return True

# ++++++++++++++++ The Main function. Loads icons, registeres plugins on startup etc. ++++++++++++++++++
if __name__ == "__main__":
    dir, file = os.path.split(__file__)
    bmp = bitmaps.BaseBitmap()
    bmp.InitWith(os.path.join(dir, "res", "icon.tif"))
    plugins.RegisterTagPlugin(id=PLUGIN_ID, str="AWD Skeleton", g=AWDSkeletonTagXpression, description="AWDSkeletonTag", icon=bmp, info=c4d.TAG_MULTIPLE|c4d.TAG_EXPRESSION|c4d.TAG_VISIBLE)