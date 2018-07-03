import os
import pandas as pd

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)

files_dir = os.path.join(parent_dir, "personal_info")

produce_data = 'produce_data.csv'
status = os.path.join(files_dir, 'status.csv')

pdf = pd.read_csv(produce_data)
sdf = pd.read_csv(status)
df = pd.merge(pdf, sdf, how='left', on=['name_rom'])

df.to_csv('produce_data.csv', index=False)