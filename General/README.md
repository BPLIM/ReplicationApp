# ReplicationApp

Python application to create a replication package. The application may be used by researchers to ensure that their analysis is reproducible.

## Version
Python >= 3.6

## Dependencies
PySimpleGUI

## Installation

1. Install [PySimpleGUI](https://www.pysimplegui.org/en/latest/)

Using **pip**
```
pip install PySimpleGUI
```

Using **conda**
```
conda install -c conda-forge pysimplegui
```


2. Clone this repository 


3. Open a terminal, move to the directory that was cloned in the previous step and type:

```
python3 replicationApp.py
```



It is possible to use a [Singularity](https://sylabs.io/singularity/) container to control your software environment. In such case, it is **very important** that, when creating the container, the definition file contains the following instructions:

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


