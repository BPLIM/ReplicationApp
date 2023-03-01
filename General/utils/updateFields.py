# removeFields.py
from typing import List, Union
import json

def updateField(
    window: object,
    key: str,
    newValue: str
):
    """Updates an existing field

    Parameters
    ----------
    window: object:
        App window
    key: str
        field key
    newValue : str
        new value of the field
    """
    window[key].update(newValue)

def updateListboxItems(
    window: object,
    key: str,
    files: List[str] = None,
    append: bool = True
) -> None:
    """Updates items from a Listbox. If `files` is
    None, the selected values are removed

    Parameters
    ----------
    window : object
        App window
    key : str
        field key
    files : List[str], optional
        files to insert, by default None
    append: bool
        Append files to current listbox if True, by default True
    """
    currentFiles = window[key].get_list_values()
    if files:
        if append:
            for file in files:
                currentFiles.append(file)
            window[key].update(sorted(currentFiles))
        else:
            window[key].update(sorted(files))
    else:
        selectedIndexes = window[key].get_indexes()
        if selectedIndexes:
            newValues = [file for index, file in enumerate(currentFiles) if index not in selectedIndexes]
            window[key].update(sorted(newValues))

def enableDisableFields(
    window: object,
    exceptionKeys: List[str],
    enable: bool = False
) -> None:
    """Enable / disable fields 

    Parameters
    ----------
    window : object
        App window
    exceptionKeys : List[str]
        keys not to enable/disable
    enable : bool, optional
        enable fields, by default False;
    """
    disabled = not enable
    windowKeys = window.key_dict.keys()
    for field in windowKeys:
        if field not in exceptionKeys:
            window[field].update(disabled=disabled)


def setFromJson(window: object, jsonFile: str) -> None:
    """Sets App fields based on JSON file

    Parameters
    ----------
    window : object
        App window
    jsonFile : str
        path to JSON file
    """
    with open(jsonFile) as fieldsFile:
        data = json.load(fieldsFile)

    for key in data:
        window[key].update(data[key])

