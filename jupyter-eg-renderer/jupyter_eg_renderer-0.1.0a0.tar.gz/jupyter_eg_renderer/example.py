import json
import networkx
import ipywidgets as widgets
# from ipywidgets import interact, interactive
from traitlets import Unicode, HasTraits, TraitError, Int,  Float, Bool
from networkx.readwrite import json_graph
@widgets.register
class EgRenderer(widgets.DOMWidget):
    _view_name = Unicode('GraphView').tag(sync=True)
    _model_name = Unicode('GraphModel').tag(sync=True)
    _view_module = Unicode('jupyter-eg-renderer').tag(sync=True)
    _model_module = Unicode('jupyter-eg-renderer').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)
    data = Unicode('{"nodes": [], "links": []}').tag(sync=True)
    layout_method = Unicode('hierarchy').tag(sync=True)

    # Data Loading

    # Node Geometry
    default_node_width = Int(5).tag(sync=True)
    default_node_height = Int(5).tag(sync=True)
    default_link_stroke_width = Float(1.0).tag(sync=True)

    # Node Representation
    default_node_fill_color = Unicode('#eee').tag(sync=True)
    default_node_fill_opacity = Float(1.0).tag(sync=True)
    default_node_label = Unicode('').tag(sync=True)

    default_link_stroke_color = Unicode('#222').tag(sync=True)
    default_link_stroke_opacity = Float(1.0).tag(sync=True)
    default_link_label = Unicode('').tag(sync=True)

    def render(self, graph):
        data = json_graph.node_link_data(graph)
        self.data = json.dumps(data)


# class InputForm(widgets.DOMWidget):
    # @interact(self, y=1)
    # def render(self, y):
    #     return (self, y)
