# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 14:43:28 2019

@author: mayn
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 08:53:43 2019

@author: mayn
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 19:53:02 2019

@author: mayn
"""

from bs4 import BeautifulSoup
import re
import time
from lmf.dbv2 import db_query
import numpy as np
import pandas as pd
from sqlalchemy import Column, String, create_engine
import psycopg2

np.set_printoptions(threshold=1e10000)
pd.set_option('display.max_colwidth', 10000)


# 连接数据库
def getpage_herf_ggstart_time(quyu):
    arr = quyu.split('_')
    db, schema = arr[0], arr[1]
    engine = create_engine('postgresql+psycopg2://postgres:since2015@192.168.3.171/%s' % (db))
    data_gg = pd.read_sql_table(table_name='gg', con=engine, schema=schema, index_col=None, coerce_float=True,
                                parse_dates=None, columns=None, chunksize=None)
    data_gg_html = pd.read_sql_table(table_name='gg_html', con=engine, schema=schema, index_col=None, coerce_float=True,
                                     parse_dates=None, columns=None, chunksize=None)
    data = data_gg.merge(data_gg_html, left_on='href', right_on='href')
    df = data[['href', 'page', 'ggstart_time']]
    return df


def ext_from_ggtime(ggstart_time):
    t1 = ggstart_time
    a = re.findall('([1-9][0-9]{3})[\-\./\\年]([0-9]{1,2})[\-\./\\月]([0-9]{1,2}) ([0-9]{2}):([0-9]{2}):([0-9]{2})', t1)

    if a != []:
        y = a[0]
        x = y[0] + "-" + (y[1] if len(y[1]) == 2 else '0%s' % y[1]) + '-' + (y[2] if len(y[2]) == 2 else '0%s' % y[2])
        return x

    a = re.findall('([1-9][0-9]{3})[\-\./\\年]([0-9]{1,2})[\-\./\\月]([0-9]{1,2})', t1)
    if a != []:
        y = a[0]
        x = y[0] + "-" + (y[1] if len(y[1]) == 2 else '0%s' % y[1]) + '-' + (y[2] if len(y[2]) == 2 else '0%s' % y[2])
        return x

    a = re.findall('^([0-2][0-9])[\-\./\\年]([0-9]{1,2})[\-\./\\月]([0-9]{1,2})', t1)
    if a != []:
        y = a[0]
        x = y[0] + "-" + (y[1] if len(y[1]) == 2 else '0%s' % y[1]) + '-' + (y[2] if len(y[2]) == 2 else '0%s' % y[2])
        x = '20' + x
        return x

    a = re.findall('^(20[0-9]{2})--([0-9]{1,2})-([0-9]{1,2})', t1)

    if a != []:
        x = '-'.join([a[0][0], a[0][1] if a[0][1] != '0' else '1', a[0][2] if a[0][2] != '0' else '1'])

        return x

    if ' CST ' in t1:
        try:
            x = time.strptime(t1, '%a %b %d %H:%M:%S CST %Y')
            x = time.strftime('%Y-%m-%d %H:%M:%S', x)
        except:
            x = ''
        if x != '': return x
    a = re.findall('^(20[0-9]{6})', t1)
    if a != []:
        x = '-'.join([a[0][:4], a[0][4:6], a[0][6:8]])
        return x

    return None


# 大部分区域提取时间的格式
def extime(page):
    soup = BeautifulSoup(page, 'lxml')
    txt = re.sub('[^\u4E00-\u9Fa5a-zA-Z0-9:：\-\\/]', '', soup.text.strip())
    p = "(?:信息时间|信息日期|更新时间|发稿时间|发文时间|发文日期|发布时间|发布日期|录入时间|生成时间)(20[0-2][0-9])[\-\.年\\/]([1-9]|[0][1-9]|[1][0-2])[\-\.\\月/]([0-9]{,2})"
    a = re.findall(p, txt.replace('documentwrite', ''))
    # print(a)
    if a != []:
        return '-'.join(a[0])
    return None


# 提取特殊的时间
def strptime_transfrom_CST(page):
    soup = BeautifulSoup(page, 'lxml')
    p = "(?:信息时间|信息日期|信息发布日期|发稿时间|发布时间|生成日期)[：:\s]{,4}(.{0,20}CST.{0,5})"

    txt = soup.text

    a = re.findall(p, txt)
    if a != []:
        a = time.strptime(a[0], '%a %b %d %H:%M:%S CST %Y')
        a = time.strftime('%Y-%m-%d', a)
        return a

    return None


def strptime_transfrom_yunan(page):
    soup = BeautifulSoup(page, 'lxml')
    txt = re.sub('[^\u4E00-\u9Fa5a-zA-Z0-9:：\-\\/]', '', soup.text.strip())
    p = '(?:发布时间|提交时间|公示时间)[：:]{0,1}(20[0-2][0-9])[\-\.年\\/]([1-9]|[0][1-9]|[1][0-2])[\-\.\\月/]([0-9]{,2})'

    a = re.findall(p, txt)
    if a != []:
        return ('-'.join(a[0]))
    return None


def strptime_transfrom_jiangxi(page):
    soup = BeautifulSoup(page, 'lxml')
    txt = re.sub('^\u4E00-\u9Fa5a-zA-Z0-9:：\-\\/', '', soup.text.strip())
    p = "\[(20[0-2][0-9])[\-\.年\\/]([1-9]|[0][1-9]|[1][0-2])[\-\.\\月/]([0-9]{,2})\]"

    a = re.findall(p, txt)
    if a != []:
        return ('-'.join(a[0]))
    return None


def strptime_transfrom_yue_r_n(page):
    soup = BeautifulSoup(page, 'lxml')
    txt = re.sub('^\u4E00-\u9Fa5a-zA-Z0-9:：\-\\/', '', soup.text.strip())
    p = "(?:信息时间|信息日期|信息发布日期|发稿时间|发布时间|生成日期)[：:]([1-9]|[0][1-9]|[1][0-2])[\-\.\\月/]([0-9]{,2})[\-\.\\日/](20[0-2][0-9])"
    a = re.findall(p, txt)
    if a != []:
        return (a[0][2] + '-' + a[0][0] + '-' + a[0][1])
    return None


list_all = ['anhui_anqing',
            'anhui_bozhou',
            'anhui_huainan',
            'anhui_bengbu',
            'anhui_chaohu',
            'anhui_chizhou',
            'anhui_chuzhou',
            'anhui_fuyang',
            'anhui_huaibei',
            'anhui_huangshan',
            'anhui_maanshan',
            'anhui_suzhou',
            'anhui_tongling',
            'chongqing_chongqing',
            'anhui_xuancheng',
            'fujian_fuqing',
            'fujian_longyan',
            'fujian_ningde',
            'fujian_quanzhou',
            'fujian_wuyishan',
            'fujian_putian',
            'fujian_sanming',
            'fujian_yongan',
            'fujian_shaowu',
            'fujian_zhangzhou',
            'gansu_zhangye',
            'gansu_longnan',
            'gansu_qingyang',
            'guangdong_dongguan',
            'guangdong_guangdong',
            'guangdong_heyuan',
            'guangdong_huizhou',
            'guangdong_jiangmen',
            'guangdong_jieyang',
            'guangdong_lianzhou',
            'guangdong_maoming',
            'guangdong_meizhou',
            'guangdong_nanxiong',
            'guangdong_qingyuan',
            'guangdong_shanwei',
            'guangdong_shaoguan',
            'guangdong_sihui',
            'guangdong_yangjiang',
            'guangdong_yingde',
            'guangdong_yunfu',
            'guangdong_zhanjiang',
            'guangdong_zhaoqing',
            'guangdong_shantou',
            'guangdong_zhuhai',
            'guangxi_baise',
            'guangxi_beihai',
            'guangxi_chongzuo',
            'guangxi_fangchenggang',
            'guangxi_guangxi',
            'guangxi_guigang',
            'guangxi_guilin',
            'guangxi_hechi',
            'guangxi_laibin',
            'guangxi_liuzhou',
            'guangxi_nanning',
            'guangxi_qinzhou',
            'guangxi_wuzhou',
            'guizhou_anshun',
            'guizhou_bijie',
            'guizhou_guiyang',
            'guizhou_qiannan',
            'guizhou_qianxi',
            'guizhou_liupanshui',
            'guizhou_tongren',
            'hainan_danzhou',
            'hainan_dongfang',
            'hainan_haikou',
            'hainan_hainan',
            'hainan_sansha',
            'hainan_qionghai',
            'hainan_sanya',
            'heilongjiang_daqing',
            'heilongjiang_hegang',
            'henan_anyang',
            'henan_dengfeng',
            'henan_gongyi',
            'henan_hebi',
            'henan_linzhou',
            'henan_luohe',
            'henan_luoyang',
            'henan_nanyang',
            'henan_puyang',
            'henan_sanmenxia',
            'henan_shangqiu',
            'henan_weihui',
            'henan_xinxiang',
            'henan_xinyang',
            'henan_xinzheng',
            'henan_yanshi',
            'henan_zhengzhou',
            'henan_zhoukou',
            'henan_zhumadian',
            'hubei_huangshi',
            'hubei_jingmen',
            'hubei_suizhou',
            'hunan_changde',
            'hunan_changsha',
            'hunan_chenzhou',
            'hunan_hengyang',
            'hunan_huaihua',
            'hunan_liling',
            'hunan_liuyang',
            'hunan_shaoyang',
            'hunan_xiangtan',
            'hunan_yiyang',
            'hunan_yongzhou',
            'hunan_zhuzhou',
            'jiangsu_changshu',
            'jiangsu_changzhou',
            'jiangsu_danyang',
            'jiangsu_dongtai',
            'jiangsu_huaian',
            'jiangsu_jiangsu',
            'jiangsu_jiangyin',
            'jiangsu_kunshan',
            'jiangsu_lianyungang',
            'jiangsu_nanjing',
            'jiangsu_nantong',
            'jiangsu_suqian',
            'jiangsu_suzhou',
            'jiangsu_taizhou',
            'jiangsu_xinyi',
            'jiangsu_xuzhou',
            'jiangsu_yangzhou',
            'jiangsu_zhangjiagang',
            'jiangsu_zhenjiang',
            'jiangxi_ganzhou',
            'jiangxi_jian',
            'jiangxi_jiangxi',
            'jiangxi_jingdezhen',
            'jiangxi_jinggangshan',
            'jiangxi_lushan',
            'jiangxi_ruichang',
            'jiangxi_ruijin',
            'jiangxi_yingtan',
            'jilin_baicheng',
            'liaoning_anshan',
            'liaoning_chaoyang',
            'liaoning_dalian',
            'liaoning_dandong',
            'liaoning_donggang',
            'liaoning_fuxin',
            'liaoning_huludao',
            'liaoning_liaoyang',
            'liaoning_panjin',
            'liaoning_jinzhou',
            'neimenggu_alashan',
            'neimenggu_baotou',
            'neimenggu_bayannaoer',
            'neimenggu_eeduosi',
            'neimenggu_huhehaote',
            'neimenggu_hulunbeier',
            'neimenggu_manzhouli',
            'neimenggu_neimenggu',
            'neimenggu_tongliao',
            'neimenggu_wuhai',
            'neimenggu_wulanchabu',
            'neimenggu_chifeng',
            'neimenggu_xinganmeng',
            'qinghai_xining',
            'shandong_anqiu',
            'shandong_binzhou',
            'shandong_feicheng',
            'shandong_jinan',
            'shandong_linqing',
            'shandong_rizhao',
            'shandong_rongcheng',
            'shandong_shandong',
            'shandong_taian',
            'shandong_weifang',
            'shandong_xintai',
            'shandong_yucheng',
            'shandong_dezhou',
            'shandong_weihai',
            'shandong_zibo',
            'shanxi_shenghui',
            'shanxi_weinan',
            'shanxi_xianyang',
            'shanxi_yanan',
            'sichuan_bazhong',
            'sichuan_dazhou',
            'sichuan_deyang',
            'sichuan_dujiangyan',
            'sichuan_guangan',
            'sichuan_guanghan',
            'sichuan_guangyuan',
            'sichuan_leshan',
            'sichuan_luzhou',
            'sichuan_meishan',
            'sichuan_nanchong',
            'sichuan_pengzhou',
            'sichuan_qionglai',
            'sichuan_shifang',
            'sichuan_sichuan',
            'sichuan_sichuan2',
            'sichuan_suining',
            'sichuan_wanyuan',
            'sichuan_yaan',
            'xinjiang_akesu',
            'xinjiang_wulumuqi',
            'xinjiang_xinjiang',
            'xizang_xizang',
            'yunnan_kunming',
            'zhejiang_cixi',
            'zhejiang_huzhou',
            'zhejiang_jiaxing',
            'zhejiang_jinhua',
            'zhejiang_lishui',
            'zhejiang_ningbo',
            'zhejiang_pinghu',
            'zhejiang_ruian',
            'zhejiang_shaoxing',
            'zhejiang_shengzhou',
            'zhejiang_wenzhou',
            'zhejiang_yiwu',
            'zhejiang_yueqing',
            'zhejiang_zhejiang',
            'zhejiang_zhoushan',
            'zhejiang_zhuji',
            'beijing_beijing',
            'anhui_hefei',
            'anhui_luan',
            'anhui_wuhu',
            'chongqing_yongchuan',
            'fujian_fuzhou',
            'fujian_xiamen',
            'fujian_jianou',
            'gansu_lanzhou',
            'guangdong_zhongshan',
            'guizhou_qiandong',
            'hebei_hebei',
            'heilongjiang_heilongjiang',
            'heilongjiang_yichun',
            'henan_kaifeng',
            'henan_mengzhou',
            'henan_pingdingshan',
            'henan_ruzhou',
            'henan_wugang',
            'henan_xinmi',
            'henan_yongcheng',
            'hubei_dangyang',
            'hubei_enshi',
            'hubei_lichuan',
            'hubei_xiaogan',
            'hubei_yichang',
            'hubei_yidu',
            'hunan_yueyang',
            'hunan_zhangjiajie',
            'jiangxi_dexing',
            'jiangxi_fengcheng',
            'jiangxi_fuzhou',
            'jiangxi_nanchang',
            'jiangxi_xinyu',
            'jiangxi_yichun',
            'jiangxi_zhangshu',
            'jilin_baishan',
            'jilin_changchun',
            'jilin_jilinshi',
            'jilin_siping',
            'jilin_songyuan',
            'jilin_jilin',
            'jilin_tonghua',
            'ningxia_ningxia',
            'ningxia_yinchuan',
            'qinghai_qinghai',
            'shandong_heze',
            'shandong_jiaozhou',
            'shandong_laiwu',
            'shandong_linyi',
            'shandong_pingdu',
            'shandong_rushan',
            'shandong_zaozhuang',
            'sichuan_jiangyou',
            'sichuan_yibin',
            'xizang_lasa',
            'zhejiang_longquan',
            'zhejiang_yuhuan',
            'zhejiang_dongyang',
            'guangxi_hezhou',
            'yunnan_tengchong'
            'shanxi_chenzhou',
            'fujian_nanan',
            'fujian_nanping',
            'gansu_baiyin',
            'gansu_jiuquan',
            'gansu_pingliang',
            'gansu_wuwei',
            'gansu_longan',
            'gansu_gansu',
            'gansu_tianshui',
            'gansu_dingxi',
            'gansu_jiayuguan',
            'guangdong_chaozhou',
            'heilongjiang_qiqihaer',
            'henan_xuchang',
            'henan_jiaozhuo',
            'henan_jiyuan',
            'henan_qinyang',
            'hubei_shiyan',
            'hubei_xiangyang',
            'hunan_loudi',
            'hunan_yuanjiang',
            'jiangxi_ganzhou',
            'jiangxi_shangrao',
            'liaoning_haicheng',
            'liaoning_liaoning',
            'liaoning_yingkou',
            'shandong_leling',
            'shandong_qingdao',
            'shandong_qufu',
            'shandong_jining',
            'shandong_liaocheng',
            'shandong_zoucheng',
            'shandong_tengzhou',
            'sichuan_longchang',
            'sichuan_mianyang1',
            'sichuan_chengdu',
            'sichuan_chongzhou',
            'sichuan_jianyang',
            'sichuan_mianyang2',
            'xizang_rikaze',
            'yunnan_tengchong',
            'zhejiang_linhai',
            'zhejiang_hangzhou',
            'yunnan_yunnan',
            'jiangxi_gaoan',
            'yunnan_baoshan',
            'yunnan_chuxiong',
            'yunnan_wenshan',
            'yunnan_xishuangbanna',
            'yunnan_yunnan2',
            'yunnan_yuxi',
            'yunnan_zhaotong'
            ]

list_page_time = [
    'anhui_anqing',
    'anhui_bozhou',
    'anhui_huainan',
    'anhui_bengbu',
    'anhui_chaohu',
    'anhui_chizhou',
    'anhui_chuzhou',
    'anhui_fuyang',
    'anhui_huaibei',
    'anhui_huangshan',
    'anhui_maanshan',
    'anhui_suzhou',
    'anhui_tongling',
    'chongqing_chongqing',
    'anhui_xuancheng',
    'fujian_fuqing',
    'fujian_longyan',
    'fujian_ningde',
    'fujian_quanzhou',
    'fujian_wuyishan',
    'fujian_putian',
    'fujian_sanming',
    'fujian_yongan',
    'fujian_shaowu',
    'fujian_zhangzhou',
    'gansu_zhangye',
    'gansu_longnan',
    'gansu_qingyang',
    'guangdong_dongguan',
    'guangdong_guangdong',
    'guangdong_heyuan',
    'guangdong_huizhou',
    'guangdong_jiangmen',
    'guangdong_jieyang',
    'guangdong_lianzhou',
    'guangdong_maoming',
    'guangdong_meizhou',
    'guangdong_nanxiong',
    'guangdong_qingyuan',
    'guangdong_shanwei',
    'guangdong_shaoguan',
    'guangdong_sihui',
    'guangdong_yangjiang',
    'guangdong_yingde',
    'guangdong_yunfu',
    'guangdong_zhanjiang',
    'guangdong_zhaoqing',
    'guangdong_shantou',
    'guangdong_zhuhai',
    'guangxi_baise',
    'guangxi_beihai',
    'guangxi_chongzuo',
    'guangxi_fangchenggang',
    'guangxi_guangxi',
    'guangxi_guigang',
    'guangxi_guilin',
    'guangxi_hechi',
    'guangxi_laibin',
    'guangxi_liuzhou',
    'guangxi_nanning',
    'guangxi_qinzhou',
    'guangxi_wuzhou',
    'guizhou_anshun',
    'guizhou_bijie',
    'guizhou_guiyang',
    'guizhou_qiannan',
    'guizhou_qianxi',
    'guizhou_liupanshui',
    'guizhou_tongren',
    'hainan_danzhou',
    'hainan_dongfang',
    'hainan_haikou',
    'hainan_hainan',
    'hainan_sansha',
    'hainan_qionghai',
    'hainan_sanya',
    'heilongjiang_daqing',
    'heilongjiang_hegang',
    'henan_anyang',
    'henan_dengfeng',
    'henan_gongyi',
    'henan_hebi',
    'henan_linzhou',
    'henan_luohe',
    'henan_luoyang',
    'henan_nanyang',
    'henan_puyang',
    'henan_sanmenxia',
    'henan_shangqiu',
    'henan_weihui',
    'henan_xinxiang',
    'henan_xinyang',
    'henan_xinzheng',
    'henan_yanshi',
    'henan_zhengzhou',
    'henan_zhoukou',
    'henan_zhumadian',
    'hubei_huangshi',
    'hubei_jingmen',
    'hubei_suizhou',
    'hunan_changde',
    'hunan_changsha',
    'hunan_chenzhou',
    'hunan_hengyang',
    'hunan_huaihua',
    'hunan_liling',
    'hunan_liuyang',
    'hunan_shaoyang',
    'hunan_xiangtan',
    'hunan_yiyang',
    'hunan_yongzhou',
    'hunan_zhuzhou',
    'jiangsu_changshu',
    'jiangsu_changzhou',
    'jiangsu_danyang',
    'jiangsu_dongtai',
    'jiangsu_huaian',
    'jiangsu_jiangsu',
    'jiangsu_jiangyin',
    'jiangsu_kunshan',
    'jiangsu_lianyungang',
    'jiangsu_nanjing',
    'jiangsu_nantong',
    'jiangsu_suqian',
    'jiangsu_suzhou',
    'jiangsu_taizhou',
    'jiangsu_xinyi',
    'jiangsu_xuzhou',
    'jiangsu_yangzhou',
    'jiangsu_zhangjiagang',
    'jiangsu_zhenjiang',
    'jiangxi_ganzhou',
    'jiangxi_jian',
    'jiangxi_jiangxi',
    'jiangxi_jingdezhen',
    'jiangxi_jinggangshan',
    'jiangxi_lushan',
    'jiangxi_ruichang',
    'jiangxi_ruijin',
    'jiangxi_yingtan',
    'jilin_baicheng',
    'liaoning_anshan',
    'liaoning_chaoyang',
    'liaoning_dalian',
    'liaoning_dandong',
    'liaoning_donggang',
    'liaoning_fuxin',
    'liaoning_huludao',
    'liaoning_liaoyang',
    'liaoning_panjin',
    'liaoning_jinzhou',
    'neimenggu_alashan',
    'neimenggu_baotou',
    'neimenggu_bayannaoer',
    'neimenggu_eeduosi',
    'neimenggu_huhehaote',
    'neimenggu_hulunbeier',
    'neimenggu_manzhouli',
    'neimenggu_neimenggu',
    'neimenggu_tongliao',
    'neimenggu_wuhai',
    'neimenggu_wulanchabu',
    'neimenggu_chifeng',
    'neimenggu_xinganmeng',
    'qinghai_xining',
    'shandong_anqiu',
    'shandong_binzhou',
    'shandong_feicheng',
    'shandong_jinan',
    'shandong_linqing',
    'shandong_rizhao',
    'shandong_rongcheng',
    'shandong_shandong',
    'shandong_taian',
    'shandong_weifang',
    'shandong_xintai',
    'shandong_yucheng',
    'shandong_dezhou',
    'shandong_weihai',
    'shandong_zibo',
    'shanxi_shenghui',
    'shanxi_weinan',
    'shanxi_xianyang',
    'shanxi_yanan',
    'sichuan_bazhong',
    'sichuan_dazhou',
    'sichuan_deyang',
    'sichuan_dujiangyan',
    'sichuan_guangan',
    'sichuan_guanghan',
    'sichuan_guangyuan',
    'sichuan_leshan',
    'sichuan_luzhou',
    'sichuan_meishan',
    'sichuan_nanchong',
    'sichuan_pengzhou',
    'sichuan_qionglai',
    'sichuan_shifang',
    'sichuan_sichuan',
    'sichuan_sichuan2',
    'sichuan_suining',
    'sichuan_wanyuan',
    'sichuan_yaan',
    'xinjiang_akesu',
    'xinjiang_wulumuqi',
    'xinjiang_xinjiang',
    'xizang_xizang',
    'yunnan_kunming',
    'zhejiang_cixi',
    'zhejiang_huzhou',
    'zhejiang_jiaxing',
    'zhejiang_jinhua',
    'zhejiang_lishui',
    'zhejiang_ningbo',
    'zhejiang_pinghu',
    'zhejiang_ruian',
    'zhejiang_shaoxing',
    'zhejiang_shengzhou',
    'zhejiang_wenzhou',
    'zhejiang_yiwu',
    'zhejiang_yueqing',
    'zhejiang_zhejiang',
    'zhejiang_zhoushan',
    'zhejiang_zhuji',
    'beijing_beijing']

list_page_notime = [
    'anhui_hefei',
    'anhui_luan',
    'anhui_wuhu',
    'chongqing_yongchuan',
    'fujian_fuzhou',
    'fujian_xiamen',
    'fujian_jianou',
    'gansu_lanzhou',
    'guangdong_zhongshan',
    'guizhou_qiandong',
    'hebei_hebei',
    'heilongjiang_heilongjiang',
    'heilongjiang_yichun',
    'henan_kaifeng',
    'henan_mengzhou',
    'henan_pingdingshan',
    'henan_ruzhou',
    'henan_wugang',
    'henan_xinmi',
    'henan_yongcheng',
    'hubei_dangyang',
    'hubei_enshi',
    'hubei_lichuan',
    'hubei_xiaogan',
    'hubei_yichang',
    'hubei_yidu',
    'hunan_yueyang',
    'hunan_zhangjiajie',
    'jiangxi_dexing',
    'jiangxi_fengcheng',
    'jiangxi_fuzhou',
    'jiangxi_nanchang',
    'jiangxi_xinyu',
    'jiangxi_yichun',
    'jiangxi_zhangshu',
    'jilin_baishan',
    'jilin_changchun',
    'jilin_jilinshi',
    'jilin_siping',
    'jilin_songyuan',
    'jilin_jilin',
    'jilin_tonghua',
    'ningxia_ningxia',
    'ningxia_yinchuan',
    'qinghai_qinghai',
    'shandong_heze',
    'shandong_jiaozhou',
    'shandong_laiwu',
    'shandong_linyi',
    'shandong_pingdu',
    'shandong_rushan',
    'shandong_zaozhuang',
    'sichuan_jiangyou',
    'sichuan_yibin',
    'xizang_lasa',
    'zhejiang_longquan',
    'zhejiang_yuhuan',
    'zhejiang_dongyang',
    'guangxi_hezhou',
    'yunnan_tengchong'
    'shanxi_chenzhou',
    'fujian_nanan',
    'fujian_nanping',
    'gansu_baiyin',
    'gansu_jiuquan',
    'gansu_pingliang',
    'gansu_wuwei',
    'gansu_longan',
    'gansu_gansu',
    'gansu_tianshui',
    'gansu_dingxi',
    'gansu_jiayuguan',
    'guangdong_chaozhou',
    'heilongjiang_qiqihaer',
    'henan_xuchang',
    'henan_jiaozhuo',
    'henan_jiyuan',
    'henan_qinyang',
    'hubei_shiyan',
    'hubei_xiangyang',
    'hunan_loudi',
    'hunan_yuanjiang',
    'jiangxi_ganzhou',
    'jiangxi_shangrao',
    'liaoning_haicheng',
    'liaoning_liaoning',
    'liaoning_yingkou',
    'shandong_leling',
    'shandong_qingdao',
    'shandong_qufu',
    'shandong_jining',
    'shandong_liaocheng',
    'shandong_zoucheng',
    'shandong_tengzhou',
    'sichuan_longchang',
    'sichuan_mianyang1',
    'sichuan_chengdu',
    'sichuan_chongzhou',
    'sichuan_jianyang',
    'sichuan_mianyang2',
    'xizang_rikaze',
    'yunnan_tengchong',
    'zhejiang_linhai',
    'zhejiang_hangzhou',
    'yunnan_yunnan']

list_page_yunan = ['yunnan_baoshan',
                   'yunnan_chuxiong',
                   'yunnan_wenshan',
                   'yunnan_xishuangbanna',
                   'yunnan_yunnan2',
                   'yunnan_yuxi',
                   'yunnan_zhaotong'
                   ]


def extime_all(page, ggstart_time, quyu):
    if quyu in list_page_time:
        if extime(page) is not None:
            return extime(page)
        elif strptime_transfrom_CST(page):
            return strptime_transfrom_CST(page)
        elif ggstart_time is not None:
            return ggstart_time
        else:
            return None
    elif quyu in list_page_notime:
        if ggstart_time is not None:
            return ggstart_time
        else:
            return None
    elif quyu in list_page_yunan:
        if strptime_transfrom_yunan(page) is not None:
            return strptime_transfrom_yunan(page)
        elif ggstart_time is not None:
            return extime(page)
        else:
            return None
    elif quyu in ['jiangxi_gaoan']:
        if strptime_transfrom_jiangxi(page) is not None:
            return strptime_transfrom_jiangxi(page)
        elif ggstart_time is not None:
            return ggstart_time
        else:
            return None


# 读入数据
def write_to_table(df, table_name, quyu, if_exists='replace'):
    import io
    import pandas as pd
    from sqlalchemy import create_engine
    arr = quyu.split('_')
    db, schema = arr[0], arr[1]
    db_engine = create_engine('postgresql+psycopg2://postgres:since2015@192.168.3.171/%s' % db)
    string_data_io = io.StringIO()
    df.to_csv(string_data_io, sep='|', index=False)
    pd_sql_engine = pd.io.sql.pandasSQL_builder(db_engine)
    table = pd.io.sql.SQLTable(table_name, pd_sql_engine, frame=df,
                               index=False, if_exists=if_exists, schema=schema)
    table.create()
    string_data_io.seek(0)
    string_data_io.readline()  # remove header
    with db_engine.connect() as connection:
        with connection.connection.cursor() as cursor:
            copy_cmd = "COPY %s.%s FROM STDIN HEADER DELIMITER '|' CSV" % (schema, table_name)
            cursor.copy_expert(copy_cmd, string_data_io)
        connection.connection.commit()


if __name__ == '__main__':
    for quyu in list_all:
        # 链接数据库,读取数据
        df = getpage_herf_ggstart_time(quyu)
        df.drop_duplicates(['href', 'ggstart_time'], inplace=True)
        df_count = pd.pivot_table(df, index=["href"], values=["ggstart_time"], aggfunc=[len])
        df_count.reset_index(inplace=True)
        df_count.columns = ['href', 'ggstart_time_cnt']
        df = df.merge(df_count, left_on='href', right_on='href')
        df['ggstart_time'] = df['ggstart_time'].map(lambda x: ext_from_ggtime(x))
        df['ggstart_time'] = df['ggstart_time'].map(lambda x: x if x is not None else '')
        # print(df.head(2))
        # 传入参数
        df['data'] = (df['page'].map(lambda x: x if x is not None else '') + '##shm##'
                      + df['ggstart_time'].map(lambda x: x if x is not None else '')
                      + "##shm##%s" % quyu).map(
            lambda x: extime_all(*x.split("##shm##")) if extime_all(*x.split("##shm##")) is not None else
            x.split("##shm##")[1])
        df['data'] = df['data'].map(lambda x: x if x is not None else '')
        df['data'] = df['data'].map(lambda x: ext_from_ggtime(x))
        # 如何一个网页有两个时间，那么展示时间直接去GG表的时间
        # print(1,df['data'][df['ggstart_time_cnt'] > 1])
        if df['ggstart_time_cnt'].max() > 1:
            df['data'][df['ggstart_time_cnt'] > 1] = df['ggstart_time'][df['ggstart_time_cnt'] > 1]
        write_to_table(df, 'gg_time', quyu, if_exists='replace')

