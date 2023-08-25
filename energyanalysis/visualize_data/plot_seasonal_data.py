
import plotly.graph_objects as go
from energyanalysis.utils.parameters import RESULTS

def plot_all_seasonal_data_for_one_energy(seasonal_dict:dict, energy:str, fig_name:str):
    fig = go.Figure()
    for keys, values in seasonal_dict.items():

        target = energy + ' [MWh]'
        fig.add_trace(go.Scatter(x=values['Timestamp'], y=values[target],
                                    name=keys)) # line_color='rgba(18,85,194,082)' black

        fig.update_layout(
            title=go.layout.Title(text= target + ' for every season'),
            xaxis_title='Timestamp',
            yaxis_title='MWh')

    fig.write_html( RESULTS + '/' + fig_name + '.html')
    fig.show()
