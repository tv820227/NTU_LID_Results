#%%
import matplotlib.pyplot as plt
import matplotlib.markers as mak
import pandas as pd
import numpy as np
import os

# define to path to reach data
path = 'D:\梁崇淵\論文\Result\OptimalResult\Result'
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
subdf = pd.read_csv('../Subcatchment.csv')
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
print(groupSub)


#%%
import seaborn as sns
# setting styles and figure
fig ,ax= plt.subplots(figsize=(9, 7.5))
sns.set_style("white")
sns.set_context("paper", font_scale=1.7)

# plot box of LID ration, and point of mean and impervious ratio
sns.boxplot(x='Sub', y='LID_ratio',data=gdf, fliersize=0, color='w')
sns.stripplot(x='Sub',y='Impervious',data=groupSub, ax=ax,
size=8, label='impervious ratio', color='g')
sns.stripplot(x='Sub',y='LID_ratio',data=groupSub, marker='D', ax=ax,
size=8, label='mean of LID ratio', color='b')

# only show one legend of second and third plots
handles, labels = ax.get_legend_handles_labels()
ax.legend([handles[0],handles[30]],[labels[0],labels[30]])

# customizing x, y axes 
plt.xlabel('Subcatchment')
plt.ylabel('LID ratio $(\%)$')
plt.xticks(rotation='45')
plt.title('Distribution of LID ratio')
plt.axis([-1,30,0,0.6])
plt.show()


# #%%
# period=[2,5,10,25,50,100]
# duration=[1,2,3,6,9,12]

# for i in range(6):
#     for j in range(6):
#         d = duration[i]
#         p = period[j]
        
#         # 計數在這樣的降雨條件下有多少的模擬輸出檔
#         num = 0
#         while (os.path.exists('C:\\Users\\user\\Desktop\\Results\\OptimalResult\\Result\\%shr_%syear-opt-%s.txt'%(str(d),str(p),str(num)))):
#             num += 1
#         if num == 0:
#             continue
            
#         # 若此降雨尚未開設資料夾，則新開一個屬於此降雨之資料夾
#         if not os.path.exists('C:\\Users\\user\\Desktop\\Results\\OptimalResult\\Figure\\%shr_%syear'%(str(d),str(p))):
#             os.makedirs('C:\\Users\\user\\Desktop\\Results\\OptimalResult\\Figure\\%shr_%syear'%(str(d),str(p)))

#         mainfunction(d,p,num)
