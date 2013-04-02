# functions that will run inside the background-worker-thread
# main-functions for mesh-converting

import c4d
from c4d import documents

from awdexporter import ids
from awdexporter import classesAWDBlocks
from awdexporter import workerSubMeshReader
from awdexporter import classesHelper
from awdexporter import workerHelpers
from awdexporter import mainMaterials
from awdexporter import mainLightRouting

# convert all the geometry-blocks from c4d-polygon-object to away3d mesh
def convertMeshes(meshBlockList,exportData,workerthreat):
    for meshBlock in meshBlockList:                     # we check if the user cancelled the process
        if workerthreat.TestBreak():                        # if user cancelled 
            return                                              # and return if he has   
        convertMesh(meshBlock,exportData,workerthreat)      # convert the geometry-block into away3d-mesh-data

# collect all Skeletons that are used by a weighttag in a list
def getUsedSkeletons(cntLength,weightTag,jointIdsToSkeletonsBlocks,curDoc):
    jointCnt=0
    usedSkeletons=[]
    while jointCnt<cntLength:
        curJoint=weightTag.GetJoint(jointCnt,curDoc)
        if curJoint is not None:
            curJointName=curJoint.GetName()
            nextSkeleton=jointIdsToSkeletonsBlocks.get(str(curJointName),None) 
            if nextSkeleton is not None:
                if len(usedSkeletons)==0:
                    usedSkeletons.append(nextSkeleton)
                if len(usedSkeletons)>0:
                    allreadyExists=False
                    for skeleton in usedSkeletons:
                        if skeleton==nextSkeleton:
                            allreadyExists=True
                            break
                    if allreadyExists==False:
                        usedSkeletons.append(nextSkeleton)
        jointCnt+=1
    return usedSkeletons
    
