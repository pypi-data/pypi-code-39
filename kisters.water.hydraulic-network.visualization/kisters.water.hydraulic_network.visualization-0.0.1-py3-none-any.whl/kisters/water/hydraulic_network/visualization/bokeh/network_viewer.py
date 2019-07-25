from pathlib import Path

import numpy as np
from bokeh.models import GraphRenderer, ImageURL, MultiLine, StaticLayoutProvider
from bokeh.models.ranges import Range1d
from bokeh.models.tiles import WMTSTileSource
from bokeh.plotting import figure
from scipy.interpolate import make_interp_spline

from kisters.water.hydraulic_network.client import Network


class NetworkViewer:
    node_size = 10

    image_path = "https://gitlab.com/kisters/water/hydraulic-network/visualization/raw/master/kisters/water/hydraulic_network/visualization/images"
    vertex_interpolation_density = 1.0 / 50.0

    link_as_node_types = set(["Pump", "Turbine", "Valve", "Pump", "Orifice"])

    def __init__(self, network: Network):
        self.figure = figure(x_axis_type="mercator", y_axis_type="mercator")

        # Store network
        self.__network = network
        self.__get_topology()

        # Add OpenStreetMaps background
        tile_source = WMTSTileSource(
            url="https://tiles.basemaps.cartocdn.com/light_all/{z}/{x}/{y}@2.png",
            # url="http://c.tile.openstreetmap.org/{z}/{x}/{y}.png",
            attribution=(
                '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, '
                '&copy; <a href="https://cartodb.com/attributions">CartoDB</a>'
            ),
            initial_resolution=None,
        )

        self.figure.add_tile(tile_source)

        # Add renderer
        self.__graph_renderer = GraphRenderer()
        self.figure.renderers.append(self.__graph_renderer)

        # Render
        self.__render()

    def __get_topology(self):
        self.__nodes = {node.uid: node.asdict() for node in self.__network.get_nodes()}

        raw_links = [link.asdict() for link in self.__network.get_links()]
        links = []

        def centroid(a, b):
            va = np.array([a["location"]["x"], a["location"]["y"]])
            vb = np.array([b["location"]["x"], b["location"]["y"]])
            return np.mean(np.vstack([va, vb]), axis=0)

        for link in raw_links:
            # In hydraulic network, pumps and valves are links.  We display a pump (or a valve) as a
            # link - node - link in the graph.
            if link["type"] in self.link_as_node_types:
                source_node = self.__nodes[link["source_uid"]]
                target_node = self.__nodes[link["target_uid"]]
                vertices = link.get("vertices", [])
                if len(vertices) >= 1:
                    center = vertices[len(vertices) // 2]
                else:
                    center = centroid(source_node, target_node)
                self.__nodes[link["uid"]] = {
                    "uid": link["uid"],
                    "display_name": link["display_name"],
                    "location": {"x": center[0], "y": center[1]},
                    "type": link["type"],
                }
                links.append(
                    {
                        "uid": f"{source_node['uid']}__{link['uid']}",
                        "source_uid": link["source_uid"],
                        "target_uid": link["uid"],
                        "vertices": vertices[: len(vertices) // 2],
                    }
                )
                links.append(
                    {
                        "uid": f"{link['uid']}__{target_node['uid']}",
                        "source_uid": link["uid"],
                        "target_uid": link["target_uid"],
                        "vertices": vertices[len(vertices) // 2 + 1 :],
                    }
                )
            else:
                links.append(link)

        self.__links = {link["uid"]: link for link in links}

    def __render(self):
        nodes, links = self.__nodes.values(), self.__links.values()

        # Add nodes
        def image_url(node):
            return f"{self.image_path}/{node['type']}.svg"

        self.__graph_renderer.node_renderer.data_source.data = dict(
            index=[node["uid"] for node in nodes],
            url=[image_url(node) for node in nodes],
        )
        self.__graph_renderer.node_renderer.glyph = ImageURL(
            w={"value": self.node_size, "units": "screen"},
            h={"value": self.node_size, "units": "screen"},
            anchor="center",
            url="url",
        )

        # Interpolate edge vertices using B-Splines
        xs = []
        ys = []
        for link in links:
            # Concatenate start coordinate, vertices, and end coordinate
            x = [
                self.__nodes[link["source_uid"]]["location"]["x"],
                *[v["x"] for v in link.get("vertices", [])],
                self.__nodes[link["target_uid"]]["location"]["x"],
            ]

            y = [
                self.__nodes[link["source_uid"]]["location"]["y"],
                *[v["y"] for v in link.get("vertices", [])],
                self.__nodes[link["target_uid"]]["location"]["y"],
            ]

            # Compute path length
            ds = np.sqrt(np.diff(x) ** 2 + np.diff(y) ** 2)
            if np.any(ds == 0):
                raise ValueError(
                    f"Please make sure that the vertices of link {link['uid']} do not overlap with themselves or with the location of the node upstream or downstream."
                )
            s = [np.sum(ds[0:i]) for i in range(len(x))]

            # Carry out interpolation if needed
            if len(s) > 2:
                # B-Spline order
                k = min(3, len(s) - 1)

                # If 3rd order, we want the natural B-Spline
                if k >= 3:
                    bc_type = ([(2, 0.0)], [(2, 0.0)])
                else:
                    bc_type = None

                # Fit B-Splines and interpolate for both coordinates
                spl = make_interp_spline(s, x, k=k, bc_type=bc_type)
                x = spl(
                    np.linspace(
                        0,
                        s[-1],
                        max(len(s), int(self.vertex_interpolation_density * s[-1])),
                    )
                )

                spl = make_interp_spline(s, y, k=k, bc_type=bc_type)
                y = spl(
                    np.linspace(
                        0,
                        s[-1],
                        max(len(s), int(self.vertex_interpolation_density * s[-1])),
                    )
                )

            # Store points
            xs.append(x)
            ys.append(y)

        # Add edges
        self.__graph_renderer.edge_renderer.data_source.data = dict(
            start=[link["source_uid"] for link in links],
            end=[link["target_uid"] for link in links],
            xs=xs,
            ys=ys,
        )
        self.__graph_renderer.edge_renderer.glyph = MultiLine(
            line_color="#6686ba", line_alpha=1.0, line_width=5
        )

        # Set node layout
        graph_layout = {
            node["uid"]: (node["location"]["x"], node["location"]["y"])
            for node in nodes
        }
        self.__graph_renderer.layout_provider = StaticLayoutProvider(
            graph_layout=graph_layout
        )

        # Set viewport
        x = [node["location"]["x"] for node in nodes] + [
            v["x"] for link in links for v in link.get("vertices", [])
        ]
        y = [node["location"]["y"] for node in nodes] + [
            v["y"] for link in links for v in link.get("vertices", [])
        ]
        min_x = np.min(x)
        max_x = np.max(x)
        min_y = np.min(y)
        max_y = np.max(y)

        margin = 0.5 * self.node_size
        width = np.max([max_x - min_x, max_y - min_y]) + 2 * margin

        mean_x = np.mean([min_x, max_x])
        self.figure.x_range = Range1d(
            int(mean_x - 0.5 * width), int(mean_x + 0.5 * width)
        )
        self.figure.x_range.reset_start = self.figure.x_range.start
        self.figure.x_range.reset_end = self.figure.x_range.end

        mean_y = np.mean([min_y, max_y])
        self.figure.y_range = Range1d(
            int(mean_y - 0.5 * width), int(mean_y + 0.5 * width)
        )
        self.figure.y_range.reset_start = self.figure.y_range.start
        self.figure.y_range.reset_end = self.figure.y_range.end
