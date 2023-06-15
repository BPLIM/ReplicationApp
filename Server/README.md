# ReplicationApp
Application for researchers to use on the External Server when working with perturbed data. The use of the application should be mandatory for researchers working with perturbed data. Researchers not working with modified data might still find the application useful, since one of the byproducts of the application is the creation of a replication package, which improves the reproducibility of results.

## Version
Python >= 3.6

## Dependencies
PySimpleGUI

## Installation

### BPLIM Staff

Example for project **pxxx_BPLIM**

Tree structure of project

```
Root: /bplimext/projects/pxxx_BPLIM
├── initial_dataset/
├── results/
├── tools/
└── work_area
```

1. Clone this repository 

2. Create directory named `.replication` under `work_area`

3. Copy the files in the **Server** version of the Application to the directory created in the previous step

4. Open a terminal and type the following commands:

```
cd /bplimext/projects/pxxx_BPLIM/work_area
chmod -R 755 .replication
```

5. Create a file named `ReplicationApp.desktop` under `work_area`. The file should look like this:

```
#!/usr/bin/env xdg-open
[Desktop Entry]
Name=Run Replication
Exec=cd "$(dirname %k)" && python3 .replication/replicationApp.py -p "$(dirname %k)";
Icon=/bplimext/projects/pxxx_BPLIM/work_area/.replication/.images/appLogo.gif
Terminal=false
Type=Application
Categories=Application;
```

In 4 and 5, replace *pxxx_BPLIM* with the name of the project.

**Important Note**: researchers must use a container to run the analysis. When creating the container, it is very important that the definition file contains the following 
instructions:

**Stata**
```
%runscript
    if [ $# -ne 2 ]; then
        echo "Please provide the main path and main script"
        exit 1
    fi
    cd "$1"
    log="$(basename -s .do "$2").log"
    stata-mp -e do "$2"
    if tail -1 "$log" | egrep "^r\([0-9]+\);"
    then
        exit 1
    else
        exit 0
    fi
```

**Python**
```
%runscript
    if [ $# -ne 2 ]; then
        echo "Please provide the main path and main script"
        exit 1
    fi
    cd "$1"
    python3 "$2"
```

**R**
```
%runscript
    if [ $# -ne 2 ]; then
        echo "Please provide the main path and main script"
        exit 1
    fi
    cd "$1"
    Rscript "$2"
```

### Researcher

To use the application, the user must have **PySimpleGUI** installed. In order to do so, he or she must:


1. Open a terminal and type:

```
cd ~ 
installPySimpleGui.sh
```

After these steps, the researcher may click on the desktop file to launch the application.


