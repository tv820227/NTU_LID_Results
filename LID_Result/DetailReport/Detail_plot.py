
def peaktime(dat,d,p):

    ''' function of find peak time from one rainfall
        DataFrame data as data
        duration as d
        period as p
    '''
    import pandas as pd
    import numpy as np
    # create a filter to get total_inflow under specific duration, period
    filter0 = ((dat['duration'] == d) & 
    (dat['period'] == p) & 
    (dat['property'] =='total_inflow'))
    # pick needed data 
    pick = dat[filter0] # pick data frame
    pick_v = pick['value'].max() # pick peak value
    pick = pick[pick['value'] == pick_v] # pick the row which have peak value 
    pick_t = float(pick['time(hr)'].values[0]) # the time which have peak value
    return pick_t, pick_v

def detail_plot(dat, d, mode):
    ''' plot the distribution under different periods 
        DataFrame data as data
        duration as d
    '''
    import seaborn as sns
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    p_order = ['2year','5year' ,'10year' ,'25year' ,'50year' ,'100year']
    pickdf = dat[dat['duration'] == d]
    xmax = {'1hr':1.2, '2hr':2.4, '3hr':3.6, '6hr':7.2, '9hr':10.8, '12hr':14.4}
    ymax = {'1hr':1400, '2hr':1000, '3hr':800, '6hr':600, '9hr':500, '12hr':500}
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
    g = (g.map(sns.lineplot,'time(hr)', 'value')).set(xlim=(0, xmax[d]), ylim=(0, ymax[d]))
    for i in range(6):
        peak_time, peak_value = peaktime(dat, d, p_order[i])
        # given the auxilary lines
        g.axes[i].axhline(y=150+peak_value/20, color='b', label='surface capacity', linestyle='--',linewidth=1)
        g.axes[i].axhline(y=450, color='k', label='drain pipe', linestyle='--',linewidth=1)
        g.axes[i].axvline(x=peak_time, color='r', label='peak', linestyle='--',linewidth=1)

    # customizing setting
    h, l = g.axes[0].get_legend_handles_labels()
    g.add_legend(handles=h,labels=l, loc='right')
    g.set_ylabels('value (mm/hr, mm)')
    g.set_xlabels('time (hr)')
    # plt.show()
    plt.savefig('D:/梁崇淵/論文/Result/New/Detail/%s/%s.jpg'%(mode,d),
    bbox_inches='tight')


