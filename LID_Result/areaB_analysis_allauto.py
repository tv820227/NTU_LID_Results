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
path = 'C:\\ChungYuan\\Chung-Yuan\\Publish\\Result\\OptimalResult\\halfBillion\\Picked'
os.chdir(path)

#%%
# --------------------
# get data
# --------------------
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
# --------------------
# modify DataFrame
# --------------------
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
# groupSub.to_csv('../groupbymean.csv', sep=',')

#%%
# ----------------------------------------
# plot LID distruibution 
# ----------------------------------------
from matplotlib.lines import Line2D
import seaborn as sns
# setting styles and figure
plt.clf()
sns.set_style("white")
sns.set_context("paper", font_scale=1.6)
fig ,ax= plt.subplots(figsize=(9, 7.5))


# plot box of LID ratio, and point of mean and impervious ratio
sns.boxplot(x='Sub', y='LID_ratio',data=gdf, fliersize=0, 
color='w',showmeans=True, 
meanprops={'marker':'D', 'markerfacecolor':'blue', 'markersize':'8'})
sns.stripplot(x='Sub',y='Impervious',data=groupSub, ax=ax,
size=8, label='impervious ratio', color='g')
# sns.stripplot(x='Sub',y='LID_ratio',data=groupSub, marker='D', ax=ax,
# size=8, label='mean of LID ratio', color='b')

# only show one legend of second and third plots
h = [Line2D([0],[0],marker='D',color='b',markersize=6, linewidth=0),
Line2D([0],[0],marker='o',color='g',markersize=6, linewidth=0)]
l = ['mean of LID ratio', 'impervious ratio']
ax.legend(h,l, loc=1)
# ax.legend([handles[0],handles[30]],[labels[0],labels[30]], loc=1)

# customizing x, y axes 
plt.xlabel('Subcatchment')
plt.ylabel('LID ratio $(\%)$')
plt.xticks(rotation='45')
plt.title('Distribution of LID ratio (50M)')
plt.axis([-1,30,0,1.0])

# plt.show()
plt.savefig('../../../New/Distribution of LID/Distribution of LID ratio(50M).jpg')


# %%
# --------------------------------------------------
# plot the distribution under different durations
# --------------------------------------------------
# from matplotlib.markers import markers
d_order = ['1hr', '2hr', '3hr', '6hr', '9hr', '12hr']
# setting styles and figure
plt.clf()
sns.set_style("white")
sns.set_context("paper", font_scale=2)

# plot box of LID ratio, and point of mean and impervious ratio
g = sns.catplot(x='Sub', y='LID_ratio', kind='box',
col='duration', col_order=d_order, col_wrap=2,
data=gdf, fliersize=0, color='w',showmeans=True, meanline=False,
meanprops={'marker':'D', 'markerfacecolor':'blue', 'markersize':'6',
'label':'mean of LID ratio'},size=5, aspect=1.25,legend_out=False)
g.map(sns.stripplot, x='Sub',y='Impervious',data=groupSub,
size=6, color='g', label='impervious ratio')

# customizing x, y axes 
g.set_xticklabels(rotation=90)
g.set_xlabels('Subcatchment')
g.set_ylabels('LID ratio $(\%)$')
# g.set_xlim([-1,30])
# g.set_ylim([0,0.7])
# create handles and labels for legend
h = [Line2D([0],[0],marker='D',color='b',markersize=6, linewidth=0),
Line2D([0],[0],marker='o',color='g',markersize=6, linewidth=0)]
l = ['mean', 'impervious']
g.add_legend(handles=h, labels=l)

# add legend in axes[1] (row 0 column 1) figure
# with anchor on the upper right
# g.axes[1].legend(handles, labels, bbox_to_anchor=(1.2,1.2,0,0))

# plt.show()
plt.savefig('../../../New/Distribution of LID/Distribution of LID ratio (duration, 50M).jpg',
bbox_inches='tight')

#%%
# --------------------------------------------------
# plot the distribution under different periods 
# --------------------------------------------------
p_order = ['2year','5year' ,'10year' ,'25year' ,'50year' ,'100year']
# setting styles and figure
plt.clf()
sns.set_style("white")
sns.set_context("paper", font_scale=2)

# plot box of LID ratio, and point of mean and impervious ratio
g = sns.factorplot(x='Sub', y='LID_ratio', kind='box',
col='period', col_order=p_order, col_wrap=2,
data=gdf, fliersize=0, color='w',showmeans=True, meanline=False,
meanprops={'marker':'D', 'markerfacecolor':'blue', 'markersize':'6',
'label':'mean of LID ratio'},size=5, aspect=1.25,legend_out=False)
g.map(sns.stripplot, x='Sub',y='Impervious',data=groupSub,
size=6, label='impervious ratio', color='g')

# customizing x, y axes 
g.set_xticklabels(rotation=90)
g.set_xlabels('Subcatchment')
g.set_ylabels('LID ratio $(\%)$')
# g.set_xlim([-1,30])
# g.set_ylim([0,0.7])
# create handles and labels for legend
h = [Line2D([0],[0],marker='D',color='b',markersize=6, linewidth=0),
Line2D([0],[0],marker='o',color='g',markersize=6, linewidth=0)]
l = ['mean of LID ratio', 'impervious ratio']
# add legend in axes[0] (row 0 column 0) figure
# with location on the upper left
g.axes[0].legend(handles=h, labels=l, loc='upper left')
# plt.show()
plt.savefig('../../../New/Distribution of LID/Distribution of LID ratio (period, 50M).jpg',
bbox_inches='tight')