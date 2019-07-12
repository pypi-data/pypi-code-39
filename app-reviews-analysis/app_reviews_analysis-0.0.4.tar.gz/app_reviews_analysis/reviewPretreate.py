# -*- coding: utf-8 -*-
#@Author: lailai
#@Date: 2019/4/30 19:20
#@Version: 1.0

import pandas as pd
from dateutil.parser import parse
from datetime import timedelta
import langid
import nltk
import nltk.corpus
import subprocess
import shlex
import re
import emoji
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.collocations import *
from nltk.corpus import wordnet as wn
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class reviewPretreate:

    def __init__(self):
        self.sentimentPath = BASE_DIR+"/app_reviews_analysis/static/sentiment"  # 情感词典文件路径
        self.SentiStrengthLocation = BASE_DIR+"/app_reviews_analysis/static/SentiStrength.jar"  # 情感分析工具SentiStrength.jar路径
        self.SentiStrengthLanguageFolder = BASE_DIR+"/app_reviews_analysis/static/SentStrength_Data/"  # 情感词文件路径

    # 数据导入
    def dataimport(self,path,encoding='utf-8'):
        # df = pd.read_csv("G:/bigDataFile/app/app/appInfoAll20190125/appInfoAll20190125.csv", encoding='utf-8')
        df3 = pd.read_csv(path, encoding=encoding)  # 导入评论数据
        # 查询语句，选出dataanalysis_appreviewinfo表中的所有数据
        # sql = '''
        #       select * from dataanalysis_appreviewinfo where product_name='Uber';
        #       '''
        # df3 = pd.read_sql_query(sql,self.app_reviews_analysis)
        ix = []
        for i in range(len(df3["review_text"])):
            if langid.classify(df3["review_text"][i])[0] == 'en': # 去掉非英文评论
                ix.append(i)
        df3 = df3.iloc[ix,:]
        df3["review_date"] = [parse(d) for d in df3["review_date"]]  # 将日期转化为datetime格式
        # 导入情感词词典
        path=self.sentimentPath
        sentimentword = []
        for filename in os.listdir(path):
            fo = open(os.path.join(path, filename), "r")
            for line in fo.readlines():
                sentimentword.append(line.replace(" \n", "").replace("\n", ""))
        return df3,sentimentword  # 返回数据表，情感词典

    # 判断两个二元搭配词是否为同义词
    def issynonyms(self, word1, word2):
        synonyms = []
        for word in word1:
            for syn in wn.synsets(word):
                for l in syn.lemmas():
                    synonyms.append(l.name())
        if set(word2).issubset(set(synonyms)):
            return 1
        else:
            return 0

    # 数据预处理为特征向量
    def pretreat(self, reviewslist, sentimentword):
        text1 = []
        lemmatizer = WordNetLemmatizer()  # 词还原主干函数
        sr = stopwords.words('english')
        sr.extend(
            ["app", "please", "fix", "android", "google", "youtube", "as", "uber", "dont", "cousin", "pp", "facebook",
             "fitbit"])
        english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%', '{',
                                '}', '`', '<', ">", '/', "^", "-", "_", "``", "''", "...", "......"]  # 标点符号列表
        for text in reviewslist:
            try:
                text = text.lower()  # 小写形式
                text = emoji.get_emoji_regexp().sub("", text)  # 去掉表情符
                texts_filtered = [word for word in word_tokenize(text) if
                                  word not in english_punctuations]  # 去掉标点符号
                #                 texts_filtered1=[Word(word).spellcheck()[0][0] for word in texts_filtered]#拼写校正
                texts_filtered2 = [word for word in texts_filtered if word not in sr]  # 去掉停用词
                #             texts_filtered2=[word for word in texts_filtered1 if len(word)>1]#去掉单词长度小于1的单词
                texts_filtered3 = [word for word in texts_filtered2 if word not in sentimentword]  # 去掉情感词
                texts_filtered4 = [lemmatizer.lemmatize(word) for word in texts_filtered3]  # 主干还原法
                texts_filtered5 = [word for word in texts_filtered4 if len(word) > 1]  # 去掉单词长度小于1的单词
                refiltered = nltk.pos_tag(texts_filtered5)
                filtered = [w for w, pos in refiltered if
                            pos in ['NN', 'VB', "VBG", "VBD", "VBN", 'JJ', "NNS"]]  # 提取名词、动词、形容词
                #             texts_stemmed = [lemmatizer.lemmatize(word) for word in filtered] #主干还原法
                if len(filtered) >= 1:  # 提取大于1个词的评论
                    text1.append(filtered)
            except:
                print("评论预处理失败：", text)
        return text1

    # 降维列表
    def flatten(self,a):
        for each in a:
            if not isinstance(each, list):
                yield each
            else:
                yield from self.flatten(each)

    # nltk库搭配词提取
    def Cole(self,featurelist):
        featurecol1 = []
        featurecol2 = []
        featurecol3 = []
        bigram_measures = nltk.collocations.BigramAssocMeasures()  # 二元搭配词提取函数
        trigram_measures = nltk.collocations.TrigramAssocMeasures()  # 三元搭配词提取函数
        finder = BigramCollocationFinder.from_words(list(self.flatten(featurelist)))
        finder.apply_freq_filter(3)  # 过滤出现频率少于三的搭配词
        featurecol = finder.score_ngrams(bigram_measures.likelihood_ratio)
        for word, freq in featurecol:
            t = False
            for text in featurelist:
                if (word[0] in text) & (word[1] in text):
                    if (abs(text.index(word[0]) - text.index(word[1])) <= 3) & (
                            word[0] != word[1]):  # 过滤掉距离大于三的搭配词且两个搭配词不一样
                        t = True
            if t & (set(word) not in featurecol1):  # 对于顺序不一样但是相同的搭配合并操作
                l = list(word)
                l.append(freq)
                featurecol3.append(l)
                featurecol1.append(set(word))
                featurecol2.append(word)
        #     featurecol2=[list(word) for word in featurecol2]
        for i in range(len(featurecol3)):
            for j in range(i + 1, len(featurecol3)):
                try:
                    if self.issynonyms(featurecol3[i][0:2], featurecol3[j][0:2]):
                        print("%s和%s是同义词" % (
                        featurecol3[i][0] + " " + featurecol3[i][1], featurecol3[j][0] + " " + featurecol3[j][1]))
                        featurecol3.pop(j)
                except:
                    continue

        print(featurecol2)
        return featurecol3

    # 分析每一句评论的情感指数
    def RateSentiment(self, reviewslist):
        sentiment = []
        reviewslist1 = []
        for text in reviewslist:
            try:
                text = text.lower()  # 小写形式
                text = emoji.get_emoji_regexp().sub("", text)  # 去掉表情符
                reviewslist1.append(text)
            except:
                print("无法处理该评论：", text)
        SentiStrengthLocation = self.SentiStrengthLocation
        SentiStrengthLanguageFolder = self.SentiStrengthLanguageFolder
        if not os.path.isfile(SentiStrengthLocation):
            print("SentiStrength not found at: ", SentiStrengthLocation)
        if not os.path.isdir(SentiStrengthLanguageFolder):
            print("SentiStrength data folder not found at: ", SentiStrengthLanguageFolder)
        for review in reviewslist1:
            # 使用shlex打开子进程以将命令行字符串转换为正确的args列表格式
            p = subprocess.Popen(shlex.split(
                "java -jar '" + SentiStrengthLocation + "' stdin sentidata '" + SentiStrengthLanguageFolder + "'"),
                                 stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # 通过stdin通信要进行评级的字符串。请注意，所有空格都替换为+
            b = bytes(review.replace(" ", "+"), 'utf-8')  # Can't send string in Python 3, must send bytes
            stdout_byte, stderr_text = p.communicate(b)
            stdout_text = stdout_byte.decode("utf-8")  # convert from byte
            stdout_text = stdout_text.rstrip().replace("\t", " ")
            # remove the tab spacing between the positive and negative ratings. e.g. 1    -5 -> 1 -5
            if stdout_text != "":
                sentiment.append("{" + stdout_text.replace("+", "")+ "}"+review)
        return sentiment

    # 分析每一句评论情感，返回评论中词情感分以及评论情感指数
    def RateSentimentWord(self,df3):
        df3 = df3.dropna()
        df3.index=range(len(df3))
        sentiment = []
        reviewwordscore = []
        reviewslist2= []
        reviewslist=list(df3['review_text'])
        for i in range(len(reviewslist)):
            text = reviewslist[i]
            try:
                text = text.lower()  # 小写形式
                text = emoji.get_emoji_regexp().sub("", text)  # 去掉表情符
            except:
                df3=df3.drop(i,axis=0)
                print("无法处理该评论：", text)
        reviewslist1=list(df3['review_text'])
        df3.index=range(len(df3))
        SentiStrengthLocation = self.SentiStrengthLocation
        SentiStrengthLanguageFolder = self.SentiStrengthLanguageFolder
        if not os.path.isfile(SentiStrengthLocation):
            print("SentiStrength not found at: ", SentiStrengthLocation)
        if not os.path.isdir(SentiStrengthLanguageFolder):
            print("SentiStrength data folder not found at: ", SentiStrengthLanguageFolder)
        for r in range(len(reviewslist1)):
            review = reviewslist1[r]
            try:
                # 使用shlex打开子进程以将命令行字符串转换为正确的args列表格式
                p = subprocess.Popen(shlex.split(
                    "java -jar '" + SentiStrengthLocation + "' stdin sentidata '" + SentiStrengthLanguageFolder + "' explain'" + "'"),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                # 通过stdin通信要进行评级的字符串。请注意，所有空格都替换为+
                b = bytes(review.replace(" ", "+"), 'utf-8')  # Can't send string in Python 3, must send bytes
                stdout_byte, stderr_text = p.communicate(b)
                stdout_text = stdout_byte.decode("utf-8")  # convert from byte
                stdout_text = stdout_text.rstrip().replace("\t", " ")
                # remove the tab spacing between the positive and negative ratings. e.g. 1    -5 -> 1 -5
                if stdout_text != "":
                    sentiment.append("{" + stdout_text.replace("+", "")[0:4] + "}")
                    reviewwordscore.append(stdout_text.replace("+", "")[4:])
            except:
                df3=df3.drop(r, axis=0)
                continue
        return sentiment,reviewwordscore

    # 建立情感分-特征列表
    def scoredfeature(self, sentiment, sentimentword):
        scorefeature = []
        lemmatizer = WordNetLemmatizer()  # 词还原主干函数
        sr = stopwords.words('english')
        sr.extend(["app", "please", "fix", "android", "google", "youtube", "uber", "facebook"])
        english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%', '{',
                                '}', '`', '<', ">", '/', "^", "-", "_", "``", "''"]  # 标点符号列表
        for i in sentiment:
            text = emoji.get_emoji_regexp().sub("", i[7:])  # 去掉表情符
            texts_filtered = [word for word in word_tokenize(text) if not word in english_punctuations]  # 去掉标点符号
            #         texts_filtered1=[Word(word).spellcheck()[0][0] for word in texts_filtered]#拼写校正
            texts_filtered2 = [word for word in texts_filtered if not word in sr]  # 去掉停用词
            texts_filtered3 = [word for word in texts_filtered2 if not word in sentimentword]  # 去掉情感词
            texts_filtered4 = [lemmatizer.lemmatize(word) for word in texts_filtered3]  # 主干还原法
            texts_filtered5 = [word for word in texts_filtered4 if len(word) > 1]  # 去掉单词长度小于1的单词
            refiltered = nltk.pos_tag(texts_filtered5)
            filtered = [w for w, pos in refiltered if
                        pos in ['NN', 'VB', "VBG", "VBD", "VBN", 'JJ', "NNS"]]  # 提取名词、动词、形容词
            if len(filtered) >= 1:  # 提取大于1个词的评论
                filtered.insert(0, i[0:6])
                scorefeature.append(filtered)
        return scorefeature

    # 返回列表出现次数最多的函数
    def max_value(self, valuelist):
        maxValue = {}
        result = []
        for i in valuelist:
            maxValue[" ".join(i)] = valuelist.count(i)
        for key, val in maxValue.items():
            if val == max(maxValue.values()):
                result.append(key.split(" "))
        return result

    # #计算特征向量情感分-方法一
    # # 还需要比较出现在评论中的次数，选择出现次数最高的情感
    # def featurescored(featurecol,scorefeature):
    #     feature_score=[]
    #     Reviewf=[]
    #     for word in featurecol:#遍历特征词向量
    #         score=[]
    #         scorenumlist=[]
    #         reviewf=[]
    #         maxnum=0
    #         feature=word[0]+"|"+word[1]#这里只有二元词
    #         for text in scorefeature:
    #             if (word[0] in text) & (word[1] in text):#查找存在特征词的情感评论
    #                 #提取情感分绝对值最大的分数，如果正负情感分数绝对值相等，则取负值
    #                 scorenum=re.findall("[-]?\d",text[0])
    #                 scorenumlist.append(scorenum)
    #                 reviewf.append(text)
    #                 print(reviewf)
    #         Reviewf.append(reviewf)
    #         if scorenumlist != []:
    #             for scoreNum in max_value(scorenumlist):
    #                 abs_score=[abs(int(num)) for num in scoreNum]
    #                 if max(abs_score)>= maxnum:
    #                     maxnum=max(abs_score)
    #                     if abs(int(scoreNum[0]))==abs(int(scoreNum[1])):
    #                         score.append(min(scoreNum))
    #                     else:
    #                         score.append(scoreNum[abs_score.index(max(abs_score))])
    #             feature_score.append(str(min(score))+", "+word[0]+" "+word[1])
    #         else:
    #             continue
    # 计算特征向量情感分-方法二
    # 取出所在该评论的情感分，然后求和
    def featurescored(self,featurecol, scorefeature):
        feature_score = []
        for word in featurecol:  #
            scoretotal = 0  # 特征情感分总和
            feature = word[0] + "|" + word[1]  # 这里只有二元词
            for text in scorefeature:
                if (word[0] in text) & (word[1] in text):  # 查找存在特征词的情感评论
                    # 提取情感分绝对值最大的分数，如果正负情感分数绝对值相等，则取负值
                    scorenum = re.findall("[-]?\d", text[0])
                    abs_score = [abs(int(num)) for num in scorenum]
                    if abs_score[0] == abs_score[1]:
                        scoretotal = scoretotal + int(min(scorenum))
                    else:
                        scoretotal = scoretotal + int(scorenum[abs_score.index(max(abs_score))])
            feature_score.append(word[0] + " " + word[1] + ", " + str(round(word[2], 2)) + ", " + str(scoretotal))
        return feature_score

    # 取出所在该评论的情感分，然后求和
    def featurescored1(self,featurecol, scorefeature):
        feature_score = []
        for word in featurecol:  #
            scoretotal = 0  # 特征情感分总和
            feature = word[0] + "|" + word[1]  # 这里只有二元词
            for text in scorefeature:
                if (word[0] in text) & (word[1] in text):  # 查找存在特征词的情感评论
                    # 提取情感分绝对值最大的分数，如果正负情感分数绝对值相等，则取负值
                    scorenum = re.findall("[-]?\d", text[0])
                    abs_score = [abs(int(num)) for num in scorenum]
                    if abs_score[0] == abs_score[1]:
                        scoretotal = scoretotal + int(min(scorenum))
                    else:
                        scoretotal = scoretotal + int(scorenum[abs_score.index(max(abs_score))])
            feature_score.append(word[0] + " " + word[1])
        return feature_score

    # 根据time分割时间段
    def timeColname(self,df3,appname,time):
        colname = []
        app = df3[df3["product_name"] == appname]
        # 按照时间段评论分割评论
        enddate = max(app["review_date"])
        startdate = min(app["review_date"])
        datecut = []
        date = startdate
        if time <= 0:
            print("时间段太短")
            print(app["review_date"])
            return
        while date <= enddate:
            datecut.append(date)
            date = date + timedelta(time)
        for i in range(len(datecut) - 1):
            colname.append(str(datecut[i]).split(" ")[0])
        return colname

    #返回前端需要的数据类型
    def outputdata(self,df3,reviewword,appname,reviewsRating):
        colname = []
        app = df3[df3["product_name"] == appname]
        # 按照时间段评论分割评论
        enddate = max(app["review_date"])
        startdate = min(app["review_date"])
        datecut = []
        date = startdate
        reviewsweek = []
        if (enddate - startdate) / timedelta(7) < 20:
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


        feature_scorelist=[]
        for reviewlist in reviewsweek:
            featurecol=self.Cole(self.pretreat(reviewlist,reviewword))
            # print(featurecol)
            sentiment=self.RateSentiment(reviewlist)
            # print(sentiment)
            scorefeature=self.scoredfeature(sentiment,reviewword)
            print(scorefeature)
            feature_score=self.featurescored(featurecol,scorefeature)
            feature_scorelist.append(feature_score)
        print(feature_scorelist)

            # 特征对应原始评论集列表获取
        Originreviewweeks=[]
        for feature_score in feature_scorelist:
            Originreview = []
            if len(feature_score)>3:
                index=3
            else:
                index=len(feature_score)
            for i in feature_score[0:index]:
                originreview = []
                featureword = []
                print((i.split(",")[0].split(" ")))
                for t in list(set(reviewlist)):
                    try:
                        if ((i.split(",")[0].split(" ")[0]) in list(self.flatten(self.pretreat([t])))) & ((i.split(",")[0].split(" ")[1]) in list(self.flatten(self.pretreat([t])))) & (list(self.flatten(self.pretreat([t]))) not in featureword):
                            print(t)
                            featureword.append(list(self.flatten(self.pretreat([t]))))
                            originreview.append(t)
                        else:
                            continue
                    except:
                        print("error")
                try:
                    if originreview!=[]:
                        Originreview.append(min(originreview,key=len))
                except:
                    continue
            Originreviewweeks.append(Originreview)



        #时间-特征字典
        time_feature={}
        for t in range(len(colname)):
            time_feature[colname[t]]=feature_scorelist[t][0:5]


        #时间-特征演化
        reviewsweek_feature = []
        colname1 = []
        time = 7
        datecut_feature = []
        date = startdate
        while date <= enddate:
            datecut_feature.append(date)
            date = date + timedelta(time)
        # print(datecut_feature)
        for i in range(len(datecut_feature) - 1):
            print(i)
            colname1.append(str(datecut_feature[i]).split(" ")[0])
            reviewsweek_feature.append(
                                app[(app["review_date"] >= datecut_feature[i]) & (app["review_date"] < datecut_feature[i + 1])][
                                    "review_text"].values)
        print(reviewsweek_feature)
        feature_dist_lists = {}
        for i in range(len(colname1)-1):
            featurecol = self.Cole(self.pretreat(list(set(reviewsweek_feature[i])),reviewword))
            # print(featurecol)
            sentiment = self.RateSentiment(reviewsweek_feature[i])
            # print(sentiment)
            scorefeature = self.scoredfeature(sentiment,reviewword)
            feature_score = self.featurescored(featurecol, scorefeature)
            feature_dist_list = []
            if len(feature_score)>5:
                l=5
            else:
                l=len(feature_score)
            for j in range(l):
                feature_dist = {}
                feature_dist['value'] = float(feature_score[j].split(",")[1])
                feature_dist['name'] = feature_score[j].split(",")[0] + "(" + feature_score[j].split(",")[2].replace(
                    " ", "") + ")"
                feature_dist_list.append(feature_dist)
            feature_dist_lists[colname1[i]] = feature_dist_list
        print(feature_dist_lists)
        return time_feature, feature_dist_lists,Originreviewweeks


