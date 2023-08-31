#%%
import pathlib

path = pathlib.Path('src')

path = path / 'data' / 'url_data' / '2019-01-01_to_2019-01-30_planning_tender.json'

import pandas

df = pandas.read_json(path)
import json

# Flatten the lists in the 'releases' column into a single list of dictionaries
all_dicts = [item for sublist in df['releases'] for item in sublist]

# Convert this list of dictionaries into a new DataFrame
new_df = pandas.DataFrame(all_dicts)

new_df.head()