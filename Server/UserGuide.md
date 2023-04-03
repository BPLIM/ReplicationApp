# Replication Guide

This document serves as a guide for replications by external researchers. It is mainly targeted at researchers that work with BPLIM's modified datasets, but it is not exclusive to this type of researchers. Researchers that do not work with modified data may still want to use the application (see section 1) to ensure full reproducibility of their results.

Researchers use modified datasets to test and prepare their code. Once they are done with coding they should request that BPLIM replicates the analysis on the original data. 
This replication process has two phases. The first phase is the responsibility of the researcher, who must confirm that the process runs flawlessly in a single execution. Ideally this should be done using BPLIM's Replication Application. If this phase is successful, researchers should communicate this outcome to BPLIM staff and request the code to be run on the original data. Researchers working only with non-modified data should abstain from making the aforementioned request (second phase). After verifying that the code has indeed run successfully and that no file has been tampered with upon conclusion of the first phase, BPLIM staff will run the researcher's scripts on the original data.

## 1. Replication Application

Inside every researcher's project  work area there is a ".desktop" file, which launches an application developed by BPLIM staff for replication purposes. To illustrate how the application works, we will use a mock Stata based project, **pxxx_BPLIM**[^1]. The projects' directory structure is as follows:

```
/bplimext/projects/pxxx_BPLIM/
│
├── initial_dataset/
│   ├── modified/
│   │   ├── PM110_BBS_P_MBNK_JAN2000DEC2020_JUN21_ASSET_V01.dta
│   │   └── ...
│   ├── intermediate/
│   │   └── ...
│   └── ...
│
├── work_area/
│   ├── run_replication.desktop
│   └── Submissions/
|       ├──  master.do
|       └──  do_files/
|           ├──  data_creation.do
|           ├──  dissertation.do
|           ├──  dissertation_interest.do
|           ├──  dissertation_extra.do
|           ├──  dissertation_means.do
|           └──  dissertation_until2017.do
│
├── tools/
|
└── results/
```

[^1]: Although this is a mock project, we are actually using real data and code from a student who used BPLIM data in her Masters Dissertation. In this project the student only worked with modified data.

If the researcher clicks on the file *ReplicationApp.desktop*, the application is launched, displaying the following dialog box:

<p style="text-align:center;"><img src="https://user-images.githubusercontent.com/51088103/223689793-8f2dae41-634d-45f0-ac93-2c010a2f27f7.PNG"  width="60%" height="30%"></p>

The first step is to select the source path for the replication, i.e., the directory where the researcher placed his/her scripts to run the analysis. This directory may include other directories and sub-directories. Please note that every directory and sub-directory under the selected path will be copied to the **replication area**. If we click the `browse` button, a dialog box opens to enable the user to select the path. In our mock example, the path is *"/bplimext/projects/pxxx_BPLIM/work_area/Submissions"*:  

<p style="text-align:center;"><img src="https://user-images.githubusercontent.com/51088103/223689796-028b18b3-00b5-44bc-bec0-ee1e81a429b4.PNG"  width="60%" height="30%"></p>

After selecting the main path, we have to select the main script. This is the entry point of the replication. It is the file that runs the replication and calls dependencies in case they exist. The file must be under the main path (not necessarily the first level) selected in the previous set, otherwise the replication will not run. Only **Stata**, **Python**, **R** and **Julia** file extensions are allowed in this field:

<p style="text-align:center;"><img src="https://user-images.githubusercontent.com/51088103/223689800-c82d5932-79db-4d19-a4ae-296a1111361c.PNG"  width="60%" height="30%"></p>

<p style="text-align:center;"><img src="https://user-images.githubusercontent.com/51088103/223689804-5b401e5a-25d2-471a-af02-32548a51042a.PNG"  width="60%" height="30%"></p>

In the third field we must select the container image used to run the replication. Containers are a great way to control your software environment and make it easier to ensure (not completely) that your research is reproducible. For more information on containers and how we use them at BPLIM, please follow this [link](). In the context of the application, the user only has to select the **Singularity Image** (\*.sif file), usually placed by BPLIM staff in *".../tools/_containers/"*:

