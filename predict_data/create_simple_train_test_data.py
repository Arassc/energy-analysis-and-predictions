
import pandas as pd
import numpy as np
from process_data.preprocessor import scale_data
from typing import Tuple

def split_df_in_train_test(df: pd.DataFrame, split_ratio, memory_ratio)-> Tuple:
    len_train = round(df.shape[0]*split_ratio)
    memory_sequence = round(df.shape[0]*memory_ratio)
    df_train = df.iloc[0:len_train]
    df_test = df.iloc[len_train-memory_sequence :]
    return df_train, df_test

def get_simple_X_y_strides(df: pd.DataFrame, stride_length:int, target: str)-> Tuple:
    X = []
    y = []
    for i in range(df.shape[0]-stride_length):
        X.append(df.iloc[i:i+stride_length])
        y.append(df.iloc[i+stride_length][[target]])

    return np.asanyarray(X), np.asanyarray(y)

def get_X_y_scaled_and_splited(df: pd.DataFrame,
                               split_ratio: float,
                               memory_split_ratio: float,
                               stride_ratio: float,
                               target: str,
                               scale_range_min : float ,
                               scale_range_max: float
                               ) -> Tuple:
    cols = df.columns
    #split data
    (df_train, df_test) = split_df_in_train_test(df, split_ratio, memory_split_ratio)

    #scale data
    scaler = scale_data(df_train, scale_range_min , scale_range_max)

    train_scaled = scaler.transform(df_train)
    test_scaled = scaler.transform(df_test)

    # transform scaled arrays into dataframes
    df_train_scaled = pd.DataFrame(train_scaled)
    df_train_scaled.columns = df.columns
    df_test_scaled = pd.DataFrame(test_scaled)
    df_test_scaled.columns = df.columns

    stride_length = round(df_test_scaled.shape[0]*stride_ratio)
    X_train,y_train = get_simple_X_y_strides(df_train_scaled, stride_length, target)
    X_test,y_test = get_simple_X_y_strides(df_test_scaled, stride_length, target)

    return X_train, y_train, X_test, y_test, scaler
