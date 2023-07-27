from src.vector_store import vector_store
from src.embellish import embellish
df = vector_store.get_main_df()

# print(df.columns)

df = embellish.embellish_dataframe(df.sample(n=3))

for i, row in df.iterrows():
    # print(df['title'])
    print(row['Description'])
    print(row['unforseen_costs'])
    print('-' * 50)