<p style="text-align:center;"><img src="https://user-images.githubusercontent.com/51088103/223689765-1e8c84c9-e411-4b01-9f17-865bc21a706f.PNG"  width="60%" height="30%"></p>

<p style="text-align:center;"><img src="https://user-images.githubusercontent.com/51088103/223689771-336accff-d93c-4f7e-a653-c886a3de7790.PNG"  width="60%" height="30%"></p>

Next we may select the Definition file (\*.def file) used to create the container. This field is optional, since it is possible to use external images from credible sources without a definition file. Although not mandatory, it is recommended that you provide a definition file, which will be copied to the replication area. Since we do not copy the image to the replication area for storage reasons, the definition file is a way to ensure (again, not completely) that your environment can be recreated in the future to reproduce the analysis.

<img src="https://user-images.githubusercontent.com/51088103/223689776-bdaec802-c79b-40b5-9a76-bdd38837e85b.PNG"  width="60%" height="30%"></p>

<p style="text-align:center;"><img src="https://user-images.githubusercontent.com/51088103/223689778-0d0101d3-dcee-4158-89f4-bf65ee6a8d2e.PNG"  width="60%" height="30%"></p>

In the fifth field we provide the dependencies that are going to be used in the replication. Dependencies are nothing more than other scripts called by the main script which may be placed in directories or sub-directories for organization purposes. This field is not mandatory because the researcher is free to run the entire analysis using only the main script. In our mock example, we specify six files in this field:

<p style="text-align:center;"><img src="https://user-images.githubusercontent.com/51088103/223689780-0398d00a-2e63-440c-9c67-94bde31bc862.PNG"  width="60%" height="30%"></p>

<p style="text-align:center;"><img src="https://user-images.githubusercontent.com/51088103/223689789-88073f3e-6909-40ff-a2cd-17e52adf9dad.PNG"  width="60%" height="30%"></p>

Finally, we can select directories for tools. By tools we mean programs, modules or packages used by the researcher in the replication. The application creates a configuration file that will point to these directories in order to enable the researcher to access them. The user may select one or more directories. Two cases are possible: if the directory specified is under the main path selected in the first field, the entire directory is copied to the replication area, although its size cannot exceed 10MB; otherwise, the configuration file will simply point to that path, not copying its contents to the replication area. In the example at hand, only the latter applies, since the ado-files needed are all placed outside the base replication path:

<p style="text-align:center;"><img src="https://user-images.githubusercontent.com/51088103/223708507-2b2bfbc9-ad0d-42da-8639-796d227e80d6.PNG"  width="60%" height="30%"></p>

<p style="text-align:center;"><img src="https://user-images.githubusercontent.com/51088103/223708516-a37af1e4-f25b-48e2-90c5-120111476713.PNG"  width="60%" height="30%"></p>

With every field filled, we click the **Run** button to run the replication. If there are no errors and warnings, the replication should start immediately. However, If any warning is found, the application will prompt a dialog box asking the user if he or she wishes to proceed with the replication. For example, if we did not specify a definition file, we would get a warning:

<p style="text-align:center;"><img src="https://user-images.githubusercontent.com/51088103/223708519-907b5a8e-d13f-428c-b36b-6477024bf743.PNG"  width="60%" height="30%"></p>

We may proceed with the replication by clicking **Yes**. The situation is different if any error is found by the application. In this case, the user is not allowed to proceed with the replication and must change the field that is causing the error. As an example, imagine that we had specified a main script that is not under the main path of replication (first field). This will result in an error:

<p style="text-align:center;"><img src="https://user-images.githubusercontent.com/51088103/223708523-e268f238-2948-471c-96c1-e3c83aa16e06.PNG"  width="60%" height="30%"></p>

The user will have to provide a valid file in the main script field in order to run the replication. On the other hand, if every field is correctly filled, the replication will start and the application will show a counter, displaying the elapsed time since the replication started:

<p style="text-align:center;"><img src="https://user-images.githubusercontent.com/51088103/223708529-948e9024-6086-46be-bf19-3603098c6701.PNG"  width="60%" height="30%"></p>

The user should see the following after a successful replication:

