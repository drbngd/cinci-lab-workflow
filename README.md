# cinci-lab-workflow

This repository contains the workflow used by the Cinci Lab for processing and analyzing acoustic data. The workflow consists of three Python scripts: `acoustic-calc.py`, `meas-generator.py`, and `xlsxerator.py`. These scripts automate the process of generating acoustic measurements and exporting data to Excel files.

## Installation

To use the Cinci Lab Workflow, you'll need to have Python 3 installed on your machine. You can download the latest version of Python from the official website: https://www.python.org/downloads/.

Once you have Python installed, you can download the Cinci Lab Workflow repository by running the following command in your terminal:

```
git clone https://github.com/drbngd/cinci-lab-workflow.git
```


## Usage

The Cinci Lab Workflow can be used to generate summary statistics for acoustic data in three steps:

1. **Generate .meas files with acoustic measurements**. Run `acoustic-calc.py` with the path to a directory containing .txt files as input to generate .meas files with acoustic measurements. For example:

```
python3 meas-generator.py <gender> /path/to/directory
```

2. **Generate summary statistics for a single patient**. Run `meas-generator.py` with the patient's gender and the path to a directory containing .meas files as input to generate a new .meas file with summary statistics for the patient. Replace `<gender>` with "male", "female", or "child" depending on the patient's gender. For example:

```
python3 meas-generator.py <gender> /path/to/directory
```

3. **Generate Excel files with summary statistics for all patients**. Run `xlsxerator.py` with the path to a directory containing .meas files as input to generate Excel files with summary statistics for each patient. For example:

```
python3 xlsxerator.py /path/to/directory
```

Make sure to replace `/path/to/directory` with the path to the directory you want to operate on, and replace `<gender>` with the patient's gender.



