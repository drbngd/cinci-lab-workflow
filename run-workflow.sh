#!/bin/bash
# ==================================================================================
# author:   Dhruv Raj Bangad (bangaddj@mail.uc.edu)
# purpose:  To automate .meas generation, .xlsx conversion, 
#           and acoustic values calculations
# usage:    ./run-workflow.sh <full/path/to/target/dir/>
# prereq:   make sure you run the setup-workflow.sh file
#           to get any missing dependencies
# ==================================================================================

directory="$1"

read -p "This script will delete/overwrite all existing {.TextGrid}, {.meas}, and {.xlsx} files. Do you want to continue? (y/n): " answer

if [[ "$answer" =~ [yY](es)* ]]; then
    if [ -d "$directory" ]; then
        rm -rf $directory*.xlsx
        rm -rf $directory*.meas
        rm -rf $directory*.TextGrid
        read -p "Select patient's gender for files being run (male/female/child): " gender
        ./run_scripts/textgrid-generator.sh "$directory"                # generate .TextGrid files
        python3 run_scripts/meas-generator.py "$gender" "$directory"    # generate .meas files
        python3 run_scripts/xlsxerator.py "$directory"                  # convert .meas to .xlsx 
        python3 run_scripts/acoustic-calc.py "$directory"               # do all the calculations
    else
        echo "Directory does not exist"
    fi
else
    echo "Exiting script"
fi
