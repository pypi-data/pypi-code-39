# encoding=utf-8
import json
import os
import re
# from lmf.dbv2 import db_query
from bs4 import BeautifulSoup
import jieba
import collections
import time
import pandas as  pd
from sqlalchemy import create_engine
from functools import reduce

# 连接数据库
def getpage_herf_ggstart_time(quyu):
    arr = quyu.split('*')
    db, schema = arr[0], arr[1]
    engine = create_engine('postgresql+psycopg2://postgres:since2015@192.168.3.171/%s' % (db))
    data_gg_html = pd.read_sql_table(table_name='gg_html', con=engine, schema=schema, index_col=None, coerce_float=True,
                                     parse_dates=None, columns=None, chunksize=None)
    df = data_gg_html[['href', 'page']]
    return df


# 读入数据库
def write_to_table(df, table_name, quyu, if_exists='replace'):
    import io
    import pandas as pd
    from sqlalchemy import create_engine
    arr = quyu.split('*')
    db, schema = arr[0], arr[1]
    db_engine = create_engine('postgresql+psycopg2://postgres:since2015@192.168.3.171/%s' % db)
    string_data_io = io.StringIO()
    df.to_csv(string_data_io, sep='|', index=False)
    pd_sql_engine = pd.io.sql.pandasSQL_builder(db_engine)
    table = pd.io.sql.SQLTable(table_name, pd_sql_engine, frame=df, index=False, if_exists=if_exists, schema=schema)
    table.create()
    string_data_io.seek(0)
    string_data_io.readline()  # remove header
    with db_engine.connect() as connection:
        with connection.connection.cursor() as cursor:
            copy_cmd = "COPY %s.%s FROM STDIN HEADER DELIMITER '|' CSV" % (schema, table_name)
            cursor.copy_expert(copy_cmd, string_data_io)
        connection.connection.commit()



class parseDiqu(object):
    def __init__(self):
        self.__jieba_init__()

    def __jieba_init__(self):
        json_path = os.path.join(os.path.dirname(__file__), 'xzqh_key_word.json')
        print(json_path)
        with open(json_path, 'r', encoding='utf-8') as f:
            self.xzqh_key_word = f.read()
        self.xzqh_key_word_dict_list = json.loads(self.xzqh_key_word)
        self.data = pd.DataFrame(self.xzqh_key_word_dict_list)
        self.new_diqu_list = []
        diqu = self.data['word'].tolist()
        self.new_diqu_list = []
        for d in diqu:
            self.new_diqu_list.extend(d.split(','))
        jieba.load_userdict(self.new_diqu_list)
        for word in self.new_diqu_list:
            word = word.strip()
            jieba.suggest_freq(word, tune=True)
    def t_page(self, page):
        if page is None:
            return []
        soup = BeautifulSoup(page, 'lxml')
        tmp = soup.find('style')
        if tmp is not None:
            tmp.clear()
        tmp = soup.find('script')
        if tmp is not None:
            tmp.clear()
        txt = re.sub('[^\u4E00-\u9Fa5a-zA-Z0-9:：\-\\/]', '', soup.text.strip())
        return txt

    def count_diqu(self, txt_list):
        object_list = []
        for word in jieba.cut(txt_list, cut_all=False):
            if word in self.new_diqu_list:
                object_list.append(self.data['code'][self.data['word'].str.contains(word)].tolist()[0])
        if object_list != []:
            count = {}
            dit = {}
            for value, key in enumerate(object_list):
                if dit.get(key, 0):
                    count[key] = count[key] + 1
                else:
                    count[key] = 1
                    dit[key] = value + 1
            cnt_data = pd.DataFrame([count])
            cnt_data = pd.melt(cnt_data)
            cnt_data.columns = ['code', 'cnt']
            rank_data = pd.DataFrame([dit])
            rank_data = pd.melt(rank_data)
            rank_data.columns = ['code', 'rank']
            df_final = cnt_data.merge(rank_data, left_on='code', right_on='code')
            df_final['length'] = df_final['code'].map(lambda x: len(x))
            df_final.sort_values(by=['rank'], ascending=True, inplace=True)
            df_final.sort_values(by=['cnt'], ascending=False, inplace=True)
            df_final.reset_index(drop=True, inplace=True)
            if df_final.shape[0] > 1:
                if re.findall('[0-9]{2}', str([df_final['code'][0]]))[0] == re.findall('[0-9]{2}', str([df_final['code'][1]]))[0]:
                    df_final.sort_values(by=['length'], ascending=False, inplace=True)
                    df_final.reset_index(drop=True, inplace=True)
            # print(df_final)
            return df_final['code'][0]
        else:
            return None

    def parse_diqu(self, page):
        """

        :param page: html 文本
        :return: diqu_code
        """
        txt_list = self.t_page(page)
        # print(txt_list)
        diqu_code = self.count_diqu(txt_list)
        return diqu_code

