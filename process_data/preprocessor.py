
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def scale_data(df_train:pd.DataFrame)-> MinMaxScaler:
    minmax_scaler = MinMaxScaler(feature_range = (0,1))
    minmax_scaler.fit(df_train)

    return minmax_scaler
