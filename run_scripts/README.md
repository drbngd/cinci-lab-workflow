## Scripts in `run_scripts/` folder

The CINCI-Lab Workflow can be used to generate summary statistics for acoustic data in four steps:

1. **Generate .TextGrid files**. The `textgrid-generator.sh` file generates `Praat` `.TextGrid` files for all `.wav` and `.lab` in the specified directory. The script uses the pyalign tool to generate the TextGrid files, which are used to visualize and annotate the `.wav` files in `Praat`. Run this file with the path to the directory containing the `.wav` and `.lab` files. For example:

```
cd cinci-lab-workflow/run_scripts/
./textgrid-generator.sh /path/to/directory
```
> This file will generate .TextGrid files for all the .wav and .lab files present in the directory.

2. **Generate .meas files**. Run `meas-generator.py` with the patient's gender and the path to the directory containing .TextGrid files(along with .wav & .lab) as input to generate .meas files with acoustic measurements. Replace `<gender>` with "male", "female", or "child" depending on the patient's gender. For example:

```
cd cinci-lab-workflow/run_scripts/
python3 meas-generator.py <gender> /path/to/directory
```
> This file will generate .meas files for all the .TextGrid files present in the directory.


3. **Convert all .meas files to .xlsx**. Run `xlsxerator.py` with the path to a directory containing .meas files as input to generate Excel files. This is important as analysis can't be performed on a .meas file. For example:

```
cd cinci-lab-workflow/run_scripts/
python3 xlsxerator.py /path/to/directory
```

4. **Perform all the Calculations and Generate an excel f**. Run `acoustic-calc.py` with the path to a directory containing .xlxs files as input to perform the calculations to get VAI, F0 IQR, F2 Slopes, and Vowel Durations. The acoustic values can be found in each .xlsx file in a sheet named `CALCULATIONS`. Additionally, it will generate a `allfiles_result.xlsx` which will contain all the data for each file in one sheet. This can be run as follows:

```
cd cinci-lab-workflow/run_scripts/
python3 acoustic-calc.py /path/to/directory
```

Make sure to replace `/path/to/directory` with the path to the directory you want to operate on, and replace `<gender>` with the patient's gender.
