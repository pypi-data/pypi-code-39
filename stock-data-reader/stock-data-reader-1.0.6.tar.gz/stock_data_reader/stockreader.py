##
# Contains the stock data reader functionality.
#
# @file
# @copyright 2019
#


import requests
import bs4
import time
import sys
import argparse


class StockReader:
    """
        This class is used get the stock price data from finance.yahoo.com

        Attributes:
            company - The company for which we need to get the stock price

        Methods:
            read_data - This method is used to read the stock price from yahoo finance url
    """

    @staticmethod
    def read_data():
        """
        :exception Exception: the exception will print the error and exit
        """
        # create argument parser object
        parser = argparse.ArgumentParser(description="Stock Data Reader")

        parser.add_argument("-q", "--query", type=str, nargs=1,
                            metavar="company", default=None, help="Company")

        # parse the arguments from standard input
        try:
            args = parser.parse_args()
            company_name = args.query[0]
        except Exception:
            print('Please write cmd like this:= stock-data-reader -q tcs')
            sys.exit()

        while True:
            try:
                response = requests.get('https://in.finance.yahoo.com/quote/'
                                        '{}.NS?p={}.NS&.tsrc=fin-srch'.format(company_name, company_name))
                soup = bs4.BeautifulSoup(response.text, "html.parser")

                price = soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text

                time.sleep(2)

                if price:
                    print('The current price is {}'.format(price))

            except Exception:
                print('Not able to read the data for a company specified')
                sys.exit()


if __name__ == "__main__":
    StockReader.read_data()
