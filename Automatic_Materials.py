""" Automatic Materials 1.1 Created by Michael Fischer

This script imports the images from your projects sourceimages folder,
creates a shader for each material and connects them based off of the file names.
Non color maps are changed to raw, ignore cs rules on and normal maps have bump2d maps / rsnormal maps.

--- USER ADJUSTMENT INSTRUCTIONS ---
Change the default_shader to change the shader the script creates. ex: default_shader = redshift (NO QUOTES)
Change the project_is_set to False to select a file folder instead of the automatic sourceimages folder.
Change object_material_connect to False to disable auto assigning objects to materials based off their names.
Change the image names inside the quotes if you named your files differently. ex: color_text = 'col'
Save the python file to save your settings for next time and add to shelf or a hotkey for easier access.

"""
import maya.cmds as cmds
import maya.mel as mel

arnold = 'aiStandardSurface'
blinn = 'blinn'
phong = 'phong'
redshift = 'RedshiftMaterial'
lambert = 'lambert'

Beckmann = 0
GGX = 1
Ashikhmin = 2

''' CHANGE YOUR DEFAULT SHADER HERE '''
default_shader = redshift   #Change the default shader the script creates from any of the above variables. Copy the left side names.

''' Change additional settings here '''
project_is_set = True   #True: Searches project's sourceimages for images. False: User selects the folder that will be searched.
object_material_connect = True   #True: Assigns matching object and material names. False: Does not assign materials to objects for you.
default_project_image_directory = 'sourceimages'   #Change 'sourceimages' to another folder name in your set project.
bumpDepth_def = 0.150   #Change the default bump depth value for your normal maps.
material_suffix = '_mat' #Adds a material suffix to shaders it creates if non in your map names
object_suffix = '_low' #Looks to match object names to shader name ignoring the object_suffix defined here
default_BRDF = GGX #For Redshift pick from Beckmann, GGX or Ashikmin

''' Change your image names here ''' #Refers to the suffix of your images. ex: arm_material_Base_Color is found in color_text.
color_text = 'Color'
color_alt_text = 'Diffuse'
color_alt2_text = 'Albedo'
roughness_text = 'Roughness'
roughness_alt_text = 'Glossiness'
metal_text = "Metal"
metal_alt_text = 'Reflection'
normal_text = 'Normal'  #If you have two normal maps for the same material the first normal called is assigned OpenGL, DirectX, Normal.
emissive_text = 'Emissive'
scatter_text = 'Scattering'
opacity_text = 'Opacity'  #'opacity' is also already searched for.
opacity_alt_text = 'Alpha'
ior_text = 'IOR'  #'IOR' and 'Ior' are also already searched for.
translucency_text = 'Translucency'

dir_total = []
shaders_list = [arnold, blinn, phong, redshift, lambert]
shaders_color_list = ['.baseColor', '.color', '.color', '.diffuse_color', '.color']
node_list = ['RedshiftNormalMap','RedshiftPostEffects','bump2d']
all_nodes_list = shaders_list + node_list
counter = 0
number_of_shaders = len(shaders_list)
default_shadingEngine = 'aiStandardSurface*SG'
basePath = cmds.workspace(q = True, rd = True)
basePath = basePath + default_project_image_directory
i = 'test'
b = 'test'
runit = False
obj_shad_name = 'testt'
default_pano = "C:\Program Files\Allegorithmic\Substance Painter\\resources\shelf\\allegorithmic\environments\Exterior\Panorama.hdr"
ui = True # True or False if you want the ui window or not

if default_shader == arnold:
    default_shadingEngine = 'aiStandardSurface*SG'

if default_shader == blinn:
    default_shadingEngine = 'blinn*SG'
    
if default_shader == phong:
    default_shadingEngine = 'phong*SG'
    
if default_shader == redshift:
    default_shadingEngine = 'rsMaterial*SG'
    
if default_shader == lambert:
    default_shadingEngine = 'lambert*SG'

def color_space (): #Sets color space of images to raw and ignore cs rules on
    cmds.setAttr(i + '.ignoreColorSpaceFileRules', 1)
    cmds.setAttr(i + '.cs', 'Raw', type='string')

def color_func (a = '.color'):
    try:
        cmds.disconnectAttr(connected_1[0] +'.outColor', selected_shader + a) 
    except:
        pass
    finally:
        cmds.connectAttr(i + '.outColor' ,selected_shader + a)

def color_func2 (a = '.color'):
    try:
        connect_1 = cmds.listConnections(selected_shader2 + my_array[0])
        cmds.disconnectAttr(connect_1[0] +'.outColor', selected_shader2 + a) 
    except:
        pass
    finally:
        cmds.connectAttr(i + '.outColor' ,selected_shader2 + a)
        
def roughness_func(a = '.specularRoughness'):
    try:
        cmds.disconnectAttr(connected_2[0] +'.outAlpha', selected_shader + a) 
    except:
        pass
    finally:
        cmds.connectAttr(i + '.outAlpha' , selected_shader + a)
        color_space()  
        
def roughness_func2(a = '.specularRoughness'):
    try:
        cmds.disconnectAttr(connect_2[0] +'.outAlpha', selected_shader2 + a) 
    except:
        pass
    finally:
        cmds.connectAttr(i + '.outAlpha' , selected_shader2 + a)

        color_space()  
            
def metal_func(a = '.reflectivity'):
    try:
        cmds.disconnectAttr(connected_3[0] +'.outAlpha', selected_shader + a) 
    except:
        pass
    finally:
        cmds.connectAttr(i + '.outAlpha' , selected_shader + a)
        color_space()
        
def metal_func2(a = '.reflectivity'):
    try:
        cmds.disconnectAttr(connect_3[0] +'.outAlpha', selected_shader2 + a) 
    except:
        pass
    finally:
        cmds.connectAttr(i + '.outAlpha' , selected_shader2 + a)
        color_space()

def normal_func(a = '.normalCamera', b = 'bump2d'):
    bump = cmds.shadingNode(b, asUtility = True) 
    try:
        cmds.disconnectAttr(connected_4[0] +'.outNormal', selected_shader + a)
        cmds.delete(connected_4)[0]
    except:
        pass
    finally:
        cmds.connectAttr(i + '.outAlpha' ,  bump + '.bumpValue')
        cmds.connectAttr(bump + '.outNormal' , selected_shader + a)
        cmds.setAttr(bump + '.bumpDepth', bumpDepth_def)
        color_space()
        
def normal_func2(a = '.normalCamera', b = 'bump2d'):
    bump = cmds.shadingNode(b, asUtility = True) 
    try:
        cmds.disconnectAttr(connect_4[0] +'.outNormal', selected_shader2 + a)
        cmds.delete(connected_4)[0]
    except:
        pass
    finally:
        cmds.connectAttr(i + '.outAlpha' ,  bump + '.bumpValue')
        cmds.connectAttr(bump + '.outNormal' , selected_shader2 + a)
        cmds.setAttr(bump + '.bumpDepth', bumpDepth_def)
        color_space()

def rs_normal_func(a = '.bump_input'):
    bump2 = cmds.shadingNode('RedshiftNormalMap', asUtility = True)
    try:
        cmds.disconnectAttr(connected_4[0] +'.outDisplacementVector', selected_shader + a)
        cmds.disconnectAttr(connected_4[0] +'.outNormal', selected_shader + a)
    except:
        pass
    finally:
        fileNode = cmds.listConnections(i)
        currentFile = cmds.getAttr(i + ".fileTextureName" , fileNode[0])
        cmds.setAttr(bump2 + '.tex0', currentFile ,type="string")
        cmds.connectAttr(bump2 + '.outDisplacementVector', selected_shader + '.bump_input')
        
def rs_normal_func2(a = '.bump_input'):
    bump2 = cmds.shadingNode('RedshiftNormalMap', asUtility = True)
    try:
        cmds.disconnectAttr(connect_4[0] +'.outDisplacementVector', selected_shader2 + a)
        cmds.disconnectAttr(connect_4[0] +'.outNormal', selected_shader2 + a)
    except:
        pass
    finally:
        fileNode = cmds.listConnections(i)
        currentFile = cmds.getAttr(i + ".fileTextureName" , fileNode[0])
        cmds.setAttr(bump2 + '.tex0', currentFile ,type="string")
        cmds.connectAttr(bump2 + '.outDisplacementVector', selected_shader2 + '.bump_input')
        
def vr_normal_func(a = '.bumpMap'):
    try:
        cmds.disconnectAttr(connected_4[0] +'.outColor', selected_shader + a)
    except:
        pass
    finally:
        cmds.connectAttr(i + '.outColor' , selected_shader + a)
        color_space()
        
def vr_normal_func2(a = '.bumpMap'):
    try:
        cmds.disconnectAttr(connect_4[0] +'.outColor', selected_shader2 + a)
    except:
        pass
    finally:
        cmds.connectAttr(i + '.outColor' , selected_shader2 + a)
        color_space()
        
def scatter_func(a = '.subsurface'):
    try:
        cmds.disconnectAttr(connect_5[0] +'.outAlpha', selected_shader + a) 
    except:
        pass
    finally:
        cmds.connectAttr(i + '.outAlpha' , selected_shader + a)
        color_space()
        
def scatter_func2(a = '.subsurface'):
    try:
        cmds.disconnectAttr(connect_5[0] +'.outAlpha', selected_shader2 + a) 
    except:
        pass
    finally:
        cmds.connectAttr(i + '.outAlpha' , selected_shader2 + a)
        color_space()
        
def emissive_func(a = '.emissionColor'):
    try:
        cmds.disconnectAttr(connected_6[0] +'.outColor', selected_shader + a) 
    except:
        pass
    finally:
        cmds.connectAttr(i + '.outColor' , selected_shader + a)
#9 mfis        
def emissive_func2(a = '.emissionColor'):
    try:
        cmds.disconnectAttr(connect_6[0] +'.outColor', selected_shader2 + a) 
    except:
        pass
    finally:
        cmds.connectAttr(i + '.outColor' , selected_shader2 + a)
        
def ior_func(a = '.thinFilmIOR'):
    try:
        cmds.disconnectAttr(connected_7[0] +'.outAlpha', selected_shader + a) 
    except:
        pass
    finally:
        cmds.connectAttr(i + '.outAlpha' , selected_shader + a)
        color_space()
        
def ior_func2(a = '.thinFilmIOR'):
    try:
        cmds.disconnectAttr(connect_7[0] +'.outAlpha', selected_shader2 + a) 
    except:
        pass
    finally:
        cmds.connectAttr(i + '.outAlpha' , selected_shader2 + a)
        color_space()
        
def opacity_func(a = '.transparency'):
    try:
        cmds.disconnectAttr(connected_8[0] +'.outColor', selected_shader + a) 
    except:
        pass
    finally:
        cmds.connectAttr(i + '.outColor' , selected_shader + a)
        color_space()
        
def opacity_func2(a = '.transparency'):
    try:
        cmds.disconnectAttr(connect_8[0] +'.outColor', selected_shader2 + a) 
    except:
        pass 
    finally:
        cmds.connectAttr(i + '.outColor' , selected_shader2 + a)
        color_space()
        
def translucency_func2(a = '.translucency_func2'):
    try:
        cmds.disconnectAttr(connect_9[0] +'.outColor', selected_shader2 + a) 
    except:
        pass 
    finally:
        cmds.connectAttr(i + '.outColor' , selected_shader2 + a)
        color_space()
        
def delete_shader(a = arnold, b = '.baseColor'):
    if default_shader == a:
        if cmds.listConnections(selected_shader + b) == None:
            cmds.delete(selected_shader)
            cmds.delete(shadingEngine)
            
def arrays_func(a = 0):                                
    try:
        for i in dir_array[a]:
            dir_total.append(i)       
    except:
        pass
        
def shader_create_func():
    place2d = cmds.shadingNode('place2dTexture', asUtility = True)
    text_file = cmds.shadingNode('file', isColorManaged = True, asTexture = True, name = i[:-4])
    cmds.connectAttr(place2d +'.outUV', text_file + '.uvCoord')
    cmds.setAttr(text_file + '.fileTextureName', basePath + '/' + cut[0] + '/' + i, type = 'string')
    cmds.connectAttr(place2d +'.outUvFilterSize',text_file + '.uvFilterSize')
    connections = ['rotateUV','offset','noiseUV','vertexCameraOne','vertexUvThree','vertexUvTwo','vertexUvOne',
    'repeatUV','wrapV','wrapU','stagger','mirrorU','mirrorV','rotateFrame','translateFrame','coverage']
    for c in connections:
        cmds.connectAttr(place2d + '.' + c, text_file + '.' + c)
        
        
#UI Stuff
def project():
    global project_is_set
    project_is_set = True
    global basePath
    basePath = cmds.workspace(q = True, rd = True)
    basePath = basePath + default_project_image_directory
    
def filedirectory():
    global project_is_set
    project_is_set = False
    global basePath
    basePath = cmds.fileDialog2(fileMode=2, caption="Import Folder")[0]

def red():
    global default_shader
    default_shader = redshift

def arn():
    global default_shader
    default_shader = arnold
    
def lam():
    global default_shader
    default_shader = lambert
    
def pho():
    global default_shader
    default_shader = phong
    
def bli():
    global default_shader
    default_shader = blinn

def obj_match():
    global object_material_connect
    object_material_connect = True
    
def obj_no_match():
    global object_material_connect
    object_material_connect = False
    
def suffix_func():
    global runit
    runit = True
    
