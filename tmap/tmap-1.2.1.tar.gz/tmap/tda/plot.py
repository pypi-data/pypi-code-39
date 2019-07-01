# -*- coding: utf-8 -*-
import colorsys
from collections import defaultdict

import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objs as go
from pandas.api import types
from plotly import tools
from scipy import stats
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

from tmap.netx.SAFE import get_significant_nodes
from tmap.tda.utils import c_node_text, write_figure


class Color(object):
    """
    map colors to target values for TDA network visualization

    * If ``target_by`` set as *samples*, it means that it will pass original data instead of SAFE score for colorizing the node on the graph.
    * If ``node`` set as *node*, it means that it will pass SAFE score for colorizing the node on the graph. So the target must be a dictionary generated by SAFE_batch function. If you using single SAFE function called ``SAFE``, it will also create a dict which could be used.

    The basically code assign the highest values with red and the lowest values with blue. Before we assign the color, it will split the target into 4 parts with ``np.percentile`` and scale each part with different upper and lower boundary.

    It is normally have 4 distinct parts in color bar but it will easily missing some parts due to some skewness which misleading the values of percentile.

    :param list/np.ndarray/pd.Series/dict target: target values for samples or nodes
    :param str dtype: type of target values, "numerical" or "categorical"
    :param str target_by: target type of "sample" or "node"

    """

    def __init__(self,
                 target,
                 dtype="numerical",
                 target_by="sample"):
        """
        :param list/np.ndarray/pd.Series target: target values for samples or nodes
        :param str dtype: type of target values, "numerical" or "categorical"
        :param str target_by: target type of "sample" or "node"
        (for node target values, accept a node associated dictionary of values)
        """
        if target is None:
            raise Exception("target must not be None.")
        if dtype not in ["numerical", "categorical"]:
            raise ValueError("data type must be 'numerical' or 'categorical'.")
        if target_by not in ["sample", "node"]:
            raise ValueError("target values must be by 'sample' or 'node'")
        # for node target values, accept a node associated dictionary of values
        if target_by == 'node':
            _target = np.zeros(len(target))
            if type(target) == list:
                _target = np.array(target[::])
            elif type(target) == dict:
                for _node_idx, _node_val in target.items():
                    _target[_node_idx] = _node_val
            else:
                _target = np.array(target[::])
            target = _target

        if type(target) is not np.ndarray:
            target = np.array(target)
        if len(target.shape) == 1:
            target = target.reshape(-1, 1)

        # target values should be numbers, auto-check and encode categorical labels
        # but the labels must like the original target, so it assigned before process the target
        self.labels = target[:, 0]
        if types.is_numeric_dtype(target):
            # if target is numeric no matter assigned dtype
            self.label_encoder = None
            self.target = target
        else:
            # if target is cat.
            self.label_encoder = LabelEncoder()
            self.target = self.label_encoder.fit_transform(target.astype(str).ravel()).reshape(-1, 1)

        self.dtype = dtype

        self.target_by = target_by

    def _process_cat_color(self, cmap=None):
        if self.dtype == 'categorical':
            if cmap is None:
                generated_color_v = np.arange(0.0,
                                              1 + 1e-6,
                                              1.0 / (len(set(self.labels)) - 1))  # add 1 into idx, so it is 1 + 1e-6 which is little bigger than 1.
                generated_colors = [self._get_hex_color(_) for _ in generated_color_v]
                cat2color = dict(zip(sorted(set(self.labels)),  # order doesn't matter
                                     generated_colors))
                # generate a series of color corresponding to each categorical
            else:
                for label in self.labels:
                    if label not in cmap:
                        raise Exception('assigned cmap is not contain all cmap. such as %s' % label)
                cat2color = cmap
            return cat2color

    def _get_hex_color(self, i, cmap=None):
        """
        map a normalize i value to HSV colors
        :param i: input for the hue value, normalized to [0, 1.0]
        :return: a hex color code for i
        """
        # H values: from 0 (red) to 240 (blue), using the HSV color systems for color mapping
        # largest value of 1 mapped to red, and smallest of 0 mapped to blue
        c = colorsys.hsv_to_rgb((1 - i) * 240 / 360, 1.0, 0.75)
        return "#%02x%02x%02x" % (int(c[0] * 255), int(c[1] * 255), int(c[2] * 255))

    def _rescale_target(self, target):
        """
        scale target values according to density/percentile
        to make colors distributing evenly among values
        :param target: numerical target values
        :return:
        """
        rescaled_target = np.zeros(target.shape)

        scaler_min_q1 = MinMaxScaler(feature_range=(0, 0.25))
        scaler_q1_median = MinMaxScaler(feature_range=(0.25, 0.5))
        scaler_median_q3 = MinMaxScaler(feature_range=(0.5, 0.75))
        scaler_q3_max = MinMaxScaler(feature_range=(0.75, 1))

        q1, median, q3 = np.percentile(target, 25), np.percentile(target, 50), np.percentile(target, 75)

        index_min_q1 = np.where(target <= q1)[0]
        index_q1_median = np.where(((target >= q1) & (target <= median)))[0]
        index_median_q3 = np.where(((target >= median) & (target <= q3)))[0]
        index_q3_max = np.where(target >= q3)[0]

        try:
            target_min_q1 = scaler_min_q1.fit_transform(target[index_min_q1]) if any(index_min_q1) else np.zeros(target[index_min_q1].shape)
            target_q1_median = scaler_q1_median.fit_transform(target[index_q1_median]) if any(index_q1_median) else np.zeros(target[index_q1_median].shape)
            target_median_q3 = scaler_median_q3.fit_transform(target[index_median_q3]) if any(index_median_q3) else np.zeros(target[index_median_q3].shape)
            target_q3_max = scaler_q3_max.fit_transform(target[index_q3_max]) if any(index_q3_max) else np.zeros(target[index_q3_max].shape)
            # in case the situation which will raise ValueError when sliced_index is all False.
        except Exception as e:
            import pdb;
            pdb.set_trace()

        # using percentile to cut and assign colors will meet some special case which own weak distribution.
        # below `if` statement is trying to determine and solve these situations.
        if all(target_q3_max == 0.75):
            # all transformed q3 number equal to the biggest values 0.75.
            # if we didn't solve it, red color which representing biggest value will disappear.
            # solution: make it all into 1.
            target_q3_max = np.ones(target_q3_max.shape)
        if q1 == median == q3:
            # if the border of q1,median,q3 area are all same, it means the the distribution is extremely positive skewness.
            # Blue color which represents smallest value will disappear.
            # Solution: Make the range of transformed value output from the final quantile into 0-1.
            target_q3_max = np.array([_ if _ != 0.75 else 0 for _ in target_q3_max[:, 0]]).reshape(target_q3_max.shape)

        rescaled_target[index_median_q3] = target_median_q3
        rescaled_target[index_q1_median] = target_q1_median
        rescaled_target[index_min_q1] = target_min_q1
        rescaled_target[index_q3_max] = target_q3_max

        return rescaled_target

    def get_colors(self, nodes, cmap=None):
        """
        :param dict nodes: nodes from graph
        :param cmap: not implemented yet...For now, it only accept manual assigned dict like {sample1:color1,sample2:color2.....}
        :return: nodes colors with keys, and the color map of the target values
        :rtype: tuple (first is a dict node_ID:node_color, second is a tuple (node_ID_index,node_color))
        """
        if self.target.shape[0] != len(nodes) and self.target_by == 'node':
            print("Warning!!! target you provided may not the nodes associated values. it won't raise fatal error but may raise silent error.")
        # todo: accept a customzied color map [via the 'cmap' parameter]
        node_keys = nodes
        cat2color = {}
        if self.dtype == 'categorical' and cmap is not None:
            cat2color = cmap
        elif self.dtype == 'categorical':
            cat2color = self._process_cat_color(cmap=cmap)
        # map a color for each node
        node_colors = []
        node_color_target = []
        for i, node_id in enumerate(node_keys):
            if self.target_by == 'node':
                target_in_node = self.target[[node_id]]
            else:
                try:
                    target_in_node = self.target[nodes[node_id]['sample']]
                except IndexError:
                    raise SyntaxError("Maybe you provide a data with row number equal to nodes,"
                                      "and doesn't change default params 'target_by' of Color into 'node'")

            # summarize target values from samples/nodes for each node
            if self.dtype == "numerical":
                node_color_target.append(np.nanmean(target_in_node))

            else:  # self.dtype == "categorical":
                # Return an array of the modal (most common) value in the passed array. (if more than one, the smallest is return)
                # target_in_node could be str or int...
                most_num = stats.mode(target_in_node)[0][0][0]
                if self.label_encoder is not None:
                    num2str = dict(zip(self.target[:, 0],
                                       self.label_encoder.inverse_transform(self.target.ravel())))
                    most_str = num2str[most_num]
                else:
                    most_str = most_num
                node_colors.append(cat2color.get(most_str, 'blue'))
                node_color_target.append(most_str)

        node_color_target = np.array(node_color_target).reshape(-1, 1)
        if self.dtype == 'numerical':
            _node_color_idx = self._rescale_target(node_color_target)
            node_colors = [self._get_hex_color(idx) for idx in _node_color_idx]
        # if np.any(np.isnan(node_color_target)):
        #     print("Nan was found in the given target, Please check the input data.")
        return dict(zip(node_keys,
                        node_colors)), \
               (node_color_target,
                node_colors)

    def get_sample_colors(self, cmap=None):
        """
        :param dict nodes: nodes from graph
        :param cmap: not implemented yet...For now, it only accept manual assigned dict like {sample1:color1,sample2:color2.....}
        :return: nodes colors with keys, and the color map of the target values
        :rtype: tuple (first is a list samples_colors, second is a tuple (node_ID_index,node_color))
        """
        cat2color = {}

        if self.target_by == "node":
            sample_colors = ['red' for _ in self.target]
            # because passed target is node-shapes data. could not proper broadcast
        else:
            if self.dtype == "numerical":
                _sample_color_idx = self._rescale_target(self.target)
                sample_colors = [self._get_hex_color(idx) for idx in _sample_color_idx]
            else:  # self.dtype == "categorical"
                cat2color = self._process_cat_color(cmap=cmap)
                sample_colors = [cat2color[each] for each in self.labels]

                # todo: implement more custom cmap
        return sample_colors, cat2color


