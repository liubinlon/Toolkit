#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import maya.cmds as cmds
from uuid import getnode
import hmLicense.pyLic as licModule
from hmScripts.hm_global_variables import language
from hmScripts.hm_global_variables import PLATFORMS, PUX_LICENSE_NAME, RLM_LICENSE_NAME

current_language = language.get()
win_title = language.values['install_win']['title']
descriptions = language.values['install_win']['descriptions']
labels = language.values['install_win']['labels']
result_string_val = language.values['install_win']['result_string']


class HmLicensingWindow:

    def __init__(self, hm_location):
        # Maya window UI vars
        self.winName = 'HmInstallationWin'
        self.winSize = [518, 600]
        self.rowSpacing = [100, 100, 10, 100]
        self.rowAttach = [(1, 'both', 10)]

        self.platform = PLATFORMS[licModule.get_sys()]
        self.splashImage = 'splashLogo.png'
        self.currentLocation = hm_location

        # UI elements to query from the commands
        self.subscription_lic_col = None
        self.subscriptionTextField = None
        self.lifetime_lic_col = None
        self.licenseTextField = None

        # Licensing files
        self.licensingClassRelPath = os.path.join('scripts', 'hmLicense', 'pyLic.py')

        # Store the directory
        self.install_path = os.path.dirname(self.currentLocation)

        # Create the image string
        self.splashImage = os.path.join(self.install_path, 'icons', self.splashImage)

        # Get the path for files
        self.mayaAppDir = cmds.internalVar(userAppDir=True)
        self.scriptsFolder = cmds.internalVar(usd=True)

        # Store the different mac addresses and stop the windows if there is an error
        error_messages = ''

        try:
            pux_mac_address_dll_folder = os.path.join(self.install_path, 'dll', self.platform)
            self.mac_address = licModule.get_mac(pux_mac_address_dll_folder)
            # Initialize the license class
            self.licClass = licModule.MyLic(self.mayaAppDir, self.mac_address)
        except Exception as e:
            error_messages += 'PUX mac error: {} \n'.format(e)

        try:
            mac = getnode()
            mactext = ("%012X" % mac).lower()
            self.rlm_mac_address = mactext
        except Exception as e:
            error_messages += 'RLM mac error: {} \n'.format(e)

        if error_messages:
            raise Exception(error_messages)

    def _showPermanentLic(self, *args):
        cmds.columnLayout(self.lifetime_lic_col, edit=True, visible=True)
        cmds.columnLayout(self.subscription_lic_col, edit=True, visible=False)

    def _showSubscriptionLic(self, *args):
        cmds.columnLayout(self.lifetime_lic_col, edit=True, visible=False)
        cmds.columnLayout(self.subscription_lic_col, edit=True, visible=True)

    # ---------------------------------------------------------------------------------------------------------------- #
    def createWin(self):
        """Build the Maya cmds window"""

        if cmds.window(self.winName, exists=True):
            cmds.deleteUI(self.winName)

        cmds.window(self.winName,
                    title=win_title,
                    width=self.winSize[0],
                    height= self.winSize[1],
                    resizeToFitChildren=False)

        # SPLASH IMAGE
        cmds.columnLayout(adjustableColumn=True, columnAlign='center')
        cmds.image( image= self.splashImage )
        cmds.setParent('..')

        # ------------------------------------------- LICENSING PART ------------------------------------------------- #
        cmds.setParent('..')
        lic_frame = cmds.frameLayout(label=labels['license_sect'], marginWidth=10, marginHeight = 10 )

        cmds.columnLayout(adjustableColumn=True, columnOffset=['both', 10], rowSpacing=3, visible=True)
        cmds.radioButtonGrp(numberOfRadioButtons=2,
                            label=labels['lic_type'],
                            labelArray2=[labels['radio_lic_pux'], labels['radio_lic_rlm']],
                            on1=self._showPermanentLic,
                            on2=self._showSubscriptionLic,
                            select=1)
        cmds.separator(horizontal=True, vis=True, w=300)
        cmds.setParent('..')

        # ------------------------------------------------- RLM ------------------------------------------------------ #
        self.subscription_lic_col = cmds.columnLayout(adjustableColumn=True,
                                                      columnOffset=['both', 10],
                                                      rowSpacing=3,
                                                      visible=False)
        cmds.rowLayout(numberOfColumns=1, rowAttach=[(1, 'both', 10)])
        cmds.text(label=descriptions['rlm_license'], align='left')
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, adj=2, rowAttach=[(1, 'both', 10)])
        cmds.text(label=labels['mac_address'])
        cmds.textField(text=self.rlm_mac_address, editable=True)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, columnWidth2=[100,100], adjustableColumn=2, rowAttach= [1, 'top', 3] )
        cmds.text(label='RLM License', align='left' )
        self.subscriptionTextField = cmds.scrollField( text='Paste Here your SINGLE license', h=100 )
        cmds.setParent('..')

        cmds.button(label=labels['activate_btn'], c=self.generateRlmLicense)
        cmds.setParent(lic_frame)

        # ------------------------------------------------- PUX ------------------------------------------------------ #
        self.lifetime_lic_col = cmds.columnLayout(adjustableColumn=True,
                                                  columnOffset=['both', 10],
                                                  rowSpacing=3,
                                                  visible=True)

        cmds.rowLayout(numberOfColumns=1, rowAttach=[(1, 'both', 10)])
        cmds.text(label = descriptions['license'], align='left')
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, columnWidth2=[100,100], adjustableColumn=2, rowAttach= self.rowAttach )
        cmds.text( label= labels['lic_num'], align='left' )
        self.licenseTextField = cmds.textField( text = labels['lic_def_txt'])
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, columnWidth2=[100,100], adjustableColumn=2, rowAttach= self.rowAttach )
        cmds.text(label=labels['mac_address'])
        cmds.textField(text=self.mac_address, editable=True)
        cmds.setParent('..')

        cmds.button(label=labels['activate_btn'], c=self.activatePermanentLicense)

        if current_language == language.SUPPORTED_LANGUAGES[1]:
            cmds.button(label=labels['deactivate_btn'], c=self.deactivatePermanentLicense)

        # ===========================================
        cmds.showWindow(self.winName)

    # ---------------------------------------------------------------------------------------------------------------- #
    def generateRlmLicense(self, *args):
        # Get the pasted license
        stringInput = cmds.scrollField(self.subscriptionTextField, q=True, text=True)

        if not stringInput:
            cmds.confirmDialog(title=labels['invalid_license'],
                               message=result_string_val['RLM_empty_field'],
                               button=[labels['ok']],
                               defaultButton=labels['ok'])
        else:
            print stringInput
            if 'LICENSE soupdev hardmesh' in stringInput:

                if self.rlm_mac_address in stringInput:

                    full_rlm_path = os.path.join(self.mayaAppDir, RLM_LICENSE_NAME)

                    with open(full_rlm_path, 'w') as rlm_file:
                        rlm_file.write(stringInput)

                        result = cmds.confirmDialog(title=labels['lic_file_created'],
                                                    message=result_string_val['RLM_lic_created'].format(full_rlm_path),
                                                    button=[labels['yes'], labels['no']],
                                                    defaultButton=labels['yes'],
                                                    cancelButton=labels['no'],
                                                    dismissString=labels['no'])

                        if result == labels['yes']:
                            cmds.evalDeferred("cmds.loadPlugin('hmTools')")

                else:
                    cmds.confirmDialog(title=labels['invalid_license'],
                                       message=result_string_val['RLM_mac_not_in_lic'].format(self.rlm_mac_address),
                                       button=[labels['ok']],
                                       defaultButton=labels['ok'])

            else:
                cmds.confirmDialog(title=labels['invalid_license'],
                                   message=result_string_val['RLM_invalid_lic'],
                                   button=[labels['ok']],
                                   defaultButton=labels['ok'])


    def activatePermanentLicense(self, *args):
        '''
        Perform the Hard Mesh licensing
        '''
        # read the pasted input
        stringInput = cmds.textField(self.licenseTextField, q=True, text = True )

        # ===== Valid license message
        writeLicense = True

        # Query If a license file already exist, and is associated with this computer
        # promt a message before overwriting
        if self.licClass.state:
            if self.mac_address == self.licClass.getLicense()['license']['mac']:
                writeLicense = cmds.confirmDialog(title=labels['license_found'],
                                                  message=descriptions['overwrite_license'] % (PUX_LICENSE_NAME,
                                                                                               self.mayaAppDir),
                                                  button=[labels['yes'], labels['no']],
                                                  defaultButton=labels['yes'],
                                                  cancelButton=labels['no'],
                                                  dismissString=labels['no'])

        if writeLicense:
            # Write the license
            licResult = self.licClass.activateLic(stringInput.strip())
            # TODO catch if lic result is None
            # print licResult, 'licResult'

            # If we recieve a True message from the activator
            if licResult[0]:
                result = cmds.confirmDialog(title=labels['confirm'],
                                            message=u'{} {}.\n'.format(stringInput, result_string_val['success_activate']),
                                            button=[labels['yes'], labels['no']],
                                            defaultButton=labels['yes'],
                                            cancelButton=labels['no'],
                                            dismissString=labels['no'])

                if result == labels['yes']:
                    cmds.loadPlugin('hmTools')

            # ===== Invalid license message
            else:
                cmds.confirmDialog(title=labels['invalid_license'],
                                   message = stringInput + licResult[1],
                                   button=[labels['ok']],
                                   defaultButton=labels['ok'] )


        else:
            cmds.warning(descriptions['lic_not_installed'])

    def deactivatePermanentLicense(self, *args):
        if not self.licClass.state:
            cmds.confirmDialog(title=labels['no_lic_on_machine'],
                               message=result_string_val['no_lic_on_machine_msg'],
                               button=[labels['ok']],
                               defaultButton=labels['ok'])
        else:
            curr_lic = self.licClass.getLicense()['license']
            key_to_deactivate = curr_lic['key']

            if curr_lic['mac'] == self.mac_address:
                result = self.licClass.deactivateLic(key_to_deactivate, curr_lic['mac'])

                if result[0] is True:

                    cmds.confirmDialog(title=labels['deactivated_successfully'],
                                       message=u'{} {}'.format(key_to_deactivate, labels['deactivated_successfully']),
                                       button=[labels['ok']],
                                       defaultButton=labels['ok'])

                else:
                    if result[1] == licModule.MyLic.DEACTIVATE_ON_INVALID_LICENSE:
                        cmds.confirmDialog(title=labels['unable_to_deactivate'],
                                           message=result_string_val['deactivation_on_wrong_lic'],
                                           button=[labels['ok']],
                                           defaultButton=labels['ok'])

                    elif result[1] == licModule.MyLic.DEACTIVATE_LIMIT_REACHED:
                        cmds.confirmDialog(title=labels['unable_to_deactivate'],
                                           message=result_string_val['deactivation_max_reach'],
                                           button=[labels['ok']],
                                           defaultButton=labels['ok'])

                    elif result[1] == licModule.MyLic.DEACTIVATE_ERROR:
                        cmds.confirmDialog(title=labels['unable_to_deactivate'],
                                           message=result_string_val['unable_deactivate_msg'],
                                           button=[labels['ok']],
                                           defaultButton=labels['ok'])
            else:
                cmds.confirmDialog(labels['no_valid_lic'],
                                   message=result_string_val['no_lic_to_deactiv'],
                                   button=[labels['ok']],
                                   defaultButton=labels['ok'])
