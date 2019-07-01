import multiprocessing as mp
import subprocess

import numpy as np
import os
import pandas as pd
from tqdm import tqdm_notebook


def drop_duplicate_cols(df):
    """Drop duplicate column names from a DataFrame, keeping the first."""
    seen = set()
    renamer = {}
    cols = df.columns.tolist()
    for i, c in enumerate(df.columns):
        if c in seen:
            renamer[i] = c + '_dup'
            cols[i] = renamer[i]
        else:
            seen.add(c)
    df.columns = cols
    df = df.drop(renamer.values(), 1)
    return df

def drop_zero_variance_cols(df):
    keep_col_mask = df.apply(lambda x: x.nunique()) > 1
    return df.loc[:, keep_col_mask]


def make_yhat_softmax_with_transform(df, grouper='right_id', agg_col='yhat'):
    log_yhat = np.exp(df[agg_col])
    sum_grp_yhat = df.groupby(grouper).log_yhat.transform('sum')
    return log_yhat / sum_grp_yhat


def list_tables(cursor):
    """Convenience method to test state of class at different points in lifetime."""
    cursor.execute(''' SELECT name FROM sqlite_master  ''')
    return cursor.fetchall()


def run_query(sqlite_manager, query):
    with sqlite_manager.connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        items = cursor.fetchall()
    return items


def add_right_df_blocked_col(right_df, blk_df):
    if isinstance(blk_df, pd.DataFrame):
        blocked_rids = set(blk_df.right_id.unique())
    elif isinstance(blk_df, set):  # take sets for convenience
        blocked_rids = blk_df

    if 'blocked' in right_df.columns:
        print('Old blocked mean {:.2f}'.format(right_df['blocked'].mean()))
    right_df['blocked'] = [x in blocked_rids for x in tqdm_notebook(right_df['id'].values)]
    print('New blocked mean {:.2f}'.format(right_df['blocked'].mean()))


def inspector(blk_df, left_df, right_df, mi_id_col='companyid'):
    return blk_df.merge(right_df, left_on='right_id', right_on='id',
                        suffixes=('_blk', '_right')).merge(
        left_df, left_on='left_id', right_on=mi_id_col, suffixes=('_right', '_left'))


def get_git_rev(root='.'):
    '''try to return the current git rev, or None if not a git branch'''

    git_dir = os.path.join(root, '.git')
    if not os.path.exists(git_dir):
        print('found no .git at {}'.format(git_dir))
        return None

    # copy os.environ to avoid setting GIT_DIR for future subprocesses
    env = dict(os.environ)
    env['GIT_DIR'] = git_dir

    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD'], env=env).strip()
    except subprocess.CalledProcessError:
        return None


def get_cpus_to_use():
    '''return the number of CPUs to use for multiprocessing'''
    return max(mp.cpu_count() - 1, 0)


def assign_id_cols(df, index_pairs) -> None:
    """Assign left_id and right_id columns from index pairs to df. Works in place."""
    if df.shape[0] != len(index_pairs):
        raise ValueError('df has {} rows but only received {} pairs'.format(
            df.shape[0], len(index_pairs)
        ))
    df['left_id'] = [x[0] for x in index_pairs]
    df['right_id'] = [x[1] for x in index_pairs]
