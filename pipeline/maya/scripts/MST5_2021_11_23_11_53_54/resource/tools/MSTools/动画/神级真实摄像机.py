import pymel.core as pmc


getTheCamPath = pmc.moduleInfo(mn='MS_Toolkit',p=True)+'/scripts/camRig.ma'


pmc.system.importFile(getTheCamPath,
                          loadReferenceDepth="all",
                          mergeNamespacesOnClash=False,
                          namespace='Cam_0001')

