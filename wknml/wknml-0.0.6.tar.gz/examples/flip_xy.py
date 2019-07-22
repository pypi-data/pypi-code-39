from argparse import ArgumentParser
from wknml import parse_nml, dump_nml
import xml.etree.ElementTree as ET

parser = ArgumentParser(description="Splits trees in order to fix unlinked nodes.")
parser.add_argument("source", help="Source NML file")
parser.add_argument("target", help="Target NML file")
args = parser.parse_args()


file = parse_nml(ET.parse(args.source).getroot())

new_trees = []
for t in file.trees:
  new_nodes = []
  for n in t.nodes:
    xyz = n.position
    xyz = (xyz[0], xyz[2], xyz[1])
    new_nodes.append(n._replace(position=xyz))
  new_trees.append(t._replace(nodes=new_nodes))

file = file._replace(trees=new_trees)

with open(args.target, "wb") as f:
  f.write(ET.tostring(dump_nml(file)))