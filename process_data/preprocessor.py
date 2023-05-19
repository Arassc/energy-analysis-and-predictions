
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def scale_data(df_train:pd.DataFrame, start_range: float, end_range:float)-> MinMaxScaler:
    minmax_scaler = MinMaxScaler(feature_range = (start_range,end_range))
    minmax_scaler.fit(df_train)

    return minmax_scaler
