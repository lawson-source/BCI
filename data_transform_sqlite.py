# -*- coding: utf-8 -*-
"""
The raw data is filtered. Each product id only keep a record that  value of deviation is  maximum.
"""
import os
import sqlite3 as db

import pandas as pd

engine = db.connect('wujinDB.db')
dirf = os.path.abspath(os.path.dirname(__file__))  # root directory
File_dir = dirf + '/data'  # directory of data source
Filelist = os.listdir(File_dir)  # all of file name of data source
for i in range(0, len(Filelist)):
    if Filelist[i] == ".DS_Store":
        continue
    print(i, Filelist[i] + '--start')
    data = pd.read_csv(File_dir + '/' + Filelist[i])
    # data = data.dropna()
    data['Production Date'] = pd.to_datetime(data['Production Date'].str.replace(' ASIA/SHANGHAI', ''),
                                             format='%d-%b-%y %I.%M.%S.%f %p', errors='ignore')
    data = data.sort_values('Deviation', ascending=False)
    data = data.drop_duplicates('Ident No.', keep='first')
    data.to_sql('dataunique', engine, if_exists='append', index=None, )
    print(i, Filelist[i] + '--end')
