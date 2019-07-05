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
    arr = quyu.split('.')
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

    p = "(?:信息时间|信息日期|更新时间|发稿时间|发文时间|发文日期|发布时间|发布日期)(20[0-2][0-9])[\-\.年\\/]([1-9]|[0][1-9]|[1][0-2])[\-\.\\月/]([0-9]{,2})"
    a = re.findall(p, txt.replace('documentwrite', ''))

    if a != []:
        return '-'.join(a[0])
    return None


def strptime_transfrom_nokey(page):
    soup = BeautifulSoup(page, 'lxml')
    txt = soup.text
    parterns = [
        "(?:更新时间|发布时间|发布|加入时间|信息提供日期)[：:]{0,1}(20[0-2][0-9])[\-\.年\\/]([1-9]|[0][1-9]|[1][0-2])[\-\.\\月/]([0-9]{,2})",
        "(20[0-2][0-9])[\-\.年\\/]{0,1}([1-9]|[0][1-9]|[1][0-2])[\-\.\\月/]{0,1}([0-9]{,2})(?:发布)"
    ]
    for p in parterns:
        a = re.findall(p, txt.replace('varstrvarstr1', ''))
        if a != []:
            return '-'.join(a[0])
    return None


##不去掉空格
def strptime_transfrom_nospace(page):
    soup = BeautifulSoup(page, 'lxml')
    txt = soup.text
    p = "(?:更新时间|发布时间)[：:]{0,1}.{0,2}(20[0-2][0-9])[\-\.年\\/]([1-9]|[0][1-9]|[1][0-2])[\-\.\\月/]([0-9]{,2})"
    a = re.findall(p, txt)

    if a != []:
        return '-'.join(a[0])
    return None


