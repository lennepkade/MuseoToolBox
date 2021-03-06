# -*- coding: utf-8 -*-
"""
Compute Moran's I with different lags from raster
===============================================================

Compute Moran's I with different lags, support mask.

"""

##############################################################################
# Import librairies
# -------------------------------------------
import numpy as np
from museotoolbox import raster_tools
from museotoolbox.datasets import historicalMap

##############################################################################
# Load HistoricalMap dataset
# -------------------------------------------

raster,vector = historicalMap()

##############################################################################
# Default, invert is False, it means only polygons will be kept (the rest is set to nodata)
mask = '/tmp/mask.tif'
raster_tools.rasterMaskFromVector(vector,raster,mask,invert=False)

################################
# Compute Moran's I for lag 1
lags = range(1,5)
Is = []
for lag in lags:
    MoransI = raster_tools.Moran(raster,'/tmp/mask.tif',lag=lag)
    Is.append(MoransI.scores['I'])

#######################
# Plot result
# -----------------------------------
from matplotlib import pyplot as plt 
plt.title('Evolution of Moran\'s I')
plt.plot(lags,np.mean(Is,axis=1),'-o')
plt.xlabel('Spatial lag')
plt.xticks(lags)
plt.ylabel('Moran\'s I')