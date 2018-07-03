import plotly as py
import plotly.graph_objs as go
import os
import pandas as pd
from utils import *

NUM_EP = '3'

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
data_dir = os.path.join(parent_dir, 'data')

produce_data = os.path.join(data_dir, 'produce_data.csv')
df = pd.read_csv(produce_data)

df.sort_values('rank3_num', inplace=True)
df_rank1 = df.sort_values('rank1_num')
df_rank2 = df.sort_values('rank2_num')

# TOP 12 CHICAS
top_12 = df.head(12)
top12_r1 = df_rank1.head(12)
top12_r2 = df_rank2.head(12)

title = 'Produce 48 TOP 12 Ranking evolution'.format(NUM_EP)

labels = list(top_12['name_rom'])
labels1 = [name for name in top12_r1['name_rom'] if name not in labels]
labels2 = [name for name in top12_r2['name_rom'] if name not in labels]
labels += labels1
labels += labels2

rank1 = [int(df[df['name_rom'] == girl]['rank1_num'].values[0]) for girl in labels]
rank2 = [int(df[df['name_rom'] == girl]['rank2_num'].values[0]) for girl in labels]
rank3 = [int(df[df['name_rom'] == girl]['rank3_num'].values[0]) for girl in labels]

colors = ['mediumvioletred', 'darkred', 'red', 'orange', 'gold', 'darkkhaki', 'green', 'darkcyan', 'dodgerblue', 'slateblue', 'black', 'brown', 'blue', 'green', 'orange', 'red', 'purple', 'pink', 'violet', 'black', 'brown', 'gray', 'teal', 'gold', 'crimson']

maxr = max(max(rank1), max(rank2), max(rank3))
yvalues = map(list, zip(rank1, rank2, rank3))
#
# #rosa produce
# ##FF009C
#

num_chicas = len(labels)
mode_size = [10]*num_chicas

line_size = [3]*num_chicas

x_data = [['<b>EP1</b>', '<b>EP2</b>', '<b>EP3</b>']]*num_chicas

y_data = yvalues

traces = []

for i in xrange(0, num_chicas):

    traces.append(go.Scatter(
        x=x_data[i],
        y=y_data[i],
        mode='lines',
        line=dict(color=colors[i], width=line_size[i]),
        connectgaps=True,
        hoverinfo='none'
    ))

    traces.append(go.Scatter(
        x=[x_data[i][0], x_data[i][1]],
        y=[y_data[i][0], y_data[i][1]],
        mode='markers',
        marker=dict(color='white', size=mode_size[i], line=dict(color='#FF009C',
                                                                width='2'))
    ))

    traces.append(go.Scatter(
        x=[x_data[i][1], x_data[i][2]],
        y=[y_data[i][1], y_data[i][2]],
        mode='markers',
        marker=dict(color='white', size=mode_size[i], line=dict(color='#FF009C',
                                                                width='2'))
    )
    )

traces.append(go.Scatter(
    x=x_data[0],
    y=[12.5]*len(x_data[0]),
    line=dict(color=produce_color, width=1, dash='dash')
))

layout = go.Layout(
    xaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        autotick=False,
        ticks='outside',
        tickcolor='rgb(204, 204, 204)',
        tickwidth=2,
        ticklen=5,
        tickfont=dict(
            family='Arial',
            size=16,
            color='rgb(82, 82, 82)',
        ),
    ),
    yaxis=dict(
        range=[maxr+1, 0],
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=False,
    ),
    autosize=True,
    margin=dict(
        autoexpand=False,
        l=100,
        r=20,
        t=110,
    ),
    showlegend=False,
)

annotations = []

# Adding labels
for y_trace, label, color in zip(y_data, labels, colors):
    # labeling the left_side of the plot
    annotations.append(dict(xref='paper', x=0.05, y=y_trace[0],
                                  xanchor='right', yanchor='middle',
                                  text="<b>"+label + ' {}</b>'.format(y_trace[0]),
                                  font=dict(family='Arial',
                                            size=16,
                                            color=color,),
                                  showarrow=False))
    # labeling the right_side of the plot
    annotations.append(dict(xref='paper', x=0.95, y=y_trace[2],
                                  xanchor='left', yanchor='middle',
                                  text='<b>{}</b>'.format(y_trace[2]),
                                  font=dict(family='Arial',
                                            size=16,
                                            color=color,),
                                  showarrow=False))
# Title
annotations.append(dict(xref='paper', yref='paper', x=0.3, y=1.05,
                              xanchor='left', yanchor='bottom',
                              text=title,
                              font=dict(family='Arial',
                                        size=30,
                                        color='#FF009C'),
                              showarrow=False))
# Source
annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                              xanchor='center', yanchor='top',
                              text='Source: PewResearch Center & ' +
                                   'Storytelling with data',
                              font=dict(family='Arial',
                                        size=12,
                                        color='rgb(150,150,150)'),
                              showarrow=False))

annotations.append(dict(x=0.2, y=12.5, showarrow=True, text='TOP 12 ends here', ay=80))

layout['annotations'] = annotations

layout['height'] = 1000
layout['width'] = 1000

fig = go.Figure(data=traces, layout=layout)
py.offline.plot(fig, filename='ranking_evol.html')