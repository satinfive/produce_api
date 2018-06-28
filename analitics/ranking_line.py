# import os
# import pandas as pd
# from bokeh.plotting import figure, output_file, show
# from bokeh.models.sources import ColumnDataSource
# from bokeh.models import Range1d, FactorRange
# from colors import colors
# from numpy.random import randint
#
# current_dir = os.path.dirname(__file__)
# parent_dir = os.path.dirname(current_dir)
# data_dir = os.path.join(parent_dir, 'data')
#
# produce_data = os.path.join(data_dir, 'produce_data.csv')
#
# df = pd.read_csv(produce_data)
#
# df.sort_values('rank2_num', inplace=True)
#
#
# # TOP 12 CHICAS
# top_12 = df.head(12)
#
# # xvalues = [[girl, girl] for girl in list(top_12['name_rom'])]
# xvalues = [['EP1', 'EP2']]*12
# rank1 = list(top_12['rank1_num'])
# rank2 = list(top_12['rank2_num'])
# max1 = max(rank1)
# max2 = max(rank2)
# maxr = max1 if max1 > max2 else max2
# yvalues = map(list, zip(rank1, rank2))
#
# output_file("patch.html")
# p = figure(x_range=('EP1', 'EP2'), y_range=Range1d(maxr+1, 0), plot_height=500, plot_width=1000, toolbar_location=None)
#
# # colors_lines = [colors[color].hex_format() for color in [colors.keys()[num] for num in randint(len(colors.keys()), size=12)]]
# colors_lines = ['mediumvioletred', 'darkred', 'red', 'orange', 'gold', 'darkkhaki', 'green', 'darkcyan', 'dodgerblue', 'slateblue', 'black', 'brown']
#
# data = {'xs': xvalues,
#         'ys': yvalues,
#         'labels': list(top_12['name_rom']),
#         'colors': colors_lines}
#
# source = ColumnDataSource(data)
#
# p.multi_line(xs='xs', ys='ys', legend='labels', color='colors', source=source, line_width=2)
# p.circle(['EP1']*12, rank1, size=10, fill_color="white", line_color="#ADD8E6", line_width=2)
# p.circle(['EP2']*12, rank2, size=10, fill_color="white", line_color="#FF6666", line_width=2)
#
# p.legend.location = "top_left"
# p.x_range = FactorRange(factors=['EP1', 'EP2'])
# # p.xrange.start = 'EP1'
#
# show(p)