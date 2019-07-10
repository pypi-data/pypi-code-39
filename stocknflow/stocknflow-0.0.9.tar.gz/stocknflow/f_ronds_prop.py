from math import pi 
from math import sqrt
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from shapely.geometry import MultiPoint

def f_ronds_prop(fond, var, x_legend, y_legend, data = None, key_fond = None, key_data = None, round_legend = 0, quantile_legend = 0.5):
    """
    Crée un fond de ronds proportionnels à partir du fond et des données passés en paramètres.
    La géométrie en entrée peut être des polygones ou des points.
    En sortie, la géométrie sera des polygones et contiendra l'ensemble des variables qui composaient le fond à l'origine,
    plus éventuellement la variable quantitative qui a servi à calculer les ronds.
    
    - **parameters**, **types**, **return** and **return types**::
    
    :param fond: fond spatial importé avec geopandas
    :type fond: geopandas.geodataframe.GeoDataFrame
    :param var: nom de la variable quantitative servant à la détermination de la taille des ronds
    :type var: string
    :param x_legend: coordonnées x du centre de la légende
    :type x_legend: int, float
    :param y_legend: coordonnées y du centre de la légende
    :type y_legend: int, float
    :param data: Eventuellement, le tableau dans lequel trouver la variable var
    :type data: pandas.DataFrame
    :param key_fond: Nom de la variable du fond pour effectuer la jointure
    :type key_fond: string
    :param key_data: Nom de la variable du data pour effectuer la jointure. laisser None si la jointure porte le même nom.
    :type key_data: string
    :param round_legend: Arrondi des valeurs affichées en légende
    :type round_legend: integer
    :param quantile_legend: Quantile de la variable à représenter dans la légende comme le plus petit rond
    :type quantile_legend: float (entre 0 et 1)
    
    :return: fonds de ronds et de légende fournis séparément
    :rtype: tuple of two geopandas.geodataframe.GeoDataFrame
    
    .. todo:: 
        * translate doc
        * add try-except block (make sure that parameters have the right type)
    
    .. note:: La surface totale des ronds représente 1/7e de la surface convexe enveloppant les centroïdes.
    
    .. note:: La taille du fond de ronds peut être importante une fois exporté en shp, si le nombre de ronds est grand. Cela peut
    être optimisé en réalisant des polygônes avec un nomre de points fonction de la taille du rond.
    """
    fond = fond.rename(columns={fond.geometry.name: 'geometry'}).set_geometry('geometry')
    #géométrie en Points
    if True in fond.type.isin(['Polygon', 'MultiPolygon']):
        fond['centroides'] = fond.representative_point()
        fond = fond.set_geometry('centroides')
    else:        
        fond = fond.rename(columns={fond.geometry.name: 'centroides'}).set_geometry('centroides')
    
    #fusion avec les données si pertinent
    if data is not None:
        data[key_fond] = data[key_data] if key_data is not None else data[key_fond]
        fond = fond.merge(data.loc[:,[key_fond, var]], on = key_fond)
    
    #détermination de l'emprise
    emprise = MultiPoint([ point for point in fond['centroides']]).convex_hull.area
    
    #coefficient de proportionalité
    tot_var = sum(fond[var])
    k = emprise / (7*tot_var)
    
    #rayon des cercles
    def calcul_rayon(variable):
        return(np.sqrt(k*variable/pi))
    
    fond['rayon'] = calcul_rayon(fond[var]) #np.sqrt(k*fond[var]/pi)
    
    #création fond de ronds
    fond['ronds'] = [fond.centroides[i].buffer(fond.rayon[i]) for i in fond.index]
    fond = fond.set_geometry('ronds')
    fond.sort_values(var, ascending = False, inplace = True)
    fond = fond.drop(columns=['geometry', 'centroides'])
    fond = fond.rename(columns={fond.geometry.name: 'geometry'}).set_geometry('geometry')
    
    #création fond de légende
    min_x, min_y, max_x, max_y = fond.total_bounds
    var_max = round(max(fond[var]),round_legend)
    rayon_max = calcul_rayon(var_max)
    var_q = round(np.quantile(fond[var],quantile_legend), round_legend)
    rayon_q = calcul_rayon(var_q)

    df = pd.DataFrame(
        {'nom': ['max', 'tiers'],
         'label': [var_max, var_q],
         'rayon': [rayon_max, rayon_q],
         'x': [x_legend, x_legend],
         'y': [y_legend, y_legend - rayon_max + rayon_q]})
    fond_legend = gpd.GeoDataFrame(df, geometry=[Point(x,y) for x,y in zip(df.x, df.y)])
    fond_legend['ronds'] = [fond_legend.centroid[i].buffer(fond_legend.rayon[i]) for i in fond_legend.index]
    fond_legend = fond_legend.set_geometry('ronds')
    fond_legend = fond_legend.drop(columns=['geometry'])
    fond_legend = fond_legend.rename(columns={fond_legend.geometry.name: 'geometry'}).set_geometry('geometry')
    
    return(fond, fond_legend)