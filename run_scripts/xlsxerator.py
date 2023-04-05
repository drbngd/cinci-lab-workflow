# ===============================================================================
# author:   Dhruv Raj Bangad (bangaddj@mail.uc.edu)
# purpose:  To convert .meas -> .xlsx and add a new sheet named 'calculations'
# usage:    python3 xlsxerator.py <target_folder_address>
# ===============================================================================

import os, sys, glob, pandas as pd

wd = str(sys.argv[1])
print(f'xlsxerator.py: Getting all the .meas files in {wd}...')

search_path = f'{wd}/*.meas'            # search text to get all .meas files in wd
meas_files = glob.glob(search_path)     # meas_files contains the addresses of all .meas files in wd
print('xlsxerator.py: DONE FETCHING')
print(f'xlsxerator.py: Number of files fetched: {len(meas_files)}')


for file in meas_files:
    print(f'xlsxerator.py: Converting {file} into .xlsx')
    xlsx_name = f'{os.path.splitext(file)[0]}.xlsx'
    # df = pd.read_csv(file, sep='\s+', header=None)
    df = pd.read_csv(file , delim_whitespace=True)
    df.to_excel(xlsx_name, 'MEAS_DATA')
    print('xlsxerator.py: DONE')

print('xlsxerator.py: COMPLETED All .meas files have been converted to .xlsx')
