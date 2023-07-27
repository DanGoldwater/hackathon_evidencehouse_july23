#%%
from src.vector_store import vector_store
from src.embellish import embellish


df = vector_store.get_main_df()
# df = df.sample(n=1000)

df['Title'] = df['Title'].fillna('')
df['Description'] = df['Description'].fillna('')
df['Additional Details'] = df['Additional Text'].fillna('')

df['text'] = df['Title'] + ' ' + df['Description'] + ' ' + df['Additional Details']

# Save the DataFrame to a CSV file
df.to_csv('src/data/Contract_Data.csv', index=False)
