import  numpy as np
import pickle
import os
from os.path import join


from chitti.nlp.download_pretrained_vectors import download
def load_matrix(EMBEDDING_FILE):

    def get_coefs(word, *arr):
        return word, np.asarray(arr, dtype='float32')

    embeddings_index = dict(get_coefs(*o.split(" ")) for o in open(EMBEDDING_FILE, encoding='utf-8'))

    return embeddings_index

def load_glove(embeddings_index, word_index):
    all_embs = np.stack(list(embeddings_index.values()))
    emb_mean, emb_std = -0.005838499, 0.48782197
    embed_size = all_embs.shape[1]

    nb_words = len(word_index)
    embedding_matrix = np.random.normal(emb_mean, emb_std, (nb_words, embed_size))
    for word, i in word_index.items():
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None: embedding_matrix[i] = embedding_vector

    return embedding_matrix

def download_pretrained_vectors(EMBEDDING_FILE, dir = 'Pretrained_Word2Vectors'):

    embeddings_index = load_matrix(EMBEDDING_FILE)
    word_index = dict([(word, i + 2) for i, word in enumerate(embeddings_index.keys())])
    word_index['<pad>'] = 0
    word_index['<unk>'] = 1

    embedding_matrix = load_glove(embeddings_index, word_index)

    if not os.path.exists(dir):
        os.makedirs(dir)

    with open(join(dir, 'word_index.pkl'), 'wb') as f:
        pickle.dump(word_index, f)

    np.save( join(dir, 'embedding_matrix.npy') , embedding_matrix)

    message = '''
    Two Files Created !!
    word_index.pkl => it is word2index dictionary
    embedding_matrix.npy => 2D Numpy matrix of shape vocab_size, embedding_size
    
    Files Saved to Pretrained_Word2Vectors Directory !!!
    
    '''
    print(message)



def download_pretrained_vectors_(name='', dir = 'Pretrained_Word2Vectors'):
    supported_vectors = ['GloVe.6B.50d', 'GloVe.6B.100d', 'GloVe.6B.200d', 'GloVe.6B.300d', 'GloVe.42B.300d',
                         'GloVe.840B.300d', 'word2vec.GoogleNews', 'GloVe.Twitter.25d', 'GloVe.Twitter.50d', 'GloVe.Twitter.100d', 'GloVe.Twitter.200d']

    if name not in supported_vectors:
        for each in supported_vectors:
            print(each)
            return
    path = download(name=name, save_dir=dir)

    print('Files  Downloaded to {}'.format(dir))

    EMBEDDING_FILE = join(dir, name.lower()+'.txt')
    download_pretrained_vectors(EMBEDDING_FILE, dir)





if __name__ == '__main__':
    download_pretrained_vectors_('GloVe.6B.50d')
    # EMBEDDING_FILE = '/Users/rajamohanreddybollavaram/Downloads/glove.6B/glove.6B.50d.txt'
    # download_pretrained_vectors(EMBEDDING_FILE)
