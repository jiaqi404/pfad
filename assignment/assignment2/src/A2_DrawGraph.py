from ObtainData import obtainData
from DrawPlots import drawPlots
import numpy as np

# Run this code to produce a static diagram

# Obtain Data
tideData = obtainData()[:31*24]
tideArr = np.array(tideData).reshape(31,24)

# Draw Plots
drawPlots(
    dataArr=tideArr,
    xNum=24,
    interpolationP=200,   # use linear interpolation to smooth plot
    plotsNum=31,   # draw plots of the whole January
    plotTile="24hrs Tide Height of Januaray",
    plotXLabel="time",
    plotYLabel="Tide Height"
).show()