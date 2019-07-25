import xml.etree.ElementTree as ET
import pandas as pd


class ReadXML(object):

    def __init__(self, xml_file):
        self.root = ET.parse(xml_file).getroot()
        self.children = self.root.getchildren()
        self.columns = self.get_all_columns()

    def __call__(self, *args, **kwargs):
        self.df = self.build_df()
        if kwargs['detect'] == True:
            self.type_detector()
        return self

    def get_all_columns(self):
        # TODO: Build functionality with schema file
        cols = []
        for row in self.children:
            for el in row:
                if el.tag not in cols:
                    cols.append(el.tag)
        return cols

    def build_df(self):
        df = pd.DataFrame(columns=self.columns, index=range(len(self.children)))
        ind = 0
        for row in self.children:
            for el in row:
                df.at[ind, el.tag] = el.text
            ind += 1
        return df

    def type_detector(self):
        for col in self.columns:
            try:
                self.df[col] = pd.to_numeric(self.df[col])
            except ValueError:
                print("{0} was considered a string Series by pd.to_numeric".format(col))



