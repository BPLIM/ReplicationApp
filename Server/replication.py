# run.py
import PySimpleGUI as sg
import os
import shlex
import shutil
import re
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Union, Tuple, Generator, Any
from templates.stata import createProfile
from templates.rlang import createConfigFile as createRConfigFile
from utils.misc import tree

# Gobals
STATA_VERSION = 18
PROJECT_REGULAR_EXPRESSION = r'(p|r)(\d{3}|xxx)_[a-zA-Z]+'
# Use commands (Stata): key -> command; value -> regular expression
USE_COMMANDS = {
    "use": r"^use", 
    "using": " using ",
    "import": r"^import"
}
# Alert commands (Stata): key -> command; value -> regular expression
ALERT_COMMANDS = {
    "display": r"^dis?p?l?a?y? ",
    "list": r"^li?s?t? "
}

class Replication(object):
    """Class that handles the replication process
    """

    def __init__(self, window: sg.Window):

        self._window = window
        self._mainFolderPath = self._window['mainFolderInput'].get()
        self._mainScript = self._window['mainScriptInput'].get()
        self._containerImage = self._window['containerImage'].get()
        self._containerDef = self._window['containerDefinition'].get()
        self._dependencies = self._window['dependencies'].get_list_values()
        self._userDefinedTools, self._externalTools = self._splitToolsPaths()
        self._replicationPath = self._getReplicationPath()

    def _splitToolsPaths(self) -> Tuple[List[str]]:
        """Splits tools paths into user paths and 
        external paths

        Returns
        -------
        Tuple[List[str]]
            tuple with lists of paths
        """
        userDefinedTools = list()
        externalTools = list()
        toolsFolders = self._window['tools'].get_list_values()
        for folder in toolsFolders:
            if self.isFolderUnderMain(folder):
                userDefinedTools.append(folder)
            else:
                externalTools.append(folder)

        return userDefinedTools, externalTools

    def _getReplicationPath(self) -> str:
        """Getter for replication path

        Returns
        -------
        str
            Replication path
        """
        replicationFolderExists = self._replicationFolderExists(self._mainFolderPath)
        if not replicationFolderExists:
            repPath = self._makeDir(self._mainFolderPath, 'Replications')
            repPathNumber = self._makeDir(repPath, 'Rep001')
        else:
            repPath = os.path.join(self._mainFolderPath, 'Replications')
            repNumber = self._getReplicationNumber(repPath)
            repPathNumber  = self._makeDir(repPath, f'Rep{repNumber:03}')
 
        return repPathNumber

    def _replicationFolderExists(self, mainFolder) -> bool:
        """Verifies if there is a replication path set

        Parameters
        ----------
        mainFolder : str
            App main folder

        Returns
        -------
        bool
            True if replication folder already exists
        """
        return "Replications" in os.listdir(mainFolder)

    def _getReplicationNumber(self, replicationsPath: str) -> int:
        """Gets the number of the current replication

        Parameters
        ----------
        replicationsPath : str
            Path for replications

        Returns
        -------
        int
            Replication number
        """
        dirs = [file for file in os.listdir(replicationsPath) 
                if os.path.isdir(os.path.join(replicationsPath, file))]
        try:
            replicationNumber = max(
                [int(re.search(r'\d{3}', file)[0]) for file in dirs]
            ) + 1
        except ValueError:
            replicationNumber = 1

        return replicationNumber

    def _makeDir(self, base: str, folder: str) -> str:
        """Creates a new folder in a specified path

        Parameters
        ----------
        base : str
            path where the folder is going to be created
        folder : str
            folder to create

        Returns
        -------
        str
            folder created
        """
        os.mkdir(os.path.join(base, folder))
        
        return os.path.join(base, folder)
        
    def _getItems(self) -> Dict[str, Union[str, List[str]]]:
        """Gets main folder input

        Returns
        -------
        Dict[str, Union[str, List[str]]]
            Main entry path for replication
        """
        finalDict = {}
        windowDict = self._window.key_dict
        for key in windowDict.keys():
            if isinstance(windowDict[key], sg.Input):
                finalDict[key] = windowDict[key].get()
            if isinstance(windowDict[key], sg.Listbox):   
                finalDict[key] = windowDict[key].get_list_values()

        return finalDict

    def _writeToJson(self) -> None:
        """writes dictionary with replication info to a 
        JSON file
        """
        replicationInfo = self._getItems()
        jsonFile = os.path.join(self._replicationPath, 'structure.json')
        with open(jsonFile, 'w') as outFile:
            json.dump(replicationInfo, outFile, indent=4)

    def _createReplicationStructure(self) -> None:
        """Creates folders and copies files needed 
        for the replication process
        """
        self._replicateFolderStructure(
            self._replicationPath,
            self._mainFolderPath
        )
        self._copyFiles(
            self._replicationPath,
            self._mainFolderPath
        )

    def _replicateFolderStructure(self, destinationPath: str, sourcePath: str) -> None:
        """Replicates the folder structure under `sourcePath`
        in `destinationPath`
        Parameters
        ----------
        destinationPath : str
            destination path
        sourcePath : str
            source path
        """
        with os.scandir(sourcePath) as content:
            for item in content:
                if (
                    item.is_dir() and 
                    not item.name.startswith(".") and 
                    not item.name.startswith("initial_dataset") and 
                    not item.name.startswith("Replications")
                ):
                    os.mkdir(os.path.join(destinationPath, item.name))
                    self._replicateFolderStructure(
                        os.path.join(destinationPath, item.name),
                        os.path.join(sourcePath, item.name)
                    ) 

    def _copyFiles(self, destinationPath: str, sourcePath: str) -> None:
        """Copy the files selected by the user to the directory where
        the replication is going to be run
        Parameters
        ----------
        destinationPath : str
            destination path
        sourcePath : str
            main folder selected by the user
        """
        filesList = self._getFilesForReplication()
        for file in filesList:
            relativeFilePath = os.path.relpath(file, sourcePath) 
            shutil.copy2(
                file,
                os.path.join(destinationPath, relativeFilePath)
            )
        if self._containerDef:
            shutil.copy2(
                self._containerDef,
                self._replicationPath
            )

    def _getFilesForReplication(self) -> List[str]:
        """Gets list of files to proceed with
        the replication process

        Returns
        -------
        List[str]
            List of files for replication
        """
        replicationFiles = list()
        # Main script and dependencies
        replicationFiles.append(self._mainScript)
        replicationFiles.extend(self._dependencies)
        if self._userDefinedTools:
            for path in self._userDefinedTools:
                for root, _, files in os.walk(path):
                    for file in files:
                        replicationFiles.append(os.path.join(root, file))

        return replicationFiles

    def isFolderUnderMain(self, folder: str) -> bool:
        """Checks if a folder is under the main 
        path

        Parameters
        ----------
        folder : str
            folder checked

        Returns
        -------
        bool
            True if folder under main path
        """
        foldersPath = list()
        for root, dirs, _ in os.walk(self._mainFolderPath):
            for directory in dirs:
                foldersPath.append(os.path.normcase(os.path.join(root, directory)))

        return os.path.normcase(folder) in foldersPath
    
    def _createTreeFile(self, rootPath: str, outFile: str) -> None:
        """Creates tree file with the initial structure inside 
        the directory `rootPath`. The file is saved in the 
        replication area

        Parameters
        ----------
        rootPath : str
            root path to be inspected (tree structure)
        outFile : str
            file with the tree structure saved
        """
        treeList = list(tree(Path(rootPath)))
        numberFolders = len([item for item in treeList if item.endswith('/')])
        numberFiles = len([item for item in treeList if not item.endswith('/')])
        treeFile = os.path.join(self._replicationPath, outFile)
        with open(treeFile, 'w', encoding='utf-8') as fileOut:
            fileOut.write('Root: ' + rootPath + '\n')
            for line in treeList:
                fileOut.write(line + '\n')
            fileOut.write("\n")
            infoLine = f'{numberFolders} directories, {numberFiles} files'
            fileOut.write(infoLine)

    def _prepareReplication(self) -> None:
        """Creates structure for the replication, including
        copying necessary files, creating folders and creating 
        configuration files 
        """
        self._writeToJson()
        self._createReplicationStructure()
        self._mainScript = os.path.join(
            self._replicationPath,
            os.path.relpath(self._mainScript, self._mainFolderPath)
        )
        _temp = list() 
        if self._userDefinedTools:
            for path in self._userDefinedTools:
                newUserPath = os.path.join(
                    self._replicationPath,
                    os.path.relpath(path, self._mainFolderPath)
                )
                _temp.append(newUserPath)
            
            self._userDefinedTools = _temp  

        self._createConfigFile()

    def _createProcessArgs(self, script: str) -> List[str]:
        """Creates the arguments to run in the subprocess 
        command. The command depends on the extension of the 
        script

        Parameters
        ----------
        script : str
            main script for the replication

        Returns
        -------
            List[str]: arguments for subprocess.Popen
        """
        if script.endswith(".py"):
            program = "python3"
        elif script.endswith(".R"):
            program = "Rscript"
        elif script.endswith(".do"):
            program = "stata-mp -b do"

        command = f"singularity exec {self._containerImage} {program} {script}"

        return shlex.split(command)

    def run(self) -> subprocess.Popen:
        """Public method to run replication

        Returns
        -------
        subprocess.Popen
            Replication process
        """
        self._prepareReplication()
        self._createTreeFile(self._replicationPath, "tree.txt")
        # List data files and save them in file "datafiles.txt"
        dataPath = os.path.join(
            self._getRootPath(mainFolderPath=self._mainFolderPath),
            "initial_dataset"
        )
        self._createTreeFile(dataPath, "datafiles.txt")
        path, script = os.path.split(self._mainScript)
        if path:
            os.chdir(path)
        
        args = self._createProcessArgs(script)
        
        return subprocess.Popen(
            args,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid
        )

    def _createConfigFile(self) -> None:
        """Create configure script
        """
        head, _ = os.path.split(self._mainScript)
        if self._mainScript.endswith(".do"):
            self._createStataProfile(os.path.join(head, 'profile.do'))
        elif self._mainScript.endswith(".R"):
            self._createRconfig(os.path.join(head, 'config.R'))

    def _createRconfig(self, outfile: str) -> None:
        """Create R configuration file

        Parameters
        ----------
        outfile : str
            path to profile do
        """
        rootPath = self._getRootPath(
            mainFolderPath=self._mainFolderPath
        )
        createRConfigFile(
            replicationPath=self._replicationPath,
            outFile=outfile,
            rootPath=rootPath,
            toolsPaths=[
                *self._externalTools,
                *self._userDefinedTools
            ]
        )

    def _createStataProfile(self, outfile: str) -> None:
        """Create Stata profile do

        Parameters
        ----------
        outfile : str
            path to profile do
        """
        rootPath = self._getRootPath(
            mainFolderPath=self._mainFolderPath
        )
        createProfile(
            version=STATA_VERSION,
            replicationPath=self._replicationPath,
            outFile=outfile,
            rootPath=rootPath,
            toolsPaths=[
                *self._externalTools,
                *self._userDefinedTools
            ]
        )

    def _getRootPath(self, mainFolderPath: str) -> str:
        """Gets the project root path. This is specific to BPLIM

        Parameters
        ----------
        mainFolderPath : str
            Main folder specified by the user

        Returns
        -------
        str
            Project's root path
        """
        try:
            projectName = re.search(
                PROJECT_REGULAR_EXPRESSION, 
                mainFolderPath
            )[0]
        except TypeError:
            raise ValueError('Project not found')
        else: 
            return os.path.join('/bplimext', 'projects', projectName)

        
    def writeReport(self, startTime: float) -> None:
        """Writes a report on the details of the replication, namely the start and
        finish times, the process exit code, the files used and created in the 
        replication and their corresponding modification times 

        Parameters
        ----------
        startTime : float
            Process start time      
        """
        startTime = datetime.fromtimestamp(startTime)
        filesInfo = self._getFilesInfo()
        maxFileLength = max([len(file) for file, _ in filesInfo])
        leftJUstified = maxFileLength + 5
        reportPath = os.path.join(self._replicationPath, '.report.txt') 
        with open(reportPath, 'w') as report:
            report.write("Started  : " + startTime.strftime('%Y-%m-%d %H:%M:%S') + "\n")
            report.write("Finished : " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
            report.write("Exit code: 0\n\n")
            report.write("Root Path: " + self._replicationPath + "\n\n")
            header = f"{'File':<{leftJUstified}}{'Date modified':>23}\n"
            report.write(header)
            report.write((leftJUstified + 23) * '-' + '\n')
            for file, dateModified in filesInfo:
                line = f"{file:<{leftJUstified}}{dateModified:>23}\n"
                report.write(line)
            scriptFiles = list(self._getScriptFiles())
            self._writeFlagCommands(report, scriptFiles)
            self._writeFlagCommands(report, scriptFiles, flag='alert')

    def _writeFlagCommands(
            self, 
            fileHandler: object, 
            scriptFiles: List[str], 
            flag: str = 'use'
        ) -> None:
        """Writes commands to flag in the report. Commands may
        be of two types: use commands and alert commands 
        Parameters
        ----------
        fileHandler : io.TextIOWrapper
            file handler
        scriptFiles : list[str]
            files to inspect
        flag : str, optional
            use or alert or command, by default 'use'
        """
        flagCommands = USE_COMMANDS if flag == 'use' else ALERT_COMMANDS
        fileHandler.write('\n\n')
        flagDict = {}
        for file in scriptFiles:
            flagDict.update(Replication._flagScript(file, flagCommands))
        if flag == 'use':
            fileHandler.write("********* Use commands *********\n\n")
        else:
            fileHandler.write("******* Alert commands *********\n\n")
        header = f"{'Command Name':<15}{'Regex':>15}\n"
        fileHandler.write(header)
        fileHandler.write(30 * '-' + '\n')
        for command, regex in flagCommands.items():
            line = f"{command:<15}{regex:>15}\n"
            fileHandler.write(line)
        fileHandler.write("\n\n")
        fileNumber = 0
        for file, lines in flagDict.items():
            if lines:
                fileNumber += 1
                relativePath = os.path.relpath(file, self._replicationPath)
                fileLine = f"[{fileNumber}] File: {relativePath}\n\n"
                fileHandler.write(fileLine)
                rightOffset = Replication._getRightOffset([line for _, line in lines], 14)
                header = f"{'Line Text':<{rightOffset}}{'Line Number':>15}\n"
                fileHandler.write(header)
                fileHandler.write((15 + rightOffset) * '-' + '\n')
                for num, line in sorted(lines, key=lambda x: x[1], reverse=True):
                    lineFlagged = f"{line:<{rightOffset}}{str(num):>15}\n"
                    fileHandler.write(lineFlagged)
                fileHandler.write('\n')

    def _getScriptFiles(self) -> Generator[str, Any, Any]:
        """Gets names of scripts (.do, .py, .R files)
        Yields
        ------
        str
            files' full path
        """
        for root, _, files in os.walk(self._replicationPath):
            for file in files:
                if re.search(r"(\.do$)|(\.py$)|(\.R$)|(\.jl$)", file):
                    yield os.path.join(root, file)

    def _getFilesInfo(self) -> List[Tuple[str, str]]:
        """Gets information (name and modification time) about all the
        files used and created during the replication 
        Returns
        -------
        list[tuple[str, str]]
            files and corresponding modification time
        """
        filesInfo = list()
        for root, _, files in os.walk(self._replicationPath):
            for file in files:
                fullPath = os.path.join(root, file)
                relativePath = os.path.relpath(fullPath, self._replicationPath)
                filesInfo.append(
                    (
                        relativePath, 
                        datetime.\
                            fromtimestamp(os.path.getmtime(fullPath)).\
                            strftime('%Y-%m-%d %H:%M:%S')
                    )
                ) 
        filesInfo.sort(key=lambda x: x[0])

        return filesInfo

    @staticmethod
    def _readLines(file: str) -> List[str]:
        """Reads a file and returns its lines
        Parameters
        ----------
        file : str
            file to be read
        Returns
        -------
        list[str]
            file lines
        """
        with open(file, 'r', encoding='latin-1') as f:
            lines = f.readlines()
            
        return lines

    @staticmethod
    def _flagLines(lines: List[str], flagCommands: Dict[str, str]) -> List[int]:
        """Flags lines that contain specific
        expressions
        Parameters
        ----------
        lines : list[str]
            lines to flag
        flagCommands: dict[str, str]
            commands to flag
        Returns
        -------
        list[int]
            list of flagged lines' indexes 
        """
        linesFlagged = list()
        for _, pattern in flagCommands.items():
            for index, line in enumerate(lines):
                if re.search(pattern, line):
                    linesFlagged.append(index)   
        
        return sorted(list(set(linesFlagged)))

    @staticmethod
    def _getFlaggedLines(
        file: str, 
        flagCommands: Dict[str, str]
    ) -> Generator[Tuple[int, str], Any, Any]:
        """Fetch lines and indexes that contain specific 
        expressions in a file
        Parameters
        ----------
        file : str
            script file
        flagCommands: dict[str, str]
            commands to flag
        Yields
        ------
        tuple[int, str]
            line index and line text
        """
        lines = Replication._readLines(file)
        flaggedLines = Replication._flagLines(
            [line.strip() for line in lines], 
            flagCommands
        )
        for index in flaggedLines:
            yield (index + 1, lines[index].strip())
            
    @staticmethod          
    def _flagScript(
        file: str, 
        flagCommands: Dict[str, str]
    ) -> Dict[str, List[Tuple[int, str]]]:
        """Flags specific expressions in a script
        Parameters
        ----------
        file : str
            script file
        flagCommands: dict[str, str]
            commands to flag
        Returns
        -------
        dict[str, list[tuple[int, str]]]
            Script's name and list of flagged lines and indexes
        """
        linesAndIndexes = list(
            Replication._getFlaggedLines(file, flagCommands)
        )
        return {
            file: linesAndIndexes
        }

    @staticmethod
    def _getRightOffset(lines: str, minOffset: int) -> int:
        """Gets the right offset for the report
        based on the lines' maximum length 
        Parameters
        ----------
        lines : list
            list of lines
        minOffset : int
            minimum offset allowed
        Returns
        -------
        int
            right offset 
        """
        offset = max([len(line) for line in lines]) + 5
        if offset > minOffset:
            return offset
        return minOffset
