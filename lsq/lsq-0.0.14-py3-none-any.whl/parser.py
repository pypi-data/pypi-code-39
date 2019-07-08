import argparse
from argparse import RawTextHelpFormatter

parser=argparse.ArgumentParser(
    description='''Hello, Please use this link to get more information about this library. ''',
    epilog="\n\nThats it\n----------\
    		\n\nDeveloped by : anand.sandilya@leadsquared.com\
    		\nGit Repo Link : https://github.com/seanjin17/lsq-python\
    		\n\n-----------", formatter_class=RawTextHelpFormatter)



parser.add_argument('help', help='Library to interact with Leadsquared API!, Find more details about'+
									' Leadsquared API at https://apidocs.leadsquared.com/capture-lead/')
args=parser.parse_args()