def Run_shader():
    if default_shader == arnold:
        default_shadingEngine = 'aiStandardSurface*SG'

    if default_shader == blinn:
        default_shadingEngine = 'blinn*SG'
        
    if default_shader == phong:
        default_shadingEngine = 'phong*SG'
        
    if default_shader == redshift:
        default_shadingEngine = 'rsMaterial*SG'
        
    if default_shader == lambert:
        default_shadingEngine = 'lambert*SG'
    
    global material_suffix
    material_suffix = '_mat'
    if runit == True:
        material_suffix = cmds.textField('suffix', query = True, text = True)
        if material_suffix == '':
            global material_suffix
            material_suffix = '_mat'
    directory = cmds.getFileList(folder = basePath)
    for i in directory:
        if '.png' in i or '.jpg' in i or '.jpeg' in i or '.tga' in i or '.tif' in i or 'raw' in i:
            if cmds.objExists(i[:-4]):
                pass
            else:
                place2d = cmds.shadingNode('place2dTexture', asUtility = True)
                text_file = cmds.shadingNode('file', isColorManaged = True, asTexture = True, name = i[:-4])
                cmds.connectAttr(place2d +'.outUV', text_file + '.uvCoord')
                cmds.setAttr(text_file + '.fileTextureName', basePath + '/' + i, type = 'string')
                cmds.connectAttr(place2d +'.outUvFilterSize',text_file + '.uvFilterSize')
                connections = ['rotateUV','offset','noiseUV','vertexCameraOne','vertexUvThree','vertexUvTwo','vertexUvOne',
                'repeatUV','wrapV','wrapU','stagger','mirrorU','mirrorV','rotateFrame','translateFrame','coverage']
                for c in connections:
                    cmds.connectAttr(place2d + '.' + c, text_file + '.' + c)
    
    global selected_shader
    selected_shader = cmds.shadingNode(default_shader, asShader = True)
    global shadingEngine
    shadingEngine = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
    cmds.connectAttr(selected_shader + '.outColor', shadingEngine + '.surfaceShader')
    global selected_shader2
    selected_shader2 = selected_shader
    
    arnold_shaders = cmds.ls(type = 'aiStandardSurface')
    blinn_shaders = cmds.ls(type = 'blinn')
    phong_shaders = cmds.ls(type = 'phong')
    lambert_shaders = cmds.ls(type = 'lambert')
    redshift_shaders = cmds.ls(type = 'RedshiftMaterial')
    #Arnold
    if cmds.nodeType(selected_shader) == 'aiStandardSurface':
        my_array = ['.baseColor','.specularRoughness','.metalness','.normalCamera',
        '.subsurface', '.emissionColor', '.thinFilmIOR', '.opacity']
        global connected_1
        connected_1 = cmds.listConnections(selected_shader + my_array[0])
        global connected_2
        connected_2 = cmds.listConnections(selected_shader + my_array[1])
        global connected_3
        connected_3 = cmds.listConnections(selected_shader + my_array[2])
        global connected_4
        connected_4 = cmds.listConnections(selected_shader + my_array[3])
        global connected_5
        connected_5 = cmds.listConnections(selected_shader + my_array[4])
        global connected_6
        connected_6 = cmds.listConnections(selected_shader + my_array[5])
        global connected_7
        connected_7 = cmds.listConnections(selected_shader + my_array[6])
        global connected_8
        connected_8 = cmds.listConnections(selected_shader + my_array[7])
        global connect_1
        connect_1 = cmds.listConnections(selected_shader2 + my_array[0])
        global connect_2
        connect_2 = cmds.listConnections(selected_shader2 + my_array[1])
        global connect_3
        connect_3 = cmds.listConnections(selected_shader2 + my_array[2])
        global connect_4
        connect_4 = cmds.listConnections(selected_shader2 + my_array[3])
        global connect_5
        connect_5 = cmds.listConnections(selected_shader2 + my_array[4])
        global connect_6
        connect_6 = cmds.listConnections(selected_shader2 + my_array[5])
        global connect_7
        connect_7 = cmds.listConnections(selected_shader2 + my_array[6])
        global connect_8
        connect_8 = cmds.listConnections(selected_shader2 + my_array[7])
        
        
        names = cmds.ls(type = 'file')
        if default_shader == arnold:
            global i
            for i in names:
                if color_text in i or color_text.lower() in i: 
                    if color_text in i:
                        cut = i.partition( '_Base' + color_text)
                    elif color_text.lower() in i:
                        cut = i.partition( '_base' + color_text.lower())
                    same_name = False
                    arnold_shaders = cmds.ls(type = 'aiStandardSurface')
                    global b
                    for b in arnold_shaders:
                        if cut[0] in b:
                            global selected_shader2
                            selected_shader2 = b
                            connect_1
                            same_name = True
                            if not cmds.listConnections('{0}.baseColor'.format(b)):
                                color_func2('.baseColor')        
                    if same_name == False:
                        if material_suffix in cut[0]:
                            global obj_shad_name
                            obj_shad_name = cut[0] 
                        else:
                            obj_shad_name = cut[0] + material_suffix
                        
                        selected_shader2 = cmds.shadingNode(arnold, asShader = True, name = obj_shad_name)
                        if cut[0] in selected_shader2:
                            extra = cmds.listConnections(selected_shader2 + '.outColor')
                            shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                            cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                            color_func2('.baseColor')
                
                if color_alt_text in i or color_alt_text.lower() in i:           
                    if color_alt_text in i:
                        cut = i.partition( '_' + color_alt_text)
                    elif color_alt_text.lower() in i:
                        cut = i.partition( '_' + color_alt_text.lower())
                    same_name = False
                    global b
                    for b in arnold_shaders:
                        if cut[0] in b:
                            global selected_shader2
                            selected_shader2 = b
                            connect_1
                            same_name = True
                            if not cmds.listConnections('{0}.baseColor'.format(b)):
                                color_func2('.baseColor')
                    if same_name == False:
                        if material_suffix in cut[0]:
                            global obj_shad_name
                            obj_shad_name = cut[0]
                        else:
                            obj_shad_name = cut[0] + material_suffix
                        selected_shader2 = cmds.shadingNode(arnold, asShader = True, name = obj_shad_name)
                        if cut[0] in selected_shader2:
                            extra = cmds.listConnections(selected_shader2 + '.outColor')
                            shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                            cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                            color_func2('.baseColor')
                
                if color_alt2_text in i or color_alt2_text.lower() in i:           
                    if color_alt2_text in i:
                        cut = i.partition( '_' + color_alt2_text)
                    elif color_alt2_text.lower() in i:
                        cut = i.partition( '_' + color_alt2_text.lower())
                    same_name = False
                    global b
                    for b in arnold_shaders:
                        if cut[0] in b:
                            global selected_shader2
                            selected_shader2 = b
                            connect_1
                            same_name = True
                            if not cmds.listConnections('{0}.baseColor'.format(b)):
                                color_func2('.baseColor')
                    if same_name == False:
                        if material_suffix in cut[0]:
                            global obj_shad_name
                            obj_shad_name = cut[0]
                        else:
                            obj_shad_name = cut[0] + material_suffix
                        selected_shader2 = cmds.shadingNode(arnold, asShader = True, name = obj_shad_name)
                        if cut[0] in selected_shader2:
                            extra = cmds.listConnections(selected_shader2 + '.outColor')
                            shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                            cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                            color_func2('.baseColor')
                        
                if roughness_text in i or roughness_text.lower() in i: 
                    if roughness_text in i:
                        cut = i.partition( '_' + roughness_text)
                    elif roughness_text.lower() in i:
                        cut = i.partition( '_' + roughness_text.lower())
                    same_name = False
                    for b in arnold_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_2
                            same_name = True
                            if not cmds.listConnections('{0}.specularRoughness'.format(b)):
                                roughness_func2()
                    if same_name == False:
                        roughness_func2()
                        
                if roughness_alt_text in i or roughness_alt_text.lower() in i: 
                    if roughness_alt_text in i:
                        cut = i.partition( '_' + roughness_alt_text)
                    elif roughness_alt_text.lower() in i:
                        cut = i.partition( '_' + roughness_alt_text.lower())
                    same_name = False
                    for b in arnold_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_2
                            same_name = True
                            if not cmds.listConnections('{0}.specularRoughness'.format(b)):
                                roughness_func2()
                    if same_name == False:
                        roughness_func2()
                    
                if metal_text in i or metal_text.lower() in i: 
                    if metal_text in i:
                        cut = i.partition( '_' + metal_text)
                    elif metal_text.lower() in i:
                        cut = i.partition( '_' + metal_text.lower())
                    same_name = False
                    for b in arnold_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_3
                            same_name = True
                            if not cmds.listConnections('{0}.metalness'.format(b)):
                                metal_func2('.metalness')
                    if same_name == False:
                        metal_func2('.metalness')
                        
                if metal_alt_text in i or metal_alt_text.lower() in i: 
                    if metal_alt_text in i:
                        cut = i.partition( '_' + metal_alt_text)
                    elif metal_alt_text.lower() in i:
                        cut = i.partition( '_' + metal_alt_text.lower())
                    same_name = False
                    for b in arnold_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_3
                            same_name = True
                            if not cmds.listConnections('{0}.metalness'.format(b)):
                                metal_func2('.metalness')
                    if same_name == False:
                        metal_func2('.metalness')
                  
                if normal_text in i or normal_text.lower() in i: 
                    if normal_text in i:
                        cut = i.partition( '_' + normal_text)
                    elif normal_text.lower() in i:
                        cut = i.partition( '_' + normal_text.lower())
                    same_name = False
                    for b in arnold_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_4
                            same_name = True
                            if not cmds.listConnections('{0}.normalCamera'.format(b)):
                                normal_func2()
                    if same_name == False:
                        normal_func2()  
                
                if scatter_text in i or scatter_text.lower() in i: 
                    if scatter_text in i:
                        cut = i.partition( '_' + scatter_text)
                    elif scatter_text.lower() in i:
                        cut = i.partition( '_' + scatter_text.lower())
                    same_name = False
                    for b in arnold_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_5
                            same_name = True
                            if not cmds.listConnections('{0}.subsurface'.format(b)):
                                scatter_func2('.subsurface')
                    if same_name == False:
                        scatter_func2('.subsurface')
                         
                if emissive_text in i or emissive_text.lower() in i: 
                    if emissive_text in i:
                        cut = i.partition( '_' + emissive_text)
                    elif emissive_text.lower() in i:
                        cut = i.partition( '_' + emissive_text.lower())
                    same_name = False
                    for b in arnold_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_6
                            same_name = True
                            if not cmds.listConnections('{0}.emissionColor'.format(b)):
                                emissive_func2('.emissionColor')
                    if same_name == False:
                        emissive_func2('.emissionColor')
                   
                if ior_text in i or ior_text.lower() in i: 
                    if ior_text in i:
                        cut = i.partition( '_' + ior_text)
                    elif ior_text.lower() in i:
                        cut = i.partition( '_' + ior_text.lower())
                    same_name = False
                    for b in arnold_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_7
                            same_name = True
                            if not cmds.listConnections('{0}.specularIOR'.format(b)):
                                ior_func2('.specularIOR')
                    if same_name == False:
                        ior_func2('.specularIOR')

                if opacity_text in i or opacity_text.lower() in i: 
                    if opacity_text in i:
                        cut = i.partition( '_' + opacity_text)
                    elif opacity_text.lower() in i:
                        cut = i.partition( '_' + opacity_text.lower())
                    same_name = False
                    for b in arnold_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_8
                            same_name = True
                            if not cmds.listConnections('{0}.opacity'.format(b)):
                                opacity_func2('.opacity')
                    if same_name == False:
                        opacity_func2('.opacity') 
                        
                if opacity_alt_text in i or opacity_alt_text.lower() in i: 
                    if opacity_alt_text in i:
                        cut = i.partition( '_' + opacity_alt_text)
                    elif opacity_alt_text.lower() in i:
                        cut = i.partition( '_' + opacity_alt_text.lower())
                    same_name = False
                    for b in arnold_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_8
                            same_name = True
                            if not cmds.listConnections('{0}.opacity'.format(b)):
                                opacity_func2('.opacity')
                    if same_name == False:
                        opacity_func2('.opacity') 
                        
                        
    #Blinn
    elif cmds.nodeType(selected_shader) == 'blinn':
        my_array = ['.baseColor','.specularRoughness','.metalness','.normalCamera',
        '.subsurface', '.emissionColor', '.thinFilmIOR', '.opacity']
        my_array[0] = '.color'
        my_array[2] = '.reflectivity'
        my_array[7] = '.transparency'
        global connected_1
        connected_1 = cmds.listConnections(selected_shader + my_array[0])
        global connected_3
        connected_3 = cmds.listConnections(selected_shader + my_array[2])
        global connected_4
        connected_4 = cmds.listConnections(selected_shader + my_array[3])
        global connected_8
        connected_8 = cmds.listConnections(selected_shader + my_array[7])
        global connect_1
        connect_1 = cmds.listConnections(selected_shader2 + my_array[0])
        global connect_3
        connect_3 = cmds.listConnections(selected_shader2 + my_array[2])
        global connect_4
        connect_4 = cmds.listConnections(selected_shader2 + my_array[3])
        global connect_8
        connect_8 = cmds.listConnections(selected_shader2 + my_array[7])
        names = cmds.ls( type = 'file')
        if default_shader == blinn:
            global i
            for i in names:
                if color_text in i:
                    cut = i.partition('_Base_' + color_text)
                    same_name = False
                    for b in blinn_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_1
                            same_name = True
                            color_func2()
                    if same_name == False:
                        if material_suffix in cut[0]:
                            obj_shad_name = cut[0]
                        else:
                            obj_shad_name = cut[0] + material_suffix
                        selected_shader2 = cmds.shadingNode(blinn, asShader = True, name = obj_shad_name)
                        if cut[0] in selected_shader2:
                            extra = cmds.listConnections(selected_shader2 + '.outColor')
                            shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                            cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                            color_func2()   
                if color_alt_text in i:
                    cut = i.partition('_' + color_alt_text)
                    same_name = False
                    for b in blinn_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_1
                            same_name = True
                            color_func2()
                    if same_name == False:
                        if material_suffix in cut[0]:
                            obj_shad_name = cut[0]
                        else:
                            obj_shad_name = cut[0] + material_suffix
                        selected_shader2 = cmds.shadingNode(blinn, asShader = True, name = obj_shad_name)
                        if cut[0] in selected_shader2:
                            extra = cmds.listConnections(selected_shader2 + '.outColor')
                            shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                            cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                            color_func2() 
                            
                if metal_text in i:
                    cut = i.partition('_' + metal_text)
                    same_name = False
                    for b in blinn_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_3
                            same_name = True
                            metal_func2()
                    if same_name == False:
                        metal_func2()    
                        
                if metal_alt_text in i:
                    cut = i.partition('_' + metal_alt_text)
                    same_name = False
                    for b in blinn_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_3
                            same_name = True
                            metal_func2()
                    if same_name == False:
                        metal_func2()   
                        
                if normal_text in i:
                    cut = i.partition('_' + normal_text)
                    same_name = False
                    for b in blinn_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_4
                            same_name = True
                            normal_func2()
                    if same_name == False:
                        normal_func2()   
                        
                if opacity_text in i:
                    cut = i.partition('_' + opacity_text)
                    same_name = False
                    for b in blinn_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_8
                            same_name = True
                            opacity_func2()
                    if same_name == False:
                        opacity_func2()   
                
                if 'opacity' in i:
                    cut = i.partition('_opacity')
                    same_name = False
                    for b in blinn_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_8
                            same_name = True
                            opacity_func2()
                    if same_name == False:
                        opacity_func2()    
                     

    #Phong
    elif cmds.nodeType(selected_shader) == 'phong':
        my_array = ['.baseColor','.specularRoughness','.metalness','.normalCamera',
        '.subsurface', '.emissionColor', '.thinFilmIOR', '.opacity']
        my_array[0] = '.color'
        my_array[2] = '.reflectivity'
        my_array[7] = '.transparency'
        global connected_1
        connected_1 = cmds.listConnections(selected_shader + my_array[0])
        global connected_3
        connected_3 = cmds.listConnections(selected_shader + my_array[2])
        global connected_4
        connected_4 = cmds.listConnections(selected_shader + my_array[3])
        global connected_8
        connected_8 = cmds.listConnections(selected_shader + my_array[7])
        global connect_1
        connect_1 = cmds.listConnections(selected_shader2 + my_array[0])
        global connect_3
        connect_3 = cmds.listConnections(selected_shader2 + my_array[2])
        global connect_4
        connect_4 = cmds.listConnections(selected_shader2 + my_array[3])
        global connect_8
        connect_8 = cmds.listConnections(selected_shader2 + my_array[7])
        
        names = cmds.ls(type = 'file')
        if default_shader == phong:
            global i
            for i in names:
                if color_text in i:
                    cut = i.partition('_Base_' + color_text)
                    same_name = False
                    for b in phong_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_1
                            same_name = True
                            color_func2()
                    if same_name == False:
                        if material_suffix in cut[0]:
                            obj_shad_name = cut[0]
                        else:
                            obj_shad_name = cut[0] + material_suffix
                        selected_shader2 = cmds.shadingNode(phong, asShader = True, name = obj_shad_name)
                        if cut[0] in selected_shader2:
                            extra = cmds.listConnections(selected_shader2 + '.outColor')
                            shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                            cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                            color_func2()   
                            
                if color_alt_text in i:
                    cut = i.partition('_' + color_alt_text)
                    same_name = False
                    for b in phong_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_1
                            same_name = True
                            color_func2()
                    if same_name == False:
                        if material_suffix in cut[0]:
                            obj_shad_name = cut[0]
                        else:
                            obj_shad_name = cut[0] + material_suffix
                        selected_shader2 = cmds.shadingNode(phong, asShader = True, name = obj_shad_name)
                        if cut[0] in selected_shader2:
                            extra = cmds.listConnections(selected_shader2 + '.outColor')
                            shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                            cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                            color_func2() 
                            
                if metal_text in i:
                    cut = i.partition('_' + metal_text)
                    same_name = False
                    for b in phong_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_3
                            same_name = True
                            metal_func2()
                    if same_name == False:
                        metal_func2()     
                        
                if metal_alt_text in i:
                    cut = i.partition('_' + metal_alt_text)
                    same_name = False
                    for b in phong_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_3
                            same_name = True
                            metal_func2()
                    if same_name == False:
                        metal_func2()    
                        
                if normal_text in i:
                    cut = i.partition('_' + normal_text)
                    same_name = False
                    for b in phong_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_4
                            same_name = True
                            normal_func2()
                    if same_name == False:
                        normal_func2()   
                        
                if opacity_text in i :
                    cut = i.partition('_' + opacity_text)
                    same_name = False
                    for b in phong_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_8
                            same_name = True
                            opacity_func2()
                    if same_name == False:
                        opacity_func2() 
                        
                if 'opacity' in i:
                    cut = i.partition('_opacity')
                    same_name = False
                    for b in phong_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_8
                            same_name = True
                            opacity_func2()
                    if same_name == False:
                        opacity_func2()        
    #RedshiftMaterial
    elif cmds.nodeType(selected_shader) == 'RedshiftMaterial':
        my_array = ['.diffuse_color','.refl_roughness','.refl_metalness','.bump_input',
        '.ms_amount', '.emission_color', '.refl_ior', '.opacity_color', '.transl_color']
        global connected_1
        connected_1 = cmds.listConnections(selected_shader + my_array[0])
        global connected_2
        connected_2 = cmds.listConnections(selected_shader + my_array[1])
        global connected_3
        connected_3 = cmds.listConnections(selected_shader + my_array[2])
        global connected_4
        connected_4 = cmds.listConnections(selected_shader + my_array[3])
        global connected_5
        connected_5 = cmds.listConnections(selected_shader + my_array[4])
        global connected_6
        connected_6 = cmds.listConnections(selected_shader + my_array[5])
        global connected_7
        connected_7 = cmds.listConnections(selected_shader + my_array[6])
        global connected_8
        connected_8 = cmds.listConnections(selected_shader + my_array[7])
        global connect_1
        connect_1 = cmds.listConnections(selected_shader2 + my_array[0])
        global connect_2
        connect_2 = cmds.listConnections(selected_shader2 + my_array[1])
        global connect_3
        connect_3 = cmds.listConnections(selected_shader2 + my_array[2])
        global connect_4
        connect_4 = cmds.listConnections(selected_shader2 + my_array[3])
        global connect_5
        connect_5 = cmds.listConnections(selected_shader2 + my_array[4])
        global connect_6
        connect_6 = cmds.listConnections(selected_shader2 + my_array[5])
        global connect_7
        connect_7 = cmds.listConnections(selected_shader2 + my_array[6])
        global connect_8
        connect_8 = cmds.listConnections(selected_shader2 + my_array[7])
        global connect_9
        connect_9 = cmds.listConnections(selected_shader2 + my_array[8])
        
        names = cmds.ls( type = 'file')
        
        if default_shader == redshift:
            global i
            for i in names:
                if color_text in i or color_text.lower() in i: #Roughness
                    if color_text in i:
                        cut = i.partition( '_Base' + color_text)
                    elif color_text.lower() in i:
                        cut = i.partition( '_base' + color_text.lower())
                    same_name = False
                    for b in redshift_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_1
                            global same_name
                            same_name = True
                            if not cmds.listConnections('{0}.diffuse_color'.format(b)):
                                color_func2('.diffuse_color')
                            cmds.setAttr(selected_shader2 + '.refl_brdf', default_BRDF)
                    if same_name == False:
                        if material_suffix in cut[0]:
                            obj_shad_name = cut[0]
                        else:
                            obj_shad_name = cut[0] + material_suffix
                        selected_shader2 = cmds.shadingNode(redshift, asShader = True, name = obj_shad_name)
                        if cut[0] in selected_shader2:
                            extra = cmds.listConnections(selected_shader2 + '.outColor')
                            shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                            cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                            color_func2('.diffuse_color')      
                            cmds.setAttr(selected_shader2 + '.refl_brdf', default_BRDF)
                            
                if color_alt_text in i or color_alt_text.lower() in i: #Roughness
                    if color_alt_text in i:
                        cut = i.partition( '_' + color_alt_text)
                    elif color_alt_text.lower() in i:
                        cut = i.partition( '_' + color_alt_text.lower())
                    same_name = False
                    for b in redshift_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_1
                            same_name = True
                            if not cmds.listConnections('{0}.diffuse_color'.format(b)):
                                color_func2('.diffuse_color')
                            cmds.setAttr(selected_shader2 + '.refl_brdf', default_BRDF)
                    if same_name == False:
                        if material_suffix in cut[0]:
                            obj_shad_name = cut[0]
                        else:
                            obj_shad_name = cut[0] + material_suffix
                        selected_shader2 = cmds.shadingNode(redshift, asShader = True, name = obj_shad_name)
                        if cut[0] in selected_shader2:
                            extra = cmds.listConnections(selected_shader2 + '.outColor')
                            shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                            cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                            color_func2('.diffuse_color')  
                            cmds.setAttr(selected_shader2 + '.refl_brdf', default_BRDF)           
                            
                if color_alt2_text in i or color_alt2_text.lower() in i: #Roughness
                    if color_alt2_text in i:
                        cut = i.partition( '_' + color_alt2_text)
                    elif color_alt2_text.lower() in i:
                        cut = i.partition( '_' + color_alt2_text.lower())
                    same_name = False
                    for b in redshift_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_1
                            same_name = True
                            if not cmds.listConnections('{0}.diffuse_color'.format(b)):
                                color_func2('.diffuse_color')
                            cmds.setAttr(selected_shader2 + '.refl_brdf', default_BRDF)
                    if same_name == False:
                        if material_suffix in cut[0]:
                            obj_shad_name = cut[0]
                        else:
                            obj_shad_name = cut[0] + material_suffix
                        selected_shader2 = cmds.shadingNode(redshift, asShader = True, name = obj_shad_name)
                        if cut[0] in selected_shader2:
                            extra = cmds.listConnections(selected_shader2 + '.outColor')
                            shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                            cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                            color_func2('.diffuse_color')  
                            cmds.setAttr(selected_shader2 + '.refl_brdf', default_BRDF)                                
                        
                if roughness_text in i or roughness_text.lower() in i: #Roughness
                    if roughness_text in i:
                        cut = i.partition( '_' + roughness_text)
                    elif roughness_text.lower() in i:
                        cut = i.partition( '_' + roughness_text.lower())
                    same_name = False
                    for b in redshift_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_2
                            same_name = True
                            if not cmds.listConnections('{0}.refl_roughness'.format(b)):
                                roughness_func2('.refl_roughness')
                    if same_name == False:
                        roughness_func2('.refl_roughness')
                        
                if roughness_alt_text in i or roughness_alt_text.lower() in i:
                    if roughness_alt_text in i:
                        cut = i.partition( '_' + roughness_alt_text)
                    elif roughness_alt_text.lower() in i:
                        cut = i.partition( '_' + roughness_alt_text.lower())
                    same_name = False
                    for b in redshift_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_2
                            same_name = True
                            if not cmds.listConnections('{0}.refl_roughness'.format(b)):
                                roughness_func2('.refl_roughness')
                    if same_name == False:
                        roughness_func2('.refl_roughness')
                        
                if metal_text in i or metal_text.lower() in i:
                    if metal_text in i:
                        cut = i.partition( '_' + metal_text)
                    elif metal_text.lower() in i:
                        cut = i.partition( '_' + metal_text.lower())
                    same_name = False
                    for b in redshift_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_3
                            same_name = True
                            if not cmds.listConnections('{0}.refl_metalness'.format(b)):
                                metal_func2('.refl_metalness')
                            cmds.setAttr(selected_shader2 + '.refl_fresnel_mode', 2)
                    if same_name == False:
                        metal_func2('.refl_metalness')
                        cmds.setAttr(selected_shader2 + '.refl_fresnel_mode', 2)
                        
                if metal_alt_text in i or metal_alt_text.lower() in i:
                    if metal_alt_text in i:
                        cut = i.partition( '_' + metal_alt_text)
                    elif metal_alt_text.lower() in i:
                        cut = i.partition( '_' + metal_alt_text.lower())
                    same_name = False
                    for b in redshift_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_3
                            same_name = True
                            if not cmds.listConnections('{0}.refl_metalness'.format(b)):
                                metal_func2('.refl_metalness')
                            cmds.setAttr(selected_shader2 + '.refl_fresnel_mode', 2)
                    if same_name == False:
                        metal_func2('.refl_metalness')
                        cmds.setAttr(selected_shader2 + '.refl_fresnel_mode', 2)
                    
                if normal_text in i or normal_text.lower() in i:
                    if normal_text in i:
                        cut = i.partition( '_' + normal_text)
                    elif normal_text.lower() in i:
                        cut = i.partition( '_' + normal_text.lower())
                    same_name = False
                    for b in redshift_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_4
                            same_name = True
                            if not cmds.listConnections('{0}.bump_input'.format(b)):
                                rs_normal_func2()
                    if same_name == False:
                        rs_normal_func2() 
                     
                if scatter_text in i or scatter_text.lower() in i:
                    if scatter_text in i:
                        cut = i.partition( '_' + scatter_text)
                    elif scatter_text.lower() in i:
                        cut = i.partition( '_' + scatter_text.lower())
                    same_name = False
                    for b in redshift_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_5
                            same_name = True
                            if not cmds.listConnections('{0}.ms_amount'.format(b)):
                                scatter_func2('.ms_amount')
                    if same_name == False:
                        scatter_func2('.ms_amount')
                         
                if emissive_text in i or emissive_text.lower() in i:
                    if emissive_text in i:
                        cut = i.partition( '_' + emissive_text)
                    elif emissive_text.lower() in i:
                        cut = i.partition( '_' + emissive_text.lower())
                    same_name = False
                    for b in redshift_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_6
                            same_name = True
                            if not cmds.listConnections('{0}.emission_color'.format(b)):
                                emissive_func2('.emission_color')
                            
                    if same_name == False:
                        emissive_func2('.emission_color')
                    
                if ior_text in i or ior_text.lower() in i:
                    if ior_text in i:
                        cut = i.partition( '_' + ior_text)
                    elif ior_text.lower() in i:
                        cut = i.partition( '_' + ior_text.lower())
                    same_name = False
                    for b in redshift_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_7
                            same_name = True
                            if not cmds.listConnections('{0}.refl_ior'.format(b)):
                                ior_func2('.refl_ior')
                    if same_name == False:
                        ior_func2('.refl_ior')
                        
                if opacity_text in i or opacity_text.lower() in i:
                    if opacity_text in i:
                        cut = i.partition( '_' + opacity_text)
                    elif opacity_text.lower() in i:
                        cut = i.partition( '_' + opacity_text.lower())
                    same_name = False
                    for b in redshift_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_8
                            same_name = True
                            if not cmds.listConnections('{0}.opacity_color'.format(b)):
                                opacity_func2('.opacity_color')
                    if same_name == False:
                        opacity_func2('.opacity_color') 
                        
                if opacity_alt_text in i or opacity_alt_text.lower() in i:
                    if opacity_alt_text in i:
                        cut = i.partition( '_' + opacity_alt_text)
                    elif opacity_alt_text.lower() in i:
                        cut = i.partition( '_' + opacity_alt_text.lower())
                    same_name = False
                    for b in redshift_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_8
                            same_name = True
                            if not cmds.listConnections('{0}.opacity_color'.format(b)):
                                opacity_func2('.opacity_color')
                    if same_name == False:
                        opacity_func2('.opacity_color') 
                        
                if translucency_text in i or translucency_text.lower() in i:
                    if translucency_text in i:
                        cut = i.partition( '_' + translucency_text)
                    elif translucency_text.lower() in i:
                        cut = i.partition( '_' + translucency_text.lower())
                    same_name = False
                    for b in redshift_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_8
                            same_name = True
                            if not cmds.listConnections('{0}.transl_color'.format(b)):
                                translucency_func2('.transl_color')
                    if same_name == False:
                        translucency_func2('.transl_color') 
                        
    #lambert 
    elif cmds.nodeType(selected_shader) == 'lambert':
        my_array = ['.baseColor','.specularRoughness','.metalness','.normalCamera',
        '.subsurface', '.emissionColor', '.thinFilmIOR', '.opacity']
        my_array[0] = '.color'
        my_array[7] = '.transparency'
        global connected_1
        connected_1 = cmds.listConnections(selected_shader + my_array[0])
        global connected_4
        connected_4 = cmds.listConnections(selected_shader + my_array[3])
        global connected_8
        connected_8 = cmds.listConnections(selected_shader + my_array[7])
        global connect_1
        connect_1 = cmds.listConnections(selected_shader2 + my_array[0])
        global connect_4
        connect_4 = cmds.listConnections(selected_shader2 + my_array[3])
        global connect_8
        connect_8 = cmds.listConnections(selected_shader2 + my_array[7])
        names = cmds.ls( type = 'file')
        if default_shader == lambert:
            global i
            for i in names:
                if color_text in i:
                    cut = i.partition('_Base_' + color_text)
                    same_name = False
                    for b in lambert_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_1
                            same_name = True
                            color_func2()
                    if same_name == False:
                        if material_suffix in cut[0]:
                            obj_shad_name = cut[0]
                        else:
                            obj_shad_name = cut[0] + material_suffix
                        global selected_shader2
                        selected_shader2 = cmds.shadingNode(lambert, asShader = True, name = obj_shad_name)
                        if cut[0] in selected_shader2:
                            extra = cmds.listConnections(selected_shader2 + '.outColor')
                            shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                            cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                            color_func2()     
                            
                if color_alt_text in i:
                    cut = i.partition('_' + color_alt_text)
                    same_name = False
                    for b in lambert_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_1
                            same_name = True
                            color_func2()
                    if same_name == False:
                        if material_suffix in cut[0]:
                            obj_shad_name = cut[0]
                        else:
                            obj_shad_name = cut[0] + material_suffix
                        selected_shader2 = cmds.shadingNode(lambert, asShader = True, name = obj_shad_name)
                        if cut[0] in selected_shader2:
                            extra = cmds.listConnections(selected_shader2 + '.outColor')
                            shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                            cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                            color_func2()     
                        
                if normal_text in i:
                    cut = i.partition('_' + normal_text)
                    same_name = False
                    for b in lambert_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_4
                            same_name = True
                            normal_func2()
                    if same_name == False:
                        normal_func2()   
                        
                if opacity_text in i:
                    cut = i.partition('_' + opacity_text)
                    same_name = False
                    for b in lambert_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_8
                            same_name = True
                            opacity_func2()
                    if same_name == False:
                        opacity_func2()        
                        
                if 'opacity' in i:
                    cut = i.partition('_opacity')
                    same_name = False
                    for b in lambert_shaders:
                        if cut[0] in b:
                            selected_shader2 = b
                            connect_8
                            same_name = True
                            opacity_func2()
                    if same_name == False:
                        opacity_func2()     
    # Deletes any materials without incoming color connection               
    counter = 0   
    global counter                      
    while counter < number_of_shaders:
        delete_shader(shaders_list[counter], shaders_color_list[counter])
        counter = counter + 1
            
    # assigns objects with the same name as the materials created.   
    arnold_final_shaders = cmds.ls(type = arnold)
    blinn_final_shaders = cmds.ls(type = blinn)
    phong_final_shaders = cmds.ls(type = phong)
    redshift_final_shaders = cmds.ls(type = redshift)
    lambert_final_shaders = cmds.ls(type = lambert)
    
    object_suf_len = len(object_suffix)
    object_names = cmds.ls(type = 'transform')
    shader_arnold_len = len(arnold_final_shaders)
    shader_blinn_len = len(blinn_final_shaders)
    shader_phong_len = len(phong_final_shaders)
    shader_redshift_len = len(redshift_final_shaders)
    shader_lambert_len = len(lambert_final_shaders)
    
    var = 0
    if object_material_connect == True:
        if default_shader == arnold:
            while var < shader_arnold_len:
                for b in object_names:
                    c = arnold_final_shaders[var]
                    d = c.partition(material_suffix)[0]
                    if d in b:
                        test = cmds.listConnections((arnold_final_shaders[var]) + '.outColor')[0]
                        cmds.select(b)
                        check = cmds.sets(e = True, forceElement = test)      
                var = var + 1  
               
        elif default_shader == blinn:
            while var < shader_blinn_len:
                for b in object_names:
                    c = blinn_final_shaders[var]
                    d = c.partition(material_suffix)[0]
                    if d in b:
                        test = cmds.listConnections((blinn_final_shaders[var]) + '.outColor')[0]
                        cmds.select(b)
                        check = cmds.sets(e = True, forceElement = test)    
                var = var + 1  
       
        elif default_shader == phong:
            while var < shader_phong_len:
                for b in object_names:
                    c = phong_final_shaders[var]
                    d = c.partition(material_suffix)[0]
                    if d in b:
                        test = cmds.listConnections((phong_final_shaders[var]) + '.outColor')[0]
                        cmds.select(b)
                        check = cmds.sets(e = True, forceElement = test)  
                var = var + 1  
                
        elif default_shader == redshift:
            while var < shader_redshift_len:
                for b in object_names:
                    c = redshift_final_shaders[var]
                    d = c.partition(material_suffix)[0]
                    x = b.lower()
                    y = d.lower()
                    if y in x:
                        test = cmds.listConnections((redshift_final_shaders[var]) + '.outColor')[0]
                        cmds.select(b)
                        check = cmds.sets(e = True, forceElement = test)  
                var = var + 1  
                
        elif default_shader == lambert:
            while var < shader_lambert_len:
                for b in object_names:
                    c = lambert_final_shaders[var]
                    d = c.partition(material_suffix)[0]
                    if d in b:
                        test = cmds.listConnections((lambert_final_shaders[var]) + '.outColor')[0]
                        cmds.select(b)
                        check = cmds.sets(e = True, forceElement = test)
                var = var + 1                 
            
