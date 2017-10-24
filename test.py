#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

# example data
x = [0.1]
y = [0.2]

# example variable error bar values
yerr = [[0.05], [0.15]]
xerr = [[0.05], [0.15]]

plt.errorbar(x=x, y=y, xerr=xerr, yerr=yerr)

plt.show()