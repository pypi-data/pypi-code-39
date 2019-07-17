"""
A few basic routines to explore a cgns file
"""


def get_nodes(base, cgns_type):
    """ Get sub nodes of a given type from upper_node """
    node_list = []
    for node_name in base:
        node = base[node_name]
        if 'label' in node.attrs:
            if node.attrs['label'] == cgns_type:
                node_list.append(node)
    return node_list


def get_node_by_name(base, name):
    """Get a node by name"""
    for node_name in base:
        node = base[node_name]
        if ('name' in node.attrs) and (node.attrs['name'] == name):
            return node
    raise ValueError('Node not found')


def get_node_by_type(base, ntype):
    """Get a node by type, but only if it is unique"""
    found = [base[node] for node in base
             if (('label' in base[node].attrs) and
                 (base[node].attrs['label'] == ntype))]
    if len(found) > 1:
        raise ValueError('Node is not unique')
    if len(found) == 1:
        return found[0]
    raise ValueError('Node not found')


def get_names(base, ntype):
    """ Get the names of all nodes of a given type """
    output = []
    for node in get_nodes(base, ntype):
        output.append(node.attrs['name'])
    return output


def node_exists(base, name):
    """
    Check if a node exists given his name
    """
    exists = False
    for node_name in base:
        node = base[node_name]
        if 'name' in node.attrs:
            print((node.attrs['name'], name))
            if node.attrs['name'] == name:
                exists = True
    return exists


def get_value(up_node, name):
    """ Get value out of a node """
    node = get_node_by_name(up_node, name)
    return node[' data'].value


def ascii2string(ascii_list):
    """ Ascii to string convertion """
    return ''.join(chr(i) for i in ascii_list)
