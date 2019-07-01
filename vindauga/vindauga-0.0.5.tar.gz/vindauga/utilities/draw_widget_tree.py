# -*- coding: utf-8 -*-

from io import StringIO

nodeChild = '  ├─'
nodeLast = '  └─'
treeLine = '  │'


def drawWidgetTree(node, prefix='', last=False):
    buf = StringIO()
    if prefix:
        buf.write(prefix[:-3])
        if not last:
            buf.write(nodeChild)
        else:
            buf.write(nodeLast)
    buf.write(f' {node.name}\n')
    subPrefix = prefix + treeLine
    last = False
    for index, child in enumerate(node.children):
        if index + 1 == len(node.children):
            subPrefix = prefix + '   '
            last = True
        buf.write(drawWidgetTree(child, subPrefix, last))
    return buf.getvalue()
