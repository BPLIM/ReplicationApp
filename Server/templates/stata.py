# Template for Stata 
from typing import List, Union
import os


def createProfile(
    version: int,
    replicationPath: str,
    outFile: str,
    rootPath: str,
    toolsPaths: Union[List[str], None] = None
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
    rootPath : str
        Path for project
    toolsPaths : List[str]
        List of paths for tools, by default []
    """  
    replicationRelPath = os.path.relpath(replicationPath, rootPath)
    script = f"""*********************************************************
*            Initialization
*********************************************************
version {version}
clear all
program drop _all
set more off
set rmsg on
set matsize 10000
set linesize 255
capture log close
*********************************************************
*               Define globals                          *
*********************************************************  
**** Path for replication ****
* Root path
global root_path "{rootPath}"
* Base path for replications
global path_rep "${{root_path}}/{replicationRelPath}"  

**** Paths for data ****
* Set the path for non perturbed data source
global path_source "${{root_path}}/initial_dataset"
* Set the path for perturbed data source
global path_source_p "${{path_source}}/modified"
* Set the path for intermediate data source
global path_source_i "${{path_source}}/intermediate"
* Set the path for external data source
global path_source_e "${{path_source}}/external"

**** Globals for type of modified dataset
* Perturbed
global M1 "P"
* Shuffled
global M2 "S"
* Randomized
global M3 "R"
* Dummy 
global M4 "D"
/********************************************************************* 
********* Example: using non-modified and modified data sets *********
* Anonymized (CB_A_YFRM_2010_JUN21_ROSTO_V01.dta)
use "${{path_source}}/CB_A_YFRM_2010_JUN21_ROSTO_V01.dta"
* Perturbed (CRC_P_MFRM_2010_APR19_COBR_V01.dta)
use "${{path_source_p}}/CRC_${{M1}}_MFRM_2010_APR19_COBR_V01.dta"
* Shuffle (PE056_S_rejected_applications.dta)
use "${{path_source_p}}/PE056_${{M2}}_rejected_applications.dta"
* Randomized (CRC_R_MFRMBNK_2007_APR19_CO_V01.dta)
use "${{path_source_p}}/CRC_${{M3}}_MFRMBNK_2007_APR19_CO_V01.dta"
* Dummy (SLB_D_YBNK_20102018_OCT20_QA1_V01.dta)
use "${{path_source_p}}/SLB_${{M4}}_YBNK_20102018_OCT20_QA1_V01.dta"
*********************************************************************/

**** Path for project specific ado files ****

"""
    if toolsPaths:
        for path in toolsPaths:
            relPath = os.path.relpath(path, rootPath)
            script += f'adopath ++ "${{root_path}}/{relPath}"\n'


    with open(outFile, 'w') as fOut:
        fOut.write(script)