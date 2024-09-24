import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline

# Define the function to draw a diagram
def drawPlots(dataArr, xNum, interpolationP, plotsNum, plotTile, plotXLabel, plotYLabel):
    x = np.arange(xNum)
    xnew = np.linspace(x.min(), x.max(), interpolationP)

    fig, ax = plt.subplots()
    for i in range(plotsNum):
        spl = make_interp_spline(x, dataArr[i], k=3)
        ynew = spl(xnew)
        ax.plot(xnew, ynew, color="blue", alpha=(plotsNum-i)/plotsNum)

    ax.set_title(plotTile)
    ax.set_xlabel(plotXLabel)
    ax.set_ylabel(plotYLabel)
    return plt