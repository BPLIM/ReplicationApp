# Template for Stata 
from typing import List


def createProfile(
    version: int,
    replicationPath: str,
    outFile: str,
    pathSource: str = '',
    pathSourceModified: str = '',
    pathSourceIntermediate: str = '',
    toolsPaths: List[str] = []
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
    pathSource : str
        Path for source data, by default ''
    pathSourceModified : str
        Path for modified data, by default ''
    pathSourceIntermediate : str
        Path for intermediate data, by default ''
    toolsPaths : List[str]
        List of paths for tools, by default []
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
* Set the path for non perturbed data source
global path_source "{pathSource}"
* Set the path for perturbed data source
global path_source_p "{pathSourceModified}"
* Set the path for intermediate data source
global path_source_i "{pathSourceIntermediate}"

**** Globals for type of modified dataset
* Perturbed
global M1 "P"
* Shuffle
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

*** Ado PLUS directory ***
sysdir set PLUS "/opt/stata{version}/ado/plus"

**** Path for project specific ado files ****

"""
    if toolsPaths:
        for path in toolsPaths:
            script += f'adopath ++ "{path}"\n'


    with open(outFile, 'w') as fOut:
        fOut.write(script)