<p style="text-align:center;"><img src="https://user-images.githubusercontent.com/51088103/223708534-efb2ae9f-912f-464c-8fe5-9615e90a02cd.PNG"  width="60%" height="30%"></p>

The **Status** field has two possible outcomes: **Finished** - when the replication finishes, either with an error or no errors - or **Interrupted** - when the user clicks the **Stop** button during a run, effectively killing the replication. The **Return code** field is displayed when the **Status** outcome is **Finished**, and also has two possible outcomes: **0** - the replication ended without errors - or **1** - the replication finished, but with errors. In our example, the replication finished without errors. 

But what is the benefit of running the replication through the application instead of, for example, running it directly in Stata? Besides being a BPLIM product that helps us expedite the replication process, the application presents advantages for researchers. In order to see these advantages, we must inspect the outputs of the application. When we click the **Run** button, the application goes through a series of steps prior to actually running the code. 

First, if it does not exist, the *Replications* directory is created under the base path of the replication - in our case, *"/bplimext/projects/pxxx_BPLIM/work_area/Submissions"*. Under the *Replications* directory, the directory *Rep001* will be automatically created. Please note that the number included in the directory name will be automatically updated if there are already other replications inside *Replications*. *"/bplimext/projects/pxxx_BPLIM/work_area/Submissions/Replications/Rep001"* is what we previously mentioned as the replication area. The structure of the directory for our example is displayed in the image below (after the replication finishes):

<p style="text-align:center;"><img src="https://user-images.githubusercontent.com/51088103/223743250-0ce592a5-0bdf-460a-b848-0e538600c304.PNG"  width="60%" height="30%"></p>

The directories *data*, *Logs* and *results*, as well as the files they contain, are created by the code during the replication. The other directories and files were copied or created by the application. We can see that the dependencies, master script and definition file were copied to the replication area. The entire structure of the base path (first field of the replication) is copied to the replication area. But some additional files were also created, like *structure.json*,

<p style="text-align:center;"><img src="https://user-images.githubusercontent.com/51088103/223743256-e1f273a8-eb5a-4f71-b776-2fa67a4b8047.PNG"  width="60%" height="30%"></p>

which contains information of every field input for a specific replication. It serves not only to document your replication, providing the original paths for files and directories, but it is also useful in future replications. Imagine that user's second run uses the same files as the first, or additional dependencies for example. In that case, when the user launches the application, he does not need to fill every field again. The **Load from file** button launches a dialog box to choose a a **JSON** file:

<p style="text-align:center;"><img src="https://user-images.githubusercontent.com/51088103/223743237-1c389012-96b3-4712-b129-5926bf65a177.PNG"  width="60%" height="30%"></p>

After selecting the file *structure.json*, click "Open" and all the fields are automatically filled with the information of first replication:

<p style="text-align:center;"><img src="https://user-images.githubusercontent.com/51088103/223743247-27176bf0-3601-4eac-8dfe-536a89fc525a.PNG"  width="60%" height="30%"></p>


Other file created created by the application is *tree.txt*, which contains the tree structure of the replication area prior to running the replication:

<p style="text-align:center;"><img src="https://user-images.githubusercontent.com/51088103/223744691-aa431f25-8667-43cf-91dd-39b768e19fc1.PNG"  width="60%" height="30%"></p>

Finally, the last file that the application creates is the configuration file to run this particular replication. Since we are using Stata, our configuration file is named *profile.do* and is placed on the same directory of the master script. The contents of this file in our mock example are displayed below:


