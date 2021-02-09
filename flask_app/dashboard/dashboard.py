import io
import functools
import numpy as np
import pandas as pd
from datetime import datetime
from flask import render_template, make_response, Blueprint
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from utils import models
from utils import sql_utils


dashboard_app = Blueprint('dashboard', __name__, template_folder='templates')

__dashboard_version__ = 'v0.0.2'

# TODO import variables from main file newshorizon.py
host = sql_utils.getHost()
schema = models.schema


@dashboard_app.route("/dashboard")
def dashboard():
    templateData = {
        'datetime': str(datetime.now()),
        'host': sql_utils.getHost().name,
        'version': __dashboard_version__,
        'time': ''
    }
    return render_template('d_index.html', **templateData)


@dashboard_app.route('/plot/article-source-number')
def plot_article_source_number():
    fig = Figure(tight_layout=True)
    left_axis = fig.add_subplot(1, 1, 1)

    sad = sql_utils.getSourceAddDates(host=host, schema=schema)
    aad = sql_utils.getArticleAddDates(host=host, schema=schema)

    sad_dates, sad_count = list(zip(*sad))
    aad_dates, aad_count = list(zip(*aad))
    sad_cum = np.cumsum(sad_count)
    aad_cum = np.cumsum(aad_count)

    left_color = 'tab:red'
    left_axis.set_ylabel(ylabel='Number of Sources', color=left_color)
    left_axis.plot(sad_dates, sad_cum, color=left_color)
    left_axis.tick_params(axis='y', labelcolor=left_color)
    left_axis.tick_params(axis='x', labelrotation=75)

    right_axis = left_axis.twinx()

    right_color = 'tab:blue'
    right_axis.set_ylabel(ylabel='Number of Articles', color=right_color)  # we already handled the x-label with ax1
    right_axis.plot(aad_dates, aad_cum, color=right_color)
    right_axis.tick_params(axis='y', labelcolor=right_color)

    right_axis.set_title('Number of searches and articles')
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response


@dashboard_app.route('/plot/article-search-occurence')
def plot_search_occurence():
    fig = Figure(tight_layout=True)
    axis = fig.add_subplot(1, 1, 1)
    asd = sql_utils.getArticleSearchDates(host=host, schema=schema)
    distinct_dates = list(set(functools.reduce(lambda a, b: a + b[1], asd, [])))
    distinct_dates.sort()
    max_y = 0
    for i in range(len(asd)):
        elems = np.array([asd[i][1].count(d) for d in distinct_dates])
        label = asd[i][0] if asd[i][0] != '' else 'FAILURE: Pipeline error'
        axis.plot(distinct_dates, elems, label=label)
        max_y = max(max_y, max(elems))
    tick_dates = list(pd.date_range(distinct_dates[0], distinct_dates[-1], freq='7D').date) + [distinct_dates[-1]]
    axis.set_xticks(tick_dates)
    axis.set_xticklabels(tick_dates, rotation=75, ha='center')
    axis.set_yticks(range(0, max_y + 1, 5))
    axis.set_title('Article Search Occurences')
    axis.legend()
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response


@dashboard_app.route('/plot/rss-feed-availability')
def plot_rss_feed_availability():
    sourceRssShare = sql_utils.getSourceRssShare(host=host, schema=schema)
    searchSourceRssShare = sql_utils.getSearchSourceRssShare(host=host, schema=schema)

    r = [0, 1]
    raw_data = {
        'greenBars': [sourceRssShare[0], searchSourceRssShare[0]],
        'orangeBars': [sourceRssShare[1] - sourceRssShare[0], searchSourceRssShare[1] - searchSourceRssShare[0]]
    }
    df = pd.DataFrame(raw_data)
    totals = [i+j for i, j in zip(df['greenBars'], df['orangeBars'])]
    greenBars = [100.0 * i / j for i, j in zip(df['greenBars'], totals)]
    orangeBars = [100.0 * i / j for i, j in zip(df['orangeBars'], totals)]
    barWidth = 0.85
    names = ('RSS feed available\nfor existing sources', 'RSS feed available\nfor past searches')

    fig = Figure(tight_layout=True)
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("RSS feed availability")

    ax_green = axis.bar(r, greenBars, color='#b5ffb9', edgecolor='white', width=barWidth, label="available")
    ax_orange = axis.bar(r, orangeBars, bottom=greenBars, color='#f9bc86', edgecolor='white', width=barWidth,
                         label="missing")
    axis.set_xticks(ticks=r)
    axis.set_xticklabels(names)
    axis.legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=1)

    for r1, r2 in zip(ax_green, ax_orange):
        h1 = r1.get_height()
        h2 = r2.get_height()
        axis.text(r1.get_x() + r1.get_width() / 2., h1 / 2., "%d" % h1, ha="center", va="center", color="white",
                  fontsize=16, fontweight="bold")
        axis.text(r2.get_x() + r2.get_width() / 2., h1 + h2 / 2., "%d" % h2, ha="center", va="center", color="white",
                  fontsize=16, fontweight="bold")

    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response
