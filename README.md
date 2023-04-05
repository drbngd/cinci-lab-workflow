# cinci-lab-workflow

This repository contains the workflow used by the Cinci Lab for processing and analyzing acoustic data. The workflow consists of three Python scripts: `acoustic-calc.py`, `meas-generator.py`, and `xlsxerator.py`. These scripts automate the process of generating acoustic measurements and exporting data to Excel files.

## Installation

To use the Cinci Lab Workflow, you'll need to have Python 3 installed on your machine. You can download the latest version of Python from the official website: https://www.python.org/downloads/.

Once you have Python installed, you can download the Cinci Lab Workflow repository by running the following command in your terminal:

```
git clone https://github.com/drbngd/cinci-lab-workflow.git
```


## Usage

To use the Cinci Lab Workflow, navigate to the directory where the repository is located and run one of the following commands:

```
python3 acoustic-calc.py /path/to/directory
python3 meas-generator.py <gender> /path/to/directory
python3 xlsxerator.py /path/to/directory
```

- `acoustic-calc.py` takes a directory containing .txt files as input and generates .meas files with acoustic measurements.
- `meas-generator.py` takes the patient's gender and a directory containing .meas files as input and generates a new .meas file with summary statistics for the patient.
- `xlsxerator.py` takes a directory containing .meas files as input and generates Excel files with summary statistics for each patient.

Make sure to replace `/path/to/directory` with the path to the directory you want to operate on, and replace `<gender>` with "male", "female", or "child" depending on the patient's gender.


