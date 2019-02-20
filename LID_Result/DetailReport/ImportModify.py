
def import_modify(file_name):
    '''function of get data of SWMM detail output'''
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

    # # for subplot we don't need to melt the dataframes
    # df = df.melt(['time(hr)','period','duration'], var_name='property',  value_name='value')
    # df['unit'] = df['property'].apply(lambda x:'mm' if x in level else 'mm/hr')
    return df
