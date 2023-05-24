import maya.cmds as cmds


mayaVersion = int( str(cmds.about(api=True))[0:4] )
hmDockWinInterName = "hardMeshWorkspaceWindow"


def deleteUI():
    # Delete the workflow window if existing
    #
    if mayaVersion >= 2017:
        if cmds.workspaceControl(hmDockWinInterName, exists=True):
            cmds.deleteUI(hmDockWinInterName)
    else:
        if cmds.dockControl(hmDockWinInterName, exists =True):
            cmds.deleteUI(hmDockWinInterName)


    # Delete always the menu
    #
    cmds.deleteUI("hmMenuBar")
