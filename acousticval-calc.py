# ==================================================================================
# author:   Dhruv Raj Bangad (bangaddj@mail.uc.edu)
# purpose:  To calculate vai, f0IQR, f2 slopes, & vowel durations
# usage:    python3 acousticval-calc.py  <target_folder_address>
# prereq:   make sure meas-generator.py & xlsxerator.py have been run right before
# ==================================================================================

import os, sys, math, glob, pandas as pd, numpy as np
from openpyxl import load_workbook


# FUNCTION: calculates all the acoustic values and 
#           returns in pandas dataframe for individual file
def getAcousticCalc(file):
    # get data in a df from file
    print(f'acousticval-calc.py: Running calculations on {file}')
    df_in = pd.read_excel(file)

    # BEGIN: vai calculation
    # first get F1, F2, VOWELS for mid-value of each vowel
    print(f'acousticval-calc.py: Calculating VAI...')
    vai = ''
    vowels = list(df_in['vowel'])
    f1 = list(df_in['f1'])
    f2 = list(df_in['f2'])
    vowel_list_vai = ['AA', 'IY', 'UW']

    vowels_mid = []
    f1_mid = []
    f2_mid = []

    # keeping only the 4th vowel split value for each vowel
    for i in range(3,len(vowels),7):
        if vowels[i] in vowel_list_vai:
            vowels_mid.append(vowels[i])
            f1_mid.append(f1[i])
            f2_mid.append(f2[i])

    # simple list structure to calc avg F1 & F2:
    # vowel_sound = [count, f1, f2, False]
    aa = [0, 0, 0, False]
    iy = [0, 0, 0, False]
    uw = [0, 0, 0, False]
    # averaging F1 & F2 for each vowel
    for i, vowel in enumerate(vowels_mid):
        if vowel == 'AA':
            aa[0] += 1
            aa[1] += f1_mid[i]
            aa[2] += f2_mid[i]
            aa[3]  = True          # set to True to indicate that the vowel exists
        elif vowel == 'IY':
            iy[0] += 1
            iy[1] += f1_mid[i]
            iy[2] += f2_mid[i]
            iy[3]  = True           # set to True to indicate that the vowel exists
        elif vowel == 'UW':
            uw[0] += 1
            uw[1] += f1_mid[i]
            uw[2] += f2_mid[i]
            uw[3]  = True           # set to True to indicate that the vowel exists

    # checking if any vowel was absent
    if aa[3] and iy[3] and uw[3]:   # if True -> all the three vowels were present
        aa[1] = aa[1]/aa[0]     # avg of f1 for aa
        aa[2] = aa[2]/aa[0]     # avg of f2 for aa
        iy[1] = iy[1]/iy[0]     # avg of f1 for iy
        iy[2] = iy[2]/iy[0]     # avg of f2 for iy
        uw[1] = uw[1]/uw[0]     # avg of f1 for uw
        uw[2] = uw[2]/uw[0]     # avg of f2 for uw
        vai_num = (iy[2]+aa[1])/(iy[1]+uw[1]+uw[2]+aa[2])
        vai = str(vai_num)  
    else:                           # if False -> one of the vowels wasn't present
        vai = 'NA'              # vai is NA is one or more vowels were absent   
    print(f'acousticval-calc.py: DONE calculating VAI')
    # END: vai calculation

    # BEGIN: F0 IQR calculation
    print(f'acousticval-calc.py: Calculating F0 IQR...')
    f0_q1 = df_in['f0'].quantile(0.25)
    f0_q3 = df_in['f0'].quantile(0.75)
    f0_IQR = f0_q3 - f0_q1
    print(f'acousticval-calc.py: DONE calculating F0 IQR')
    # END: F0 IQR calculation

    # BEGIN: F2 SLOPE calculations
    # getting required values
    print(f'acousticval-calc.py: Calculating F2 Slopes...')
    f2 = list(df_in['f2'])
    lintime = list(df_in['lintime'])
    vowels = list(df_in['vowel'])

    rows, cols = (5, 4)
    f2_slope = [[0 for i in range(cols)] for j in range(rows)]
    # f2_slope is 2D list with following structure
    #     f2SlopeNarrow  f2SlopeWide f2SlopeMax vowelCount
    # AW              0            0          0          0  
    # AY              0            0          0          0
    # EY              0            0          0          0
    # OW              0            0          0          0
    # OY              0            0          0          0

    # calculating F2 SLOPE - narrow, wide, & max
    tb_row = 7
    i = 0
    while i < len(vowels):
        if vowels[i] == 'AW':   tb_row = 0
        elif vowels[i] == 'AY': tb_row = 1
        elif vowels[i] == 'EY': tb_row = 2
        elif vowels[i] == 'OW': tb_row = 3
        elif vowels[i] == 'OY': tb_row = 4
        else:
            i+=7
            continue
        # np.seterr(divide='ignore')
        f2_slope[tb_row][0] += (f2[i+1] - f2[i+5])/(lintime[i+1] - lintime[i+5])   # F2 Narrow Slope
        f2_slope[tb_row][1] += (f2[i+0] - f2[i+6])/(lintime[i+0] - lintime[i+6])   # F2 Wide Slope
        # F2 SLOPE Max calculations
        max_slope = 0
        for  u in range(7):
            for v in range(u+1,7): # range(u+1,7) reduces the redundant comparisons like 0,0 or 1,1 or (4,5 and 5,4)
                slope = (f2[i+u] - f2[i+v])/(lintime[i+u] - lintime[i+v])
                if abs(slope) > abs(max_slope): # looking for the max slope possible
                    max_slope = slope
        f2_slope[tb_row][2] += max_slope   # F2 Max Slope
        f2_slope[tb_row][3] += 1   # incrementing the vowel count
        i += 7  # moving onto next vowel

    # averaging the slopes using vowel frequency
    for i in range(rows):
        for j in range(cols - 1):
            if f2_slope[i][3] != 0:
                f2_slope[i][j] /= f2_slope[i][3]
            else:
                f2_slope[i][j] = 'NA'   # if den == 0, then slope is NaN
    
    print(f'acousticval-calc.py: DONE calculating F2 Slopes')        
    # END: F2 slope calculation

    # BEGIN: vowel duration calculation
    print(f'acousticval-calc.py: Calculating Vowel Duration...')
    valid_vowel_list = ['AY','AW','OY','EY','OW','IY','IH','EH','AE','UW','UH','AO','AA','AH0','AH1'] # all the vaild vowels
    vowel_duration = [[],[]]    # [[vowel], [duration]]
    vowels = list(df_in['vowel'])
    stress = list(df_in['stress'])
    t2 = list(df_in['t2'])
    t1 = list(df_in['t1'])
    i = 0
    while i < len(vowels):
        if vowels[i] in valid_vowel_list and stress[i] == 1: # if vowel is a vaild vowel and is stressed
            vowel_duration[0].append(vowels[i])
            vowel_duration[1].append(t2[i]-t1[i])
        i+=7    # skipping to next vowel

    print(f'acousticval-calc.py: DONE calculating Vowel Duration')
    # END: vowel duration calculation

    # BEGIN: putting calculated data into a dataframe
    print(f'acousticval-calc.py: Adding calculated data to pandas dataframe...')
    df_out = pd.DataFrame(columns=['MEASUREMENT', 'VALUE'])

    # populating the data frame
    df_rows = [{'MEASUREMENT': 'VAI', 'VALUE': vai},
            {'MEASUREMENT': 'F0 IQR', 'VALUE': f0_IQR},
            {'MEASUREMENT': 'F2 Slope Narrow AW', 'VALUE': f2_slope[0][0]},
            {'MEASUREMENT': 'F2 Slope Wide AW', 'VALUE': f2_slope[0][1]},
            {'MEASUREMENT': 'F2 Slope Max AW', 'VALUE': f2_slope[0][2]},
            {'MEASUREMENT': 'F2 Slope Narrow AY', 'VALUE': f2_slope[1][0]},
            {'MEASUREMENT': 'F2 Slope Wide AY', 'VALUE': f2_slope[1][1]},
            {'MEASUREMENT': 'F2 Slope Max AY', 'VALUE': f2_slope[1][2]},
            {'MEASUREMENT': 'F2 Slope Narrow EY', 'VALUE': f2_slope[2][0]},
            {'MEASUREMENT': 'F2 Slope Wide EY', 'VALUE': f2_slope[2][1]},
            {'MEASUREMENT': 'F2 Slope Max EY', 'VALUE': f2_slope[2][2]},
            {'MEASUREMENT': 'F2 Slope Narrow OW', 'VALUE': f2_slope[3][0]},
            {'MEASUREMENT': 'F2 Slope Wide OW', 'VALUE': f2_slope[3][1]},
            {'MEASUREMENT': 'F2 Slope Max OW', 'VALUE': f2_slope[3][2]},
            {'MEASUREMENT': 'F2 Slope Narrow OY', 'VALUE': f2_slope[4][0]},
            {'MEASUREMENT': 'F2 Slope Wide OY', 'VALUE': f2_slope[4][1]},
            {'MEASUREMENT': 'F2 Slope Max OY', 'VALUE': f2_slope[4][2]},
            {'MEASUREMENT': '', 'VALUE': ''},
            {'MEASUREMENT': 'VOWEL DURATION', 'VALUE': ''}]

    # populating with vowel durations
    # df_rows = []
    for i in range(len(vowel_duration[0])):
        df_rows.append({'MEASUREMENT': vowel_duration[0][i], 'VALUE': vowel_duration[1][i]})

    df_out = df_out.append(df_rows, ignore_index=True)
    print(f'acousticval-calc.py: DONE populating pandas data frame')
    return df_out
    # FUNCTION: end of function


