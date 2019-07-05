from jsondler.json_tools import get_paths_order


def sort_pandas_df(df, json_col_name, prior_list, reverse=False, inplace=True):
    paths_order = get_paths_order(in_json=list(df[json_col_name]), prior_list=prior_list, reverse=reverse)
    if inplace:
        df = df.reindex([path[0] for path in paths_order]).reset_index(drop=True)
    else:
        return df.reindex([path[0] for path in paths_order]).reset_index(drop=True)
