import rdflib as r, networkx as x
def plainQueryValues(result_dict, join_queries=False):
    """Return query values as simplest list.

    Set join_queries="hard" to keep list of lists structure
    when each result hold only one variable"""

    results = []
    if "bindings" in dir(result_dict):
        results_ = result_dict.bindings
        for result in results_:
            keys = sorted(result.keys())
            this_result = []
            for key in keys:
                value = result[key].toPython()
                this_result += [value]
            results += [this_result]
        if len(results) and len(keys) == 1 and join_queries != "hard":
            results = [i[0] for i in results]
        if len(results) == 1 and join_queries != "list":
            results = results[0]
        return results
    else:
        for result in result_dict["results"]["bindings"]:
            keys = sorted(result.keys())
            this_result = []
            for key in keys:
                value = result[key]["value"]
                type_ = result[key]["type"]
                if type_ == "uri":
                    value = r.URIRef(value)
                elif type_ in ("literal", "bnode"):
                    pass
                elif type_ == "typed-literal":
                    if result[key]["datatype"] == (NS.xsd.integer).toPython():
                        value = int(value)
                    elif result[key]["datatype"] == \
                            (NS.xsd.dateTime).toPython():
                        pass
                    elif result[key]["datatype"] == (NS.xsd.date).toPython():
                        pass
                    elif result[key]["datatype"] == (NS.xsd.boolean).toPython():
                        if value == "true":
                            value = True
                        elif value == "false":
                            value = False
                        else:
                            raise TypeError("Incomming boolean not understood")
                    else:
                        raise TypeError("Incomming typed-literal variable not\
                                        understood")
                else:
                    raise TypeError("Type of incomming variable not understood")
                this_result += [value]
            results += [this_result]
        if len(results) and len(keys) == 1 and join_queries != "hard":
            results = [i[0] for i in results]
        return results

def mkInteractionNetwork(interactions):
    '''Return a directed and weighted network

    The weight of each node is the number of interactions started.
    The weight of each link is the number of occurrence such interaction.
    The extra attribute of each node is the text related to each interaction.

    Note: adapt this routine for specific uses.
    '''

    g = x.DiGraph()
    links = interactions
    for m in links:
        if m[0] in g.nodes(): # author
            g.node[m[0]]["weight"] += 1
        else:
            g.add_node(m[0], weight=1., extra='')
        if len(m) == 3:
            g.node[m[0]]["extra"] += m[2]
        if g.has_edge(m[0], m[1]):
            g[m[0]][m[1]]["weight"] += 1
        else:
            if m[1] not in g.nodes():
                g.add_node(m[1],weight=0., extra='')
            g.add_edge(m[0], m[1], weight=1.)
    return g

def mkRelationNetwork(relations):
    '''Return a simple (undirected, unweighted network)'''

    g = x.Graph()
    links = relations
    for link in links:
        if link[0] == link[1]:
            continue
        g.add_edge(link[0], link[1])
    return g
