import xml.etree.ElementTree as ET


###########################################################################
#
# this module meant to provide intuitive functions to work with xml files
#
###########################################################################

# will return a node specified by an attribute key and an attribute value
def get_node_from_xml(xml_file, node_tag, node_att_name, node_att_val):
    root = xml_file.getroot()
    found = root.findall(node_tag + "/[@" + node_att_name + "='" + node_att_val + "']")
    return found


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
