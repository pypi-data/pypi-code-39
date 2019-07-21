#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Author  : Shi Cheng
# @Time    : 2019/7/20 20:52
import _pickle as pickle
import numpy as np
import os

def read_pickle(path):
    f = open(path, "rb")
    data = pickle.load(f)
    f.close()
    return data

def write_pickle(path, data):
    f = open(path, 'wb')
    pickle.dump(data, f)
    f.close()

def show_in_MD(score_list, imgList, columns):
    showMD = ''
    for i in range(len(imgList)):
        showMD += "### "
        for j in range(len(score_list[i])):
            showMD += columns[j] + ':' + str(round(float(score_list[i][j]), 2))
            if (j != len(score_list[i]) - 1):
                showMD += " | "
            else:
                # showMD += "\n ![模糊图片](file:///" + imgList[i] + ")\n"
                showMD += "\n ![模糊图片](" + imgList[i] + ")\n"
    return showMD

def write_md(data, path):
    f = open(path, 'w', encoding='utf-8')
    f.write(data)
    f.close()

def save_md(df, columns, md_Home, top_k):
    # 循环排序，不排第一列用户打分
    for column_name in columns[1:]:
        temp1 = df.sort_values(by=column_name, ascending=False)
        tmp_imgList = temp1.index
        # 需要按行抽取打分生成md文件，这里按列取，转置
        score_list = np.array([temp1[colname] for colname in columns]).T
        tmp_imgList = tmp_imgList[0:top_k]
        score_list = score_list[:, 0:top_k]
        showMD = show_in_MD(score_list, tmp_imgList, columns)
        MD_path = md_Home + str(column_name) + '_high.md'
        write_md(showMD, MD_path)

        temp2 = df.sort_values(by=column_name, ascending=True)
        tmp_imgList = temp2.index
        score_list = np.array([temp2[colname] for colname in columns]).T
        tmp_imgList = tmp_imgList[0:top_k]
        score_list = score_list[:, 0:top_k]
        showMD = show_in_MD(score_list, tmp_imgList, columns)
        MD_path = md_Home + str(column_name) + '_low.md'
        write_md(showMD, MD_path)

def get_all_file_score_List(file_path):
    job_list = []
    score_list = []
    for root_path, dir_name_list, file_name_list in os.walk(file_path):
        for file_name in file_name_list:
            job_list.append(root_path + file_name)
            score_list.append(float(file_name.split('_')[1]))
    return job_list, score_list

def get_all_file_List(file_path):
    job_list = []
    for root_path, dir_name_list, file_name_list in os.walk(file_path):
        for file_name in file_name_list:
            job_list.append(root_path + file_name)
    return job_list