def show(graph, color=None, fig_size=(10, 10), node_size=10, edge_width=2, mode='spring', notshow=False, **kwargs):
    """
    Network visualization of TDA mapper

    Using matplotlib as basic engine, it is easily add title or others elements.
    :param tmap.tda.Graph.Graph graph:
    :param Color/str color: Passing ``tmap.tda.plot.Color`` or just simply color string.
    :param tuple fig_size: height and width
    :param int node_size: With given node_size, it will scale all nodes with same size ``node_size/max(node_sizes) * node_size **2``. The size of nodes also depends on the biggest node which contains maxium number of samples.
    :param int edge_width: Line width of edges.
    :param str/None mode: Currently, Spring layout is the only one style supported.
    :param float strength: Optimal distance between nodes.  If None the distance is set to ``1/sqrt(n)`` where n is the number of nodes.  Increase this value to move nodes farther apart.
    :return: plt.figure
    """
    # todo: add file path for graph saving
    node_keys = graph.nodes
    node_positions = graph.nodePos
    node_sizes = list(graph.size.values())

    # scale node sizes
    max_node_size = np.max(node_sizes)
    sizes = (node_sizes / max_node_size) * (node_size ** 2)

    # map node colors or init node color if not provided
    if color is None or type(color) == str:
        color = 'red' if color is None else color
        color_map = {node_id: color for node_id in node_keys}
        target2colors = (np.zeros((len(node_keys), 1)),
                         [color] * len(node_keys))
    else:
        color_map, target2colors = color.get_colors(node_keys)

    colorlist = [color_map[it] for it in node_keys]
    node_target_values, node_colors = target2colors
    legend_lookup = dict(zip(node_target_values.ravel(),  # flattern the node_target_values
                             node_colors))

    # if there are indicated color with ``Color``, it need to add some legend for given color.
    # Legend part
    if isinstance(color, Color):
        if color.dtype == "categorical":
            fig = plt.figure(figsize=fig_size)
            ax = fig.add_subplot(1, 1, 1)
            all_cats = legend_lookup.keys()
            label_color = [legend_lookup.get(e_cat,
                                             None) for e_cat in all_cats]
            get_label_color_dict = dict(zip(all_cats,
                                            label_color))

            # add categorical legend
            for label in sorted(set(all_cats)):
                if label_color is not None:
                    ax.plot([], [], 'o',
                            color=get_label_color_dict[label], label=label, markersize=10)

            legend = ax.legend(numpoints=1, loc="upper right")
            legend.get_frame().set_facecolor('#bebebe')

        # add numerical colorbar
        elif color.dtype == "numerical":
            fig = plt.figure(figsize=(fig_size[0] * 10 / 9, fig_size[1]))
            ax = fig.add_subplot(1, 1, 1)
            legend_values = sorted([val for val in legend_lookup])
            legned_colors = [legend_lookup.get(val, 'blue') for val in legend_values]

            # add color bar
            # TODO: Implement more details of color bar and make it more robust.
            cmap = mcolors.LinearSegmentedColormap.from_list('my_cmap', legned_colors)
            norm = mcolors.Normalize(min(legend_values), max(legend_values))
            sm = cm.ScalarMappable(cmap=cmap, norm=norm)
            sm.set_array([])

            cb = fig.colorbar(sm,
                              shrink=0.5,
                              pad=0.1)
            cb.ax.yaxis.set_ticks_position('right')
            if min(legend_values) != 0:
                # if minimum values of legend is not 0, it need to add a text to point out the minimum values.
                if min(legend_values) * 100 >= 0.1:
                    # Determine whether the minimum value is too small to visualize pretty.
                    # .2f indicates accurate to the second decimal place.
                    # .2e indicated accurate to the second decimal after scientific notation.
                    cb.ax.text(0.5, -0.02, '{:.2f}'.format(min(legend_values)), ha='center', va='top', weight='bold')
                else:
                    cb.ax.text(0.5, -0.02, '{:.2e}'.format(min(legend_values)), ha='center', va='top', weight='bold')

            if max(legend_values) * 100 >= 0.1:
                # same as the minimum values
                cb.ax.text(0.5, 1.02, '{:.2f}'.format(max(legend_values)), ha='center', va='bottom', weight='bold')
            else:
                cb.ax.text(0.5, 1.02, '{:.2e}'.format(max(legend_values)), ha='center', va='bottom', weight='bold')
    else:
        fig = plt.figure(figsize=fig_size)
        ax = fig.add_subplot(1, 1, 1)

    if mode == 'spring':
        ori_pos = graph.data
        if ori_pos.shape[1] < 2:
            pos = nx.spring_layout(graph, **kwargs)
        else:
            ori_pos = graph.transform_sn(ori_pos[:, :2], type='s2n')
            ori_pos = {n: tuple(ori_pos.iloc[n, :2]) for n in graph.nodes}
            pos = nx.spring_layout(graph, pos=ori_pos, **kwargs)
        # add legend
        nx.draw_networkx(graph,
                         ax=ax,
                         pos=pos,
                         node_size=sizes,
                         node_color=colorlist,
                         width=edge_width,
                         edge_color=[color_map[edge[0]] for edge in graph.edges],
                         with_labels=False)

    else:
        node_idx = dict(zip(node_keys, range(len(node_keys))))
        for edge in graph.edges:
            ax.plot([node_positions[node_idx[edge[0]], 0], node_positions[node_idx[edge[1]], 0]],
                    [node_positions[node_idx[edge[0]], 1], node_positions[node_idx[edge[1]], 1]],
                    c=color_map[edge[0]], zorder=1)
        ax.scatter(node_positions[:, 0], node_positions[:, 1],
                   c=colorlist, s=sizes, zorder=2)

    plt.axis("off")
    if notshow:
        return plt
    else:
        plt.show()


