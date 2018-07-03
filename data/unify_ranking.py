import os
import pandas as pd

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)

files_dir = os.path.join(parent_dir, "personal_info")

produce_data = 'produce_data.csv'
# personal_data_f = os.path.join(files_dir, 'personal_data.csv')
ranking_num = '3'
ranking_data_f = os.path.join(files_dir, 'ranking_data_{}.csv'.format(ranking_num))

# pdf = pd.read_csv(personal_data_f)
pdf = pd.read_csv(produce_data)
rdf = pd.read_csv(ranking_data_f)
rdf.rename(columns={'name': 'name_kor'}, inplace=True)

df = pd.merge(pdf, rdf, how='left', on=['name_kor'])
df.rename(columns={'rank_name': 'rank{}_num'.format(ranking_num)}, inplace=True)

df.to_csv('produce_data.csv', index=False)