```stata
*********************************************************
*            Initialization
*********************************************************
version 17
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
global path_rep "/bplimext/projects/pxxx_BPLIM/work_area/Submissions/Replications/Rep001"  

**** Paths for data ****
* Set the path for non perturbed data source
global path_source "/bplimext/projects/pxxx_BPLIM/initial_dataset"
* Set the path for perturbed data source
global path_source_p "/bplimext/projects/pxxx_BPLIM/initial_dataset/modified"
* Set the path for intermediate data source
global path_source_i "/bplimext/projects/pxxx_BPLIM/initial_dataset/intermediate"

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
use "${path_source}/CB_A_YFRM_2010_JUN21_ROSTO_V01.dta"
* Perturbed (CRC_P_MFRM_2010_APR19_COBR_V01.dta)
use "${path_source_p}/CRC_${M1}_MFRM_2010_APR19_COBR_V01.dta"
* Shuffle (PE056_S_rejected_applications.dta)
use "${path_source_p}/PE056_${M2}_rejected_applications.dta"
* Randomized (CRC_R_MFRMBNK_2007_APR19_CO_V01.dta)
use "${path_source_p}/CRC_${M3}_MFRMBNK_2007_APR19_CO_V01.dta"
* Dummy (SLB_D_YBNK_20102018_OCT20_QA1_V01.dta)
use "${path_source_p}/SLB_${M4}_YBNK_20102018_OCT20_QA1_V01.dta"
*********************************************************************/

**** Path for project specific ado files ****

adopath ++ "/bplimext/projects/pxxx_BPLIM/tools"
```

By placing the file next to the master script, Stata runs *profile.do* prior to running the master do-file, which we can use to define settings and globals. As you have probably noticed, the paths for globals `path_rep`, `path_source*` and command `adopath++` are based on the project and input fields of the application. 

Researchers must use the globals defined in *profile.do* in their scripts when submitting a replication. It is **very important** that you specify globals related to data directories (**path_source**, **path_source_p** and **path_source_i**) when reading data, either modified or not. The globals for the type of modified dataset are also **very important**. Lets look at a snippet of the code used in this particular replication, namely on file *data_creation.do*:

```
use "${path_source_p}/PM110_BBS_${M1}_MBNK_JAN2000DEC2020_JUN21_ASSET_V01.dta", clear
```

The researcher is using perturbed data, so she/he uses the global **M1** in the name of the file and the global **path_source_p**, which stands for the directory for modified data. Note that for modified data, the global **path_source_p** should always be used, because all types of modified datasets are placed in that directory. As for the type of modified data, it varies: (i) perturbed - global **M1**; (ii) shuffled - global **M2**; (iii) randomized - global **M3**; (iv) dummy - global **M4**. These configurations make the replication process much faster and smoother, since all BPLIM staff has to do, in order to run the scripts on the original data, is to change the globals in the configuration file.

The other **important** global defined in *profile.do* is **path_rep**, which is the directory of the replication area. The researcher may use this global to change the working directory to where the master script is located:

```stata
cd ${path_rep}

/*
code
code
*/
```

Every file created during the replication must be under this directory. If we have scripts in sub-directories, we simply navigate using relative paths and run those scripts. In our mock example:

```stata
cd ${path_rep}

cd do_files
do data_creation
```

Also, please note that every folder and sub-folders under the base path of the replication (first field of the application) is copied to the replication area. So, for example, if you have the following structure:

```
/bplimext/projects/pxxx_BPLIM/
....
│
├── work_area/
│   ├── run_replication.desktop
│   └── Submissions/
|       ├──  master.do
|       ├──  data/
|       ├──  do_files/
|       |   ├──  data_creation.do
|       |   ├──  dissertation.do
|       |   ├──  dissertation_interest.do
|       |   ├──  dissertation_extra.do
|       |   ├──  dissertation_means.do
|       |   └──  dissertation_until2017.do
|       └──  results/
│
...
```

The directories *data* and *results* will also be copied the replication area. So please make sure to capture any possible errors when creating your directory structure inside the scripts. In our case, and for Stata in particular, we would do the following in our master script:

```stata
cd ${path_rep}

// path for intermediate datasets
capture mkdir data 
// path for results
capture mkdir results

cd do_files
do data_creation
```

In **Python** we can use `try/except` blocks and in **R** `tryCatch()`. Also, keep in mind that during the replication, you may use absolute or relative paths. If using absolute paths, it is imperative that you use the globals defined in the profile and the master script. We will illustrate this process using *master.do* and *data_creation.do*.

**master.do**

```stata
cd ${path_rep}

global path_data "${path_rep}/data"
global path_results "${path_rep}/results"

capture mkdir ${path_data}
capture mkdir ${path_results}

cd do_files
do data_creation
```

**data_creation.do** - absolute paths

```stata
use "${path_source_p}/PM110_BBS_${M1}_MBNK_JAN2000DEC2020_JUN21_ASSET_V01.dta", clear

/*
code to modify data
*/

// save intermediate data
save "${path_data}/bbs_intermediate", replace
```

