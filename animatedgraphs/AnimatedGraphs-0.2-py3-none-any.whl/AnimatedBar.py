import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
import matplotlib.image as mpimg
import imageio
import numpy as np
from matplotlib import gridspec
import requests
import zipfile
import os

def CreateGraphBar(DS, AGGREGATION_TYPE, BAR_ATTRIBUTE_NAME, LOOP_ATTRIBUTE_NAME, SERIES_ATTRIBUTE_NAME, GRAPH_TITLE, 
                        GRAPH_XLABEL = "", GRAPH_YLABEL = "",
                        IMAGE_SET_URL = "", IMAGE_SET_EXT = "", SORT_BARS_LIST = [],
                    GRAPH_STEPS = 10, GRAPH_FRAME_DURATION = 1.0, GRAPH_FILENAME = "animated-graph.gif"):    

    #Initial variablees
    
    TMP_IMAGE_FOLDER = "tmpImgFolder"
    COLOR_BARS = ['#acfc21', '#fc8f21', '#21fcbe', '#fc21ea', '#fcf521']

    #Initial actions
    WORKING_DS = DS.copy()
    SERIES_TO_PLOT_NAMES=pd.Series(WORKING_DS[SERIES_ATTRIBUTE_NAME]).unique()
    NUMBER_OF_PLOTS = len(SERIES_TO_PLOT_NAMES)
    if (len(SORT_BARS_LIST) > 0):
        WORKING_DS[BAR_ATTRIBUTE_NAME]=pd.Categorical(WORKING_DS[BAR_ATTRIBUTE_NAME],categories=SORT_BARS_LIST)
        WORKING_DS=WORKING_DS.sort_values(BAR_ATTRIBUTE_NAME)    
    if(IMAGE_SET_URL != ""):
        #Download Zip
        resp = requests.get(IMAGE_SET_URL)
        tmpZipName = "images_set.zip"
        zfile = open(tmpZipName, 'wb')
        zfile.write(resp.content)
        zfile.close()

        #Unzip
        zip_ref = zipfile.ZipFile(tmpZipName, 'r')
        zip_ref.extractall("{}/{}/".format(os.getcwd(), TMP_IMAGE_FOLDER))
        zip_ref.close()

    #Get Max Values for Graph
    if(AGGREGATION_TYPE == "SUM"):
        SUMMARIZED_DS = WORKING_DS.groupby([LOOP_ATTRIBUTE_NAME, BAR_ATTRIBUTE_NAME]).sum()
        AXIS=0
    elif (AGGREGATION_TYPE == "COUNT"):
        SUMMARIZED_DS = WORKING_DS.groupby([LOOP_ATTRIBUTE_NAME, BAR_ATTRIBUTE_NAME]).count()
        AXIS=1

    max_values = SUMMARIZED_DS.max(axis=AXIS)

    max_value = max_values[0]
    for i in range(1, NUMBER_OF_PLOTS):
        if max_values[i] > max_value:
            max_value = max_values[i]

    max_value = max_value*1.20

    #Set Steps in Graph
    labelsX = np.arange(0, max_value, step=max_value/GRAPH_STEPS)

    #Set Loop values
    LOOP_ITEMS = pd.Series(WORKING_DS[LOOP_ATTRIBUTE_NAME]).unique()

    imgList = []
    for loopItem in LOOP_ITEMS:
        SUMMARIZED_DS = WORKING_DS.loc[(WORKING_DS[LOOP_ATTRIBUTE_NAME] == loopItem)]
        SUMMARIZED_DS = SUMMARIZED_DS.drop([LOOP_ATTRIBUTE_NAME], axis=1)
        if(AGGREGATION_TYPE == "SUM"):
            SUMMARIZED_DS = SUMMARIZED_DS.pivot_table("ID", BAR_ATTRIBUTE_NAME, SERIES_ATTRIBUTE_NAME, aggfunc="sum")
        elif (AGGREGATION_TYPE == "COUNT"):
            SUMMARIZED_DS = SUMMARIZED_DS.pivot_table("ID", BAR_ATTRIBUTE_NAME, SERIES_ATTRIBUTE_NAME, aggfunc="count")

        fig = plt.figure(figsize=(10,5))
        gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1]) 
        ax = fig.add_subplot(gs[0])

        SUMMARIZED_DS.plot.barh(ax=ax, color=COLOR_BARS)
        plt.title(GRAPH_TITLE + " " + LOOP_ATTRIBUTE_NAME + " " + loopItem)
        plt.xlabel(GRAPH_XLABEL)
        plt.ylabel(GRAPH_YLABEL)
        plt.xticks(labelsX)
        plt.legend(loc=4)

        #Add loop image if required
        if(IMAGE_SET_EXT != ""):
            ax = fig.add_subplot(gs[1])
            image = plt.imread("{}/{}/{}.{}".format(os.getcwd(), TMP_IMAGE_FOLDER, loopItem, IMAGE_SET_EXT))
            ax.imshow(image)
            plt.axis('off')

        #Save file
        filename = "temporal-H{}.png".format(loopItem)
        fig.savefig(filename)
        imgList.append(filename)

        #Clear cache
        fig.clf()
        plt.close(fig)

    #Generate animation
    images = []
    for filename in imgList:
        images.append(imageio.imread(filename))
    imageio.mimsave(GRAPH_FILENAME, images, format='GIF', duration=GRAPH_FRAME_DURATION)

    return os.getcwd() + "/" + GRAPH_FILENAME