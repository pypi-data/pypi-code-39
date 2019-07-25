# External libraries
from numpy import load, einsum, triu, array
from pandas import DataFrame
from sklearn import preprocessing
from networkx import Graph, set_node_attributes
import community

# Standard library
from typing import Tuple
from scipy import sparse

# Local libraries
from lib.closestSynonyms import closest_synonyms
from lib.globals import configFileName, dataDirPropName
from lib.jsonfs import getJsonFromFile


def plot_synonym_structure(
    words: Tuple[str],
    year: int = 2000,
    k: int = 5,
    minSim: float = 0.72
):
    # Explain hyper-parameters
    '''
    year_i : which year we are looking at 
    k: number of synonyms of each target word is included in the structure
    minSim: link if semantic similarity is larger than minSIm
    '''
    suffix = '_svd_PPMI.npy'

    w_combined = []
    for i in range(len(words)):
        w_combined.append(closest_synonyms((words[i],), year, k)[1][0])
    w_combined = sum(w_combined, [])

    dataDir = getJsonFromFile(configFileName).get(dataDirPropName)

    m = load(dataDir + '/embeddings-10-years/' + str(year) + suffix)
    voc = load(dataDir + '/vocabulary.pkl', allow_pickle=True)
    m = preprocessing.normalize(m)

    tempInd = [voc.index(w) for w in w_combined]
    word_embeddings = m[tempInd, :]

    # construct similarity table, prepare for network plot
    convert_index = {key: value for key, value in zip(
        range(0, len(w_combined)), w_combined)}

    sim_matrix = einsum('xj,yj->xy', word_embeddings, word_embeddings)
    sim_martix = triu(sim_matrix, k=1)
    coo = sparse.coo_matrix(sim_matrix)
    coo = sparse.triu(coo, k=1)

    coo = DataFrame({
        'word1': coo.row,
        'word2': coo.col,
        'value': coo.data
    })[['word1', 'word2', 'value']].sort_values(['word1', 'word2'])

    coo.word1 = [convert_index.get(i) for i in coo.word1]
    coo.word2 = [convert_index.get(i) for i in coo.word2]
    network_df = coo.copy()

    # select threshold of similarity value
    network_df = network_df[network_df.value >= minSim]

    # Plot
    G = Graph()

    # weight by similarity
    addWeight = []
    for i in range(network_df.shape[0]):
        addWeight.append(
            (network_df.word1.iloc[i], network_df.word2.iloc[i], network_df.value.iloc[i]))

    G.add_weighted_edges_from(addWeight)

    # don't remove any nodes
    remove = [node for node, degree in G.degree() if degree < 0]
    G.remove_nodes_from(remove)
    K = 0.2

    # Find modularity
    try:
        part = community.community_louvain.best_partition(G)
    except ValueError:
        raise Exception('Given your settings, the Context Network has no links. Adjust the Context Network settings to make them more inclusive.')

    try:
        mod = community.community_louvain.modularity(part, G)
    except ValueError:
        raise Exception('Given your settings, the Synonym Network has no links. Adjust the Synonym Network settings to make them more inclusive.')

    # add modularity of each nodes to network
    set_node_attributes(G, part, 'modularity')
    color_values = [part.get(node) for node in G.nodes()]  # set colors

    weights = array([G[u][v]['weight'] for u, v in G.edges()])

    '''
    plt.figure(figsize=(40,30))
    selectPosPatten = nx.spring_layout(G,iterations=100,weight = 'weight',scale=900,k = K)  #k controls the distance between the nodes and varies between 0 and 1; default k=0.1
    nx.draw_networkx_nodes(G,pos = selectPosPatten, cmap = plt.cm.plasma,node_color = color_values ,alpha=0.55,
                           #node_size = [v*50 for v in nx.degree(G).values()]) 
                           node_size = [v*200 for v in nx.degree(G).values()]) 

    nx.draw_networkx_edges(G,pos = selectPosPatten, camp = plt.cm.plasma, edge_color = 'grey', width = weights)

    x=nx.draw_networkx_labels(G,pos = selectPosPatten, font_size=45, font_family='sans-serif')
    plt.savefig('../#6_figure/emotion_'+' '.join(target_w)+'.jpg' )
    '''

    nodes_json = DataFrame(
        {'id': G.nodes(), 'group': color_values}).to_json(orient='records')
    links_json = DataFrame({'source': [x[0] for x in G.edges()], 'target': [
                              x[1] for x in G.edges()], 'weight': weights}).to_json(orient='records')

    # TODO: use json dumps
    json_file = '{"nodes":' + nodes_json + ',' + '"links":' + links_json + '}'

    return json_file