**data_creation.do** - relative paths

```stata
use "${path_source_p}/PM110_BBS_${M1}_MBNK_JAN2000DEC2020_JUN21_ASSET_V01.dta", clear

/*
code to modify data
*/

// save intermediate data
save "../data/bbs_intermediate", replace
```

Whether the researcher uses relative paths or absolute paths, BPLIM staff only needs to change the file *profile.do* in order to run the replication with other settings. In the case of absolute paths, they must always be specified in terms of previously defined globals, at least **path_rep**. 


If the researcher uses **R** instead, the application creates a configuration named *config.R*, in the same directory as the main script. In our current example, the file would have the following content:

```R
print("## Running config.R file ##")
sessionInfo()

##### Path for replication #####
# Base path for replications
path_rep <- "/bplimext/projects/pxxx_BPLIM/work_area/Submissions/Replications/Rep001"  

#### Paths for data ####
# Set the path for non perturbed data source
path_source <- "/bplimext/projects/pxxx_BPLIM/initial_dataset"
# Set the path for perturbed data source
path_source_p <- "/bplimext/projects/pxxx_BPLIM/initial_dataset/modified"
# Set the path for intermediate data source
path_source_i <- "/bplimext/projects/pxxx_BPLIM/initial_dataset/intermediate"

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
# dataA <- stringr::str_interp("${path_source}/CB_A_YFRM_2010_JUN21_ROSTO_V01.dta")
#
# Perturbed (CRC_P_MFRM_2010_APR19_COBR_V01.dta)
# dataP <- stringr::str_interp("${path_source_p}/CRC_${M1}_MFRM_2010_APR19_COBR_V01.dta")
#
# Shuffle (PE056_S_rejected_applications.dta)
# dataS <- stringr::str_interp("${path_source_p}/PE056_${M2}_rejected_applications.dta")
#
# Randomized (CRC_R_MFRMBNK_2007_APR19_CO_V01.dta)
# dataR <- stringr::str_interp("${path_source_p}/CRC_${M3}_MFRMBNK_2007_APR19_CO_V01.dta")
#
# Dummy (SLB_D_YBNK_20102018_OCT20_QA1_V01.dta)
# dataD <- stringr::str_interp("${path_source_p}/SLB_${M4}_YBNK_20102018_OCT20_QA1_V01.dta")
#############################################################################################

# User Defined libraries
additionalPaths <- 
  c(
    ...
  )
.libPaths(additionalPaths)
rm(additionalPaths)
```

Then, in the master script, one needs to run the configuration file, as displayed in the following code snippet:


```R
source('config.R')
setwd(path_rep)

```

Please note that if your master script is not directly inside **path_rep**, perhaps in a folder below named *scripts*, you should position yourself that directory, by adding a line to the previous snippet:

```R
source('config.R')
setwd(path_rep)
setwd("scripts")
```

So, the **Stata** example would look like the following in **R** (using absolute and relative paths again):

**master.R**

```R
setwd(path_rep)

path_data <- stringr::str_interp("${path_rep}/data")
path_results <- stringr::str_interp("${path_rep}/results")

dir.create(path_data)
dir.create(path_results)

setwd("do_files")
source("data_creation.R")
```

**data_creation.R** - absolute paths

```R
library(haven)

dataP <- stringr::str_interp("${path_source_p}/PM110_BBS_${M1}_MBNK_JAN2000DEC2020_JUN21_ASSET_V01.dta")
df_base <- read_stata(dataP) 
df <- as.data.frame(df_base)

####
# code to modify data
#####

# save intermediate data
write_dta(df, file.path(path_data, "bbs_intermediate.dta"))
```

**data_creation.R** - relative paths

```R
library(haven)

dataP <- stringr::str_interp("${path_source_p}/PM110_BBS_${M1}_MBNK_JAN2000DEC2020_JUN21_ASSET_V01.dta")
df_base <- read_stata(dataP) 
df <- as.data.frame(df_base)

####
# code to modify data
#####

# save intermediate data
write_dta(df, "../data/bbs_intermediate.dta")
```