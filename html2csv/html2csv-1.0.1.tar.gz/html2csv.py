from bs4 import BeautifulSoup
import csv
from urllib.request import urlopen
from sys import argv
from urllib.parse import urlparse


def _main():
    url = argv[1]
    netloc = urlparse(url).netloc
    html = urlopen(url).read().decode()
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all("table", recursive=True)

    table_count = 0
    for table in tables:
        table_count += 1
        output_rows = []
        for table_row in table.find_all('tr', recursive=True):
            columns = table_row.find_all('td', recursive=True)
            output_row = []
            for column in columns:
                output_row.append(column.text)
            output_rows.append(output_row)

        with open('{} - {}.csv'.format(netloc, table_count), 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(output_rows)

    if table_count == 0:
        print('No tables found on {}.'.format(url))

def main():
    try:
        _main()
    except IndexError:
        print("No URL Given.")
main()
