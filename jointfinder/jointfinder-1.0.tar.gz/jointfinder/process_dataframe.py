import pandas as pd
import numpy as np
import concurrent.futures
import sys
import warnings
from sklearn.cluster import KMeans
from tqdm import tqdm
from copy import deepcopy
from itertools import chain, combinations, zip_longest
from operator import itemgetter
from numba import vectorize, float64
from math import asin, acos, sin, cos, tan, floor, sqrt, copysign, ceil, isclose, degrees, radians
from statistics import mean
from pandas.core.groupby.groupby import DataError
# np.seterr(divide='ignore', invalid='ignore')


class ProcessDataframeXML:
    """
    Process every line from every part if the line bounded by a group of boundary lines (on a plane px py pz)
    Class returns pandas dataframe with t (ratio of line length)
    xml_df must contain these columns/parameters in strict sequence:
    part        <<< str     : unique panel_part|direction(px|py|pz)|segment
    nr_segment  <<< str     : running number of shape on same plane, 0 is base, others are cutouts
    is_edge     <<< bool    : True if line is weldable, may sit on a surface on other plane
    sp          <<< float   : 1.0 is shell part, 0.0 non-shell
    end_x       <<< float   : x0
    end_y       <<< float   : y0
    end_z       <<< float   : z0
    x_start     <<< float   : x1
    y_start     <<< float   : y1
    z_start     <<< float   : z1
    px          <<< float   : plane x value
    py          <<< float   : plane y value
    pz          <<< float   : plane x value
    thickness   <<< float   : tolerance offset of px py pz
    Define column names in order as above if different, otherwise default None
    Desired output df must follow this sequence:
    combo       <<< tuple   : of strings, sorted
    order       <<< bool    : if False, combo is reversed - left: line, right: bounds
    segment     <<< int     : 0 is base, others cutouts for shapes on same plane
    edge        <<< tuple   : ((x0, y0, z0), (x1, y1, z1))
    length      <<< float   : euclidean distance of edge
    joint       <<< str     : T-Joint or Butt_Joint
    t           <<< float   : clean length as the factor of length
    """

    def __init__(self, xml_df, tolerance, arc_res, input_column_names=None, output_column_names=None):
        in_columns = 'part', 'nr_segments', 'is_edge', 'sp', 'end_x', 'end_y', 'end_z', 'x_start', 'y_start', 'z_start', 'px', 'py', 'pz', 'thickness'
        out_columns = 'combo', 'order', 'segment', 'edge', 'length', 'joint', 't'
        self.is_exit = False, None
        # start of constructor -----------------------------------------------------------------------------------------
        self.xmldf = deepcopy(xml_df)   # XML dataframe, deepcopy so that does not screw up the original
        self.tol = tolerance            # maximum gap allowed
        self.res = arc_res              # minimum angle of linearized circular section
        self.in_columns = self._check_column_names('input_column_names', input_column_names, in_columns)
        # end of constructor -------------------------------------------------------------------------------------------
        if self.in_columns is not None:
            self.part, self.nr_segment, self.is_edge = self.in_columns[:3]
            self.px, self.py, self.pz, self.thickness = self.in_columns[10:]
            self.ab_columns = self.in_columns[3:10]
            self.sp, self.end_x, self.end_y, self.end_z, self.x_start, self.y_start, self.z_start = self.ab_columns
        else:
            self.is_exit = True, 'Invalid input columns'
        out_columns = self._check_column_names('output_column_names', output_column_names, out_columns)
        if out_columns is not None:
            self.COMBO, self.ORDER, self.SEGMENT, self.EDGE, self.LENGTH, self.JOINT, self.T = out_columns
        else:
            self.is_exit = True, 'Invalid output columns'
        if not self.is_exit[0]:
            # purge unnecessary columns
            self.xmldf = self.xmldf.loc[:, self.in_columns]
            # test input df for correct types
            for ct in zip(self.in_columns, [str, str, bool, float, float, float, float, float, float, float, float, float, float, float]):
                self.xmldf = self._cast_to_type(self.xmldf, *ct)
            self.parts = self.xmldf[self.xmldf.is_edge].part.unique()  # consider only shapes that on the edge
            # class constants, lowercase is externally assigned, uppercase internally
            self.NO_JOINT_ERRMSG = 'Unable to find any joint'
            self.BJ, self.TJ = 'Butt_Joint', 'T-Joint'
            self.MAX_T = 'max_t'

    @classmethod
    def _check_column_names(cls, arg, column_names, default_columns):
        if column_names is None:
            return default_columns
        else:
            try:
                if type(column_names) not in [set, list, tuple]:
                    raise ValueError
                if len(column_names) != len(default_columns):
                    raise ValueError
                if any(map(lambda each: each != str, map(type, column_names))):
                    raise ValueError
                return column_names
            except ValueError:
                print(f'Argument {arg} requires set/list/tuple of strings with length of {len(default_columns)}')
                return None

    def _cast_to_type(self, df, column, check_type):
        try:
            df[column] = df[column].astype(check_type)
        except ValueError:
            self.is_exit = True, f'Column type error: {column}, while casting to {check_type}'
        return df

    @staticmethod
    # ab is line to test, cd is the bound, p is cd plane/direction vector
    @vectorize([float64(float64, float64, float64, float64, float64, float64,
                        float64, float64, float64, float64, float64, float64,
                        float64, float64, float64, float64,
                        float64, float64, float64, float64,
                        float64)], target='parallel')
    def _tee(ax, ay, az, bx, by, bz,
             cx, cy, cz, dx, dy, dz,
             px, py, pz, thickness,
             tolerance, lpt, ppt, pie,
             el):
        # thickness applies to both directions of plane
        # return code -1 is for true parallel
        # return code -10s are division by zero
        # return code -100s are parallel rejects
        # return code -1000s are not found
        # el 0 = tab
        # el 1 = near
        # el 2 = far
        # el 3 = side

        # filter invalid vectors
        plane_mag = sqrt(px ** 2 + py ** 2 + pz ** 2)
        if plane_mag == 0:
            return -11
        # create ab and cd vectors and its mags
        abx, aby, abz = bx - ax, by - ay, bz - az
        cdx, cdy, cdz = dx - cx, dy - cy, dz - cz
        cd_mag = sqrt(cdx ** 2 + cdy ** 2 + cdz ** 2)
        ab_mag = sqrt(abx ** 2 + aby ** 2 + abz ** 2)
        # avoid division by zero, a == b, c == d, point not line, reject
        if cd_mag == 0 or ab_mag == 0:
            return -12

        # reject ab not parallel to plane (cd's)
        p_ab_theta = (180 / pie) * acos((px * abx + py * aby + pz * abz) / (plane_mag * ab_mag))
        if abs(90 - p_ab_theta) > ppt:
            return -101
        # d is "offset" for line equation: ax + by + cz + d = 0
        d = (cx + px * thickness) * px + (cy + py * thickness) * py + (cz + pz * thickness) * pz
        plane_to_a, plane_to_b = (px * ax + py * ay + pz * az) - d, (px * bx + py * by + pz * bz) - d
        # check if ab is within cd plane thickness (+tolerance)
        if abs(plane_to_a) > tolerance + thickness and abs(plane_to_b) > tolerance + thickness:
            # both a AND b away from cd plane
            if copysign(1, plane_to_a) * copysign(1, plane_to_b) > 0:
                # not cutting plane cd
                return -102

        # find ab cd angle (range: 0 ~ 90)
        is_parallel, is_far_parallel = False, False
        # U . V = |U| * |V| * cos(theta)
        for_acos = (abx * cdx + aby * cdy + abz * cdz) / (ab_mag * cd_mag)
        # to avoid cos figure larger than 1 or -1, otherwise math domain error
        if abs(for_acos) > 1:
            for_acos = copysign(1, for_acos)
        ab_cd_theta = (180 / pie) * acos(for_acos)
        if ab_cd_theta > 90:
            ab_cd_theta = 180 - ab_cd_theta
        # line parallel check
        if ab_cd_theta < lpt:
            ux, uy, uz = abx / ab_mag, aby / ab_mag, abz / ab_mag
            # ac has its c factored with thickness's middle
            acx = (cx + (px * thickness)) - ax
            acy = (cy + (py * thickness)) - ay
            acz = (cz + (pz * thickness)) - az
            u_cross_ac_x = uy * acz - uz * acy
            u_cross_ac_y = ux * acz - uz * acx
            u_cross_ac_z = ux * acy - uy * acx
            if sqrt(u_cross_ac_x ** 2 + u_cross_ac_y ** 2 + u_cross_ac_z ** 2) <= tolerance + thickness:
                # ab parallel and near cd, maybe butt joint, check if they overlap
                a_dot_cd, b_dot_cd = ax * cdx + ay * cdy + az * cdz, bx * cdx + by * cdy + bz * cdz
                c_dot_cd, d_dot_cd = cx * cdx + cy * cdy + cz * cdz, dx * cdx + dy * cdy + dz * cdz
                seq_abcd = sorted([a_dot_cd, b_dot_cd, c_dot_cd, d_dot_cd])
                seq_ab = sorted([a_dot_cd, b_dot_cd])
                if seq_abcd[:2] == seq_ab or seq_abcd[2:] == seq_ab:
                    return -103
                else:
                    # ab and cd parallel, overlap and near (distance within tolerance)
                    is_parallel = True
            else:
                is_far_parallel = True
        if el == 0:
            if is_parallel:
                # if parallel, there is no tab
                return -1
            elif is_far_parallel:
                return -104

        # near and far range for side boundaries
        uabx, uaby, uabz = abx / ab_mag, aby / ab_mag, abz / ab_mag
        ab_dot_c, ab_dot_d = uabx * cx + uaby * cy + uabz * cz, uabx * dx + uaby * dy + uabz * dz
        ab_dot_a, ab_dot_b = uabx * ax + uaby * ay + uabz * az, uabx * bx + uaby * by + uabz * bz
        if 1 <= el <= 3:
            if (ab_dot_c <= ab_dot_a and ab_dot_d <= ab_dot_a) or (ab_dot_c >= ab_dot_b and ab_dot_d >= ab_dot_b):
                # c and d are before a OR c and d are after b
                near, far = -1001, -1002
                if el == 3:
                    return -10001
            else:
                # near and far from point a
                if ab_dot_c < ab_dot_d:
                    near, far = ab_dot_c - ab_dot_a, ab_dot_d - ab_dot_a
                else:
                    near, far = ab_dot_d - ab_dot_a, ab_dot_c - ab_dot_a
                ab_span = abs(ab_dot_b - ab_dot_a)
                near, far = near / ab_span, far / ab_span
                if near < 0:
                    near = 0
                if far > 1:
                    far = 1
            if el == 1:
                return near
            elif el == 2:
                return far
            else:
                if far - near != 0 and is_parallel:
                    # side is cross if far - near != 0
                    return 10

        # determine offsets from ab surface (plane and ab)
        # |U x V| = |U|*|V|*sin(theta)
        # cross of plane (parallel with abxcd) with ab (ab now have left right on cd's plane), unit vector
        p_cross_ab_x = py * abz - pz * aby
        p_cross_ab_y = pz * abx - px * abz
        p_cross_ab_z = px * aby - py * abx
        # cd plane (p) cross ab is vector RIGHT of ab on cd plane (p)
        p_cross_ab_mag = sqrt(p_cross_ab_x ** 2 + p_cross_ab_y ** 2 + p_cross_ab_z ** 2)
        # avoid division by zero
        if p_cross_ab_mag == 0:
            return -13
        # pab is unit vector,
        p_cross_ab_x /= p_cross_ab_mag
        p_cross_ab_y /= p_cross_ab_mag
        p_cross_ab_z /= p_cross_ab_mag
        # dot product for offsets
        a_offset_from_pab = p_cross_ab_x * ax + p_cross_ab_y * ay + p_cross_ab_z * az
        # a and b offsets have the same value, c and d offset NOT the same value if not parallel to ab
        c_offset_from_pab = p_cross_ab_x * cx + p_cross_ab_y * cy + p_cross_ab_z * cz
        d_offset_from_pab = p_cross_ab_x * dx + p_cross_ab_y * dy + p_cross_ab_z * dz
        # those offsets are not applied inversion corrections

        # c and d points neither before or after ab vector
        if el == 3.0:
            if c_offset_from_pab - a_offset_from_pab < 0 and d_offset_from_pab - a_offset_from_pab < 0:
                # both c and d on the left of pab plane
                is_left = True
            elif c_offset_from_pab - a_offset_from_pab > 0 and d_offset_from_pab - a_offset_from_pab > 0:
                # both c and d on the right of pab plane
                is_left = False
            else:
                is_left = None
            if is_left is not None:
                return 11 if not is_left else 12

        # if cd perpendicular ab, pab_dot_cd is cd full projection
        pab_dot_cd = p_cross_ab_x * cdx + p_cross_ab_y * cdy + p_cross_ab_z * cdz
        if pab_dot_cd == 0:
            return -14
        # part of cd touching ab
        tcd = (a_offset_from_pab - c_offset_from_pab) / pab_dot_cd
        sin_ab_cd_theta = sin(pie * ab_cd_theta / 180)
        if sin_ab_cd_theta == 0:
            return -15
        allow_excess = tolerance / sin_ab_cd_theta
        lim = allow_excess / cd_mag
        if not (-lim <= tcd <= (1 + lim)) and el == 0:
            return -100001

        # intersection and tab
        intersection_pt_x = cx + tcd * cdx
        intersection_pt_y = cy + tcd * cdy
        intersection_pt_z = cz + tcd * cdz
        # vector a to intersection
        aix = intersection_pt_x - ax
        aiy = intersection_pt_y - ay
        aiz = intersection_pt_z - az
        ai_mag = sqrt(aix ** 2 + aiy ** 2 + aiz ** 2)
        if ai_mag == 0:
            tab = 0
        # check if intersection is behind vector ab, or at a
        elif (aix * abx + aiy * aby + aiz * abz) / (ab_mag * ai_mag) <= 0:
            tab = 0
        else:
            tab = ai_mag / ab_mag

        # check for cross before normalizing tab
        if el == 3.0 and 0 <= tab <= 1:
            return 10
        # normalizing tab
        if el == 0:
            if tab <= 0:
                tab = 0
            elif tab >= 1:
                tab = 1
            return tab

        # final check for side
        if el == 3.0:
            if ab_dot_a <= ab_dot_c <= ab_dot_b and not ab_dot_a <= ab_dot_d <= ab_dot_b:
                c_or_d = c_offset_from_pab
            elif not ab_dot_a <= ab_dot_c <= ab_dot_b and ab_dot_a <= ab_dot_d <= ab_dot_b:
                c_or_d = d_offset_from_pab
            else:
                ab_dot_i = uabx * intersection_pt_x + uaby * intersection_pt_y + uabz * intersection_pt_z
                if (ab_dot_c <= ab_dot_a and ab_dot_i <= ab_dot_a) or (ab_dot_c >= ab_dot_b and ab_dot_i >= ab_dot_b):
                    c_or_d = d_offset_from_pab
                elif (ab_dot_d <= ab_dot_a and ab_dot_i <= ab_dot_a) or (ab_dot_d >= ab_dot_b and ab_dot_i >= ab_dot_b):
                    c_or_d = c_offset_from_pab
                else:
                    c_or_d = None
            if c_or_d is None:
                return 10
            elif c_or_d - a_offset_from_pab > 0:
                return 11
            elif c_or_d - a_offset_from_pab < 0:
                return 12
            else:
                return -10002

        return -1000001

    def _make_df_by_part(self, ldf, part):
        ndf = []
        ldf['part_ab'] = part
        ab = self.xmldf[(self.xmldf.part == part)][[*self.ab_columns]].values
        filler = ldf[(ldf.keep == False)].shape[0] * [-10000]

        def chunks(l, n):
            for i in range(0, len(l), n):
                yield l[i: i + n]

        def line_executor(eab, tdf):
            # rename line end and start as a and b
            # is_edge, block and sp as well
            tdf['sp_ab'], tdf['ax'], tdf['ay'], tdf['az'], tdf['bx'], tdf['by'], tdf['bz'] = eab.copy()
            tdf['tol'], tdf['res'], tdf['pi'] = self.tol, self.res, np.pi

            # 10 deg if 0.175
            arc_res_deg = 180 * self.res / np.pi
            # this will determine butt joint
            lpt = (arc_res_deg * (1 / 2)) if tdf.sp.values[0] + tdf.sp_ab.values[0] > 0.5 else (arc_res_deg * (1 / 3))
            # if arg_res_deg == 10, shell is 45 deg else 10
            ppt = (arc_res_deg * 4.5) if tdf.sp.values[0] + tdf.sp_ab.values[0] > 0.5 else (arc_res_deg * (1 / 3))

            tdf['lpt'], tdf['ppt'] = lpt, ppt

            elements_column = self._tee(
                np.ascontiguousarray(tdf.ax.values.astype(float)),
                np.ascontiguousarray(tdf.ay.values.astype(float)),
                np.ascontiguousarray(tdf.az.values.astype(float)),
                np.ascontiguousarray(tdf.bx.values.astype(float)),
                np.ascontiguousarray(tdf.by.values.astype(float)),
                np.ascontiguousarray(tdf.bz.values.astype(float)),
                np.ascontiguousarray(tdf[self.end_x].values.astype(float)),
                np.ascontiguousarray(tdf[self.end_y].values.astype(float)),
                np.ascontiguousarray(tdf[self.end_z].values.astype(float)),
                np.ascontiguousarray(tdf[self.x_start].values.astype(float)),
                np.ascontiguousarray(tdf[self.y_start].values.astype(float)),
                np.ascontiguousarray(tdf[self.z_start].values.astype(float)),
                np.ascontiguousarray(tdf[self.px].values.astype(float)),
                np.ascontiguousarray(tdf[self.py].values.astype(float)),
                np.ascontiguousarray(tdf[self.pz].values.astype(float)),
                np.ascontiguousarray(tdf[self.thickness].values.astype(float)),
                np.ascontiguousarray(tdf.tol.values.astype(float)),
                np.ascontiguousarray(tdf['lpt'].values.astype(float)),
                np.ascontiguousarray(tdf['ppt'].values.astype(float)),
                np.ascontiguousarray(tdf.pi.values.astype(float)),
                np.ascontiguousarray(tdf.el.values.astype(float)),
            )
            elements_column = chunks(elements_column, self.xmldf.keep.shape[0])
            for el in [self.T, 'near', 'far', 'side']:
                tdf[el] = pd.Series(next(elements_column).tolist() + filler, index=tdf.index)
            # accept if sequentially not a repeat figure
            # tdf = tdf.loc[tdf[self.T].shift() != tdf[self.T]]
            return tdf[(tdf.keep == True) & ((tdf[self.T] >= -1) | (tdf.near >= 0) | (tdf.far >= 0) | (tdf.side >= 0))]

        # wfle = []
        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     for every_ab in ab:
        #         wfle.append(executor.submit(line_executor, every_ab, ldf))
        #     wfle = concurrent.futures.as_completed(wfle)
        #     for fle in wfle:
        #         ndf.append(fle.result())
        for every_ab in ab:
            ndf.append(line_executor(every_ab, ldf))
        ndf = pd.concat(ndf, sort=False, ignore_index=True).reset_index(drop=True)

        ndf[self.sp] = ndf[self.sp].transform(lambda cell: True if cell > 0.0 else False)
        ndf['sp_ab'] = ndf['sp_ab'].transform(lambda cell: True if cell > 0.0 else False)
        ndf[self.sp] = ndf.loc[:, (self.sp, 'sp_ab')].apply(np.any, axis=1)
        ndf[self.COMBO] = ndf.loc[:, ('part_ab', self.part)].apply(sorted, axis=1)
        ndf[self.COMBO] = ndf[self.COMBO].transform(tuple)
        ndf[self.ORDER] = ndf[self.COMBO].transform(itemgetter(0))
        ndf[self.ORDER] = ndf.loc[:, ('part_ab', self.ORDER)].apply(set, axis=1)
        ndf[self.ORDER] = ndf[self.ORDER].transform(lambda cell: True if len(cell) == 1 else False).astype(bool)
        ndf['edge1'] = ndf.loc[:, ('ax', 'ay', 'az')].apply(tuple, axis=1)
        ndf['edge2'] = ndf.loc[:, ('bx', 'by', 'bz')].apply(tuple, axis=1)
        ndf[self.EDGE] = ndf.loc[:, ('edge1', 'edge2')].apply(tuple, axis=1)
        # ndf[self.EDGE] = ndf.loc[:, ('part_ab', self.EDGE)].apply(tuple, axis=1)
        ndf['edge1'] = ndf['edge1'].transform(np.array)
        ndf['edge2'] = ndf['edge2'].apply(lambda x: -1 * np.array(x))
        ndf[self.SEGMENT] = ndf[self.nr_segment].transform(lambda cell: int(cell))
        ndf[self.LENGTH] = ndf.loc[:, ('edge1', 'edge2')].apply(sum, axis=1)
        ndf[self.LENGTH] = ndf[self.LENGTH].transform(np.linalg.norm)
        ndf[self.LENGTH] = ndf.apply(lambda row: row[self.LENGTH] * (1 if row[self.SEGMENT] == 0 else -1), axis=1)
        ndf = ndf[(ndf.apply(lambda row: row[self.COMBO][0] != row[self.COMBO][1], axis=1))]
        ndf = ndf.loc[:, (self.COMBO, self.ORDER, self.EDGE, self.LENGTH, self.sp, self.T, 'near', 'far', 'side')]
        return ndf

    def _get_df_w_tees(self):
        ndf = []
        wait_for = []
        self.xmldf['keep'] = False
        tdf = self.xmldf.copy()
        tdf['keep'] = True
        tdf = pd.concat([tdf] + [self.xmldf.copy() for _ in range(1, 4)], sort=False, ignore_index=True).reset_index(drop=True)
        tdf['el'] = pd.Series(chain.from_iterable([[i] * self.xmldf.shape[0] for i in range(4)]), index=tdf.index)
        tdf[self.thickness] = tdf[self.thickness].transform(lambda x: x / 2)
        with concurrent.futures.ProcessPoolExecutor() as executor:
            for part in self.parts:
                wait_for.append(executor.submit(self._make_df_by_part, tdf, part))
            wait_for = tqdm(concurrent.futures.as_completed(wait_for), file=sys.stdout, total=len(self.parts))
            for f in wait_for:
                ndf.append(f.result())
        ndf = pd.concat(ndf, sort=False, ignore_index=True).reset_index(drop=True)
        del tdf
        return ndf

    def _aggregate_t(self, select_rows_all_columns):
        cols = deepcopy(select_rows_all_columns)
        # if cols.edge.values[0][0] == 'BD1_P99-5|1.0|-0.0|0.0|0':
        #     print()

        # first filter, T must be of a range
        if len(cols[(cols[self.T] >= 0)][self.T].unique()) <= 1:
            return pd.DataFrame(columns=cols.columns)

        # joint type
        if -1 in cols[self.T].unique().tolist():
            # possible butt
            cols[self.JOINT] = self.BJ
            is_parallel = True
        else:
            # t
            cols[self.JOINT] = self.TJ
            is_parallel = False
        cols = cols[(cols[self.T] != -1)]

        # side bounds
        cross = cols[(cols.side == 10) & (cols.near >= 0) & (cols.far >= 0)]
        if not cross.empty:
            ctr, itr = cross.shape[0], 0
            try:
                while itr < ctr:
                    itr += 1
                    idx, row = next(cross.iterrows())
                    if row['near'] != row['far']:
                        s1, s2 = deepcopy(row), deepcopy(row)
                        if is_parallel:
                            pass
                        else:
                            s1['far'], s2['near'] = deepcopy(row[self.T]), deepcopy(row[self.T])
                        # s1[self.T] = -1003 if s1[self.T] < 0 else s1[self.T]
                        # s2[self.T] = -1003 if s2[self.T] < 0 else s2[self.T]
                        lwr_idx = cols[(cols.index > idx)].index
                        if len(lwr_idx) == 0:
                            upp_idx = cols[(cols.index < idx)].index
                            partial_idx = upp_idx
                        else:
                            partial_idx = lwr_idx
                        for i in partial_idx:
                            side = cols[(cols.index == i)].side.values[0]
                            if side in [11, 12]:
                                the_other_side = [11, 12]
                                the_other_side.remove(side)
                                s1['side'] = the_other_side[0]
                                s2['side'] = side
                                break
                        else:
                            # unable to split the crossing
                            s1, s2 = pd.Series(), pd.Series()
                            pass
                        cols = pd.concat([cols[(cols.index < idx)], pd.DataFrame([s1, s2], columns=cols.columns), cols[(cols.index > idx)]],
                                         sort=False,
                                         ignore_index=True).reset_index(drop=True)
                    else:
                        if row[self.T] < 0:
                            cols = cols.drop([idx])
                    cross = cols[(cols.side == 10) & (cols.near >= 0) & (cols.far >= 0)]
            except StopIteration:
                pass
        # list of tuples
        left = [tuple(ea) for ea in cols[(cols.side == 11) & (cols.near >= 0) & (cols.far >= 0)][['near', 'far']].values]
        right = [tuple(ea) for ea in cols[(cols.side == 12) & (cols.near >= 0) & (cols.far >= 0)][['near', 'far']].values]
        # reject tuple of same then flatten
        left = list(chain.from_iterable(filter(lambda x: x[0] != x[1], left)))
        right = list(chain.from_iterable(filter(lambda x: x[0] != x[1], right)))
        # accept non duplicates
        left = sorted(filter(lambda x: left.count(x) % 2 == 1, left))
        right = sorted(filter(lambda x: right.count(x) % 2 == 1, right))
        # get max_t from even bounds
        if len(left) % 2 != 0 or len(right) % 2 != 0:
            print(f'\n:WARNING bounds NOT found {cols[self.COMBO].values[0]} {cols[self.EDGE].values[0]}')
            return pd.DataFrame(columns=cols.columns)
        else:
            left = sum(chain.from_iterable([np.diff(left[i: i + 2]) for i in range(0, len(left), 2)]))
            right = sum(chain.from_iterable([np.diff(right[i: i + 2]) for i in range(0, len(right), 2)]))
            max_t = max([left, right]) if is_parallel else min([left, right])
        if max_t == 0:
            return pd.DataFrame(columns=cols.columns)
        else:
            max_t = 1 if max_t > 1 else (0 if max_t < 0 else max_t)
        cols = cols[(cols[self.T] >= 0)]
        cols[self.MAX_T] = pd.Series([max_t for _ in range(cols.shape[0])])

        # calculate length
        if len(cols[self.LENGTH]) == 0:
            return pd.DataFrame(columns=cols.columns)
        length = cols[self.LENGTH].values
        length = sum(length) / len(length)
        # shell plate is lazy
        if True in cols[self.sp].unique().tolist():
            tees = sorted(cols[self.T].unique().tolist())
            cols[self.T] = cols[self.T].transform(lambda _: (tees[0], tees[-1]))
            return cols.iloc[0, :].copy().to_frame().T
        # t acceptance conditions
        col = list(filter(lambda t: t != -1, cols[self.T]))
        temp = []
        for c in col:
            if len(temp) == 0:
                temp.insert(0, c)
            if temp[0] == c:
                # skip if same as previous, sequence not important
                continue
            else:
                temp.insert(0, c)
        tees = temp
        if len(tees) < 2:
            return pd.DataFrame(columns=cols.columns)
        # sort ascending, then find difference
        tees = sorted(tees)
        diff_temp = np.diff(tees)
        lim = tan(np.pi * self.res) * self.tol
        acc, diff = 0, []
        for td in diff_temp:
            acc += td
            if td * length <= lim:
                # accumulate short ones
                continue
            else:
                diff.append(deepcopy(acc))
                acc = 0
        if len(diff) == 0:
            return pd.DataFrame(columns=cols.columns)
        elif len(diff) == 1:
            cols[self.T] = cols[self.T].transform(lambda _: (tees[0], tees[-1]))
            return cols.iloc[0, :].copy().to_frame().T
        if True in cols[self.sp].unique().tolist():
            temp = tuple([tuple(tees[i:i+2]) for i in range(len(tees) - 1)])
        else:
            if len(diff) % 2 == 0:
                # even, remove one from either end, accept larger side
                diff1 = diff[:-1]
                diff1_sum = np.array(diff1)[::2].sum()
                diff2 = diff[1:]
                diff2_sum = np.array(diff2)[::2].sum()
                if diff1_sum > diff2_sum:
                    temp = tees[:-1]
                else:
                    temp = tees[1:]
            else:
                temp = tees
            temp = tuple(zip(temp[:-1:2], temp[1::2]))
        new_rows = cols.iloc[0, :].copy().to_frame().T
        new_rows = pd.concat([new_rows for _ in range(len(temp))],
                             sort=False,
                             ignore_index=True).reset_index(drop=True)
        new_rows[self.T] = pd.Series(temp)
        return new_rows

    def _delta_t_to_length(self, row, max_t=None):
        if max_t is None:
            max_t = self.MAX_T
        length = row[self.LENGTH]
        t = row[self.T]
        t = t[1] - t[0]
        t = row[max_t] if t > row[max_t] else t
        if t >= 1:
            return length
        return t * length

    def _reassign_edge(self, row):
        """
        Chop line based on start t and end t
        Swap ab if necessary, based on positive values
        Order of prevalence is z, y, x

        :param row: Series, one pandas row
        :return: tuple of ab tuples
        """
        t0, t1 = row[self.T]
        line = row[self.EDGE]
        line = np.array(line)
        ab = line[1] - line[0]
        a = line[0] + t0 * ab
        b = line[0] + t1 * ab

        # assert vector direction from (-) to (+)
        # z highest priority, x lowest priority
        uab = ab / np.linalg.norm(ab)
        if uab[2] < 0:
            is_invert = True
        elif uab[1] < 0 and uab[2] >= 0:
            is_invert = True
        elif uab[0] < 0 and uab[1] >= 0 and uab[2] >= 0:
            is_invert = True
        else:
            is_invert = False
        if is_invert:
            return tuple(b), tuple(a)
        else:
            return tuple(a), tuple(b)

    # to set t in order, and to remove overlapping pairs
    def _purge_overlap(self, rows, tee=None):
        if tee is None:
            tee = self.T
        tees = rows[tee]
        tees = sorted(tees, key=itemgetter(0))
        consumed = deepcopy(tees[0][0])
        new_tees = []
        for _ in tees[:]:
            t = tees.pop(0)
            if t[0] < consumed:
                t0 = consumed
            else:
                t0 = t[0]
            if t[1] <= t0:
                continue
            else:
                t1 = t[1]
            new_tees.append((t0, t1))
            consumed = t1
        if len(new_tees) <= 1:
            tees = new_tees
        else:
            tees = []
            start_1, end_1 = new_tees.pop(0)
            while True:
                start_2, end_2 = new_tees.pop(0)
                if end_1 >= start_2:
                    end_1 = end_2
                else:
                    tees.append((start_1, end_1))
                    start_1, end_1 = start_2, end_2
                if len(new_tees) == 0:
                    tees.append((start_1, end_1))
                    break
        rows = rows.iloc[0, :].copy().to_frame().T
        try:
            rows = pd.concat([rows for _ in range(len(tees))],
                             sort=False,
                             ignore_index=True).reset_index(drop=True)
        except ValueError:
            return pd.DataFrame(columns=rows.columns)
        rows[tee] = pd.Series(tees)
        return rows

    def _vector_wise(self, vsdf):
        """
        Function to name [separation_group]
        line's a and b are rotated to z plane as points
        group of a and b are separately clustered
        accept minimum number of cluster from either a or b as total number or clusters
        line is then numbered with cluster number it belongs to

        :param vsdf: DataFrame
        :return: vsdf DataFrame (after adding [separation_group] column)
        """

        num_of_rows = vsdf.shape[0]
        if num_of_rows == 1:
            # only one row, one cluster
            vsdf['separation_group'] = 0
            return vsdf
        else:
            clusters_by_a_or_b, points_by_a_or_b = [], []
            # first pass for a, second pass for b
            for a_b in [['ax', 'ay', 'az'], ['bx', 'by', 'bz']]:
                # get xyz points from a then b
                xyz = vsdf[a_b].values
                rotators = [vsdf['ux'].mean(), vsdf['uy'].mean(), vsdf['uz'].mean()]
                # if not already planar to z, rotate
                if abs(rotators[2]) != 1:
                    # x rotator is y vector, vice versa
                    rx, ry = radians(degrees(asin(rotators[1]))), radians(degrees(asin(rotators[0])))
                    points = []
                    for pt in xyz:
                        pt = np.dot([[1, 0, 0], [0, cos(rx), -sin(rx)], [0, sin(rx), cos(rx)]], pt)
                        pt = np.dot([[cos(ry), 0, -sin(ry)], [0, 1, 0], [sin(ry), 0, cos(ry)]], pt)
                        points.append(pt[0:2])
                    # store in points once rotatjon done
                    points = np.array(points)
                else:
                    points = xyz[:, [0, 1]]
                points_by_a_or_b.append(points)
                # check if there is only one point or same points
                if len(set(map(tuple, points))) == 1:
                    clusters_by_a_or_b.append(1)
                    continue
                # start with 2, if spreads beyond tolerance AND THICKNESS, keep increasing until enough
                ctr = clusters = 2
                kmeans = KMeans(n_clusters=ctr, random_state=0).fit(points)
                centers = kmeans.cluster_centers_
                thickness = vsdf[self.thickness].values[0]
                if np.linalg.norm(np.diff(centers, axis=0)) > self.tol + thickness:
                    ctr += 1
                    while ctr < len(points):
                        kmeans = KMeans(n_clusters=ctr, random_state=0).fit(points)
                        centers = kmeans.cluster_centers_
                        center_pairs = list(combinations(centers, 2))
                        separations = list(map(lambda c: np.linalg.norm(np.diff(c, axis=0)), center_pairs))
                        clear_separations = list(filter(lambda d: d > self.tol + thickness, separations))
                        if len(clear_separations) >= ctr:
                            ctr += 1
                            if ctr == len(points):
                                clusters = ctr
                                break
                        else:
                            clusters = ctr - 1
                            break
                else:
                    # otherwise, only one cluster
                    clusters = 1
                clusters_by_a_or_b.append(clusters)
            # get minimum number of clusters from two (a or b points)
            if clusters_by_a_or_b[0] <= clusters_by_a_or_b[1]:
                clusters = clusters_by_a_or_b[0]
                points = points_by_a_or_b[0]
            else:
                clusters = clusters_by_a_or_b[1]
                points = points_by_a_or_b[1]
            # apply grouping
            kmeans = KMeans(n_clusters=clusters, random_state=0).fit(points)
            km_group = kmeans.predict(points)
            vsdf.loc[:, 'separation_group'] = km_group
            return vsdf

    def _check_overlap(self, vsdf):
        """
        Non-overlapping (e.g. staggerred, disjointed) lines will not be fused

        :param vsdf:
        :return:
        """
        tolerance = self.tol
        u = vsdf[['ux', 'uy', 'uz']].values
        a, b = vsdf[['ax', 'ay', 'az']].values, vsdf[['bx', 'by', 'bz']].values
        a = list(zip_longest(map(lambda ua: np.dot(*ua), zip(u, a)), (), fillvalue=0))
        b = list(zip_longest(map(lambda ub: np.dot(*ub), zip(u, b)), (), fillvalue=0))
        if len(set(a)) == 1 and len(set(b)) == 1:
            vsdf['overlap_group'] = 0
            return vsdf
        am, bm = np.array(a), np.array(b)

        num_of_clusters_am = 1
        if len(set(a)) > 1:
            for i in range(1, len(am) + 1):
                kmeans_am = KMeans(n_clusters=i, random_state=0).fit(am)
                spread = sqrt(kmeans_am.inertia_ / len(kmeans_am.labels_))
                if spread <= tolerance:
                    num_of_clusters_am = i
                    break
        labels_am = KMeans(n_clusters=num_of_clusters_am, random_state=0).fit(am).labels_
        num_of_clusters_bm = 1
        if len(set(b)) > 1:
            for i in range(1, len(bm) + 1):
                kmeans_bm = KMeans(n_clusters=i, random_state=0).fit(bm)
                spread = sqrt(kmeans_bm.inertia_ / len(kmeans_bm.labels_))
                if spread <= tolerance:
                    num_of_clusters_bm = i
                    break
        labels_bm = KMeans(n_clusters=num_of_clusters_bm, random_state=0).fit(bm).labels_
        zipped = list(zip(labels_am, labels_bm))
        overlap_group = KMeans(n_clusters=len(set(zipped)), random_state=0).fit(zipped).labels_
        vsdf['overlap_group'] = overlap_group

        return vsdf

    def _mean_it(self, vsdf):
        if vsdf.shape[0] == 1:
            return vsdf
        else:
            ab_mean = tuple(vsdf[['ax', 'ay', 'az']].mean(axis=0, skipna=True).values), tuple(
                vsdf[['bx', 'by', 'bz']].mean(axis=0, skipna=True).values)
            vsdf[self.EDGE] = vsdf[self.EDGE].transform(lambda _: ab_mean)
            return vsdf

    def _fuse_it(self, vsdf):
        if vsdf.shape[0] == 1:
            pass
        elif vsdf.shape[0] == 2 and True in vsdf[self.ORDER].values and False in vsdf[self.ORDER].values:
            vsdf[self.JOINT] = self.BJ
            vsdf[self.ORDER] = None
            vsdf[self.LENGTH] = vsdf[self.LENGTH].max()
            # vsdf = vsdf.drop_duplicates()
        # elif vsdf.shape[0] > 2:
        else:
            vsdf[self.JOINT] = self.TJ
            true_cts = len(vsdf[(vsdf[self.ORDER])][self.ORDER].values)
            false_cts = len(vsdf[~(vsdf[self.ORDER])][self.ORDER].values)
            to_go_by = min([true_cts, false_cts]) if min([true_cts, false_cts]) != 0 else max(
                [true_cts, false_cts])
            vsdf[self.ORDER] = True if to_go_by == true_cts else False
            vsdf[self.LENGTH] = vsdf[self.LENGTH].max()
            # vsdf = vsdf.drop_duplicates()
        return vsdf

    def _fuse_edges(self, sdf):
        """
        Function to fuse multiple lines by same combo

        :param sdf: DataFrame
        :return: Same DataFrame with re-assigned line (same line). Apply drop_duplicates() to remove
        Joint type may also be re-assigned
        Length, accept max
        Order True, False, None
        """
        if sdf.shape[0] == 1:
            # only one row, nothing to fuse with
            return sdf

        # expand ab, then get ab direction vector
        ab = sdf[self.EDGE].values
        a, b = np.array(list(map(itemgetter(0), ab))), np.array(list(map(itemgetter(1), ab)))
        sdf['ax'], sdf['ay'], sdf['az'] = a[:, 0], a[:, 1], a[:, 2]
        sdf['bx'], sdf['by'], sdf['bz'] = b[:, 0], b[:, 1], b[:, 2]
        uab = b - a
        uab /= np.sqrt(uab ** 2)
        uab[np.isnan(uab)] = 0
        sdf['ux'], sdf['uy'], sdf['uz'] = uab[:, 0], uab[:, 1], uab[:, 2]

        # for grouping by vectors
        for el in ['ux', 'uy', 'uz']:
            sdf = sdf.sort_values(by=[el])
            to_group = sdf[el].tolist()
            to_group_diff = np.concatenate(([0], np.diff(to_group)))
            to_group_diff = [-2 if gd <= sin(self.res) else -1 for gd in to_group_diff]
            group_names = [0 if tgd == -2 else tgd for tgd in to_group_diff]
            num_of_groups = to_group_diff.count(-1) + 1
            for i in range(1, num_of_groups):
                mask = group_names.index(-1)
                group_names[mask] = i
                group_names = group_names[:mask] + [i if gn > -1 else -1 for gn in group_names[mask:]]
            sdf.loc[:, 'g' + el] = group_names

        # after gux, guy, guz are found
        sdf = sdf.groupby(['gux', 'guy', 'guz'], as_index=False).apply(self._vector_wise)

        # group overlapping lines
        sdf = sdf.groupby(['gux', 'guy', 'guz', 'separation_group'], as_index=False).apply(self._check_overlap)

        # assign common line
        sdf = sdf.groupby(['gux', 'guy', 'guz', 'separation_group', 'overlap_group'],
                          as_index=False).apply(self._mean_it)

        # remove helper columns
        sdf = sdf.drop(columns=['ax', 'ay', 'az', 'bx', 'by', 'bz', 'ux', 'uy', 'uz'])

        # fuse
        sdf = sdf.groupby(['gux', 'guy', 'guz', 'separation_group', 'overlap_group'],
                          as_index=False).apply(self._fuse_it)
        sdf = sdf.drop_duplicates()
        sdf = sdf.reset_index(drop=True)

        # remove helper columns
        sdf = sdf.drop(columns=['gux', 'guy', 'guz', 'separation_group', 'overlap_group'])

        return sdf

    def run(self, combo_name_clean=None, self_joint_clean=None):
        # check if inputs valid
        if self.is_exit[0]:
            return False, self.is_exit[1]

        # get millions of t using vectorize
        df = self._get_df_w_tees()

        if df.empty:
            return False, self.NO_JOINT_ERRMSG

        # remove self joints
        if self_joint_clean is not None:
            df = df[(df[self.COMBO].transform(lambda c: c[0].split('|')[0] != c[1].split('|')[0]))]
        else:
            df = df[(df[self.COMBO].transform(lambda c: c[0] != c[1]))]

        tqdm.pandas(file=sys.stdout, position=0, desc='Validating joints')
        df = df.groupby([self.COMBO, self.ORDER, self.EDGE],
                        group_keys=False).progress_apply(self._aggregate_t).reset_index(drop=True)
        df = df.drop(columns=['near', 'far', 'side', self.sp])

        if df.empty:
            return False, self.NO_JOINT_ERRMSG

        # add thickness in tolerance
        df['thickness'] = df.apply(lambda row: row[self.COMBO][1] if row[self.ORDER] else row[self.COMBO][0], axis=1)
        df['thickness'] = df['thickness'].apply(lambda surface:
                                                self.xmldf[(self.xmldf[self.part] == surface)][self.thickness].values[0])

        if combo_name_clean is not None:
            df[self.COMBO] = df[self.COMBO].apply(combo_name_clean)

        # arrange t ranges in order, and analyze for overlapping to de-bound
        df = df.groupby([self.COMBO, self.ORDER, self.EDGE],
                        group_keys=False).apply(self._purge_overlap).reset_index(drop=True)

        # factor t to length, then remove t, accept t only up to 1
        df[self.LENGTH] = df.apply(self._delta_t_to_length, axis=1)
        df = df.drop(columns=[self.MAX_T])

        # based on t range, move point a and b accordingly
        df[self.EDGE] = df.apply(self._reassign_edge, axis=1)
        df = df.drop(columns=[self.T])

        # fuse joining edges
        df = df.groupby([self.COMBO], as_index=False).apply(self._fuse_edges)

        df = df.drop(columns=[self.thickness])
        # df[self.LENGTH] = df[self.LENGTH].apply(ceil)
        return True, df