# txtx = """<div class="xl-content">
# <div class="xlnk">
# <h2>     靖州县城区P8户外全彩显示屏工程    </h2>
# <h6>
# <span>发布时间： 2017-07-31 00:00</span>
# <span>信息来源：市公共资源交易中心</span>
# <span>责任编辑：系统发布管理员</span>
# <span>点击量：<font id="webshow">19</font></span>
# </h6>
# <div class="xl-xqnr">
# <wbr/>
# <title>公告预览</title>
# <meta content="no-cache" http-equiv="pragma"/>
# <meta content="no-cache" http-equiv="cache-control"/>
# <meta content="0" http-equiv="expires"/>
# <meta content="keyword1,keyword2,keyword3" http-equiv="keywords"/>
# <meta content="This is my page" http-equiv="description"/>
# <link href="/css/BudgetMgr.css" rel="stylesheet" type="text/css"/>
# <style type="text/css">h3,h2 { font-size: 20px;}body,div,table,table tr td,h3,h2,span { font-size: 16px; margin-left: 5px; margin-top: 5px; text-indent: 20px;}div,h3,table,table tr td,span { line-height: 28px;}.table { border: 1px solid #d5d5d5;}.table tr td { border: 1px solid #d5d5d5;}</style>
# <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
# <div style="width:100%;height:100%;border: 0;">
# <p align="center" style="font-weight: bold;">靖州县城区P8户外全彩显示屏工程公开招标中标公告</p>
# <p align="center">公告日期:2017年07月17日</p>
# <div>
# <p align="justify" class="p" style="TEXT-JUSTIFY: inter-ideograph; TEXT-ALIGN: justify; LINE-HEIGHT: 20pt; TEXT-INDENT: 28pt; MARGIN: 3.8pt 0pt 0pt 3.8pt; mso-pagination: widow-orphan"><span style="TEXT-TRANSFORM: none; FONT-STYLE: normal; FONT-FAMILY: 新宋体; LETTER-SPACING: 0pt; COLOR: rgb(0,0,0); FONT-SIZE: 12pt; FONT-WEIGHT: normal; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"> </span><span style="TEXT-TRANSFORM: none; FONT-STYLE: normal; FONT-FAMILY: 新宋体; LETTER-SPACING: 0pt; COLOR: rgb(0,0,0); FONT-SIZE: 10.5pt; FONT-WEIGHT: normal; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"><font face="新宋体">受靖州苗族侗族自治县城市管理行政执法大队的委托，本代理机构对靖州县城区</font>P8户外全彩显示屏工程采购项目进行公开招标采购，现将采购结果公告如下：</span><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">
# <!--?xml:namespace prefix = o /-->
# <o:p></o:p></span></p>
# <p align="justify" class="p" style="TEXT-JUSTIFY: inter-ideograph; TEXT-ALIGN: justify; LINE-HEIGHT: 20pt; MARGIN-TOP: 3.8pt; MARGIN-BOTTOM: 0pt; MARGIN-RIGHT: 0pt; mso-pagination: widow-orphan"><b><span style="TEXT-TRANSFORM: none; FONT-STYLE: normal; FONT-FAMILY: 新宋体; LETTER-SPACING: 0pt; COLOR: rgb(0,0,0); FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"><font face="新宋体">一、采购项目情况</font></span></b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">
# <o:p></o:p></span></p>
# <p align="justify" class="p" style="TEXT-JUSTIFY: inter-ideograph; TEXT-ALIGN: justify; LINE-HEIGHT: 20pt; TEXT-INDENT: 23.5pt; MARGIN: 3.8pt 0pt 0pt 3.8pt; mso-pagination: widow-orphan"><span style="TEXT-TRANSFORM: none; FONT-STYLE: normal; FONT-FAMILY: 新宋体; LETTER-SPACING: 0pt; COLOR: rgb(0,0,0); FONT-SIZE: 10.5pt; FONT-WEIGHT: normal; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"><font face="新宋体">采购项目名称：靖州县城区</font>P8户外全彩显示屏工程</span><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">
# <o:p></o:p></span></p>
# <p align="justify" class="p" style="TEXT-JUSTIFY: inter-ideograph; TEXT-ALIGN: justify; LINE-HEIGHT: 20pt; TEXT-INDENT: 23.5pt; MARGIN: 3.8pt 0pt 0pt 3.8pt; mso-pagination: widow-orphan"><span style="TEXT-TRANSFORM: none; FONT-STYLE: normal; FONT-FAMILY: 新宋体; LETTER-SPACING: 0pt; COLOR: rgb(0,0,0); FONT-SIZE: 10.5pt; FONT-WEIGHT: normal; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"><font face="新宋体">政府采购编号：靖财采计</font>[2017]01059号</span><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">
# <o:p></o:p></span></p>
# <p align="justify" class="p" style="TEXT-JUSTIFY: inter-ideograph; TEXT-ALIGN: justify; LINE-HEIGHT: 20pt; TEXT-INDENT: 23.5pt; MARGIN: 3.8pt 0pt 0pt 3.8pt; mso-pagination: widow-orphan"><span style="TEXT-TRANSFORM: none; FONT-STYLE: normal; FONT-FAMILY: 新宋体; LETTER-SPACING: 0pt; COLOR: rgb(0,0,0); FONT-SIZE: 10.5pt; FONT-WEIGHT: normal; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"><font face="新宋体">委托代理编号：</font>HNSXJZ2017-1004</span><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">
# <o:p></o:p></span></p>
# <p align="justify" class="p" style="TEXT-JUSTIFY: inter-ideograph; TEXT-ALIGN: justify; LINE-HEIGHT: 20pt; TEXT-INDENT: 23.5pt; MARGIN: 3.8pt 0pt 0pt 3.8pt; mso-pagination: widow-orphan"><span style="TEXT-TRANSFORM: none; FONT-STYLE: normal; FONT-FAMILY: 新宋体; LETTER-SPACING: 0pt; COLOR: rgb(0,0,0); FONT-SIZE: 10.5pt; FONT-WEIGHT: normal; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"><font face="新宋体">招标信息发布日期：</font>2017年</span><span style="TEXT-TRANSFORM: none; FONT-STYLE: normal; FONT-FAMILY: 新宋体; LETTER-SPACING: 0pt; COLOR: rgb(0,0,0); FONT-SIZE: 10.5pt; FONT-WEIGHT: normal; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">6</span><span style="TEXT-TRANSFORM: none; FONT-STYLE: normal; FONT-FAMILY: 新宋体; LETTER-SPACING: 0pt; COLOR: rgb(0,0,0); FONT-SIZE: 10.5pt; FONT-WEIGHT: normal; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"><font face="新宋体">月</font></span><span style="TEXT-TRANSFORM: none; FONT-STYLE: normal; FONT-FAMILY: 新宋体; LETTER-SPACING: 0pt; COLOR: rgb(0,0,0); FONT-SIZE: 10.5pt; FONT-WEIGHT: normal; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">23</span><span style="TEXT-TRANSFORM: none; FONT-STYLE: normal; FONT-FAMILY: 新宋体; LETTER-SPACING: 0pt; COLOR: rgb(0,0,0); FONT-SIZE: 10.5pt; FONT-WEIGHT: normal; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"><font face="新宋体">日</font></span><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">
# <o:p></o:p></span></p>
# <p align="justify" class="p" style="TEXT-JUSTIFY: inter-ideograph; TEXT-ALIGN: justify; LINE-HEIGHT: 20pt; TEXT-INDENT: 23.5pt; MARGIN: 3.8pt 0pt 0pt 3.8pt; mso-pagination: widow-orphan"><span style="TEXT-TRANSFORM: none; FONT-STYLE: normal; FONT-FAMILY: 新宋体; LETTER-SPACING: 0pt; COLOR: rgb(0,0,0); FONT-SIZE: 10.5pt; FONT-WEIGHT: normal; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"><font face="新宋体">开标日期：</font>2017年</span><span style="TEXT-TRANSFORM: none; FONT-STYLE: normal; FONT-FAMILY: 新宋体; LETTER-SPACING: 0pt; COLOR: rgb(0,0,0); FONT-SIZE: 10.5pt; FONT-WEIGHT: normal; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">7</span><span style="TEXT-TRANSFORM: none; FONT-STYLE: normal; FONT-FAMILY: 新宋体; LETTER-SPACING: 0pt; COLOR: rgb(0,0,0); FONT-SIZE: 10.5pt; FONT-WEIGHT: normal; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"><font face="新宋体">月</font></span><span style="TEXT-TRANSFORM: none; FONT-STYLE: normal; FONT-FAMILY: 新宋体; LETTER-SPACING: 0pt; COLOR: rgb(0,0,0); FONT-SIZE: 10.5pt; FONT-WEIGHT: normal; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">13</span><span style="TEXT-TRANSFORM: none; FONT-STYLE: normal; FONT-FAMILY: 新宋体; LETTER-SPACING: 0pt; COLOR: rgb(0,0,0); FONT-SIZE: 10.5pt; FONT-WEIGHT: normal; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"><font face="新宋体">日</font></span><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">
# <o:p></o:p></span></p>
# <p align="justify" class="p" style="TEXT-JUSTIFY: inter-ideograph; TEXT-ALIGN: justify; LINE-HEIGHT: 20pt; MARGIN-TOP: 3.8pt; MARGIN-BOTTOM: 0pt; MARGIN-RIGHT: 0pt; mso-pagination: widow-orphan"><b><span style="TEXT-TRANSFORM: none; FONT-STYLE: normal; FONT-FAMILY: 新宋体; LETTER-SPACING: 0pt; COLOR: rgb(0,0,0); FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"><font face="新宋体">二、中标结果</font>  </span></b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">
# <o:p></o:p></span></p>
# <table align="center" class="MsoNormalTable" style="WIDTH: 426pt; BORDER-COLLAPSE: collapse; MARGIN-LEFT: 13pt; mso-table-layout-alt: fixed; mso-padding-alt: 0.0000pt 0.0000pt 0.0000pt 0.0000pt">
# <tbody>
# <tr style="HEIGHT: 31.05pt">
# <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: windowtext 1pt solid; PADDING-BOTTOM: 0pt; PADDING-LEFT: 5.4pt; WIDTH: 40.95pt; PADDING-RIGHT: 5.4pt; BORDER-TOP: windowtext 1pt solid; BORDER-RIGHT: windowtext 1pt solid; PADDING-TOP: 0pt; mso-border-left-alt: 1.0000pt solid windowtext; mso-border-right-alt: 1.0000pt solid windowtext; mso-border-top-alt: 1.0000pt solid windowtext; mso-border-bottom-alt: 1.0000pt solid windowtext" valign="center" width="54"> <p align="center" class="p" style="TEXT-ALIGN: center; LINE-HEIGHT: 16pt; MARGIN: 0pt; mso-pagination: widow-orphan"><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">中标项目</span></b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-font-kerning: 0.0000pt">
# <o:p></o:p></span></p> </td>
# <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: rgb(255,255,255) 31.875pt; PADDING-BOTTOM: 0pt; PADDING-LEFT: 5.4pt; WIDTH: 202.05pt; PADDING-RIGHT: 5.4pt; BORDER-TOP: windowtext 1pt solid; BORDER-RIGHT: windowtext 1pt solid; PADDING-TOP: 0pt; mso-border-left-alt: 31.8750pt none rgb(255,255,255); mso-border-right-alt: 1.0000pt solid windowtext; mso-border-top-alt: 1.0000pt solid windowtext; mso-border-bottom-alt: 1.0000pt solid windowtext" valign="center" width="269"> <p align="center" class="p" style="TEXT-ALIGN: center; LINE-HEIGHT: 16pt; MARGIN: 0pt; mso-pagination: widow-orphan"><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">中标候选人名称</span></b><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-font-kerning: 0.0000pt"> </span></b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-font-kerning: 0.0000pt">
# <o:p></o:p></span></p> </td>
# <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: rgb(255,255,255) 31.875pt; PADDING-BOTTOM: 0pt; PADDING-LEFT: 5.4pt; WIDTH: 66.15pt; PADDING-RIGHT: 5.4pt; BORDER-TOP: windowtext 1pt solid; BORDER-RIGHT: windowtext 1pt solid; PADDING-TOP: 0pt; mso-border-left-alt: 31.8750pt none rgb(255,255,255); mso-border-right-alt: 1.0000pt solid windowtext; mso-border-top-alt: 1.0000pt solid windowtext; mso-border-bottom-alt: 1.0000pt solid windowtext" valign="center" width="88"> <p align="center" class="p" style="TEXT-ALIGN: center; LINE-HEIGHT: 16pt; MARGIN: 0pt; mso-pagination: widow-orphan"><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">综合打分</span></b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-font-kerning: 0.0000pt">
# <o:p></o:p></span></p> </td>
# <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: rgb(255,255,255) 31.875pt; PADDING-BOTTOM: 0pt; PADDING-LEFT: 5.4pt; WIDTH: 75.7pt; PADDING-RIGHT: 5.4pt; BORDER-TOP: windowtext 1pt solid; BORDER-RIGHT: windowtext 1pt solid; PADDING-TOP: 0pt; mso-border-left-alt: 31.8750pt none rgb(255,255,255); mso-border-right-alt: 1.0000pt solid windowtext; mso-border-top-alt: 1.0000pt solid windowtext; mso-border-bottom-alt: 1.0000pt solid windowtext" valign="center" width="100"> <p align="center" class="p" style="TEXT-ALIGN: center; LINE-HEIGHT: 16pt; MARGIN: 0pt; mso-pagination: widow-orphan"><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">最终报价</span></b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-font-kerning: 0.0000pt">
# <o:p></o:p></span></p> </td>
# <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: rgb(255,255,255) 31.875pt; PADDING-BOTTOM: 0pt; PADDING-LEFT: 5.4pt; WIDTH: 41.15pt; PADDING-RIGHT: 5.4pt; BORDER-TOP: windowtext 1pt solid; BORDER-RIGHT: windowtext 1pt solid; PADDING-TOP: 0pt; mso-border-left-alt: 31.8750pt none rgb(255,255,255); mso-border-right-alt: 1.0000pt solid windowtext; mso-border-top-alt: 1.0000pt solid windowtext; mso-border-bottom-alt: 1.0000pt solid windowtext" valign="center" width="54"> <p align="center" class="p" style="TEXT-ALIGN: center; LINE-HEIGHT: 16pt; MARGIN: 0pt; mso-pagination: widow-orphan"><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">推荐排名</span></b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-font-kerning: 0.0000pt">
# <o:p></o:p></span></p> </td>
# </tr>
# <tr style="HEIGHT: 40.45pt">
# <td rowspan="3" style="BORDER-BOTTOM: rgb(255,255,255) 31.875pt; BORDER-LEFT: windowtext 1pt solid; PADDING-BOTTOM: 0pt; PADDING-LEFT: 5.4pt; WIDTH: 40.95pt; PADDING-RIGHT: 5.4pt; BORDER-TOP: rgb(255,255,255) 31.875pt; BORDER-RIGHT: windowtext 1pt solid; PADDING-TOP: 0pt; mso-border-left-alt: 1.0000pt solid windowtext; mso-border-right-alt: 1.0000pt solid windowtext; mso-border-top-alt: 31.8750pt none rgb(255,255,255); mso-border-bottom-alt: 31.8750pt none rgb(255,255,255)" valign="center" width="54"> <p align="center" class="p" style="TEXT-ALIGN: center; LINE-HEIGHT: 16pt; MARGIN: 0pt; mso-pagination: widow-orphan"><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">靖州县城区P8户外全彩显示屏工程</span><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-font-kerning: 0.0000pt">
# <o:p></o:p></span></p> </td>
# <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: rgb(255,255,255) 31.875pt; PADDING-BOTTOM: 0pt; PADDING-LEFT: 5.4pt; WIDTH: 202.05pt; PADDING-RIGHT: 5.4pt; BORDER-TOP: rgb(255,255,255) 31.875pt; BORDER-RIGHT: windowtext 1pt solid; PADDING-TOP: 0pt; mso-border-left-alt: 31.8750pt none rgb(255,255,255); mso-border-right-alt: 1.0000pt solid windowtext; mso-border-top-alt: 31.8750pt none rgb(255,255,255); mso-border-bottom-alt: 1.0000pt solid windowtext" valign="center" width="269"> <p align="justify" class="p" style="TEXT-JUSTIFY: inter-ideograph; TEXT-ALIGN: justify; LINE-HEIGHT: 21pt; MARGIN: 0pt; mso-pagination: widow-orphan"><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">怀化光捷通讯技术有限公司 </span><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-font-kerning: 0.0000pt">
# <o:p></o:p></span></p> </td>
# <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: rgb(255,255,255) 31.875pt; PADDING-BOTTOM: 0pt; PADDING-LEFT: 5.4pt; WIDTH: 66.15pt; PADDING-RIGHT: 5.4pt; BORDER-TOP: rgb(255,255,255) 31.875pt; BORDER-RIGHT: windowtext 1pt solid; PADDING-TOP: 0pt; mso-border-left-alt: 31.8750pt none rgb(255,255,255); mso-border-right-alt: 1.0000pt solid windowtext; mso-border-top-alt: 31.8750pt none rgb(255,255,255); mso-border-bottom-alt: 1.0000pt solid windowtext" valign="center" width="88"> <p align="center" class="p" style="TEXT-ALIGN: center; LINE-HEIGHT: 21pt; MARGIN: 0pt; mso-pagination: widow-orphan"><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">72.92 </span><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-font-kerning: 0.0000pt">
# <o:p></o:p></span></p> </td>
# <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: rgb(255,255,255) 31.875pt; PADDING-BOTTOM: 0pt; PADDING-LEFT: 5.4pt; WIDTH: 75.7pt; PADDING-RIGHT: 5.4pt; BORDER-TOP: rgb(255,255,255) 31.875pt; BORDER-RIGHT: windowtext 1pt solid; PADDING-TOP: 0pt; mso-border-left-alt: 31.8750pt none rgb(255,255,255); mso-border-right-alt: 1.0000pt solid windowtext; mso-border-top-alt: 31.8750pt none rgb(255,255,255); mso-border-bottom-alt: 1.0000pt solid windowtext" valign="center" width="100"> <p align="center" class="p" style="TEXT-ALIGN: center; LINE-HEIGHT: 21pt; MARGIN: 0pt; mso-pagination: widow-orphan"><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">1908801.00 </span><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-font-kerning: 0.0000pt">
# <o:p></o:p></span></p> </td>
# <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: rgb(255,255,255) 31.875pt; PADDING-BOTTOM: 0pt; PADDING-LEFT: 5.4pt; WIDTH: 41.15pt; PADDING-RIGHT: 5.4pt; BORDER-TOP: rgb(255,255,255) 31.875pt; BORDER-RIGHT: windowtext 1pt solid; PADDING-TOP: 0pt; mso-border-left-alt: 31.8750pt none rgb(255,255,255); mso-border-right-alt: 1.0000pt solid windowtext; mso-border-top-alt: 31.8750pt none rgb(255,255,255); mso-border-bottom-alt: 1.0000pt solid windowtext" valign="center" width="54"> <p align="center" class="p" style="TEXT-ALIGN: center; LINE-HEIGHT: 16pt; MARGIN: 0pt; mso-pagination: widow-orphan"><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-font-kerning: 0.0000pt">1</span><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-font-kerning: 0.0000pt">
# <o:p></o:p></span></p> </td>
# </tr>
# <tr style="HEIGHT: 40.45pt">
# <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: rgb(255,255,255) 31.875pt; PADDING-BOTTOM: 0pt; PADDING-LEFT: 5.4pt; WIDTH: 202.05pt; PADDING-RIGHT: 5.4pt; BORDER-TOP: rgb(255,255,255) 31.875pt; BORDER-RIGHT: windowtext 1pt solid; PADDING-TOP: 0pt; mso-border-left-alt: 31.8750pt none rgb(255,255,255); mso-border-right-alt: 1.0000pt solid windowtext; mso-border-top-alt: 31.8750pt none rgb(255,255,255); mso-border-bottom-alt: 1.0000pt solid windowtext" valign="center" width="269"> <p align="justify" class="p" style="TEXT-JUSTIFY: inter-ideograph; TEXT-ALIGN: justify; LINE-HEIGHT: 21pt; MARGIN: 0pt; mso-pagination: widow-orphan"><span style="FONT-FAMILY: 新宋体; COLOR: rgb(0,0,0); FONT-SIZE: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"> 怀化市海迅电子科技有限公司</span><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-font-kerning: 0.0000pt"> </span><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-font-kerning: 0.0000pt">
# <o:p></o:p></span></p> </td>
# <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: rgb(255,255,255) 31.875pt; PADDING-BOTTOM: 0pt; PADDING-LEFT: 5.4pt; WIDTH: 66.15pt; PADDING-RIGHT: 5.4pt; BORDER-TOP: rgb(255,255,255) 31.875pt; BORDER-RIGHT: windowtext 1pt solid; PADDING-TOP: 0pt; mso-border-left-alt: 31.8750pt none rgb(255,255,255); mso-border-right-alt: 1.0000pt solid windowtext; mso-border-top-alt: 31.8750pt none rgb(255,255,255); mso-border-bottom-alt: 1.0000pt solid windowtext" valign="center" width="88"> <p align="center" class="p" style="TEXT-ALIGN: center; LINE-HEIGHT: 21pt; MARGIN: 0pt; mso-pagination: widow-orphan"><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">58.29 </span><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-font-kerning: 0.0000pt">
# <o:p></o:p></span></p> </td>
# <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: rgb(255,255,255) 31.875pt; PADDING-BOTTOM: 0pt; PADDING-LEFT: 5.4pt; WIDTH: 75.7pt; PADDING-RIGHT: 5.4pt; BORDER-TOP: rgb(255,255,255) 31.875pt; BORDER-RIGHT: windowtext 1pt solid; PADDING-TOP: 0pt; mso-border-left-alt: 31.8750pt none rgb(255,255,255); mso-border-right-alt: 1.0000pt solid windowtext; mso-border-top-alt: 31.8750pt none rgb(255,255,255); mso-border-bottom-alt: 1.0000pt solid windowtext" valign="center" width="100"> <p align="center" class="p" style="TEXT-ALIGN: center; LINE-HEIGHT: 21pt; MARGIN: 0pt; mso-pagination: widow-orphan"><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"> 1916802.00</span><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-font-kerning: 0.0000pt">
# <o:p></o:p></span></p> </td>
# <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: rgb(255,255,255) 31.875pt; PADDING-BOTTOM: 0pt; PADDING-LEFT: 5.4pt; WIDTH: 41.15pt; PADDING-RIGHT: 5.4pt; BORDER-TOP: rgb(255,255,255) 31.875pt; BORDER-RIGHT: windowtext 1pt solid; PADDING-TOP: 0pt; mso-border-left-alt: 31.8750pt none rgb(255,255,255); mso-border-right-alt: 1.0000pt solid windowtext; mso-border-top-alt: 31.8750pt none rgb(255,255,255); mso-border-bottom-alt: 1.0000pt solid windowtext" valign="center" width="54"> <p align="center" class="p" style="TEXT-ALIGN: center; LINE-HEIGHT: 16pt; MARGIN: 0pt; mso-pagination: widow-orphan"><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-font-kerning: 0.0000pt">2</span><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-font-kerning: 0.0000pt">
# <o:p></o:p></span></p> </td>
# </tr>
# <tr style="HEIGHT: 40.45pt">
# <td style="BORDER-BOTTOM: rgb(255,255,255) 31.875pt; BORDER-LEFT: rgb(255,255,255) 31.875pt; PADDING-BOTTOM: 0pt; PADDING-LEFT: 5.4pt; WIDTH: 202.05pt; PADDING-RIGHT: 5.4pt; BORDER-TOP: rgb(255,255,255) 31.875pt; BORDER-RIGHT: windowtext 1pt solid; PADDING-TOP: 0pt; mso-border-left-alt: 31.8750pt none rgb(255,255,255); mso-border-right-alt: 1.0000pt solid windowtext; mso-border-top-alt: 31.8750pt none rgb(255,255,255); mso-border-bottom-alt: 31.8750pt none rgb(255,255,255)" valign="center" width="269"> <p align="justify" class="p" style="TEXT-JUSTIFY: inter-ideograph; TEXT-ALIGN: justify; LINE-HEIGHT: 21pt; MARGIN: 0pt; mso-pagination: widow-orphan"><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">怀化联威科技有限公司</span><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-font-kerning: 0.0000pt"> </span><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-font-kerning: 0.0000pt">
# <o:p></o:p></span></p> </td>
# <td style="BORDER-BOTTOM: rgb(255,255,255) 31.875pt; BORDER-LEFT: rgb(255,255,255) 31.875pt; PADDING-BOTTOM: 0pt; PADDING-LEFT: 5.4pt; WIDTH: 66.15pt; PADDING-RIGHT: 5.4pt; BORDER-TOP: rgb(255,255,255) 31.875pt; BORDER-RIGHT: windowtext 1pt solid; PADDING-TOP: 0pt; mso-border-left-alt: 31.8750pt none rgb(255,255,255); mso-border-right-alt: 1.0000pt solid windowtext; mso-border-top-alt: 31.8750pt none rgb(255,255,255); mso-border-bottom-alt: 31.8750pt none rgb(255,255,255)" valign="center" width="88"> <p align="center" class="p" style="TEXT-ALIGN: center; LINE-HEIGHT: 21pt; MARGIN: 0pt; mso-pagination: widow-orphan"><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">54.64 </span><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-font-kerning: 0.0000pt">
# <o:p></o:p></span></p> </td>
# <td style="BORDER-BOTTOM: rgb(255,255,255) 31.875pt; BORDER-LEFT: rgb(255,255,255) 31.875pt; PADDING-BOTTOM: 0pt; PADDING-LEFT: 5.4pt; WIDTH: 75.7pt; PADDING-RIGHT: 5.4pt; BORDER-TOP: rgb(255,255,255) 31.875pt; BORDER-RIGHT: windowtext 1pt solid; PADDING-TOP: 0pt; mso-border-left-alt: 31.8750pt none rgb(255,255,255); mso-border-right-alt: 1.0000pt solid windowtext; mso-border-top-alt: 31.8750pt none rgb(255,255,255); mso-border-bottom-alt: 31.8750pt none rgb(255,255,255)" valign="center" width="100"> <p align="center" class="p" style="TEXT-ALIGN: center; LINE-HEIGHT: 21pt; MARGIN: 0pt; mso-pagination: widow-orphan"><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"> 1914503.00</span><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-font-kerning: 0.0000pt">
# <o:p></o:p></span></p> </td>
# <td style="BORDER-BOTTOM: rgb(255,255,255) 31.875pt; BORDER-LEFT: rgb(255,255,255) 31.875pt; PADDING-BOTTOM: 0pt; PADDING-LEFT: 5.4pt; WIDTH: 41.15pt; PADDING-RIGHT: 5.4pt; BORDER-TOP: rgb(255,255,255) 31.875pt; BORDER-RIGHT: windowtext 1pt solid; PADDING-TOP: 0pt; mso-border-left-alt: 31.8750pt none rgb(255,255,255); mso-border-right-alt: 1.0000pt solid windowtext; mso-border-top-alt: 31.8750pt none rgb(255,255,255); mso-border-bottom-alt: 31.8750pt none rgb(255,255,255)" valign="center" width="54"> <p align="center" class="p" style="TEXT-ALIGN: center; LINE-HEIGHT: 16pt; MARGIN: 0pt; mso-pagination: widow-orphan"><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-font-kerning: 0.0000pt">3</span><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-font-kerning: 0.0000pt">
# <o:p></o:p></span></p> </td>
# </tr>
# <tr style="HEIGHT: 18.9pt">
# <td style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: windowtext 1pt solid; PADDING-BOTTOM: 0pt; PADDING-LEFT: 5.4pt; WIDTH: 40.95pt; PADDING-RIGHT: 5.4pt; BORDER-TOP: windowtext 1pt solid; BORDER-RIGHT: windowtext 1pt solid; PADDING-TOP: 0pt; mso-border-left-alt: 1.0000pt solid windowtext; mso-border-right-alt: 1.0000pt solid windowtext; mso-border-top-alt: 1.0000pt solid windowtext; mso-border-bottom-alt: 1.0000pt solid windowtext" valign="center" width="54"> <p align="center" class="p" style="TEXT-ALIGN: center; LINE-HEIGHT: 16pt; MARGIN: 0pt; mso-pagination: widow-orphan"><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-font-kerning: 0.0000pt"> </span><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-font-kerning: 0.0000pt">
# <o:p></o:p></span></p> </td>
# <td colspan="4" style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: rgb(255,255,255) 31.875pt; PADDING-BOTTOM: 0pt; PADDING-LEFT: 5.4pt; WIDTH: 385.05pt; PADDING-RIGHT: 5.4pt; BORDER-TOP: windowtext 1pt solid; BORDER-RIGHT: windowtext 1pt solid; PADDING-TOP: 0pt; mso-border-left-alt: 31.8750pt none rgb(255,255,255); mso-border-right-alt: 1.0000pt solid windowtext; mso-border-top-alt: 1.0000pt solid windowtext; mso-border-bottom-alt: 1.0000pt solid windowtext" valign="center" width="513"> <p align="justify" class="p" style="TEXT-JUSTIFY: inter-ideograph; TEXT-ALIGN: justify; LINE-HEIGHT: 16pt; MARGIN: 0pt; mso-pagination: widow-orphan"><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">注：排位在第一的中标候选人为中标单位</span><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-font-kerning: 0.0000pt">
# <o:p></o:p></span></p> </td>
# </tr>
# </tbody>
# </table>
# <p class="p" style="TEXT-ALIGN: left; LINE-HEIGHT: 18pt; MARGIN-TOP: 7.6pt; MARGIN-BOTTOM: 0pt; MARGIN-RIGHT: 0pt; mso-pagination: widow-orphan"><b><span style="TEXT-TRANSFORM: none; FONT-STYLE: normal; FONT-FAMILY: 新宋体; LETTER-SPACING: 0pt; COLOR: rgb(0,0,0); FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"><font face="新宋体">三、评标委员会成员名单：</font></span></b><span style="TEXT-TRANSFORM: none; FONT-STYLE: normal; FONT-FAMILY: 新宋体; LETTER-SPACING: 0pt; COLOR: rgb(0,0,0); FONT-SIZE: 10.5pt; FONT-WEIGHT: normal; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"> </span><span style="TEXT-TRANSFORM: none; FONT-STYLE: normal; FONT-FAMILY: 新宋体; LETTER-SPACING: 0pt; COLOR: rgb(0,0,0); FONT-SIZE: 10.5pt; FONT-WEIGHT: normal; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"> </span><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">
# <o:p></o:p></span></p>
# <p align="justify" class="p" style="TEXT-JUSTIFY: inter-ideograph; TEXT-ALIGN: justify; LINE-HEIGHT: 18pt; TEXT-INDENT: 23.9pt; MARGIN: 7.6pt 0pt 0pt 7.6pt; mso-pagination: widow-orphan"><span style="TEXT-TRANSFORM: none; FONT-STYLE: normal; FONT-FAMILY: 新宋体; LETTER-SPACING: 0pt; COLOR: rgb(0,0,0); FONT-SIZE: 10.5pt; FONT-WEIGHT: normal; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"><font face="新宋体">投标人如对中标（成交）公告有异议的，请于本公告发布之日起七个工作日内，以书面形式向本代理机构提出质疑。</font></span><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">
# <o:p></o:p></span></p>
# <p class="MsoNormal" style="TEXT-ALIGN: left; MARGIN-TOP: 7.85pt; LAYOUT-GRID-MODE: char; TEXT-AUTOSPACE: ideograph-numeric; MARGIN-RIGHT: 0pt; mso-para-margin-right: 0.0000gd; mso-pagination: none; mso-layout-grid-align: none; mso-para-margin-top: 0.5000gd"><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt"><font face="新宋体">四、</font></span></b><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt"><font face="新宋体">采购人名称：</font></span></b><b><u><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; TEXT-DECORATION: underline; mso-spacerun: 'yes'; text-underline: single; mso-font-kerning: 1.0000pt"><font face="新宋体">靖州苗族侗族自治县城市管理行政执法大队</font></span></u></b><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">             </span></b><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">
# <o:p></o:p></span></b></p>
# <p class="MsoNormal" style="TEXT-ALIGN: left; MARGIN-TOP: 7.85pt; LAYOUT-GRID-MODE: char; TEXT-AUTOSPACE: ideograph-numeric; MARGIN-RIGHT: 0pt; mso-para-margin-right: 0.0000gd; mso-pagination: none; mso-layout-grid-align: none; mso-para-margin-top: 0.5000gd"><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt"><font face="新宋体">地址：</font></span></b><b><u><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; TEXT-DECORATION: underline; mso-spacerun: 'yes'; text-underline: single; mso-font-kerning: 1.0000pt"><font face="新宋体">靖州县</font></span></u></b><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">
# <o:p></o:p></span></b></p>
# <p class="MsoPlainText" style="TEXT-ALIGN: left; MARGIN-TOP: 7.85pt; LAYOUT-GRID-MODE: char; TEXT-AUTOSPACE: ideograph-numeric; MARGIN-RIGHT: 0pt; mso-para-margin-right: 0.0000gd; mso-pagination: none; mso-layout-grid-align: none; mso-para-margin-top: 0.5000gd"><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt"><font face="新宋体">电话：</font> </span></b><b><u><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; TEXT-DECORATION: underline; mso-spacerun: 'yes'; text-underline: single; mso-font-kerning: 1.0000pt">15974058222</span></u></b><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">                          </span></b><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">
# <o:p></o:p></span></b></p>
# <p class="MsoPlainText" style="TEXT-ALIGN: left; MARGIN-TOP: 7.85pt; LAYOUT-GRID-MODE: char; TEXT-AUTOSPACE: ideograph-numeric; MARGIN-RIGHT: 0pt; mso-para-margin-right: 0.0000gd; mso-pagination: none; mso-layout-grid-align: none; mso-para-margin-top: 0.5000gd"><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt"><font face="新宋体">联系人：</font></span></b><b><u><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; TEXT-DECORATION: underline; mso-spacerun: 'yes'; text-underline: single; mso-font-kerning: 1.0000pt"><font face="新宋体">丁忠清</font></span></u></b><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">
# <o:p></o:p></span></b></p>
# <p class="MsoNormal" style="TEXT-ALIGN: left; MARGIN-TOP: 7.85pt; TEXT-INDENT: -10.55pt; LAYOUT-GRID-MODE: char; TEXT-AUTOSPACE: ideograph-numeric; MARGIN-LEFT: 10.5pt; MARGIN-RIGHT: 0pt; mso-para-margin-right: 0.0000gd; mso-pagination: none; mso-layout-grid-align: none; mso-char-indent-count: -1.0000; mso-para-margin-top: 0.5000gd"><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt"><font face="新宋体">采购代理机构名称：湖南</font></span></b><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt"><font face="新宋体">三湘工程</font></span></b><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt"><font face="新宋体">管理有限公司</font>     </span></b><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">
# <o:p></o:p></span></b></p>
# <p class="MsoNormal" style="TEXT-ALIGN: left; MARGIN-TOP: 7.85pt; TEXT-INDENT: -10.55pt; LAYOUT-GRID-MODE: char; TEXT-AUTOSPACE: ideograph-numeric; MARGIN-LEFT: 10.5pt; MARGIN-RIGHT: 0pt; mso-para-margin-right: 0.0000gd; mso-pagination: none; mso-layout-grid-align: none; mso-char-indent-count: -1.0000; mso-para-margin-top: 0.5000gd"><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt"><font face="新宋体">地址：</font></span></b><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt"><font face="新宋体">靖州县异溪南路</font></span></b><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">172号</span></b><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">
# <o:p></o:p></span></b></p>
# <p class="MsoNormal" style="TEXT-ALIGN: left; MARGIN-TOP: 7.85pt; TEXT-INDENT: -10.55pt; LAYOUT-GRID-MODE: char; TEXT-AUTOSPACE: ideograph-numeric; MARGIN-LEFT: 10.5pt; MARGIN-RIGHT: 0pt; mso-para-margin-right: 0.0000gd; mso-pagination: none; mso-layout-grid-align: none; mso-char-indent-count: -1.0000; mso-para-margin-top: 0.5000gd"><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt"><font face="新宋体">联系人：</font></span></b><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt"><font face="新宋体">雷振</font></span></b><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">                                   </span></b><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">
# <o:p></o:p></span></b></p>
# <p class="MsoNormal" style="TEXT-ALIGN: left; MARGIN-TOP: 7.85pt; TEXT-INDENT: -10.55pt; LAYOUT-GRID-MODE: char; TEXT-AUTOSPACE: ideograph-numeric; MARGIN-LEFT: 10.5pt; MARGIN-RIGHT: 0pt; mso-para-margin-right: 0.0000gd; mso-pagination: none; mso-layout-grid-align: none; mso-char-indent-count: -1.0000; mso-para-margin-top: 0.5000gd"><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt"><font face="新宋体">电话：</font>07</span></b><b><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">45-2607577  15907458501</span></b><b><u><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; FONT-WEIGHT: bold; TEXT-DECORATION: underline; mso-spacerun: 'yes'; text-underline: single; mso-font-kerning: 1.0000pt">
# <o:p></o:p></span></u></b></p>
# <p class="MsoNormal"><span style="FONT-FAMILY: 新宋体; FONT-SIZE: 10.5pt; mso-spacerun: 'yes'; mso-font-kerning: 1.0000pt">
# <o:p>
#            
#          </o:p></span></p>
# </div>
# <p align="left"></p>
# </div>
# <b>附件下载：</b>
# <br/>      
#      <a href="http://www.ccgp-hunan.gov.cn/portal/protalAction!downloadFile2.action?fileid=1000286578">报价一览表.zip</a>
# <br/>
# <br/>
# <div id="div_div" style="text-align:center;">
# <div id="qr_container" style="margin:auto; position:relative;padding-bottom:10px;font-size:23px;">扫一扫在手机打开当前页</div>
# <canvas height="132" id="Canvas" width="132"></canvas></div>
# <!-- 用来校验该浏览器是否支持HTML5 -->
# </div>
# <div class="share-box">
# <div class="share-l fl">
# <script src="/include/cms/js/bdShare.js" type="text/javascript"></script><div id="share" style="float:right;margin-top:0px;width:100%;display: inline;"><div class="bdsharebuttonbox bdshare-button-style0-16" data-bd-bind="1555334921657" style="float:right;display: inline;white-space: nowrap;height: 28px;"><a class="bds_weixin" data-cmd="weixin" href="javascript:void(0)" title="分享到微信"></a><a class="bds_tsina" data-cmd="tsina" href="javascript:void(0)" title="分享到新浪微博"></a><a class="bds_tqq" data-cmd="tqq" href="javascript:void(0)" title="分享到腾讯微博"></a><a class="bds_qzone" data-cmd="qzone" href="javascript:void(0)" title="分享到QQ空间"></a><a class="bds_renren" data-cmd="renren" href="javascript:void(0)" title="分享到人人网"></a></div></div>
# </div>
# <div class="share-r fr">
# <span class="print" onclick="window.print();">打印本页</span> <span class="close" onclick="window.close();">关闭窗口</span>
# </div>
# </div>
# </div>
# </div>"""

if __name__ == '__main__':
    list_all = ['anbang*anhui_anqing']
    bt=time.time()
    # p_diqu = parseDiqu()
    # print(p_diqu.parse_diqu(txtx))
    for quyu in list_all:
        # 链接数据库,读取数据
        df=getpage_herf_ggstart_time(quyu)
        p_diqu = parseDiqu()
        # conp = ['postgres', 'since2015', '192.168.3.171', 'anbang', 'anhui_anqing']
        # engine = create_engine('postgresql+psycopg2://%s:%s@%s/%s' % (conp[0], conp[1], conp[2], conp[3]))
        # df = pd.read_sql_table(table_name='gg_html', con=engine, schema=conp[4], index_col=None, coerce_float=True, parse_dates=None, columns=None, chunksize=None)
        df['diqu_code'] = df['page'].map(lambda x: p_diqu.parse_diqu(x))
        write_to_table(df, 'gg_qucode',quyu, if_exists='replace')
        print(df['diqu_code'].isnull().sum())
        print(df.info())
        # print(df['diqu_code'].value_counts())
    print(time.time() - bt)













