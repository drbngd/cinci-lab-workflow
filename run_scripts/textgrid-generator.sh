#!/bin/bash
# ==================================================================================
# author:   Dhruv Raj Bangad (bangaddj@mail.uc.edu)
# purpose:  To generate .TextGrid scripts using pyalign
# usage:    ./textgrid-generator.sh <path/to/target/dir/>
# prereq:   make sure you have .wav and .lab files in the target directory
# ==================================================================================

# Check if pyalign is installed
command -v pyalign >/dev/null 2>&1 || { echo >&2 "pyalign is required but not installed. Aborting."; exit 1; }

# Get the target directory as argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <target_directory>"
    exit 1
fi

# Check if the target directory exists
if [ ! -d "$1" ]; then
    echo "Error: directory '$1' not found"
    exit 1
fi

# Get all .wav and .lab files in the target directory
wav_files=$(find "$1" -name "*.wav")
lab_files=$(find "$1" -name "*.lab")

# Generate .TextGrid files for each pair of .wav and .lab files
for wav_file in $wav_files; do
    name=$(basename "$wav_file" .wav)
    lab_file="$1/$name.lab"
    textgrid_file="$1/$name.TextGrid"
    if [ -f "$lab_file" ]; then
        echo "Generating TextGrid file for $name ..."
        pyalign "$wav_file" "$lab_file" "$textgrid_file"
        echo "Done."
    else
        echo "Warning: .lab file not found for $name.wav"
    fi
done
