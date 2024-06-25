import numpy as np, pandas as pd, random, matplotlib.pyplot as plt, seaborn as sns
from IPython.display import clear_output
from PyProbs import Probability as pr
viewer = zeros = [[0] * 7 for _ in range(32)]
for i in range(32):
    for j in range(7):
        if j == 3:
            viewer[i][j] = 0
        else:
            viewer[i][j] = 5
fig, ax = plt.subplots()
im = ax.imshow(viewer, cmap='summer', vmin=0, vmax=10)
# plt.draw()
plt.savefig('empty.pdf')