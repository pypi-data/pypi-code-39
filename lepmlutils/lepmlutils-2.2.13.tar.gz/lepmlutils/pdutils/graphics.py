def plot_against(df, name, col):
    df.groupby(name).mean()[col].plot.bar(stacked=True, figsize=(20,10))