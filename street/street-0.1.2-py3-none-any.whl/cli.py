#!/usr/bin/env python

import click

from street import get_config, set_config
from street import (
    DistilIdentificationBlocked,
    EarningsTableEmpty,
    EarningsTableNotFound,
    RequestBlocked,
    ResourceMovedTemporarily,
    UnforeseenResponseStatusCode,
)
from street import StreetScraper


@click.group()
def cli():
    pass


@cli.command(
    short_help='Set request headers to bypass bot blocker'
)
@click.option(
    '-u',
    '--user-agent',
    help='User-agent name of your browser',
    prompt=True,
)
@click.option(
    '-c',
    '--cookie',
    help='Cookie generated for your browser',
    prompt=True,
)
def setup(user_agent, cookie):
    set_config(user_agent, cookie)


@cli.command(
    short_help='Get earnings history for ticker symbol'
)
@click.option(
    '-o',
    '--outfile',
    type=click.Path(),
    help='Output CSV file to save earnings history',
)
@click.argument(
    'symbol',
)
def ticker(outfile, symbol):
    try:
        user_agent, cookie = get_config()
        ss = StreetScraper(user_agent, cookie)
        earnings = ss.scrape(symbol)
    except RequestBlocked:
        print('Request blocked! Check user-agent and wait a bit before scraping again.')
    except ResourceMovedTemporarily:
        print('Resource moved temporarily! Wait a bit before scraping again.')
    except UnforeseenResponseStatusCode:
        print('Unforeseen response status code!')
    except DistilIdentificationBlocked:
        print('Distil id blocked! Check cookie or wait a bit before scraping again.')
    except EarningsTableNotFound:
        print('Earnings table not found! Check ticker symbol.')
    except EarningsTableEmpty:
        print('Earnings history not found! Check ticker symbol.')
    else:
        print(earnings)
        if outfile:
            earnings.to_csv(outfile, index=False)


if __name__ == '__main__':
    cli()