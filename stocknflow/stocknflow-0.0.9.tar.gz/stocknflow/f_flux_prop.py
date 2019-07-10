from math import pi 
from math import sqrt
import cmath as cm
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.geometry import MultiPoint

def f_flux_prop(fond, data, code, start, end, flux, x_legend, y_legend, flux_min = 0, trunc = 0.75, head = 0.75, ratio = 1/3, round_legend = 0, quantile_legend = 0.5):
    """
    Représentation de flux entre lieux à partir de flèches proportionnelles à leur importance.
    
    :param code: Nom de la variable codant les géométries (correspondant à start et end dans data)
    :param start: Nom de la variable codant le point de depart présente dans data
    :param end: Nom de la variable codant le point d'arrivée présente dans data
    :param flux: Nom de la variable de flux présente dans data
    :param trunc: Paramètre de forme de la flèche : proportion du corps de la flèche (sur 
    """
    
    fond = fond.rename(columns={fond.geometry.name: 'geometry'}).set_geometry('geometry')
    #géométrie en Points
    if True in fond.type.isin(['Polygon', 'MultiPolygon']):
        fond['centroides'] = fond.representative_point()
        fond = fond.set_geometry('centroides')
    else:        
        fond = fond.rename(columns={fond.geometry.name: 'centroides'}).set_geometry('centroides')
    
    df = data[[start, end, flux]]
    df.columns = ["start", "end", "flux"]
    df['start'] = df.start.apply(str)
    df['end'] = df.end.apply(str)
    
    #fusion des données et du fond
    dfs = df.set_index('end').join(fond[['code','centroides']].set_index('code'))
    dfs['end'] = dfs.index
    dfs = dfs.rename(columns = {'centroides': 'centroides_end'})
    dfs = dfs.set_index('start').join(fond[['code','centroides']].set_index('code'))
    dfs['start'] = dfs.index
    dfs = dfs.rename(columns = {'centroides': 'centroides_start'})
    dfs.index = [i for i in range(dfs.shape[0])]
    dfs = dfs[['start','end','centroides_start','centroides_end','flux']]
    
    #détermination de l'emprise
    emprise = MultiPoint([ point for point in fond['centroides']]).convex_hull.area
    
    #ensemble des codes
    all_codes = fond[code]
    
    pts = list(map(lambda x: fond.geometry[fond[code] == x], all_codes))
    dict_coords = dict()
    for i in range(len(all_codes)):
        dict_coords[all_codes[i]] =  float(pts[i].x), float(pts[i].y)
        
    def distance(st,en):
        """
        st et end : coordonnées cartésiennes sous forme d'un tuple
        """
        return(sqrt((st[0]-en[0])**2+(st[1]-en[1])**2))
        
    #coefficient de proportionalité
    couples = [(dict_coords[str(dfs.start[i])],dict_coords[str(dfs.end[i])]) for i in range(dfs.shape[0])]
    distances = list(map(lambda points: distance(points[0], points[1]), couples))
    tot_var = sum([distances[i]*dfs['flux'][i] for i in range(dfs.shape[0])])
    k = ratio * emprise / (tot_var*(trunc + 1/2*(2*head+1)*(1-trunc)))
        
    def draw_arrow(code_start, code_end, flux):
        pt_a = dict_coords[code_start]
        pt_e = dict_coords[code_end]
        ae = distance(pt_a, pt_e)
        
        c_a, c_e = tuple(map(lambda pt: complex(pt[0],pt[1]), [pt_a,pt_e]))
        c_a_bis = (k*flux * (c_e - c_a))/ae + c_a
        
        c_b1 = (c_a_bis - c_a)*cm.rect(1, -pi/2) + c_a
        c_b2 = (c_a_bis - c_a)*cm.rect(1, pi/2) + c_a
        
        c_c1 = trunc*(c_e - c_a) + c_b1
        c_c2 = trunc*(c_e - c_a) + c_b2
        
        c_d1 = head*(c_b1 - c_a) + c_c1
        c_d2 = head*(c_b2 - c_a) + c_c2
        
        points = list(map(lambda z: (z.real, z.imag), [c_a, c_b1, c_c1, c_d1, c_e, c_d2, c_c2, c_b2]))
        #points = tuple(map(Point, points))
        arrow = Polygon(points)
        return(arrow)
        
    # Construction des flèches     
    dfs['geometry'] = list(map(lambda i: draw_arrow(dfs.start[i], dfs.end[i], dfs.flux[i]), dfs.index))
    
    flow = gpd.GeoDataFrame(dfs[dfs.flux >= flux_min][['start','end','flux','geometry']], crs=fond.crs, geometry='geometry')
    
    #création fond de légende
    # min_x, min_y, max_x, max_y = fond.total_bounds
    # var_max = round(max(fond[var]),round_legend)
    # rayon_max = calcul_rayon(var_max)
    # var_q = round(np.quantile(fond[var],quantile_legend), round_legend)
    # rayon_q = calcul_rayon(var_q)

    # df = pd.DataFrame(
        # {'nom': ['max', 'tiers'],
         # 'label': [var_max, var_q],
         # 'rayon': [rayon_max, rayon_q],
         # 'x': [x_legend, x_legend],
         # 'y': [y_legend, y_legend - rayon_max + rayon_q]})
    # fond_legend = gpd.GeoDataFrame(df, geometry=[Point(x,y) for x,y in zip(df.x, df.y)])
    # fond_legend['ronds'] = [fond_legend.centroid[i].buffer(fond_legend.rayon[i]) for i in fond_legend.index]
    # fond_legend = fond_legend.set_geometry('ronds')
    # fond_legend = fond_legend.drop(columns=['geometry'])
    # fond_legend = fond_legend.rename(columns={fond_legend.geometry.name: 'geometry'}).set_geometry('geometry')
    
    
    return(flow)
    