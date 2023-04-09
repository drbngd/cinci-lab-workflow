# cinci-lab-workflow

This repository contains the workflow used by the Cinci Lab for processing and analyzing acoustic data. The workflow consists of three Python scripts: `acoustic-calc.py`, `meas-generator.py`, and `xlsxerator.py`. These scripts automate the process of generating acoustic measurements and exporting data to Excel files.

## Installation

You can download the Cinci Lab Workflow repository by running the following command in your terminal:

```
git clone https://github.com/drbngd/cinci-lab-workflow.git
chmod -R +x cinci-lab-workflow
```

## Setup

Before using these scripts, you will need to install the necessary dependencies. This step will:
1. Build & Install HTK 3.4.1
2. Install & Update pip
3. Download necessary python libraries

To do so, run the following command:

```
cd cinci-lab-workflow/
./setup-workflow.sh
```

## Run
**Run all of the above scripts using just the `run-workflow.sh` file.** This is a bash script which will run all the run-scripts for you. 

This one command will perform all the following functions:
1. Generate .TextGrid files from .wav and .lab
2. Generate .meas files from .TextGrid, .wav, and .lab
3. Convert .meas files into .xlsx
4. Perform VAI, F0 IQR, F2 Slope, & Vowel Duration calculations and store the resutls in `allfiles_result.xlsx`

```
cd cinci-lab-workflow/
./run-workflow.sh /path/to/directory
```
> This file will ask you to specify the gender after running it, as it is important to generate the .meas files
