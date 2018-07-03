from utils import *

df = pd.read_csv(produce_data)


def agencies_count(df):
    # Agencias count
    df = df.agency.value_counts()

    labels = list(df.index)
    values = list(df)

    fig = {
      "data":[
        {
          "values": values,
          "labels": labels,
          # "domain": {"x": [0, .48]},
          "name": "Agencies trainees",
          "hoverinfo":"label+percent",
          "hole": .4,
          "type": "pie",
          "textinfo": "value"
        }],
      "layout": {
            "title":"Produce 48 distribution by agencies/group",
            "legend": {'x': 0.8, 'y': 1.2}
        }
    }

    py.offline.plot(fig, filename='agencies_pie_count.html')

# Rank evaluation by agencies


def eval_byagencies(df):

    df['rank_diff_total_ep2'] = df['rank1_num'] - df['rank2_num']
    df['rank_diff_total_ep3'] = df['rank2_num'] - df['rank3_num']
    grouped = df.groupby('agency')
    df = grouped.aggregate(lambda x: list(x))

    labels = list(df.index)
    episodes = ['EP1 to EP2', 'EP2 to EP3']
    columns = ['rank_diff_total_ep2', 'rank_diff_total_ep3']
    improvements = {'agencies': labels}
    worsenings = {'agencies': labels}
    for i, el in enumerate(episodes):
        improvements[el] = [sum((1 for val in agency_values if val >= 0)) for agency_values in list(df[columns[i]])]
        worsenings[el] = [sum((-1 for val in agency_values if val < 0)) for agency_values in list(df[columns[i]])]

    output_file("agencies_ranking_improve.html")

    p = figure(y_range=labels, plot_height=650, plot_width=1000, title="Trainees ranking position evaluation by agencies",
               toolbar_location=None)

    p.hbar_stack(episodes, y='agencies', height=0.9, color=[produce_color, 	'#9300ff'], source=ColumnDataSource(improvements),
                 legend=["%s trainees whose position improved" % x for x in episodes])

    p.hbar_stack(episodes, y='agencies', height=0.9, color=['#ADD8E6', '#d8e6ad'], source=ColumnDataSource(worsenings),
                 legend=["%s trainees whose position worsened" % x for x in episodes])

    p.y_range.range_padding = 0.1
    p.ygrid.grid_line_color = None
    p.legend.location = 'top_left'
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    p.title.text_color= produce_color
    p.title.text_font = 'Arial'
    p.title.text_font_size = '16px'
    p.title.align = 'center'
    p.xaxis.visible= False

    show(p)


eval_byagencies(df)