list_all = ['gcjs.anhui_huainan',
            'gcjs.anhui_xuancheng',
            'gcjs.guangxi_beihai',
            'gcjs.guangxi_qinzhou',
            'gcjs.guangxi_shenghui',
            'gcjs.hebei_shijiazhuang',
            'gcjs.hebei_tangshan',
            'gcjs.henan_pingdingshan',
            'gcjs.henan_zhengzhou',
            'gcjs.hunan_loudi',
            'gcjs.jiangsu_changzhou',
            'gcjs.jiangsu_nanjing',
            'gcjs.shandong_dongying',
            'gcjs.shandong_rizhao',
            'gcjs.shandong_zaozhuang',
            'gcjs.shanxi_ankang',
            'gcjs.shanxi_xianyang',
            'gcjs.shanxi_yanan',
            'gcjs.sichuan_zigong',
            'gcjs.xinjiang_hami',
            'gcjs.zhejiang_huzhou',
            'gcjs.zhejiang_jinhua',
            'gcjs.zhejiang_zhoushan',
            'zfcg.anhui_shenghui',
            'zfcg.fujian_fuzhou',
            'zfcg.fujian_longyan',
            'zfcg.fujian_ningde',
            'zfcg.fujian_putian',
            'zfcg.fujian_quanzhou',
            'zfcg.fujian_sanming1',
            'zfcg.fujian_xiamen',
            'zfcg.fujian_zhangzhou',
            'zfcg.gansu_jinchang',
            'zfcg.gansu_shenghui',
            'zfcg.guangxi_guilin',
            'zfcg.guangxi_liuzhou',
            'zfcg.guangxi_nanning',
            'zfcg.guangxi_shenghui',
            'zfcg.guizhou_shenghui',
            'zfcg.guizhou_tongren',
            'zfcg.hainan_haikou',
            'zfcg.hainan_shenghui',
            'zfcg.hainan_wenchang',
            'zfcg.heibei_shenghui',
            'zfcg.heilongjiang_shenghui',
            'zfcg.heilongjiang_yichun',
            'zfcg.hubei_huanggang',
            'zfcg.hubei_hubei',
            'zfcg.hubei_shiyan',
            'zfcg.hunan_changde',
            'zfcg.jiangsu_changzhou',
            'zfcg.jiangsu_huaian',
            'zfcg.jiangsu_lianyungang',
            'zfcg.jiangsu_nanjing',
            'zfcg.jiangsu_nantong',
            'zfcg.jiangsu_xuzhou',
            'zfcg.jiangsu_xuzhou2',
            'zfcg.jiangsu_zhenjiang',
            'zfcg.jiangxi_jian',
            'zfcg.jilin_jilin',
            'zfcg.jilin_shenghui',
            'zfcg.liaoning_changchun',
            'zfcg.liaoning_chaoyang',
            'zfcg.neimenggu_eerduosi',
            'zfcg.neimenggu_tongliao',
            'zfcg.qinghai_shenghui',
            'zfcg.shandong_rizhao',
            'zfcg.shanxi_shenghui',
            'zfcg.shanxi1_changzhi',
            'zfcg.shanxi1_shenghui',
            'zfcg.sichuan_shenghui',
            'zfcg.xinjiang_alashankou',
            'zfcg.xinjiang_shenghui2',
            'zfcg.shanxi_hanzhong',
            'zfcg.xizang_shenghui',
            'zfcg.zhejiang_hangzhou',
            'zfcg.zhejiang_quzhou',
            'zfcg.zhejiang_shenghui',
            'qycg.b2bcoal_crp_net_cn',
            'qycg.bid_ansteel_cn',
            'qycg.bid_powerchina_cn',
            'qycg.buy_cnooc_com_cn',
            'qycg.csbidding_csair_com',
            'qycg.dzzb_ciesco_com_cn',
            'qycg.www_cdt_eb_com',
            'qycg.www_mgzbzx_com',
            'qycg.www_qhbidding_com',
            'qycg.www_sztc_com',
            'qycg.www_wiscobidding_com_cn',
            'qycg.www_ykjtzb_com',
            'qycg.www_zeec_cn',
            'qycg.www_zmzb_com',
            'qycg.wzcgzs_95306_cn',
            'qycg.zb_crlintex_com',
            'gcjs.fujian_sanming',
            'gcjs.jilin_siping',
            'gcjs.shanxi_yulin',
            'zfcg.beijing_beijing',
            'zfcg.guangdong_shantou',
            'zfcg.guangxi_fangchenggang',
            'zfcg.guangxi_wuzhou',
            'zfcg.hunan_changsha2',
            'zfcg.jiangxi_jiangxi',
            'zfcg.neimenggu_bayannaoer',
            'zfcg.shandong_liaocheng',
            'zfcg.shandong_qingdao',
            'zfcg.xinjiang_changji',
            'zfcg.xizang_shannan',
            'zfcg.ningxia_yinchuan',
            'zfcg.xizang_shannan',
            'zfcg.xinjiang_changji2',
            'gcjs.guangdong_zhongshan',
            'gcjs.hebei_langfang',
            'gcjs.hunan_huaihua',
            'gcjs.jilin_jilin',
            'gcjs.jilin_tonghua',
            'gcjs.liaoning_shenyang',
            'gcjs.neimenggu_shenghui',
            'gcjs.shanxi_baoji',
            'gcjs.shanxi1_taiyuan',
            'gcjs.shanxi1_xinzhou2',
            'zfcg.jiangsu_wuxi',
            'zfcg.shanxi1_taiyuan',
            'qycg.www_namkwong_com_mo',
            'qycg.www_sinochemitc_com',
            'gcjs.gansu_shenghui',
            'zfcg.anhui_wuhu',
            'zfcg.guangxi_baise',
            'zfcg.sichuan_mianyang',
            'zfcg.xinjiang_hetian',
            'qycg.www_dlztb_com',
            'gcjs.fujian_zhangzhou',
            'gcjs.henan_kaifeng',
            'gcjs.hunan_changsha1',
            'gcjs.hunan_changsha2',
            'gcjs.hunan_shaoyang',
            'gcjs.hunan_wugang',
            'gcjs.hunan_yueyang',
            'gcjs.jiangxi_jiujiang',
            'gcjs.shandong_jinan',
            'gcjs.shandong_linyi',
            'zfcg.fujian_nanping',
            'zfcg.henan_hebi',
            'zfcg.henan_henan',
            'zfcg.henan_jiaozuo',
            'zfcg.henan_kaifeng',
            'zfcg.henan_luohe',
            'zfcg.henan_luoyang',
            'zfcg.henan_nanyang',
            'zfcg.henan_pingdingshan',
            'zfcg.henan_puyang',
            'zfcg.henan_sanmenxia',
            'zfcg.henan_shangqiu',
            'zfcg.henan_xinxiang',
            'zfcg.henan_xinyang',
            'zfcg.henan_xuchang',
            'zfcg.henan_zhengzhou',
            'zfcg.henan_zhoukou',
            'zfcg.henan_zhumadian',
            'zfcg.hunan_changsha',
            'zfcg.hunan_xiangtan',
            'zfcg.shandong_yantai',
            'qycg.dzzb_ciesco_com_cn',
            'qycg.epp_ctg_com_cn',
            'qycg.jzcg_cfhi_com',
            'qycg.thzb_crsc_cn',
            'qycg.www_bidding_csg_cn',
            'qycg.www_china_tender_com_cn',
            'qycg.www_chinabidding_com',
            'qycg.www_dlzb_com',
            'qycg.www_dlzb_com_c1608',
            'qycg.www_ngecc_com',
            'gcjs.fujian_fuqing',
            'gcjs.fujian_fuzhou',
            'gcjs.fujian_quanzhou',
            'gcjs.guangdong_shantou',
            'gcjs.guangdong_shaoguan',
            'gcjs.guangdong_shenzhen',
            'gcjs.guangxi_shenghui',
            'gcjs.hebei_shenghui',
            'gcjs.heilongjiang_haerbin',
            'gcjs.heilongjiang_qqhaer',
            'gcjs.heilongjiang_shenghui',
            'gcjs.jiangsu_nantong',
            'gcjs.shandong_heze',
            'gcjs.shanxi1_changzhi',
            'gcjs.shanxi1_datong',
            'zfcg.guangdong_guangzhou',
            'zfcg.hainan_sanya',
            'zfcg.hubei_ezhou',
            'zfcg.hubei_wuhan',
            'zfcg.jiangsu_shenghui',
            'zfcg.jiangsu_suqian',
            'zfcg.jiangsu_yangzhou',
            'zfcg.jilin_shenghui',
            'zfcg.liaoning_shenyang',
            'zfcg.shandong_dongying',
            'zfcg.shandong_laiwu',
            'zfcg.shandong_linyi',
            'zfcg.tianjin_tianjin',
            'zfcg.tianjin_tianjin',
            'qycg.ec1_mcc_com_cn',
            'qycg.ec_ceec_net_cn',
            'qycg.ec_chalieco_com',
            'qycg.ecp_sgcc_com_cn',
            'qycg.eps_sdic_com_cn',
            'qycg.fwgs_sinograin_com_cn',
            'qycg.gs_coscoshipping_com',
            'qycg.srm_crland_com_cn',
            'qycg.uat_ec_chng_com_cn',
            'qycg.www_cnpcbidding_com',
            'qycg.www_gmgitc_com',
            'zfcg.hunan_chenzhou',
            'zfcg.hunan_hengyang',
            'zfcg.hunan_loudi',
            'zfcg.hunan_yiyang',
            'zfcg.hunan_yueyang',
            'zfcg.hunan_zhangjiajie',
            'qycg.bidding_crmsc_com_cn',
            'gcjs.guangdong_shaoguan',
            'gcjs.guangdong_shenghui',
            'gcjs.guangdong_yunfu',
            'zfcg.guangdong_shenzhen',
            'zfcg.liaoning_wafangdian',
            'qycg.www_chdtp_com',
            'gcjs.guangxi_beihai',
            'gcjs.guangxi_fangchenggang',
            'zfcg.shanxi1_yuncheng']