# get all xlsx files
wd = sys.argv[1]
print(f'acousticval-calc.py: Getting all the .xlsx files in {wd}...')

search_path = f'{wd}/*.xlsx'            # search text to get all .xlsx files in wd
xlsx_files = glob.glob(search_path)     # xlsx_files contains the addresses of all .xlsx files in wd
print('acousticval-calc.py: DONE FETCHING')
print(f'acousticval-calc.py: Number of files fetched: {len(xlsx_files)}')


# create a new dataframe for all files in a folder
df_all = pd.DataFrame()

# performing calculations on each collected file
# https://stackoverflow.com/questions/42370977/how-to-save-a-new-sheet-in-an-existing-excel-file-using-pandas
for file in xlsx_files:
    df_file = getAcousticCalc(file)     # getting data frame with calculated values

    wbook = load_workbook(file)
    writer = pd.ExcelWriter(file, engine = 'openpyxl')
    writer.book = wbook
    df_file.to_excel(writer, sheet_name = 'CALCULATIONS') # added dataframe to a new sheet
    writer.close()
    print(f'acousticval-calc.py: ALL CALCULATIONS HAVE BEEN PERFORMED on {file}')
    print('acousticval-calc.py: ')


# get all the values in it and send to the calculator
# add a new sheet and add the calculations in it
# also generate a row to be added for the main df


# df for each individual file

# df for the main excel sheet


# calculation for each excel sheet