import pandas as pd
import numpy as np

def correct_values(df):
    df['NO2_total'] = df['NO2_total'].clip(lower=0)
    df['NO2_trop'] = df['NO2_trop'].clip(lower=0)
    return df

def create_lag(df, num_lags):
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, infer_datetime_format=True)  # Infer date format and use dayfirst if needed
    df['day'] = df['Date'].dt.day
    df['dayofweek'] = df['Date'].dt.dayofweek
    df['week'] = df['Date'].dt.isocalendar().week
    df['weekofyear'] = df['Date'].dt.isocalendar().week
    df['month'] = df['Date'].dt.month
    df['monthofyear'] = df['Date'].dt.month
    df['year'] = df['Date'].dt.year
    df['dayofyear'] = df['Date'].dt.dayofyear
    df['quarter'] = df['Date'].dt.quarter
    df.set_index('Date', inplace=True)

    df.sort_values(by=['ID', 'Date'], inplace=True)
    
    # Create lag columns using pd.concat to avoid fragmentation
    lag_dfs = [df]
    for i in range(1, num_lags + 1):
        lag_df = df.groupby('ID')['GT_NO2'].shift(i).rename(f'lag{i}')
        lag_dfs.append(lag_df)
    
    df = pd.concat(lag_dfs, axis=1)
    
    return df

def full_df(df):
    df = df.copy().reset_index()
    df = df.drop(['ID', 'ID_Zindi', 'Date', 'NO2_trop'],axis=1)
    return df