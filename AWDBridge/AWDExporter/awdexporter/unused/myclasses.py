
		
class infoObject(object):
    def __init__(self, error=None,message=None,data=None):
        self.error = error
        self.message = message
        self.data = data		
		
class sceneData(object):
    def __init__(self, name=None):
        self.name = name
        self.allObjectsDic = {}
        self.settings = []
        self.allSceneObjects = []
        self.allGeometries = []
        self.allSkeletons = []
        self.allAnimations = []
        self.allLightPickers = []
        self.allTextures = []   
        self.allMaterials = []   
		
class sceneObject(object):
    def __init__(self, name=None):
        self.name = name
        self.sceneID = None
        self.blockID = None		
        self.parentID = None	# used to restore the hirarchy in away3d
        self.type = None
        self.sceneKeyFrames = []
        self.objectKeyFrames = []
        self.sceneMorphShapes = []
		
class objectSettings(object):
    def __init__(self, uvs=None, normals=None, optimize=None, nameSpace=None):
        self.uvs = uvs
        self.normals = normals
        self.optimize = optimize   
        self.nameSpace = nameSpace   
		
class animation(object):
    def __init__(self, name=None, animationID=None, firstFrame=None, lastFrame=None, fps=None):
        self.name = name
        self.animationID = animationID
        self.firstFrame = firstFrame
        self.lastFrame = lastFrame   
        self.fps = fps   
		
class exportObject(object):
    def __init__(self, name=None,type=None):
        self.name = name
        self.type = type
        self.params = {}
        self.children = []     

class PointAndUvMorpTag(object):
    def __init__(self, morphName=None,tagName=None,morphedObject=None,tagObject=None,morphedPoints=None,morphedUVs=None):
        self.morphName = morphName
        self.tagName=tagName 
        self.morphedObject=morphedObject
        self.tagObject=tagObject
        self.morphedPoints=morphedPoints
        self.morphedUVs=morphedUVs

class SubMesh(object):
    def __init__(self, mat=None,used_indexxe=None,name=None):
        self.name = name
        self.mat = mat
        self.used_indexxe = used_indexxe
        self.indexBuffer=[]
        self.indexBufferMorphed=[]
        self.vertexBuffer=[]
        self.vertexBufferMorphed=[]
        self.sharedvertexBuffer=[]
        self.sharedvertexBufferMorphed=[]
        self.sharedvertexArrays=[]
        self.normalBuffer=[]
        self.normalBufferMorphed=[]
        self.faceNormal=[]
        self.faceNormalMorphed=[]
        self.uvBuffer=[]
        self.uvBufferMorphed=[]
        self.weightsBuffer=[]
        self.jointidxBuffer=[]
        self.hasweight_counter=0
        self.morphs=[]
        self.uniquePool=[]
        self.uniquePoolMorphed=[]
        self.polygonBuffer=[]
        self.uniquePoolDict={}
        self.polydic={}
        #self.weightsBuffer=[]

class PolySelection(object):
    def __init__(self, name=None,indexe=None):
        self.name = name
        self.indexe=indexe 