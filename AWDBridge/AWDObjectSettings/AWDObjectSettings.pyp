#AWD Object Settings (c) 2012 80prozent@differentdesign
from c4d import gui, bitmaps

import c4d
import c4d.documents
from c4d import *
from c4d import plugins, bitmaps, utils
import os, math

#be sure to use a unique ID obtained from www.plugincafe.com
PLUGIN_ID = 1028905				#ID for the tag

# here come global variables
prev_active = 0
prev_op = None   

	
# +++++++++++++++ The plugin tag ++++++++++++++++++++++++++++++		
		
class AWDObjectSettingsXpression(plugins.TagData):

    def Init(self,op):
        #print("init")
        bc = op.GetDataInstance()# Reads the tag's container and opens a copy.
        bc.SetData(1002,0)
        bc.SetData(1005,0)
        bc.SetBool(1016,True)	#children
        bc.SetBool(1014,True)	#export
        bc.SetBool(1013,True)	#lights
        bc.SetBool(1015,True)	#UV
        bc.SetBool(1017,True)	#Normal
        bc.SetBool(1018,False)	#Triangulate
        bc.SetBool(1019,True)	#Optimize
        #bc.SetData(1005, False)
        op.SetData(bc)
		
        return True
	
    def Execute(self, tag, doc, op, bt, priority, flags):
        op.KillTag(PLUGIN_ID)
        print("init")

# ++++++++++++++++ The Main function. Loads icons, registeres plugins on startup etc. ++++++++++++++++++
if __name__ == "__main__":
	dir, file = os.path.split(__file__)
	bmp = bitmaps.BaseBitmap()
	bmp.InitWith(os.path.join(dir, "res", "icon.tif"))
	plugins.RegisterTagPlugin(id=PLUGIN_ID, str="AWD Object Settings", g=AWDObjectSettingsXpression, description="AWDObjectSettings", icon=bmp, info=c4d.TAG_MULTIPLE|c4d.TAG_VISIBLE)