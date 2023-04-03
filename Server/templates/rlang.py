# Template for R
from typing import List


def createConfigFile(
    replicationPath: str,
    outFile: str,
    pathSource: str = '',
    pathSourceModified: str = '',
    pathSourceIntermediate: str = '',
    toolsPaths: List[str] = []
) -> None:
    """Creates R configuration file
    
    Parameters
    ----------
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
    script = f"""print("## Running config.R file ##")
sessionInfo()

##### Path for replication #####
# Base path for replications
path_rep <- "{replicationPath}"  

#### Paths for data ####
# Set the path for non perturbed data source
path_source <- "{pathSource}"
# Set the path for perturbed data source
path_source_p <- "{pathSourceModified}"
# Set the path for intermediate data source
path_source_i <- "{pathSourceIntermediate}"

# Globals for type of modified dataset
# Perturbed
M1 <- "P"
# Shuffle
M2 <- "S"
# Randomized
M3 <- "R"
# Dummy 
M4 <- "D"


################### Example: using non-modified and modified data sets #####################
# Anonymized (CB_A_YFRM_2010_JUN21_ROSTO_V01.dta)
# dataA <- stringr::str_interp("${{path_source}}/CB_A_YFRM_2010_JUN21_ROSTO_V01.dta")
#
# Perturbed (CRC_P_MFRM_2010_APR19_COBR_V01.dta)
# dataP <- stringr::str_interp("${{path_source_p}}/CRC_${{M1}}_MFRM_2010_APR19_COBR_V01.dta")
#
# Shuffle (PE056_S_rejected_applications.dta)
# dataS <- stringr::str_interp("${{path_source_p}}/PE056_${{M2}}_rejected_applications.dta")
#
# Randomized (CRC_R_MFRMBNK_2007_APR19_CO_V01.dta)
# dataR <- stringr::str_interp("${{path_source_p}}/CRC_${{M3}}_MFRMBNK_2007_APR19_CO_V01.dta")
#
# Dummy (SLB_D_YBNK_20102018_OCT20_QA1_V01.dta)
# dataD <- stringr::str_interp("${{path_source_p}}/SLB_${{M4}}_YBNK_20102018_OCT20_QA1_V01.dta")
#############################################################################################


"""
    if toolsPaths:
        script += '# User Defined libraries\n'
        script += 'additionalPaths <-\n'
        script += '  c(\n'
        for index, path in enumerate(toolsPaths):
            if (index + 1) != len(toolsPaths) or len(toolsPaths) == 1:
                script += f'"{path}"\n'
            else:
                script += f'"{path}",\n'

        script += '  )\n'
        script += '.libPaths(additionalPaths)\n'
        script += 'rm(additionalPaths)\n\n'

    script += 'print("## Finish running config.R file ##")\n'

    with open(outFile, 'w') as fOut:
        fOut.write(script)