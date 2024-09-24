import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from ObtainData import obtainData

# Run this code to produce an animation

# Obtain Data
tideData = obtainData()[:31*24]

# Set up the figure and the axis
fig = plt.figure()
ax = plt.axes(
    xlim=(0, 24), 
    ylim=(0, 3), 
    title="24hrs Tide Height of Januaray", 
    xlabel="time", 
    ylabel="tide height")
plt.grid(True)
line, = ax.plot([], [])

# Set initialization function
def init():
    line.set_data([], [])
    return line,

# Set animation function
def animate(frame):
    x = np.arange(24)
    y = tideData[frame:24+frame]
    line.set_data(x, y)
    return line,

# Call the animator
anim = animation.FuncAnimation(fig, animate, frames=300, init_func=init, interval=50, blit=True)

plt.show()