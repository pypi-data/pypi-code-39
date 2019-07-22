import os
import cartopy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cima.goes.utils.load_CPT import load_CPT
try:
    import cupy as cp
    import numpy as np
    asnumpy = np.asnumpy
except:
    import numpy as np
    # import numpy as cp
    asnumpy = lambda x: x


LOCAL_BASE_PATH = os.path.dirname(os.path.abspath(__file__))


def add_cultural(ax):
    states_provinces = cartopy.feature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='10m',
        facecolor='none')

    countries = cartopy.feature.NaturalEarthFeature(
        category='cultural',
        name='admin_0_countries',
        scale='10m',
        facecolor='none')

    linewidth = 0.50
    ax.coastlines(resolution='10m', color='white', linewidth=linewidth)
    ax.add_feature(countries, edgecolor='white', linewidth=linewidth)
    ax.add_feature(states_provinces, edgecolor='white', linewidth=linewidth)


def add_grid(ax, lonlat_region):
    linewidth = 1.25
    gl = ax.gridlines(linewidth=linewidth,
                      linestyle='dotted',
                      color='r',
                      crs=ccrs.PlateCarree(),
                      draw_labels=False)

    # llat = 1
    # llon = 1
    # size = 10
    # gl.xlabels_top = True
    # gl.ylabels_right = True
    # gl.ylocator = mticker.FixedLocator(np.arange(lonlat_region[2],
    #                                              lonlat_region[3] + llat, llat))
    # gl.xlocator = mticker.FixedLocator(np.arange(lonlat_region[0],
    #                                              lonlat_region[1] + llon, llon))
    # gl.xformatter = LONGITUDE_FORMATTER
    # gl.yformatter = LATITUDE_FORMATTER
    # gl.xlabel_style = {'size': size}
    # gl.ylabel_style = {'size': size}


def plot2(data, tile, lats, lons, cmap='gray'):
    fig = plt.figure(figsize=(15, 12))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    add_cultural(ax)
    add_grid(ax, tile.extent)
    ax.set_extent(tile.extent, crs=ccrs.PlateCarree())

    print('va im show')
    cm = ax.pcolormesh(lons, lats, data, cmap=cmap, vmin=0, vmax=0.7)
    #     ax.imshow(data,
    #               origin='upper',
    #               extent=[lonwest, latnorth, loneast, latsouth],
    #               transform=sat_proj,
    #               interpolation='none')
    print('vuelve')

    #     ax.axis('off')

    plt.show()


def get_SMN_palette():
    from matplotlib.colors import LinearSegmentedColormap
    filepath = os.path.join(LOCAL_BASE_PATH, 'smn_topes.cpt')
    cpt = load_CPT(filepath)
    return LinearSegmentedColormap('cpt', cpt)


def save_image(image, filepath, tile, lats, lons, cmap='gray', vmin=0, vmax=0.7, cultural=True):
    dirpath = os.path.dirname(os.path.abspath(filepath))
    if not os.path.exists(dirpath):
        os.makedirs(dirpath, exist_ok=True)
    dummy_dpi = 100
    x, y = image.shape
    print(x, y, dummy_dpi)
    fig = plt.figure(frameon=False)
    fig.set_size_inches(x / dummy_dpi, y / dummy_dpi)

    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_axis_off()
    ax.set_extent(tile.extent, crs=ccrs.PlateCarree())
    if cultural:
        add_cultural(ax)
        add_grid(ax, tile.extent)
    ax.pcolormesh(lons, lats, image, cmap=cmap, vmin=vmin, vmax=vmax)

    fig.add_axes(ax, projection=ccrs.PlateCarree())
    ax.axis('off')
    plt.savefig(filepath + '.png', dpi=dummy_dpi, bbox_inches='tight')
    plt.close()


def plot(gray, rgb, tile, lats, lons):
    fig = plt.figure(figsize=(22, 12))
    ax1 = fig.add_subplot(1, 2, 1, projection=ccrs.PlateCarree())
    ax2 = fig.add_subplot(1, 2, 2, projection=ccrs.PlateCarree())

    latsouth = tile.extent[2]
    latnorth = tile.extent[3]
    lonwest = tile.extent[0]
    loneast = tile.extent[1]

    # ax1.set_extent([lonwest, loneast, latsouth, latnorth], crs=ccrs.PlateCarree())
    ax2.set_extent([lonwest, loneast, latsouth, latnorth], crs=ccrs.PlateCarree())

    add_cultural(ax1)
    add_cultural(ax2)
    ax1.set_extent(tile.extent, crs=ccrs.PlateCarree())
    # ax2.set_extent(tile.extent, crs=ccrs.PlateCarree())

    # ax1.imshow(gray, cmap='gray', vmin=0, vmax=1)
    # ax1.axis('off')

    ax2.imshow(rgb)
    # ax2.axis('off')
    cm1 = ax1.pcolormesh(lons, lats, gray, cmap='gray', vmin=0, vmax=0.7)
    # cm2 = ax2.pcolormesh(lons, lats, rgb, vmin=0, vmax=1)
    ax2.imshow(rgb, vmin=0, vmax=1)


    plt.subplots_adjust(wspace=.02)

    plt.show()
