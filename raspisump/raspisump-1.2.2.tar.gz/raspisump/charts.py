"""Make charts using nicer styles"""

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import style
from matplotlib import dates
import time

# from pandas.plotting import register_matplotlib_converters

# register_matplotlib_converters()

df = pd.read_csv("/home/pi/raspi-sump/csv/long.csv")
df.columns = ["time", "reading"]
df["time"] = pd.to_datetime(df["time"], format="%H:%M:%S")

# style.use("seaborn-poster")
style.use("ggplot")
style.use("fivethirtyeight")
# style.use('Solarize_Light2')
#####style.use('seaborn-whitegrid')
# style.use('tableau-colorblind10')
# style.use('dark_background')
# plt.rcParams['lines.linewidth']=3
plt.rcParams["axes.facecolor"] = "ffffff"
plt.rcParams["grid.color"] = "ECE5DE"
# plt.rcParams['gridlines.color']='r'
fig = plt.figure(figsize=(12, 3.5))
ax = fig.add_subplot(111)
fig.set_facecolor("w")
plt.plot_date(df.time, df.reading, ls="solid", linewidth=2, color="#007f7f", fmt="-")
title = "Sump Pit Water Level {}".format(time.strftime("%Y-%m-%d %H:%M"))
title_set = plt.title(title)
title_set.set_y(1.09)

# hfmt = dates.DateFormatter('%H:%M')
hfmt = dates.DateFormatter("%I:%M %p")

plt.ylabel("inches")

plt.xlabel("Time of Day")
ax.xaxis.set_major_formatter(hfmt)
plt.xticks(rotation=30)
plt.savefig("/home/pi/raspi-sump/chart.png")

