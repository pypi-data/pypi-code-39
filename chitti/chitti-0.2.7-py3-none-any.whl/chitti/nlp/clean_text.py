
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def space_punctuation(text):
    puncts = '[!.,]'
    text = re.sub('([!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~])', r' \1 ', text)
    return text

def remove_punctuation(text):
    text = re.sub('[!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]', r' ', text)

    text = ''.join(text)
    text = re.sub(' +',' ',text)
    return text


stop_list = stopwords.words('english')


def remove_stopwords(text):
    text = text.split()
    text = [word for word in text if word not in stop_list]
    text = ' '.join(text)
    text = re.sub('\s+', ' ', text)
    return text

snow = nltk.stem.SnowballStemmer('english')
def stem_words(text):
    # Removing all the stopwords

    words = [snow.stem(word) for word in text.split()]
    return " ".join(words)


wnl = WordNetLemmatizer()
def lemmatize_words(text):

    text = [wnl.lemmatize(each, pos='v') for each in text.split()]
    return ' '.join(text)