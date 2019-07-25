# External libraries
from numpy import arange, sort, load, linalg, vstack
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
from pandas import DataFrame

# Standard library
from typing import Tuple

# Local libraries
from lib.getDataDirPath import getDataDirPath
from lib.enums import Reduce, ClosestSearchMethod as Method
from lib.closestSynonyms import closest_synonyms


# def getIntervalList(start: int, end: int, interval: int) -> List[int]:
#     items = list(arange(start, end, interval))

#     endIsNotIcluded = items[-1] != end
#     if endIsNotIcluded:
#         items.append(end)

#     return list(sort(items))


def procrustes_align(base_embed, other_embed):
    # """
    #    Align other embedding to base embeddings via Procrustes.
    #    Returns best distance-preserving aligned version of other_embed
    #    NOTE: Assumes indices are aligned
    # """
    basevecs = base_embed - base_embed.mean(0)
    othervecs = other_embed - other_embed.mean(0)
    m = othervecs.T.dot(basevecs)
    u, _, v = linalg.svd(m)
    ortho = u.dot(v)
    fixedvecs = othervecs.dot(ortho)
    # fixedvecs = preprocessing.normalize(fixedvecs)
    return fixedvecs


# TODO: 
# * Consecutive decades don't work
# * Breaks if yearInterval is larger than the difference between end and start year
# * Do years need to be a multiple of 10? ie the start of each decade
# * Clean up variable input using objects?
def plot_semantic_drift_path(
    words: Tuple[str],  # TODO: Should take only one word i think
    startYear: int = 1850,
    endYear: int = 2000,
    yearInterval: int = 40,
    k: int = 20,
    components: int = 2,
    reduce: Reduce = Reduce.PCA,
    method: Method = Method.SVD,  # default
    mirror: bool = False,
    align: bool = True,
    size: int = 23,
    addinBetween: bool = True
):
    '''
    Explain Hyper-Parameter
    Doesn't allow customisation:
    words:        Only the first word will be showed path
    startYear:         start year
    endYear:            end year
    interval:          if you want to show path of semantic drift,
                       interval regulate number of time points in between of starting and end year.
    k:                 number of k-nearest neighbors included for each word
    size=23:           size of fonts
    addinBetween =     True: True one wants to see a path, False if only want to visualize the two ends

    Doesn't allow customisation:
    components: FIXED parameter in PCA analysis
    reduce:     pca method. Also fixed. t-sne doesn't work well here
    method:     svd. Fixed. Alternatively one can choose word2vec trained by Hamilton 2016.
                We may provide that feature in the future
    mirror:     aestetics if one wants the image to be mirrored, so that path flows from left to right
    align=True: fixed, esepcially if one wants a historical drift.
    '''

    if words.__len__() == 0:
        raise Exception('No words in words')

    year_i = list(arange(startYear, endYear, yearInterval))
    if year_i[-1] != endYear:
        year_i.append(endYear)

    year_i = sort(year_i)

    # startYear = year_i[0]
    # endYear = year_i[-1]
    year_continues = year_i[1:-1]

    dataDirPath = getDataDirPath()
    sgnsHamiltonDir = dataDirPath + '/sgns-hamilton/'
    embeddingsDir = dataDirPath + '/embeddings/'
    suffix = '_svd_PPMI.npy'

    # 2. get k-nearest neighbor words as contextW, prepare their colour
    oldSynonyms, newSynonyms = [], []
    for word in words:
        startYearClosestSynonyms = closest_synonyms(
            (word,), startYear, k, method)
        endYearClosestSynonyms = closest_synonyms((word,), endYear, k, method)

        startYearClosestSynonyms_words = startYearClosestSynonyms[1][0][1:]
        endYearClosestSynonyms_words = endYearClosestSynonyms[1][0][1:]

        oldSynonyms = oldSynonyms + startYearClosestSynonyms_words
        newSynonyms = newSynonyms + endYearClosestSynonyms_words

    contextWords = set(oldSynonyms + newSynonyms)

    # remove target words from context words
    contextWords = [w for w in contextWords if w not in words]

    color_w = ['blue']*len(contextWords)
    size_w = [20]*len(contextWords)
    alpha_w = [0.5]*len(contextWords)

    # 3. load wordembeddings based on vector. normalize svd. sgns does not need normalized.
    m = None
    m_startYear = None
    vocab = None

    if method == Method.SGNS:
        m = load(sgnsHamiltonDir + str(endYear) + '-w.npy')
        m_startYear = load(sgnsHamiltonDir + str(startYear) + '-w.npy')

        vocab = load(sgnsHamiltonDir + str(endYear) + '-vocab.pkl', allow_pickle=True)

    elif method == Method.SVD:
        m = load(embeddingsDir + str(endYear) + suffix)
        m = preprocessing.normalize(m)

        m_startYear = load(embeddingsDir + str(startYear) + suffix)
        m_startYear = preprocessing.normalize(m_startYear)

        vocab = load(dataDirPath + '/vocabulary.pkl', allow_pickle=True)

    # 4. historical alignment
    if align:
        m_startYear = procrustes_align(m, m_startYear)

    # 5. decompose target word(wordT) --> 'gay gays' --> ['gay_1900', 'gays_1900', 'gay_1800', 'gays_1800']
    targetWordIndecies = [vocab.index(w) for w in words]  # index for gay and gays
    annotatiedTargetWords = sum(
        [[w + '_' + x for w in words] for x in [str(year) for year in [endYear, startYear]]], []
    )

    compiledWords = contextWords + list(words)
    annotation = contextWords + annotatiedTargetWords

    compiledIndex = [vocab.index(word) for word in compiledWords]

    compiledM = m[compiledIndex, :]   # get modern embeddings
    compiledM_startYear = m_startYear[targetWordIndecies, :]

    compiledM = vstack([compiledM, compiledM_startYear])

    color_w = color_w + ['red']*len(annotatiedTargetWords)
    size_w = size_w + [100]*len(annotatiedTargetWords)
    alpha_w = alpha_w + [1]*len(annotatiedTargetWords)

    if addinBetween:
        primaryWord = words[0]
        betweenWordT = []

        # years = getIntervalList(startYear, endYear, yearInterval)
        # year_continues = years[1:-1]

        if method == Method.SGNS:
            for year_c in year_continues:
                m_b = load(sgnsHamiltonDir + str(endYear) + '-w.npy')
                vocab = load(sgnsHamiltonDir + str(endYear) + '-vocab.pkl', allow_picklet=True)
                if align:
                    m_b = procrustes_align(m, m_b)
                    betweenWordT.append(m_b[vocab.index(primaryWord), :])

        elif method == Method.SVD:
            for year_c in year_continues:
                m_b = load(embeddingsDir + '10-years/' + str(year_c) + suffix)
                m_b = preprocessing.normalize(m_b)
                vocab = load(dataDirPath + '/vocabulary.pkl', allow_pickle=True)
                if align:
                    m_b = procrustes_align(m, m_b)
                betweenWordT.append(m_b[vocab.index(primaryWord), :])

        betweenWordT = vstack(betweenWordT)
        annotation_between = ['' + '' + x for x in [str(year) for year in year_continues]]
        compiledM = vstack([compiledM, betweenWordT])
        annotation = annotation + annotation_between

        color_w = color_w + ['red']*len(annotation_between)
        size_w = size_w + [20]*len(annotation_between)
        alpha_w = alpha_w + [1]*len(annotation_between)

    if reduce == Reduce.PCA:
        chosen = PCA(n_components=components).fit_transform(compiledM)
    elif reduce == Reduce.TSNE:
        pca_30 = PCA(n_components=30).fit_transform(compiledM)
        chosen = TSNE(
            n_components=components,
            init='pca',
            verbose=1,
            perplexity=40,
            n_iter=500,
            learning_rate=30
        ).fit_transform(pca_30)

    if mirror:
        chosen[:, 0] = -1*chosen[:, 0]

    texts = []
    for x, y, l, alpha in zip(chosen[:, 0], chosen[:, 1], annotation, alpha_w):
        texts.append(plt.text(x, y, l, size=size, alpha=alpha))

    outputData = DataFrame({
            'alpha': alpha_w,
            'color': color_w,
            'label': annotation,
            'size': size_w,
            'xValue': chosen[:, 0],
            'yValue': chosen[:, 1]
        })

    return outputData.to_csv()  # TODO: add index=False
