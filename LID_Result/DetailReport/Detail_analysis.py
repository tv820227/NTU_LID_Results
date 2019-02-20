#%%
# --------------------
# pre-processing
# --------------------
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def maincode(mode):
    # --------------------
    # pre-processing
    # --------------------
    # get data from .txt and change into DataFrame
    from glob import glob
    # import Detail_plot as dp
    import Detail_subplot as dsp
    from ImportModify import import_modify
    file_list = glob('*.txt')
    df_list = []
    for file in file_list:
        df = import_modify(file)
        df_list.append(df)
    alldf = pd.concat(df_list, axis='rows', ignore_index=True)
    # in Detail_plot does not make this modify
    alldf = alldf.set_index('time(hr)')

    # plot figures
    d_order = ['1hr', '2hr', '3hr', '6hr', '9hr', '12hr']
    for i in d_order:
        # dp.detail_plot(alldf,i,mode)
        dsp.detail_plot(alldf,i,mode)
        print('Duration '+i+' is finished.')

# define to path to reach data
for i in ('Bio', 'Pav'):
    path = 'C:\\Chung-Yuan\\Publish\\Result\\DetailReport-2017-07-19\\text\\%s'%(i)
    os.chdir(path)
    maincode(i)
