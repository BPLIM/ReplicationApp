# BPLIM Replication App
import PySimpleGUI as sg
import platform
import time
import datetime
import os
import argparse
import re
import signal
from layout import (
    mainFolderFrameLayout,
    mainScriptFrameLayout,
    containerImageFrameLayout,
    containerDefinitionFrameLayout,
    dependenciesFrameLayout,
    toolsFrameLayout,
    outLayout,
    timeLayout,
    statusLayout,
    returnLayout
)
from utils.checks import checkFields
from utils.updateFields import (
    updateField,
    updateListboxItems,
    enableDisableFields,
    setFromJson
)
from utils.dialog import (
    selectFile,
    selectFolder,
    errorMessageBox,
    warningMessageBox,
    stopMessageBox
)
from utils.misc import convertFileToBase64
from replication import Replication


##### Globals #####
PY_SCRIPT_ABS_PATH, _ = os.path.split(os.path.abspath(__file__))
APP_RELATIVE_WIDTH = 0.6
APP_RELATIVE_HEIGHT = 0.5 if platform.system() == "Windows" else 0.4
PROJECT_REGULAR_EXPRESSION = r'p(\d{3}|xxx)_[a-zA-Z]+'
STATA_ERROR_REGEX = "^r\(([0-9]+)\);"
APP_LOGO_ENCODED = convertFileToBase64(os.path.join(PY_SCRIPT_ABS_PATH, '.images/appLogo.gif'))
WARNING_ICON_ENCODED = convertFileToBase64(os.path.join(PY_SCRIPT_ABS_PATH, '.images/warning.gif'))
ERROR_ICON_ENCODED = convertFileToBase64(os.path.join(PY_SCRIPT_ABS_PATH, '.images/error.gif'))

# Allowed types for main script
mainScriptFileTypes = ( 
    ('Do-file (*.do)', '*.do'),
    ('Python file (*.py)', '*.py'),
    ('R file (*.R)', '*.R'),
    ('Julia file (*.jl)', '*.jl')
)
# Allowed types for dependencies
dependenciesFileTypes = (
    ('ALL Files (*.do; *.py; *.R; *.jl)', '*.do *.py *.R *.jl'), 
    ('Do-files (*.do)', '*.do'),
    ('Python files (*.py)', '*.py'),
    ('R files (*.R)', '*.R'),
    ('Julia files (*.jl)', '*.jl')
)
# Allowed types for container image
containerImageFileTypes = (
    ('Singularity image (*.sif)', '*.sif'),
)
# Allowed types for container definition file
containerDefinitionFileTypes = (
    ('Singularity definition file (*.def)', '*.def'),
)
# Allowed types for load from file button
loadFileTypes = (
    ('JSON file (*.json)', '*.json'),
)

parser = argparse.ArgumentParser("replicationApp.py")
required = parser.add_argument_group('required named arguments')
required.add_argument('-p', '--path', help='Replication path', required=False)
args = parser.parse_args()

if args.path:
    os.chdir(args.path)

appLayout = [
    *mainFolderFrameLayout,
    *mainScriptFrameLayout,
    *containerImageFrameLayout,
    *containerDefinitionFrameLayout,
    *dependenciesFrameLayout,
    *toolsFrameLayout,
    *outLayout,
    *timeLayout,
    *statusLayout,
    *returnLayout
]

# screenWidth, screenHeight = sg.Window.get_screen_size()
# appWidth = int(APP_RELATIVE_WIDTH * screenWidth)
# appHeight = int(APP_RELATIVE_HEIGHT * screenWidth)


window = sg.Window(
    'Replication - BPLIM', 
    appLayout,
    icon=APP_LOGO_ENCODED,
    #size=(appWidth, appHeight),
    resizable=True,
    finalize=True
)

# Buttons bindings
for i in range(1, 7):
    window.bind(f"<Control-KeyPress-{i}>", f"Ctrl-b-{i}")
    window.bind(f"<Alt-KeyPress-{i}>", f"Ctrl-r-{i}")

window.bind(f"<Control-Q>", "ctrl-shift-q")
window.bind(f"<Control-L>", "ctrl-shift-l")
window.bind(f"<Control-R>", "ctrl-shift-r")

running = False

