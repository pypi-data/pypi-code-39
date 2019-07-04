from random import shuffle
import pandas as pd

def train_val_split_(dfs, text_col, target_col):
    train = []
    val = []
    targets = dfs[target_col].unique()
    for target in targets:
        sents = dfs[dfs[target_col] == target][text_col].tolist()
        shuffle(sents)

        temp = [(sent, target) for sent in sents]
        n = len(temp)
        k = int(0.8 *n)

        train.extend(temp[:k])
        val.extend(temp[k:])
    return train, val

def train_val_split(df, text_col, target_col):
    train, val = train_val_split_(df, text_col, target_col)
    train_df = pd.DataFrame(train, columns=['text', 'labels'])
    val_df = pd.DataFrame(val, columns=['text', 'labels'])

    return train_df, val_df


if __name__ == '__main__':
    path = '/Users/rajamohanreddybollavaram/Documents/Youplus/Projects/News_Classification/Notebooks/tt.csv'
    df = pd.read_csv(path)
    t_df, v_df = train_val_split(df, text_col='Article_clean', target_col='NewsType')

    print(t_df['labels'].value_counts())
    print(v_df['labels'].value_counts())