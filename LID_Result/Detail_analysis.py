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
# set function
# --------------------
# function of get data of SWMM detail output
def import_modify(file_name):
    import pandas as pd
    # the names of columns
    column_names=['date_time', 'time(hr)', 'total_inflow', 'total_evap',
    'surface_infil','pavement_perc', 'soil_perc', 'storage_exfil', 
    'surface_runoff','drain_outflow', 'surface_level', 
    'pavement_level', 'soil_level','storage_level']
    useless = ['date_time', 'total_evap', 'storage_exfil','pavement_level']
    # level = ['surface_level', 'pavement_level','storage_level']
    
    # import and modify data
    df=pd.read_csv(file_name, skiprows=9, header=None, sep="\t")
    df.columns = column_names
    for i in useless:
        del df[i]
        column_names.remove(i)
    
    # add duration and period columns
    fsplit = file_name.split('-') 
    d = fsplit[0]
    p = fsplit[1].split('.')[0]
    df['period'] = p
    df['duration'] = d
    # change soil_moisture into water level in soil
    df['soil_level'] = df['soil_level']/0.25*400

    df = df.melt(['time(hr)','period','duration'], var_name='property',  value_name='value')
    # df['unit'] = df['property'].apply(lambda x:'mm' if x in level else 'mm/hr')
    return df

# function of find peak time from one rainfall
def peaktime(df,d,p):
    # create a filter to get total_inflow under specific duration, period
    filter0 = ((alldf['duration'] == d) & 
    (alldf['period'] == p) & 
    (alldf['property'] =='total_inflow'))
    # pick needed data 
    pick =alldf[filter0] # pick data frame
    pick_v = pick['value'].max() # pick peak value
    pick = pick[pick['value'] == pick_v] # pick the row which have peak value 
    pick_t = float(pick['time(hr)'].values) # the time which have peak value
    return pick_t, pick_v

#%%
# --------------------
# get data
# --------------------
# get data from .txt and change into DataFrame
file_list = glob('*.txt')
df_list = []
for file in file_list:
    df = import_modify(file)
    df_list.append(df)
alldf = pd.concat(df_list, axis='rows', ignore_index=True)
print(alldf.head())


#%%
import seaborn as sns
p_order = ['2year','5year' ,'10year' ,'25year' ,'50year' ,'100year']
d_order = ['1hr', '2hr', '3hr', '6hr', '9hr', '12hr']
pickdf = alldf[alldf['duration'] == d_order[0]]

# setting styles and figure
plt.clf()
# color codes for palette
mypal = ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd',
'#8c564b','#e377c2','#7f7f7f','#17becf']
sns.set_style("white")
sns.set_context("paper", font_scale=2)

# plot with FacetGird for same duration different periods
g = sns.FacetGrid(data=pickdf,col='period', hue='property', col_order=p_order, 
col_wrap=2, height=4,palette=mypal, aspect=1.25)
g = (g.map(sns.lineplot,'time(hr)', 'value')).set(xlim=(0, 1.2), ylim=(0, 1400))
for i in range(6):
    peak_time, peak_value = peaktime(alldf, d_order[0], p_order[i])
    # given the auxilary lines
    g.axes[i].axhline(y=150+peak_value/20, color='r', label='surface capacity', linestyle='--',linewidth=1)
    g.axes[i].axhline(y=450, color='k', label='drain pipe', linestyle='--',linewidth=1)
    g.axes[i].axvline(x=peak_time, color='r', label='peak', linestyle='--',linewidth=1)

# customizing setting
h, l = g.axes[0].get_legend_handles_labels()
g.add_legend(handles=h,labels=l, loc='right')
g.set_ylabels('value (mm/hr, mm)')
g.set_xlabels('time (hr)')
# plt.show()
plt.savefig('D:/梁崇淵/論文/Result/New/Detail/Bio/1hr.jpg',
bbox_inches='tight')