list_page_time = ['gcjs.anhui_huainan',
                  'gcjs.anhui_xuancheng',
                  'gcjs.guangxi_beihai',
                  'gcjs.guangxi_qinzhou',
                  'gcjs.guangxi_shenghui',
                  'gcjs.hebei_shijiazhuang',
                  'gcjs.hebei_tangshan',
                  'gcjs.henan_pingdingshan',
                  'gcjs.henan_zhengzhou',
                  'gcjs.hunan_loudi',
                  'gcjs.jiangsu_changzhou',
                  'gcjs.jiangsu_nanjing',
                  'gcjs.shandong_dongying',
                  'gcjs.shandong_rizhao',
                  'gcjs.shandong_zaozhuang',
                  'gcjs.shanxi_ankang',
                  'gcjs.shanxi_xianyang',
                  'gcjs.shanxi_yanan',
                  'gcjs.sichuan_zigong',
                  'gcjs.xinjiang_hami',
                  'gcjs.zhejiang_huzhou',
                  'gcjs.zhejiang_jinhua',
                  'gcjs.zhejiang_zhoushan',
                  'zfcg.anhui_shenghui',
                  'zfcg.fujian_fuzhou',
                  'zfcg.fujian_longyan',
                  'zfcg.fujian_ningde',
                  'zfcg.fujian_putian',
                  'zfcg.fujian_quanzhou',
                  'zfcg.fujian_sanming1',
                  'zfcg.fujian_xiamen',
                  'zfcg.fujian_zhangzhou',
                  'zfcg.gansu_jinchang',
                  'zfcg.gansu_shenghui',
                  'zfcg.guangxi_guilin',
                  'zfcg.guangxi_liuzhou',
                  'zfcg.guangxi_nanning',
                  'zfcg.guangxi_shenghui',
                  'zfcg.guizhou_shenghui',
                  'zfcg.guizhou_tongren',
                  'zfcg.hainan_haikou',
                  'zfcg.hainan_shenghui',
                  'zfcg.hainan_wenchang',
                  'zfcg.heibei_shenghui',
                  'zfcg.heilongjiang_shenghui',
                  'zfcg.heilongjiang_yichun',
                  'zfcg.hubei_huanggang',
                  'zfcg.hubei_hubei',
                  'zfcg.hubei_shiyan',
                  'zfcg.hunan_changde',
                  'zfcg.jiangsu_changzhou',
                  'zfcg.jiangsu_huaian',
                  'zfcg.jiangsu_lianyungang',
                  'zfcg.jiangsu_nanjing',
                  'zfcg.jiangsu_nantong',
                  'zfcg.jiangsu_xuzhou',
                  'zfcg.jiangsu_xuzhou2',
                  'zfcg.jiangsu_zhenjiang',
                  'zfcg.jiangxi_jian',
                  'zfcg.jilin_jilin',
                  'zfcg.jilin_shenghui',
                  'zfcg.liaoning_changchun',
                  'zfcg.liaoning_chaoyang',
                  'zfcg.neimenggu_eerduosi',
                  'zfcg.neimenggu_tongliao',
                  'zfcg.qinghai_shenghui',
                  'zfcg.shandong_rizhao',
                  'zfcg.shanxi_shenghui',
                  'zfcg.shanxi1_changzhi',
                  'zfcg.shanxi1_shenghui',
                  'zfcg.sichuan_shenghui',
                  'zfcg.xinjiang_alashankou',
                  'zfcg.xinjiang_shenghui2',
                  'zfcg.shanxi_hanzhong',
                  'zfcg.xizang_shenghui',
                  'zfcg.zhejiang_hangzhou',
                  'zfcg.zhejiang_quzhou',
                  'zfcg.zhejiang_shenghui',
                  'qycg.b2bcoal_crp_net_cn',
                  'qycg.bid_ansteel_cn',
                  'qycg.bid_powerchina_cn',
                  'qycg.buy_cnooc_com_cn',
                  'qycg.csbidding_csair_com',
                  'qycg.dzzb_ciesco_com_cn',
                  'qycg.www_cdt_eb_com',
                  'qycg.www_mgzbzx_com',
                  'qycg.www_qhbidding_com',
                  'qycg.www_sztc_com',
                  'qycg.www_wiscobidding_com_cn',
                  'qycg.www_ykjtzb_com',
                  'qycg.www_zeec_cn',
                  'qycg.www_zmzb_com',
                  'qycg.wzcgzs_95306_cn',
                  'qycg.zb_crlintex_com'
                  ]