def tm_plot(graph, filename, mode='file', include_plotlyjs='cdn', color=None, _color_SAFE=None, min_size=10, max_size=40, **kwargs):
    vis_progressX(graph, simple=True, filename=filename, include_plotlyjs=include_plotlyjs, color=color, _color_SAFE=_color_SAFE, min_size=min_size, max_size=max_size,
                  mode=mode, **kwargs)


def vis_progressX(graph, simple=False, mode='file', color=None, _color_SAFE=None, min_size=10, max_size=40, **kwargs):
    """
    For dynamic visualizing tmap construction process, it performs a interactive graph based on `plotly` with a slider to present the process from ordination to graph step by step. Currently, it doesn't provide any API for overriding the number of step from ordination to graph. It may be implemented at the future.

    If you want to draw a simple graph with edges and nodes instead of the process,  try the params ``simple``.

    This visualized function is mainly based on plotly which is a interactive Python graphing library. The params mode is trying to provide multiple type of return for different purpose. There are three different modes you can choose including "file" which return a html created by plotly, "obj" which return a reusable python dict object and "web" which normally used at notebook and make inline visualization possible.

    The color part of this function has a little bit complex because of the multiple sub-figures. Currently, it use the ``tmap.tda.plot.Color`` class to auto generate color with given array. More detailed about how to auto generate color could be reviewed at the annotation of ``tmap.tda.plot.Color``.

    In this function,  there are two kinds of color need to implement.

        * First, all color and its showing text values of samples points should be followed by given color params. The color could be **any array** which represents some measurement of Nodes or Samples. **It doesn't have to be SAFE score**.

        * Second, The ``_color_SAFE`` param should be a ``Color`` with a nodes-length array, which is normally a SAFE score.

    :param tmap.tda.Graph.Graph graph:
    :param str mode: [file|obj|web]
    :param bool simple:
    :param color:
    :param _color_SAFE:
    :param kwargs:
    :return:
    """
    node_pos = graph.nodePos
    # shape is average projected_data (node x lens)
    sample_pos = graph.data
    # shape is raw projected_data (sample x lens)
    nodes = graph.nodes
    sizes = graph.size

    sample_names = np.array(graph.sample_names.astype(str))
    minmax_scaler = MinMaxScaler(feature_range=(min_size, max_size))
    mms_color = MinMaxScaler(feature_range=[0, 1])

    scaled_size = minmax_scaler.fit_transform(np.array([sizes[_] for _ in range(len(nodes))]).reshape(-1, 1))

    # init some empty values if color wasn't given
    target_v_raw = [0 for _ in nodes]
    target_v = [0 for _ in nodes]
    target_colors = ['blue' for _ in nodes]
    sample_colors = ['red' for _ in sample_names]
    cat2color = defaultdict(lambda: 'blue')
    legend_names = []

    if color is None or type(color) == str:
        color = 'red' if color is None else color
        color_map = {node_id: color for node_id in graph.nodes}
        target2colors = (np.zeros((len(graph.nodes), 1)),
                         [color] * len(graph.nodes))
    else:
        color_map, target2colors = color.get_colors(graph.nodes)
        if types.is_numeric_dtype(target2colors[0]):
            target_v = mms_color.fit_transform(target2colors[0]).ravel()
        else:
            target_v = []
        target_v_raw = target2colors[0].ravel()
        target_colors = target2colors[1]

        sample_colors, cat2color = color.get_sample_colors()
        if color.dtype == 'categorical':
            legend_names = target2colors[0][:, 0]

    # For calculating the dynamic process. It need to duplicate the samples first.
    # reconstructing the ori_MDS into the samples_pos
    # reconstructing the node_pos into the center_pos
    sample_tmp = []
    center_tmp = []
    text_tmp = []
    duplicated_sample_colors = []
    for n in nodes:
        sample_tmp.append(sample_pos[nodes[n]['sample'], :])
        center_tmp.append(np.repeat(node_pos[[n], :],
                                    sizes[n],
                                    axis=0))
        text_tmp.append(sample_names[nodes[n]['sample']])
        if color is not None:
            duplicated_sample_colors += list(np.repeat(color_map.get(n, 'blue'),
                                                       sizes[n]))
        else:
            duplicated_sample_colors += ["blue"] * sizes[n]
    duplicated_sample_pos = np.concatenate(sample_tmp, axis=0)
    duplicated_node_pos = np.concatenate(center_tmp, axis=0)
    duplicated_samples_text = np.concatenate(text_tmp, axis=0)
    assert duplicated_sample_pos.shape[0] == duplicated_node_pos.shape[0] == duplicated_samples_text.shape[0] == len(duplicated_sample_colors)
    # For visualizing the movement of samples, it need to multiply one sample into multiple samples which is need to reconstruct pos,text.

    # prepare edge data
    xs = []
    ys = []
    if node_pos.shape[1] < 2:
        raise Exception("using first two axis as original position, there is only one filter")
    # todo: init some more robust way to draw network
    for edge in graph.edges:
        xs += [node_pos[edge[0], 0],
               node_pos[edge[1], 0],
               None]
        ys += [node_pos[edge[0], 1],
               node_pos[edge[1], 1],
               None]

    # if there are _color_SAFE, it will present two kinds of color. if simple != True
    # one is base on original data, one is transformed-SAFE data. Use the second one.
    if _color_SAFE is not None:
        safe_color, safe_t2c = _color_SAFE.get_colors(graph.nodes)
        # former is a dict which key is node id and values is node color
        # second is a tuple (node values, node color)
        target_SAFE_color = [safe_color[_] for _ in graph.nodes]
        target_SAFE_raw_v = safe_t2c[0].ravel()  # raw node values
    else:
        target_SAFE_color = []
        target_SAFE_raw_v = []

    # prepare node & samples text
    node_text = c_node_text(nodes,
                            sample_names,
                            target_v_raw)
    ### samples text
    samples_text = ['sample ID:%s' % _ for _ in sample_names]

    node_line = go.Scatter(
        # ordination line
        visible=False,
        x=xs,
        y=ys,
        marker=dict(color="#8E9DA2",
                    opacity=0.7),
        line=dict(width=1),
        hoverinfo='skip',
        showlegend=False,
        mode="lines")

    node_marker = go.Scatter(
        # node position
        visible=False,
        x=node_pos[:, 0],
        y=node_pos[:, 1],
        hovertext=node_text,
        hoverinfo="text",
        marker=dict(color=target_colors,
                    size=scaled_size,
                    opacity=1),
        showlegend=False,
        mode="markers")

    sample_marker = go.Scatter(
        visible=True,
        x=sample_pos[:, 0],
        y=sample_pos[:, 1],
        marker=dict(color=sample_colors),
        hovertext=samples_text,
        hoverinfo="text",
        showlegend=False,
        mode="markers")
    # After all prepared work have been finished.
    # Append all traces instance into fig
    if simple:
        fig = plotly.tools.make_subplots(1, 1)
        node_line['visible'] = True
        node_marker['visible'] = True
        fig.append_trace(node_line, 1, 1)

        if color is not None and type(color) != str:
            if color.dtype == 'numerical':
                # with continuous legend bar
                # A dict which includes values of node to color
                # For make continuous color legend
                nv2c = dict(zip(target_v,
                                target_colors))
                colorscale = []
                for _ in sorted(set(target_v)):
                    colorscale.append([_,
                                       nv2c[_]])
                colorscale[-1][0] = 1  # the last value must be 1
                colorscale[0][0] = 0  # the first value must be 0

                node_marker['marker']['color'] = target2colors[0].ravel()
                # it is not necessary to use target_v, it could use original data target2colors.
                # Or it will display normalized values which will confuse reader.
                node_marker['marker']['colorscale'] = colorscale
                node_marker['marker']['cmin'] = target2colors[0].min()
                node_marker['marker']['cmax'] = target2colors[0].max()
                node_marker['marker']['showscale'] = True
                fig.append_trace(node_marker, 1, 1)
            else:  # if color.dtype == 'categorical'
                for cat in np.unique(legend_names):
                    # it won't missing variables legend_names. check 434 line
                    # it will auto sort with alphabetic order
                    node_marker = go.Scatter(
                        # node position
                        visible=True,
                        x=node_pos[legend_names == cat, 0],
                        y=node_pos[legend_names == cat, 1],
                        text=np.array(node_text)[legend_names == cat],
                        hoverinfo="text",
                        marker=dict(color=cat2color[cat],
                                    size=scaled_size[legend_names == cat, 0],
                                    opacity=1),
                        name=str(cat),
                        showlegend=True,
                        mode="markers")
                    fig.append_trace(node_marker, 1, 1)
        elif type(color) == str:
            node_marker['marker']['color'] = color
            fig.append_trace(node_marker, 1, 1)
        else:
            fig.append_trace(node_marker, 1, 1)
        fig.layout.hovermode = "closest"
    else:
        fig = plotly.tools.make_subplots(rows=2,
                                         cols=2,
                                         specs=[[{'rowspan': 2}, {}],
                                                [None, {}]],
                                         )
        # original place or ordination place
        fig.append_trace(sample_marker, 1, 1)

        # dynamic process to generate 5 binning positions
        n_step = 5
        for s in range(1, n_step + 1):
            # s = 1: move 1/steps
            # s = steps: move to node position.
            fig.append_trace(go.Scatter(
                visible=False,
                x=duplicated_sample_pos[:, 0] + ((duplicated_node_pos - duplicated_sample_pos) / n_step * s)[:, 0],
                y=duplicated_sample_pos[:, 1] + ((duplicated_node_pos - duplicated_sample_pos) / n_step * s)[:, 1],
                marker=dict(color=duplicated_sample_colors),
                hoverinfo="text",
                hovertext=duplicated_samples_text,
                showlegend=False,
                mode="markers"), 1, 1)

        # Order is important, do not change the order !!!
        # There are the last 5 should be visible at any time
        fig.append_trace(node_line, 1, 1)
        fig.append_trace(node_marker, 1, 1)
        node_line['visible'] = True
        node_marker['visible'] = True
        sample_marker['visible'] = True
        fig.append_trace(node_line, 2, 2)
        if _color_SAFE is not None:
            node_text = c_node_text(nodes,
                                    sample_names,
                                    target_SAFE_raw_v)
            node_marker['hovertext'] = node_text
            node_marker['marker']['color'] = target_SAFE_color
        fig.append_trace(node_marker, 2, 2)
        fig.append_trace(sample_marker, 1, 2)
        ############################################################
        steps = []
        for i in range(n_step + 1):
            step = dict(
                method='restyle',
                args=['visible', [False] * (n_step + 3) + [True, True, True]],
            )
            if i >= n_step:
                step["args"][1][-5:] = [True] * 5  # The last 5 should be some traces must present at any time.
            else:
                step['args'][1][i] = True  # Toggle i'th trace to "visible"
            steps.append(step)

        sliders = [dict(
            active=0,
            currentvalue={"prefix": "status: "},
            pad={"t": 20},
            steps=steps
        )]
        ############################################################
        layout = dict(sliders=sliders,
                      width=2000,
                      height=1000,
                      xaxis1={  # "range": [0, 1],
                          "domain": [0, 0.5]},
                      yaxis1={  # "range": [0, 1],
                          "domain": [0, 1]},
                      xaxis2={  # "range": [0, 1],
                          "domain": [0.6, 0.9]},
                      yaxis2={  # "range": [0, 1],
                          "domain": [0.5, 1]},
                      xaxis3={  # "range": [0, 1],
                          "domain": [0.6, 0.9]},
                      yaxis3={  # "range": [0, 1],
                          "domain": [0, 0.5]},
                      hovermode="closest"
                      )
        fig.layout.update(layout)

    return write_figure(fig, mode, **kwargs)


