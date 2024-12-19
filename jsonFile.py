import json
import random
import matplotlib.cm as cm
import numpy as np


def load(filename):
    with open(filename, 'r') as f:
        jsonFile = json.load(f)
    return jsonFile


def get_signals(file):
    signals = []
    for key in file:
        signals.append(file[key]['Leads'])
    return signals


def get_DelineationDoc(file):
    delDoc = []
    for key in file:
        delDoc.append(file[key]['Leads']['v1']['DelineationDoc'])
    return delDoc


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def getSignalsAndDelDoc(file, lead, top):
    signals = []
    delDoc = []

    for patient in file:
        signals.append(file[patient]['Leads'][lead]['Signal'])
        points = [
            Point(
                x=file[patient]['Leads'][lead]['DelineationDoc'][top][i][0],
                y=file[patient]['Leads'][lead]['Signal'][file[patient]['Leads'][lead]['DelineationDoc'][top][i][0]]
            )
            for i in range(len(file[patient]['Leads'][lead]['DelineationDoc'][top]))
        ]
        delDoc.append(points)

    return signals, delDoc


def draw_signal(signal, ax):
    ax.plot(signal)
    ax.grid(True)
    ax.legend()


def draw_point(x, y, ax):
    cmap = cm.get_cmap('jet')
    color = cmap(random.random())
    ax.plot(x, y, marker='o', linestyle='', color=color)


def drawRtop(R_top, ax):
    cmap = cm.get_cmap('jet')
    color = cmap(random.random())
    for r in R_top:
        ax.plot(r.x, r.y, marker='o', linestyle='', color='red')


def drawXtop(R_top, ax):
    cmap = cm.get_cmap('jet')
    color = cmap(random.random())
    for r in R_top:
        ax.axvline(r.x, color='red', alpha=0.5)
        # ax.plot(r.x, 1, marker='o', linestyle='', color=color)


def draw_DelineationDoc(signal, delDoc, ax):
    cmap = cm.get_cmap('jet')
    for key in delDoc:
        draw_x = []
        draw_y = []
        for j in range(len(delDoc[key])):
            for x in range(len(delDoc[key][j]) - 1):
                draw_x.append(delDoc[key][j][x])
                draw_y.append(signal[delDoc[key][j][x]])
        color = cmap(random.random())
        ax.plot(draw_x, draw_y, marker='o', linestyle='', color=color, label=key)
