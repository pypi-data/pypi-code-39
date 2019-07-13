import os_tools.XmlFileHandler as xh
import os_tools.Tools as tools

xml = xh.read_xml_file('/Users/home/Programming/Python/modules/android/strings.xml')
nodes = xh.get_nodes_from_xml_without_att(xml, 'string', 'translatable')
dict = {}