def draw_enriched_plot(graph,
                       safe_score,
                       metainfo,
                       fea,
                       _filter_size=0,
                       mode='file',
                       **kwargs):
    """
    Draw simple node network which only show component which is larger than _filter_size and colorized with its safe_score.

    :param tmap.tda.Graph.Graph graph:
    :param pd.DataFrame safe_score:
    :param fea:
    :param metainfo:
    :param _filter_size:
    :param kwargs:
    :return:
    """

    enriched_nodes, comps_nodes = metainfo[fea]

    node_pos = graph.nodePos
    sizes = graph.size
    safe_score = safe_score.to_dict(orient='dict')

    fig = plotly.tools.make_subplots(1, 1)
    node_line = vis_progressX(graph, simple=True, mode='obj').data[0]
    fig.append_trace(node_line, 1, 1)

    for idx, nodes in enumerate(comps_nodes):
        if _filter_size:
            if len(nodes) <= _filter_size:
                continue

        tmp1 = {k: v if k in nodes else np.nan for k, v in safe_score[fea].items()}
        node_position = go.Scatter(
            # node position
            visible=True,
            x=node_pos[[k for k, v in safe_score[fea].items() if not np.isnan(tmp1[k])], 0],
            y=node_pos[[k for k, v in safe_score[fea].items() if not np.isnan(tmp1[k])], 1],
            hoverinfo="text",
            text=['node:%s,SAFE:%s' % (k, safe_score[fea][k]) for k, v in safe_score[fea].items() if not np.isnan(tmp1[k])],
            marker=dict(  # color=node_colors,
                size=[7 + sizes[_] for _ in [k for k, v in safe_score[fea].items() if not np.isnan(tmp1[k])]],
                opacity=0.8),
            showlegend=True,
            name='comps_%s' % idx,
            mode="markers")
        fig.append_trace(node_position, 1, 1)

    fig.layout.font.size = 15
    fig.layout.title = fea
    fig.layout.height = 1500
    fig.layout.width = 1500
    fig.layout.hovermode = 'closest'
    return write_figure(fig, mode, **kwargs)


