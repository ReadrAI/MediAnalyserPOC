"""
Data visualisation
"""

import logging

import numpy as np
import pandas as pd

from utils import models
from utils import sql_utils
from utils.data_manager import DataManager

from utils import sql_utils, models, data_science_utils
from utils.data_manager import DataManager
from utils.data_science_utils import Models

import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.axisartist.axislines import SubplotZero


def plotResults(results, axes):
    if results.index.dtype != 'int64':
        results.reset_index(drop=False, inplace=True)

    results.drop_duplicates(subset=[__getColumnName__(axis) for axis in axes], inplace=True)
    x = list(results[__getColumnName__(axes[0])])
    y = list(results[__getColumnName__(axes[1])])

    fig = plt.figure()
    ax = SubplotZero(fig, 111)
    fig.add_subplot(ax)

    ticklabelpad = mpl.rcParams['xtick.major.pad']

    for direction in ["xzero", "yzero"]:
        ax.axis[direction].set_axisline_style("-|>")
        ax.axis[direction].set_visible(True)

    for direction in ["left", "right", "bottom", "top"]:
        ax.axis[direction].set_visible(False)

    ax.scatter(x, y)
    for i in range(len(x)):
        ax.text(x[i], y[i], i, color="red", fontsize=14)

    ax.tick_params(axis='x', colors='#FFFFFF')
    ax.tick_params(axis='y', colors='#FFFFFF')
    ax.set_xticklabels('')
    ax.set_yticklabels('')

    ax.annotate(axes[0][1], xy=(1, 0.5), xytext=(5, -ticklabelpad), ha='center', va='top',
                xycoords='axes fraction', textcoords='offset points')

    ax.annotate(axes[0][0], xy=(0, 0.5), xytext=(5, -ticklabelpad), ha='center', va='top',
                xycoords='axes fraction', textcoords='offset points')

    ax.annotate(axes[1][1], xy=(0.5, 1), xytext=(5, 3*ticklabelpad), ha='left', va='bottom',
                xycoords='axes fraction', textcoords='offset points')

    ax.annotate(axes[1][0], xy=(0.5, 0), xytext=(0, 0), ha='left', va='top',
                xycoords='axes fraction', textcoords='offset points')

    plt.tight_layout()
    plt.show()


def addAxis(results, elems):
    if results.index.dtype != 'int64':
        results.reset_index(drop=False, inplace=True)

    wv = DataManager.getModel(Models.W2V).wv
    news_vect = DataManager.getModel(Models.NEWS_VECT)
    news_index = DataManager.getModel(Models.NEWS_INDEX)
    column_name = __getColumnName__(elems)
    vec_1 = wv[elems[0]]
    vec_2 = wv[elems[1]]
    base_vec = vec_2 - vec_1
    projected_vecs = [news_vect['title']['news_vector'][news_index.index(i)] for i in results['article_uuid']]
    results[column_name] = [np.dot(vec, base_vec) / np.dot(base_vec, base_vec) for vec in projected_vecs]
    return results


def __getColumnName__(elems):
    return 'projection_factor_' + '_'.join(elems)
