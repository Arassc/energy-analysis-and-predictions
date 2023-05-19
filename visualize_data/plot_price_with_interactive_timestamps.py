"""
Plot companies stocks interactivelly selecting timestamp/date
"""
import plotly.express as px
#Creating interactive plots for the three timeframes.

def plot_price_with_interactive_timestamps(df, column_index_x_axis,
                                      column_list_y_axis, fig_title, y_axis_label):
    """
    Args:\n
    - df: dataframe\n
    - column_index_x_axis = df.index\n
    -  column_list_y_axis = df.columns. This is always the date \n
    - fig_title: string with figure title\n
    - y_axis_label: string wiht label for Y axis\n

    Retunrs:\n
    Interactive plot where one can select x data per month, 6 months o year\n
    and also from a particular range
    """
    #Entering a sliding scale to zoom into the plots.
    fig = px.line(df, x=column_index_x_axis, y=column_list_y_axis, title=fig_title)

    fig.update_layout(yaxis_title=y_axis_label,
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label='1m',
                        step='month',
                        stepmode='backward'),
                    dict(count=6,
                        label='6m',
                        step='month',
                        stepmode='backward'),
                    dict(count=1,
                        label='1y',
                        step='year',
                        stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type='date'
        )
    )#Necessary to also zoom into the y-axis.
    fig.update_yaxes(fixedrange=False)#Actually plotting the data.
    fig.show()
    #plt.savefig(filename)
