# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 19:53:02 2019

@author: mayn
"""
import datetime
from zhulong.util.data import zhulong_diqu_dict
import pandas as pd
from bs4 import BeautifulSoup
import re
import time
from lmf.dbv2 import db_query

ggzy_list_all =[]
for key , l in zhulong_diqu_dict.items():
    for l1 in l:
        ggzy_list_all.append(key+'_'+l1)

not_ggzy_list_page_time = ['gcjs_anhui_huainan',
                           'gcjs_anhui_xuancheng',
                           'gcjs_guangxi_beihai',
                           'gcjs_guangxi_qinzhou',
                           'gcjs_guangxi_shenghui',
                           'gcjs_hebei_shijiazhuang',
                           'gcjs_hebei_tangshan',
                           'gcjs_henan_pingdingshan',
                           'gcjs_henan_zhengzhou',
                           'gcjs_hunan_loudi',
                           'gcjs_jiangsu_changzhou',
                           'gcjs_jiangsu_nanjing',
                           'gcjs_shandong_dongying',
                           'gcjs_shandong_rizhao',
                           'gcjs_shandong_zaozhuang',
                           'gcjs_shanxi_ankang',
                           'gcjs_shanxi_xianyang',
                           'gcjs_shanxi_yanan',
                           'gcjs_sichuan_zigong',
                           'gcjs_xinjiang_hami',
                           'gcjs_zhejiang_huzhou',
                           'gcjs_zhejiang_jinhua',
                           'gcjs_zhejiang_zhoushan',
                           'zfcg_anhui_shenghui',
                           'zfcg_fujian_fuzhou',
                           'zfcg_fujian_longyan',
                           'zfcg_fujian_ningde',
                           'zfcg_fujian_putian',
                           'zfcg_fujian_quanzhou',
                           'zfcg_fujian_sanming1',
                           'zfcg_fujian_xiamen',
                           'zfcg_fujian_zhangzhou',
                           'zfcg_gansu_jinchang',
                           'zfcg_gansu_shenghui',
                           'zfcg_guangxi_guilin',
                           'zfcg_guangxi_liuzhou',
                           'zfcg_guangxi_nanning',
                           'zfcg_guangxi_shenghui',
                           'zfcg_guizhou_shenghui',
                           'zfcg_guizhou_tongren',
                           'zfcg_hainan_haikou',
                           'zfcg_hainan_shenghui',
                           'zfcg_hainan_wenchang',
                           'zfcg_heibei_shenghui',
                           'zfcg_heilongjiang_shenghui',
                           'zfcg_heilongjiang_yichun',
                           'zfcg_hubei_huanggang',
                           'zfcg_hubei_hubei',
                           'zfcg_hubei_shiyan',
                           'zfcg_hunan_changde',
                           'zfcg_jiangsu_changzhou',
                           'zfcg_jiangsu_huaian',
                           'zfcg_jiangsu_lianyungang',
                           'zfcg_jiangsu_nanjing',
                           'zfcg_jiangsu_nantong',
                           'zfcg_jiangsu_xuzhou',
                           'zfcg_jiangsu_xuzhou2',
                           'zfcg_jiangsu_zhenjiang',
                           'zfcg_jiangxi_jian',
                           'zfcg_jilin_jilin',
                           'zfcg_jilin_shenghui',
                           'zfcg_liaoning_changchun',
                           'zfcg_liaoning_chaoyang',
                           'zfcg_neimenggu_eerduosi',
                           'zfcg_neimenggu_tongliao',
                           'zfcg_qinghai_shenghui',
                           'zfcg_shandong_rizhao',
                           'zfcg_shanxi_shenghui',
                           'zfcg_shanxi1_changzhi',
                           'zfcg_shanxi1_shenghui',
                           'zfcg_sichuan_shenghui',
                           'zfcg_xinjiang_alashankou',
                           'zfcg_xinjiang_shenghui2',
                           'zfcg_shanxi_hanzhong',
                           'zfcg_xizang_shenghui',
                           'zfcg_zhejiang_hangzhou',
                           'zfcg_zhejiang_quzhou',
                           'zfcg_zhejiang_shenghui',
                           'qycg_b2bcoal_crp_net_cn',
                           'qycg_bid_ansteel_cn',
                           'qycg_bid_powerchina_cn',
                           'qycg_buy_cnooc_com_cn',
                           'qycg_csbidding_csair_com',
                           'qycg_dzzb_ciesco_com_cn',
                           'qycg_www_cdt_eb_com',
                           'qycg_www_mgzbzx_com',
                           'qycg_www_qhbidding_com',
                           'qycg_www_sztc_com',
                           'qycg_www_wiscobidding_com_cn',
                           'qycg_www_ykjtzb_com',
                           'qycg_www_zeec_cn',
                           'qycg_www_zmzb_com',
                           'qycg_wzcgzs_95306_cn',
                           'qycg_zb_crlintex_com'
                           ]

not_ggzy_list_page_notime = [
    'gcjs_fujian_sanming',
    'gcjs_jilin_siping',
    'gcjs_shanxi_yulin',
    'zfcg_beijing_beijing',
    'zfcg_guangdong_shantou',
    'zfcg_guangxi_fangchenggang',
    'zfcg_guangxi_wuzhou',
    'zfcg_hunan_changsha2',
    'zfcg_jiangxi_jiangxi',
    'zfcg_neimenggu_bayannaoer',
    'zfcg_shandong_liaocheng',
    'zfcg_shandong_qingdao',
    'zfcg_xinjiang_changji',
    'zfcg_xizang_shannan',
    'zfcg_ningxia_yinchuan',
    'zfcg_xizang_shannan',
    'zfcg_xinjiang_changji2',
    'gcjs_guangdong_zhongshan',
    'gcjs_hebei_langfang',
    'gcjs_hunan_huaihua',
    'gcjs_jilin_jilin',
    'gcjs_jilin_tonghua',
    'gcjs_liaoning_shenyang',
    'gcjs_neimenggu_shenghui',
    'gcjs_shanxi_baoji',
    'gcjs_shanxi1_taiyuan',
    'gcjs_shanxi1_xinzhou2',
    'zfcg_jiangsu_wuxi',
    'zfcg_shanxi1_taiyuan',
    'qycg_www_namkwong_com_mo',
    'qycg_www_sinochemitc_com',
    'gcjs_gansu_shenghui',
    'zfcg_anhui_wuhu',
    'zfcg_guangxi_baise',
    'zfcg_sichuan_mianyang',
    'zfcg_xinjiang_hetian',
    'qycg_www_dlztb_com',
    'gcjs_fujian_zhangzhou',
    'gcjs_henan_kaifeng',
    'gcjs_hunan_changsha1',
    'gcjs_hunan_changsha2',
    'gcjs_hunan_shaoyang',
    'gcjs_hunan_wugang',
    'gcjs_hunan_yueyang',
    'gcjs_jiangxi_jiujiang',
    'gcjs_shandong_jinan',
    'gcjs_shandong_linyi',
    'zfcg_fujian_nanping',
    'zfcg_henan_hebi',
    'zfcg_henan_henan',
    'zfcg_henan_jiaozuo',
    'zfcg_henan_kaifeng',
    'zfcg_henan_luohe',
    'zfcg_henan_luoyang',
    'zfcg_henan_nanyang',
    'zfcg_henan_pingdingshan',
    'zfcg_henan_puyang',
    'zfcg_henan_sanmenxia',
    'zfcg_henan_shangqiu',
    'zfcg_henan_xinxiang',
    'zfcg_henan_xinyang',
    'zfcg_henan_xuchang',
    'zfcg_henan_zhengzhou',
    'zfcg_henan_zhoukou',
    'zfcg_henan_zhumadian',
    'zfcg_hunan_changsha',
    'zfcg_hunan_xiangtan',
    'zfcg_shandong_yantai',
    'qycg_dzzb_ciesco_com_cn',
    'qycg_epp_ctg_com_cn',
    'qycg_jzcg_cfhi_com',
    'qycg_thzb_crsc_cn',
    'qycg_www_bidding_csg_cn',
    'qycg_www_china_tender_com_cn',
    'qycg_www_chinabidding_com',
    'qycg_www_dlzb_com',
    'qycg_www_dlzb_com_c1608',
    'qycg_www_ngecc_com',
    'gcjs_fujian_fuqing',
    'gcjs_fujian_fuzhou',
    'gcjs_fujian_quanzhou',
    'gcjs_guangdong_shantou',
    'gcjs_guangdong_shaoguan',
    'gcjs_guangdong_shenzhen',
    'gcjs_guangxi_shenghui',
    'gcjs_hebei_shenghui',
    'gcjs_heilongjiang_haerbin',
    'gcjs_heilongjiang_qqhaer',
    'gcjs_heilongjiang_shenghui',
    'gcjs_jiangsu_nantong',
    'gcjs_shandong_heze',
    'gcjs_shanxi1_changzhi',
    'gcjs_shanxi1_datong',
    'zfcg_guangdong_guangzhou',
    'zfcg_hainan_sanya',
    'zfcg_hubei_ezhou',
    'zfcg_hubei_wuhan',
    'zfcg_jiangsu_shenghui',
    'zfcg_jiangsu_suqian',
    'zfcg_jiangsu_yangzhou',
    'zfcg_jilin_shenghui',
    'zfcg_liaoning_shenyang',
    'zfcg_shandong_dongying',
    'zfcg_shandong_laiwu',
    'zfcg_shandong_linyi',
    'zfcg_tianjin_tianjin',
    'zfcg_tianjin_tianjin',
    'qycg_ec1_mcc_com_cn',
    'qycg_ec_ceec_net_cn',
    'qycg_ec_chalieco_com',
    'qycg_ecp_sgcc_com_cn',
    'qycg_eps_sdic_com_cn',
    'qycg_fwgs_sinograin_com_cn',
    'qycg_gs_coscoshipping_com',
    'qycg_srm_crland_com_cn',
    'qycg_uat_ec_chng_com_cn',
    'qycg_www_cnpcbidding_com',
    'qycg_www_gmgitc_com',
    'zfcg_hunan_chenzhou',
    'zfcg_hunan_hengyang',
    'zfcg_hunan_loudi',
    'zfcg_hunan_yiyang',
    'zfcg_hunan_yueyang',
    'zfcg_hunan_zhangjiajie']

not_ggzy_list_page_nokey = ['gcjs_guangdong_shaoguan', 'gcjs_guangdong_shenghui', 'zfcg_guangdong_shenzhen',
                            'zfcg_guangdong_shenzhen', 'zfcg_liaoning_wafangdian', 'qycg_www_chdtp_com']

not_ggzy_list_page_nospace = ['gcjs_guangxi_beihai', 'gcjs_guangxi_fangchenggang', 'zfcg_shanxi1_yuncheng']

ggzy_list_page_time = [
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

ggzy_list_page_notime = [
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

ggzy_list_page_yunan = ['yunnan_baoshan',
                        'yunnan_chuxiong',
                        'yunnan_wenshan',
                        'yunnan_xishuangbanna',
                        'yunnan_yunnan2',
                        'yunnan_yuxi',
                        'yunnan_zhaotong'
                        ]

ggzy_not_exists_list = [
    # 不存在数据的quyu
    'jiangsu_yancheng',# 网站挂了
    'liaoning_beizhen',# 网站挂了
    'liaoning_fushun',# 网站挂了
    'shandong_dongying',
    'tianjin_tianjin',
    'shanghai_shanghai'

    # # 有问题的quyu
    # 'fujian_fujian',
    # 'guizhou_shenghui',
    # 'hubei_huanggang',
    # 'hubei_wuhan',
    # 'liaoning_shenyang',
    # 'liaoning_tieling',
    # 'neimenggu_xilinguolemeng',
    # 'shanxi_xian',
    # 'sichuan_neijiang',
    # 'sichuan_panzhihua',
    # 'zhejiang_taizhou',
    # 'zhejiang_tongxian'
    # 'jiangsu_wuxi',
    # 'yunnan_lijiang',
    # 'yunnan_puer',
    # 'yunnan_dali',
    # 'yunnan_honghe',
    # 'yunnan_lincang',

]

not_ggzy_not_exists_list = [
    # 不存在数据表的非ggzy的quyu
    'gcjs_hebei_xingtai',
    'gcjs_henan_puyang',
    'gcjs_shanxi1_linfen',
    'gcjs_sichuan_mianyang',
    'zfcg_shandong_weihai',
    'zfcg_xinjiang_akesu',
    'zfcg_xinjiang_kashi',
    'zfcg_xinjiang_kelamayi',
    'zfcg_xinjiang_shenghui',
    'zfcg_xinjiang_tacheng',
    'zfcg_xinjiang_tulufan',
    'zfcg_xinjiang_yining',
    'qycg_www_chinabidding_com_total'

#    # 有问题的非ggzy的quyu
#    'qycg_etp_fawiec_com',
#    'qycg_syhggs_dlzb_com',
#    'qycg_sytrq_dlzb_com',
#    'qycg_zgdxjt_dlzb_com',
#    'qycg_ysky_dlzb_com',
#    'qycg_zgdzxx_dlzb_com',
#    'qycg_zghkgy_dlzb_com',
#    'qycg_zghkyl_dlzb_com',
#    'qycg_zgyy_dlzb_com',

    # 'gcjs_guangdong_yangjiang',
    # 'gcjs_guangxi_baise',
    # 'gcjs_heilongjiang_qqhaer',
    # 'gcjs_hunan_shenghui',
    # 'gcjs_jiangsu_yangzhou',
    # 'gcjs_jiangsu_yangzhou',
    # 'gcjs_jiangxi_pingxiang',
    # 'gcjs_jiangxi_nanchang',
    # 'gcjs_jiangxi_shangrao',
    # 'gcjs_jilin_changchun',
    # 'gcjs_liaoning_dalian',
    # 'gcjs_ningxia_shenghui',
    # 'gcjs_shandong_shenghui',
    # 'gcjs_shanxi_hanzhong',
    # 'gcjs_shanxi_xian',
    # 'gcjs_shanxi1_xinzhou',
    # 'gcjs_sichuan_chengdu',
    # 'gcjs_xinjiang_atushi',
    # 'gcjs_xinjiang_bole',
    # 'gcjs_xinjiang_changji',
    # 'gcjs_xinjiang_shenghui',
    # 'gcjs_xinjiang_kashi',
    # 'gcjs_xinjiang_tacheng',
    # 'gcjs_xinjiang_wulumuqi',
    # 'gcjs_xinjiang_yining',
    # 'gcjs_zhejiang_shenghui',
    # 'zfcg_anhui_anqing',
    # 'zfcg_chongqing_chongqing',
    # 'zfcg_fujian_sanming',
    # 'zfcg_guangdong_zhongshan',
    # 'zfcg_guangxi_guigang',
    # 'zfcg_jiangsu_suzhou',
    # 'zfcg_jiangsu_taizhou',
    # 'zfcg_jiangxi_pingxiang',
    # 'zfcg_neimenggu_shenghui',
    # 'zfcg_ningxia_shenghui',
    # 'zfcg_shandong_dezhou',
    # 'zfcg_shandong_shandong',
    # 'zfcg_xinjiang_wulumuqi',
    # 'zfcg_zhejiang_ningbo',
    # 'zfcg_zhejiang_wenzhou',
    # 'qycg_baowu_ouyeelbuy_com',
    # 'qycg_bidding_ceiec_com_cn',
    # 'qycg_dfqcgs_dlzb_com',
    # 'qycg_ec_ccccltd_cn',
    # 'qycg_ec_ceec_net_cn',
    # 'qycg_ecp_cgnpc_com_cn',
    # 'qycg_etp_fawiec_com',
    # 'qycg_syhggs_dlzb_com',
    # 'qycg_sytrq_dlzb_com',
    # 'qycg_www_cgdcbidding_com',
    # 'qycg_www_dlswzb_com',
    # 'qycg_zgdxjt_dlzb_com',
    # 'qycg_ysky_dlzb_com',
    # 'qycg_zgdzxx_dlzb_com',
    # 'qycg_zghkgy_dlzb_com',
    # 'qycg_zghkyl_dlzb_com',
    # 'qycg_zgyy_dlzb_com',

]


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


def strptime_transfrom_nofg(page):
    # 时间没有分隔。
    soup = BeautifulSoup(page, 'lxml')
    txt = re.sub('[^\u4E00-\u9Fa5a-zA-Z0-9:：\-\\/]', '', soup.text.strip())
    patterns = ["(?:变更日期时间|更新时间|发布时间|发布日期)[：:]([0-9]{8})", "(20[0-2][0-9])[\-\.年\\/]([1-9]|[0][1-9]|[1][0-2])[\-\.\\月/]([0-9]{,2}).{1}公布"]
    for p in patterns:
        a = re.findall(p, txt)
        if a != []:
            return '-'.join([a[0][:4], a[0][4:6], a[0][6:]])
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


def strptime_transfromgg_guangdong_shenghui(page):
    list1 = []
    soup = BeautifulSoup(page, 'lxml')
    soup_input = soup.find_all('input')[-3:]
    for i in soup_input:
        value = i['value']
        list1.append(value)
    #    print('----',txt)
    if list1 != []:
        return ('-'.join([list1[0], list1[1], list1[2]]))
    return None


def strptime_transfromgs(page):
    soup = BeautifulSoup(page, 'lxml')
    txt = re.sub('[^\u4E00-\u9Fa5a-zA-Z0-9:：\-\\/]', '', soup.text.strip())
    p = "(?:信息时间|信息日期|信息发布日期|发稿时间|发布时间|发布日期|发文日期|更新日期|生成日期|公示日期|公示时间|公告时间)[:：]{0,1}(20[0-2][0-9])[\-\.年\\/]([1-9]|[0][1-9]|[1][0-2])[\-\.月\\/]([0-9]{,2})"
    # print(txt)
    a = re.findall(p, txt)
    #    print('----',txt)
    if a != []:
        return ('-'.join(a[0]))
    return None


def strptime_transfromrq(page):
    soup = BeautifulSoup(page, 'lxml')
    txt = re.sub('[^\u4E00-\u9Fa5a-zA-Z0-9:：\-\\/]', '', soup.text.strip())
    p = "(?:日期|信息时间|信息日期|信息发布日期|发稿时间|发布时间|发布日期|发文日期|更新日期|生成日期)[:：]{0,1}(20[0-2][0-9])[\-\.年\\/]([1-9]|[0][1-9]|[1][0-2])[\-\.月\\/]([0-9]{,2})"
    # print(txt)
    a = re.findall(p, txt)
    #    print('----',txt)
    if a != []:
        return ('-'.join(a[0]))
    return None


def not_ggzy_extime_all(page, ggstart_time, quyu):
    if quyu in not_ggzy_list_page_time:
        if extime(page) is not None:
            return extime(page)
        elif strptime_transfrom_CST(page):
            return strptime_transfrom_CST(page)
        elif ggstart_time is not None:
            return ggstart_time
    elif quyu in not_ggzy_list_page_notime:
        if ggstart_time is not None:
            return ggstart_time
        else:
            return None
    elif quyu in not_ggzy_list_page_nokey:
        # 没有标准头部时间
        if strptime_transfrom_nokey(page) is not None:
            return strptime_transfrom_nokey(page)
        elif ggstart_time is not None:
            return ggstart_time
        else:
            return None
    elif quyu in not_ggzy_list_page_nospace:
        if strptime_transfrom_nospace(page) is not None:
            # print(strptime_transfrom_nospace(page))
            return strptime_transfrom_nospace(page)
        elif ggstart_time is not None:
            return ggstart_time
        else:
            return None
    elif quyu in ['gcjs_guangdong_yangjiang',
                  'gcjs_heilongjiang_qqhaer', 'gcjs_hunan_shenghui',
                  'gcjs_jiangxi_pingxiang', 'gcjs_jiangxi_nanchang',
                  'gcjs_jiangxi_shangrao', 'gcjs_liaoning_dalian', 'gcjs_ningxia_shenghui',
                  'gcjs_shandong_shenghui', 'gcjs_shanxi_hanzhong',
                  'gcjs_shanxi_xian', 'gcjs_sichuan_chengdu', 'gcjs_xinjiang_atushi',
                  'gcjs_xinjiang_bole', 'gcjs_xinjiang_changji',
                  'gcjs_xinjiang_yining', 'gcjs_xinjiang_shenghui', 'gcjs_xinjiang_wulumuqi',
                  'gcjs_zhejiang_shenghui', 'zfcg_anhui_anqing', 'zfcg_chongqing_chongqing', 'zfcg_guangxi_guigang',
                  'zfcg_jiangsu_suzhou', 'zfcg_jiangsu_taizhou', 'zfcg_jiangxi_pingxiang',
                  'zfcg_neimenggu_shenghui', 'zfcg_ningxia_shenghui', 'zfcg_shandong_dezhou',
                  'zfcg_xinjiang_wulumuqi', 'zfcg_zhejiang_ningbo', 'zfcg_zhejiang_wenzhou',
                  'qycg_baowu_ouyeelbuy_com', 'qycg_bidding_ceiec_com_cn', 'qycg_dfqcgs_dlzb_com', 'qycg_ec_ccccltd_cn',
                  'qycg_ec_ceec_net_cn', 'qycg_ecp_cgnpc_com_cn', 'qycg_etp_fawiec_com', 'qycg_www_dlswzb_com', 'gcjs_jiangsu_yangzhou',
                  'gcjs_guangdong_dongguan']:
        print('*******')
        if quyu in ['gcjs_jiangsu_yangzhou', 'qycg_ec_ceec_net_cn']:
            if strptime_transfrom_nospace(page):
                return (strptime_transfrom_nospace(page))
            return (ggstart_time)
        if quyu in ['gcjs_guangdong_yangjiang', 'gcjs_shandong_shenghui', 'gcjs_shanxi_hanzhong']:
            print('ok')
            if strptime_transfromgs(page):
                return (strptime_transfromgs(page))
            return ggstart_time
        if quyu in ['gcjs_zhejiang_shenghui', 'qycg_www_dlswzb_com']:
            if extime(page):
                return (extime(page))
            return None
        if quyu in ['gcjs_hunan_shenghui']:
            if strptime_transfromrq(page):
                return strptime_transfromrq(page)
            return ggstart_time
        elif extime(page):
            if extime(page) is not None:
                return extime(page)
            
        elif strptime_transfrom_nofg(page) is not None:
            return strptime_transfrom_nofg(page)
        else:
            return ggstart_time

    elif quyu in ['gcjs_henan_sanmenxia', 'gcjs_sichuan_bazhong', 'gcjs_sichuan_shenghui', 'zfcg_anhui_huainan', 'zfcg_fujian_nanping1',
                  'zfcg_guangdong_shenghui', 'zfcg_hubei_jingmen', 'zfcg_hubei_wuhan2', 'zfcg_jiangsu_yancheng',
                  'zfcg_neimenggu_baotou', 'zfcg_neimenggu_huhehaote', 'qycg_www_crpsz_com', 'qycg_zgyy_dlzb_com', 'qycg_zghkyl_dlzb_com',
                  'qycg_zghkgy_dlzb_com', 'qycg_zgdzxx_dlzb_com', 'qycg_ysky_dlzb_com', 'qycg_zgdxjt_dlzb_com', 'qycg_www_dlswzb_com',
                  'qycg_sytrq_dlzb_com',
                  'qycg_syhggs_dlzb_com', 'qycg_etp_fawiec_com','gcjs_guangdong_dongguan','gcjs_jinlin_shenghui','qycg_b2b_10086_cn']:
        if quyu in ['zfcg_guangdong_shenghui']:
            if strptime_transfromgg_guangdong_shenghui(page):
                return (strptime_transfromgg_guangdong_shenghui(page))
            return None
        if quyu in ['zfcg_hubei_wuhan2']:
            if extime(page):
                return (extime(page))
            return None
        if quyu in ['gcjs_henan_sanmenxia','gcjs_sichuan_bazhong']:
            if strptime_transfromsj(page):
                return (strptime_transfromsj(page))
            return ggstart_time
        elif extime(page):
            return extime(page)
        else:
            return ggstart_time


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
    p = "(?:信息时间|信息日期|更新时间|发稿时间|发文时间|发文日期|发布时间|发布日期|录入时间|生成时间|生成日期|公示期为)[：:](20[0-2][0-9])[\-\.年\\/]([1-9]|[0][1-9]|[1][0-2])[\-\.\\月/]([0-9]{,2})"
    a = re.findall(p, txt.replace('documentwrite', ''))
    # print(a)
    if a != []:
        return '-'.join(a[0])
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


#def strptime_transfromgg_question1(page):
#    soup = BeautifulSoup(page, 'lxml')
#    txt = re.sub('[^\u4E00-\u9Fa5a-zA-Z0-9:：\-\\/]', '', soup.text.strip())
#    p = "(?:信息时间|信息日期|发布日期|发稿时间|发布时间|发布日期|发文日期|更新日期|生成日期|公示期为)(20[0-2][0-9])[\-\.年\\/]([1-9]|[0][1-9]|[1][0-2])[\-\.月\\/]([0-9]{,2})"
#    # print(txt)
#    a = re.findall(p, txt)
#    #    print('----',txt)
#    if a != []:
#        return ('-'.join(a[0]))
#    return None






def strptime_transfromsj(page):
    soup = BeautifulSoup(page, 'lxml')
    txt = re.sub('[^\u4E00-\u9Fa5a-zA-Z0-9:：\-\\/]', '', soup.text.strip())
    p = "(?:时间|信息日期|信息发布日期|发稿时间|发布时间|发布日期|发文日期|更新日期|生成日期)[:：]{0,1}(20[0-2][0-9])[\-\.年\\/]([1-9]|[0][1-9]|[1][0-2])[\-\.月\\/]([0-9]{,2})"
    # print(txt)
    a = re.findall(p, txt)
    #    print('----',txt)
    if a != []:
        return ('-'.join(a[0]))
    return None


def ggzy_extime_all(page, ggstart_time, quyu):
    if quyu in ggzy_list_page_time:
        if extime(page) is not None:
            return extime(page)
        elif strptime_transfrom_CST(page):
            return strptime_transfrom_CST(page)
        elif ggstart_time is not None:
            return ggstart_time
        else:
            return None
    elif quyu in ggzy_list_page_notime:
        if ggstart_time is not None:
            return ggstart_time
        else:
            return None
    elif quyu in ggzy_list_page_yunan:
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

    # ggstart_time时间有问题
    elif quyu in ['fujian_fujian', 'guizhou_shenghui', 'hubei_huanggang', 'hubei_wuhan',
                  'liaoning_shenyang', 'liaoning_tieling', 'neimenggu_xilinguolemeng', 'shanxi_xian',
                  'sichuan_panzhihua', 'zhejiang_tongxiang', 'jiangsu_wuxi', 'yunnan_lijiang',
                  'yunnan_puer', 'yunnan_dali', 'yunnan_honghe', 'yunnan_lincang']:
        if quyu in ['yunnan_lijiang', 'yunnan_puer', 'yunnan_dali', 'yunnan_honghe', 'yunnan_lincang']:
            if strptime_transfrom_yunan(page):
                return (strptime_transfrom_yunan(page))
            return (ggstart_time)
        elif quyu in ['liaoning_shenyang']:
            if strptime_transfrom_yue_r_n(page) is not None:
                return strptime_transfrom_yue_r_n(page)
            else:
                return (ggstart_time)
        elif extime(page) is not None:
            return extime(page)
        else:
            return ggstart_time
    elif quyu in ['gansu_gansu', 'gansu_jiayuguan',
                  'gansu_tianshui', 'guangdong_foshan', 'guizhou_zunyi', 'hunan_hunan', 'jilin_liaoyuan',
                  'liaoning_benxi', 'shanxi_shanxi', 'xinjiang_kezhou', 'yunnan_dehong','gcjs_guangdong_dongguan',
              'jiangsu.yizheng']:
        if quyu in ['guangdong_foshan']:
            if strptime_transfromsj(page):
                return (strptime_transfromsj(page))
            return ggstart_time
        if quyu in ['hunan_hunan']:
            if strptime_transfromsj(page):
                return (strptime_transfromsj(page))
            return ggstart_time
        elif extime(page) is not None:
            return extime(page)
        else:
            return ggstart_time





def extime_all(page, ggstart_time, quyu):
    '''
    df['data']=df['data'].map(lambda x:x if x is not None  else '')
    df['ggstart_time']=df['ggstart_time'].map(lambda x:x if x is not None  else '')

    '''
    ggstart_time = ext_from_ggtime(ggstart_time if ggstart_time is not None else '')

    if quyu in ggzy_list_all:
        if quyu not in ggzy_not_exists_list:
            res = ggzy_extime_all(page, ggstart_time, quyu)
        else:
            res = ggstart_time
    else:
        if quyu not in not_ggzy_not_exists_list:
            res = not_ggzy_extime_all(page, ggstart_time, quyu)
        else:
            res = ggstart_time
    res = ext_from_ggtime(res if res is not None else '')
    if not res: return None
    if pd.to_datetime(res, format='%Y-%m-%d', errors='ignore') <= pd.to_datetime(datetime.datetime.now().strftime('%Y-%m-%d'), format='%Y-%m-%d',
                                                                                 errors='ignore'):
        return res
    else:
        return None









if __name__ == '__main__':
    # print(zhulong_diqu_dict)
    # ggzy_list_all = []
    # for key in zhulong_diqu_dict.keys():
    #
    #     for value in zhulong_diqu_dict[key]:
    #         if value not in ['public']:
    #             quyu = key + '_' + value
    #             if quyu not in ggzy_not_exists_list:
    #                 ggzy_list_all.append(quyu)
    #
    # print(ggzy_list_all)
    # print(os.path.dirname(os.path.abspath(__file__)))

    pass
    # df = getpage_herf_ggstart_time('gcjs.guangxi_beihai')
    # df['ggstart_time'] = df['ggstart_time'].map(lambda x: ext_from_ggtime(x))
    # df['data'] = None
    # df['ggstart_time'] = df['ggstart_time'].map(lambda x: x if x is not None else '')
    # for i in df.index:
    #     page, ggstart_time, quyu = df.at[i, 'page'], df.at[i, 'ggstart_time'], 'gcjs.guangxi_beihai'
    #
    #     df.at[i, 'data'] = extime_all(page, ggstart_time, quyu)
    #     soup = BeautifulSoup(df.at[i, 'page'], 'lxml')
    #     #    print(soup)
    #     txt = re.sub('[^\u4E00-\u9Fa5a-zA-Z0-9:：\-\\/]', '', soup.text.strip())
    #     print(i, txt, df.at[i, 'href'])
    #     #    print(df.at[i,'href'])
    #     print(df.at[i, 'ggstart_time'])
    #
    # df['data'] = df['data'].map(lambda x: x if x is not None else '')
    # df['data'] = df['data'].map(lambda x: ext_from_ggtime(x))
    # # print(df['href'])
    # # print(df['data'])
    # df['ggstart_time'] = df['ggstart_time'].map(lambda x: ext_from_ggtime(x))
    # # print(df['ggstart_time'])
    #
    # df.drop_duplicates(['href', 'ggstart_time'], inplace=True)
    # df_count = pd.pivot_table(df, index=["href"], values=["ggstart_time"], aggfunc=[len])
    # df_count.reset_index(inplace=True)
    # df_count.columns = ['href', 'ggstart_time_cnt']
    # df = df.merge(df_count, left_on='href', right_on='href')
    # df['data'][df['ggstart_time_cnt'] > 1] = df['ggstart_time'][df['ggstart_time_cnt'] > 1]
    # t = df['data'] == df['ggstart_time']
    # print(t.sum())











































