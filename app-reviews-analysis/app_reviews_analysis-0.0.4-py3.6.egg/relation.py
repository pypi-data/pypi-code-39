# -*- coding: utf-8 -*-
#@Author: lailai
#@Date: 2019/5/3 9:50
#@Version: 1.0

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import timedelta
import app_reviews_analysis.reviewPretreate as rP
import pandas as pd
import re
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


# star与情感得分的相关性分析，以及时间段内的平均的star的得分和情感分计算
class Relation:
    def __init__(self,appname):
        self.appname=appname

    # star加权平均函数
    def WA(self,starlist):
        if len(starlist) != 0:
            return (starlist.count(5) * 5 + starlist.count(4) * 4 + starlist.count(3) * 3 + starlist.count(
                2) * 2 + starlist.count(1)) / len(starlist)
        else:
            return 0

    # 单个app的star与sentiment关系分析
    def relation(self,df3):
        app = df3[df3["product_name"] == self.appname]
        # 按照时间段评论分割评论
        enddate = max(app["review_date"])
        startdate = min(app["review_date"])
        datecut = []
        date = startdate
        reviewsweek = []
        starweek = []
        if (enddate-startdate)/timedelta(7)<20:
            time = int((enddate - startdate) / timedelta(20))
        else:
            time = 7
        print("time", time)
        if time <= 0:
            print("时间段太短")
            return
        while date <= enddate:
            datecut.append(date)
            date = date + timedelta(time)
        for i in range(len(datecut) - 1):
            print(i)
            reviewsweek.append([text for text in
                                app[(app["review_date"] >= datecut[i]) & (app["review_date"] < datecut[i + 1])][
                                    "review_text"]])
            starweek.append([text for text in
                             app[(app["review_date"] >= datecut[i]) & (app["review_date"] < datecut[i + 1])][
                                 "rating_star"]])
        # 评论情感分计算
        revirescoreweek = []
        for reviewlist in reviewsweek:
            revirescoreweek.append(rP.reviewPretreate().RateSentiment(reviewlist))
        print("评论分", revirescoreweek)

        # 平均评分列表构建
        starsRating = []
        reviewsRating = []
        reviewsRatingLable=[]
        for starlist in starweek:
            starmean = []
            for star in starlist:
                starmean.append(int(re.findall("\d", star)[0]))
            starsRating.append(self.WA(starmean))
        for reviewlist in revirescoreweek:
            reviewsmean = []
            posmean = []
            negmean = []
            for rscore in reviewlist:
                try:
                    scorenum = [int(i) for i in rscore[1:5].split(" ")]
                except:
                    print("情感分格式不符合")
                posmean.append(scorenum[0])
                negmean.append(scorenum[1])
                if abs(scorenum[0]) == abs(scorenum[1]):
                    reviewsmean.append(scorenum[1])
                elif (abs(scorenum[0]) > abs(scorenum[1])):
                    reviewsmean.append(scorenum[0])
                else:
                    reviewsmean.append(scorenum[1])
            reviewsRating.append(np.mean(reviewsmean))


        # 皮尔逊相关系数
        personcoef = pd.Series(starsRating).corr(pd.Series(reviewsRating))
        spearmancoef = pd.Series(starsRating).corr(pd.Series(reviewsRating), method='spearman')
        print("皮尔逊线性相关系数为：", pd.Series(starsRating).corr(pd.Series(reviewsRating)))
        print("斯皮尔曼相关系数为：", pd.Series(starsRating).corr(pd.Series(reviewsRating), method='spearman'))

        # 画图
        fig = plt.figure()
        ax = fig.add_subplot(111)
        x, y = pd.Series(starsRating, name="x_var"), pd.Series(reviewsRating, name="y_var")
        sns.regplot(x, y)
        plt.xlabel('SST(star_score)')
        plt.ylabel('average sentiment score')
        plt.title(self.appname)
        plt.show()
        return personcoef,spearmancoef,starsRating,reviewsRating