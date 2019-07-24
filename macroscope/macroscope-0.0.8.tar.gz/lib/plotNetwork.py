# External libraries
from numpy import array, log, sqrt, seterr
from pandas import DataFrame
from networkx import Graph, set_node_attributes
import community

# Standard library
from heapq import nlargest
from scipy import sparse

# Local libraries
from lib.enums import NetworkMethod as Method
from lib.globals import dataDir
from lib.getPickleData import getVocab50k, getKernelYearFrequency, getSumYear
from lib.loadSparseCsr import load_sparse_csr

# https://docs.scipy.org/doc/numpy/reference/generated/numpy.seterr.html
# https://stackoverflow.com/questions/15933741/how-do-i-catch-a-numpy-warning-like-its-an-exception-not-just-for-testing
seterr(divide='ignore', invalid='ignore')


# plotNetwork_new("hello")
def plotNetwork_new(
    word: str,
    year: int = 2000,
    w_pmi: float = 0.7,
    nodeSize: int = 300,
    e_PMI: float = 0.7,
    pmi_threshold: float = 3.5,
    D: int = 5,
    cap: int = 70,
    method: Method = Method.PMI
):
    # Parameter to be put in the tool bar
    # w_pmi (0-1), nodeSize (100-500), pmi_threshold (2.5-5) , D (2-8), cap (20-150)

    # paramter:
    # year
    # w_pmi: First step: assign value to each selected words based on its relation with the target word.
    # w_pmi * PMI + (1-w_pmi) * cor
    # nodeSize: get top n (n=nodeSize) most relevant words based on w_pmi

    # pmi_threshold: Second step: remove edges if pmi is less than pmi_threshold

    # e_PMI: Third step: In the network, each nodes is re-evaluated based on its connections wih other nodes:
    # e_PMI* network_df.PMI/max(network_df.PMI) + (1-e_PMI)* network_df.co_occur/max(network_df.co_occur)

    # D: remove nodes if degree is less than D
    # cap: total number of words included in words exceed cap threshold

    # Step 1.load data
    voc_50k = getVocab50k()
    kernel_year_freq = getKernelYearFrequency()
    sum_year = getSumYear()

    fileName = dataDir + '/compiled-co-matrix/' + str(year) + '.npz'
    tempData = load_sparse_csr(fileName)

    index = voc_50k.index(word)
    front = tempData.getrow(index).toarray()
    back = tempData.getcol(index).toarray().transpose()

    combined_i = front + back

    # count of 'risk' occur with top 20,000 words
    combined_i = combined_i[0][0:50000]

    # count of occurence of top 20,000 words
    year_i_freq = kernel_year_freq[:, year-1800]
    year_i_freq = year_i_freq[0:50000]
    word_freq = year_i_freq[index]  # number of times 'risk' appears
    lexicon_size_year_i = sum_year[str(year)]  # lexicon size of the eyar

    # Step 2: get cor and PMI between each word and target word: cor(x_i, risk) and PMI (x_i, risk)
    PMI = log(
        (combined_i[:50000]/lexicon_size_year_i) /
        ((word_freq/lexicon_size_year_i) *
         (year_i_freq[:50000]/lexicon_size_year_i))
    )
    PMI[PMI <= 0] = 0
    PMI[PMI > 20] = 0
    temp = PMI <= 20
    PMI[temp is False] = 0
    cor = log(combined_i.copy())
    cor_size = combined_i.copy()
    PMI = PMI/max(PMI)
    cor = cor/max(cor)  # after taking log of count, normalize between 0-1

    relevance_nodes = w_pmi * PMI + (1-w_pmi) * cor

    # Step3: 1st Screen. Reduce number of nodes
    # Get nodesize score, top-n (n=nodeSize) most relevant words, and its relevance score.
    temp = nlargest(nodeSize, zip(relevance_nodes, list(range(0, 50000))))
    temp_size = nlargest(nodeSize, zip(relevance_nodes, cor_size))
    cor_size = [y for x, y in temp_size]

    node = [y for x, y in temp]
    node_score = [x for x, y in temp]
    node_words = [voc_50k[x] for x in node]
    del temp

    # set for key words PMI and cor vale
    if word in node_words:
        node_score[node_words.index(word)] = max(node_score)/3
        cor_size[node_words.index(word)] = max(cor_size)/3

    if word not in node_words:
        node_words.append(word)
        node_score.append(max(node_score)/3)
        cor_size.append(max(cor_size)/3)

    cor_size = cor_size/lexicon_size_year_i
    cor_size_K = {key: value for key, value in zip(node_words, cor_size)}

    # Step 4. prepare edges
    # reduce matrix to 500*500
    tempIndex = [voc_50k.index(w) for w in node_words]
    tempData = tempData[tempIndex, :][:, tempIndex]
    tempData = tempData.transpose() + tempData

    convert_index = {key: value for key, value in zip(
        range(0, len(tempIndex)), tempIndex)}

    # Return a Coordinate (coo) representation of the Compresses-Sparse-Column (csc) matrix.
    coo = tempData.tocoo(copy=False)
    coo = sparse.triu(coo, k=1)

    # Access `row`, `col` and `data` properties of coo matrix.
    coo = DataFrame({
        'word1': coo.row,
        'word2': coo.col,
        'co_occur_count': coo.data
    })[['word1', 'word2', 'co_occur_count']].sort_values(['word1', 'word2'])

    coo = coo[coo.co_occur_count >= 10]
    coo = coo.reset_index(drop=True)

    coo.word1 = [convert_index.get(i) for i in coo.word1]
    coo.word2 = [convert_index.get(i) for i in coo.word2]

    # compute PMI
    p_w1 = year_i_freq[coo.word1.tolist()]/lexicon_size_year_i
    p_w2 = year_i_freq[coo.word2.tolist()]/lexicon_size_year_i
    p_w1_w2 = array(coo.co_occur_count)/lexicon_size_year_i  # (p(a,b))
    tempPMI = log(p_w1_w2/(p_w1*p_w2))

    network_df = coo.copy()
    network_df['PMI'] = tempPMI

    # TODO: This line is the line producing the warning when executing this file
    network_df['PMI'][network_df['PMI'] <= 0] = 0

    network_df = network_df.sort_values('co_occur_count', ascending=False)
    network_df['word1'] = [voc_50k[i] for i in network_df.word1]
    network_df['word2'] = [voc_50k[i] for i in network_df.word2]

    # Trim edges based on PMI
    network_df = network_df[network_df.PMI >= pmi_threshold]

    # Get edge_score
    network_df['co_occur'] = log(network_df.co_occur_count)
    network_df['edge_score'] = e_PMI * network_df.PMI / \
        max(network_df.PMI) + (1-e_PMI) * \
        network_df.co_occur/max(network_df.co_occur)
    network_df.sort_values(by='edge_score', ascending=False)

    words = network_df.word1.tolist()+network_df.word2.tolist()
    edge_scores = network_df.edge_score.tolist()+network_df.edge_score.tolist()
    temp = DataFrame({'words': words, 'edge_scores': edge_scores})
    temp = temp.groupby('words', as_index=False).agg({'edge_scores': 'sum'})
    temp = temp.sort_values(by='edge_scores', ascending=False)
    keep = temp.words[:cap].tolist()

    # Step 5. Prepare plot
    network_df = network_df.reset_index(drop=True)

    if method == Method.COR:
        network_df['co_occurnew'] = sqrt(network_df.co_occur)/60
    if method == Method.PMI:
        network_df['PMInew'] = (network_df.PMI*network_df.PMI)/40

    G = Graph()

    addWeight = []
    for i in range(network_df.shape[0]):
        if method == Method.COR:
            addWeight.append(
                (network_df.word1[i], network_df.word2[i], network_df.co_occurnew[i]))
        if method == Method.PMI:
            addWeight.append(
                (network_df.word1[i], network_df.word2[i], network_df.PMInew[i]))

    G.add_weighted_edges_from(addWeight)

    # remove nodes if connection is less than 5
    remove = [node for node, degree in G.degree() if degree < D]
    G.remove_nodes_from(remove)
    remove = [node for node, degree in G.degree() if degree == 0]
    G.remove_nodes_from(remove)

    if len(G.nodes()) > cap:
        if word not in keep:
            keep = keep + [word]
        remove = [x for x in G.nodes() if x not in keep]
        G.remove_nodes_from(remove)
        remove = [node for node, degree in G.degree().items() if degree <= 1]
        G.remove_nodes_from(remove)

    weights = array([G[u][v]['weight'] for u, v in G.edges()])
    nodesize = array([cor_size_K.get(x) for x in G.nodes()])
    try:
        nodesize = 15*log((nodesize/max(nodesize)+1))
    except ValueError:
        raise Exception(
            'Given your settings, the Context Network has no nodes. Adjust the Context Network settings (set Context Relevance, Context Cohesiveness or Individual World Relevance to a smaller value), making the node filtering less restrictive.'
        )

    if word in G.nodes():
        nodesize[list(G.nodes()._nodes).index(word)] = max(nodesize)

    # Find modularity
    part = None
    try:
        part = community.community_louvain.best_partition(G)
    except ValueError:
        raise Exception(
            'Given your settings, the Context Network has no links. Adjust the Context Network settings to make them more inclusive.')

    # add modularity of each nodes to network
    set_node_attributes(G, part, 'modularity')
    color_values = [part.get(node) for node in G.nodes()]

    # generate node
    nodes_json = DataFrame(
        {
            'id': G.nodes(),
            'nodeSize': nodesize,
            'group': color_values
        }).to_json(orient='records')

    links_json = DataFrame({
        'source': [x[0] for x in G.edges()],
        'target': [x[1] for x in G.edges()],
        'weight': weights
    }).to_json(orient='records')

    json_file = '{"nodes":' + nodes_json + ',' + '"links":' + links_json + '}'

    return json_file
