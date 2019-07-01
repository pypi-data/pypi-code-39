import os
import click
import pandas as pd
import subprocess
import random
WHITMORE = 'Samantha Whitmore'
MIKEY = 'Mikey Shulman'
aliases = {'sam_shleifer': 'sshleifer', 'sjwhitmore': WHITMORE,
           'matthewwillian': 'Matthew Willian', 'Sam_Whitmore': WHITMORE,
           'mikeyshulman': MIKEY}
# 'vadymbarda'
NICE_THINGS = ['How does it feel!?', 'Give a speech!']
REPO_NAME = 'zentreefish'

Z_PATH = '/Users/shleifer/k2/zentreefish'
KL_PATH = '~/k2/kenshp-learn'


FREUNDS = ['Harrison', 'Yurtsev', 'sshleifer', 'Shulman', 'Kucsko', 'Barda', 'Anthony Liu']

def save_history(repo_path, save_path='commit_history_ztf.mp'):
    # Unused
    from gitpandas import Repository
    repo = Repository(working_dir=repo_path, verbose=True)
    ch = repo.commit_history()
    ch.to_msgpack(save_path)


def get_df():
    cmd = 'git shortlog HEAD -s -n'
    retcode = subprocess.check_output(cmd.split()).decode()
    df = pd.DataFrame([row.strip().split('\t') for row in retcode.split('\n')],
                      columns=['n_commits', 'author']).iloc[:-1]
    df['n_commits'] = df['n_commits'].astype(int)
    for k, v in aliases.items():
        df['author'] = df.author.replace(k, v)
    return df.groupby('author')[['n_commits']].sum()


def _filter(df, milestone_mod):
    return df[df.n_commits % milestone_mod == 0]


def print_milestones(df, milestone_mod=100):
    yay = _filter(df, milestone_mod)
    if yay.empty:
        print('No Milestones :(')
        return []
    else:
        return print_out(yay)


def print_out(yay):
    messages = []
    for k, v in yay.items():
        nice_thing = random.choice(NICE_THINGS)
        messages.append(
            'Congratulations {} on {} commit number {}! {}'.format(k, REPO_NAME, v, nice_thing))
    return messages


def nearby(df, below=3):
    df = df[df['n_commits'] > 90].assign(mod=lambda x: x.n_commits % 100)
    above = 100 - below
    return df[(df['mod'] < below) | (df['mod'] > above)].set_index('author')[['n_commits']]

def blind_descending_sort(data):
    '''Sorts dataframe by first column, without knowing its name.
    Ideal after multi_unstack, and other notebook stuff.
    Args:
        data: (pd.Series or pd.DataFrame)
    '''
    if isinstance(data, pd.Series):
        return data.sort_values(ascending=False)
    return data.sort_values(data.columns[0], ascending=False)

@click.command()
@click.option('--dir', default='.')
@click.option('--mod', default=100, help='what mod is a milestone')
@click.option('--author', default=None, help='Show stats for an author')
def cli(dir, mod, author):
    os.chdir(dir)
    stats_df = get_df()

    if author == 'friends':
        print(pd.concat([stats_df[stats_df.index.str.contains(friend)] for friend in FREUNDS]).pipe(blind_descending_sort))
        return
    elif author == 'lb':
        print(stats_df.pipe(blind_descending_sort).head(10))
        return
    if author is not None:
        print(stats_df[stats_df.index.str.lower().str.contains(author)])
        return



    print('\n'.join(print_milestones(stats_df.reset_index(), milestone_mod=mod)))
    print('Near Milestones:')
    print(nearby(stats_df.reset_index()))




if __name__ == '__main__':
    cli()
