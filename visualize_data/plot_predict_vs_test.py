import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
# rgba from https://rgbacolorpicker.com/

def plot_predict_vs_test(df:pd.DataFrame,
                         y_test:np.ndarray,
                         y_pre: np.ndarray,
                         fig_title:str, scaler_used:bool):
    if scaler_used:
        y_test_df = pd.DataFrame(y_test[:,0])
    else:
        y_test_df = pd.DataFrame(y_test[:,0,0])

    y_pre_df = pd.DataFrame(y_pre[:,0])
    len_train = df.shape[0] - y_test_df.shape[0]
    df_train_plt = df[0:len_train]
    df_test_plt = df[len_train:]
    y_pre_df.index = df_test_plt.index
    y_test_df.index = df_test_plt.index
    # Z = (y_pre_df-y_test_df).abs().max()[0]
    Z = (y_pre_df-y_test_df).abs().std()[0]
    # lower = y_pre_df - 0.5*abs(y_test_df-y_pre_df)
    # upper = y_pre_df +  0.5*abs(y_test_df-y_pre_df)
    lower = y_pre_df - 0.5*Z
    upper = y_pre_df +  0.5*Z
    energy = df_train_plt.columns[0]

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df_train_plt.index, y=df_train_plt[energy],
                             line_color='rgba(0,0,0,1)',
                             name='Train data')) # black

    fig.add_trace(go.Scatter(x=y_test_df.index, y=y_test_df[0],
                             line_color='rgba(0,0,0,1)', line_dash='dash',
                             name='Test data'))

    fig.add_trace(go.Scatter(x=y_pre_df.index, y=y_pre_df[0],
                             line_color='rgba(210, 153, 26, 1)',
                             name='Predict data')) # orange

    fig.add_trace(go.Scatter(x=upper.index , y=upper[0],
                             line_color='rgba(174, 173, 172, 1)', showlegend=False
                             )) # grey

    fig.add_trace(go.Scatter(x=lower.index , y=lower[0],
                             line_color='rgba(174, 173, 172, 1)', showlegend=False
                             )) # grey

    fig.add_trace(go.Scatter(x=lower.index , y=lower[0],
                             fill='tonexty', fillcolor='rgba(174, 173, 172, 1)',
                             line_color='rgba(174, 173, 172, 1)', name='Confidence interval'
                             )) # grey


    fig.update_layout(
        title=go.layout.Title(
        text=fig_title))

    fig.show()