def Selected():
    if cmds.ls(selection = True, type = 'file'): #If a texture file is selected
        #Arnold
        if cmds.ls(selection = True, type = 'aiStandardSurface'):#If arnold is selected
            global selected_shader
            selected_shader = cmds.ls(selection = True, type = 'aiStandardSurface')[0]
            my_array = ['.baseColor','.specularRoughness','.metalness','.normalCamera',
            '.subsurface', '.emissionColor', '.thinFilmIOR', '.opacity']
            global connected_1
            connected_1 = cmds.listConnections(selected_shader + my_array[0])
            global connected_2
            connected_2 = cmds.listConnections(selected_shader + my_array[1])
            global connected_3
            connected_3 = cmds.listConnections(selected_shader + my_array[2])
            global connected_4
            connected_4 = cmds.listConnections(selected_shader + my_array[3])
            global connected_5
            connected_5 = cmds.listConnections(selected_shader + my_array[4])
            global connected_6
            connected_6 = cmds.listConnections(selected_shader + my_array[5])
            global connected_7
            connected_7 = cmds.listConnections(selected_shader + my_array[6])
            global connected_8
            connected_8 = cmds.listConnections(selected_shader + my_array[7])
            
            names = cmds.ls(selection = True, type = 'file')
            global i
            for i in names:
                if color_text in i or color_alt_text in i:
                    color_func('.baseColor')
                if roughness_text in i or roughness_alt_text in i:
                    roughness_func()
                if metal_text in i or metal_alt_text in i:
                    metal_func('.metalness')
                if normal_text in i:
                    normal_func()  
                if scatter_text in i:
                    scatter_func('.subsurface')
                if emissive_text in i:
                    emissive_func('.emissionColor')
                if ior_text in i or 'Ior' in i or 'IOR' in i:
                    ior_func('.specularIOR')
                if opacity_text in i or 'opacity' in i:
                    opacity_func('.opacity') 
        #Blinn
        elif cmds.ls(selection = True, type = 'blinn'):
            global selected_shader
            selected_shader = cmds.ls(selection = True, type = 'blinn')[0]
            my_array = ['.baseColor','.specularRoughness','.metalness','.normalCamera',
            '.subsurface', '.emissionColor', '.thinFilmIOR', '.opacity']
            my_array[0] = '.color'
            my_array[2] = '.reflectivity'
            my_array[7] = '.transparency'
            global connected_1
            connected_1 = cmds.listConnections(selected_shader + my_array[0])
            global connected_3
            connected_3 = cmds.listConnections(selected_shader + my_array[2])
            global connected_4
            connected_4 = cmds.listConnections(selected_shader + my_array[3])
            global connected_8
            connected_8 = cmds.listConnections(selected_shader + my_array[7])
            names = cmds.ls(selection = True, type = 'file')
            global i
            for i in names:
                if color_text in i or color_alt_text in i:
                    color_func()
                if metal_text in i or metal_alt_text in i:
                    metal_func()
                if normal_text in i:
                    normal_func()  
                if opacity_text in i or 'opacity' in i:
                    opacity_func() 
        #Phong
        elif cmds.ls(selection = True, type = 'phong'):
            global selected_shader
            selected_shader = cmds.ls(selection = True, type = 'phong')[0]
            my_array = ['.baseColor','.specularRoughness','.metalness','.normalCamera',
            '.subsurface', '.emissionColor', '.thinFilmIOR', '.opacity']
            my_array[0] = '.color'
            my_array[2] = '.reflectivity'
            my_array[7] = '.transparency'
            global connected_1
            connected_1 = cmds.listConnections(selected_shader + my_array[0])
            global connected_3
            connected_3 = cmds.listConnections(selected_shader + my_array[2])
            global connected_4
            connected_4 = cmds.listConnections(selected_shader + my_array[3])
            global connected_8
            connected_8 = cmds.listConnections(selected_shader + my_array[7])
            names = cmds.ls(selection = True, type = 'file')
            global i
            for i in names:
                if color_text in i or color_alt_text in i:
                    color_func()
                if metal_text in i or metal_alt_text in i:
                    metal_func()
                if normal_text in i:
                    normal_func()  
                if opacity_text in i or 'opacity' in i:
                    opacity_func() 
        #RedshiftMaterial
        elif cmds.ls(selection = True, type = 'RedshiftMaterial'):
            global selected_shader
            selected_shader = cmds.ls(selection = True, type = 'RedshiftMaterial')[0]
            my_array = ['.diffuse_color','.refl_roughness','.refl_metalness','.bump_input',
            '.ms_amount', '.emission_color', '.refl_ior', '.opacity_color']
            global connected_1
            connected_1 = cmds.listConnections(selected_shader + my_array[0])
            global connected_2
            connected_2 = cmds.listConnections(selected_shader + my_array[1])
            global connected_3
            connected_3 = cmds.listConnections(selected_shader + my_array[2])
            global connected_4
            connected_4 = cmds.listConnections(selected_shader + my_array[3])
            global connected_5
            connected_5 = cmds.listConnections(selected_shader + my_array[4])
            global connected_6
            connected_6 = cmds.listConnections(selected_shader + my_array[5])
            global connected_7
            connected_7 = cmds.listConnections(selected_shader + my_array[6])
            global connected_8
            connected_8 = cmds.listConnections(selected_shader + my_array[7])
            names = cmds.ls(selection = True, type = 'file')
            global i
            for i in names:
                if color_text in i or color_alt_text in i:
                    color_func('.diffuse_color')
                if roughness_text in i or roughness_alt_text in i:
                    roughness_func('.refl_roughness')
                if metal_text in i or metal_alt_text in i:
                    metal_func('.refl_metalness')
                if normal_text in i:
                    rs_normal_func()
                if scatter_text in i:
                    scatter_func('.ms_amount')
                if emissive_text in i:
                    emissive_func('.emission_color')
                if ior_text in i or 'Ior' in i or 'IOR' in i:
                    ior_func('.refl_ior')
                if opacity_text in i or 'opacity' in i:
                    opacity_func('.opacity_color') 
        #lambert 
        elif cmds.ls(selection = True, type = 'lambert'):
            global selected_shader
            selected_shader = cmds.ls(selection = True, type = 'lambert')[0]
            my_array = ['.baseColor','.specularRoughness','.metalness','.normalCamera',
            '.subsurface', '.emissionColor', '.thinFilmIOR', '.opacity']
            my_array[0] = '.color'
            my_array[7] = '.transparency'
            global connected_1
            connected_1 = cmds.listConnections(selected_shader + my_array[0])
            global connected_4
            connected_4 = cmds.listConnections(selected_shader + my_array[3])
            global connected_8
            connected_8 = cmds.listConnections(selected_shader + my_array[7])
            names = cmds.ls(selection = True, type = 'file')
            global i
            for i in names:
                if color_text in i or color_alt_text in i:
                    color_func()
                if normal_text in i:
                    normal_func()  
                if opacity_text in i or 'opacity' in i:
                    opacity_func()   
                             
