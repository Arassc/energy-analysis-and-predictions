
import plotly.graph_objects as go

def plot_all_seasonal_data_for_one_energy(seasonal_dict:dict, energy:str):
    fig = go.Figure()
    for keys, values in seasonal_dict.items():

        target = energy + ' [MWh]'
        fig.add_trace(go.Scatter(x=values['Timestamp'], y=values['Photovoltaik [MWh]'],
                                    name=keys)) # line_color='rgba(18,85,194,082)' black

        fig.update_layout(
            title=go.layout.Title(text= target + ' for every season'),
            xaxis_title='Timestamp',
            yaxis_title='MWh')
    fig.show()
