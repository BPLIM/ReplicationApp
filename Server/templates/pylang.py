# Template for Stata 
from typing import List, Union
import os


def createConfigFile(
    replicationPath: str,
    outFile: str,
    rootPath: str,
    toolsPaths: Union[List[str], None] = None
) -> None:
    """Creates the Python configuration file

    Parameters
    ----------
    replicationPath : str
       Base path for replication
    outFile: str
       Path to profile
    rootPath : str
        Path for project
    toolsPaths : List[str]
        List of paths for tools, by default []
    """  
    replicationRelPath = os.path.relpath(replicationPath, rootPath)
    script = f"""from pathlib import Path

print("Running configuration file")

### Path for replication ###
# Root path 
ROOT_PATH = Path("{rootPath}")
# Base path for replications 
PATH_REP = ROOT_PATH / "{replicationRelPath}"

### Paths for data ###
# Set the path for non perturbed data source
PATH_SOURCE = ROOT_PATH / "initial_dataset"
# Set the path for perturbed data source
PATH_SOURCE_P = PATH_SOURCE / "modified"
# Set the path for intermediate data source
PATH_SOURCE_I = PATH_SOURCE / "intermediate"
# Set the path for external data source
PATH_SOURCE_E = PATH_SOURCE / "external"

### Globals for type of modified dataset ###
# Perturbed
M1 = "P"
# Shuffled
M2 = "S"
# Randomized
M3 = "R"
# Dummy
M4 = "D"

####################################################################### 
######### Example: using non-modified and modified data sets ##########
# import pandas as pd
# Anonymized (CB_A_YFRM_2010_JUN21_ROSTO_V01.dta)
# pd.read_stata(PATH_SOURCE / "CB_A_YFRM_2010_JUN21_ROSTO_V01.dta")
# Perturbed (CRC_P_MFRM_2010_APR19_COBR_V01.dta)
# pd.read_stata(PATH_SOURCE_P / f"CRC_{{M1}}_MFRM_2010_APR19_COBR_V01.dta")
# Shuffle (PE056_S_rejected_applications.dta)
# pd.read_stata(PATH_SOURCE_P / f"PE056_{{M2}}_rejected_applications.dta")
# Randomized (CRC_R_MFRMBNK_2007_APR19_CO_V01.dta)
# pd.read_stata(PATH_SOURCE_P / f"CRC_{{M3}}_MFRMBNK_2007_APR19_CO_V01.dta")
# Dummy (SLB_D_YBNK_20102018_OCT20_QA1_V01.dta)
# pd.read_stata(PATH_SOURCE_P / f"SLB_{{M4}}_YBNK_20102018_OCT20_QA1_V01.dta")
#######################################################################
"""
    if toolsPaths:
        script += "\nimport sys\n\n"
        for path in toolsPaths:
            relPath = os.path.relpath(path, rootPath)
            script += f'sys.path.append(ROOT_PATH / "{relPath}")\n'

    script += '\nprint("Configuration settings defined")'

    with open(outFile, 'w') as fOut:
        fOut.write(script)