def Delete_shaders():
    cmds.delete(cmds.ls(type = 'shadingDependNode'))
    cmds.delete(cmds.ls(type = 'shadingEngine'))
    for i in all_nodes_list:
        cmds.delete(cmds.ls(type = i))

def normal_flip():
    if default_shader == redshift:
        norm_flip_var = cmds.ls( type = 'RedshiftNormalMap')
        for i in norm_flip_var:
            norm_flip_val = cmds.getAttr('{0}.flipY'.format(i))
            if norm_flip_val == False:
                cmds.setAttr('{0}.flipY'.format(i), 1)
            else:
                cmds.setAttr('{0}.flipY'.format(i), 0)    

def light_func():
    if default_shader == redshift:
        mel.eval('redshiftCreateDomeLight')
        rs_dome = cmds.ls(type = 'RedshiftDomeLight')[0]
        cmds.setAttr('{0}.tex0'.format(rs_dome),default_pano, type = 'string')
    elif default_shader == arnold:
        mel.eval('cmdSkydomeLight')
        ar_dome = cmds.ls(type = 'aiSkyDomeLight')[0]
        place2d = cmds.shadingNode('place2dTexture', asUtility = True)
        text_file = cmds.shadingNode('file', isColorManaged = True, asTexture = True, name = ar_dome)
        cmds.connectAttr(place2d +'.outUV', text_file + '.uvCoord')
        cmds.setAttr(text_file + '.fileTextureName',default_pano, type = 'string')
        cmds.connectAttr(place2d +'.outUvFilterSize',text_file + '.uvFilterSize')
        connections = ['rotateUV','offset','noiseUV','vertexCameraOne','vertexUvThree','vertexUvTwo','vertexUvOne',
        'repeatUV','wrapV','wrapU','stagger','mirrorU','mirrorV','rotateFrame','translateFrame','coverage']
        for c in connections:
            cmds.connectAttr(place2d + '.' + c, text_file + '.' + c)
        cmds.connectAttr('{0}.outColor'.format(text_file),'{0}.color'.format(ar_dome))

   
seperator_size = 20
but_wid = 60
but_hi = 30
if cmds.window('myWindow', exists = True):
    cmds.deleteUI('myWindow')
        
cmds.window('myWindow', title = 'Automatic Materials') 
cmds.showWindow('myWindow')

third_layout = cmds.columnLayout()
cmds.separator(height= seperator_size/4)
cmds.text(label = 'Search set project or select a file folder?')

# Project is set?
collection1 = cmds.radioCollection()
cmds.radioButton( label='Set Project', select = True, onCommand = 'project()')
cmds.radioButton( label='Select a File Directory', onCommand = 'filedirectory()')

#object matching?
cmds.separator(height= seperator_size)
cmds.text(label = 'Apply materials to matching object names')
collection2 = cmds.radioCollection()
cmds.radioButton( label='True', select = True, onCommand = 'obj_match()')
cmds.radioButton( label='False', onCommand = 'obj_no_match()')

#Material Suffix
sep = cmds.separator(height= seperator_size)

third_layout
cmds.text(align = 'left', label = 'Material_Suf')
mat_but = cmds.textField('suffix', receiveFocusCommand = 'suffix_func()', width = 60)
cmds.separator(height = 20)
#Selected shader

cmds.text(label = 'Select a Shader')
#Shader List
sec_layout = cmds.rowColumnLayout(numberOfColumns = 5)
collection3 = cmds.radioCollection()

cmds.radioButton( label='redshift',select = True, onCommand = 'red()')
cmds.radioButton( label='arnold', onCommand = 'arn()')
cmds.radioButton( label='lambert', onCommand = 'lam()')
cmds.radioButton( label='phong', onCommand = 'pho()')
cmds.radioButton( label='blinn', onCommand = 'bli()')

cmds.separator(height= seperator_size, visible = False)
cmds.separator(height= seperator_size, visible = False)
cmds.separator(height= seperator_size, visible = False)
cmds.separator(height= seperator_size, visible = False)
cmds.separator(height= seperator_size, visible = False)

cmds.button(label = 'Run', width = but_wid, height = but_hi, command = 'Run_shader()')
cmds.button(label = 'Delete', width = but_wid, height = but_hi, command = 'Delete_shaders()')
cmds.button(label = 'Selected', width = but_wid, height = but_hi, command = 'Selected()')
cmds.button(label = 'Norm Flip', width = but_wid, height = but_hi, command = 'normal_flip()')
cmds.button(label = 'Light', width = but_wid, height = but_hi, command = 'light_func()')
#End of UI Stuff        
        
