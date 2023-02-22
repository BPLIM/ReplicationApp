import PySimpleGUI as sg

# Tooltips
mainPathTooltip = """Main directory of the replication. All sub-directories contained in 
this path will be copied to the directory of the replication. The 
main script and the dependencies must be found in this directory."""
mainScriptTooltip = """Main script for the replication. This is the entry point of the 
replication. It is the master file that runs the analysis and calls 
dependencies in case they exist. This file must be in the main 
directory, otherwise the replication will not run."""
containerImageTooltip = """Container to run the replication. Singularity image that contains 
the runtime used (Stata, R, Python, Julia) to run the analysis."""
containerDefTooltip = """Definition file used to create the container. This field is optional,
 but it is recommended that the user provides this file for 
reproducibility purposes."""
dependenciesTooltip = """Dependencies called by the main script. Every file used in the 
replication other than the main script and the files under the 
folders specified in the tools field should be included in this 
field. This field is optional because users are allowed to run 
the analysis from top to bottom in the main script"""
toolsTooltip = """This field is where the user specifies additional paths for third party
 tools or user-written commands (commands, modules, etc.). The 
 application creates a configuration file that points to these 
paths to use the tools inside them during the replication. If 
the path(s) is(are) under the main directory, the entire folder,
 as well as sub-folders and files are copied to the replication 
area. In this case the folder size cannot exceed 10MB."""

############################
########## Layout ##########
############################

# Main folder frame layout
mainFolderFrameLayout = [
    [sg.Text('[1] Select Main Path', text_color='white', expand_x=True)],
    [
        sg.Input(key='mainFolderInput', expand_x=True, tooltip=mainPathTooltip), 
        sg.Button(
            'Browse', 
            key='mainFolderBrowse', 
            tooltip='Ctrl+1', size=(8, 1), 
            button_color=('#FFFFFE', sg.theme_button_color_background())
        ),
        sg.Button('Remove', key='removeMainFolderInput', tooltip='Alt+1', size=(14, 1))
    ]
]

# Main script frame layout
mainScriptFrameLayout = [
    [sg.Text('[2] Select Main Script')],
    [
        sg.Input(key='mainScriptInput', expand_x=True, tooltip=mainScriptTooltip), 
        sg.Button('Browse', key='mainScriptBrowse', tooltip='Ctrl+2', size=(8, 1)),
        sg.Button('Remove', key='removeMainScriptInput', tooltip='Alt+2', size=(14, 1))
    ]    
]
# Container Image frame layout
containerImageFrameLayout = [
    [sg.Text('[3] Select Container Image')],
    [
        sg.Input(key='containerImage', expand_x=True, tooltip=containerImageTooltip), 
        sg.Button('Browse', key='containerImageBrowse', tooltip='Ctrl+3', size=(8, 1)),
        sg.Button('Remove', key='removeContainerImage', tooltip='Alt+3', size=(14, 1))
    ]    
]
# Container Image frame layout
containerDefinitionFrameLayout = [
    [sg.Text('[4] Select Definition File (Optional)')],
    [
        sg.Input(key='containerDefinition', expand_x=True, tooltip=containerDefTooltip), 
        sg.Button('Browse', key='containerDefinitionBrowse', tooltip='Ctrl+4', size=(8, 1)),
        sg.Button('Remove', key='removeContainerDefinition', tooltip='Alt+4', size=(14, 1))
    ]    
]
# Dependencies layout
dependenciesFrameLayout = [
    [sg.Text('[5] Select Dependencies (Optional)')],
    [
        sg.Listbox(
            [],
            key='dependencies', 
            select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED,
            expand_x=True,
            horizontal_scroll=True,
            size=(1, 6),
            tooltip=dependenciesTooltip
        ), 
        sg.Button('Browse', key='dependenciesBrowse', tooltip='Ctrl+5', size=(8, 1)),
        sg.Button('Remove Selected', key='removeDependencies', tooltip='Alt+5', size=(14, 1))
    ]    
]
# Tools
toolsFrameLayout = [
    [sg.Text('[6] Select Tools Folders (Optional)')],
    [
        sg.Listbox(
            [],
            key='tools', 
            select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED,
            expand_x=True,
            horizontal_scroll=True,
            size=(1, 3),
            tooltip=toolsTooltip
        ), 
        sg.Button('Browse', key='toolsBrowse', tooltip='Ctrl+6', size=(8, 1)),
        sg.Button('Remove Selected', key='removeToolsFolders', tooltip='Alt+6', size=(14, 1))
    ]    
]
# Run and load from File
outLayout = [
    [sg.VPush()],
    [
        sg.Push(), 
        sg.Button('Load From File', key='loadFromFile', tooltip='Ctrl+Shift+L', size=(16, 1)),
        sg.Button('Run', key='runStopApp', tooltip='Ctrl+Shift+R', size=(5, 1)),
        sg.Push()
    ],
    [sg.VPush()]
]
# Time 
timeLayout = [
    [sg.Push(), sg.Text('', font='Young 15', key='time'), sg.Push()]
]
# Status
statusLayout = [
    [sg.Push(), sg.Text('', font='Young 15', key='status'), sg.Push()]
]
# Return code
returnLayout = [
    [sg.Push(), sg.Text('', font='Young 15', key='return'), sg.Push()]
]