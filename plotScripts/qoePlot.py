import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import operator
import numpy as np
import sys, json, re

data = np.loadtxt("QoE.txt", dtype=float)

def normalize(arr, t_min, t_max):
    norm_arr = []
    diff = t_max - t_min
    diff_arr = max(arr) - min(arr)    
    for i in arr:
        temp = (((i - min(arr))*diff)/diff_arr) + t_min
        norm_arr.append(temp)
    return norm_arr

data = normalize(data, 0, 1)

fig, ax = plt.subplots()

labels = ["bicycle", "bus", "car", "foot", "train", "fluctuation", "rampDown", "rampUp", "stable"]
ax.bar(labels, data, color="blue")

ax.set_ylabel("QoE")
ax.set_xlabel("Scenario")
ax.set_title("QoE for each scenario")

plt.show()