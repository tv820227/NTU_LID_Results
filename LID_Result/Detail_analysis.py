#%%
# --------------------
# pre-processing
# --------------------
import matplotlib.pyplot as plt
import matplotlib.markers as mak
import pandas as pd
import numpy as np
import os

# define to path to reach data
path = 'D:/梁崇淵/論文/Result/DetailReport-2017-07-19/text/Bio'
os.chdir(path)

#%%
# --------------------
# get data
# --------------------
# get data from .txt and change into DataFrame
from glob import glob

def import_modify(file_name):
    # the names of columns
    column_names=['date_time', 'time(hr)', 'total_inflow', 'total_evap',
    'surface_infil','pavement_perc', 'soil_perc', 'storage_exfil', 
    'surface_runoff','drain_outflow', 'surface_level', 
    'pavement_level', 'soil_moisture','storage_level']
    level = ['surface_level', 'pavement_level','storage_level']
    
    # import and modify data
    df=pd.read_csv(file_name, skiprows=9, header=None, sep="\t")
    df.columns = column_names
    del df['date_time']
    del column_names[0]
    
    # add duration and period columns
    fsplit = file_name.split('-') 
    d = fsplit[0]
    p = fsplit[1].split('.')[0]
    df['period'] = p
    df['duration'] = d

    df = df.melt(['time(hr)','period','duration'], var_name='property',  value_name='value')
    df['unit'] = df['property'].apply(lambda x:'mm' if x in level else 'mm/hr')
    return df

file_list = glob('*.txt')
df_list = []
for file in file_list:
    df = import_modify(file)
    df_list.append(df)
alldf = pd.concat(df_list, axis='rows', ignore_index=True)
print(alldf.head())


# df['unit'] = df['cols'].apply(x:'mm' if x in mm else 'mm/hr')

# #%%
# import seaborn as sns
# # setting styles and figure
# fig ,ax= plt.subplots(figsize=(9, 7.5))
# sns.set_style("white")
# sns.set_context("paper", font_scale=2)
# sns.lineplot(x='time(hr)', y='vals', hue='cols', data=df, palette='husl')

# plt.xlim([0,1.2])
# plt.ylim([0,800])
# plt.show()

#%%

print(leveldf.head)

#%%
import seaborn as sns
p_order = ['2year','5year' ,'10year' ,'25year' ,'50year' ,'100year']
d_order = ['1hr', '2hr', '3hr', '6hr', '9hr', '12hr']
level_filter = (alldf['duration']== d_order[0]) & (alldf['unit']=='mm')
speed_filter = (alldf['duration']== d_order[0]) & (alldf['unit']=='mm/hr') 
leveldf = alldf[level_filter]
speeddf = alldf[speed_filter]

# setting styles and figure
plt.clf()
# fig = plt.figure(figsize=(12,10))
sns.set_style("white")
sns.set_context("paper", font_scale=2)
g = sns.FacetGrid(data=speeddf,col='period', hue='property', col_order=p_order, col_wrap=2, height=5,palette='dark')
g = (g.map(sns.lineplot,'time(hr)', 'value')).set(xlim=(0, 1.2), ylim=(0, 1400)).add_legend()
# ax2 = plt.twinx()
# g = (g.map(sns.lineplot,x='time(hr)', 'value')).set(xlim=(0, 1.2), ylim=(0, 1400)).add_legend()
for i in range(6):
    g.axes[i].axhline(y=250, color='r', label='surface capacity', linestyle='--',linewidth=2)
    g.axes[i].axhline(y=450, color='k', label='drain pipe', linestyle='--',linewidth=2)
    ax2 = g.axes[i].twinx()
    sns.lineplot(x='time(hr)',y='value', hue='property', data=leveldf, ax=ax2)
plt.show()