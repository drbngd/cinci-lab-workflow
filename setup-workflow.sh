#!/bin/bash

# unzip htk
sudo tar -xvf htk_files/HTK-3.4.1.tar.gz
sudo bpm-update htk_local

# update pip version
sudo python -m pip install -U pip

# these are the dependencies to be installed for this project
pip install psutil
pip install pandas
pip install openpyxl
pip install numpy
pip install XlsxWriter
 
