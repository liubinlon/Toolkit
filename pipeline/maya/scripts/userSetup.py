
from maya import cmds, mel, utils

def addPilelineMenuItem():
    if not cmds.about(batch=True):
        import generate_tools_menu
        reload(generate_tools_menu)
        generate_tools_menu.make_menu()
utils.executeDeferred(addPilelineMenuItem)