class ProcessDataframeCSV:
    def __init__(self, df, csv_df, xml_df, tolerance, arc_res, default_bevel, csv_input_column_names=None):
        self.df, self.csvdf, self.xmldf = df, csv_df, xml_df
        self.tol, self.res, self.defbev = tolerance, arc_res, default_bevel
        csv_header = 'startpoint x', 'startpoint y', 'startpoint z', 'endpoint x', 'endpoint y', 'endpointz', 'plate', 'attribute_key', 'model name'
        if csv_input_column_names is None:
            self.x_start, self.y_start, self.z_start, self.end_x, self.end_y, self.end_z, self.plate_key, self.attribute_key, self.model_name = csv_header
        else:
            self.x_start, self.y_start, self.z_start, self.end_x, self.end_y, self.end_z, self.plate_key, self.attribute_key, self.model_name = csv_input_column_names

    @staticmethod
    @vectorize([float64(float64, float64, float64, float64, float64, float64, float64, float64, float64, float64,
                        float64, float64, float64)], target='parallel')
    def _inline(ax, ay, az, bx, by, bz, cx, cy, cz, dx, dy, dz, tolerance):
        """Identify if ab cd are parallel or anti-parallel, then check if they overlap.
        If none overlaps or either only by a length of tolerance, reject. Otherwise, accept as 1"""
        # x,   y,   z
        abx, aby, abz = bx - ax, by - ay, bz - az
        cdx, cdy, cdz = dx - cx, dy - cy, dz - cz
        cd_mag = sqrt(cdx ** 2 + cdy ** 2 + cdz ** 2)
        ab_mag = sqrt(abx ** 2 + aby ** 2 + abz ** 2)
        # check if each line is almost a point
        if ab_mag <= tolerance or cd_mag <= tolerance:
            return 0
        # cross product
        ab_cross_cd_x = aby * cdz - abz * cdy
        ab_cross_cd_y = abz * cdx - abx * cdz
        ab_cross_cd_z = abx * cdy - aby * cdx
        cross_mag_ab_cd = sqrt(ab_cross_cd_x ** 2 + ab_cross_cd_y ** 2 + ab_cross_cd_z ** 2)
        # # parallel or anti-parallel only
        if cross_mag_ab_cd > tolerance:
            return -1
        # see if they overlap
        # x,   y,   z
        acx, acy, acz = cx - ax, cy - ay, cz - az
        bdx, bdy, bdz = dx - bx, dy - by, dz - bz
        # x,   y,   z
        adx, ady, adz = dx - ax, dy - ay, dz - az
        bcx, bcy, bcz = cx - bx, cy - by, cz - bz
        ac_mag = sqrt(acx ** 2 + acy ** 2 + acz ** 2)
        ad_mag = sqrt(adx ** 2 + ady ** 2 + adz ** 2)
        bc_mag = sqrt(bcx ** 2 + bcy ** 2 + bcz ** 2)
        bd_mag = sqrt(bdx ** 2 + bdy ** 2 + bdz ** 2)
        if ac_mag > tolerance and ad_mag > tolerance and bc_mag > tolerance and bd_mag > tolerance:
            # https://math.stackexchange.com/questions/1347604/find-3d-distance-between-two-parallel-lines-in-simple-way
            cross_x = (cdy / cd_mag) * acz - (cdz / cd_mag) * acy
            cross_y = (cdz / cd_mag) * acx - (cdx / cd_mag) * acz
            cross_z = (cdx / cd_mag) * acy - (cdy / cd_mag) * acx
            d = sqrt(cross_x ** 2 + cross_y ** 2 + cross_z ** 2)
            if d > tolerance:
                return -3
        da = -(ax * cdx + ay * cdy + az * cdz) / cd_mag
        db = -(bx * cdx + by * cdy + bz * cdz) / cd_mag
        dc = -(cx * cdx + cy * cdy + cz * cdz) / cd_mag
        dd = -(dx * cdx + dy * cdy + dz * cdz) / cd_mag
        if dd > dc:
            # if none inside
            if not (dc - tolerance <= da <= dd + tolerance or dc - tolerance <= db <= dd + tolerance):
                return -4
            # if both inside
            if dc - tolerance <= da <= dd + tolerance or dc - tolerance <= db <= dd + tolerance:
                return 1
            # either inside
            if da - dc < tolerance or dd - da < tolerance or db - dc < tolerance or dd - db < tolerance:
                return -5
        else:
            # if none inside
            if not (dd - tolerance <= da <= dc + tolerance or dd - tolerance <= db <= dc + tolerance):
                return -6
            # if both inside
            if dd - tolerance <= da <= dc + tolerance or dd - tolerance <= db <= dc + tolerance:
                return 1
            # either inside
            if dc - da < tolerance or da - dd < tolerance or dc - db < tolerance or db - dd < tolerance:
                return -7
        return 1

    def _find_bevel(self, pl):
        """Accept tuple of part_assy and tuple of two points (edge line). Find match in ptdf to return bevel type"""
        # part, line = pl
        line = pl
        ldf = self.csvdf
        ldf['ax'], ldf['ay'], ldf['az'] = line[0][0], line[0][1], line[0][2]
        ldf['bx'], ldf['by'], ldf['bz'] = line[1][0], line[1][1], line[1][2]
        is_valid = self._inline(
            np.ascontiguousarray(ldf.ax.values),
            np.ascontiguousarray(ldf.ay.values),
            np.ascontiguousarray(ldf.az.values),
            np.ascontiguousarray(ldf.bx.values),
            np.ascontiguousarray(ldf.by.values),
            np.ascontiguousarray(ldf.bz.values),
            np.ascontiguousarray(ldf[self.end_x].values),
            np.ascontiguousarray(ldf[self.end_y].values),
            np.ascontiguousarray(ldf[self.end_z].values),
            np.ascontiguousarray(ldf[self.x_start].values),
            np.ascontiguousarray(ldf[self.y_start].values),
            np.ascontiguousarray(ldf[self.z_start].values),
            np.ascontiguousarray([float(self.tol) for _ in range(int(ldf.size / len(ldf.columns)))]),
        )
        ldf['is_valid'] = pd.Series(np.array(is_valid).astype(int))
        ldf = ldf[(ldf.is_valid > 0)].reset_index(drop=True)
        bevel = ldf[[self.plate_key, self.attribute_key, self.model_name]].unique().tolist()
        bevel = list(map(lambda pkakmn: tuple([tuple(pkakmn[:-1]), pkakmn[-1]]), bevel))
        del ldf
        if len(bevel) != 0:
            bevel = dict(bevel)
            return bevel
        else:
            return self.defbev

    def _weld_location(self, rows):
        row = rows.sort_values(by=['length'], ascending=False).head(1).copy()
        # part, line = row['edge'].values[0]
        line = row['edge'].values[0]
        part = row['combo'].values[0][0] if row['order'].values[0] else row['combo'].values[0][1]
        # TODO
        # if none Butt_Joint
        if abs(line[0][2] - line[1][2]) > self.tol:
            to_return = tuple(['3'])
        else:
            part_ab = part
            combo = list(row['combo'].values[0])
            combo.remove(part_ab)
            part_cd = combo[0]
            pz_ab = abs(self.xmldf[(self.xmldf['part_assy'] == part_ab)].pz.values.astype(float)[0])
            pz_cd = abs(self.xmldf[(self.xmldf['part_assy'] == part_cd)].pz.values.astype(float)[0])
            if row['joint'].values[0] == 'Butt_Joint':
                if pz_ab >= cos(np.pi / 4) or pz_cd >= cos(np.pi / 4):
                    to_return = tuple(['1', '4'])
                else:
                    # not level
                    to_return = tuple(['2'])
            else:
                # T-Joint
                if pz_cd <= cos(np.pi / 4):
                    # not facing up z plane
                    to_return = tuple(['2'])
                else:
                    cogz_ab = self.xmldf[(self.xmldf['part_assy'] == part_ab)].cogz.values.astype(float)[0]
                    cogz_cd = self.xmldf[(self.xmldf['part_assy'] == part_cd)].cogz.values.astype(float)[0]
                    if cogz_ab >= cogz_cd:
                        # facing z plane, and ab higher than cd
                        to_return = tuple(['2'])
                        # to_return = tuple(['1'])
                    else:
                        to_return = tuple(['4'])
        rows['location'] = pd.Series([to_return] * rows.index.size, index=rows.index)
        return rows

    def run(self):
        tqdm.pandas(file=sys.stdout, position=0, desc='Finding bevels')
        self.df.loc[:, 'bevel'] = self.df['edge'].progress_apply(self._find_bevel)
        self.df = self.df.groupby(['combo'], as_index=False).apply(self._weld_location)
        self.df['bevel'] = self.df.apply(lambda row: (row['edge'][0], row['bevel']), axis=1)
        return True, self.df


