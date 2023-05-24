import maya.cmds as cmds
import inspect
from functools import partial


class attrManager():
    def __init__(self):
        print "Attribute Manager v 1.5.5 by VK (vk.vkpost@gmail.com | behance.net/vkpost)"
        self.sel                = cmds.ls(sl=1, l=1)
        self.sel_shapes         = []
        self.sel_shapes_count   = 0
        
        self.convertSelectionToShapes(self.sel)
        
        # ATTRIBUTES
        self.RenderAttributes = {}        
        self.RenderAttributes['Maya'] = [   ("Primary Visibility",      "primaryVisibility",        'bool',     'Root'),
                                            ("Cast Shadows",            "castsShadows",             'bool',     'Root'),
                                            ("Recieve Shadows",         "receiveShadows",           'bool',     'Root'),
                                            ("Hold-Out",                "holdOut",                  'bool',     'Root'),
                                            ("Motion Blur",             "motionBlur",               'bool',     'Root'),                                            
                                            ("Smooth Shading",          "smoothShading",            'bool',     'Root'),
                                            ("Visible In Reflections",  "visibleInReflections",     'bool',     'Root'),
                                            ("Visible In Refractions",  "visibleInRefractions",     'bool',     'Root'),
                                            ("Double Sided",            "doubleSided",              'bool',     'Root'),
                                            ("Opposite",                "opposite",                 'bool',     'Root'),
                                            ("Display Subdivisions",    "displaySubdComps",         'bool',     'Tessellation'),
                                            ("Preview Divisions Level", "smoothLevel",              'short',    'Tessellation'),
                                            ("Preview Level for Render","useSmoothPreviewForRender",'bool',     'Tessellation'),
                                            ("Render Divisions Level",  "renderSmoothLevel",        'short',    'Tessellation'),
                                            #("Subdivision Method",      "smoothDrawType",           'enum',     'Tessellation'),
                                            ("Display Immediate",       "displayImmediate",         'bool',     'Display'),
                                            ("Display Vertices",        "displayVertices",          'bool',     'Display'),
                                            ("Vertex Size",             "vertexSize",               'float',    'Display'),
                                            ("Backface Culling",        "backfaceCulling",          'enum',     'Display'),
                                            ("Display Edges",           "displayEdges",             'enum',     'Display'),
                                            ("Display Borders",         "displayBorders",           'bool',     'Display'),                                            
                                            ("Border Width",            "borderWidth",              'double',   'Display'),
                                            ("Display Center",          "displayCenter",            'bool',     'Display'),
                                            ("Display Triangles",       "displayTriangles",         'bool',     'Display'),
                                            ("Display UVs",             "displayUVs",               'bool',     'Display'),
                                            ("UV Size",                 "uvSize",                   'double',   'Display'),
                                                                                       
                                            ("Display Non Planar",      "displayNonPlanar",         'bool',     'Display'),
                                            ("Display Invisible Faces", "displayInvisibleFaces",    'bool',     'Display'),
                                            ("Display Colors",          "displayColors",            'bool',     'Display'),
                                            ("Display Normal",          "displayNormal",            'bool',     'Display'),
                                            ("Display Tangent",         "displayTangent",           'bool',     'Display'),
                                            ("Normal Size",             "normalSize",               'double',   'Display'),
                                            #("Normal Type",             "normalType",               'enum',     'Display'),
                                            
                                            ]
        
        self.attrs_shape_arnold = [('Self Shadows',             'aiSelfShadows'),
                                   ("Opaque",                   "aiOpaque"),
                                   ("Visible In Diffuse",       "aiVisibleInDiffuse"),
                                   ("Visible In Glossy",        "aiVisibleInGlossy"),
                                   ("Matte",                    "aiMatte")]
        
        
        
        self.RenderAttributes['Arnold'] = [ ('Translator',              'aiTranslator',             'string',   'Root'),
                                            ('Self Shadows',            'aiSelfShadows',            'bool',     'Root'),
                                            ('Opaque',                  'aiOpaque',                 'bool',     'Root'),
                                            ('Visible In Diffuse',      'aiVisibleInDiffuse',       'bool',     'Root'),
                                            ('Visible In Glossy',       'aiVisibleInGlossy',        'bool',     'Root'),
                                            ('Matte',                   'aiMatte',                  'bool',     'Root'),                                            
                                            ('Sss Setname',             'aiSssSetname',             'string',   'Root'),
                                            ('Motion Vector Source',    'aiMotionVectorSource',     'string',   'Root'),
                                            ('Motion Vector Unit',      'aiMotionVectorUnit',       'enum',     'Root'),
                                            ('Motion Vector Scale',     'aiMotionVectorScale',      'float',    'Root'),                                                                                       
                                            ('Trace Sets',              'aiTraceSets',              'string',   'Root'),                                            
                                            ('Color',                   'color',                    'float3',   'MeshLight'),
                                            ('Intensity',               'intensity',                'float',    'MeshLight'),
                                            ('Exposure',                'aiExposure',               'float',    'MeshLight'),
                                            ('Use Color Temperature',   'aiUseColorTemperature',    'bool',     'MeshLight'),
                                            ('Color Temperature',       'aiColorTemperature',       'float',    'MeshLight'),                                            
                                            ('Emit Diffuse',            'emitDiffuse',              'bool',     'MeshLight'),
                                            ('Emit Specular',           'emitSpecular',             'bool',     'MeshLight'),
                                            ('Light Visible',           'lightVisible',             'bool',     'MeshLight'),
                                            ('Decay Type',              'aiDecayType',              'enum',     'MeshLight'),
                                            ('Samples',                 'aiSamples',                'long',     'MeshLight'),
                                            ('Normalize',               'aiNormalize',              'bool',     'MeshLight'),                                            
                                            ('Cast Shadows',            'aiCastShadows',            'bool',     'MeshLight'),
                                            ('Shadow Density',          'aiShadowDensity',          'float',    'MeshLight'),
                                            ('Shadow Color',            'aiShadowColor',            'float3',   'MeshLight'),                                            
                                            ('Affect Volumetrics',      'aiAffectVolumetrics',      'bool',     'MeshLight'),
                                            ('Cast Volumetric Shadows', 'aiCastVolumetricShadows',  'bool',     'MeshLight'),
                                            ('Volume Samples',          'aiVolumeSamples',          'long',     'MeshLight'),
                                            #('Filters',                 'aiFilters',                'message',  'Root'),
                                            ('Diffuse',                 'aiDiffuse',                'float',    'MeshLight'),
                                            ('Specular',                'aiSpecular',               'float',    'MeshLight'),
                                            ('Sss',                     'aiSss',                    'float',    'MeshLight'),
                                            ('Indirect',                'aiIndirect',               'float',    'MeshLight'),
                                            ('Volume',                  'aiVolume',                 'float',    'MeshLight'),
                                            ('Max Bounces',             'aiMaxBounces',             'long',     'MeshLight'),                                            
                                            #('Aov',                     'aiAov',                    'string',   'Root'),
                                            

                                            ('Export Tangents',         'aiExportTangents',         'bool',     'Export'),
                                            ('Export Colors',           'aiExportColors',           'bool',     'Export'),
                                            ('Export Ref Points',       'aiExportRefPoints',        'bool',     'Export'),
                                            ('Export Ref Normals',      'aiExportRefNormals',       'bool',     'Export'),
                                            ('Export Ref Tangents',     'aiExportRefTangents',      'bool',     'Export'),
                                            
                                            ('Subdiv Type',             'aiSubdivType',             'enum',     'Subdivision'),
                                            ('Subdiv Iterations',       'aiSubdivIterations',       'byte',     'Subdivision'),
                                            ('Subdiv Adaptive Metric',  'aiSubdivAdaptiveMetric',   'enum',     'Subdivision'),
                                            ('Subdiv Pixel Error',      'aiSubdivPixelError',       'float',    'Subdivision'),
                                            ('Subdiv Adaptive Space',   'aiSubdivAdaptiveSpace',    'enum',     'Subdivision'),
                                            ('Subdiv Dicing Camera',    'aiSubdivDicingCamera',     'message',  'Subdivision'),
                                            ('Subdiv Uv Smoothing',     'aiSubdivUvSmoothing',      'enum',     'Subdivision'),
                                            ('Subdiv Smooth Derivs',    'aiSubdivSmoothDerivs',     'bool',     'Subdivision'),
                                            ('Disp Height',             'aiDispHeight',             'float',    'Displacement'),
                                            ('Disp Padding',            'aiDispPadding',            'float',    'Displacement'),
                                            ('Disp Zero Value',         'aiDispZeroValue',          'float',    'Displacement'),
                                            ('Disp Autobump',           'aiDispAutobump',           'bool',     'Displacement'),
                                            ('User Options',            'aiUserOptions',            'string',   'Volume'),
                                            ('Step Size',               'aiStepSize',               'float',    'Volume')
                                            ]
        
        
        #                            Normal Name                            Attrinute Name                Type        Group
        self.RenderAttributes['Redshift'] = [  ('Enable Visibility Overrides',      'rsEnableVisibilityOverrides',  'bool',     'Root'),
                                               ('Object Id',                        'rsObjectId',                   'long',     'Root'),
                                               ('Primary Ray Visible',              'rsPrimaryRayVisible',          'bool',     'General'),
                                               ('Secondary Ray Visible',            'rsSecondaryRayVisible',        'bool',     'General'),
                                               ('Casts Shadows',                    'rsShadowCaster',               'bool',     'General'),
                                               ('Receive Shadows',                  'rsShadowReceiver',             'bool',     'General'),
                                               ('Self-Shadows',                     'rsSelfShadows',                'bool',     'General'),
                                               ('Cast AO',                          'rsAOCaster',                   'bool',     'General'),
                                               ('Cast Reflections',                 'rsReflectionCaster',           'bool',     'Reflection And Refraction'),
                                               ('Visible in Reflections',           'rsReflectionVisible',          'bool',     'Reflection And Refraction'),
                                               ('Cast Refractions',                 'rsRefractionCaster',           'bool',     'Reflection And Refraction'),
                                               ('Visible in Refractions',           'rsRefractionVisible',          'bool',     'Reflection And Refraction'),
                                               ('Visible to Non-Photon GI',         'rsFgVisible',                  'bool',     'Global Illumination'),
                                               ('Visible to GI Photons',            'rsGiVisible',                  'bool',     'Global Illumination'),
                                               ('Visible to Caustic Photons',       'rsCausticVisible',             'bool',     'Global Illumination'),
                                               ('Receive GI Photons',               'rsFgCaster',                   'bool',     'Global Illumination'),
                                               ('Force Brute-Force GI',             'rsForceBruteForceGI',          'bool',     'Global Illumination'),
                                               ('Cast GI Photons',                  'rsGiCaster',                   'bool',     'Global Illumination'),                                   
                                               ('Cast Caustic Photons',             'rsCausticCaster',              'bool',     'Global Illumination'),                                   
                                               ('Recieve GI Photons',               'rsGiReceiver',                 'bool',     'Global Illumination'),
                                               ('Receive Caustic Photons',          'rsCausticReceiver',            'bool',     'Global Illumination'),
                                               ('Matte Enable',                 'rsMatteEnable',                'bool',     'Matte'),
                                               ('Show Background',              'rsMatteShowBackground',        'bool',     'Matte'),
                                               ('Apply To Secondary Rays',      'rsMatteApplyToSecondaryRays',  'bool',     'Matte'),                                   
                                               ('Affected By Matte Lights',     'rsMatteAffectedByMatteLights', 'bool',     'Matte'),
                                               ('Alpha',                        'rsMatteAlpha',                 'double',   'Matte'),
                                               ('Reflection Scale',             'rsMatteReflectionScale',       'double',   'Matte'),
                                               ('Refraction Scale',             'rsMatteRefractionScale',       'double',   'Matte'),
                                               ('Diffuse Scale',                'rsMatteDiffuseScale',          'double',   'Matte'),
                                               ('Shadow Enable',                'rsMatteShadowEnable',          'bool',     'Matte'),
                                               ('Shadow Affects Alpha',         'rsMatteShadowAffectsAlpha',    'bool',     'Matte'),
                                               ('Shadow Color',                 'rsMatteShadowColor',           'float3',   'Matte'),
                                               ('Shadow Transparency',          'rsMatteShadowTransparency',    'double',   'Matte'),                                   
                                               
                                               ('Enable Tesselation',               'rsEnableSubdivision',          'bool',     'Tessellation'),
                                               ('Subdivision Rule',                 'rsSubdivisionRule',            'enum',     'Tessellation'),
                                               ('Screen Space Adaptive',            'rsScreenSpaceAdaptive',        'bool',     'Tessellation'),
                                               ('Smooth Subdivision',               'rsDoSmoothSubdivision',        'bool',     'Tessellation'),
                                               ('Min Edge Length',                  'rsMinTessellationLength',      'double',   'Tessellation'),
                                               ('Max Subdivs',                      'rsMaxTessellationSubdivs',     'long',     'Tessellation'),
                                               ('Out Of Frustum Tess. Factor',      'rsOutOfFrustumTessellationFactor','double','Tessellation'),
                                               
                                               ('Enable Displacement',              'rsEnableDisplacement',         'bool',     'Displacement'),
                                               ('Max Displacement',                 'rsMaxDisplacement',            'double',   'Displacement'),
                                               ('Displacement Scale',               'rsDisplacementScale',          'double',   'Displacement'),
                                               ('Auto Bump Mapping',                'rsAutoBumpMap',                'bool',     'Displacement')                                   
                                   ]
        
        self.group_order = [('Root',                        0),
                            ('General',                     1),
                            ('MeshLight',                   1),
                            ('Display',                     1),
                            ('Reflection And Refraction',   3),
                            ('Global Illumination',         5),
                            ('Matte',                       7),
                            ('Tessellation',                9),
                            ('Subdivision',                 9),
                            ('Displacement',                11),
                            ('Volume',                      13),
                            ('Export',                      13)
                            ]
        
        
        # CREATE Structure : GROUP > SubGroup > [name, attr, type]
        self.ATTRS = {a : None for a in self.RenderAttributes}
        for group in self.ATTRS:
            sub_groups = list(set([a[3] for a in self.RenderAttributes[group]]))
            self.ATTRS[group] = {group : list() for group in sub_groups}
           
            for name, attr, type, sub_group in self.RenderAttributes[group]:
                self.ATTRS[group][sub_group].append([name, attr, type])
          
        
        #UI
        self.UI                 = {}
        self.UIframe_layouts    = {}
        self.window             = None
        self.win_main_id        = "attrManager1550"
        self.win_main_title     = 'VK Attribute Manager 1.5.5'
        self.win_main_width     = 350
        self.win_main_height    = 400
        
        
        self.ui_colors          = {'frame_RSA'      : (.3, .4, .3),
                                   'frame_CA'       : (.3, .3, .4),
                                   'frame_ARA'      : (.25, .3, .5),
                                   'frame_RRA'      : (.5, .2, .2),
                                   'frame_RRA_sub'  : (.5, .25, .25),
                                   'sep_ON'         : (.4, .85, .0),
                                   'sep_OFF'        : (.85, .0, .0),
                                   'sep_MIX'        : (.85, .9, .0),
                                   'sep_DEF'        : (.3, .3, .3),
                                   'rcl_DEF'        : (.27, .27, .27),                                   
                                   'rcl_WARN'       : (.7, .27, .7),
                                   'btn_ON'         : (.2, .49, .1),                                   
                                   'btn_OFF'        : (.49, .1, .15),
                                   'btn_GRAY'       : (.3, .3, .3),
                                   'btn_sel_ON'     : (.2, .4, .4),
                                   'btn_sel_OFF'    : (.4, .2, .4)}
        self.ui_colors_frame    = {'Maya'       : [(.25, .5, .1),    (.35, .5, .2)],
                                   'Arnold'     : [(.25, .3, .5),   (.33, .4, .5)],
                                   'Redshift'   : [(.5, .2, .2),    (.5, .25, .25)]
                                   
                                   }
        
        
        self.UInames = ('update_UI_SRA_ARA',
                        'update_UI_RRA')
    
        self.mkUI()        
    
    def mkUI(self):
        #print 'FN: "' + inspect.stack()[0][3] + '"'
        dot_size_x = 10
        dot_size_y = 10
        
        if cmds.window(self.win_main_id, exists = 1): cmds.deleteUI(self.win_main_id)
        self.window = window = cmds.window(self.win_main_id, 
                                           title      = self.win_main_title,
                                           w          = self.win_main_width,
                                           h          = self.win_main_height,
                                           mnb        = 1, 
                                           mxb        = 1,
                                           titleBar   = 1,                                                        
                                           sizeable   = 1)
        
        main_layout = cmds.rowColumnLayout(w=self.win_main_width, parent = window)
        rcl_info = cmds.rowColumnLayout(parent=main_layout)        
        self.UI['txt_sel_shapes'] = cmds.text(parent=rcl_info, font='boldLabelFont', backgroundColor=(self.ui_colors['rcl_DEF']))

        
        # BUILD -->
        for group in self.RenderAttributes:
            collapse = 1
            sub_collapse = 1
            #if group == 'Arnold': collapse = 0; 
            
            # colors
            group_color     = self.ui_colors_frame[group][0]
            sub_group_color = self.ui_colors_frame[group][1]
            
            # MAIN FRAMES           
            self.UIframe_layouts[group] = frame = cmds.frameLayout(l=group, 
                                                                   w=self.win_main_width, 
                                                                   collapsable = 1, 
                                                                   collapse=collapse,
                                                                   marginWidth = 10,
                                                                   parent=main_layout, 
                                                                   backgroundColor=group_color,                                                                   
                                                                   collapseCommand = partial(self.command, 'resize_UI'))
            
            # get sub groups
            sub_groups = [[sub_group, i] for sub_group, i in self.group_order if sub_group in self.ATTRS[group]]
            
            
            # Create UI Frames        
            for sub_group, index in sub_groups:
                frame_name = group+'_'+sub_group
                
                if index == 0:  self.UIframe_layouts[frame_name] = cmds.rowColumnLayout(parent=frame)                    
                if index != 0:  self.UIframe_layouts[frame_name] = cmds.frameLayout(l=sub_group, 
                                                                                    w=self.win_main_width, 
                                                                                    collapsable = 1, 
                                                                                    collapse=sub_collapse,                                                                                    
                                                                                    parent=frame, 
                                                                                    backgroundColor=sub_group_color,                                                                        
                                                                                    collapseCommand = partial(self.command, 'resize_UI'))

                parent_dst = self.UIframe_layouts[frame_name]
                
                
                for name, attr, type in self.ATTRS[group][sub_group]:                
                    if type == 'bool':
                        line_height = 18
                        self.UI['rcl_' + attr]   = cur_line =   cmds.rowLayout(parent=parent_dst, nc=8, h=line_height)
                        self.UI['txt_' + attr]              =   cmds.text(parent=cur_line, l="  "+ name, w=150, align='left', h=line_height)
                        self.UI['sep_' + attr]              =   cmds.separator(parent=cur_line, w=dot_size_x, h=dot_size_y, backgroundColor=(.5, .5, .5), style='none')
                        cmds.separator(parent=cur_line, w=5, h=line_height, style='none')
                        self.UI['btn_ON_' + attr]           =   cmds.button(parent=cur_line, l='ON',    h=line_height, w=30,    c=partial(self.command, 'ATTR_set_'+attr+'_1'), backgroundColor = self.ui_colors['btn_ON'])
                        self.UI['btn_OFF_' + attr]          =   cmds.button(parent=cur_line, l='OFF',   h=line_height, w=30,    c=partial(self.command, 'ATTR_set_'+attr+'_0'), backgroundColor = self.ui_colors['btn_OFF'])
                        cmds.separator(parent=cur_line, w=35,   h=3, style='none')                    
                        self.UI['btn_sel_OFF_' + attr]      =   cmds.button(parent=cur_line, l='OFF',   h=line_height, w=30,    c=partial(self.command, 'ATTR_sel_'+attr+'_0'), backgroundColor = self.ui_colors['btn_sel_OFF'])
                        self.UI['btn_sel_ON_' + attr]       =   cmds.button(parent=cur_line, l='ON',    h=line_height, w=30,    c=partial(self.command, 'ATTR_sel_'+attr+'_1'), backgroundColor = self.ui_colors['btn_sel_ON'])                                    
                    if type == 'double' or type == 'float':
                        line_height = 20
                        self.UI['rcl_' + attr]   = cur_line =   cmds.rowLayout(parent=parent_dst, nc=7, h=line_height)
                        self.UI['txt_' + attr]              =   cmds.text(parent=cur_line, l="  "+ name, w=150, align='left', h=line_height)
                        self.UI['sep_' + attr]              =   cmds.separator(parent=cur_line, w=dot_size_x, h=dot_size_y, backgroundColor=(.5, .5, .5), style='none')
                        cmds.separator(parent=cur_line, w=5, h=line_height, style='none')
                        self.UI['flt_'+ attr]    =               cmds.floatField(parent=cur_line, h=line_height, w=50,    cc=partial(self.command, 'ATTR_set_'+attr+'_get_flt'))                    
                        cmds.separator(parent=cur_line, w=45, h=1, style='none')
                        cmds.button(parent=cur_line, l='Min',   h=line_height, w=30,    c=partial(self.command, 'ATTR_sel_'+attr+'_Min'), backgroundColor = self.ui_colors['btn_sel_OFF'])
                        cmds.button(parent=cur_line, l='Max',   h=line_height, w=30,    c=partial(self.command, 'ATTR_sel_'+attr+'_Max'), backgroundColor = self.ui_colors['btn_sel_ON'])                    
                    if type == 'long' or type == 'short':
                        line_height = 20
                        self.UI['rcl_' + attr]   = cur_line =   cmds.rowLayout(parent=parent_dst, nc=7, h=line_height)
                        self.UI['txt_' + attr]              =   cmds.text(parent=cur_line, l="  "+ name, w=150, align='left', h=line_height)
                        self.UI['sep_' + attr]              =   cmds.separator(parent=cur_line, w=dot_size_x, h=dot_size_y, backgroundColor=(.5, .5, .5), style='none')
                        cmds.separator(parent=cur_line, w=5, h=line_height, style='none')
                        self.UI['int_'+ attr]               =   cmds.intField(parent=cur_line, h=line_height, w=50,    cc=partial(self.command, 'ATTR_set_'+attr+'_get_int'))
                        cmds.separator(parent=cur_line, w=45, h=3, style='none')                    
                        cmds.button(parent=cur_line, l='Min',   h=line_height, w=30,    c=partial(self.command, 'ATTR_sel_'+attr+'_Min'), backgroundColor = self.ui_colors['btn_sel_OFF'])
                        cmds.button(parent=cur_line, l='Max',   h=line_height, w=30,    c=partial(self.command, 'ATTR_sel_'+attr+'_Max'), backgroundColor = self.ui_colors['btn_sel_ON'])
                    if type == 'float3':
                        line_height = 20
                        self.UI['rcl_' + attr]  = cur_line  =   cmds.rowLayout(parent=parent_dst, nc=4, h=line_height)
                        self.UI['txt_' + attr]              =   cmds.text(parent=cur_line, l="  "+ name, w=150, align='left', h=line_height)
                        self.UI['sep_' + attr]              =   cmds.separator(parent=cur_line, w=dot_size_x, h=dot_size_y, backgroundColor=(.5, .5, .5), style='none')
                        cmds.separator(parent=cur_line, w=5, h=line_height, style='none')                    
                        self.UI['col_' + attr]              =   cmds.colorSliderGrp(parent=cur_line, w=170, cc=partial(self.command, 'ATTR_set_'+attr+'_get_col'))                        
                    if type == 'enum':
                        line_height = 20
                        self.UI['rcl_' + attr]  = cur_line  =   cmds.rowLayout(parent=parent_dst, nc=6, h=line_height)
                        self.UI['txt_' + attr]              =   cmds.text(parent=cur_line, l="  "+ name, w=150, align='left', h=line_height)
                        self.UI['sep_' + attr]              =   cmds.separator(parent=cur_line,w=dot_size_x, h=dot_size_y, backgroundColor=(.5, .5, .5), style='none')
                        cmds.separator(parent=cur_line, w=5, h=line_height, style='none')
                        self.UI['opm_'+ attr]               =   cmds.optionMenu('SBD', parent = cur_line, w=165, cc=partial(self.command, 'ATTR_set_'+attr+'_get_opm')) 
        
        

            if group == 'Arnold' or group == 'Redshift':
                cmds.separator(parent = self.UIframe_layouts[group])
                # Hide Show Buttons
                buttons = cmds.rowLayout(parent=self.UIframe_layouts[group], nc=5, h=30)
                cmds.button(    parent = buttons, l='Hide '+ group[0:3] +' Attrs',  h = 20, w=80, c=partial(self.command, 'attrVisChange_'+group, 0), backgroundColor = self.ui_colors['btn_OFF'])
                cmds.separator( parent = buttons, w=50, style='none')    
                cmds.button(    parent = buttons, l='Show '+ group[0:3] +' Attrs',  h = 20, w=80, c=partial(self.command, 'attrVisChange_'+group, 1), backgroundColor = self.ui_colors['btn_ON'])
                if group == 'Redshift':
                    cmds.separator( parent = buttons, w=20, style='none')    
                    cmds.button(    parent = buttons, l='Show RS IDs',              h = 20, w=95, c=partial(self.command, 'attrVisChange_'+group, 2), backgroundColor = self.ui_colors['btn_ON'])

        
        cmds.button(parent = main_layout, l='Refresh', c=partial(self.command, 'reload_selection'))
        
        cmds.showWindow(window)
        cmds.window(window, e=True, w=self.win_main_width, h=10)
        #cmds.window(window, e=True, le=10, te=10)
        
        # add script job (p - parent)    
        cmds.scriptJob(e=["SelectionChanged", partial(self.command, "reload_selection")], parent = window)
        
        self.updUI()        
        
    
    def updUI(self, UIelement=None, val=None, *args, **kwargs):
        #print 'FN: "' + inspect.stack()[0][3] + '"', UIelement, val, args
        try:    el = self.UI[UIelement]
        except: el = None

        sep_color           = 'sep_DEF'
        rcl_color           = 'rcl_DEF'
        btn_On_color        = 'btn_ON'
        btn_Off_color       = 'btn_OFF'
        btn_Gray_color      = 'btn_GRAY'
        btn_Off_sel_color   = 'btn_sel_OFF'
        btn_On_sel_color    = 'btn_sel_ON'

        # update count
        cmds.text(self.UI['txt_sel_shapes'], e=1, l="  Shapes Selected:   " + str(self.sel_shapes_count))
        
                                           
        for group in self.ATTRS:
            for sub_group in self.ATTRS[group]:
                for element in self.ATTRS[group][sub_group]:       
                    name, attr, type = element
                    
                    txt_link = self.UI['txt_' + attr] if ('txt_' + attr) in self.UI else None
                    sep_link = self.UI['sep_' + attr] if ('sep_' + attr) in self.UI else None
                    rcl_link = self.UI['rcl_' + attr] if ('rcl_' + attr) in self.UI else None
                    flt_link = self.UI['flt_' + attr] if ('flt_' + attr) in self.UI else None
                    int_link = self.UI['int_' + attr] if ('int_' + attr) in self.UI else None
                    col_link = self.UI['col_' + attr] if ('col_' + attr) in self.UI else None
                    opm_link = self.UI['opm_' + attr] if ('opm_' + attr) in self.UI else None
                    btn_ON_link     = self.UI['btn_ON_'     + attr] if ('btn_ON_'       + attr) in self.UI else None                    
                    btn_OFF_link    = self.UI['btn_OFF_'    + attr] if ('btn_OFF_'      + attr) in self.UI else None
                    btn_OFF_sel_link= self.UI['btn_sel_OFF_'+ attr] if ('btn_sel_OFF_'  + attr) in self.UI else None
                    btn_ON_sel_link = self.UI['btn_sel_ON_' + attr] if ('btn_sel_ON_'   + attr) in self.UI else None
                    
                    
        
                    # process bools
                    if type == 'bool':
                        attr_info = self.getAttrInfo(attr)
                        if attr_info:                            
                            if attr_info[0] > 0     : sep_color = 'sep_ON'
                            if attr_info[0] == 0    : sep_color = 'sep_OFF'
                            if attr_info[1]         : sep_color = 'sep_MIX'                    
                            if attr_info[2]         : rcl_color = 'rcl_WARN'
                            
                            # Color elements
                            cmds.separator(sep_link, backgroundColor=self.ui_colors[sep_color], e=1)                        
                            cmds.text(txt_link, backgroundColor=self.ui_colors[rcl_color], e=1)
        
                            cmds.button(btn_OFF_link, e=1, backgroundColor=self.ui_colors[btn_Off_color], enable = 1)
                            cmds.button(btn_ON_link, e=1, backgroundColor=self.ui_colors[btn_On_color], enable = 1)
                            cmds.button(btn_OFF_sel_link, e=1, backgroundColor=self.ui_colors[btn_Off_sel_color], enable = 1)
                            cmds.button(btn_ON_sel_link, e=1, backgroundColor=self.ui_colors[btn_On_sel_color], enable = 1)
                            if attr_info[1] == None:                            
                                if attr_info[0] == 0: cmds.button(btn_OFF_link, e=1, backgroundColor=self.ui_colors[btn_Gray_color], enable=0)
                                if attr_info[0] == 1: cmds.button(btn_OFF_sel_link, e=1, backgroundColor=self.ui_colors[btn_Gray_color], enable=0)
                                if attr_info[0] == 1: cmds.button(btn_ON_link, e=1, backgroundColor=self.ui_colors[btn_Gray_color], enable=0)
                                if attr_info[0] == 0: cmds.button(btn_ON_sel_link, e=1, backgroundColor=self.ui_colors[btn_Gray_color], enable=0)
                                                        
                    if type == 'double' or type == 'float':
                        attr_info = self.getAttrInfo(attr)
                        if attr_info:                        
                            if attr_info[0] > 0     : sep_color = 'sep_ON'
                            if attr_info[0] == 0    : sep_color = 'sep_OFF'
                            if attr_info[1]         : sep_color = 'sep_MIX'                    
                            if attr_info[2]         : rcl_color = 'rcl_WARN'
                            
                            val = attr_info[1] if attr_info[1] != None else attr_info[0]
                            if val != None: cmds.floatField(flt_link, e=1, v=val)
                    
                    if type == 'long' or type == 'short':                        
                        attr_info = self.getAttrInfo(attr)
                        if attr_info:
                            if attr_info[0] > 0     : sep_color = 'sep_ON'
                            if attr_info[0] == 0    : sep_color = 'sep_OFF'
                            if attr_info[1]         : sep_color = 'sep_MIX'                    
                            if attr_info[2]         : rcl_color = 'rcl_WARN'
                        
                            val = attr_info[1] if attr_info[1] != None else attr_info[0]                        
                            if val != None: cmds.intField(int_link, e=1, v=val)                        
                            
                    if type == 'float3':
                        attr_info = self.getAttrInfo(attr)                   
                        if attr_info:
                            if attr_info[0] == None: attr_info[0] = (0,0,0)
                            
                            if sum(attr_info[0]) > 0    : sep_color = 'sep_ON'
                            if sum(attr_info[0]) == 0   : sep_color = 'sep_OFF'
                            if attr_info[1]             : sep_color = 'sep_MIX'                    
                            if attr_info[2]             : rcl_color = 'rcl_WARN'
                        
                            val = attr_info[1] if attr_info[1] else attr_info[0]                        
                            if val: cmds.colorSliderGrp(col_link, e=1, rgb=(val[0], val[1], val[2]))
                        
                    if type == 'enum':
                        attr_info = self.getAttrInfo(attr)                        
                        if attr_info and attr_info[0]:
                            # clear existing list items
                            opm_items = cmds.optionMenu(opm_link, q=1, itemListLong=1)                                                
                            if opm_items: [cmds.deleteUI(ui) for ui in opm_items] 
        
                            # Check for mixed values
                            if attr_info[1] == 'Mixed': attr_info[0] = ['Mixed'] + attr_info[0]
                            
                            # Create new list items                    
                            [cmds.menuItem(parent=opm_link, label=str(item)) for item in attr_info[0]]
                            
                            # Update UI
                            if attr_info[1] == 'Mixed': cmds.optionMenu(opm_link, e=1, v='Mixed'); sep_color = 'sep_MIX'
                            else:                       cmds.optionMenu(opm_link, e=1, v=attr_info[0][attr_info[1]])
                                        
                    # Color elements                    
                    if sep_link:    cmds.separator(sep_link, backgroundColor=self.ui_colors[sep_color], e=1)                        
                    if txt_link:    cmds.text(txt_link, backgroundColor=self.ui_colors[rcl_color], e=1)
                               
    
    def command(self, cmd=None, *args, **kwargs):
        #print 'FN: "' + inspect.stack()[0][3] + '"', cmd, args
        if cmd == 'reload_selection':
            #print 'reloading selection'
            self.sel = cmds.ls(sl=1)
            self.convertSelectionToShapes()            
            self.updUI()
            return True        
        
        if cmd == 'resize_UI':  cmds.window(self.window, e=1, h=10); return True
        
        if 'attrVisChange' in cmd:
            group = cmd.split('_')[1]            
            val = args[0]
            sel = self.sel_shapes if self.sel_shapes else cmds.ls(type='mesh', l=1)            
            for each in sel:                
                if val < 2:
                    for sub_group in self.ATTRS[group]:
                        for name, attr, type in self.ATTRS[group][sub_group]:
                            try: cmds.setAttr(each + "." + attr, keyable=val, channelBox=val)
                            except: cmds.warning('Unable to ' + ('hide', 'show')[val] + ' "' + attr +'" attribute for ' + each)
                            if type == 'float3':
                                for color in ('R', 'G', 'B'):
                                    try: cmds.setAttr(each + "." + attr + color, keyable=val, channelBox=val)
                                    except: cmds.warning('Unable to ' + ('hide', 'show')[val] + ' "' + attr +'" attribute for ' + each)
                            
                if val == 2: # Show rsObjectId attribute                            
                    try: cmds.setAttr(each + ".rsObjectId", keyable=1, channelBox=1)
                    except: cmds.warning('Unable to ' + ('hide', 'show')[val] + ' "' + attr +'" attribute for ' + each)
        
        new_sel         = []
        ui_to_update    = []
        do              = None
        attr            = None
        val             = None
        
                            
        # SET Render Attributes
        if "ATTR_set" in cmd[0:8] or 'ATTR_sel' in cmd[0:8]:
            
            ui_to_update.append('update_UI_RRA')
            
            cmd_parse   = cmd.split('_')
            do          = cmd_parse[1]
            attr        = cmd_parse[2]
            val         = cmd_parse[3]
                        
            try:    type = cmds.getAttr(self.sel_shapes[0] + '.' + attr, type=1)            
            except: return False          
                       
        
            # SET VALUES
            if do == 'set':
                for each in self.sel_shapes:
                    if val == 'get': # "READ UI Value"
                        for ui_name in self.UI:
                            if attr in ui_name:                        
                                if ui_name[0:3] == 'flt': val = cmds.floatField(self.UI[ui_name], q=1, v=1)
                                if ui_name[0:3] == 'int': val = cmds.intField(self.UI[ui_name], q=1, v=1)
                                if ui_name[0:3] == 'col': val = cmds.colorSliderGrp(self.UI[ui_name], q=1, rgb=1)
                                if ui_name[0:3] == 'opm': val = cmds.optionMenu(self.UI[ui_name], q=1, v=1)
                    
                    if type == 'float3':
                        try:    cmds.setAttr(each + '.' + attr, val[0], val[1], val[2])
                        except: cmds.warning('Unable to set "' + attr +'" attribute for ' + each)
                    elif type == 'enum':
                        attr_info = self.getAttrInfo(attr)
                        for i, item in enumerate(attr_info[0]):
                            if val == item: 
                                try:    cmds.setAttr(each + '.' + attr, i)
                                except: cmds.warning('Unable to set "' + attr +'" attribute for ' + each)
                    else:
                        try:    cmds.setAttr(each + '.' + attr, float(val))
                        except: cmds.warning('Unable to set "' + attr +'" attribute for ' + each)                
            
            
            # SELECT By Value
            if do == 'sel' and self.sel_shapes:                              
                min_value = cmds.getAttr(self.sel_shapes[0] + "." + attr)
                max_value = cmds.getAttr(self.sel_shapes[0] + "." + attr)
                
                if type == 'bool':
                    for each in self.sel_shapes:
                        try:    cur_val = cmds.getAttr(each + '.' + attr)                        
                        except: continue                        
                        if int(cur_val) == int(val): new_sel.append(each)
                if type == 'double' or type == 'float' or type == 'long':
                    # Get Min-Max
                    for each in self.sel_shapes:
                        cur_val = cmds.getAttr(each + '.' + attr)
                        if cur_val < min_value: min_value = cur_val
                        if cur_val > max_value: max_value = cur_val
                    # Add to selection list
                    for each in self.sel_shapes:
                        cur_val = cmds.getAttr(each + '.' + attr)
                        if val == 'Min' and cur_val == min_value: new_sel.append(each) 
                        if val == 'Max' and cur_val == max_value: new_sel.append(each)

        if do == 'sel':            
            if new_sel:
                self.sel = new_sel;
                self.convertSelectionToShapes()
                cmds.select(self.sel, r=1)
            else:               
                cmds.select(cl=1)
            
        
        # Update UI
        self.updUI()
    
    
    def convertSelectionToShapes(self, type=None):
        #print 'FN: "' + inspect.stack()[0][3] + '"', type
        
        self.sel_shapes = []
        all_descendents = []
        all_objects     = []
        for obj in self.sel: 
            if cmds.objectType(obj) == 'transform':     all_descendents = cmds.listRelatives(self.sel, allDescendents=1, pa=1, f=1)
            else:                                       all_objects.append(obj)

        all_objects = list(set(all_descendents) | set(all_objects))
        
        # filter shapes with Primary Visibilty attr 
        for obj in all_objects:
            if cmds.attributeQuery('primaryVisibility', node=obj, exists=1): self.sel_shapes.append(obj)

        if self.sel_shapes  : self.sel_shapes_count = len(self.sel_shapes)
        else                : self.sel_shapes_count = 0      

    def getAttrInfo(self, attr, sel=None):
        #print 'FN: "' + inspect.stack()[0][3] + '"', attr, sel
                        
        if sel == None: sel = self.sel_shapes
        if not sel: return False      
        
        result  = [None, None, 0]  # [ON/OFF, VALUE, ERROR]
        cur_val = None
        type    = None
        
        # get attr type
        try:    type = cmds.getAttr(sel[0] + '.' + attr, type=1)            
        except: result[2] += 1  # Error Attribute Reading       
               
        # get attr values
        val_bool        = []
        val_double      = []
        val_long        = []
        val_color       = []
        val_enum_list   = []
        val_enum_cur    = []
        for each in sel:
            if type == 'bool'   :   val_bool.append(int(cmds.getAttr(each + "." + attr)))                
            if type == 'double' :   val_double.append(cmds.getAttr(each + '.' + attr))
            if type == 'float'  :   val_double.append(cmds.getAttr(each + '.' + attr))
            if type == 'long'   :   val_long.append(int(cmds.getAttr(each + '.' + attr)))
            if type == 'short'  :   val_long.append(int(cmds.getAttr(each + '.' + attr)))                
            if type == 'float3' :   val_color.append(cmds.getAttr(each + '.' + attr)[0])
            if type == 'enum'   :                
                attr_values = cmds.attributeQuery(attr, node=each, listEnum=1)[0].split(":")
                cur_val_str = cmds.getAttr(each + '.' + attr, asString = 1)                
                
                # mk list of available attributes 
                [val_enum_list.append(x) for x in attr_values if x not in val_enum_list]
                # mk list of used attributes 
                [val_enum_cur.append(i) for i,x in enumerate(attr_values) if cur_val_str == x and i not in val_enum_cur]                
                """
                for i, x in enumerate(attr_values):                    
                    if cur_val_str == x and i not in val_enum_cur:
                        val_enum_cur.append(i)"""
                
        
       
        

        # procced result
        if type == 'bool':
            if min(val_bool) == max(val_bool):      result[0] = max(val_bool)                
            else:                                   result[1] = sum(val_bool) / float(len(sel))                
        if type == 'double' or type == 'float':
            if min(val_double) ==   max(val_double):    result[0] = max(val_double);
            else:                                       result[1] = sum(val_double) / float(len(sel))                
        if type == 'long' or type == 'short':
            if min(val_long) == max(val_long):  result[0] = max(val_long);
            else:                               result[1] = sum(val_long) / float(len(sel))
        if type == 'float3':
            min_color = (val_color[0])
            max_color = (val_color[0])
            sum_color = (0,0,0)
            avg_color = (0,0,0)
            for color in val_color:
                if color < min_color: min_color = color
                if color > max_color: max_color = color
                sum_color = (sum_color[0] + color[0], sum_color[1] + color[1], sum_color[2] + color[2])
                avg_color = ((avg_color[0] + color[0] / float(len(sel))), (avg_color[1] + color[1] / float(len(sel))), (avg_color[2] + color[2] / float(len(sel))))            
            if min_color == max_color: result[0] = max_color;
            else: result[1] = avg_color
        if type == 'enum': # RESULT = ([str(Values)], int(cur_value))
            cur_val = val_enum_cur[0] if len(val_enum_cur) <= 1 else 'Mixed'            
            result = [val_enum_list, cur_val]            

        
        return result

    

#am = attrManager()