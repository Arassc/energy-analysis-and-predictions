import plotly.graph_objects as go
import plotly.express as px
from itertools import cycle
import pandas as pd

def plot_loop_ndarray(X_train):
    palette = cycle(px.colors.qualitative.Bold)
    fig = go.Figure()

    for sequence in range(0, 10):
            df = pd.DataFrame(X_train[sequence,:,0])
            fig.add_trace(go.Scatter(x=df.index, y=df[0],
                                marker_color=next(palette),
                                name=f'sequence = {sequence}'))
    fig.show()
