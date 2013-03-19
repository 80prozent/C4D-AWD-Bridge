# the main Scene containing all the data and parameters needed for export
# One Instance of this class is create at the beginning of the export process in the "mainExporter.py" 
# this instance is stored in the variable "exportData" and gets modified withhin the export-process


import c4d


from awdexporter import ids
from awdexporter import classesAWDBlocks
from awdexporter import mainHelpers 
from awdexporter import classesHelper 

class mainScene(object):
    def __init__(self, doc,mainDialog):
        self.doc = doc
        self.name = doc.GetDocumentName()
        self.fps = doc.GetFps()
        self.animationCounter=0
        self.allStatusLength = 0
        self.allStatus = 0
        self.subStatus = 0
        self.status = 0
        self.scale = mainDialog.GetReal(ids.REAL_SCALE)
        self.firstFrame=mainDialog.GetReal(ids.REAL_FIRSTFRAME)
        self.lastFrame=mainDialog.GetReal(ids.REAL_LASTFRAME)
        self.unusedMats=mainDialog.GetReal(ids.CBOX_UNUSEDMATS) 
        self.debug=mainDialog.GetBool(ids.CBOX_DEBUG)        
        self.embedTextures=mainDialog.GetLong(ids.COMBO_TEXTURESMODE)        
        self.openPrefab=mainDialog.GetBool(ids.CBOX_OPENPREFAB)
        
        # store the current selected objects/tags/materials, so we can restore the selection after export
        self.originalActiveObjects = doc.GetActiveObjects(True)
        self.originalActiveTags = doc.GetActiveTags()
        self.originalActiveMaterials = doc.GetActiveMaterials()
        
        self.allc4dMaterials = doc.GetMaterials() # get all Materials found in the document
        
        self.externalFilePath=""
        	
        # define the infos needed for the AWD-File-Header     
        self.headerMagicString = "AWD"
        self.headerVersionNumberMajor = 0
        self.headerVersionNumberMinor = 0           
        self.headerFlagBits=0x0
        if mainDialog.GetBool(ids.CBOX_STREAMING)==True:
            self.headerFlagBits=0x1			
        self.headerCompressionType=0
        if mainDialog.GetBool(ids.CBOX_COMPRESSED)==True:
            self.headerCompressionType=1
        
        
        self.jointIDstoJointBlocks = {} # dictionary to find a JointBlock using a joints ID
        self.jointIDstoSkeletonBlocks = {} # dictionary to find a SkeletonBlock using a joints ID
        
        #texturesURL=mainDialog.GetString(ids.LINK_EXTERNTEXTURESPATH)
        #if texturesURL!=None:
            #self.externalFilePath=texturesURL	
					
        self.IDsToAWDBlocksDic = {}                
        self.texturePathToAWDBlocksDic = {}        
        self.MaterialsToAWDBlocksDic = {}
        self.objectsIDsDic = {}
        self.skeletonIDsDic = {}
        self.meshIDsDic = {}
        self.lightsIDsDic = {}
        self.materialsIDsDic = {}
        self.cameraIDsDic = {}
        self.texturesIDsDic = {}   
        self.allObjectsDic = {}
        self.unusedIDsDic = {}   
        self.blockDic = {}    
        self.geoDic = {}    
        self.texDic = {}    
        self.materialsDic = {}   

        self.allMatBlocks = []
        self.objList = []
        self.allSaveAWDBlocks = []
        self.allAWDBlocks = []
        self.allc4dObjects = []
        self.allUsedc4dMaterials = []
        self.AWDerrorObjects = []
        self.AWDwarningObjects = []
        self.errorMessages=[0]
        self.unconnectedInstances = []
        self.allSceneObjects = []
        self.allMeshObjects = []
        self.allSkeletonBlocks = []
        self.allMaterialsNames = []
        self.allMaterialsBlockIDS = []
        self.allMaterials = []
        self.reorderedAWDBlockss = []
        self.settings = []
        self.allSceneObjects = []
        self.allGeometries = []
        self.allSkeletons = []
        self.allSkeletonAnimations = []
        self.allAnimations = []
        self.allLightPickers = []
        self.allTextures = []   
        self.allMaterials = []   
        self.allAnimations = []

        self.saveTexturesEmbed = True
        self.cancel=False
        self.parsingOK=False
		
        self.bodyLength=0
        self.path = ""

        self.idCounter = 0
        self.defaultObjectSettings = 0

        self.texturesExternPathMode = 0  
        self.texturesEmbedPathMode = 0  
        self.texturesExternPath = None  
        self.texturesEmbedPath = None          
  
            

                                