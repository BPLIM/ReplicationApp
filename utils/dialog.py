# popups.py
import PySimpleGUI as sg
from typing import Tuple, Union, List, Dict
from .updateFields import enableDisableFields # window.disable() not working on linux

enableDisableExceptions = [
    'status',
    'time',
    'return'
]

def errorMessageBox(window: object, errors: Dict[str, List[str]], icon=bytes) -> None:
    """Display error message box

    Parameters
    ----------
    window : object
        Master window
    errors : Dict[str, List[str]]
        Dictionary with errors 
    icon: bytes
        Window icon
    """
    layout = list()
    for key in errors:
        layout.append([sg.Text(text=key)])
        for value in errors[key]:
            layout.append([sg.Text(text=f'    - {value}')])
    layout.append(
        [sg.Push(), sg.Button('Close', key='closeError'), sg.Push()]
    )
    errorWindow = sg.Window(
        title='Errors', 
        icon=icon,
        layout=layout, 
        auto_size_text=True,
        keep_on_top=True
    )
    
    enableDisableFields(
        window=window,
        exceptionKeys=enableDisableExceptions,
        enable=False
    )

    while True:
        event, _ = errorWindow.read()

        if event in (sg.WIN_CLOSED, 'closeError'):
            break 

    errorWindow.close()

    enableDisableFields(
        window=window,
        exceptionKeys=enableDisableExceptions,
        enable=True
    )
    window.bring_to_front()


def warningMessageBox(window: object, warnings: List[str],  icon=bytes) -> bool:
    """Display warning message box. Asks the user if
    he or she wants to proceed

    Parameters
    ----------
    window : object
        Master window
    warnings : List[str]
        List of warnings
    icon: bytes
        Window icon

    Returns
    -------
    bool
        True if the user wants to continue
    """
    layout = list()
    for warning in warnings:
        layout.append([sg.Text(text=f'- {warning}')])
    layout = [
        *layout,
        [sg.VPush()],
        [sg.Text('Do you want to proceed with the replication?')],
        [sg.Push(), sg.Button('No'), sg.Button('Yes'), sg.Push()]
    ]
    warningWindow = sg.Window(
        title='Warnings', 
        layout=layout, 
        icon=icon,
        auto_size_text=True,
        keep_on_top=True,
        disable_close=True
    )
    
    enableDisableFields(
        window=window,
        exceptionKeys=enableDisableExceptions,
        enable=False
    )

    while True:
        event, _ = warningWindow.read()

        if event == 'Yes':
            proceed = True
            break 

        if event == 'No':
            proceed = False
            break 

    warningWindow.close()

    enableDisableFields(
        window=window,
        exceptionKeys=enableDisableExceptions,
        enable=True
    )
    window.bring_to_front()

    return proceed


def stopMessageBox(window: object,  icon=bytes) -> bool:
    """Display warning message box. Asks the user if
    he or she wants to kill the application

    Parameters
    ----------
    window : object
        Master window
    icon: bytes
        Window icon

    Returns
    -------
    bool
        True if the user wants to continue
    """
    layout = [
        [sg.Text('You are going to kill to replication. Continue?')],
        [sg.Push(), sg.Button('No'), sg.Button('Yes'), sg.Push()]
    ]
    warningWindow = sg.Window(
        title='Warning', 
        layout=layout, 
        icon=icon,
        auto_size_text=True,
        keep_on_top=True,
        disable_close=True
    )
    
    enableDisableFields(
        window=window,
        exceptionKeys=enableDisableExceptions,
        enable=False
    )

    while True:
        event, _ = warningWindow.read()

        if event == 'Yes':
            kill = True
            break 

        if event == 'No':
            kill = False
            break 

    warningWindow.close()

    enableDisableFields(
        window=window,
        exceptionKeys=enableDisableExceptions,
        enable=True
    )
    window.bring_to_front()

    return kill


def selectFile(
    title: str,
    fileTypes: Tuple[Tuple[str]],
    multipleFiles: bool = False
) -> Union[Tuple[str], str]:
    """Dialog box to select file or multiple
    files

    Parameters
    ----------
    title : str
        dialog box title
    fileTypes : Tuple[Tuple[str]]
        File types accepted
    multipleFiles : bool 
        Selects multiple files (default = False) 

    Returns
    -------
    Tuple[str] | str
        File or files selected ()
    """
    files = sg.PopupGetFile(
        title, 
        file_types=fileTypes,
        no_window=True, 
        multiple_files=multipleFiles
    )
    
    return files


def selectFolder(title: str) -> str:
    """Dialog box to select folder

    Parameters
    ----------
    title : str
        dialog box title

    Returns
    -------
    str
        Selected folder
    """
    folder = sg.PopupGetFolder(
        title, 
        no_window=True
    )
    
    return folder