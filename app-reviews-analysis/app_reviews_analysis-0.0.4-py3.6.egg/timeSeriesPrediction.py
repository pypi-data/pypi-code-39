# -*- coding: utf-8 -*-
#@Author: lailai
#@Date: 2019/5/3 13:37
#@Version: 1.0

from datetime import timedelta
from app_reviews_analysis.reviewPretreate import reviewPretreate
import pandas as pd
from numpy import *
from dateutil.parser import parse


# 预测情感分的类

class timeSeriesPrediction:
    def __init__(self,appid,df):
        self.appname=appid
        self.df3=df

    # 单个app的sentiment分预测
    def computes(self):  # p是1,2,3,4之类参数，tsplit训练集划分比例
        app = self.df3[self.df3["product_name"] == self.appname]
        # 按照时间段评论分割评论
        enddate = max(app["review_date"])
        startdate = min(app["review_date"])
        datecut = []
        colname = []
        date = startdate
        reviewsweek = []
        if (enddate - startdate) / timedelta(7) < 20:  #以20个时间段划分数据
            time = int((enddate - startdate) / timedelta(20))
        else:
            time = 7
        print("time", time)
        if time <= 0:
            print("时间段太短")
            print(app["review_date"])
            return
        while date <= enddate:
            datecut.append(date)
            date = date + timedelta(time)
        for i in range(len(datecut) - 1):
            print(i)
            colname.append(str(datecut[i]).split(" ")[0])
            reviewsweek.append([text for text in
                                app[(app["review_date"] >= datecut[i]) & (app["review_date"] < datecut[i + 1])][
                                    "review_text"]])
        # 评论情感分计算
        revirescoreweek = []
        for reviewlist in reviewsweek:
            revirescoreweek.append(reviewPretreate().RateSentiment(reviewlist))
        print("评论分", revirescoreweek)
        # 平均评分列表构建
        reviewsRating = []
        for reviewlist in revirescoreweek:
            reviewsmean = []
            #         posmean=[]
            #         negmean=[]
            for rscore in reviewlist:
                try:
                    scorenum = [int(i) for i in rscore[1:5].split(" ")]
                except:
                    print("情感分格式不符合")
                #             posmean.append(scorenum[0])
                #             negmean.append(scorenum[1])
                if abs(scorenum[0]) == abs(scorenum[1]):
                    reviewsmean.append(scorenum[1])
                elif (abs(scorenum[0]) > abs(scorenum[1])):
                    reviewsmean.append(scorenum[0])
                else:
                    reviewsmean.append(scorenum[1])
            reviewsRating.append(np.mean(reviewsmean))

        # 时间序列预测
        print(reviewsRating)
        reviewsRating1 = pd.DataFrame(reviewsRating)
        return reviewsRating1, colname, self.appname,time


    # 衰减速度的序列权重调节
    def sk(self,Rt, k, p):
        # Rt特征-时间评分矩阵，k时间段，
        bias = abs(Rt - Rt.mean(axis=1).reshape(Rt.shape[0], 1))  # △ij矩阵
        s = 1 - (bias.min(axis=1) + p * bias.max(axis=1)) / (
                    bias[:, Rt.shape[1] - k] + p * bias.max(axis=1))  # ξ(k)函数
        s[nonzero(isnan(s))] = 0
        return s

    # 时间序列预测
    def predictScored(self,Rt, p, L):
        Rt = Rt[:, -L:]
        fk = [np.exp(-self.sk(Rt, k, p) * k) for k in range(1, Rt.shape[1] + 1)]  # f(k)函数
        fk = np.array(fk)
        Rt1 = np.dot(Rt, fk) / fk.sum()
        return Rt1

    # MAE平均绝对误差
    def MAE(self,y, yp):
        N = len(yp)
        return abs(y - yp).sum() / N

    # NMAE规范化平均绝对值误差
    def NMAE(self,y, yp):
        N = len(yp)
        return self.MAE(y, yp) / (y.sum() / N)

    #时间序列模型评估
    def modelEvaluation(self,pstart=1,pend=9,pinterval=2,tsplit=0.8):
        reviewsRating1, colname, appname ,time= self.computes(tsplit)
        print(colname)
        reviewsRating1.index = colname
        reviewsRating1 = reviewsRating1.dropna()
        colname = reviewsRating1.index
        reviewsRatingTrue = reviewsRating1
        minnmae = inf
        minmae = inf
        minp = inf
        minL = inf
        for p in np.arange(pstart, pend, pinterval):
            for L in range(len(reviewsRating1) - int(len(reviewsRating1) * tsplit), int(len(reviewsRating1) * tsplit)):
                print("p=%d,L=%d" % (p, L))
                preds = []
                for i in range(int(len(reviewsRating1) * tsplit - 1), len(reviewsRating1) - 1):
                    pred = self.predictScored(reviewsRating1.values[:i].T, p, L).diagonal()  # 对角线上元素
                    preds.append(pred)
                print(preds)
                nmae = self.NMAE(reviewsRating1.values[int(len(reviewsRating1) * tsplit):len(reviewsRating1)], preds)
                mae = self.MAE(reviewsRating1.values[int(len(reviewsRating1) * tsplit):len(reviewsRating1)], preds)
                if minnmae>nmae:
                    minnmae = nmae
                    minmae = minmae
                    minp = p
                    minL = L
        print(minL,minp)
        print(colname)
        colname=list(colname)
        for i in range(len(reviewsRating1)-1,len(reviewsRating1)+int(len(reviewsRating1) * (1-tsplit)) - 1):
            print(i)
            print(str(parse(colname[i]) + timedelta(7)))
            pred = self.predictScored(reviewsRating1.values[:i].T, minp, minL).diagonal()  # 对角线上元素
            colname.append(str(parse(colname[i]) + timedelta(time))[0:10])
            print(colname)
            print(list(pred))
            print(shape(reviewsRating1.values))
            print(reviewsRating1.values)
            print(np.insert(reviewsRating1.values,i+1,values=pred,axis=0))
            reviewsRating1 = pd.DataFrame(np.insert(reviewsRating1.values,i+1,values=pred,axis=0))
            print(reviewsRating1)
            preds.append(pred)
        print("preds",preds)
        print(reviewsRating1)
        reviewsRating1.index = colname

        return reviewsRatingTrue,reviewsRating1,preds
