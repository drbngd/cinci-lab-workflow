# ==================================================================================
# author:   Dhruv Raj Bangad (bangaddj@mail.uc.edu)
# purpose:  To generate .meas files through the meas_formants.py code
# usage:    python3 meas-generator.py  <male/female/chile> <target_folder_address>
# prereq:   meas_formants.py & meas-generator.py should be in the samee dir
#           all the .TextGrid & .wav & .lab files in the target dir
#           should have the same gender
# ==================================================================================

import os, sys, glob

# get all .TextGrid files
gender = str(sys.argv[1])
wd = str(sys.argv[2])
print(f'meas-generator.py: Getting all the .TextGrid files in {wd}...')

search_path = f'{wd}/*.TextGrid'            # search text to get all .meas files in wd
tg_files = glob.glob(search_path)     # meas_files contains the addresses of all .TextGrid files in wd
print('meas-generator.py: DONE FETCHING')
print(f'meas-generator.py: Number of files fetched: {len(tg_files)}\n')


success_count = 0
print('meas-generator.py: Running meas_formants.py on each .TextGrid file...')
for file in tg_files:
    print(f'meas-generator.py: Generating .meas file for {file}')
    exit_code = os.system(f'python3 run_scripts/meas_formants.py {gender} {file}')
    if exit_code != 0:
        print('meas-generator.py: ERROR while generating .meas file for {file}')
        print('meas-generator.py: make sure that .wav and .lab files are present as well')
    else:
        print('meas-generator.py: DONE')
        success_count += 1
        

print('meas-generator.py: COMPLETED generation of .meas files')
print(f'meas-generator.py: MEAS FILES GENERATED - {success_count} | FAILS - {len(tg_files) - success_count}')
