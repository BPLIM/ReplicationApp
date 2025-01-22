# Template for R
from typing import List, Union
import os


def createConfigFile(
    replicationPath: str,
    outFile: str,
    rootPath: str,
    toolsPaths: Union[List[str], None] = None
) -> None:
    """Creates R configuration file
    
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
    script = f"""print("## Running config.R file ##")
sessionInfo()

# Root path
root_path <- "{rootPath}"
# Base path for replications
path_rep <- file.path(root_path, "{replicationRelPath}") 

#### Paths for data ####
paths <- list(
    source = file.path(root_path, "initial_dataset"),
    source_p = file.path(root_path, "initial_dataset", "modified"),
    source_i = file.path(root_path, "initial_dataset", "intermediate"),
    source_e = file.path(root_path, "initial_dataset", "external")
)

# Globals for type of modified dataset
# Perturbed
M1 <- "P"
# Shuffle
M2 <- "S"
# Randomized
M3 <- "R"
# Dummy 
M4 <- "D"

#### Example: using non-modified and modified datasets ####
# anonymized <- file.path(paths$source, "CB_A_YFRM_2010_JUN21_ROSTO_V01.dta"),
# perturbed <- file.path(paths$source_p, sprintf("CRC_%s_MFRM_2010_APR19_COBR_V01.dta", M1),
# shuffle <- file.path(paths$source_p, sprintf("PE056_%s_rejected_applications.dta", M2),
# randomized <- file.path(paths$source_p, sprintf("CRC_%s_MFRMBNK_2007_APR19_CO_V01.dta", M3),
# dummy <- file.path(paths$source_p, sprintf("SLB_%s_YBNK_20102018_OCT20_QA1_V01.dta", M4)
# Example reading the perturbed dataset
# data <- read_dta(perturbed)

"""
    if toolsPaths:
        script += '# User Defined libraries\n'
        script += '.libPaths(c('
        for path in toolsPaths:
            relPath = os.path.relpath(path, rootPath)
            script += f'file.path(root_path, "{relPath}"), '

        script += '.libPaths()))\n\n'

    script += 'print("## Finish running config.R file ##")\n'

    with open(outFile, 'w') as fOut:
        fOut.write(script)