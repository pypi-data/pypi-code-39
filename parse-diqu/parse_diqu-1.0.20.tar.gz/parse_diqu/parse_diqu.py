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
        if object_list !=[]:
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
            df_final['length']=df_final['code'].map(lambda x:len(x))
            df_final.sort_values(by=['rank'], ascending=True, inplace=True)
            df_final.sort_values(by=['cnt'], ascending=False, inplace=True)
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

# txtx = """<div class="frameReport" id="myPrintArea">
# <div class="reportTitle">
# <h1>安庆一中龙山校区空调采购项目质疑的回复（二）</h1>
# <span>访问次数：</span><span id="count"></span>
# </div>
# <p>
# </p><p align="justify" class="MsoNormal" style="TEXT-ALIGN: justify; TEXT-JUSTIFY: inter-ideograph; LINE-HEIGHT: 26pt; TEXT-AUTOSPACE: ideograph-numeric; MARGIN-RIGHT: 0pt; TEXT-INDENT: 24pt; mso-pagination: none; mso-line-height-rule: exactly; mso-char-indent-count: 2.0000; mso-para-margin-right: 0.0000gd"><span style="FONT-SIZE: 12pt; FONT-FAMILY: 宋体; COLOR: rgb(51,51,51); mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"><font face="宋体">安庆一中龙山校区空调采购（</font>CG-AQ-2018-149 &amp;nbsp;&amp;nbsp;&amp;nbsp;AQZB-2018-0161）的质疑已收悉，现答复如下：</span><span style="FONT-SIZE: 12pt; FONT-FAMILY: 宋体; COLOR: rgb(51,51,51); mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"><!--?xml:namespace prefix = "o" /--><o:p></o:p></span></p>
# <p align="justify" class="MsoNormal" style="TEXT-ALIGN: justify; MARGIN-LEFT: 0pt; TEXT-JUSTIFY: inter-ideograph; LINE-HEIGHT: 26pt; TEXT-AUTOSPACE: ideograph-numeric; MARGIN-RIGHT: 0pt; TEXT-INDENT: 24pt; mso-pagination: none; mso-line-height-rule: exactly; mso-char-indent-count: 2.0000; mso-para-margin-right: 0.0000gd; mso-para-margin-left: 0.0000gd"><span style="FONT-SIZE: 12pt; FONT-FAMILY: 宋体; COLOR: rgb(51,51,51); mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">1、招标文件第三章：《货物需求及技术要求》中货物需求一览表中第2项“分体柜机”中“额定功率制制热：2240W及以下”的要求，目前只有个别品牌生产，属于非标准常规型号，建议更改为常规型号，也方便以后维修和配件的通用。</span><span style="FONT-SIZE: 12pt; FONT-FAMILY: 宋体; COLOR: rgb(51,51,51); mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"><o:p></o:p></span></p>
# <p align="justify" class="MsoNormal" style="TEXT-ALIGN: justify; MARGIN-LEFT: 0pt; TEXT-JUSTIFY: inter-ideograph; LINE-HEIGHT: 26pt; TEXT-AUTOSPACE: ideograph-numeric; MARGIN-RIGHT: 0pt; TEXT-INDENT: 24pt; mso-pagination: none; mso-line-height-rule: exactly; mso-char-indent-count: 2.0000; mso-para-margin-right: 0.0000gd; mso-para-margin-left: 0.0000gd"><span style="FONT-SIZE: 12pt; FONT-FAMILY: 宋体; COLOR: rgb(51,51,51); mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"><font face="宋体">答：按照招标文件执行。格力、美的、海尔等品牌能够满足以上要求。</font></span><span style="FONT-SIZE: 12pt; FONT-FAMILY: 宋体; COLOR: rgb(51,51,51); mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"><o:p></o:p></span></p>
# <p align="justify" class="MsoNormal" style="TEXT-ALIGN: justify; MARGIN-LEFT: 0pt; TEXT-JUSTIFY: inter-ideograph; LINE-HEIGHT: 26pt; TEXT-AUTOSPACE: ideograph-numeric; MARGIN-RIGHT: 0pt; TEXT-INDENT: 24pt; mso-pagination: none; mso-line-height-rule: exactly; mso-char-indent-count: 2.0000; mso-para-margin-right: 0.0000gd; mso-para-margin-left: 0.0000gd"><span style="FONT-SIZE: 12pt; FONT-FAMILY: 宋体; COLOR: rgb(51,51,51); mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">2、招标文件第三章：《货物需求及技术要求》中货物需求一览表中第3项“分体柜机”中“额定功率制冷/制热：3550W/3880W 及以下”的要求，目前只有个别品牌生产，属于非标准常规型号，建议更改为常规型号，也方便以后维修和配件的通用。</span><span style="FONT-SIZE: 12pt; FONT-FAMILY: 宋体; COLOR: rgb(51,51,51); mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"><o:p></o:p></span></p>
# <p align="justify" class="MsoNormal" style="TEXT-ALIGN: justify; MARGIN-LEFT: 0pt; TEXT-JUSTIFY: inter-ideograph; LINE-HEIGHT: 26pt; TEXT-AUTOSPACE: ideograph-numeric; MARGIN-RIGHT: 0pt; TEXT-INDENT: 24pt; mso-pagination: none; mso-line-height-rule: exactly; mso-char-indent-count: 2.0000; mso-para-margin-right: 0.0000gd; mso-para-margin-left: 0.0000gd"><span style="FONT-SIZE: 12pt; FONT-FAMILY: 宋体; COLOR: rgb(51,51,51); mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"><font face="宋体">答：按照招标文件执行。格力、美的、海尔等品牌能够满足以上要求。</font></span><span style="FONT-SIZE: 12pt; FONT-FAMILY: 宋体; COLOR: rgb(51,51,51); mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"><o:p></o:p></span></p>
# <p align="justify" class="MsoNormal" style="TEXT-ALIGN: justify; MARGIN-LEFT: 0pt; TEXT-JUSTIFY: inter-ideograph; LINE-HEIGHT: 26pt; TEXT-AUTOSPACE: ideograph-numeric; MARGIN-RIGHT: 0pt; TEXT-INDENT: 24pt; mso-pagination: none; mso-line-height-rule: exactly; mso-char-indent-count: 2.0000; mso-para-margin-right: 0.0000gd; mso-para-margin-left: 0.0000gd"><span style="FONT-SIZE: 12pt; FONT-FAMILY: 宋体; COLOR: rgb(51,51,51); mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">3、招标文件其他内容保持不变，按照招标文件的条款执行。</span><span style="FONT-SIZE: 12pt; FONT-FAMILY: 宋体; COLOR: rgb(51,51,51); mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"><o:p></o:p></span></p>
# <p align="justify" class="MsoNormal" style="TEXT-ALIGN: justify; MARGIN-LEFT: 0pt; TEXT-JUSTIFY: inter-ideograph; LINE-HEIGHT: 26pt; TEXT-AUTOSPACE: ideograph-numeric; MARGIN-RIGHT: 0pt; TEXT-INDENT: 24pt; mso-pagination: none; mso-line-height-rule: exactly; mso-char-indent-count: 2.0000; mso-para-margin-right: 0.0000gd; mso-para-margin-left: 0.0000gd"><span style="FONT-SIZE: 12pt; FONT-FAMILY: 宋体; COLOR: rgb(51,51,51); mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"><o:p>&amp;nbsp;</o:p></span></p>
# <p align="justify" class="MsoNormal" style="TEXT-ALIGN: justify; TEXT-JUSTIFY: inter-ideograph; LINE-HEIGHT: 23pt; TEXT-AUTOSPACE: ideograph-numeric; MARGIN-RIGHT: 0pt; mso-pagination: none; mso-line-height-rule: exactly; mso-para-margin-right: 0.0000gd"><span style="FONT-SIZE: 12pt; FONT-FAMILY: 宋体; COLOR: rgb(51,51,51); mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"><o:p>&amp;nbsp;</o:p></span></p>
# <p align="justify" class="MsoNormal" style="TEXT-ALIGN: justify; TEXT-JUSTIFY: inter-ideograph; LINE-HEIGHT: 23pt; TEXT-AUTOSPACE: ideograph-numeric; MARGIN-RIGHT: 0pt; mso-pagination: none; mso-line-height-rule: exactly; mso-para-margin-right: 0.0000gd"><span style="FONT-SIZE: 12pt; FONT-FAMILY: 宋体; COLOR: rgb(51,51,51); mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"><o:p>&amp;nbsp;</o:p></span></p>
# <p align="justify" class="MsoNormal" style="TEXT-ALIGN: justify; MARGIN-LEFT: 0pt; TEXT-JUSTIFY: inter-ideograph; LINE-HEIGHT: 23pt; TEXT-AUTOSPACE: ideograph-numeric; MARGIN-RIGHT: 0pt; TEXT-INDENT: 24pt; mso-pagination: none; mso-line-height-rule: exactly; mso-char-indent-count: 2.0000; mso-para-margin-right: 0.0000gd; mso-para-margin-left: 0.0000gd"><span style="FONT-SIZE: 12pt; FONT-FAMILY: 宋体; COLOR: rgb(51,51,51); mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"><o:p>&amp;nbsp;</o:p></span></p>
# <p align="right" class="MsoNormal" style="TEXT-ALIGN: right; MARGIN-LEFT: 0pt; LINE-HEIGHT: 23pt; TEXT-AUTOSPACE: ideograph-numeric; MARGIN-RIGHT: 0pt; TEXT-INDENT: 24pt; mso-pagination: none; mso-line-height-rule: exactly; mso-char-indent-count: 2.0000; mso-para-margin-right: 0.0000gd; mso-para-margin-left: 0.0000gd"><span style="FONT-SIZE: 12pt; FONT-FAMILY: 宋体; COLOR: rgb(51,51,51); mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"><font face="宋体">安庆市公共资源交易中心</font></span><span style="FONT-SIZE: 12pt; FONT-FAMILY: 宋体; COLOR: rgb(51,51,51); mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"><o:p></o:p></span></p>
# <p align="center" class="MsoNormal" style="TEXT-ALIGN: center; MARGIN-LEFT: 0pt; LINE-HEIGHT: 23pt; TEXT-AUTOSPACE: ideograph-numeric; MARGIN-RIGHT: 0pt; TEXT-INDENT: 24pt; mso-pagination: none; mso-line-height-rule: exactly; mso-char-indent-count: 2.0000; mso-para-margin-right: 0.0000gd; mso-para-margin-left: 0.0000gd"><span style="FONT-SIZE: 12pt; FONT-FAMILY: 宋体; COLOR: rgb(51,51,51); mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt">&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp; &amp;nbsp;&amp;nbsp;&amp;nbsp;2018年5月21日</span><span style="FONT-SIZE: 12pt; FONT-FAMILY: 宋体; COLOR: rgb(51,51,51); mso-spacerun: 'yes'; mso-font-kerning: 0.0000pt"><o:p></o:p></span></p>
# <p></p>
# <div class="file">
# <ul>
# </ul>
# <!--添加审核意见-->
# <div id="a">
# <div class="related" id="related">
# </div>
# </div>
# <!--被退回的显示审核意见-->
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
        bt = time.time()
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













