# check fields from ReplicationApp
import PySimpleGUI as sg
from typing import List, Tuple, Dict
import os
from pathlib import Path
from .dialog import errorMessageBox

# Maximum size for tools folder in MegaBytes
maxToolsSize = 10

def checkFields(window: object, values: dict) -> Tuple[List[str], Dict[str, List[str]]]:
    """Check if fields are correctly filled

    Parameters
    ----------
    window: object
        App window
    values : dict
        window values

    Returns
    -------
    Tuple[List[str], Dict[str, List[str]]]
        List of warnings and errors dictionary
    """
    errors = dict()
    warnings = list()
    ### Main folder ###
    flagMainFolder, errorsMainFolder = checkMainFolder(
        values['mainFolderInput']
    )
    if not flagMainFolder:
        errors['Main folder'] = errorsMainFolder
    ### Main script ###
    flagMainScript, errorsMainScript = checkMainScript(
        values['mainScriptInput'],
        values['mainFolderInput']
    )
    if not flagMainScript:
        errors['Main script'] = errorsMainScript
    ### Container image ### 
    flagContainerIMage, errorsContainerImage = checkContainerFiles(
        values['containerImage']
    )
    if not flagContainerIMage:
        errors['Container - Image'] = errorsContainerImage
    ### Container definition file ###
    definitionFile = values['containerDefinition']
    if definitionFile:
        flagContainerDefinition, errorsContainerDefinition = checkContainerFiles(
            definitionFile
        )
        if not flagContainerDefinition:
            errors['Container - Definition file'] = errorsContainerDefinition
    else:
        warnings.append('No definition file for container specified. This file is important for reproducibility purposes')
    ### Dependencies
    dependencies = window['dependencies'].get_list_values()
    if dependencies:
        flagDependencies, errorsDependencies = checkDependencies(
            dependencies,
            values['mainFolderInput']
        ) 
        if not flagDependencies:
            errors['Dependencies'] = errorsDependencies
    else:
        warnings.append('Dependencies field is empty')
    ### Tools
    tools = window['tools'].get_list_values()
    if tools:
        flagTools, errorsTools = checkTools(
            tools,
            values['mainFolderInput']
        ) 
        if not flagTools:
            errors['Tools'] = errorsTools

    return warnings, errors


def checkMainFolder(inputText: str) -> Tuple[bool, List[str]]:
    """Check main folder field

    Parameters
    ----------
    inputText : str
        field text

    Returns
    -------
    bool
        True if checks passed. If false return also the 
        errors (List of strings)
    """
    if isPathValid(inputText, file=False):
        return True, []
    return False, [f'"{inputText}" is not a valid folder']


def checkMainScript(inputText: str, mainFolder: str) -> Tuple[bool, List[str]]:
    """Check main folder field

    Parameters
    ----------
    inputText : str
        field text
    mainFolder : str
        Main folder

    Returns
    -------
    Tuple[bool, List[str]]
        True if checks passed. If false return also the 
        errors (List of strings)
    """
    flagErrors = []
    errorMessages = []
    # Check if file is valid
    flagPathValid = isPathValid(inputText)
    flagErrors.append(flagPathValid)
    if not flagPathValid:
        errorMessages.append(f'"{inputText}" is not a valid file')
    # Check if file is under main folder
    if mainFolder:
        flagFileUnderMain = isFileUnderMain(inputText, mainFolder, main=True)
        flagErrors.append(flagFileUnderMain)
        if not flagFileUnderMain:
            errorMessages.append(f'"{inputText}" not in main folder')
    else:
        flagErrors.append(False)
        errorMessages.append('Main folder not specified')

    return all(flagErrors), errorMessages


def checkContainerFiles(inputText: str) -> Tuple[bool, List[str]]:
    """Check main folder field

    Parameters
    ----------
    inputText : str
        field text

    Returns
    -------
    Tuple[bool, List[str]]
        True if checks passed. If false return also the 
        errors (List of strings)
    """
    if isPathValid(inputText):
        return True, []
    return False, [f'"{inputText}" is not a valid file']


def checkDependencies(dependencies: List[str], mainFolder: str) -> Tuple[bool, List[str]]:
    """Check main folder field

    Parameters
    ----------
    dependencies : LIst[str]
        list of dependencies
    mainFolder : str
        Main folder

    Returns
    -------
    Tuple[bool, List[str]]
        True if checks passed. If false return also the 
        errors (List of strings)
    """
    if mainFolder:
        flagErrors = []
        errorMessages = []
        for dependency in dependencies:
            flag = isFileUnderMain(dependency, mainFolder)
            if not flag:
                flagErrors.append(flag)
                errorMessages.append(f'"{dependency}" not in main folder')
                break
    else:
        return False, ['Main folder not specified']

    return all(flagErrors), errorMessages

def checkTools(tools: List[str], mainFolder: str) -> Tuple[bool, List[str]]:
    """Check main folder field

    Parameters
    ----------
    tools : List[str]
        list of paths for tools
    mainFolder : str
        Main folder
    Returns
    -------
    Tuple[bool, List[str]]
        True if checks passed. If false return also the 
        errors (List of strings)
    """
    flagErrors = []
    errorMessages = []
    for folder in tools:
        flag = isFileUnderMain(folder, mainFolder, folder=True)
        if flag:
            if getFolderSize(folder) > maxToolsSize:
                flagErrors.append(False)
                errorMessages.append(f'"{folder}" > {maxToolsSize}MB')

    return all(flagErrors), errorMessages

    
def isPathValid(path: str, file=True) -> bool:
    """Checks if a path is valid

    Parameters
    ----------
    path : str
        Path to be checked
    file: bool
        True if path is file

    Returns
    -------
    bool
        True if path is valid
    """
    if file:
        return os.path.isfile(path)
    return os.path.isdir(path)


def isFileUnderMain(file: str, mainFolder: str, main: bool = False, folder: bool = False) -> bool:
    """Check if file is under the main folder

    Parameters
    ----------
    file : str
        file to be inspected
    mainFolder : str
        main folder
    main : bool, optional
        True if main script under analysis, by default False
    folder : bool, optional
        True if file is a directory, by default False

    Returns
    -------
    bool
        True if file under main folder
    """
    if main:
        filesPath = [os.path.normcase(os.path.join(mainFolder, fileU)) for fileU in os.listdir(mainFolder)]
        return os.path.normcase(file) in filesPath
    else:
        if folder:
            dirsPath = list()
            for root, dirs, _ in os.walk(mainFolder):
                for directory in dirs:
                    dirsPath.append(os.path.normcase(os.path.join(root, directory)))

            return os.path.normcase(file) in dirsPath
        else:
            filesPath = list()
            for root, _, files in os.walk(mainFolder):
                for fileU in files:
                    filesPath.append(os.path.normcase(os.path.join(root, fileU)))

            return os.path.normcase(file) in filesPath

def getFolderSize(folder: str) -> float:
    """Returns the folder size in MB

    Parameters
    ----------
    folder : str
        folder

    Returns
    -------
    float
        size in MB
    """
    return sum(p.stat().st_size for p in Path(folder).rglob('*')) / (1024 ** 2)
