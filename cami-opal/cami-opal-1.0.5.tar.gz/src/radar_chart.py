"""
======================================
Radar chart (aka spider or star chart)
======================================

This example creates a radar chart, also known as a spider or star chart [1]_.

Although this example allows a frame of either 'circle' or 'polygon', polygon
frames don't have proper gridlines (the lines are circles instead of polygons).
It's possible to get a polygon grid by setting GRIDLINE_INTERPOLATION_STEPS in
matplotlib.axis to the desired number of vertices, but the orientation of the
polygon is not aligned with the radial axes.

.. [1] http://en.wikipedia.org/wiki/Radar_chart
"""

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
from collections import OrderedDict
from src.utils import constants as c


def radar_factory(num_vars, frame='circle'):
    """Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarAxes(PolarAxes):

        name = 'radar'
        # use 1 line segment to connect specified points
        RESOLUTION = 1

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)
                return {'polar': spine}
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta


def example_data():
    # The following data is from the Denver Aerosol Sources and Health study.
    # See doi:10.1016/j.atmosenv.2008.12.017
    #
    # The data are pollution source profile estimates for five modeled
    # pollution sources (e.g., cars, wood-burning, etc) that emit 7-9 chemical
    # species. The radar charts are experimented with here to see if we can
    # nicely visualize how the modeled source profiles change across four
    # scenarios:
    #  1) No gas-phase species present, just seven particulate counts on
    #     Sulfate
    #     Nitrate
    #     Elemental Carbon (EC)
    #     Organic Carbon fraction 1 (OC)
    #     Organic Carbon fraction 2 (OC2)
    #     Organic Carbon fraction 3 (OC3)
    #     Pyrolized Organic Carbon (OP)
    #  2)Inclusion of gas-phase specie carbon monoxide (CO)
    #  3)Inclusion of gas-phase specie ozone (O3).
    #  4)Inclusion of both gas-phase species is present...
    # data = [
    #     ['Test'],
    #     ('Base', [
    #         [0.8065753617740602, 0.8232619881138277, 0.737810856077883, 1.0, 0.6798314936096235, 0.9206270157553685, 0.8213148449426132],
    #         [0.558151998251968, 0.7923767870943428, 0.43154988918633713, 1.0, 0.1792521879260715, 0.7571436986566638, 0.37614401060559277],
    #         [0.4166666666666667, 1.0, 0.9833333333333332, 0.5, 0.9166666666666666, 0.5333333333333334, 0.7500000000000001],
    #         [0.9333333333333333, 0.3192034139402561, 0.532034632034632, 1.0, 0.47427536231884054, 0.8278571428571428, 0.44585190597978325],
    #         [0.015625, 1.0, 0.40625, 0.0, 0.47656249999999994, 0.05468749999999999, 0.43749999999999994]
    #     ]),
    # ]

    data = [
        ('Base', [
            [.5,1.0,1.0,1.0,1.0,1.0,1.0],
            [1.0,1.0,1.0,1.0,1.0,1.0,1.0]
            # [0.4166666666666667, 1.0, 0.9833333333333332, 0.5, 0.9166666666666666, 0.5333333333333334, 0.7500000000000001],
            # [0.9333333333333333, 0.3192034139402561, 0.532034632034632, 1.0, 0.47427536231884054, 0.8278571428571428, 0.44585190597978325]
        ]),
    ]



    # data = [
    #     ['Sulfate', 'Nitrate', 'EC', 'OC1', 'OC2', 'OC3', 'OP', 'CO', 'O3'],
    #     ('Basecase', [
    #         [0.88, 0.01, 0.03, 0.03, 0.00, 0.06, 0.01, 0.00, 0.00],
    #         [0.07, 0.95, 0.04, 0.05, 0.00, 0.02, 0.01, 0.00, 0.00],
    #         [0.01, 0.02, 0.85, 0.19, 0.05, 0.10, 0.00, 0.00, 0.00],
    #         [0.02, 0.01, 0.07, 0.01, 0.21, 0.12, 0.98, 0.00, 0.00],
    #         [0.01, 0.01, 0.02, 0.71, 0.74, 0.70, 0.00, 0.00, 0.00]]),
    #     ('With CO', [
    #         [0.88, 0.02, 0.02, 0.02, 0.00, 0.05, 0.00, 0.05, 0.00],
    #         [0.08, 0.94, 0.04, 0.02, 0.00, 0.01, 0.12, 0.04, 0.00],
    #         [0.01, 0.01, 0.79, 0.10, 0.00, 0.05, 0.00, 0.31, 0.00],
    #         [0.00, 0.02, 0.03, 0.38, 0.31, 0.31, 0.00, 0.59, 0.00],
    #         [0.02, 0.02, 0.11, 0.47, 0.69, 0.58, 0.88, 0.00, 0.00]]),
    #     ('With O3', [
    #         [0.89, 0.01, 0.07, 0.00, 0.00, 0.05, 0.00, 0.00, 0.03],
    #         [0.07, 0.95, 0.05, 0.04, 0.00, 0.02, 0.12, 0.00, 0.00],
    #         [0.01, 0.02, 0.86, 0.27, 0.16, 0.19, 0.00, 0.00, 0.00],
    #         [0.01, 0.03, 0.00, 0.32, 0.29, 0.27, 0.00, 0.00, 0.95],
    #         [0.02, 0.00, 0.03, 0.37, 0.56, 0.47, 0.87, 0.00, 0.00]]),
    #     ('CO & O3', [
    #         [0.87, 0.01, 0.08, 0.00, 0.00, 0.04, 0.00, 0.00, 0.01],
    #         [0.09, 0.95, 0.02, 0.03, 0.00, 0.01, 0.13, 0.06, 0.00],
    #         [0.01, 0.02, 0.71, 0.24, 0.13, 0.16, 0.00, 0.50, 0.00],
    #         [0.01, 0.03, 0.00, 0.28, 0.24, 0.23, 0.00, 0.44, 0.88],
    #         [0.02, 0.00, 0.18, 0.45, 0.64, 0.55, 0.86, 0.00, 0.16]])
    # ]
    return data


# if __name__ == '__main__':
# # def x():
#     N = 7
#     theta = radar_factory(N, frame='polygon')
#
#     data = example_data()
#     # spoke_labels = data.pop(0)
#     spoke_labels = ['CommonKmers', 'Quikr', 'TIPP', 'MP2.0', 'MetaPhyler', 'mOTU', 'FOCUS']
#
#     fig, axes = plt.subplots(figsize=(9, 9), nrows=2, ncols=2,
#                              subplot_kw=dict(projection='radar'))
#     fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)
#
#     colors = ['b', 'r', 'g', 'm', 'y']
#     # Plot the four cases from the example data on separate axes
#     for ax, (title, case_data) in zip(axes.flat, data):
#         ax.set_rgrids([0.2, 0.4, 0.6, 0.8])
#         ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1),
#                      horizontalalignment='center', verticalalignment='center')
#         for d, color in zip(case_data, colors):
#             ax.plot(theta, d, color=color)
#             ax.fill(theta, d, facecolor=color, alpha=0.25)
#     ax.set_varlabels(spoke_labels)
#
#     # add legend relative to top-left plot
#     ax = axes[0, 0]
#     # labels = ('Factor 1', 'Factor 2', 'Factor 3', 'Factor 4', 'Factor 5')
#     labels = ['Completeness (recall)', 'Purity (precision)']
#     legend = ax.legend(labels, loc=(0.9, .95),
#                        labelspacing=0.1, fontsize='small')
#
#     fig.text(0.5, 0.965, '5-Factor Solution Profiles Across Four Scenarios',
#              horizontalalignment='center', color='black', weight='bold',
#              size='large')
#
#     plt.show()


def spider_plot(metrics, labels, rank_to_metric_to_toolvalues, colors, grid_points=None, fill=False, absolute=False):
    N = len(labels)
    if N < 3:
        return []
    theta = radar_factory(N, frame='polygon')
    fig, axes = plt.subplots(figsize=(9, 9), nrows=2, ncols=3, subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(wspace=0.35, hspace=0.05, top=0.87, bottom=0.3)

    for ax, rank in zip(axes.flat, c.PHYLUM_SPECIES):
        # print(rank)
        if grid_points:
            ax.set_rgrids(grid_points, fontsize='xx-small')
        else:
            ax.set_rgrids([0.2, 0.4, 0.6, 0.8], ('', '', '', ''))  # get rid of the labels of the grid points
        ax.set_title(rank, weight='bold', size='medium', position=(0.5, 1.1),
                     horizontalalignment='center', verticalalignment='center')

        if absolute:
            metric_suffix = 'absolute'
        else:
            metric_suffix = ''
        # select only metrics in metrics list
        metrics_subdict = OrderedDict((metric, rank_to_metric_to_toolvalues[rank][metric + metric_suffix]) for metric in metrics)
        # print(metrics_subdict)
        # print(metrics_subdict.values())
        # print()
        it = 1
        metric_to_toolindex = []
        for d, color in zip(metrics_subdict.values(), colors):
            # store index of tools without a value for the current metric
            metric_to_toolindex.append([i for i, x in enumerate(d) if x is None or np.isnan(x)])
            d = [0.0 if x is None or np.isnan(x) else x for x in d]

            ax.plot(theta, d, '--', color=color, linewidth=3, dashes=(it, 1))
            if fill:
                ax.fill(theta, d, facecolor=color, alpha=0.25)
            it += 1
        # print(labels)
        ax.set_varlabels(labels)
        # xticklabels = ax.get_xticklabels()
        # print(xticklabels)

        # print(ax.get_rlabel_position())
        # ax.set_rlabel_position(-30)
        # print(ax.get_rlabel_position())

        # ax.set_ylim([0.0, 1.0])
        # ax.set_xlim([0.0, 1.0])
        ax.set_rmax(1)
        # print(str(ax.get_xlim()) + " " + str(ax.get_ylim()))

        # color red label of tools without a value for at least one metric
        xticklabels = ax.get_xticklabels()
        # print(xticklabels[2].get_position())

        for xticklabel in xticklabels:
            xticklabel.set_position((.1,.1))
            xticklabel.set_fontsize('small')

        for metric in metric_to_toolindex:
            for toolindex in metric:
                xticklabels[toolindex].set_color([1, 0, 0])

    # print(metrics)
    ax = axes[0, 0]
    ax.legend(metrics, loc=(1.6 - 0.353 * len(metrics), 1.3), labelspacing=0.1, fontsize='small', ncol=len(metrics))
    # fig.savefig(os.path.join(output_dir, file_name + '.pdf'), dpi=100, format='pdf', bbox_inches='tight')
    # fig.savefig(os.path.join(output_dir, file_name + '.png'), dpi=100, format='png', bbox_inches='tight')
    # plt.close(fig)
    plt.show()


if __name__ == '__main__':
    metrics = ['Completeness (recall)', 'Purity (precision)']
    labels = ['CommonKmers', 'Quikr', 'TIPP', 'MP2.0', 'MetaPhyler', 'mOTU', 'FOCUS']
    rank_to_metric_to_toolvalues = {'phylum': {'L1 norm error': [0.558151998251968, 0.7923767870943429, 0.43154988918633713, 1.0, 0.1792521879260715, 0.7571436986566638, 0.37614401060559277], 'Completeness (recall)': [0.4166666666666667, 1.0, 0.9833333333333332, 0.5, 0.9166666666666666, 0.5333333333333334, 0.7500000000000001], 'Purity (precision)': [0.9333333333333333, 0.3192034139402561, 0.532034632034632, 1.0, 0.47427536231884054, 0.8278571428571428, 0.44585190597978325], 'False positives': [0.015625, 1.0, 0.40625, 0.0, 0.47656249999999994, 0.05468749999999999, 0.43749999999999994], 'Completeness (recall)absolute': [0.4166666666666667, 1.0, 0.9833333333333332, 0.5, 0.9166666666666666, 0.5333333333333334, 0.7500000000000001], 'Purity (precision)absolute': [0.9333333333333333, 0.3192034139402561, 0.532034632034632, 1.0, 0.47427536231884054, 0.8278571428571428, 0.44585190597978325], 'Weighted UniFrac error': [0.8065753617740599, 0.8232619881138276, 0.737810856077883, 1.0, 0.6798314936096236, 0.9206270157553682, 0.8213148449426126]}, 'class': {'L1 norm error': [0.43610852091113095, 0.47689504140457795, 0.39489425740810974, 1.0, 0.22432019276642937, 0.6363174697810569, 0.34220457512416974], 'Completeness (recall)': [0.5142857142857142, 1.0, 0.9904761904761905, 0.7047619047619047, 0.9523809523809523, 0.6952380952380952, 0.8285714285714285], 'Purity (precision)': [1.0, 0.3881787080391499, 0.4599843695173691, 0.9112576064908723, 0.40111988742246313, 0.8477100459058396, 0.6180566930288844], 'False positives': [0.011428571428571429, 1.0, 0.7428571428571429, 0.05714285714285714, 0.9028571428571429, 0.09142857142857143, 0.3371428571428572], 'Completeness (recall)absolute': [0.5142857142857142, 1.0, 0.9904761904761905, 0.7047619047619047, 0.9523809523809523, 0.6952380952380952, 0.8285714285714285], 'Purity (precision)absolute': [0.9666666666666666, 0.3752394177711782, 0.4446515572001234, 0.8808823529411764, 0.387749224508381, 0.8194530443756449, 0.5974548032612549], 'Weighted UniFrac error': [0.8065753617740599, 0.8232619881138276, 0.737810856077883, 1.0, 0.6798314936096236, 0.9206270157553682, 0.8213148449426126]}, 'order': {'L1 norm error': [0.5035977517142916, 0.574706031578084, 0.7257362565301337, 1.0, 0.6041954682820021, 0.9542914348127273, 0.4167512866364307], 'Completeness (recall)': [0.5349999999999999, 1.0, 0.9949999999999999, 0.675, 0.975, 0.72, 0.78], 'Purity (precision)': [1.0, 0.3609491097631057, 0.3749318113972444, 0.775918328200369, 0.32902709701776867, 0.5754005536908893, 0.5564411987578004], 'False positives': [0.004901960784313726, 0.8921568627450981, 0.8357843137254903, 0.10294117647058824, 1.0, 0.2720588235294118, 0.31617647058823534], 'Completeness (recall)absolute': [0.5349999999999999, 1.0, 0.9949999999999999, 0.675, 0.975, 0.72, 0.78], 'Purity (precision)absolute': [0.9829710144927535, 0.35480251260409623, 0.3685471030147551, 0.762705226234638, 0.3234240993511617, 0.5656020660012255, 0.546965569648519], 'Weighted UniFrac error': [0.8065753617740599, 0.8232619881138276, 0.737810856077883, 1.0, 0.6798314936096236, 0.9206270157553682, 0.8213148449426126]}, 'family': {'L1 norm error': [0.7439130615101096, 0.7856958115592245, 0.4096213063871006, 1.0, 0.3561926172695886, 0.8142037510420729, 0.6342988784052365], 'Completeness (recall)': [0.49014778325123165, 0.9926108374384236, 1.0, 0.6206896551724139, 0.9975369458128078, 0.7339901477832513, 0.704433497536946], 'Purity (precision)': [1.0, 0.37965699165558203, 0.4031661304240073, 0.8789862663276582, 0.3336367112050077, 0.6051503773901149, 0.5545064730725786], 'False positives': [0.008215962441314553, 0.818075117370892, 0.7476525821596244, 0.0528169014084507, 1.0, 0.2488262910798122, 0.29107981220657275], 'Completeness (recall)absolute': [0.4522727272727273, 0.9159090909090908, 0.9227272727272726, 0.5727272727272728, 0.9204545454545453, 0.6772727272727272, 0.65], 'Purity (precision)absolute': [0.9657486287781538, 0.3666532190974173, 0.38935713762677937, 0.848879781420765, 0.3222091963562891, 0.5844231471690857, 0.5355138660184531], 'Weighted UniFrac error': [0.8065753617740599, 0.8232619881138276, 0.737810856077883, 1.0, 0.6798314936096236, 0.9206270157553682, 0.8213148449426126]}, 'genus': {'L1 norm error': [0.7930859500230144, 0.9939057088615595, 0.7956575142251343, 1.0, 0.7498821202099898, 0.9278389966231845, 0.8890892197521735], 'Completeness (recall)': [0.4539130434782608, 1.0, 0.7269565217391306, 0.5304347826086956, 0.7286956521739132, 0.5669565217391305, 0.4156521739130435], 'Purity (precision)': [1.0, 0.24079463582169836, 0.2497915638563291, 0.9854530997310924, 0.18917825071280095, 0.39633729824401476, 0.3429826944332572], 'False positives': [0.03056768558951965, 1.0, 0.6943231441048034, 0.038110361254466055, 0.9722111949186185, 0.2933703850734419, 0.26399364827312427], 'Completeness (recall)absolute': [0.26907216494845354, 0.5927835051546392, 0.43092783505154647, 0.31443298969072164, 0.431958762886598, 0.33608247422680415, 0.2463917525773196], 'Purity (precision)absolute': [0.7722845439893999, 0.18596197552065394, 0.1929101639851842, 0.7610501977487674, 0.14609943908444786, 0.30608516964036975, 0.2648802337666437], 'Weighted UniFrac error': [0.8065753617740599, 0.8232619881138276, 0.737810856077883, 1.0, 0.6798314936096236, 0.9206270157553682, 0.8213148449426126]}, 'species': {'L1 norm error': [0.8964336978362055, 0.9701946592545329, 0.9649482346940671, 0.9471385029456892, 0.9701898762425502, 0.9743127557219444, 1.0], 'Completeness (recall)': [0.5, 1.0, 0.11363636363636365, 0.10795454545454547, 0.11363636363636365, 0.07386363636363637, 0.011363636363636366], 'Purity (precision)': [1.0, 0.40229480767900533, 0.06431149754479291, 0.9057495107267007, 0.03709641447265344, 0.07458206071557193, 0.01859035468189624], 'False positives': [0.15037707390648566, 0.7877828054298642, 0.5755656108597286, 0.03619909502262444, 1.0, 0.3220211161387632, 0.20301659125188537], 'Completeness (recall)absolute': [0.07302904564315352, 0.14605809128630703, 0.016597510373443983, 0.015767634854771784, 0.016597510373443983, 0.010788381742738589, 0.0016597510373443983], 'Purity (precision)absolute': [0.0810763525008136, 0.03261659563663005, 0.005214141644796839, 0.07343486660911744, 0.003007641976301134, 0.0060468414448127915, 0.0015072381493045702], 'Weighted UniFrac error': [0.8065753617740599, 0.8232619881138276, 0.737810856077883, 1.0, 0.6798314936096236, 0.9206270157553682, 0.8213148449426126]}}
    colors = ['r', 'k']
    grid_points = [0.2, 0.4, 0.6, 0.8, 1.0]
    fill = True
    absolute = True
    spider_plot(metrics, labels, rank_to_metric_to_toolvalues, colors, grid_points, fill, absolute)