# # revise joint types
# def revise_joint(vsdf):
#     if vsdf.shape[0] == 1:
#         # is single line (T-Joint)
#         vsdf.loc[:, 'bevel'] = vsdf['bevel'].transform(lambda _: tuple(vsdf['bevel'].unique()))
#         vsdf.loc[:, 'joint'] = 'T-Joint'
#     elif vsdf.shape[0] == 2 and 'Butt_Joint' in vsdf['joint'] and 'T-Joint' not in vsdf['joint']:
#         # merge the bevels for butt
#         vsdf.loc[:, 'bevel'] = vsdf['bevel'].transform(lambda _: tuple(vsdf['bevel'].unique()))
#     else:
#         # is two rows and there is T-Joint, or greater than two rows
#         vsdf.loc[:, 'bevel'] = vsdf['bevel'].transform(lambda _: tuple(vsdf[(vsdf['joint'] == 'T-Joint') & (vsdf['length'] == vsdf['length'].max())]['bevel'].unique()))
#         vsdf.loc[:, 'joint'] = 'T-Joint'
#     return vsdf
#
#
# def fuse_edges(df, tolerance, arc_res):
#     # utility function
#
#     # fuse by same combo
#     def execute(sdf: pd.DataFrame):
#         if sdf.shape[0] == 1:
#             return sdf
#
#         # expand ab
#         # ab = list(map(itemgetter(1), sdf['edge'].values))
#         # ab = np.array(ab)
#         ab = sdf['edge'].values
#         a, b = np.array(list(map(itemgetter(0), ab))), np.array(list(map(itemgetter(1), ab)))
#         # a, b = ab[:, 0], ab[:, 1]
#         sdf['ax'], sdf['ay'], sdf['az'] = a[:, 0], a[:, 1], a[:, 2]
#         sdf['bx'], sdf['by'], sdf['bz'] = b[:, 0], b[:, 1], b[:, 2]
#         uab = b - a
#         uab /= np.sqrt(uab ** 2)
#         uab[np.isnan(uab)] = 0
#         sdf['ux'], sdf['uy'], sdf['uz'] = uab[:, 0], uab[:, 1], uab[:, 2]
#
#         # grouping by vectors
#         def vector_wise(vsdf):
#             num_of_rows = vsdf.shape[0]
#             if num_of_rows == 1:
#                 vsdf.loc[:, 'separation_group'] = 0
#                 return vsdf
#             else:
#                 clusters_by_a_or_b = []
#                 for a_b in [['ax', 'ay', 'az'], ['bx', 'by', 'bz']]:
#                     xyz = vsdf[a_b].values
#                     rotators = [vsdf['ux'].mean(), vsdf['uy'].mean(), vsdf['uz'].mean()]
#                     if abs(rotators[2]) != 1:
#                         rotators = [radians(acos(rotators[0])), radians(acos(rotators[1]))]
#                         points = []
#                         for pt in xyz:
#                             for r in rotators[:2]:
#                                 pt = np.dot([[1, 0, 0], [0, cos(r), -sin(r)], [0, sin(r), cos(r)]], pt)
#                                 pt = np.dot([[cos(r), 0, -sin(r)], [0, 1, 0], [sin(r), 0, cos(r)]], pt)
#                             points.append(pt[0:2])
#                         points = np.array(points)
#                     else:
#                         points = xyz[:, [0, 1]]
#                     ctr, clusters = 2, 1
#                     kmeans = KMeans(n_clusters=ctr, random_state=0).fit(points)
#                     centers = kmeans.cluster_centers_
#                     if np.linalg.norm(np.diff(centers, axis=0)) > tolerance:
#                         ctr += 1
#                         while ctr <= len(points):
#                             kmeans = KMeans(n_clusters=ctr, random_state=0).fit(points)
#                             centers = kmeans.cluster_centers_
#                             center_pairs = list(combinations(centers, 2))
#                             separations = list(map(lambda c: np.linalg.norm(np.diff(c, axis=0)), center_pairs))
#                             clear_separations = list(filter(lambda d: d > tolerance, separations))
#                             if len(clear_separations) >= ctr:
#                                 ctr += 1
#                                 continue
#                             else:
#                                 clusters = ctr - 1
#                                 break
#                     clusters_by_a_or_b.append(clusters)
#                 kmeans = KMeans(n_clusters=min(clusters_by_a_or_b), random_state=0).fit(points)
#                 vsdf.loc[:, 'separation_group'] = kmeans.predict(points)
#                 return vsdf
#
#         for el in ['ux', 'uy', 'uz']:
#             sdf = sdf.sort_values(by=[el])
#             to_group = sdf[el].tolist()
#             to_group_diff = np.concatenate(([0], np.diff(to_group)))
#             to_group_diff = [-2 if gd <= sin(arc_res) else -1 for gd in to_group_diff]
#             group_names = [0 if tgd == -2 else tgd for tgd in to_group_diff]
#             num_of_groups = to_group_diff.count(-1) + 1
#             for i in range(1, num_of_groups):
#                 mask = group_names.index(-1)
#                 group_names[mask] = i
#                 group_names = group_names[:mask] + [i if gn > -1 else -1 for gn in group_names[mask:]]
#             sdf.loc[:, 'g' + el] = group_names
#         sdf = sdf.groupby(['gux', 'guy', 'guz'], as_index=False).apply(vector_wise)
#
#         # group overlapping lines
#         def check_overlap(vsdf):
#             u = vsdf[['ux', 'uy', 'uz']].values
#             a, b = vsdf[['ax', 'ay', 'az']].values, vsdf[['bx', 'by', 'bz']].values
#             a, b = list(map(lambda ua: np.dot(*ua), zip(u, a))), list(map(lambda ub: np.dot(*ub), zip(u, b)))
#             minim = min([*a, *b])
#             a, b = np.array(a) - minim, np.array(b) - minim
#             overlaps = []
#             for ab01 in combinations(zip(a, b), 2):
#                 if not (ab01[0][0] - tolerance <= ab01[1][0] <= ab01[0][1] + tolerance or
#                         ab01[0][0] - tolerance <= ab01[1][1] <= ab01[0][1] + tolerance or
#                         ab01[1][0] - tolerance <= ab01[0][0] <= ab01[1][1] + tolerance or
#                         ab01[1][0] - tolerance <= ab01[0][1] <= ab01[1][1] + tolerance):
#                     overlaps.append((False, ab01))
#                 else:
#                     overlaps.append((True, ab01))
#             if False in map(itemgetter(0), overlaps):
#                 overlapping = map(itemgetter(1), filter(lambda ol: ol[0], overlaps))
#                 overlapping = list(overlapping)
#                 overlap_set = set(chain.from_iterable(overlapping))
#                 groupping = []
#                 for ol_set in overlap_set:
#                     groupping.append((ol_set, list(map(lambda ol: True if ol_set in ol else False, overlapping))))
#                 groupped = []
#                 for g in groupping:
#                     g = filter(lambda z: z[0], zip(g[1], overlapping))
#                     g = map(itemgetter(1), g)
#                     groupped.append(tuple(set(chain.from_iterable(g))))
#                 overlapping = set(groupped)
#
#                 no_overlap = map(itemgetter(1), filter(lambda ol: not ol[0], overlaps))
#                 no_overlap = list(no_overlap)
#                 no_overlap = set(chain.from_iterable(no_overlap))
#                 no_overlap = list(map(lambda sa: (sa,), no_overlap - set(chain.from_iterable(overlapping))))
#
#                 groupped = list(overlapping) + no_overlap
#                 for i, g in zip(range(len(groupped)), groupped):
#                     for eg in g:
#                         vsdf.loc[(vsdf['ax'] == eg[0]) & (vsdf['bx'] == eg[1]), 'overlap_group'] = i
#             else:
#                 # one group
#                 vsdf['overlap_group'] = 0
#             return vsdf
#
#         sdf = sdf.groupby(['gux', 'guy', 'guz', 'separation_group'], as_index=False).apply(check_overlap)
#
#         # fuse edges
#         def mean_it(vsdf):
#             if vsdf.shape[0] == 1:
#                 return vsdf
#             else:
#                 # ab = zip_longest(tuple(map(itemgetter(0), vsdf['edge'].values)),
#                 #                  (),
#                 #                  fillvalue=(tuple(vsdf[['ax', 'ay', 'az']].mean(axis=0, skipna=True).values),
#                 #                             tuple(vsdf[['bx', 'by', 'bz']].mean(axis=0, skipna=True).values)))
#                 # vsdf['edge'] = tuple(map(tuple, ab))
#                 ab_mean = tuple(vsdf[['ax', 'ay', 'az']].mean(axis=0, skipna=True).values), tuple(vsdf[['bx', 'by', 'bz']].mean(axis=0, skipna=True).values)
#                 vsdf['edge'] = vsdf['edge'].transform(lambda _: ab_mean)
#                 return vsdf
#         sdf = sdf.groupby(['gux', 'guy', 'guz', 'separation_group', 'overlap_group'],
#                           as_index=False).apply(mean_it)
#
#         # remove helper columns
#         sdf = sdf.drop(columns=['ax', 'ay', 'az', 'bx', 'by', 'bz', 'ux', 'uy', 'uz', 'gux', 'guy', 'guz', 'separation_group', 'overlap_group'])
#
#         def fuse_it(vsdf):
#             if vsdf.shape[0] == 1:
#                 pass
#             elif vsdf.shape[0] == 2 and True in vsdf['order'] and False in vsdf['order']:
#                 vsdf['joint'] = 'Butt_Joint'
#                 vsdf['order'] = None
#                 vsdf['length'] = vsdf['length'].max()
#                 vsdf = vsdf.drop_duplicates()
#             elif vsdf.shape[0] > 2:
#                 vsdf['joint'] = 'T-Joint'
#                 true_cts = len(vsdf[(vsdf['order'])]['order'].values)
#                 false_cts = len(vsdf[~(vsdf['order'])]['order'].values)
#                 to_go_by = min([true_cts, false_cts]) if min([true_cts, false_cts]) != 0 else max([true_cts, false_cts])
#                 vsdf['order'] = True if to_go_by == true_cts else False
#                 vsdf['length'] = vsdf['length'].max()
#                 vsdf = vsdf.drop_duplicates()
#             return vsdf
#         sdf = sdf.groupby(['combo', 'edge'], as_index=False).apply(fuse_it)
#
#         return sdf
#
#     df = df.groupby(['combo'], as_index=False).apply(execute)
#     df['length'] = df['length'].transform(ceil)
#     return df