def convertMesh(meshBlock,exportData,workerthreat):
    exportData.doc.SetActiveObject(meshBlock.sceneObject)
    if not meshBlock.sceneObject.GetTag(5604): 
        return    
    if not meshBlock.sceneObject.GetTag(5600):
        return  
        
    
    createGeoMaterials=[] # this will store the list of materials used to split the polygons into submeshes
    applyToinstanceMaterials=[] # a list of materials that will be applied for each instance that is using this geometry
    allmaterials=[]
    allInstanceMaterials=[]
    allSelections=workerHelpers.getAllPolySelections(meshBlock.sceneObject) # get all the polygon-selections as a list of helperclass.PolySelection
    baseGeoMaterials=workerHelpers.getMaterials(meshBlock.sceneObject,allSelections,False) # get all the Materials that are applied by a textureTag on the PolygonObject directly
    useSelectionsComplete=False
    useInstanceSelection=[]
    if len(baseGeoMaterials)>0:        # if a material is directly applied to the polygonObject, all instances will have this same materials (if they have not a different objectColorMode)
        for instanceBlock in meshBlock.sceneBlocks:
            if instanceBlock.isRenderInstance==True:
                instanceBlock=meshBlock
            textBaseMat=baseGeoMaterials[0] # the first material in this list should allways be a material not restricted by polySelection (e.g. the 'baseMaterial')
            useSelections, returnBasemat = workerHelpers.getObjectColorMode(instanceBlock.sceneObject,textBaseMat,exportData)# get the BaseMaterial used by this Instance, and a boolean, if the selections should be used on this instance or not
            applyToinstanceMaterials.append(returnBasemat)   
            useInstanceSelection.append(useSelections)
            if useSelections==True: # if the selections are used on this Instance:
                useSelectionsComplete=True # the polygonObject must be split into the selections
          
        if useSelectionsComplete==True: # if the polygonObject must be split:
            createGeoMaterials=workerSubMeshReader.cleanMaterialRestriction(meshBlock,baseGeoMaterials) # get all the Materials and make shure that each polygon is used ba only one material, delete unused materials
            instanceCnt=0
            useFirst=True
            if str(createGeoMaterials[0][1].name)!="Base":
                useFirst=False
            for instanceBlock in meshBlock.sceneBlocks:
                newInstanceMats=[]
                geoMatCnt=0
                if useFirst==True:
                    newInstanceMats.append(applyToinstanceMaterials[instanceCnt][0])
                    geoMatCnt=1
                while geoMatCnt<len(createGeoMaterials):
                    if useInstanceSelection[instanceCnt]==True:
                        newInstanceMats.append(createGeoMaterials[geoMatCnt][0])
                    if useInstanceSelection[instanceCnt]==False:
                        newInstanceMats.append(applyToinstanceMaterials[instanceCnt][0])
                    geoMatCnt+=1
                instanceBlock.saveMaterials=newInstanceMats
                instanceCnt+=1   
                      
            
    if len(baseGeoMaterials)==0:       # if no materials are directly applied, we check all instances for their directly applied and inherited materials and the baseobject for the inherited too.
 
        instanceCnt=0
        for instanceBlock in meshBlock.sceneBlocks:
            instanceMaterials=workerHelpers.getMaterials(instanceBlock.sceneObject,allSelections,True)# search for all materials that are applied to the instance-object (including inheritet tags)
            textBaseMat=None
            if instanceBlock.isRenderInstance==True: # if the instance is considered a renderInstance, we use the baseObject (meshblock.sceneObject) for the ObjectColorMode-check
                instanceBlock=meshBlock
            if len(instanceMaterials)>0:
                textBaseMat=instanceMaterials[0]
            useSelections, returnMat = workerHelpers.getObjectColorMode(instanceBlock.sceneObject,textBaseMat,exportData)
            if len(instanceMaterials)==0:
                instanceMaterials.append([])
            instanceMaterials[0]= returnMat
            useInstanceSelection.append(useSelections)
            if useSelections==True: # if the selections are used on this Instance:
                useSelectionsComplete=True # the polygonObject must be split into the selections
            allInstanceMaterials.append(instanceMaterials)
            applyToinstanceMaterials.append(instanceMaterials[0])
            if instanceCnt==0:
                baseGeoMaterials=instanceMaterials
            instanceCnt+=1
                
        if useSelectionsComplete==True: # if the polygonObject must be split:
            allMatsDic={} 
            allmaterials=[]
            instanceCnt=0
            allCleanMats=[]
            for instanceBlock in meshBlock.sceneBlocks:
                if useInstanceSelection[instanceCnt]==True:
                    cleanedMats=workerSubMeshReader.cleanMaterialRestriction(meshBlock,allInstanceMaterials[instanceCnt]) # get all the Materials and make shure that each polygon is used ba only one material, delete unused materials
                    allCleanMats.append(cleanedMats)
                    for cleanedMat in cleanedMats:                    
                        matExists=allMatsDic.get(str(cleanedMat[1].name),None)
                        if matExists is None:
                            allMatsDic[str(cleanedMat[1].name)]=cleanedMat
                            cleanedMat.append(instanceBlock)
                            allmaterials.append(cleanedMat)  
                if useInstanceSelection[instanceCnt]==False:
                    allCleanMats.append([allInstanceMaterials[instanceCnt][0]])
                instanceCnt+=1
            createGeoMaterials=workerSubMeshReader.mergeMaterialRestriction(meshBlock,allmaterials)
            instanceCnt=0
            useFirst=True
            if str(createGeoMaterials[0][1].name)!="Base":
                useFirst=False
            for instanceBlock in meshBlock.sceneBlocks:
                newInstanceMats=[]
                geoMatCnt=0
                if useFirst==True:
                    newInstanceMats.append(applyToinstanceMaterials[instanceCnt][0])
                    geoMatCnt=1
                while geoMatCnt<len(createGeoMaterials):
                    if useInstanceSelection[instanceCnt]==True:
                        foundOnInstance=applyToinstanceMaterials[instanceCnt][0] # if this will not be changed, the baseMaterial will be set for this Submesh                        
                        for intMat in allCleanMats[instanceCnt]:
                            if str(intMat[1].name)==str(createGeoMaterials[geoMatCnt][1].name):
                                foundOnInstance=intMat[0]
                                break
                            nameCnt=0
                            for name in createGeoMaterials[geoMatCnt][1].multiNames:
                                if str(intMat[1].name)==str(name):
                                    foundOnInstance=createGeoMaterials[geoMatCnt][1].multiMats[nameCnt]
                                nameCnt+=1  
                        newInstanceMats.append(foundOnInstance)
                    if useInstanceSelection[instanceCnt]==False:# if the instance des not use selections, we just apply the baseMaterial of this instance to all submeshes
                        newInstanceMats.append(applyToinstanceMaterials[instanceCnt][0])
                    geoMatCnt+=1
                instanceBlock.saveMaterials=newInstanceMats
                instanceCnt+=1                     
        
    if useSelectionsComplete==False: # if the polygonObject must not be split
        createGeoMaterials=workerSubMeshReader.clearSubmeshIndexe(meshBlock,baseGeoMaterials) 
        instanceCnt=0
        for instanceBlock in meshBlock.sceneBlocks:
            newInstanceMats=[]
            geoMatCnt=0
            newInstanceMats.append(applyToinstanceMaterials[instanceCnt][0])
            instanceBlock.saveMaterials=newInstanceMats
            instanceCnt+=1
        
        # since the material-selections can overwrite each other, we make shure one polygon can only be used by one material/selection  
    
    #print "finalMats = "+str(finalMats) 
    if workerthreat.TestBreak():
        return        
         
    # for all materialBlocks that will be applied to MeshInstanceBlocks, we make shure that they are fully created (the textureBlocks will be created here) and set to tagForExport = True
    for instanceBlock in meshBlock.sceneBlocks:
        instanceBlock.lightPickerIdx=mainLightRouting.getObjectLights(instanceBlock.sceneObject,exportData)# get the LightPicker for this sceneObject (if the lightpicker does not allready exists, it will be created)
        for mat in instanceBlock.saveMaterials:
            matAwdBlock=exportData.allAWDBlocks[int(mat)]
            if matAwdBlock is not None:
                if matAwdBlock.isCreated==False and matAwdBlock.colorMat==False:
                    matAwdBlock.isCreated=True                
                    mainMaterials.createMaterial(matAwdBlock,exportData)
                if matAwdBlock.tagForExport==False:
                    matAwdBlock.tagForExport=True
   
   
    for mat in createGeoMaterials:    # create a SubMeshBlock for every Material/selection found and used
        #print "create Submesh: "+str(mat[0])
        meshBlock.saveSubMeshes.append(classesAWDBlocks.awdSubMesh(mat[0],mat[1].name,mat[1].selectionIndexe,mat[2]))
    if workerthreat.TestBreak():
        return       
            
    #for instanceMat in allInstanceMaterials
        
    #for mat in finalMats:    # create a SubMeshBlock for every Material/selection found
    #    for instanceBlock in meshBlock.sceneBlocks:
    #        saveMaterials=

    # if the meshBlock has a WeightTag-applied, we check if the mesh is used by one single skeleton or not.
    weightTag=meshBlock.sceneObject.GetTag(c4d.Tweights)
    if weightTag is not None:
        jointCount=weightTag.GetJointCount()
        allSkeletons=getUsedSkeletons(jointCount,weightTag,exportData.jointIDstoSkeletonBlocks,exportData.doc)           
        if len(allSkeletons)==0:
            print "Warning - No Joints are bound to a valid Skeleton"
        if len(allSkeletons)>1:
            print "Warning - Not all Joints are bound to the same Skeleton"
        if len(allSkeletons)==1:
            meshBlock.weightTag=weightTag
            
    if workerthreat.TestBreak():
        return
        
    #morphs=[]    
    #for morphState in allPointAndUvMorpTag:
        #if morphState.morphedObject==cur_mesh:
            #morphs.append(morphState)   
    #for submesh in new_submeshes:
        #for morphState in morphs:
            #submorphVerts=[]
            #submorphUVs=[]
            #submorphActiv=False
            #submorphdata=[submorphVerts,submorphUVs,submorphActiv,morphState.morphName,morphState.tagName,morphState.tagObject]
            #submesh.morphs.append(submorphdata)                
    #print ("parse = "+str(meshBlock.sceneObject.GetName()))            
    workerSubMeshReader.collectSubmeshData(meshBlock,exportData,workerthreat)   # parse this object into a awd2-geometry-block
    
    if workerthreat.TestBreak():                                                # when the user has cancelled the process: 
        return                                                                      # we stop executing and return 
        
    for subMesh in meshBlock.saveSubMeshes:                                     # for every SubMeshBlock that has been created:
        if workerthreat.TestBreak():                                                # we check if the user cancelled the process
            return                                                                      # and return if he has
        workerSubMeshReader.transformUVS(subMesh)                                   # transform the uvs if needed (to allow for tilling etc)
        if workerthreat.TestBreak():                                                # check if the user cancelled the process
            return                                                                      # and return if he has
        workerSubMeshReader.buildGeometryStreams(subMesh,exportData.scale)          # build the AWD-geometry-streams for all submeshes



          
  
