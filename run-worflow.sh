#!/bin/bash
# ==================================================================================
# author:   Dhruv Raj Bangad (bangaddj@mail.uc.edu)
# purpose:  To automate .meas generation, .xlsx conversion, 
#           and acoustic values calculations
# usage:    ./run-workflow.sh <path/to/target/dir/>
# prereq:   make sure you run the setup-workflow.sh file
#           to get any missing dependencies
# ==================================================================================

directory="$1"

read -p "This script will overwrite all existing .meas and .xlsx files. Do you want to continue? (y/n): " answer

if [[ "$answer" =~ [yY](es)* ]]; then
    if [ -d "$directory" ]; then
        rm -rf $directory*.xlsx
        rm -rf $directory*.mean
        read -p "Select patient's gender for files being run (male/female/child): " gender
        python3 meas-generator.py "$gender" "$directory"
        python3 xlsxerator.py "$directory"
        python3 acoustic-calc.py "$directory"
    else
        echo "Directory does not exist"
    fi
else
    echo "Exiting script"
fi
