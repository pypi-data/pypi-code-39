import glob
import os
import shutil
from football_tools.storage import StorageRepository
from football_tools.statistics import Statistics
from time import time
from bs4 import BeautifulSoup
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import pickle
import click
import shutil

def get_files(url, ext='csv'):
        try:
            page = requests.get(url).text
            soup = BeautifulSoup(page, 'html.parser')
            return ["/".join(url.split('/')[:3]) + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]
        except:
            return "Invalid Url."

def decode_files(files):
    files_output = []

    for rfile in files:
        with open(rfile, 'r') as file:
            files_output.append(file.readlines())
    return StorageRepository(files_output)

def get_map():
    try:
        with open('.map', 'rb') as file:
            files = pickle.load(file)
        return decode_files(files)
    except TypeError:
        memory_files = glob.glob("data/*.csv")
        if len(memory_files) != 0:
            return StorageRepository(decode_files(memory_files))
        else:
            raise RuntimeError('Unable to find memory files.')

def update_source(new_files):
    try:
        shutil.rmtree('data')
        os.mkdir('data')
    except:
        os.mkdir('data')
    for file in new_files:
            print(file)
            write_csv_file(file)

def write_csv_file(file_url):
    try:
        response = requests.get(file_url, verify=False, stream=True) 
        year = file_url.split('/')[len(file_url.split('/')) - 2]  
        file_name = 'data/{}'.format(file_url.split('/')[len(file_url.split('/')) - 1].replace('.csv', '-{}.csv'.format(year)))  
        response.raw.decode_content = True

        with open(file_name, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
    except Exception as ex:
        print("Error to write csv file.", ex)

@click.group()
def cli():
    try:
        get_map()
    except:
        pass
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    pass

@cli.command()
def build():
    stats = time()
    map = glob.glob("data/*.csv")
    if len(map) != 0:
        stats = time() - stats
        click.echo(f'Route map built in {stats:.1f}s.')
        with open('.map', 'wb') as file:
                pickle.dump(map, file)
        get_map()
    else:
        return click.echo(f'Unable to find memory files, please use update_storage command.')

@cli.command()
@click.argument('team')
def statistics(team):
    stats = time()
    statistics = Statistics(team)
    stats = time() - stats
    click.echo(f'Get Statistics in {stats:.1f}s.')
    click.echo('\n====================')
    click.echo(f'''{statistics.team_name} STATISTICS:
        Team Name: {statistics.team_name}.
        Total Matches: {statistics.total_matches}.
        Total Matches Winner: {statistics.total_matches_winner}.
        Total Matches Draw: {statistics.total_matches_draw}.
        Total Matches Losed: {statistics.total_matches_lose}.
        Percentage Of Total Matches Winner: {statistics.percentage_of_matches_winner:.2f} %.
        Percentage Of Total Matches Draw: {statistics.percentage_of_matches_draw:.2f} %.
        Percentage Of Total Matches Losed: {statistics.percentage_of_matches_lose:.2f} %.''')

@cli.command()
def storage():
        map = get_map()
        click.echo(map.storage)

@cli.command()
@click.argument('country')
@click.option('--url', default="https://www.football-data.co.uk")
def update(url, country):    
        if country.lower() == 'portugal':
            url += "/portugalm.php"
        stats = time()
        update_source(get_files(url))
        stats = time() - stats
        click.echo(f'Updated in {stats:.1f}s, please make build command.')
        

if __name__ == '__main__':
    cli()
