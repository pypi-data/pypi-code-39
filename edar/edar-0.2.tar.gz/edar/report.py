from collections import namedtuple
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.core.display import display, HTML
import os
import time
import shutil
import random


class Report:
    def __init__(self, data):
        """
        :param data: path to csv,xlsx or pandas dataframe
        """
        if isinstance(data, pd.DataFrame):
            self.df = data
        elif isinstance(data, str):
            _, file_extension = os.path.splitext(data)
            if file_extension == '.csv':
                self.df = pd.read_csv(data)
            elif file_extension == '.xlsx':
                self.df = pd.read_excel(data)
            else:
                raise FileNotFoundError
        self.write_html_report()
        self.display_html_report()
        self.empty_directory()

    @staticmethod
    def display_html_report():
        """ display the written html in jupyter notebook"""
        display(HTML('report_page.html'))

    @staticmethod
    def empty_directory():
        time.sleep(5)
        shutil.rmtree('hist_images')
        os.mkdir('hist_images')

    def write_html_report(self):
        html_page = self.create_html_layout()
        with open("report_page.html", "w") as html_file:
            html_file.write(html_page)
            html_file.close()

    def create_html_layout(self):
        """ create html page to render out
        :param df: dataframe
        """
        page = """<!DOCTYPE html>
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
          </head>
        </html>
        <head>
        	<meta charset="UTF-8">
        </head>
        <body>
          <div class="container">
          <div class="row">
            <div class="col-sm">
              <h4>eda report: Exploratory data analysis</h4>
            </div>
            <div class="col-sm">
              <h3>Inspecting dataframe of size: {size}
            </div>
            </div>
          </div>
        	<table class="table table-hover" style=".table">
              <thead>
                <tr style="font-size: 15px;">
                  <th width="5%" align="left" scope="col">Variable Name</th>
                  <th width="12%" align="left"  scope="col">Data Type</th>
                  <th width="15%" align="left"  scope="col">Histogram</th>
                  <th width="11%" align="left"  scope="col">Stats</th>
                  <th width="7%" align="left"  scope="col">Missing NA</th>
                  <th width="5%" align="left"  scope="col">Outliers</th>
                </tr>
              </thead>
              <tbody>""".format(size=self.df.size)

        end_page = """  
        </tbody>
        </table>
        </body>
        """
        rows_html = []
        for i, column in enumerate(self.df.columns):
            Summary = ColumnSummary(data=self.df[column])
            datatype = Summary.data_type()
            missing = Summary.missing_values()
            stats = Summary.statistic_summary()
            outliers = Summary.outliers()
            Summary.create_histogram(i)
            html = f"""
            <tr>
              <td style="font-size: 15px;" width="10%" align="left"> {column}</td>
              <td style="font-size: 15px;"width="10%" align="left"> {datatype}</td>
              <td><img class="img-fluid" src="hist_images/histogram{i}.png?{random.randint(0,
                                                                                           2e9)}" style="width:800px"> </td>
              <td style="font-size: 15px;">mean: {stats.mean}<br>
                  mode: {stats.mode}<br><br>
                  min: {stats.min}<br>
                  max: {stats.max}<br><br>
                  lower-bound: {stats.lower}<br>
                  upper-bound: {stats.upper}<b</td>
              <td style="font-size: 15px;">{missing}</td>
              <td style="font-size: 15px;">{outliers}</td>
            </tr>
            """
            rows_html.append(html)

        merged_html = page + "".join(rows_html) + end_page
        return merged_html


class ColumnSummary:
    def __init__(self, data):
        """
        :param data: pandas.Series
        """
        self.data = data

    def statistic_summary(self):
        stats = namedtuple('stats', ['mean', 'mode', 'min', 'max', 'upper', 'lower'])
        if not self.dtype_is_object():
            return stats(round(self.mean(), 2), round(self.mode()[0],2), round(self.min(),2),
                         round(self.max(), 2), round(self.q3(), 2), round(self.q1(), 2))
        else:
            return stats('', self.mode()[0], '', '', '', '')

    def num_of_values(self):
        """ number of unique values"""
        return len(self.data.dropna().unique())

    def missing_values(self):
        """ return number of missing values"""
        missing_values = self.data.isna().sum()
        if missing_values:
            fracture = missing_values / self.data.count()
            return f"N={missing_values},{round(fracture, 2)}%"
        else:
            return "no missing values"

    def dtype_is_object(self):
        if self.data.dtype in ('int64', 'float64', 'int32', 'float32'):
            return False
        else:
            return True

    def data_type(self):
        """:return string of datatype"""
        values = self.num_of_values()
        dtype = str(self.data.dtype)
        if dtype in ('int64', 'float64', 'int32', 'float32'):
            if values == 1:
                return f"{dtype}=single number"
            elif values == 2:
                return f"{dtype}=binary number"
            elif 2 < values <= 10:
                return f"{dtype}=category number"
            else:
                return f"{dtype}=continuous number"
        elif self.data.dtype == 'object':
            if values == 1:
                return "single text"
            elif values == 2:
                return "binary text"
            elif 2 < values <= 10:
                return "category text"
            else:
                return "general text"
        else:
            return str(dtype)

    def create_histogram(self, i):
        """
        create a plot from the data serie
        :param i: iteration for each histogram ot make unique
        """
        # styling
        sns.set(style="whitegrid")
        font = {'weight': 'normal'}
        plt.rc('font', **font)
        plt.rc('axes', labelsize=25)  # fontsize of the x and y labels
        plt.rc('xtick', labelsize=25)  # fontsize of the tick labels
        plt.rc('ytick', labelsize=25)
        fig, ax = plt.subplots(1, 1, figsize=(5, 5), dpi=100)
        try:
            if self.dtype_is_object() or self.num_of_values() <= 15:
                if self.num_of_values() > 15:
                    data = pd.to_numeric(self.data, errors='coerce')
                    plot = sns.distplot(data.dropna())
                else:
                    plot = sns.countplot(self.remove_nan_values())
            else:
                plot = sns.distplot(self.remove_nan_values())
            plot.set(xlabel='', ylabel='')
        except Exception:
            plt.text(0.5, 0.5, f'Unable to plot', ha='center', va='center', transform=ax.transAxes, fontsize=16)
        if not os.path.isdir('hist_images'):
            os.mkdir('hist_images')
        plt.savefig(f'hist_images/histogram{i}.png', bbox_inches='tight')
        plt.close()
        plt.clf()

    def remove_nan_values(self):
        return self.data.dropna().copy()

    def outliers(self):
        """:return number of outliers 1.5x the interquartile range"""
        if not self.dtype_is_object():
            data_clean = self.remove_nan_values()
            q1 = self.q1()
            q3 = self.q3()
            iqr = self.q3() - self.q1()
            cut_off = iqr * 1.5
            lower, upper = q1 - cut_off, q3 + cut_off
            mask = data_clean.between(lower, upper)
            data_between = data_clean[mask]
            outliers = len(data_clean) - len(data_between)
            if outliers == 0:
                return 'no outliers'
            return outliers
        return 'no outliers'

    def mean(self):
        return self.data.mean()

    def mode(self):
        return self.data.mode()

    def min(self):
        return self.data.min()

    def max(self):
        return self.data.max()

    def q1(self):
        return self.data.quantile(q=.25)

    def q3(self):
        return self.data.quantile(q=0.75)
