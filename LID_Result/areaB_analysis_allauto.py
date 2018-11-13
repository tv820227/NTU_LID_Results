#%%
import matplotlib.pyplot as plt
import matplotlib.markers as mak
import pandas as pd
import numpy as np
import os

# define to path to reach data
path = 'D:\梁崇淵\論文\Result\OptimalResult\Billion\Picked'
os.chdir(path)

#%%
# get data from .txt and change into DataFrame
from glob import glob
file_list = glob('*.txt')
df_list = []
for file in file_list:
    df = pd.read_csv(file, skiprows=1, header=0, sep="\t")
    drop_index = list(df.index)[-4:]
    df = df.drop(drop_index)

    # change column index
    df = df[['Subcatchment', 'Bio_Area', 'Pav_Area']]
    df.columns = ['Sub', 'Bio_Area', 'Pav_Area']
    
    # label rain style into duration and period 
    rain = file.split('-')[0]
    df['duration'] = rain.split('_')[0]
    df['period'] = rain.split('_')[1]

    df_list.append(df)

#%%
# concat all data into one DataFrame
alldf = pd.concat(df_list, axis='rows', ignore_index=True)
# read information of subcatchment and merge into results of simulation
subdf = pd.read_csv('../../Subcatchment.csv')
alldf = pd.merge(alldf, subdf, on='Sub')
# calculate the ratio of intalled LID
alldf['Sub'] = alldf['Sub'].astype('category')
alldf['LID_area'] = alldf['Bio_Area'] + alldf['Pav_Area']
alldf['LID_ratio'] = alldf['LID_area']/alldf['Area']
alldf['Impervious'] = alldf['Impervious']/100
# groupby Subcatchment name, rainfall duration, and periond 
# by take mean of data
gdf = alldf.groupby(['Sub','duration','period'], as_index=False).mean()
groupSub = alldf.groupby('Sub', as_index=False).mean()


#%%
import seaborn as sns
# setting styles and figure
fig ,ax= plt.subplots(figsize=(9, 7.5))
sns.set_style("white")
sns.set_context("paper", font_scale=1.65)

# plot box of LID ration, and point of mean and impervious ratio
sns.boxplot(x='Sub', y='LID_ratio',data=gdf, fliersize=0, color='w')
sns.stripplot(x='Sub',y='Impervious',data=groupSub, ax=ax,
size=8, label='impervious ratio', color='g')
sns.stripplot(x='Sub',y='LID_ratio',data=groupSub, marker='D', ax=ax,
size=8, label='mean of LID ratio', color='b')

# only show one legend of second and third plots
handles, labels = ax.get_legend_handles_labels()
ax.legend([handles[0],handles[30]],[labels[0],labels[30]], loc=1)

# customizing x, y axes 
plt.xlabel('Subcatchment')
plt.ylabel('LID ratio $(\%)$')
plt.xticks(rotation='45')
plt.title('Distribution of LID ratio')
plt.axis([-1,30,0,1.0])
# plt.show()
plt.savefig('../../New/Distribution of LID ratio.jpg')
