def peaktime(dat,d,p):

    ''' function of find peak time from one rainfall
        DataFrame data as data
        duration as d
        period as p
    '''
    import pandas as pd
    import numpy as np
    pick = dat['total_inflow']
    pick_v = pick.max() # pick peak value
    pick = pick[pick == pick_v] # pick the row which have peak value 
    pick_t = pick.index.values[0] # the time which have peak value
    return pick_t, pick_v

def detail_plot(dat, d, mode):
    ''' plot the distribution under different periods 
        DataFrame data as dat
        duration as d
        In this function, we used subplot in matplotlib instead of FacetGird in seaborn to delineate figures
    '''
    import seaborn as sns
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    
    # set the range of x and y for different duration
    xmax = {'1hr':1.2, '2hr':2.4, '3hr':3.6, '6hr':7.2, '9hr':10.8, '12hr':14.4}
    ymax = {'1hr':1400, '2hr':1000, '3hr':800, '6hr':600, '9hr':500, '12hr':500}
    # create the list to store six different return period
    p_order = ['2year','5year' ,'10year' ,'25year' ,'50year' ,'100year']

    # ----------------------------------------
    # setting styles and figure
    # ----------------------------------------
    plt.clf()
    # color codes for palette
    mypal = ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd',
    '#8c564b','#e377c2','#7f7f7f','#17becf']

    # setting the subplot parameters
    hight = 3*4.5 # the total hight to subplot
    width = 14 # the total width to subplot
    fig, axes = plt.subplots(3, 2,sharey=True, sharex=True, squeeze=True, figsize=(width,hight))
    fig.subplots_adjust(wspace=0.08) # the width between to columns in subplot

    # ----------------------------------------
    # plotting under different return period
    # ----------------------------------------
    cnt = 0
    pick_duration = dat[dat['duration'] == d] # pick the dataframe with specific duration
    for i in p_order:   
        sns.set(style='whitegrid')
        sns.set_context('paper', font_scale=2)

        
        row, col = cnt//2, cnt%2 # calculate the row number and column number for subplot
        pick = pick_duration[pick_duration['period'] == i] # pick the dataframe with specific return period 

        # pick without the categories column whcih are duration and return period
        # divide variables into the volume part and the rate part
        volume = pick.iloc[:,-5:-2]
        rate = pick.iloc[:,:-5]
        # plot different types of variable with different lines
        ax = rate.plot(ax=axes[row, col], color=mypal[:6])
        ax = volume.plot(ax=axes[row, col], color=mypal[6:], dashes=[10, 2])
        # set the twin-x for the plots in the right column
        if cnt%2 == 1:
            sns.set_style("white", {'axes.grid' : False})
            ax2 = ax.twinx()
            ax2.set_ylabel('Volume (mm)')
            ax2.set_ylim(0,ymax[d])
            # modify the tick parameters
            ax2.tick_params(axis='y', which='both', direction='in', bottom=False, top=False, left=False, right=True)
            ax.tick_params(axis='y', which='both', bottom=False, top=False, left=False, right=False)
            # modify the spines
            ax2.spines['bottom'].set_color('black')
            ax2.spines['top'].set_color('black')
            ax2.spines['left'].set_color('black')
            ax2.spines['right'].set_color('black')
            ax2.xaxis.grid(False)
            ax2.yaxis.grid(False)
        else:
            ax.tick_params(axis='y', which='both', direction='in', bottom=False, top=False, left=True, right=False)
        
        ax.set_title('%s %s return period'%(i[:-4], i[-4:])) # set the title to describe return periods
        
        # find out the peak time to delineate auxiliary lines
        peak_time, peak_value = peaktime(pick, d, i)
        if mode == 'Bio':
            # plot auxiliary lines for bio-retention
            ax.axhline(y=150+peak_value/20, color='b', label='surface capacity', linestyle='--',linewidth=1)
            ax.axhline(y=250, color='k', label='drain pipe', linestyle='--',linewidth=1)
        else:
            # plot auxiliary lines for permeable pavement
            ax.axhline(y=peak_value/20, color='b', label='surface capacity', linestyle='--',linewidth=1)
            ax.axhline(y=200, color='k', label='drain pipe', linestyle='--',linewidth=1)
        # plot auxiliary lines for peak time
        ax.axvline(x=peak_time, color='r', label='peak', linestyle='--',linewidth=1)
        
        # legend and label costomer modifing
        ax.legend().remove()
        ax.set_ylabel('Flowrate (mm/hr)')
        ax.set_xlabel('Time (hr)')
        ax.set_xlim(0,xmax[d])
        ax.set_ylim(0,ymax[d])
        ax.xaxis.grid(False)
        ax.yaxis.grid(False)
        cnt += 1

    # show the legend under costomer setting
    h, l = ax.get_legend_handles_labels()
    l = ['Total inflow (mm/hr)', 'Surface infiltration (mm/hr)', 'Pavement percolation (mm/hr)',
        'Soil percolation (mm/hr)', 'Surface Outflow (mm/hr)', 'Drain outflow (mm/hr)', 'Surface level (mm)',
        'Soil level (mm)', 'Storage level (mm)', 'Surface capacity (mm)', 'Drain pipe level (mm)']
    axes[2][0].legend(h[:6], l[:6], loc = (-0.15, -0.55), ncol=2, fontsize=14)
    axes[2][1].legend(h[6:-1], l[6:], loc = (0, -0.55), ncol=2, fontsize=14)

    # save figures
    plt.savefig('C:\\Chung-Yuan\\Publish\\Result\\New\\Detail\\%s\\%s.jpg'%(mode,d),bbox_inches='tight')

