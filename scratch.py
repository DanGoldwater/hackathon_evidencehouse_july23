import pandas

df = pandas.read_csv(
    "src/data/nhs_contract_data/NHS_early_future_opportunity_awarded_closed.csv"
)
print(df.head())
