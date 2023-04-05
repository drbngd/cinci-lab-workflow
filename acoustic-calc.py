# ==================================================================================
# author:   Dhruv Raj Bangad (bangaddj@mail.uc.edu)
# purpose:  To calculate vai, f0IQR, f2 slopes, & vowel durations
# usage:    python3 acoustic-calc.py  <target_folder_address>
# prereq:   make sure meas-generator.py & xlsxerator.py have been run right before
# ==================================================================================

import os, sys, glob, pandas as pd
from openpyxl import load_workbook


# FUNCTION: calculates all the acoustic values and 
#           returns in pandas dataframe for individual file
def getAcousticCalc(file):
    # get data in a df from file
    print(f'acoustic-calc.py: Running calculations on {file}')
    df_in = pd.read_excel(file)

    # BEGIN: vai calculation
    # first get F1, F2, VOWELS for mid-value of each vowel
    print(f'acoustic-calc.py: Calculating VAI...')
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
    print(f'acoustic-calc.py: DONE calculating VAI')
    # END: vai calculation

    # BEGIN: F0 IQR calculation
    print(f'acoustic-calc.py: Calculating F0 IQR...')
    f0_q1 = df_in['f0'].quantile(0.25)
    f0_q3 = df_in['f0'].quantile(0.75)
    f0_IQR = f0_q3 - f0_q1
    print(f'acoustic-calc.py: DONE calculating F0 IQR')
    # END: F0 IQR calculation

    # BEGIN: F2 SLOPE calculations
    # getting required values
    print(f'acoustic-calc.py: Calculating F2 Slopes...')
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
    
    print(f'acoustic-calc.py: DONE calculating F2 Slopes')        
    # END: F2 slope calculation

    # BEGIN: vowel duration calculation
    print(f'acoustic-calc.py: Calculating Vowel Duration...')
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

    print(f'acoustic-calc.py: DONE calculating Vowel Duration')
    # END: vowel duration calculation

    # BEGIN: putting calculated data into a dataframe
    print(f'acoustic-calc.py: Adding calculated data to pandas dataframe...')
    df_out = pd.DataFrame(columns=['MEASUREMENT', 'VALUE'])

    # populating the data frame
    df_rows = [{'MEASUREMENT': 'VAI', 'VALUE': vai},
            {'MEASUREMENT': 'F0_IQR', 'VALUE': f0_IQR},
            {'MEASUREMENT': 'F2Slope_Narrow_AW', 'VALUE': f2_slope[0][0]},
            {'MEASUREMENT': 'F2Slope_Wide_AW', 'VALUE': f2_slope[0][1]},
            {'MEASUREMENT': 'F2Slope_Max_AW', 'VALUE': f2_slope[0][2]},
            {'MEASUREMENT': 'F2Slope_Narrow_AY', 'VALUE': f2_slope[1][0]},
            {'MEASUREMENT': 'F2Slope_Wide_AY', 'VALUE': f2_slope[1][1]},
            {'MEASUREMENT': 'F2Slope_Max_AY', 'VALUE': f2_slope[1][2]},
            {'MEASUREMENT': 'F2Slope_Narrow_EY', 'VALUE': f2_slope[2][0]},
            {'MEASUREMENT': 'F2Slope_Wide_EY', 'VALUE': f2_slope[2][1]},
            {'MEASUREMENT': 'F2Slope_Max_EY', 'VALUE': f2_slope[2][2]},
            {'MEASUREMENT': 'F2Slope_Narrow_OW', 'VALUE': f2_slope[3][0]},
            {'MEASUREMENT': 'F2Slope_Wide_OW', 'VALUE': f2_slope[3][1]},
            {'MEASUREMENT': 'F2Slope_Max_OW', 'VALUE': f2_slope[3][2]},
            {'MEASUREMENT': 'F2Slope_Narrow_OY', 'VALUE': f2_slope[4][0]},
            {'MEASUREMENT': 'F2Slope_Wide_OY', 'VALUE': f2_slope[4][1]},
            {'MEASUREMENT': 'F2slope_Max_OY', 'VALUE': f2_slope[4][2]},
            {'MEASUREMENT': '', 'VALUE': ''},
            {'MEASUREMENT': 'VOWEL_DURATION', 'VALUE': ''}]

    # populating with vowel durations
    # df_rows = []
    for i in range(len(vowel_duration[0])):
        df_rows.append({'MEASUREMENT': vowel_duration[0][i], 'VALUE': vowel_duration[1][i]})

    df_out = df_out.append(df_rows, ignore_index=True)
    print(f'acoustic-calc.py: DONE populating pandas data frame')
    return df_out
    # FUNCTION: end of function

