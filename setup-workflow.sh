#!/bin/bash

# unzip htk
cd htk_files/
sudo bpm-update htk_local
cd ..

# update pip version
sudo apt-get update
curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
python get-pip.py

# these are the dependencies to be installed for this project
pip install psutil
pip install pandas
pip install openpyxl
pip install numpy
pip install XlsxWriter
