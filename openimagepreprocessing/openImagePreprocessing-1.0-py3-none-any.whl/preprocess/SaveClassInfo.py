import json
import pandas as pd
from typing import List, Tuple, Dict

def list_dictionary(parents_dict:Dict, line:int, boxes_classes:pd.DataFrame, file):
    """Save the label hierachy to a txt file

    :param parents_dict: parent_dict data.
    :type parents_dict: Dict.
    :param line: depth of the class.
    :type line: int.
    :param boxes_classes: box classes data.
    :type boxes_classes: pd.DataFrame.
    :param file: a file object.
    :type file: file.
    """

    LabelName = parents_dict['LabelName']
    className = "Entity"
    if LabelName!= '/m/0bl9f':
        className = boxes_classes.loc[LabelName][1]
    print(" "*line*2 + str(line) + "." + className)
    file.write(" "*line*2 + str(line) + "." + className+"\n")
    if 'Subcategory' in parents_dict.keys():
        for subdict in parents_dict['Subcategory']:
            list_dictionary(subdict, line+1, boxes_classes, file)
    if 'Part' in parents_dict.keys():
        for subdict in dictionary['Part']:
            list_dictionary(subdict, line+1, boxes_classes, file)

def list_parent(parents_dict:Dict, dic:Dict, temp:List, boxes_classes:pd.DataFrame) -> Dict:
    """Get a dictionary of the classes

    :param parents_dict: parent_dict data.
    :type parents_dict: Dict.
    :param dic: the dic result.
    :type dic: Dict.
    :param temp: temp list.
    :type temp: List.
    :param boxes_classes: box classes data.
    :type boxes_classes: pd.DataFrame.
    :return: a class dict.
    :rtype: Dict
    """

    LabelName = parents_dict['LabelName']
    className = "Entity"
    if LabelName!= '/m/0bl9f':
        className = boxes_classes.loc[LabelName][1]

    if  LabelName not in dic.keys():
        dic[LabelName] = []
        dic[LabelName].append(temp)
    else:
        flag = True
        for lis in dic[LabelName]:
            if set(temp) <= set(lis):
                flag = False
                break
        if flag:
            dic[LabelName].append(temp)
    temp = [className] + temp    
    if 'Subcategory' in parents_dict.keys():
        for subdict in parents_dict['Subcategory']:
            list_parent(subdict,dic, temp, boxes_classes)
    if 'Part' in parents_dict.keys():
        for subdict in dictionary['Part']:
            list_parent(subdict, dic, temp, boxes_classes)
