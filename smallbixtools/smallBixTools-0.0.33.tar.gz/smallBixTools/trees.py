import sys
import argparse
import random
from ete3 import Tree, TreeStyle, NodeStyle, faces, AttrFace, CircleFace
import smallBixTools as st


def layout(node):
    if node.is_leaf():
        # Add node name to laef nodes
        N = AttrFace("name", fsize=14, fgcolor="black")
        faces.add_face_to_node(N, node, 0)
    if "weight" in node.features:
        # Creates a sphere face whose size is proportional to node's
        # feature "weight"
        C = CircleFace(radius=node.weight, color="RoyalBlue", style="sphere")
        # Let's make the sphere transparent
        C.opacity = 0.3
        # And place as a float face over the tree
        faces.add_face_to_node(C, node, 0, position="float")


def get_example_tree():
    # Random tree
    t = Tree()
    t.populate(20, random_branches=True)

    # Some random features in all nodes
    for n in t.traverse():
        n.add_features(weight=random.randint(0, 50))

    # Create an empty TreeStyle
    ts = TreeStyle()

    # Set our custom layout function
    ts.layout_fn = layout

    # Draw a tree
    ts.mode = "c"

    # We will add node names manually
    ts.show_leaf_name = False
    # Show branch data
    ts.show_branch_length = True
    ts.show_branch_support = True

    return t, ts


def get_haplo_tree(infile, fasta_fn):
    t = Tree(infile)
    dct = st.fasta_to_dct(fasta_fn)
    for n in t.traverse():
        #print(n)
        #print(dir(n))
        if n.name != '':
            print("is leaf")
            print(n.name)
            print(n.name.split("_"))
            this_freq = float(n.name.split("_")[-1])
            n.add_features(weight=50*this_freq)
        else:
            print("not leaf")
    ts = TreeStyle()
    # Set our custom layout function
    ts.layout_fn = layout

    # Draw a tree
    ts.mode = "r"

    # We will add node names manually
    ts.show_leaf_name = False
    # Show branch data
    ts.show_branch_length = True
    ts.show_branch_support = True

    return t, ts


if __name__ == "__main__":
    #t, ts = get_example_tree()

    tree_with_freq = '/media/dave/0D168CEA7C1531B5/uct/google_drive/University_of_Cape_Town/dev/source/hvtn703/703_sga_ngs_overlap/0902_haplo_tree_freq.nwk'
    partner_fasta = '/media/dave/0D168CEA7C1531B5/uct/google_drive/University_of_Cape_Town/dev/source/hvtn703/703_sga_ngs_overlap/H703_0902_140_to_haplo-ed_sga_HXB2.fasta'
    t, ts = get_haplo_tree(tree_with_freq, partner_fasta)

    #t.render("bubble_map.png", w=600, dpi=300, tree_style=ts)
    t.show(tree_style=ts)

#
# def main(infile):
#     print("Doing main stuff")
#
#
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='some program description')
#     parser.add_argument('-in', '--infile', type=str,
#                         help='some helpful help text', required=True)
#
#     args = parser.parse_args()
#     infile = args.infile
#
#     main(infile)
