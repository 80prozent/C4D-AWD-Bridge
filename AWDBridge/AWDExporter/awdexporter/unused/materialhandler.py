import c4d
from c4d import documents

from awdexporter import ids

def parse_mats(self,mats_xml,unused_mats,used_mat_names):
    mats_xml.setAttribute("name","Materials")
    doc=documents.GetActiveDocument()
    all_mats=doc.GetMaterials()
    for mat in all_mats:
        export=False
        if unused_mats==False:
            for usedmats in used_mat_names:
                if mat.GetName()==usedmats:
                    export=True
        if unused_mats==True or export==True:
            if str(mat.GetTypeName())!="Mat":
                pass
            #print "found unsupported shader - type = "+str(mat.GetTypeName())+" / name = "+str(mat.GetName())
            if str(mat.GetTypeName())=="Mat":
                oneMat_xml=dom.Element("Mat")#create a new XML-Node. "obj_counter" descripes the level (hirachy)
                oneMat_xml.setAttribute("name",str(mat.GetName())) 
    
                colorShader_xml=dom.Element("ColorShader")
                colorShader_xml.setAttribute("name","Color")
                colorShader_xml.setAttribute("enabled",str(mat[c4d.MATERIAL_USE_COLOR]))
                colorShader_xml.setAttribute("fileLink","None")
                if(mat[c4d.MATERIAL_COLOR_SHADER]):  
                    colorShader_xml.setAttribute("fileLink",str(mat[c4d.MATERIAL_COLOR_SHADER][c4d.BITMAPSHADER_FILENAME]))
                    colorShader_xml.setAttribute("texMixMode",str(mat[c4d.MATERIAL_COLOR_TEXTUREMIXING]))
                    colorShader_xml.setAttribute("texStrength",str(mat[c4d.MATERIAL_COLOR_TEXTURESTRENGTH]))
                    color_ar= str(mat[c4d.MATERIAL_COLOR_COLOR].x)+"#"+str(mat[c4d.MATERIAL_COLOR_COLOR].y)+"#"+str(mat[c4d.MATERIAL_COLOR_COLOR].z)
                    colorShader_xml.setAttribute("texColor",color_ar)
                    colorShader_xml.setAttribute("Brightness",str(mat[c4d.MATERIAL_COLOR_BRIGHTNESS]))
                    oneMat_xml.appendChild(colorShader_xml)
        
                diffuseShader_xml=dom.Element("DiffusionShader")
                diffuseShader_xml.setAttribute("name","Diffusion")
                diffuseShader_xml.setAttribute("enabled",str(mat[c4d.MATERIAL_USE_DIFFUSION]))
                diffuseShader_xml.setAttribute("brightness",str(mat[c4d.MATERIAL_DIFFUSION_BRIGHTNESS]))
                diffuseShader_xml.setAttribute("affectLuminace",str(mat[c4d.MATERIAL_DIFFUSION_AFFECT_LUMINANCE]))
                diffuseShader_xml.setAttribute("affectLuminace",str(mat[c4d.MATERIAL_DIFFUSION_AFFECT_SPECULAR]))
                diffuseShader_xml.setAttribute("affectLuminace",str(mat[c4d.MATERIAL_DIFFUSION_AFFECT_REFLECTION]))
                if(mat[c4d.MATERIAL_DIFFUSION_SHADER]): 
                    diffuseShader_xml.setAttribute("fileLink",str(mat[c4d.MATERIAL_DIFFUSION_SHADER][c4d.BITMAPSHADER_FILENAME]))
                    oneMat_xml.appendChild(diffuseShader_xml)
                     
                luminaceShader_xml=dom.Element("LuminanceShader")
                luminaceShader_xml.setAttribute("name","Luminance")
                luminaceShader_xml.setAttribute("enabled",str(mat[c4d.MATERIAL_USE_LUMINANCE]))
                color_ar= str(mat[c4d.MATERIAL_LUMINANCE_COLOR].x)+"#"+str(mat[c4d.MATERIAL_LUMINANCE_COLOR].y)+"#"+str(mat[c4d.MATERIAL_LUMINANCE_COLOR].z)
                luminaceShader_xml.setAttribute("texColor",color_ar)
                luminaceShader_xml.setAttribute("Brightness",str(mat[c4d.MATERIAL_LUMINANCE_BRIGHTNESS]))
                if(mat[c4d.MATERIAL_LUMINANCE_SHADER]):  
                    luminaceShader_xml.setAttribute("fileLink",str(mat[c4d.MATERIAL_LUMINANCE_SHADER][c4d.BITMAPSHADER_FILENAME]))
                    luminaceShader_xml.setAttribute("texMixMode",str(mat[c4d.MATERIAL_LUMINANCE_TEXTUREMIXING]))
                    luminaceShader_xml.setAttribute("texStrength",str(mat[c4d.MATERIAL_LUMINANCE_TEXTURESTRENGTH]))
                    oneMat_xml.appendChild(luminaceShader_xml)
        
                transShader_xml=dom.Element("TransparencyShader")
                transShader_xml.setAttribute("name","Transparency")
                transShader_xml.setAttribute("enabled",str(mat[c4d.MATERIAL_USE_TRANSPARENCY]))
                color_ar= str(mat[c4d.MATERIAL_TRANSPARENCY_COLOR].x)+"#"+str(mat[c4d.MATERIAL_TRANSPARENCY_COLOR].y)+"#"+str(mat[c4d.MATERIAL_TRANSPARENCY_COLOR].z)
                transShader_xml.setAttribute("texColor",color_ar)
                transShader_xml.setAttribute("Brightness",str(mat[c4d.MATERIAL_TRANSPARENCY_BRIGHTNESS]))
                transShader_xml.setAttribute("Refraction",str(mat[c4d.MATERIAL_TRANSPARENCY_REFRACTION]))
                transShader_xml.setAttribute("TotalInternalReflection",str(mat[c4d.MATERIAL_TRANSPARENCY_FRESNEL]))
                transShader_xml.setAttribute("ExternalReflection",str(mat[c4d.MATERIAL_TRANSPARENCY_EXITREFLECTIONS]))
                transShader_xml.setAttribute("FresnelReflectivity",str(mat[c4d.MATERIAL_TRANSPARENCY_FRESNELREFLECTIVITY]))
                transShader_xml.setAttribute("Additiv",str(mat[c4d.MATERIAL_TRANSPARENCY_ADDITIVE]))
                transShader_xml.setAttribute("ExternalReflection",str(mat[c4d.MATERIAL_TRANSPARENCY_EXITREFLECTIONS]))
                if(mat[c4d.MATERIAL_TRANSPARENCY_SHADER]):  
                    transShader_xml.setAttribute("fileLink",str(mat[c4d.MATERIAL_TRANSPARENCY_SHADER][c4d.BITMAPSHADER_FILENAME]))
                    transShader_xml.setAttribute("texMixMode",str(mat[c4d.MATERIAL_TRANSPARENCY_TEXTUREMIXING]))
                    transShader_xml.setAttribute("texStrength",str(mat[c4d.MATERIAL_TRANSPARENCY_TEXTURESTRENGTH]))
                    color_ar= str(mat[c4d.MATERIAL_TRANSPARENCY_ABSORPTIONCOLOR].x)+"#"+str(mat[c4d.MATERIAL_TRANSPARENCY_ABSORPTIONCOLOR].y)+"#"+str(mat[c4d.MATERIAL_TRANSPARENCY_ABSORPTIONCOLOR].z)
                    transShader_xml.setAttribute("Absorptioncolo",color_ar)
                    transShader_xml.setAttribute("AbsorptionDistance",str(mat[c4d.MATERIAL_TRANSPARENCY_ABSORPTIONDISTANCE]))
                    transShader_xml.setAttribute("Bluminess",str(mat[c4d.MATERIAL_TRANSPARENCY_DISPERSION]))
                    transShader_xml.setAttribute("MinSamples",str(mat[c4d.MATERIAL_TRANSPARENCY_MINSAMPLES]))
                    transShader_xml.setAttribute("MaxSamples",str(mat[c4d.MATERIAL_TRANSPARENCY_MAXSAMPLES]))
                    transShader_xml.setAttribute("Accuracy",str(mat[c4d.MATERIAL_TRANSPARENCY_ACCURACY]))
                    oneMat_xml.appendChild(transShader_xml)
        
                reflectShader_xml=dom.Element("ReflectionShader")
                reflectShader_xml.setAttribute("name","Reflection")
                reflectShader_xml.setAttribute("enabled",str(mat[c4d.MATERIAL_USE_REFLECTION]))
                color_ar= str(mat[c4d.MATERIAL_REFLECTION_COLOR].x)+"#"+str(mat[c4d.MATERIAL_REFLECTION_COLOR].y)+"#"+str(mat[c4d.MATERIAL_REFLECTION_COLOR].z)
                reflectShader_xml.setAttribute("texColor",color_ar)
                reflectShader_xml.setAttribute("Brightness",str(mat[c4d.MATERIAL_REFLECTION_BRIGHTNESS]))
                reflectShader_xml.setAttribute("Additive",str(mat[c4d.MATERIAL_REFLECTION_ADDITIVE]))
                if(mat[c4d.MATERIAL_REFLECTION_SHADER]):  
                    reflectShader_xml.setAttribute("fileLink",str(mat[c4d.MATERIAL_REFLECTION_SHADER][c4d.BITMAPSHADER_FILENAME]))
                    reflectShader_xml.setAttribute("texMixMode",str(mat[c4d.MATERIAL_REFLECTION_TEXTUREMIXING]))
                    reflectShader_xml.setAttribute("texStrength",str(mat[c4d.MATERIAL_REFLECTION_TEXTURESTRENGTH]))              
                    reflectShader_xml.setAttribute("Bluminess",str(mat[c4d.MATERIAL_REFLECTION_DISPERSION]))
                    reflectShader_xml.setAttribute("MinSamples",str(mat[c4d.MATERIAL_REFLECTION_MINSAMPLES]))
                    reflectShader_xml.setAttribute("MaxSamples",str(mat[c4d.MATERIAL_REFLECTION_MAXSAMPLES]))
                    reflectShader_xml.setAttribute("Accuracy",str(mat[c4d.MATERIAL_REFLECTION_ACCURACY]))
                    oneMat_xml.appendChild(reflectShader_xml)
        
                enviromentShader_xml=dom.Element("EnviromentShader")
                enviromentShader_xml.setAttribute("name","Enviroment")
                enviromentShader_xml.setAttribute("enabled",str(mat[c4d.MATERIAL_USE_ENVIRONMENT]))
                color_ar= str(mat[c4d.MATERIAL_ENVIRONMENT_COLOR].x)+"#"+str(mat[c4d.MATERIAL_ENVIRONMENT_COLOR].y)+"#"+str(mat[c4d.MATERIAL_ENVIRONMENT_COLOR].z)
                enviromentShader_xml.setAttribute("texColor",color_ar)
                enviromentShader_xml.setAttribute("Brightness",str(mat[c4d.MATERIAL_ENVIRONMENT_BRIGHTNESS]))
                if(mat[c4d.MATERIAL_ENVIRONMENT_SHADER]):  
                    enviromentShader_xml.setAttribute("fileLink",str(mat[c4d.MATERIAL_ENVIRONMENT_SHADER][c4d.BITMAPSHADER_FILENAME]))
                    enviromentShader_xml.setAttribute("texMixMode",str(mat[c4d.MATERIAL_ENVIRONMENT_TEXTUREMIXING]))
                    enviromentShader_xml.setAttribute("texStrength",str(mat[c4d.MATERIAL_ENVIRONMENT_TEXTURESTRENGTH]))              
                    enviromentShader_xml.setAttribute("TilesX",str(mat[c4d.MATERIAL_ENVIRONMENT_TILESX]))
                    enviromentShader_xml.setAttribute("TilesY",str(mat[c4d.MATERIAL_ENVIRONMENT_TILESY]))
                    enviromentShader_xml.setAttribute("exclusive",str(mat[c4d.MATERIAL_ENVIRONMENT_EXCLUSIVE]))
                    oneMat_xml.appendChild(enviromentShader_xml)
        
                fogShader_xml=dom.Element("FogShader")
                fogShader_xml.setAttribute("name","Fog")
                fogShader_xml.setAttribute("enabled",str(mat[c4d.MATERIAL_USE_FOG]))
                color_ar= str(mat[c4d.MATERIAL_FOG_COLOR].x)+"#"+str(mat[c4d.MATERIAL_FOG_COLOR].y)+"#"+str(mat[c4d.MATERIAL_FOG_COLOR].z)
                fogShader_xml.setAttribute("texColor",color_ar)
                fogShader_xml.setAttribute("Brightness",str(mat[c4d.MATERIAL_FOG_BRIGHTNESS]))
                fogShader_xml.setAttribute("Distance",str(mat[c4d.MATERIAL_FOG_DISTANCE]))
                oneMat_xml.appendChild(fogShader_xml)
        
                bumpShader_xml=dom.Element("BumpShader")
                bumpShader_xml.setAttribute("name","Bump")
                bumpShader_xml.setAttribute("enabled",str(mat[c4d.MATERIAL_USE_BUMP]))
                if(mat[c4d.MATERIAL_BUMP_SHADER]):  
                    bumpShader_xml.setAttribute("fileLink",str(mat[c4d.MATERIAL_BUMP_SHADER][c4d.BITMAPSHADER_FILENAME]))
                    bumpShader_xml.setAttribute("Strength",str(mat[c4d.MATERIAL_BUMP_STRENGTH]))
                    bumpShader_xml.setAttribute("Strength",str(mat[c4d.MATERIAL_BUMP_MIPFALLOFF]))
                    oneMat_xml.appendChild(bumpShader_xml)
        
                normalShader_xml=dom.Element("NormalShader")
                normalShader_xml.setAttribute("name","Normal")
                normalShader_xml.setAttribute("enabled",str(mat[c4d.MATERIAL_USE_NORMAL]))
                normalShader_xml.setAttribute("fileLink","None")
                if(mat[c4d.MATERIAL_NORMAL_SHADER]):  
                    normalShader_xml.setAttribute("fileLink",str(mat[c4d.MATERIAL_NORMAL_SHADER][c4d.BITMAPSHADER_FILENAME]))
                    normalShader_xml.setAttribute("normStrength",str(mat[c4d.MATERIAL_NORMAL_STRENGTH]))
                    normal_method=""
                    if mat[c4d.MATERIAL_NORMAL_SPACE]==0:
                        normal_method="tangent"
                        normalShader_xml.setAttribute("flipZ",str(0))
                    if mat[c4d.MATERIAL_NORMAL_SPACE]==1:
                        normal_method="object"
                        normalShader_xml.setAttribute("flipZ",str(mat[c4d.MATERIAL_NORMAL_REVERSEZ]))
                    if mat[c4d.MATERIAL_NORMAL_SPACE]==2:
                        normal_method="world" 
                        normalShader_xml.setAttribute("flipZ",str(mat[c4d.MATERIAL_NORMAL_REVERSEZ]))            
                    normalShader_xml.setAttribute("normMethod",normal_method)
                    normalShader_xml.setAttribute("flipX",str(mat[c4d.MATERIAL_NORMAL_REVERSEX]))
                    normalShader_xml.setAttribute("flipY",str(mat[c4d.MATERIAL_NORMAL_REVERSEY]))
                    normalShader_xml.setAttribute("swapYandZ",str(mat[c4d.MATERIAL_NORMAL_SWAP]))
                    oneMat_xml.appendChild(normalShader_xml)    
        
                alphaShader_xml=dom.Element("AlphaShader")
                alphaShader_xml.setAttribute("name","Alpha")
                alphaShader_xml.setAttribute("enabled",str(mat[c4d.MATERIAL_USE_ALPHA]))
                color_ar= str(mat[c4d.MATERIAL_ALPHA_COLOR].x)+"#"+str(mat[c4d.MATERIAL_ALPHA_COLOR].y)+"#"+str(mat[c4d.MATERIAL_ALPHA_COLOR].z)
                alphaShader_xml.setAttribute("Color",color_ar)
                color_ar= str(mat[c4d.MATERIAL_ALPHA_DELTA].x)+"#"+str(mat[c4d.MATERIAL_ALPHA_DELTA].y)+"#"+str(mat[c4d.MATERIAL_ALPHA_DELTA].z)
                alphaShader_xml.setAttribute("Delta",color_ar)
                alphaShader_xml.setAttribute("invert",str(mat[c4d.MATERIAL_ALPHA_INVERT]))
                alphaShader_xml.setAttribute("soft",str(mat[c4d.MATERIAL_ALPHA_SOFT]))
                alphaShader_xml.setAttribute("imageAlpha",str(mat[c4d.MATERIAL_ALPHA_IMAGEALPHA]))
                alphaShader_xml.setAttribute("premultiplied",str(mat[c4d.MATERIAL_ALPHA_PREMULTIPLIED]))
                if(mat[c4d.MATERIAL_ALPHA_SHADER]):  
                    alphaShader_xml.setAttribute("fileLink",str(mat[c4d.MATERIAL_ALPHA_SHADER][c4d.BITMAPSHADER_FILENAME]))
                    oneMat_xml.appendChild(alphaShader_xml)
        
                specShader_xml=dom.Element("SpecularShader")
                specShader_xml.setAttribute("name","Specular")
                specShader_xml.setAttribute("enabled",str(mat[c4d.MATERIAL_USE_SPECULAR]))
                spec_method=""
                if mat[c4d.MATERIAL_SPECULAR_MODE]==0:
                    spec_method="plastic"
                if mat[c4d.MATERIAL_SPECULAR_MODE]==1:
                    spec_method="metall"
                if mat[c4d.MATERIAL_SPECULAR_MODE]==2:
                    spec_method="colored"         
                specShader_xml.setAttribute("specMethod",spec_method)
                specShader_xml.setAttribute("specWidth",str(mat[c4d.MATERIAL_SPECULAR_WIDTH]))
                specShader_xml.setAttribute("specHeight",str(mat[c4d.MATERIAL_SPECULAR_HEIGHT]))
                specShader_xml.setAttribute("fallOFF",str(mat[c4d.MATERIAL_SPECULAR_FALLOFF]))
                specShader_xml.setAttribute("innerWidth",str(mat[c4d.MATERIAL_SPECULAR_INNERWIDTH]))
                oneMat_xml.appendChild(specShader_xml)
        
                specColorShader_xml=dom.Element("SpecColorShader")
                specColorShader_xml.setAttribute("name","Specular Color")
                specColorShader_xml.setAttribute("enabled",str(mat[c4d.MATERIAL_USE_SPECULARCOLOR]))
                color_ar= str(mat[c4d.MATERIAL_SPECULAR_COLOR].x)+"#"+str(mat[c4d.MATERIAL_SPECULAR_COLOR].y)+"#"+str(mat[c4d.MATERIAL_SPECULAR_COLOR].z)
                specColorShader_xml.setAttribute("Color",color_ar)
                specColorShader_xml.setAttribute("Brigthness",str(mat[c4d.MATERIAL_SPECULAR_BRIGHTNESS]))
                if(mat[c4d.MATERIAL_SPECULAR_SHADER]):  
                    specColorShader_xml.setAttribute("fileLink",str(mat[c4d.MATERIAL_SPECULAR_SHADER][c4d.BITMAPSHADER_FILENAME]))
                    specColorShader_xml.setAttribute("texMixMode",str(mat[c4d.MATERIAL_SPECULAR_TEXTUREMIXING]))
                    specColorShader_xml.setAttribute("texStrength",str(mat[c4d.MATERIAL_SPECULAR_TEXTURESTRENGTH])) 
                    oneMat_xml.appendChild(specColorShader_xml)
        
                glowShader_xml=dom.Element("GlowShader")
                glowShader_xml.setAttribute("name","Glow")
                glowShader_xml.setAttribute("enabled",str(mat[c4d.MATERIAL_USE_GLOW]))
                oneMat_xml.appendChild(glowShader_xml)
                #print "assigned "+str(mat.GetTypeName())#[c4d.MATERIAL_PAGE_ASSIGNMENT])
                #print "texture_strength "+str(i.__getitem__([0,c4d.MatAssignData]))#[c4d.MatAssignData])
                #print "mat assigned to: "+str(mat[c4d.MatAssignData].GetData())
                #print "Texture : "+str(i.GetMaterial()[c4d.MATERIAL_USE_COLOR])
                #print "Texture : "+str(i.GetMaterial().GetData())
                mats_xml.appendChild(oneMat_xml)
        #cur_xml.appendChild(mats_xml)