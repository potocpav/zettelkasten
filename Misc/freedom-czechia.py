# %%

import numpy as np
from matplotlib import pyplot as plt

# %% Economist Intelligence Unit - Democracy Index

di_y = [8.17, 8.19, 8.19, 8.19, 8.19, 8.06, 7.94, 7.94, 7.82, 7.62, 7.69, 7.69, 7.67]
di_x = [x for x in range(2006, 2021) if x not in [2007, 2009]]

# %% V-Dem Institute - Electoral Democracy Index

# import csv

# vdi_x, vdi_y = [], []
# for l in csv.reader(open('/home/pavel/Downloads/Czech Republic.csv').readlines()):
#   if l[0] == 'Year':
#     print('Column:', l[10])
#   else:
#     vdi_x.append(int(l[0]))
#     vdi_y.append(float(l[10]))

vdi_x = [1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
vdi_y = [0.896, 0.896, 0.896, 0.895, 0.894, 0.887, 0.881, 0.881, 0.881, 0.889, 0.896, 0.896, 0.896, 0.9, 0.902, 0.902, 0.892, 0.887, 0.894, 0.894, 0.858, 0.852, 0.852, 0.852, 0.846, 0.812, 0.803, 0.805]

# %% Reporters Without Borders

rsf_x = [x for x in range(2006,2022)]
rsf_y = list(reversed([91, 91, 91, 93, 94, 95, 95, 94, 95, 95, 95, 95, 95, 95, 95, 92]))
# Remove 2006 as an outlier?
rsf_x = rsf_x[1:]
rsf_y = rsf_y[1:]
plt.plot(rsf_x, rsf_y)

# %% plot

def norm(l, offset=0):
  ma, mi = max(l), min(l)
  return (np.array(l) - mi) / (ma - mi) + offset

frame = plt.gca()
frame.axes.get_yaxis().set_visible(False)
plt.plot(di_x, norm(di_y), label="Economist Intelligence Unit")
plt.plot(vdi_x, norm(vdi_y, 0), label="V-Dem Institute")
plt.plot(rsf_x, norm(rsf_y, 0), label="Reporters Without Borders")
plt.legend()
plt.savefig('graph.svg')

# %%
