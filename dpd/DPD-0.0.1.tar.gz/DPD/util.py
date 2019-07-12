import nltk
nltk.download('perluniprops')
nltk.download('nonbreaking_prefixes')
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize.toktok import ToktokTokenizer
from sklearn.cluster import KMeans

STOP_WORDS_SPANISH = ['y','e','un','una','unos','unas','la','las','les','le','lo','los',u'el','a','al','de','del','en','se','este','esto','esta','estos','estas','aquel','aquello','aquella','aquellos','aquellas','ese','eso','esa','esos','esas']
W2V_STD_PARAMS = {"min_count":5,
                  "window":5,
                  "size":300,
                  "negative":5,
                  "iter":5}
STD_CLUSTERING = KMeans
STD_CLUSTERING_PARAMS = {"n_clusters":10,
                         "n_init":30}
STD_DENDROGRAM_METHOD = "complete"
STD_DISTANCE = "cityblock"

def tokenize_text(text):
    toktok = ToktokTokenizer()
    tokenized = sent_tokenize(text,language='spanish')
    tokenized = [toktok.tokenize(t) for t in tokenized]
    tokenized = [[word.lower() for word in sentence if word.isalpha()] for sentence in tokenized]
    return tokenized

#def