while True:
    event, values = window.read(timeout=10)

    if event in (sg.WIN_CLOSED, 'ctrl-shift-q'):
        if running:
            killReplication = stopMessageBox(
                window=window,
                icon=WARNING_ICON_ENCODED
            )
            if killReplication:
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                break
        break 
    ##### Main folder #####
    
    # Select Input
    if event in ('mainFolderBrowse', 'Ctrl-b-1'):
        mainFolder = selectFolder('Select Folder')
        if mainFolder:
            updateField(
                window, key='mainFolderInput', newValue=mainFolder 
            )
    # Remove Input
    if event in ('removeMainFolderInput', 'Ctrl-r-1'):
        updateField(
            window, key='mainFolderInput', newValue='' 
        )  

    ##### Main script #####
    
    # Select Input
    if event in ('mainScriptBrowse', 'Ctrl-b-2'):
        mainScript = selectFile(
            title='Select File',
            fileTypes=mainScriptFileTypes
        )
        if mainScript:
            updateField(
                window, key='mainScriptInput', newValue=mainScript
            )
    # Remove Input
    if event in ('removeMainScriptInput', 'Ctrl-r-2'):
        updateField(
            window, key='mainScriptInput', newValue='' 
        )  

    ##### Container  Image #####

    # Select Input
    if event in ('containerImageBrowse', 'Ctrl-b-3'):
        containerImage = selectFile(
            title='Select File',
            fileTypes=containerImageFileTypes
        )
        if containerImage:
            updateField(
                window, key='containerImage', newValue=containerImage
            )
    # Remove Input
    if event in ('removeContainerImage', 'Ctrl-r-3'):
        updateField(
            window, key='containerImage', newValue='' 
        ) 

    ##### Container  Definition #####

    # Select Input
    if event in ('containerDefinitionBrowse', 'Ctrl-b-4'):
        containerDefinition = selectFile(
            title='Select File',
            fileTypes=containerDefinitionFileTypes
        )
        if containerDefinition:
            updateField(
                window, key='containerDefinition', newValue=containerDefinition
            )
    # Remove Input
    if event in ('removeContainerDefinition', 'Ctrl-r-4'):
        updateField(
            window, key='containerDefinition', newValue='' 
        ) 

    ##### Dependencies #####

    # Select inputs
    if event in ('dependenciesBrowse', 'Ctrl-b-5'):
        dependencies =  selectFile(
            "Select Files",
            fileTypes=dependenciesFileTypes,
            multipleFiles=True
        )
        if dependencies:
            updateListboxItems(
                window=window,
                key='dependencies',
                files=dependencies
            )
    # Remove inputs
    if event in ('removeDependencies', 'Ctrl-r-5'):
        updateListboxItems(
            window=window,
            key='dependencies'
        )

    ##### Tools #####

    # Select inputs
    if event in ('toolsBrowse', 'Ctrl-b-6'):
        toolsFolder =  selectFolder("Select Folder")
        if toolsFolder:
            updateListboxItems(
                window=window,
                key='tools',
                files=[toolsFolder]
            )
    # Remove inputs
    if event in ('removeToolsFolders', 'Ctrl-r-6'):
        updateListboxItems(
            window=window,
            key='tools'
        )

    ##### Load file and Run #####
    if event in ('loadFromFile', "ctrl-shift-l"):
        jsonFile = selectFile(
            'Select File',
            fileTypes=loadFileTypes
        )
        if jsonFile:
            setFromJson(
                window=window,
                jsonFile=jsonFile
            )

    ### Run and Stop App ###
    if event in ('runStopApp', "ctrl-shift-r"):
        if running:
            killReplication = stopMessageBox(
                window=window,
                icon=WARNING_ICON_ENCODED
            )
            if killReplication:
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                window['runStopApp'].update('Run')
                window['status'].update('Status: Interrupted')
                running = False
                enableDisableFields(
                    window=window,
                    exceptionKeys=['runStopApp', 'time', 'status', 'return'],
                    enable=True
                )
        else:
            proceed = False
            warnings, errors = checkFields(window, values)
            if errors:
                errorMessageBox(
                    window=window,
                    errors=errors,
                    icon=ERROR_ICON_ENCODED
                )
            else:
                if warnings:
                    proceed = warningMessageBox(
                        window=window,
                        warnings=warnings,
                        icon=WARNING_ICON_ENCODED
                    )
                else:
                    proceed = True
            if proceed:
                window['runStopApp'].update('Stop')
                window['status'].update('')
                window['return'].update('')
                running = True
                startTime = time.time()
                enableDisableFields(
                    window=window,
                    exceptionKeys=['runStopApp', 'time', 'status', 'return']
                )
                replication = Replication(window)
                process = replication.run()

    if running:
        elapsedTime = round(time.time() - startTime, 0)
        elapsedTimeFormatted = str(datetime.timedelta(seconds=elapsedTime))
        window['time'].update(f'Elapsed: {elapsedTimeFormatted}')
        if process.poll() is None:
            pass
        else:
            out, err = process.communicate()
            # the script is the last element of the process arguments
            script = process.args[-1]
            # Stata always return a code of 0, so we have to examine the log
            if script.endswith(".do"):
                log_file = script[:-3] + ".log"
                with open(log_file, 'r', encoding="latin-1") as f:
                    last_line = f.readlines()[-1]
                    error_match = re.search(STATA_ERROR_REGEX, last_line)
                    if error_match:
                        returnCode = 1
                    else:
                        returnCode = 0
            else:
                returnCode = process.returncode
            print(f"\nProcess {process.pid} finished")
            print(f"Return code: {returnCode}")
            if returnCode == 1:
                if script.endswith(".do"):
                    print("Errors:", last_line)
                else:
                    print("Errors:", err)
            print("Arguments: ", process.args)
            print("Main script directory:", os.getcwd())
            running = False
            window['runStopApp'].update('Run')
            enableDisableFields(
                window=window,
                exceptionKeys=['runStopApp', 'time', 'status', 'return'],
                enable=True
            )
            window['status'].update('Status: Finished')
            window['return'].update(f'Return code: {returnCode}')
            if returnCode == 0:
                replication.writeReport(startTime)

window.close()