list_page_notime = [
    'gcjs.fujian_sanming',
    'gcjs.jilin_siping',
    'gcjs.shanxi_yulin',
    'zfcg.beijing_beijing',
    'zfcg.guangdong_shantou',
    'zfcg.guangxi_fangchenggang',
    'zfcg.guangxi_wuzhou',
    'zfcg.hunan_changsha2',
    'zfcg.jiangxi_jiangxi',
    'zfcg.neimenggu_bayannaoer',
    'zfcg.shandong_liaocheng',
    'zfcg.shandong_qingdao',
    'zfcg.xinjiang_changji',
    'zfcg.xizang_shannan',
    'zfcg.ningxia_yinchuan',
    'zfcg.xizang_shannan',
    'zfcg.xinjiang_changji2',
    'gcjs.guangdong_zhongshan',
    'gcjs.hebei_langfang',
    'gcjs.hunan_huaihua',
    'gcjs.jilin_jilin',
    'gcjs.jilin_tonghua',
    'gcjs.liaoning_shenyang',
    'gcjs.neimenggu_shenghui',
    'gcjs.shanxi_baoji',
    'gcjs.shanxi1_taiyuan',
    'gcjs.shanxi1_xinzhou2',
    'zfcg.jiangsu_wuxi',
    'zfcg.shanxi1_taiyuan',
    'qycg.www_namkwong_com_mo',
    'qycg.www_sinochemitc_com',
    'gcjs.gansu_shenghui',
    'zfcg.anhui_wuhu',
    'zfcg.guangxi_baise',
    'zfcg.sichuan_mianyang',
    'zfcg.xinjiang_hetian',
    'qycg.www_dlztb_com',
    'gcjs.fujian_zhangzhou',
    'gcjs.henan_kaifeng',
    'gcjs.hunan_changsha1',
    'gcjs.hunan_changsha2',
    'gcjs.hunan_shaoyang',
    'gcjs.hunan_wugang',
    'gcjs.hunan_yueyang',
    'gcjs.jiangxi_jiujiang',
    'gcjs.shandong_jinan',
    'gcjs.shandong_linyi',
    'zfcg.fujian_nanping',
    'zfcg.henan_hebi',
    'zfcg.henan_henan',
    'zfcg.henan_jiaozuo',
    'zfcg.henan_kaifeng',
    'zfcg.henan_luohe',
    'zfcg.henan_luoyang',
    'zfcg.henan_nanyang',
    'zfcg.henan_pingdingshan',
    'zfcg.henan_puyang',
    'zfcg.henan_sanmenxia',
    'zfcg.henan_shangqiu',
    'zfcg.henan_xinxiang',
    'zfcg.henan_xinyang',
    'zfcg.henan_xuchang',
    'zfcg.henan_zhengzhou',
    'zfcg.henan_zhoukou',
    'zfcg.henan_zhumadian',
    'zfcg.hunan_changsha',
    'zfcg.hunan_xiangtan',
    'zfcg.shandong_yantai',
    'qycg.dzzb_ciesco_com_cn',
    'qycg.epp_ctg_com_cn',
    'qycg.jzcg_cfhi_com',
    'qycg.thzb_crsc_cn',
    'qycg.www_bidding_csg_cn',
    'qycg.www_china_tender_com_cn',
    'qycg.www_chinabidding_com',
    'qycg.www_dlzb_com',
    'qycg.www_dlzb_com_c1608',
    'qycg.www_ngecc_com',
    'gcjs.fujian_fuqing',
    'gcjs.fujian_fuzhou',
    'gcjs.fujian_quanzhou',
    'gcjs.guangdong_shantou',
    'gcjs.guangdong_shaoguan',
    'gcjs.guangdong_shenzhen',
    'gcjs.guangxi_shenghui',
    'gcjs.hebei_shenghui',
    'gcjs.heilongjiang_haerbin',
    'gcjs.heilongjiang_qqhaer',
    'gcjs.heilongjiang_shenghui',
    'gcjs.jiangsu_nantong',
    'gcjs.shandong_heze',
    'gcjs.shanxi1_changzhi',
    'gcjs.shanxi1_datong',
    'zfcg.guangdong_guangzhou',
    'zfcg.hainan_sanya',
    'zfcg.hubei_ezhou',
    'zfcg.hubei_wuhan',
    'zfcg.jiangsu_shenghui',
    'zfcg.jiangsu_suqian',
    'zfcg.jiangsu_yangzhou',
    'zfcg.jilin_shenghui',
    'zfcg.liaoning_shenyang',
    'zfcg.shandong_dongying',
    'zfcg.shandong_laiwu',
    'zfcg.shandong_linyi',
    'zfcg.tianjin_tianjin',
    'zfcg.tianjin_tianjin',
    'qycg.ec1_mcc_com_cn',
    'qycg.ec_ceec_net_cn',
    'qycg.ec_chalieco_com',
    'qycg.ecp_sgcc_com_cn',
    'qycg.eps_sdic_com_cn',
    'qycg.fwgs_sinograin_com_cn',
    'qycg.gs_coscoshipping_com',
    'qycg.srm_crland_com_cn',
    'qycg.uat_ec_chng_com_cn',
    'qycg.www_cnpcbidding_com',
    'qycg.www_gmgitc_com',
    'zfcg.hunan_chenzhou',
    'zfcg.hunan_hengyang',
    'zfcg.hunan_loudi',
    'zfcg.hunan_yiyang',
    'zfcg.hunan_yueyang',
    'zfcg.hunan_zhangjiajie']

