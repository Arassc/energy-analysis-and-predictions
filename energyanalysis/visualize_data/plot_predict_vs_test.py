import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import math
from sklearn.metrics import mean_squared_error
from energyanalysis.utils.parameters import RESULTS

# rgba from https://rgbacolorpicker.com/

def plot_predict_vs_test(df:pd.DataFrame,
                         y_test:np.ndarray,
                         y_pre: np.ndarray,
                         fig_title:str,
                         target: str,
                         fig_name: str):

    y_test_df = pd.DataFrame(y_test[:,0])
    y_pre_df = pd.DataFrame(y_pre[:,0])
    len_train = df.shape[0] - y_test_df.shape[0]
    df_train_plt = df[0:len_train]
    df_test_plt = df[len_train:]
    y_pre_df.index = df_test_plt.index
    y_test_df.index = df_test_plt.index

    Z = math.sqrt(mean_squared_error(y_test_df, y_pre_df))
    lower = y_pre_df - 0.5*Z
    upper = y_pre_df +  0.5*Z

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df_train_plt.index, y=df_train_plt[target],
                             line_color='rgba(0,0,0,1)',
                             name='Train data')) # black


    fig.add_trace(go.Scatter(x=upper.index , y=upper[0],
                             line_color='rgba(174, 173, 172, 1)', showlegend=False
                             )) # grey

    fig.add_trace(go.Scatter(x=upper.index , y=upper[0],
                                line_color='rgba(174, 173, 172, 1)', showlegend=False,
                                fill=None
                                )) # grey

    fig.add_trace(go.Scatter(x=lower.index , y=lower[0],
                                line_color='rgba(174, 173, 172, 1)',
                                fill='tonexty', fillcolor='rgba(174, 173, 172, 1)',
                                name='Confidence interval'
                                )) # grey

    fig.add_trace(go.Scatter(x=y_test_df.index, y=y_test_df[0],
                             line_color='rgba(0,0,0,1)', line_dash='dash',
                             name='Test data')) # black dash line

    fig.add_trace(go.Scatter(x=y_pre_df.index, y=y_pre_df[0],
                             line_color='rgba(210, 153, 26, 1)',
                             name='Predict data')) # orange

    fig.update_layout(
        title=go.layout.Title(
        text=fig_title))
    fig.write_html( RESULTS + '/' + fig_name + '.html')
    fig.show()
