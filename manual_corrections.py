import data
path = 'data/RelsB-2IMZYfNi21MGqxopj9fWx8.csv'
df = data.read_as_df(path)

df['YouTube_Title'] = [None for _ in range(len(df))]
df['YouTube_URL'] = [None for _ in range(len(df))]
data.save_df(df, path)