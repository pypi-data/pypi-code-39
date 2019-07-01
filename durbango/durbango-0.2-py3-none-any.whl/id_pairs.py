from .nb_utils import get_membership_mask


def get_id_pairs(df):
    """Helper function to get list of id pairs from dataframe."""
    return list(zip(df['left_id'], df['right_id']))


#lidrid = ['left_id', 'right_id']

def filter_to_id_pairs(train_df, id_pairs):
    id1 = get_id_pairs(train_df)
    id2 = set(id_pairs)
    mask = get_membership_mask(id1, id2)
    return train_df.loc[mask]
