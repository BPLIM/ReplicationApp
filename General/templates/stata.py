# Template for Stata 
import os
import stat
from typing import List


def createProfile(
    version: int,
    replicationPath: str,
    outFile: str,
    replicationDataPaths: List[str] = [],
    externalDataPaths: List[str] = [],
    replicationToolsPaths: List[str] = [],
    externalToolsPaths: List[str] = []
) -> None:
    """Creates the Stata profile do-file
    Parameters
    ----------
    version : int
        Stata version
    replicationPath : str
       Base path for replication
    outFile: str
       Path to profile
    replicationDataPaths : List[str]
        List of paths for data inside replication folder, by default []
    externalDataPaths : List[str]
        List of paths for data outside replication folder, by default []
    replicationToolsPaths : List[str]
        List of paths for tools inside replication folder, by default []
    replicationToolsPaths : List[str]
        List of paths for tools outside replication folder, by default []
    """  
    script = f"""*********************************************************
*            Initialization
*********************************************************
version {version}
clear all
program drop _all
set more off
set rmsg on
set matsize 10000
set maxvar 10000
set linesize 255
capture log close
*********************************************************
*               Define globals                          *
*********************************************************  
**** Path for replication ****
* Base path for replications
global path_rep "{replicationPath}"  

**** Paths for data ****
"""

    for index, path in enumerate(replicationDataPaths):
        script += f'global path_source_{index} "${{path_rep}}/{path}"\n'

    if externalDataPaths:
        script += '\n'
        start = len(replicationDataPaths)
        for index, path in enumerate(externalDataPaths):
            script += f'global path_source_{start+index} "{path}"\n'       

    script += """
/* Set additional globals 
.....
.....
*/

"""

    if replicationToolsPaths or externalToolsPaths:
        script += '**** Path for project specific ado files ****\n'

    if replicationToolsPaths:
        for path in replicationToolsPaths:
            script += f'adopath ++ "${{path_rep}}/{path}"\n'

    if externalToolsPaths:
        for path in externalToolsPaths:
            script += f'adopath ++ "{path}"\n'


    with open(outFile, 'w') as fOut:
        fOut.write(script)


def createStataBash(outFile: str, doFile: str, stataPath: str) -> None:
    """Creates the bash script that runs the replication 
    in Stata
    Parameters
    ----------
    outFile : str
        path to bash script file
    doFile : str
        master do-file to run in the replication
    stataPath: str
        path to Stata executable
    """
    path, file = os.path.split(doFile)
    if outFile.endswith('.ps1'):
        script = f"""# Path to Stata exec 
$stata = "{stataPath}"
# Path where main script is located
$workpath = "{path}"
# Main do-file
$dofile = "{file}"

# Do not change this part
$log = ([io.fileinfo] $dofile | % basename) + ".log"
cd $workpath
$arguments = "-e do $dofile"
$proc = $(Start-Process $stata -PassThru -ArgumentList $arguments)
Wait-Process $proc.Id
if (Get-Content "$log" -Tail 1 | Select-String -Pattern  "^r\([0-9]+\);") {{
    exit 1
}} else {{
    exit 0
}}
"""

    else:
        script = f"""#!/bin/bash
# Path to Stata exec 
stata="{stataPath}"
# Path where main script is located
workpath="{path}"
# Main do-file
dofile="{file}"
# Do not change this part
log="$(basename -s .do "$dofile").log"
cd $workpath
$stata -e do "$dofile"
if tail -1 "$log" | egrep "^r\([0-9]+\);"
then
    exit 1
else
    exit 0
fi
"""


    with open(outFile, 'w') as fOut:
        fOut.write(script)
    # Make it executable
    st = os.stat(outFile)
    os.chmod(outFile, st.st_mode | stat.S_IEXEC)