import plotly as py
import plotly.graph_objs as go
import os
import pandas as pd
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, Title, HoverTool
from bokeh.palettes import Magma256
from bokeh.plotting import figure

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
data_dir = os.path.join(parent_dir, 'data')

produce_data = os.path.join(data_dir, 'produce_data.csv')
produce_color = '#FF009C'