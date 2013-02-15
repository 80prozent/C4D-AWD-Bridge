#AWD Skeleton Animation Tag (c) 2012 80prozent
from c4d import gui, bitmaps

import c4d
import c4d.documents
from c4d import *
from c4d import plugins, bitmaps, utils
import os, math

PLUGIN_ID = 1028938				#ID for the tag


	
# +++++++++++++++ The plugin tag ++++++++++++++++++++++++++++++		
		
class AWDSkeletonAnimationTagXpression(plugins.TagData):

    def Init(self,node):
        bc = node.GetDataInstance()# Reads the tag's container and opens a copy.
        bc.SetBool(1010,True)#children
        bc.SetLong(1012,int(1015))
        bc.SetLong(1013,0)
        bc.SetLong(1014,45)
        node.SetData(bc)
        return True
		
    def Message(self, node, type, data):
        if type==c4d.MSG_DESCRIPTION_POSTSETPARAMETER:
            pass#print "fuck jes data changed"
        if type==c4d.MSG_DESCRIPTION_COMMAND:
            doc = data
            #print "fuck jes"
        return True
		
    def Draw(self, tag, op, bd, bh):
        if tag[1011]!=op.GetName():
            #tag[1011]=op.GetName()
            c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
            c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
            c4d.EventAdd(c4d.EVENT_ANIMATE)

        
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
	plugins.RegisterTagPlugin(id=PLUGIN_ID, str="AWD Skeleton Animation", g=AWDSkeletonAnimationTagXpression, description="AWDSkeletonAnimationTag", icon=bmp, info=c4d.TAG_MULTIPLE|c4d.TAG_VISIBLE)