def compare_draw(data,
                 graph,
                 fit_result,
                 safe_scores,
                 fea1,
                 fea2=None,
                 nr_threshold=0.5,
                 mode='obj',
                 **kwargs):
    if fea2 is not None:
        col = 2
        subtitles = ['%s ordination' % fea1,
                     '%s Tmap' % fea1,
                     '%s ordination' % fea2,
                     '%s Tmap' % fea2]
        feas = [fea1, fea2]
    else:
        col = 1
        subtitles = ['%s ordination' % fea1,
                     '%s Tmap' % fea1]
        feas = [fea1]

    fig = tools.make_subplots(2, col, subplot_titles=subtitles,
                              horizontal_spacing=0,
                              vertical_spacing=0)
    projected_X = graph.data

    def draw_ord_and_tmap(fig, fit_result, fea, row, col, data):
        if fea in data.columns:
            color = Color(data.loc[:, fea].astype(float), target_by='sample')
        else:
            raise Exception('Error occur, %s seem like a new feature for given data' % fea)

        fig.append_trace(go.Scatter(x=projected_X[:, 0],
                                    y=projected_X[:, 1],
                                    #                                      text=metadata.loc[:,fea],
                                    hoverinfo='text',
                                    mode='markers',
                                    marker=dict(color=color.get_sample_colors())
                                    , showlegend=False),
                         row, col)
        if fea in fit_result.index:
            fig.append_trace(go.Scatter(x=[0, fit_result.loc[fea, 'adj_Source']],
                                        y=[0, fit_result.loc[fea, 'adj_End']],
                                        mode='lines+text', showlegend=False,
                                        text=['', round(fit_result.loc[fea, 'r2'], 4)]), row, col)

    enriched_nodes = get_significant_nodes(graph=graph,
                                           safe_scores=safe_scores,
                                           nr_threshold=nr_threshold
                                           )  # todo

    fig_container = []
    for idx, fea in enumerate(feas):
        draw_ord_and_tmap(fig, projected_X, fit_result, fea, idx + 1, 1, data)
        cache = {node: safe_scores[fea][node] if node in enriched_nodes[fea] else 0 for node in safe_scores[fea].keys()}
        f = vis_progressX(graph,
                          color=Color(cache, target_by='node'),
                          mode='obj',
                          simple=True)
        fig_container.append(f)

    for idx, f in enumerate(fig_container):
        for _ in f.data:
            fig.append_trace(_,
                             idx + 1,
                             2)

    fig.layout.width = 2000
    fig.layout.height = 2000
    fig.layout.xaxis1.zeroline = False
    fig.layout.yaxis1.zeroline = False
    fig.layout.xaxis3.zeroline = False
    fig.layout.yaxis3.zeroline = False
    fig.layout.hovermode = 'closest'
    # showticklabels
    for _ in dir(fig.layout):
        if _.startswith('xaxis') or _.startswith('yaxis'):
            fig.layout[_]['showticklabels'] = False
    fig.layout.font.update(dict(size=20))
    for _ in fig.layout.annotations:
        _['font'].update(dict(size=25))

    return write_figure(fig, mode, **kwargs)
