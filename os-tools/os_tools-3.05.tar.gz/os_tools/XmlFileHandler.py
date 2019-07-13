import xml.etree.ElementTree as ET


###########################################################################
#
# this module meant to provide intuitive functions to work with xml files
#
###########################################################################


# will return a list of nodes specified by an attribute key and an attribute value
def get_nodes_from_xml(xml_file, node_tag, node_att_name=None, node_att_val=None):
    root = xml_file.getroot()
    selector = node_tag
    if node_att_name is not None:
        if node_att_val is not None:
            selector = node_tag + "/[@" + node_att_name + "='" + node_att_val + "']"
        else:
            selector = node_tag + "/[@" + node_att_name + "]"
    return root.findall(selector)


# will return a list of nodes which doesn't have a specific attribute
def get_nodes_from_xml_without_att(xml_file, node_tag, node_att_name=None):
    root = xml_file.getroot()
    relevant_nodes = []
    nodes = root.findall(node_tag)
    for node in nodes:
        if get_att_value_from_node(node, node_att_name) is None:
            relevant_nodes.append(node)
    return relevant_nodes


def nodes_to_dict(nodes, att_key):
    """
    Will turn a list of xml nodes to a dictionary carrying the nodes.
    The keys of the dictionary will be the attribute value of each node and the values of of the dictionary will be the inner text
    of each node.

    For example, if we have these xml nodes:
        <string name="app_name">First Remote</string>
        <string name="app_short_name" translatable="false">remote</string>

    xml_nodes_to_dict(nodes, 'name') will return:
    dict = {'app_name': 'First Remote', 'app_short_name': 'remote'}

    param nodes: the xml nodes to search upon
    param att_key: the attribute to search for it's value in each node
    return: a dictionary representation of the nodes
    """

    nodes_dict = {}
    for node in nodes:
        nodes_dict[get_att_value_from_node(node, att_key)] = get_text_from_node(node)
    return nodes_dict


# will return the text (inner html) of a given node
def get_text_from_node(node):
    return node.text


# will set the text (inner html) in a given node
def set_text_in_node(node, text):
    node.text = text


# will return the value of a given att from a desired node
def get_att_value_from_node(node, att_name):
    return node.get(att_name)


# will return an xml file
def read_xml_file(xml_path):
    return ET.parse(xml_path)


# will save the changes made in an xml file
def save_xml_file(xml_file, xml_path):
    xml_file.write(xml_path)
