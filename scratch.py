import pandas

df = pandas.read_csv(
    "src/data/Contract_Data.csv"
)
print(df.columns)
print(df.head())