# FUNCTION: generates a data set per sentence for the main results file
def getRowDataAllFiles(file, df):
    
    # df_in = pd.read_excel(file, sheet_name='CALCULATIONS')
    # adding data into a row:
    filename = os.path.splitext(os.path.basename(file))[0]
    values = [filename]
    values += list(df['VALUE'][0:17]) # getting values until F2SLOPE

    # calculating the vowel durations
    vowels_fromDF = list(df['MEASUREMENT'][19:])
    duration_fromDF = list(df['VALUE'][19:])
    
    # calculating duration for each vowel
    vowel_duration_data = [[0,0,0] for _ in range(15)] # initializing list for duration and count of each vowel
    total_vowel_duration = 0
    total_vowel_count = 0
    avg_vowel_duration = 0

    vowel_indices = {'AY': 0, 'AW': 1, 'OY': 2, 'EY': 3, 'OW': 4, 'IY': 5, 'IH': 6, 'EH': 7, 'AE': 8, 'UW': 9, 'UH': 10, 'AO': 11, 'AA': 12, 'AH0': 13, 'AH1': 14}

    for i, vowel in enumerate(vowels_fromDF):
        if vowel in vowel_indices:
            index = vowel_indices[vowel]
            vowel_duration_data[index][0] += duration_fromDF[i] # cumulating duration time
            vowel_duration_data[index][1] += 1                  # incrementing on occurences
            total_vowel_duration += duration_fromDF[i]
            total_vowel_count += 1
    
    # calculating average duration
    for i, vowel in enumerate(vowels_fromDF):
        if vowel in vowel_indices:
            index = vowel_indices[vowel]
            vowel_duration_data[index][2] = vowel_duration_data[index][0]/vowel_duration_data[index][1]

    # appending to values
    values += [val for sublist in vowel_duration_data for val in sublist]
    values += [total_vowel_duration, total_vowel_count, avg_vowel_duration]

    return values   # to be inserted as a new row in the all file dataframe
    # FUNCTION: end of function
    

    
'''---fetching all the files in the target dir---'''
# get all xlsx files in the target dir
wd = sys.argv[1]
print(f'acoustic-calc.py: Getting all the .xlsx files in {wd}...')

search_path = f'{wd}/*.xlsx'            # search text to get all .xlsx files in wd
xlsx_files = glob.glob(search_path)     # xlsx_files contains the addresses of all .xlsx files in wd
print('acoustic-calc.py: DONE FETCHING')
print(f'acoustic-calc.py: Number of files fetched: {len(xlsx_files)}')

'''---setting up results file's pandas dataframe and filename---'''
# file name for storing all file results
final_results_file = dir_address = wd + 'allfile_results.xlsx'

# data frame for the all results file
df_all = pd.DataFrame(columns=['SOURCE', 'VAI', 'F0_IQR', 'F2Slope_Narrow_AW', 'F2Slope_Wide_AW', 'F2Slope_Max_AW',
                                'F2Slope_Narrow_AY', 'F2Slope_Wide_AY', 'F2Slope_Max_AY', 'F2Slope_Narrow_EY', 'F2Slope_Wide_EY',
                                'F2Slope_Max_EY', 'F2Slope_Narrow_OW', 'F2Slope_Wide_OW', 'F2Slope_Max_OW', 'F2Slope_Narrow_OY',
                                'F2Slope_Wide_OY', 'F2Slope_Max_OY', 'AY_TOTAL_DURATION', 'AY_COUNT', 'AY_AVG_DURATION',
                                'AW_TOTAL_DURATION', 'AW_COUNT', 'AW_AVG_DURATION', 'OY_TOTAL_DURATION', 'OY_COUNT',
                                'OY_AVG_DURATION', 'EY_TOTAL_DURATION', 'EY_COUNT', 'EY_AVG_DURATION', 'OW_TOTAL_DURATION',
                                'OW_COUNT', 'OW_AVG_DURATION', 'IY_TOTAL_DURATION', 'IY_COUNT', 'IY_AVG_DURATION', 'IH_TOTAL_DURATION',
                                'IH_COUNT', 'IH_AVG_DURATION', 'EH_TOTAL_DURATION', 'EH_COUNT', 'EH_AVG_DURATION', 'AE_TOTAL_DURATION',
                                'AE_COUNT', 'AE_AVG_DURATION', 'UW_TOTAL_DURATION', 'UW_COUNT', 'UW_AVG_DURATION', 'UH_TOTAL_DURATION',
                                'UH_COUNT', 'UH_AVG_DURATION', 'AO_TOTAL_DURATION', 'AO_COUNT', 'AO_AVG_DURATION', 'AA_TOTAL_DURATION',
                                'AA_COUNT', 'AA_AVG_DURATION', 'AH0_TOTAL_DURATION', 'AH0_COUNT', 'AH0_AVG_DURATION', 'AH1_TOTAL_DURATION',
                                'AH1_COUNT', 'AH1_AVG_DURATION', 'TOTAL_VOWEL_DURATION', 'TOTAL_VOWEL_COUNT', 'AVG_VOWEL_DURATION'])


'''---starting calculation and processing of all the acoustic values---'''
# performing calculations on each collected file
# also getting row data for df_all dataframe
# https://stackoverflow.com/questions/42370977/how-to-save-a-new-sheet-in-an-existing-excel-file-using-pandas
for file in xlsx_files:
    df_file = getAcousticCalc(file)     # getting data frame with calculated values
    row_data = getRowDataAllFiles(file, df_file)    # getting row data for all results file
    
    # storing the calculated the acoustic values
    wbook = load_workbook(file)
    writer = pd.ExcelWriter(file, engine = 'openpyxl')
    writer.book = wbook
    df_file.to_excel(writer, sheet_name = 'CALCULATIONS') # added dataframe to a new sheet
    writer.close()
    print(f'acoustic-calc.py: ALL CALCULATIONS HAVE BEEN PERFORMED & STORED in {file}')
    
    df_all.loc[len(df_all)] = row_data
    print('acoustic-calc.py: and results have been written to the all_results.xlsx file\n')

# uploading row data to excel workbook
df_all.to_excel(final_results_file, 'RESULTS')
print(f'acoustic-calc.py: FINAL RESULTS file has been generated and is located here: {final_results_file}')
print('acoustic-calc.py: COMPLETED')
