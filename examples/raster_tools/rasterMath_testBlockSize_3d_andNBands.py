# -*- coding: utf-8 -*-
"""
Using rasterMath with 3d block or 2d block
==================================================================

Test notebook to validate code.
"""

##############################################################################
# Import librairies
# -------------------------------------------

from museotoolbox.raster_tools import rasterMath,rasterMaskFromVector
from museotoolbox import datasets
from matplotlib import pyplot as plt
import numpy as np

##############################################################################
# Load HistoricalMap dataset
# -------------------------------------------

raster,vector = datasets.historicalMap()

##############################################################################
# Initialize rasterMath with raster
# ------------------------------------

# Set return_3d to True to have full block size (not one pixel per row)
# Create raster mask to only keep pixel inside polygons.

rasterMaskFromVector(vector,raster,'/tmp/mask.tif',invert=False)

for return_3d in [True,False]:
    rM = rasterMath(raster,inMaskRaster='/tmp/mask.tif',return_3d=return_3d)
    
    rM.customBlockSize(128,128) # block of 200x200pixels
    
    print(rM.getRandomBlock().shape)
    
    x = rM.getRandomBlock()
    
    # Returns with only 1 dimension
    returnFlatten = lambda x : x[...,0]
    
    # Returns 3x the original last dimension
    addOneBand = lambda x : np.repeat(x,3,axis=x.ndim-1)
    
    # Add functions to rasterMath
    rM.addFunction(addOneBand,'/tmp/x_repeat_{}.tif'.format(str(return_3d)))
    rM.addFunction(returnFlatten,'/tmp/x_flatten_{}.tif'.format(str(return_3d)))
    
    rM.run()
    
import gdal
dst = gdal.Open('/tmp/x_flatten_False.tif')
arr = dst.GetRasterBand(1).ReadAsArray()
plt.imshow(np.ma.masked_where(arr == np.min(arr), arr))
