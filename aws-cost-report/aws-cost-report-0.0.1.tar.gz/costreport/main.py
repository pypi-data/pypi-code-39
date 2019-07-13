#!/usr/bin/env python

"""command line tool which will return total cost for the current month's AWS usage."""

import subprocess
import json
import datetime
from dateutil import relativedelta
import locale
import argparse
from argparse import RawTextHelpFormatter as rawtxt

class Bcolors:
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    GREY = '\033[90m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def main():
    """command line tool which will return total cost for the current month's AWS usage."""

    parser = argparse.ArgumentParser(
        description="""command line tool which will return total cost for the current month's AWS usage.
usage:
    $ cost-report
expected output:
    AWS Costs for Current Month (July): """+Bcolors.CYAN+"""$2.18"""+Bcolors.ENDC,
        prog='cost-report',
        formatter_class=rawtxt
    )
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.0.1')
    args = parser.parse_args()

    months = {"01":"January", "02":"February", "03":"March", "04":"April", "05":"May", "06":"June", "07":"July", "08":"August", "09":"September", "10":"October", "11":"November", "12":"December"}
    datem = datetime.datetime.today().strftime("%Y-%m")
    dateparts = datem.split("-")
    year = dateparts[0]
    month = dateparts[1]
    nextdateparts = (datetime.date.today() + datetime.timedelta(1*365/12)).isoformat().split("-")
    nextyear = nextdateparts[0]
    nextmontharr = str(datetime.date.today() + relativedelta.relativedelta(months=1)).split("-")
    nextmonth = nextmontharr[1]
    # aws ce get-cost-and-usage --time-period Start=2017-09-01,End=2017-10-01 --granularity MONTHLY --metrics "BlendedCost" "UnblendedCost" "UsageQuantity"
    cmd = 'aws ce get-cost-and-usage --time-period Start={}-{}-01,End={}-{}-01 --granularity MONTHLY --metrics "BlendedCost"'
    try:
        output = subprocess.check_output(cmd.format(year, month, nextyear, nextmonth), shell=True)
        output = output.decode('utf-8')
        output = json.loads(output)
        amount = output['ResultsByTime'][0]['Total']['BlendedCost']['Amount']
        amount = float(amount)
        locale.setlocale(locale.LC_ALL, 'en_US')
        price = locale.currency( amount, grouping = True )
        print("AWS Costs for Current Month ("+months[month]+"):", Bcolors.CYAN+price+Bcolors.ENDC)
    except:
        print(Bcolors.WARNING+"unable to provide AWS cost and usage."+Bcolors.ENDC)

if __name__ == "__main__":
    main()
