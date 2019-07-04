from chitti.nlp.pretrained_vectors import download_pretrained_vectors_
from chitti.nlp.clean_text import stem_words, lemmatize_words, remove_punctuation, remove_stopwords, space_punctuation

def test_download_pretrained_vectors_():
    download_pretrained_vectors_('GloVe.6B.50d')


def test_stem_words():
    print()
    print('Testing Stem Words')
    text = 'i am running'
    print(stem_words(text))

def test_lemmatize_words():
    print()
    print('Testing Lemmatize Words')
    text = 'i am running'
    print(lemmatize_words(text))

def test_remove_punctuation():
    print()
    print('Testing remove punctuation')
    text = 'i,am.loving.you    ..... ,,, !!! ?? ?> >> '
    print(remove_punctuation(text))

def test_remove_stopwords():
    print()
    print('Testing remove stopwords')
    text = ' and i love you to from'
    print(remove_stopwords(text))


def test_space_punctuation():
    print()
    print('Testing Space punctuation')
    text = 'i.love,,,)(;; ;; ".you'
    print(space_punctuation(text))

if __name__ == '__main__':
    # test_lemmatize_words()
    test_stem_words()
    test_remove_punctuation()
    test_remove_stopwords()
    test_space_punctuation()
    # test_download_pretrained_vectors_()