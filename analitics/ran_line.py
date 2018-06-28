import plotly as py
import plotly.graph_objs as go
import os
import pandas as pd

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
data_dir = os.path.join(parent_dir, 'data')

produce_data = os.path.join(data_dir, 'produce_data.csv')
df = pd.read_csv(produce_data)

df.sort_values('rank2_num', inplace=True)

# TOP 12 CHICAS
top_12 = df.head(12)

title = 'Produce 48 TOP 12 Ranking evolution'

labels = top_12['name_rom']
colors = ['mediumvioletred', 'darkred', 'red', 'orange', 'gold', 'darkkhaki', 'green', 'darkcyan', 'dodgerblue', 'slateblue', 'black', 'brown']

rank1 = list(top_12['rank1_num'])
rank2 = list(top_12['rank2_num'])
yvalues = map(list, zip(rank1, rank2))

#rosa produce
##FF009C

mode_size = [12]*12

line_size = [2]*12

x_data = [['EP1', 'EP2']]*12

y_data = yvalues

traces = []

for i in xrange(0, 12):
    traces.append(go.Scatter(
        x=x_data[i],
        y=y_data[i],
        mode='lines',
        line=dict(color=colors[i], width=line_size[i]),
        connectgaps=True,
    ))

    traces.append(go.Scatter(
        x=[x_data[i][0], x_data[i][1]],
        y=[y_data[i][0], y_data[i][1]],
        mode='markers',
        marker=dict(color='white', size=mode_size[i], line=dict(color='#FF009C',
                                                                width='2'))
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
            size=12,
            color='rgb(82, 82, 82)',
        ),
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=False,
    ),
    autosize=False,
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
                                  text=label + ' {}'.format(y_trace[0]),
                                  font=dict(family='Arial',
                                            size=16,
                                            color=colors,),
                                  showarrow=False))
    # labeling the right_side of the plot
    annotations.append(dict(xref='paper', x=0.95, y=y_trace[1],
                                  xanchor='left', yanchor='middle',
                                  text='{}%'.format(y_trace[1]),
                                  font=dict(family='Arial',
                                            size=16,
                                            color=colors,),
                                  showarrow=False))
# Title
annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                              xanchor='left', yanchor='bottom',
                              text=title,
                              font=dict(family='Arial',
                                        size=30,
                                        color='rgb(37,37,37)'),
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

layout['annotations'] = annotations

fig = go.Figure(data=traces, layout=layout)
py.offline.plot(fig, filename='news-source.html')