if ui == False:    
    if cmds.ls(selection = True, type = 'file'): #If a texture file is selected
        #Arnold
        if cmds.ls(selection = True, type = 'aiStandardSurface'):#If arnold is selected
            selected_shader = cmds.ls(selection = True, type = 'aiStandardSurface')[0]
            my_array = ['.baseColor','.specularRoughness','.metalness','.normalCamera',
            '.subsurface', '.emissionColor', '.thinFilmIOR', '.opacity']
            connected_1 = cmds.listConnections(selected_shader + my_array[0])
            #3 mfis  
            connected_2 = cmds.listConnections(selected_shader + my_array[1])
            connected_3 = cmds.listConnections(selected_shader + my_array[2])
            connected_4 = cmds.listConnections(selected_shader + my_array[3])
            connected_5 = cmds.listConnections(selected_shader + my_array[4])
            connected_6 = cmds.listConnections(selected_shader + my_array[5])
            connected_7 = cmds.listConnections(selected_shader + my_array[6])
            connected_8 = cmds.listConnections(selected_shader + my_array[7])
            
            names = cmds.ls(selection = True, type = 'file')
            for i in names:
                if color_text in i or color_alt_text in i:
                    color_func('.baseColor')
                if roughness_text in i or roughness_alt_text in i:
                    roughness_func()
                if metal_text in i or metal_alt_text in i:
                    metal_func('.metalness')
                if normal_text in i:
                    normal_func()  
                if scatter_text in i:
                    scatter_func('.subsurface')
                if emissive_text in i:
                    emissive_func('.emissionColor')
                if ior_text in i or 'Ior' in i or 'IOR' in i:
                    ior_func('.specularIOR')
                if opacity_text in i or 'opacity' in i:
                    opacity_func('.opacity') 
             
        #Blinn
        elif cmds.ls(selection = True, type = 'blinn'):
            selected_shader = cmds.ls(selection = True, type = 'blinn')[0]
            my_array = ['.baseColor','.specularRoughness','.metalness','.normalCamera',
            '.subsurface', '.emissionColor', '.thinFilmIOR', '.opacity']
            my_array[0] = '.color'
            my_array[2] = '.reflectivity'
            my_array[7] = '.transparency'
            connected_1 = cmds.listConnections(selected_shader + my_array[0])
            connected_3 = cmds.listConnections(selected_shader + my_array[2])
            connected_4 = cmds.listConnections(selected_shader + my_array[3])
            connected_8 = cmds.listConnections(selected_shader + my_array[7])
            names = cmds.ls(selection = True, type = 'file')
            for i in names:
                if color_text in i or color_alt_text in i:
                    color_func()
                if metal_text in i or metal_alt_text in i:
                    metal_func()
                if normal_text in i:
                    normal_func()  
                if opacity_text in i or 'opacity' in i:
                    opacity_func() 
        #Phong
        elif cmds.ls(selection = True, type = 'phong'):
            selected_shader = cmds.ls(selection = True, type = 'phong')[0]
            my_array = ['.baseColor','.specularRoughness','.metalness','.normalCamera',
            '.subsurface', '.emissionColor', '.thinFilmIOR', '.opacity']
            my_array[0] = '.color'
            my_array[2] = '.reflectivity'
            my_array[7] = '.transparency'
            connected_1 = cmds.listConnections(selected_shader + my_array[0])
            connected_3 = cmds.listConnections(selected_shader + my_array[2])
            connected_4 = cmds.listConnections(selected_shader + my_array[3])
            connected_8 = cmds.listConnections(selected_shader + my_array[7])
            names = cmds.ls(selection = True, type = 'file')
            for i in names:
                if color_text in i or color_alt_text in i:
                    color_func()
                if metal_text in i or metal_alt_text in i:
                    metal_func()
                if normal_text in i:
                    normal_func()  
                if opacity_text in i or 'opacity' in i:
                    opacity_func() 
        #RedshiftMaterial
        elif cmds.ls(selection = True, type = 'RedshiftMaterial'):
            selected_shader = cmds.ls(selection = True, type = 'RedshiftMaterial')[0]
            my_array = ['.diffuse_color','.refl_roughness','.refl_metalness','.bump_input',
            '.ms_amount', '.emission_color', '.refl_ior', '.opacity_color']
            connected_1 = cmds.listConnections(selected_shader + my_array[0])
            connected_2 = cmds.listConnections(selected_shader + my_array[1])
            connected_3 = cmds.listConnections(selected_shader + my_array[2])
            connected_4 = cmds.listConnections(selected_shader + my_array[3])
            connected_5 = cmds.listConnections(selected_shader + my_array[4])
            connected_6 = cmds.listConnections(selected_shader + my_array[5])
            connected_7 = cmds.listConnections(selected_shader + my_array[6])
            connected_8 = cmds.listConnections(selected_shader + my_array[7])
            names = cmds.ls(selection = True, type = 'file')
            for i in names:
                if color_text in i or color_alt_text in i:
                    color_func('.diffuse_color')
                if roughness_text in i or roughness_alt_text in i:
                    roughness_func('.refl_roughness')
                if metal_text in i or metal_alt_text in i:
                    metal_func('.refl_metalness')
                if normal_text in i:
                    rs_normal_func()
                if scatter_text in i:
                    scatter_func('.ms_amount')
                if emissive_text in i:
                    emissive_func('.emission_color')
                if ior_text in i or 'Ior' in i or 'IOR' in i:
                    ior_func('.refl_ior')
                if opacity_text in i or 'opacity' in i:
                    opacity_func('.opacity_color') 
        #lambert 
        elif cmds.ls(selection = True, type = 'lambert'):
            selected_shader = cmds.ls(selection = True, type = 'lambert')[0]
            my_array = ['.baseColor','.specularRoughness','.metalness','.normalCamera',
            '.subsurface', '.emissionColor', '.thinFilmIOR', '.opacity']
            my_array[0] = '.color'
            my_array[7] = '.transparency'
            connected_1 = cmds.listConnections(selected_shader + my_array[0])
            connected_4 = cmds.listConnections(selected_shader + my_array[3])
            connected_8 = cmds.listConnections(selected_shader + my_array[7])
            names = cmds.ls(selection = True, type = 'file')
            for i in names:
                if color_text in i or color_alt_text in i:
                    color_func()
                if normal_text in i:
                    normal_func()  
                if opacity_text in i or 'opacity' in i:
                    opacity_func()   
        else:
            cmds.warning('Please select your file(s) and a shader.')
            
    else:
        if project_is_set == True:
            basePath = cmds.workspace(q = True, rd = True)
            basePath = basePath + default_project_image_directory
            
        if project_is_set == False:
            basePath = cmds.fileDialog2(fileMode=2, caption="Import Folder")[0]
            
        directory = cmds.getFileList(folder = basePath)
        dir_array = []
        dir = ''
        dir_path_array = []
        dir_len_array = []
        
        for i in directory:
            if not '.png' in i:
                if not '.tx' in i:
                    if not '.tga' in i:
                        if not '.jpeg' in i:
                            if not '.jpg' in i:
                                if not '.tif' in i:
                                    if not'.raw' in i:
                                        dir = (basePath + '/' + i)
                                        dir_path_array.append(dir)
                                        dir2 = cmds.getFileList(folder = dir)
                                        dir_len_array.append(dir)
                                        dir_array.append(dir2)
                                        
        dir_length = len(dir_len_array)
        dir_var = 0
        
        while dir_var < dir_length:
            arrays_func(dir_var)
            dir_var = dir_var + 1
            
        selected_shader = cmds.shadingNode(default_shader, asShader = True)
        shadingEngine = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
        cmds.connectAttr(selected_shader + '.outColor', shadingEngine + '.surfaceShader')
        selected_shader2 = selected_shader
        
        my_array = ['.baseColor','.specularRoughness','.metalness','.normalCamera',
                    '.subsurface', '.emissionColor', '.thinFilmIOR', '.opacity']
        
        arnold_shaders = cmds.ls(type = 'aiStandardSurface')
        blinn_shaders = cmds.ls(type = 'blinn')
        phong_shaders = cmds.ls(type = 'phong')
        lambert_shaders = cmds.ls(type = 'lambert')
        redshift_shaders = cmds.ls(type = 'RedshiftMaterial')
        
        #Directory 2 
        for i in dir_total:
            if '.png' in i or '.jpg' in i or '.jpeg' in i or '.tga' in i or '.tif' in i or 'raw' in i:
                if not '.swatch' in i:
                    
                    if color_text in i:
                        cut = i.partition('_Base_' + color_text)
                        shader_create_func()
                       
                    if color_alt_text in i: 
                        cut = i.partition('_' + color_alt_text)
                        shader_create_func()
                    
                    if roughness_text in i:
                        cut = i.partition( '_' + roughness_text) 
                        shader_create_func()
                           
                    if roughness_alt_text in i:
                        cut = i.partition('_' + roughness_alt_text)
                        shader_create_func()
                    
                    if metal_text in i:
                        cut = i.partition('_' + metal_text)
                        shader_create_func()
                        
                    if metal_alt_text in i:
                        cut = i.partition('_' + metal_alt_text)
                        shader_create_func()
    
                    if normal_text in i:
                        cut = i.partition('_' + normal_text)
                        shader_create_func()
                    
                    if scatter_text in i:
                        cut = i.partition('_' + scatter_text)
                        shader_create_func()
                             
                    if emissive_text in i:
                        cut = i.partition('_' + emissive_text)
                        shader_create_func()
                        
                    if ior_text in i:
                        cut = i.partition('_' + ior_text)
                        shader_create_func()
                        
                    if 'Ior' in i:
                        cut = i.partition('_Ior')
                        shader_create_func()
                            
                    if 'IOR' in i:
                        cut = i.partition('_IOR')
                        shader_create_func()
                        
                    if opacity_text in i:
                        cut = i.partition('_' + opacity_text)
                        shader_create_func() 
                            
                    if 'opacity' in i:
                        cut = i.partition('_opacity')
                        shader_create_func()   
                        
                    if cmds.nodeType(selected_shader) == 'aiStandardSurface':
                        
                        my_array = ['.baseColor','.specularRoughness','.metalness','.normalCamera',
                        '.subsurface', '.emissionColor', '.thinFilmIOR', '.opacity']
                        connected_1 = cmds.listConnections(selected_shader + my_array[0])
                        connected_2 = cmds.listConnections(selected_shader + my_array[1])
                        connected_3 = cmds.listConnections(selected_shader + my_array[2])
                        connected_4 = cmds.listConnections(selected_shader + my_array[3])
                        connected_5 = cmds.listConnections(selected_shader + my_array[4])
                        connected_6 = cmds.listConnections(selected_shader + my_array[5])
                        connected_7 = cmds.listConnections(selected_shader + my_array[6])
                        connected_8 = cmds.listConnections(selected_shader + my_array[7])
                        
                        connect_1 = cmds.listConnections(selected_shader2 + my_array[0])
                        connect_2 = cmds.listConnections(selected_shader2 + my_array[1])
                        connect_3 = cmds.listConnections(selected_shader2 + my_array[2])
                        connect_4 = cmds.listConnections(selected_shader2 + my_array[3])
                        connect_5 = cmds.listConnections(selected_shader2 + my_array[4])
                        connect_6 = cmds.listConnections(selected_shader2 + my_array[5])
                        connect_7 = cmds.listConnections(selected_shader2 + my_array[6])
                        connect_8 = cmds.listConnections(selected_shader2 + my_array[7])
                        names = cmds.ls(selection = True, type = 'file')
                        if default_shader == arnold:
                            for i in names:
                                if color_text in i:
                                    cut = i.partition('_Base_' + color_text)
                                    same_name = False
                                    
                                    for b in arnold_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_1
                                            same_name = True
                                            color_func2('.baseColor')
                                    if same_name == False:
                                        if material_suffix in cut[0]:
                                            obj_shad_name = cut[0]
                                        else:
                                            obj_shad_name = cut[0] + material_suffix
                                        selected_shader2 = cmds.shadingNode(arnold, asShader = True, name = obj_shad_name)
                                        if cut[0] in selected_shader2:
                                            extra = cmds.listConnections(selected_shader2 + '.outColor')
                                            shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                                            cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                                            color_func2('.baseColor')
    
                                if color_alt_text in i:          
                                    cut = i.partition('_' + color_alt_text)
                                    same_name = False
                                    for b in arnold_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_1
                                            same_name = True
                                            color_func2('.baseColor')
                                    if same_name == False:
                                        if material_suffix in cut[0]:
                                            obj_shad_name = cut[0]
                                        else:
                                            obj_shad_name = cut[0] + material_suffix
                                        selected_shader2 = cmds.shadingNode(arnold, asShader = True, name = obj_shad_name)
                                        if cut[0] in selected_shader2:
                                            extra = cmds.listConnections(selected_shader2 + '.outColor')
                                            shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                                            cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                                            color_func2('.baseColor')
       
                                if roughness_text in i:
                                    cut = i.partition( '_' + roughness_text)
                                    same_name = False
                                    for b in arnold_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_2
                                            same_name = True
                                            roughness_func2()
                                    if same_name == False:
                                        roughness_func2()
        
                                if roughness_alt_text in i:
                                    cut = i.partition( '_' + roughness_alt_text)
                                    same_name = False
                                    for b in arnold_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_2
                                            same_name = True
                                            roughness_func2()
                                    if same_name == False:
                                        roughness_func2()
                               
                                if metal_text in i:
                                    cut = i.partition('_' + metal_text)
                                    same_name = False
                                    for b in arnold_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_3
                                            same_name = True
                                            metal_func2('.metalness')
                                    if same_name == False:
                                        metal_func2('.metalness')
                             
                                if metal_alt_text in i:
                                    cut = i.partition('_' + metal_alt_text)
                                    same_name = False
                                    for b in arnold_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_3
                                            same_name = True
                                            metal_func2('.metalness')
                                    if same_name == False:
                                        metal_func2('.metalness')
                                        
                                if normal_text in i:
                                    cut = i.partition('_' + normal_text)
                                    same_name = False
                                    for b in arnold_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_3
                                            same_name = True
                                            normal_func2()
                                    if same_name == False:
                                        normal_func2()
                                     
                                if scatter_text in i:
                                    cut = i.partition('_' + scatter_text)
                                    same_name = False
                                    for b in arnold_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_5
                                            same_name = True
                                            scatter_func2('.subsurface')
                                    if same_name == False:
                                        scatter_func2('.subsurface')
                              
                                if emissive_text in i:
                                    cut = i.partition('_' + emissive_text)
                                    same_name = False
                                    for b in arnold_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_6
                                            same_name = True
                                            emissive_func2('.emissionColor')
                                    if same_name == False:
                                        emissive_func2('.emissionColor')
                             
                                if ior_text in i:
                                    cut = i.partition('_' + ior_text)
                                    same_name = False
                                    for b in arnold_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_7
                                            same_name = True
                                            ior_func2('.specularIOR')
                                    if same_name == False:
                                        ior_func2('.specularIOR')
                                 
                                if 'Ior' in i:
                                    cut = i.partition('_Ior')
                                    same_name = False
                                    for b in arnold_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_7
                                            same_name = True
                                            ior_func2('.specularIOR')
                                    if same_name == False:
                                        ior_func2('.specularIOR')
                                 
                                if 'IOR' in i:
                                    cut = i.partition('_IOR')
                                    same_name = False
                                    for b in arnold_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_7
                                            same_name = True
                                            ior_func2('.specularIOR')
                                    if same_name == False:
                                        ior_func2('.specularIOR')
                               
                                if opacity_text in i:
                                    cut = i.partition('_' + opacity_text)
                                    same_name = False
                                    for b in arnold_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_8
                                            same_name = True
                                            opacity_func2('.opacity')
                                    if same_name == False:
                                        opacity_func2('.opacity') 
                                 
                                if 'opacity' in i:
                                    cut = i.partition('_opacity')
                                    same_name = False
                                    for b in arnold_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_8
                                            same_name = True
                                            opacity_func2('.opacity')
                                    if same_name == False:
                                        opacity_func2('.opacity') 
             
                    #Blinn
                    elif cmds.nodeType(selected_shader) == 'blinn':
                        my_array = ['.baseColor','.specularRoughness','.metalness','.normalCamera',
                        '.subsurface', '.emissionColor', '.thinFilmIOR', '.opacity']
                        my_array[0] = '.color'
                        my_array[2] = '.reflectivity'
                        my_array[7] = '.transparency'
                        connected_1 = cmds.listConnections(selected_shader + my_array[0])
                        connected_3 = cmds.listConnections(selected_shader + my_array[2])
                        connected_4 = cmds.listConnections(selected_shader + my_array[3])
                        connected_8 = cmds.listConnections(selected_shader + my_array[7])
                        
                        connect_1 = cmds.listConnections(selected_shader2 + my_array[0])
                        connect_3 = cmds.listConnections(selected_shader2 + my_array[2])
                        connect_4 = cmds.listConnections(selected_shader2 + my_array[3])
                        connect_8 = cmds.listConnections(selected_shader2 + my_array[7])
                        names = cmds.ls(selection = True, type = 'file')
                        if default_shader == blinn:
                            for i in names:
                                if color_text in i:
                                    cut = i.partition('_Base_' + color_text)
                                    same_name = False
                                    for b in blinn_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_1
                                            same_name = True
                                            color_func2()
                                    if same_name == False: 
                                        if material_suffix in cut[0]:
                                            obj_shad_name = cut[0]
                                        else:
                                            obj_shad_name = cut[0] + material_suffix
                                        selected_shader2 = cmds.shadingNode(blinn, asShader = True, name = obj_shad_name)
                                        if cut[0] in selected_shader2:
                                            extra = cmds.listConnections(selected_shader2 + '.outColor')
                                            shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                                            cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                                            color_func2()   
                                if color_alt_text in i:
                                    cut = i.partition('_' + color_alt_text)
                                    same_name = False
                                    for b in blinn_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_1
                                            same_name = True
                                            color_func2()
                                    if same_name == False:
                                        if material_suffix in cut[0]:
                                            obj_shad_name = cut[0]
                                        else:
                                            obj_shad_name = cut[0] + material_suffix
                                        selected_shader2 = cmds.shadingNode(blinn, asShader = True, name = obj_shad_name)
                                        if cut[0] in selected_shader2:
                                            extra = cmds.listConnections(selected_shader2 + '.outColor')
                                            shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                                            cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                                            color_func2() 
                                            
                                if metal_text in i:
                                    cut = i.partition('_' + metal_text)
                                    same_name = False
                                    for b in blinn_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_3
                                            same_name = True
                                            metal_func2()
                                    if same_name == False:
                                        metal_func2()    
                                        
                                if metal_alt_text in i:
                                    cut = i.partition('_' + metal_alt_text)
                                    same_name = False
                                    for b in blinn_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_3
                                            same_name = True
                                            metal_func2()
                                    if same_name == False:
                                        metal_func2()   
                                        
                                if normal_text in i:
                                    cut = i.partition('_' + normal_text)
                                    same_name = False
                                    for b in blinn_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_4
                                            same_name = True
                                            normal_func2()
                                    if same_name == False:
                                        normal_func2()   
                                        
                                if opacity_text in i:
                                    cut = i.partition('_' + opacity_text)
                                    same_name = False
                                    for b in blinn_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_8
                                            same_name = True
                                            opacity_func2()
                                    if same_name == False:
                                        opacity_func2()   
                                
                                if 'opacity' in i:
                                    cut = i.partition('_opacity')
                                    same_name = False
                                    for b in blinn_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_8
                                            same_name = True
                                            opacity_func2()
                                    if same_name == False:
                                        opacity_func2()  
                                        
                    #Phong
                    elif cmds.nodeType(selected_shader) == 'phong':
                        my_array = ['.baseColor','.specularRoughness','.metalness','.normalCamera',
                        '.subsurface', '.emissionColor', '.thinFilmIOR', '.opacity']
                        my_array[0] = '.color'
                        my_array[2] = '.reflectivity'
                        my_array[7] = '.transparency'
                        
                        connected_1 = cmds.listConnections(selected_shader + my_array[0])
                        connected_3 = cmds.listConnections(selected_shader + my_array[2])
                        connected_4 = cmds.listConnections(selected_shader + my_array[3])
                        connected_8 = cmds.listConnections(selected_shader + my_array[7])
                        
                        connect_1 = cmds.listConnections(selected_shader2 + my_array[0])
                        connect_3 = cmds.listConnections(selected_shader2 + my_array[2])
                        connect_4 = cmds.listConnections(selected_shader2 + my_array[3])
                        connect_8 = cmds.listConnections(selected_shader2 + my_array[7])
                        
                        names = cmds.ls(selection = True, type = 'file')
                        if default_shader == phong:
                            for i in names:
                                if color_text in i:
                                    cut = i.partition('_Base_' + color_text)
                                    same_name = False
                                    for b in phong_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_1
                                            same_name = True
                                            color_func2()
                                    if same_name == False:
                                        if material_suffix in cut[0]:
                                            obj_shad_name = cut[0]
                                        else:
                                            obj_shad_name = cut[0] + material_suffix
                                        selected_shader2 = cmds.shadingNode(phong, asShader = True, name = obj_shad_name)
                                        if cut[0] in selected_shader2:
                                            extra = cmds.listConnections(selected_shader2 + '.outColor')
                                            shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                                            cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                                            color_func2()   
                                            
                                if color_alt_text in i:
                                    cut = i.partition('_' + color_alt_text)
                                    same_name = False
                                    for b in phong_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_1
                                            same_name = True
                                            color_func2()
                                    if same_name == False:
                                        if material_suffix in cut[0]:
                                            obj_shad_name = cut[0]
                                        else:
                                            obj_shad_name = cut[0] + material_suffix
                                        selected_shader2 = cmds.shadingNode(phong, asShader = True, name = obj_shad_name)
                                        if cut[0] in selected_shader2:
                                            extra = cmds.listConnections(selected_shader2 + '.outColor')
                                            shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                                            cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                                            color_func2() 
                                            
                                if metal_text in i:
                                    cut = i.partition('_' + metal_text)
                                    same_name = False
                                    for b in phong_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_3
                                            same_name = True
                                            metal_func2()
                                    if same_name == False:
                                        metal_func2()     
                                        
                                if metal_alt_text in i:
                                    cut = i.partition('_' + metal_alt_text)
                                    same_name = False
                                    for b in phong_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_3
                                            same_name = True
                                            metal_func2()
                                    if same_name == False:
                                        metal_func2()    
                                        
                                if normal_text in i:
                                    cut = i.partition('_' + normal_text)
                                    same_name = False
                                    for b in phong_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_4
                                            same_name = True
                                            normal_func2()
                                    if same_name == False:
                                        normal_func2()  
    
                                       
                                if opacity_text in i :
                                    cut = i.partition('_' + opacity_text)
                                    same_name = False
                                    for b in phong_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_8
                                            same_name = True
                                            opacity_func2()
                                    if same_name == False:
                                        opacity_func2() 
                                        
                                if 'opacity' in i:
                                    cut = i.partition('_opacity')
                                    same_name = False
                                    for b in phong_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_8
                                            same_name = True
                                            opacity_func2()
                                    if same_name == False:
                                        opacity_func2()             
    
                    #RedshiftMaterial
                    elif cmds.nodeType(selected_shader) == 'RedshiftMaterial':
                        my_array = ['.diffuse_color','.refl_roughness','.refl_metalness','.bump_input',
                        '.ms_amount', '.emission_color', '.refl_ior', '.opacity_color']
                        connected_1 = cmds.listConnections(selected_shader + my_array[0])
                        connected_2 = cmds.listConnections(selected_shader + my_array[1])
                        connected_3 = cmds.listConnections(selected_shader + my_array[2])
                        connected_4 = cmds.listConnections(selected_shader + my_array[3])
                        connected_5 = cmds.listConnections(selected_shader + my_array[4])
                        connected_6 = cmds.listConnections(selected_shader + my_array[5])
                        connected_7 = cmds.listConnections(selected_shader + my_array[6])
                        connected_8 = cmds.listConnections(selected_shader + my_array[7])
                        
                        connect_1 = cmds.listConnections(selected_shader2 + my_array[0])
                        connect_2 = cmds.listConnections(selected_shader2 + my_array[1])
                        connect_3 = cmds.listConnections(selected_shader2 + my_array[2])
                        connect_4 = cmds.listConnections(selected_shader2 + my_array[3])
                        connect_5 = cmds.listConnections(selected_shader2 + my_array[4])
                        connect_6 = cmds.listConnections(selected_shader2 + my_array[5])
                        connect_7 = cmds.listConnections(selected_shader2 + my_array[6])
                        connect_8 = cmds.listConnections(selected_shader2 + my_array[7])
                        
                        names = cmds.ls(selection = True, type = 'file')
                        if default_shader == redshift:
                            for i in names:
                                if color_text in i:
                                    cut = i.partition('_Base_' + color_text)
                                    same_name = False
                                    for b in redshift_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_1
                                            same_name = True
                                            color_func2('.diffuse_color')
                                            cmds.setAttr(selected_shader2 + '.refl_brdf', default_BRDF)
                                    if same_name == False:
                                        if material_suffix in cut[0]:
                                            obj_shad_name = cut[0]
                                        else:
                                            obj_shad_name = cut[0] + material_suffix
                                        selected_shader2 = cmds.shadingNode(redshift, asShader = True, name = obj_shad_name)
                                        if cut[0] in selected_shader2:
                                            extra = cmds.listConnections(selected_shader2 + '.outColor')
                                            shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                                            cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                                            color_func2('.diffuse_color')      
                                            cmds.setAttr(selected_shader2 + '.refl_brdf', default_BRDF)
                                            
                                if color_alt_text in i:
                                    cut = i.partition('_' + color_alt_text)
                                    same_name = False
                                    for b in redshift_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_1
                                            same_name = True
                                            color_func2('.diffuse_color')
                                            cmds.setAttr(selected_shader2 + '.refl_brdf', default_BRDF)
                                    if same_name == False:
                                        if material_suffix in cut[0]:
                                            obj_shad_name = cut[0]
                                        else:
                                            obj_shad_name = cut[0] + material_suffix
                                        selected_shader2 = cmds.shadingNode(redshift, asShader = True, name = obj_shad_name)
                                        if cut[0] in selected_shader2:
                                            extra = cmds.listConnections(selected_shader2 + '.outColor')
                                            shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                                            cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                                            color_func2('.diffuse_color') 
                                            cmds.setAttr(selected_shader2 + '.refl_brdf', default_BRDF)                                   
                                        
                                if roughness_text in i:
                                    cut = i.partition( '_' + roughness_text)
                                    same_name = False
                                    for b in redshift_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_2
                                            same_name = True
                                            roughness_func2('.refl_roughness')
                                            cmds.setAttr(selected_shader2 + '.refl_brdf', default_BRDF)
                                    if same_name == False:
                                        roughness_func2('.refl_roughness')
                                        cmds.setAttr(selected_shader2 + '.refl_brdf', default_BRDF)
                                        
                                if roughness_alt_text in i:
                                    cut = i.partition( '_' + roughness_alt_text)
                                    same_name = False
                                    for b in redshift_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_2
                                            same_name = True
                                            roughness_func2('.refl_roughness')
                                            cmds.setAttr(selected_shader2 + '.refl_brdf', default_BRDF)
                                    if same_name == False:
                                        roughness_func2('.refl_roughness')
                                        cmds.setAttr(selected_shader2 + '.refl_brdf', default_BRDF)
                                        
                                if metal_text in i:
                                    cut = i.partition('_' + metal_text)
                                    same_name = False
                                    for b in redshift_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_3
                                            same_name = True
                                            metal_func2('.refl_metalness')
                                            cmds.setAttr(selected_shader2 + '.refl_fresnel_mode', 2)
                                    if same_name == False:
                                        metal_func2('.refl_metalness')
                                        cmds.setAttr(selected_shader2 + '.refl_fresnel_mode', 2)
                                        
                                if metal_alt_text in i:
                                    cut = i.partition('_' + metal_alt_text)
                                    same_name = False
                                    for b in redshift_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_3
                                            same_name = True
                                            metal_func2('.refl_metalness')
                                            cmds.setAttr(selected_shader2 + '.refl_fresnel_mode', 2)
                                    if same_name == False:
                                        metal_func2('.refl_metalness')
                                        cmds.setAttr(selected_shader2 + '.refl_fresnel_mode', 2)
                                    
                                if normal_text in i:
                                    cut = i.partition('_' + normal_text)
                                    same_name = False
                                    for b in redshift_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_4
                                            same_name = True
                                            rs_normal_func2()
                                    if same_name == False:
                                        rs_normal_func2() 
                                     
                                if scatter_text in i:
                                    cut = i.partition('_' + scatter_text)
                                    same_name = False
                                    for b in redshift_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_5
                                            same_name = True
                                            scatter_func2('.ms_amount')
                                    if same_name == False:
                                        scatter_func2('.ms_amount')
                                         
                                if emissive_text in i:
                                    cut = i.partition('_' + emissive_text)
                                    same_name = False
                                    for b in redshift_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_6
                                            same_name = True
                                            emissive_func2('.emission_color')
                                    if same_name == False:
                                        emissive_func2('.emission_color')
                                    
                                if ior_text in i:
                                    cut = i.partition('_' + ior_text)
                                    same_name = False
                                    for b in redshift_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_7
                                            same_name = True
                                            ior_func2('.refl_ior')
                                    if same_name == False:
                                        ior_func2('.refl_ior')
                                        
                                if 'Ior' in i:
                                    cut = i.partition('_Ior')
                                    same_name = False
                                    for b in redshift_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_7
                                            same_name = True
                                            ior_func2('.refl_ior')
                                    if same_name == False:
                                        ior_func2('.refl_ior')
                                        
                                if 'IOR' in i:
                                    cut = i.partition('_IOR')
                                    same_name = False
                                    for b in redshift_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_7
                                            same_name = True
                                            ior_func2('.refl_ior')
                                    if same_name == False:
                                        ior_func2('.refl_ior')
                                        
                                if opacity_text in i:
                                    cut = i.partition('_' + opacity_text)
                                    same_name = False
                                    for b in redshift_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_8
                                            same_name = True
                                            opacity_func2('.opacity_color')
                                    if same_name == False:
                                        opacity_func2('.opacity_color') 
                                        
                                if 'opacity' in i:
                                    cut = i.partition('_opacity')
                                    same_name = False
                                    for b in redshift_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_8
                                            same_name = True
                                            opacity_func2('.opacity_color')
                                    if same_name == False:
                                        opacity_func2('.opacity_color')
                                    
                    #lambert 
                    elif cmds.nodeType(selected_shader) == 'lambert':
                        my_array = ['.baseColor','.specularRoughness','.metalness','.normalCamera',
                        '.subsurface', '.emissionColor', '.thinFilmIOR', '.opacity']
                        my_array[0] = '.color'
                        my_array[7] = '.transparency'
                        
                        connected_1 = cmds.listConnections(selected_shader + my_array[0])
                        connected_4 = cmds.listConnections(selected_shader + my_array[3])
                        connected_8 = cmds.listConnections(selected_shader + my_array[7])
                        
                        connect_1 = cmds.listConnections(selected_shader2 + my_array[0])
                        connect_4 = cmds.listConnections(selected_shader2 + my_array[3])
                        connect_8 = cmds.listConnections(selected_shader2 + my_array[7])
                        names = cmds.ls(selection = True, type = 'file')
                        if default_shader == lambert:
                            for i in names:
                                if color_text in i:
                                    cut = i.partition('_Base_' + color_text)
                                    same_name = False
                                    for b in lambert_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_1
                                            same_name = True
                                            color_func2()
                                    if same_name == False:
                                        if material_suffix in cut[0]:
                                            obj_shad_name = cut[0]
                                        else:
                                            obj_shad_name = cut[0] + material_suffix
                                        selected_shader2 = cmds.shadingNode(lambert, asShader = True, name = obj_shad_name)
                                        if cut[0] in selected_shader2:
                                            extra = cmds.listConnections(selected_shader2 + '.outColor')
                                            shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                                            cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                                            color_func2()     
                                            
                                if color_alt_text in i:
                                    cut = i.partition('_' + color_alt_text)
                                    same_name = False
                                    for b in lambert_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_1
                                            same_name = True
                                            color_func2()
                                    if same_name == False:
                                        if material_suffix in cut[0]:
                                            obj_shad_name = cut[0]
                                        else:
                                            obj_shad_name = cut[0] + material_suffix
                                        selected_shader2 = cmds.shadingNode(lambert, asShader = True, name = obj_shad_name)
                                        if cut[0] in selected_shader2:
                                            extra = cmds.listConnections(selected_shader2 + '.outColor')
                                            shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                                            cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                                            color_func2()     
                                        
                                if normal_text in i:
                                    cut = i.partition('_' + normal_text)
                                    same_name = False
                                    for b in lambert_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_4
                                            same_name = True
                                            normal_func2()
                                    if same_name == False:
                                        normal_func2()   
                                        
                                if opacity_text in i:
                                    cut = i.partition('_' + opacity_text)
                                    same_name = False
                                    for b in lambert_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_8
                                            same_name = True
                                            opacity_func2()
                                    if same_name == False:
                                        opacity_func2()        
                                        
                                if 'opacity' in i:
                                    cut = i.partition('_opacity')
                                    same_name = False
                                    for b in lambert_shaders:
                                        if cut[0] in b:
                                            selected_shader2 = b
                                            connect_8
                                            same_name = True
                                            opacity_func2()
                                    if same_name == False:
                                        opacity_func2()     
    
                    else:
                        cmds.warning('Please select your file(s) and a shader.')    
                    
                                        
        # First Directory                                                    
        for i in directory:
            if '.png' in i or '.jpg' in i or '.jpeg' in i or '.tga' in i or '.tif' in i or 'raw' in i:
       
                place2d = cmds.shadingNode('place2dTexture', asUtility = True)
                text_file = cmds.shadingNode('file', isColorManaged = True, asTexture = True, name = i[:-4])
                cmds.connectAttr(place2d +'.outUV', text_file + '.uvCoord')
                cmds.setAttr(text_file + '.fileTextureName', basePath + '/' + i, type = 'string')
                cmds.connectAttr(place2d +'.outUvFilterSize',text_file + '.uvFilterSize')
                connections = ['rotateUV','offset','noiseUV','vertexCameraOne','vertexUvThree','vertexUvTwo','vertexUvOne',
                'repeatUV','wrapV','wrapU','stagger','mirrorU','mirrorV','rotateFrame','translateFrame','coverage']
                for c in connections:
                    cmds.connectAttr(place2d + '.' + c, text_file + '.' + c)
                #Arnold
                if cmds.nodeType(selected_shader) == 'aiStandardSurface':
                    my_array = ['.baseColor','.specularRoughness','.metalness','.normalCamera',
                    '.subsurface', '.emissionColor', '.thinFilmIOR', '.opacity']
                    connected_1 = cmds.listConnections(selected_shader + my_array[0])
                    connected_2 = cmds.listConnections(selected_shader + my_array[1])
                    connected_3 = cmds.listConnections(selected_shader + my_array[2])
                    connected_4 = cmds.listConnections(selected_shader + my_array[3])
                    connected_5 = cmds.listConnections(selected_shader + my_array[4])
                    connected_6 = cmds.listConnections(selected_shader + my_array[5])
                    connected_7 = cmds.listConnections(selected_shader + my_array[6])
                    connected_8 = cmds.listConnections(selected_shader + my_array[7])
                    
                    connect_1 = cmds.listConnections(selected_shader2 + my_array[0])
                    connect_2 = cmds.listConnections(selected_shader2 + my_array[1])
                    connect_3 = cmds.listConnections(selected_shader2 + my_array[2])
                    connect_4 = cmds.listConnections(selected_shader2 + my_array[3])
                    connect_5 = cmds.listConnections(selected_shader2 + my_array[4])
                    connect_6 = cmds.listConnections(selected_shader2 + my_array[5])
                    connect_7 = cmds.listConnections(selected_shader2 + my_array[6])
                    connect_8 = cmds.listConnections(selected_shader2 + my_array[7])
    
                    names = cmds.ls(selection = True, type = 'file')
                    if default_shader == arnold:
                        for i in names:
                            if color_text in i:
                                cut = i.partition('_Base_' + color_text)
                                same_name = False
                                for b in arnold_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_1
                                        same_name = True
                                        color_func2('.baseColor')
                                if same_name == False:
                                    if material_suffix in cut[0]:
                                        obj_shad_name = cut[0]
                                    else:
                                        obj_shad_name = cut[0] + material_suffix
                                    selected_shader2 = cmds.shadingNode(arnold, asShader = True, name = obj_shad_name)
                                    if cut[0] in selected_shader2:
                                        extra = cmds.listConnections(selected_shader2 + '.outColor')
                                        shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                                        cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                                        color_func2('.baseColor')
                            
                            if color_alt_text in i:          
                                cut = i.partition('_' + color_alt_text)
                                same_name = False
                                for b in arnold_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_1
                                        same_name = True
                                        color_func2('.baseColor')
                                if same_name == False:
                                    if material_suffix in cut[0]:
                                        obj_shad_name = cut[0]
                                    else:
                                        obj_shad_name = cut[0] + material_suffix
                                    selected_shader2 = cmds.shadingNode(arnold, asShader = True, name = obj_shad_name)
                                    if cut[0] in selected_shader2:
                                        extra = cmds.listConnections(selected_shader2 + '.outColor')
                                        shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                                        cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                                        color_func2('.baseColor')
                                    
                            if roughness_text in i:
                                cut = i.partition( '_' + roughness_text)
                                same_name = False
                                for b in arnold_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_2
                                        same_name = True
                                        roughness_func2()
                                if same_name == False:
                                    roughness_func2()
                                    
                            if roughness_alt_text in i:
                                cut = i.partition( '_' + roughness_alt_text)
                                same_name = False
                                for b in arnold_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_2
                                        same_name = True
                                        roughness_func2()
                                if same_name == False:
                                    roughness_func2()
                                    
                            if metal_text in i:
                                cut = i.partition('_' + metal_text)
                                same_name = False
                                for b in arnold_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_3
                                        same_name = True
                                        metal_func2('.metalness')
                                if same_name == False:
                                    metal_func2('.metalness')
                                    
                            if metal_alt_text in i:
                                cut = i.partition('_' + metal_alt_text)
                                same_name = False
                                for b in arnold_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_3
                                        same_name = True
                                        metal_func2('.metalness')
                                if same_name == False:
                                    metal_func2('.metalness')
                           
                            if normal_text in i:
                                cut = i.partition('_' + normal_text)
                                same_name = False
                                for b in arnold_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_4
                                        same_name = True
                                        normal_func2()
                                if same_name == False:
                                    normal_func2()  
                            
                            if scatter_text in i:
                                cut = i.partition('_' + scatter_text)
                                same_name = False
                                for b in arnold_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_5
                                        same_name = True
                                        scatter_func2('.subsurface')
                                if same_name == False:
                                    scatter_func2('.subsurface')
                                     
                            if emissive_text in i:
                                cut = i.partition('_' + emissive_text)
                                same_name = False
                                for b in arnold_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_6
                                        same_name = True
                                        emissive_func2('.emissionColor')
                                if same_name == False:
                                    emissive_func2('.emissionColor')
                                
                            if ior_text in i:
                                cut = i.partition('_' + ior_text)
                                same_name = False
                                for b in arnold_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_7
                                        same_name = True
                                        ior_func2('.specularIOR')
                                if same_name == False:
                                    ior_func2('.specularIOR')
                                    
                            if 'Ior' in i:
                                cut = i.partition('_Ior')
                                same_name = False
                                for b in arnold_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_7
                                        same_name = True
                                        ior_func2('.specularIOR')
                                if same_name == False:
                                    ior_func2('.specularIOR')
                                    
                            if 'IOR' in i:
                                cut = i.partition('_IOR')
                                same_name = False
                                for b in arnold_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_7
                                        same_name = True
                                        ior_func2('.specularIOR')
                                if same_name == False:
                                    ior_func2('.specularIOR')
                                    
                            if opacity_text in i:
                                cut = i.partition('_' + opacity_text)
                                same_name = False
                                for b in arnold_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_8
                                        same_name = True
                                        opacity_func2('.opacity')
                                if same_name == False:
                                    opacity_func2('.opacity') 
                                    
                            if 'opacity' in i:
                                cut = i.partition('_opacity')
                                same_name = False
                                for b in arnold_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_8
                                        same_name = True
                                        opacity_func2('.opacity')
                                if same_name == False:
                                    opacity_func2('.opacity') 
                                 
                #Blinn
                elif cmds.nodeType(selected_shader) == 'blinn':
                    my_array = ['.baseColor','.specularRoughness','.metalness','.normalCamera',
                    '.subsurface', '.emissionColor', '.thinFilmIOR', '.opacity']
                    my_array[0] = '.color'
                    my_array[2] = '.reflectivity'
                    my_array[7] = '.transparency'
                    connected_1 = cmds.listConnections(selected_shader + my_array[0])
                    connected_3 = cmds.listConnections(selected_shader + my_array[2])
                    connected_4 = cmds.listConnections(selected_shader + my_array[3])
                    connected_8 = cmds.listConnections(selected_shader + my_array[7])
                    
                    connect_1 = cmds.listConnections(selected_shader2 + my_array[0])
                    connect_3 = cmds.listConnections(selected_shader2 + my_array[2])
                    connect_4 = cmds.listConnections(selected_shader2 + my_array[3])
                    connect_8 = cmds.listConnections(selected_shader2 + my_array[7])
                    names = cmds.ls(selection = True, type = 'file')
                    if default_shader == blinn:
                        for i in names:
                            if color_text in i:
                                cut = i.partition('_Base_' + color_text)
                                same_name = False
                                for b in blinn_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_1
                                        same_name = True
                                        color_func2()
                                if same_name == False:
                                    if material_suffix in cut[0]:
                                        obj_shad_name = cut[0]
                                    else:
                                        obj_shad_name = cut[0] + material_suffix
                                    selected_shader2 = cmds.shadingNode(blinn, asShader = True, name = obj_shad_name)
                                    if cut[0] in selected_shader2:
                                        extra = cmds.listConnections(selected_shader2 + '.outColor')
                                        shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                                        cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                                        color_func2()   
                            if color_alt_text in i:
                                cut = i.partition('_' + color_alt_text)
                                same_name = False
                                for b in blinn_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_1
                                        same_name = True
                                        color_func2()
                                if same_name == False:
                                    if material_suffix in cut[0]:
                                        obj_shad_name = cut[0]
                                    else:
                                        obj_shad_name = cut[0] + material_suffix
                                    selected_shader2 = cmds.shadingNode(blinn, asShader = True, name = obj_shad_name)
                                    if cut[0] in selected_shader2:
                                        extra = cmds.listConnections(selected_shader2 + '.outColor')
                                        shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                                        cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                                        color_func2() 
                                        
                            if metal_text in i:
                                cut = i.partition('_' + metal_text)
                                same_name = False
                                for b in blinn_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_3
                                        same_name = True
                                        metal_func2()
                                if same_name == False:
                                    metal_func2()    
                                    
                            if metal_alt_text in i:
                                cut = i.partition('_' + metal_alt_text)
                                same_name = False
                                for b in blinn_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_3
                                        same_name = True
                                        metal_func2()
                                if same_name == False:
                                    metal_func2()   
                                    
                            if normal_text in i:
                                cut = i.partition('_' + normal_text)
                                same_name = False
                                for b in blinn_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_4
                                        same_name = True
                                        normal_func2()
                                if same_name == False:
                                    normal_func2()   
                                    
                            if opacity_text in i:
                                cut = i.partition('_' + opacity_text)
                                same_name = False
                                for b in blinn_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_8
                                        same_name = True
                                        opacity_func2()
                                if same_name == False:
                                    opacity_func2()   
                            
                            if 'opacity' in i:
                                cut = i.partition('_opacity')
                                same_name = False
                                for b in blinn_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_8
                                        same_name = True
                                        opacity_func2()
                                if same_name == False:
                                    opacity_func2()         
    
                #Phong
                elif cmds.nodeType(selected_shader) == 'phong':
                    my_array = ['.baseColor','.specularRoughness','.metalness','.normalCamera',
                    '.subsurface', '.emissionColor', '.thinFilmIOR', '.opacity']
                    my_array[0] = '.color'
                    my_array[2] = '.reflectivity'
                    my_array[7] = '.transparency'
                    
                    connected_1 = cmds.listConnections(selected_shader + my_array[0])
                    connected_3 = cmds.listConnections(selected_shader + my_array[2])
                    connected_4 = cmds.listConnections(selected_shader + my_array[3])
                    connected_8 = cmds.listConnections(selected_shader + my_array[7])
                    
                    connect_1 = cmds.listConnections(selected_shader2 + my_array[0])
                    connect_3 = cmds.listConnections(selected_shader2 + my_array[2])
                    connect_4 = cmds.listConnections(selected_shader2 + my_array[3])
                    connect_8 = cmds.listConnections(selected_shader2 + my_array[7])
                    
                    names = cmds.ls(selection = True, type = 'file')
                    if default_shader == phong:
                        for i in names:
                            if color_text in i:
                                cut = i.partition('_Base_' + color_text)
                                same_name = False
                                for b in phong_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_1
                                        same_name = True
                                        color_func2()
                                if same_name == False:
                                    if material_suffix in cut[0]:
                                        obj_shad_name = cut[0]
                                    else:
                                        obj_shad_name = cut[0] + material_suffix
                                    selected_shader2 = cmds.shadingNode(phong, asShader = True, name = obj_shad_name)
                                    if cut[0] in selected_shader2:
                                        extra = cmds.listConnections(selected_shader2 + '.outColor')
                                        shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                                        cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                                        color_func2()   
                                        
                            if color_alt_text in i:
                                cut = i.partition('_' + color_alt_text)
                                same_name = False
                                for b in phong_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_1
                                        same_name = True
                                        color_func2()
                                if same_name == False:
                                    if material_suffix in cut[0]:
                                        obj_shad_name = cut[0]
                                    else:
                                        obj_shad_name = cut[0] + material_suffix
                                    selected_shader2 = cmds.shadingNode(phong, asShader = True, name = obj_shad_name)
                                    if cut[0] in selected_shader2:
                                        extra = cmds.listConnections(selected_shader2 + '.outColor')
                                        shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                                        cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                                        color_func2() 
                                        
                            if metal_text in i:
                                cut = i.partition('_' + metal_text)
                                same_name = False
                                for b in phong_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_3
                                        same_name = True
                                        metal_func2()
                                if same_name == False:
                                    metal_func2()     
                                    
                            if metal_alt_text in i:
                                cut = i.partition('_' + metal_alt_text)
                                same_name = False
                                for b in phong_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_3
                                        same_name = True
                                        metal_func2()
                                if same_name == False:
                                    metal_func2()    
                                    
                            if normal_text in i:
                                cut = i.partition('_' + normal_text)
                                same_name = False
                                for b in phong_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_4
                                        same_name = True
                                        normal_func2()
                                if same_name == False:
                                    normal_func2()   
                                    
                            if opacity_text in i :
                                cut = i.partition('_' + opacity_text)
                                same_name = False
                                for b in phong_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_8
                                        same_name = True
                                        opacity_func2()
                                if same_name == False:
                                    opacity_func2() 
                                    
                            if 'opacity' in i:
                                cut = i.partition('_opacity')
                                same_name = False
                                for b in phong_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_8
                                        same_name = True
                                        opacity_func2()
                                if same_name == False:
                                    opacity_func2()        
                #RedshiftMaterial
                elif cmds.nodeType(selected_shader) == 'RedshiftMaterial':
                    my_array = ['.diffuse_color','.refl_roughness','.refl_metalness','.bump_input',
                    '.ms_amount', '.emission_color', '.refl_ior', '.opacity_color']
                    connected_1 = cmds.listConnections(selected_shader + my_array[0])
                    connected_2 = cmds.listConnections(selected_shader + my_array[1])
                    connected_3 = cmds.listConnections(selected_shader + my_array[2])
                    connected_4 = cmds.listConnections(selected_shader + my_array[3])
                    connected_5 = cmds.listConnections(selected_shader + my_array[4])
                    connected_6 = cmds.listConnections(selected_shader + my_array[5])
                    connected_7 = cmds.listConnections(selected_shader + my_array[6])
                    connected_8 = cmds.listConnections(selected_shader + my_array[7])
                    
                    connect_1 = cmds.listConnections(selected_shader2 + my_array[0])
                    connect_2 = cmds.listConnections(selected_shader2 + my_array[1])
                    connect_3 = cmds.listConnections(selected_shader2 + my_array[2])
                    connect_4 = cmds.listConnections(selected_shader2 + my_array[3])
                    connect_5 = cmds.listConnections(selected_shader2 + my_array[4])
                    connect_6 = cmds.listConnections(selected_shader2 + my_array[5])
                    connect_7 = cmds.listConnections(selected_shader2 + my_array[6])
                    connect_8 = cmds.listConnections(selected_shader2 + my_array[7])
                    
                    names = cmds.ls(selection = True, type = 'file')
                    if default_shader == redshift:
                        for i in names:
                            if color_text in i:
                                cut = i.partition('_Base_' + color_text)
                                same_name = False
                                for b in redshift_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_1
                                        same_name = True
                                        color_func2('.diffuse_color')
                                        cmds.setAttr(selected_shader2 + '.refl_brdf', default_BRDF)
                                if same_name == False:
                                    if material_suffix in cut[0]:
                                        obj_shad_name = cut[0]
                                    else:
                                        obj_shad_name = cut[0] + material_suffix
                                    selected_shader2 = cmds.shadingNode(redshift, asShader = True, name = obj_shad_name)
                                    if cut[0] in selected_shader2:
                                        extra = cmds.listConnections(selected_shader2 + '.outColor')
                                        shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                                        cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                                        color_func2('.diffuse_color')      
                                        cmds.setAttr(selected_shader2 + '.refl_brdf', default_BRDF)
                                        
                            if color_alt_text in i:
                                cut = i.partition('_' + color_alt_text)
                                same_name = False
                                for b in redshift_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_1
                                        same_name = True
                                        color_func2('.diffuse_color')
                                        cmds.setAttr(selected_shader2 + '.refl_brdf', default_BRDF)
                                if same_name == False:
                                    if material_suffix in cut[0]:
                                        obj_shad_name = cut[0]
                                    else:
                                        obj_shad_name = cut[0] + material_suffix
                                    selected_shader2 = cmds.shadingNode(redshift, asShader = True, name = obj_shad_name)
                                    if cut[0] in selected_shader2:
                                        extra = cmds.listConnections(selected_shader2 + '.outColor')
                                        shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                                        cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                                        color_func2('.diffuse_color')  
                                        cmds.setAttr(selected_shader2 + '.refl_brdf', default_BRDF)                                  
                                    
                            if roughness_text in i:
                                cut = i.partition( '_' + roughness_text)
                                same_name = False
                                for b in redshift_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_2
                                        same_name = True
                                        roughness_func2('.refl_roughness')
                                if same_name == False:
                                    roughness_func2('.refl_roughness')
                                    
                            if roughness_alt_text in i:
                                cut = i.partition( '_' + roughness_alt_text)
                                same_name = False
                                for b in redshift_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_2
                                        same_name = True
                                        roughness_func2('.refl_roughness')
                                if same_name == False:
                                    roughness_func2('.refl_roughness')
                                    
                            if metal_text in i:
                                cut = i.partition('_' + metal_text)
                                same_name = False
                                for b in redshift_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_3
                                        same_name = True
                                        metal_func2('.refl_metalness')
                                        cmds.setAttr(selected_shader2 + '.refl_fresnel_mode', 2)
                                if same_name == False:
                                    metal_func2('.refl_metalness')
                                    cmds.setAttr(selected_shader2 + '.refl_fresnel_mode', 2)
                                    
                            if metal_alt_text in i:
                                cut = i.partition('_' + metal_alt_text)
                                same_name = False
                                for b in redshift_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_3
                                        same_name = True
                                        metal_func2('.refl_metalness')
                                        cmds.setAttr(selected_shader2 + '.refl_fresnel_mode', 2)
                                if same_name == False:
                                    metal_func2('.refl_metalness')
                                    cmds.setAttr(selected_shader2 + '.refl_fresnel_mode', 2)
                                
                            if normal_text in i:
                                cut = i.partition('_' + normal_text)
                                same_name = False
                                for b in redshift_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_4
                                        same_name = True
                                        rs_normal_func2()
                                if same_name == False:
                                    rs_normal_func2() 
                                 
                            if scatter_text in i:
                                cut = i.partition('_' + scatter_text)
                                same_name = False
                                for b in redshift_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_5
                                        same_name = True
                                        scatter_func2('.ms_amount')
                                if same_name == False:
                                    scatter_func2('.ms_amount')
                                     
                            if emissive_text in i:
                                cut = i.partition('_' + emissive_text)
                                same_name = False
                                for b in redshift_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_6
                                        same_name = True
                                        emissive_func2('.emission_color')
                                if same_name == False:
                                    emissive_func2('.emission_color')
                                
                            if ior_text in i:
                                cut = i.partition('_' + ior_text)
                                same_name = False
                                for b in redshift_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_7
                                        same_name = True
                                        ior_func2('.refl_ior')
                                if same_name == False:
                                    ior_func2('.refl_ior')
                                    
                            if 'Ior' in i:
                                cut = i.partition('_Ior')
                                same_name = False
                                for b in redshift_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_7
                                        same_name = True
                                        ior_func2('.refl_ior')
                                if same_name == False:
                                    ior_func2('.refl_ior')
                                    
                            if 'IOR' in i:
                                cut = i.partition('_IOR')
                                same_name = False
                                for b in redshift_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_7
                                        same_name = True
                                        ior_func2('.refl_ior')
                                if same_name == False:
                                    ior_func2('.refl_ior')
                                    
                            if opacity_text in i:
                                cut = i.partition('_' + opacity_text)
                                same_name = False
                                for b in redshift_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_8
                                        same_name = True
                                        opacity_func2('.opacity_color')
                                if same_name == False:
                                    opacity_func2('.opacity_color') 
                                    
                            if 'opacity' in i:
                                cut = i.partition('_opacity')
                                same_name = False
                                for b in redshift_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_8
                                        same_name = True
                                        opacity_func2('.opacity_color')
                                if same_name == False:
                                    opacity_func2('.opacity_color')
                            
    
                #lambert 
                elif cmds.nodeType(selected_shader) == 'lambert':
                    my_array = ['.baseColor','.specularRoughness','.metalness','.normalCamera',
                    '.subsurface', '.emissionColor', '.thinFilmIOR', '.opacity']
                    my_array[0] = '.color'
                    my_array[7] = '.transparency'
                    
                    connected_1 = cmds.listConnections(selected_shader + my_array[0])
                    connected_4 = cmds.listConnections(selected_shader + my_array[3])
                    connected_8 = cmds.listConnections(selected_shader + my_array[7])
                    
                    connect_1 = cmds.listConnections(selected_shader2 + my_array[0])
                    connect_4 = cmds.listConnections(selected_shader2 + my_array[3])
                    connect_8 = cmds.listConnections(selected_shader2 + my_array[7])
                    names = cmds.ls(selection = True, type = 'file')
                    if default_shader == lambert:
                        for i in names:
                            if color_text in i:
                                cut = i.partition('_Base_' + color_text)
                                same_name = False
                                for b in lambert_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_1
                                        same_name = True
                                        color_func2()
                                if same_name == False:
                                    if material_suffix in cut[0]:
                                        obj_shad_name = cut[0]
                                    else:
                                        obj_shad_name = cut[0] + material_suffix
                                    selected_shader2 = cmds.shadingNode(lambert, asShader = True, name = obj_shad_name)
                                    if cut[0] in selected_shader2:
                                        extra = cmds.listConnections(selected_shader2 + '.outColor')
                                        shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                                        cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                                        color_func2()     
                                        
                            if color_alt_text in i:
                                cut = i.partition('_' + color_alt_text)
                                same_name = False
                                for b in lambert_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_1
                                        same_name = True
                                        color_func2()
                                if same_name == False:
                                    if material_suffix in cut[0]:
                                        obj_shad_name = cut[0]
                                    else:
                                        obj_shad_name = cut[0] + material_suffix
                                    selected_shader2 = cmds.shadingNode(lambert, asShader = True, name = obj_shad_name)
                                    if cut[0] in selected_shader2:
                                        extra = cmds.listConnections(selected_shader2 + '.outColor')
                                        shadingEngine2 = cmds.sets(name = default_shadingEngine, empty=True, renderable=True, noSurfaceShader=True)
                                        cmds.connectAttr(selected_shader2 + '.outColor', shadingEngine2 + '.surfaceShader')
                                        color_func2()     
                                    
                            if normal_text in i:
                                cut = i.partition('_' + normal_text)
                                same_name = False
                                for b in lambert_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_4
                                        same_name = True
                                        normal_func2()
                                if same_name == False:
                                    normal_func2()   
                                    
                            if opacity_text in i:
                                cut = i.partition('_' + opacity_text)
                                same_name = False
                                for b in lambert_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_8
                                        same_name = True
                                        opacity_func2()
                                if same_name == False:
                                    opacity_func2()        
                                    
                            if 'opacity' in i:
                                cut = i.partition('_opacity')
                                same_name = False
                                for b in lambert_shaders:
                                    if cut[0] in b:
                                        selected_shader2 = b
                                        connect_8
                                        same_name = True
                                        opacity_func2()
                                if same_name == False:
                                    opacity_func2()     
                else:
                    cmds.warning('Please select your file(s) and a shader.')
        
        while counter < number_of_shaders:
            delete_shader(shaders_list[counter], shaders_color_list[counter])
            counter = counter + 1
        
        
        arnold_final_shaders = cmds.ls(type = arnold)
        blinn_final_shaders = cmds.ls(type = blinn)
        phong_final_shaders = cmds.ls(type = phong)
        redshift_final_shaders = cmds.ls(type = redshift)
        lambert_final_shaders = cmds.ls(type = lambert)
        
        object_suf_len = len(object_suffix)
        object_names = cmds.ls(type = 'transform')
        shader_arnold_len = len(arnold_final_shaders)
        shader_blinn_len = len(blinn_final_shaders)
        shader_phong_len = len(phong_final_shaders)
        shader_redshift_len = len(redshift_final_shaders)
        shader_lambert_len = len(lambert_final_shaders)
    
        var = 0
        if object_material_connect == True:
            if default_shader == arnold:
                while var < shader_arnold_len:
                    for b in object_names:
                        c = b.partition(object_suffix)[0]
                        # get materails names and its shader to sets 
                        if c in arnold_final_shaders[var]:
                            #find out for b and use that instead
                            test = cmds.listConnections((arnold_final_shaders[var]) + '.outColor')[0]
                            cmds.select(b)
                            check = cmds.sets(e = True, forceElement = test)   
                    var = var + 1  
                   
            elif default_shader == blinn:
                while var < shader_blinn_len:
                    for b in object_names:
                        c = b.partition(object_suffix)[0]
                        # get materails names and its shader to sets 
                        if c in blinn_final_shaders[var]:
                            #find out for b and use that instead
                            test = cmds.listConnections((blinn_final_shaders[var]) + '.outColor')[0]
                            cmds.select(b)
                            check = cmds.sets(e = True, forceElement = test)   
                    var = var + 1  
           
            elif default_shader == phong:
                while var < shader_phong_len:
                    for b in object_names:
                        c = b.partition(object_suffix)[0]
                        # get materails names and its shader to sets 
                        if c in phong_final_shaders[var]:
                            #find out for b and use that instead
                            test = cmds.listConnections((phong_final_shaders[var]) + '.outColor')[0]
                            cmds.select(b)
                            check = cmds.sets(e = True, forceElement = test)   
                    var = var + 1  
                    
            elif default_shader == redshift:
                while var < shader_redshift_len:
                    for b in object_names:
                        c = b.partition(object_suffix)[0]
                        # get materails names and its shader to sets 
                        if c in redshift_final_shaders[var]:
                            #find out for b and use that instead
                            test = cmds.listConnections((redshift_final_shaders[var]) + '.outColor')[0]
                            cmds.select(b)
                            check = cmds.sets(e = True, forceElement = test)   
                    var = var + 1  
                    
            elif default_shader == lambert:
                while var < shader_lambert_len:
                    for b in object_names:
                        c = b.partition(object_suffix)[0]
                        # get materails names and its shader to sets 
                        if c in lambert_final_shaders[var]:
                            #find out for b and use that instead
                            test = cmds.listConnections((lambert_final_shaders[var]) + '.outColor')[0]
                            cmds.select(b)
                            check = cmds.sets(e = True, forceElement = test)   
                    var = var + 1  
        
        
        
            
            
        


















   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
        


