"""
USAGE: Just run it with python3.

This script is for reprocessing the windlidar data from hpl to netCDF.
Multicore processing is used for much faster running. (joblib)

Created by: Tobias Machnitzki (tobias.machnitzki@mpimet.mpg.de)
"""


from joblib import delayed,Parallel
from datetime import timedelta
from datetime import datetime as dt
import os
import sys
sys.path.insert(0,"/home/mpim/m300517/MPI/working/BCO")

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def startRepro(datestr):
    os.system("python3 /home/mpim/m300517/MPI/working/BCO/BCO/Quicklooks/RadarLidarVelocities.py %s"%datestr)

if __name__ == "__main__":
    start = dt(2017,12,1)
    end = dt.today()
    dates = [x.strftime("%Y%m%d") for x in daterange(start, end)]

    Parallel(n_jobs=-1,verbose=5)(delayed(startRepro)(date) for date in dates)
