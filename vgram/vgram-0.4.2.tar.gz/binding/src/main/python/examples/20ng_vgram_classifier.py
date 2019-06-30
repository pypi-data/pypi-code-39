import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.datasets import fetch_20newsgroups
from sklearn.pipeline import Pipeline, FeatureUnion
from vgram import VGram


def words():
    train, test = fetch_20newsgroups(subset='train'), fetch_20newsgroups(subset='test')

    pipeline = Pipeline([
        ("vectorizer", CountVectorizer()),
        ('tf-idf', TfidfTransformer(sublinear_tf=True)),
        ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-4, max_iter=100))
    ])
    pipeline.fit(train.data, train.target)
    print("test accuracy: ", np.mean(pipeline.predict(test.data) == test.target))
    print("train accuracy: ", np.mean(pipeline.predict(train.data) == train.target))


def vgrams():
    train, test = fetch_20newsgroups(subset='train'), fetch_20newsgroups(subset='test')

    pipeline = Pipeline([
        ("vgb", VGram(size=10000, iter_num=10)),
        ("vectorizer", CountVectorizer()),
        ('tf-idf', TfidfTransformer(sublinear_tf=True)),
        ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-4, max_iter=100))
    ])
    pipeline.fit(train.data, train.target)
    print("test accuracy: ", np.mean(pipeline.predict(test.data) == test.target))
    print("train accuracy: ", np.mean(pipeline.predict(train.data) == train.target))


def wodrs_vgrams():
    train, test = fetch_20newsgroups(subset='train'), fetch_20newsgroups(subset='test')

    pipeline = Pipeline([
        ("text_features", FeatureUnion([
            ("vgram_pipeline", Pipeline([
                ("vgram", VGram(size=15000, iter_num=3)),
                ("vgram_vectorizer", CountVectorizer())
            ])), ("words_vectorizer", CountVectorizer())])),
        ('tf-idf', TfidfTransformer(sublinear_tf=True)),
        ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-4, max_iter=100))
    ])
    pipeline.fit(train.data, train.target)
    print("test accuracy: ", np.mean(pipeline.predict(test.data) == test.target))

    print("train accuracy: ", np.mean(pipeline.predict(train.data) == train.target))


if __name__ == "__main__":
    wodrs_vgrams()
