import os
import hmScripts as root

root_path = root.__path__[0]
hm_templates_root = '%s/AETemplates' % root_path
# hmContextMenus = '%s/ContextMenu' % rootPath
maya_script_environ = 'MAYA_SCRIPT_PATH'

# -------------------------------------------------------------------------------------------------------------------- #
import hmScripts.UI.hmMenu as menu

def HM_UI():
    # Add the AE templates to script path...
    if not hm_templates_root in os.environ[maya_script_environ]:
        os.environ[maya_script_environ] += os.pathsep + hm_templates_root

    # Add the Context menus to script path...
    # if not hmContextMenus in os.environ[mayaScriptEnviron]:
    # 	os.environ[mayaScriptEnviron] += os.pathsep + hmContextMenus
        # print mayaScriptEnviron, os.environ[mayaScriptEnviron]

    menu.hmMenu()