list_page_nokey = ['gcjs.guangdong_shaoguan', 'gcjs.guangdong_shenghui', 'zfcg.guangdong_shenzhen',
                   'zfcg.guangdong_shenzhen', 'zfcg.liaoning_wafangdian', 'qycg.www_chdtp_com']
list_page_nospace = ['gcjs.guangxi_beihai', 'gcjs.guangxi_fangchenggang', 'zfcg.shanxi1_yuncheng']


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


def extime_all(page, ggstart_time, quyu):
    if quyu in list_page_time:
        if extime(page) is not None:
            return extime(page)
        elif strptime_transfrom_CST(page):
            return strptime_transfrom_CST(page)
        elif ggstart_time is not None:
            return ggstart_time
    elif quyu in list_page_notime:
        if ggstart_time is not None:
            return ggstart_time
        else:
            return None
    elif quyu in list_page_nokey:
        # 没有标准头部时间
        if strptime_transfrom_nokey(page) is not None:
            return strptime_transfrom_nokey(page)
        elif ggstart_time is not None:
            return ggstart_time
        else:
            return None
    elif quyu in list_page_nospace:
        if strptime_transfrom_nospace(page) is not None:
            # print(strptime_transfrom_nospace(page))
            return strptime_transfrom_nospace(page)
        elif ggstart_time is not None:
            return ggstart_time
        else:
            return None


#

# 读入数据
def write_to_table(df, table_name, quyu, if_exists='replace'):
    import io
    import pandas as pd
    from sqlalchemy import create_engine
    arr = quyu.split('.')
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

# print(df[['data','href','ggstart_time']][df['data']!=df['ggstart_time']])
