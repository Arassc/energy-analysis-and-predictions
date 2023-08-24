import numpy as np
import pandas as pd
import math
from typing import Tuple
from energyanalysis.preprocess_data.scale_data import scale_data


def get_train_test_split(df: pd.DataFrame,
                     train_test_ratio: float,
                     train_test_sequence: int) -> Tuple[pd.DataFrame]:
    '''
    Returns a train dataframe and a test dataframe (fold_train, fold_test)
    from which one can sample (X,y) sequences.
    df_train should contain all the timesteps until round(train_test_ratio * len(fold))
    '''
    train_size = round(df.shape[0]*train_test_ratio)
    fold_train = df.iloc[0:train_size]
    fold_test = df.iloc[train_size-train_test_sequence:]
    len_train = round(df.shape[0]*train_test_ratio)
    len_test = df.shape[0] - len_train + train_test_sequence
    print(f'length train data {len_train}')
    print(f'length test data {len_test}')
    return fold_train, fold_test

def get_X_y_strides(df: pd.DataFrame,
                    input_length_folds: int,
                    output_length: int,
                    sequence_stride: int,
                    target: str):

    """slides through a Time Series dataframe to create sequences of equal
            * `input_length` for X,
            * `output_length` for y,
        using a temporal gap `sequence_stride` between each sequence

        Args:
            fold (pd.DataFrame): One single fold dataframe
            input_length (int): Length of each X_i
            output_length (int): Length of each y_i
            sequence_stride (int): How many timesteps to take before taking the next X_i

        Returns:
            Tuple[np.array]: A tuple of numpy arrays (X, y)
    """
    i = 0
    X = []
    y = []
    while i <= (df.shape[0] - input_length_folds - output_length):
        #print(f'start index {i}')
        X_i = df.iloc[i : i + input_length_folds, :]
        y_i = df.iloc[i + input_length_folds : i + input_length_folds + output_length][target]
        X.append(X_i)
        y.append(y_i)
        i = i + sequence_stride
        #print(f'end index = {i + fold_length}')

    return np.array(X), np.array(y)


def get_scaled_X_y_train_and_test_data(df:pd.DataFrame,
                                train_test_ratio: float,
                                train_test_sequence: int,
                                fold_length_ratio: float,
                                fold_sequence: int,
                                output_length: int,
                                target: str) -> Tuple:

    # split train and test data
    (df_train, df_test) = get_train_test_split(df, train_test_ratio, train_test_sequence)

    # scale data
    scaler = scale_data(df_train,-1,1)
    df_train_scaled = scaler.transform(df_train)
    df_test_scaled = scaler.transform(df_test)

    # transforme scale data nump into a Dataframe
    df_train_scaled = pd.DataFrame(df_train_scaled)
    df_train_scaled.columns = [target]
    df_test_scaled = pd.DataFrame(df_test_scaled)
    df_test_scaled.columns = [target]

    # get folds length and the number of created folds
    input_length_folds = round((df_test_scaled.shape[0]-output_length)*fold_length_ratio)
    print('folds length =', input_length_folds)

    # get X and y strides
    (X_train, y_train) = get_X_y_strides(df_train_scaled, input_length_folds, output_length, fold_sequence, target)
    (X_test, y_test) = get_X_y_strides(df_test_scaled, input_length_folds, output_length, fold_sequence, target)
    return X_train, y_train, X_test, y_test, scaler
