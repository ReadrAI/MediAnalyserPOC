import io
import functools
import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask import render_template, make_response, request, Blueprint
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from utils import sql_utils


dashboard_app = Blueprint('dashboard', __name__, template_folder='templates')

__dashboard_version__ = 'v0.0.1'


@dashboard_app.route("/dashboard")
def dashboard():
    templateData = {
        'datetime': str(datetime.now()),
        'host': sql_utils.getHost().name,
        'version': __dashboard_version__,
        'time': ''
    }
    return render_template('index.html', **templateData)


# @dashboard.route('/dashboard', methods=['POST'])
# def dashboard_post():
#     global numSamples
#     numSamples = int(request.form['numSamples'])
#     numMaxSamples = maxRowsTable()
#     if (numSamples > numMaxSamples):
#         numSamples = (numMaxSamples-1)
#     time, temp, hum = getLastData()
#     templateData = {
#         'time': time,
#         'temp': temp,
#         'hum': hum,
#         'numSamples': numSamples
#     }
#     return render_template('index.html', **templateData)


@dashboard_app.route('/plot/article-search-occurence')
def plot_search_occurence():
    fig = Figure(tight_layout=True)
    axis = fig.add_subplot(1, 1, 1)
    asd = sql_utils.getArticleSearchDates(sql_utils.getHost())
    distinct_dates = list(set(functools.reduce(lambda a, b: a + b[1], asd, [])))
    distinct_dates.sort()
    max_y = 0
    for i in range(len(asd)):
        elems = np.array([asd[i][1].count(d) for d in distinct_dates])
        label = asd[i][0] if asd[i][0] != '' else 'FAILURE: Pipeline error'
        axis.plot(distinct_dates, elems, label=label)
        max_y = max(max_y, max(elems))
    tick_dates = pd.date_range(
        str(distinct_dates[0]),
        str(distinct_dates[-1] - pd.offsets.MonthBegin(1) + relativedelta(months=1)), freq='1M'
    ) - pd.offsets.MonthBegin(1)
    axis.set_xticks(tick_dates)
    axis.set_xticklabels(tick_dates, rotation=75, ha='center')
    axis.set_yticks(range(0, max_y + 1, 5))
    axis.set_title('Article Search Occurences')
    axis.legend()
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output, )
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response


@dashboard_app.route('/plot/rss-feed-availability')
def plot_rss_feed_availability():
    sourceRssShare = sql_utils.getSourceRssShare(host=sql_utils.getHost())
    searchSourceRssShare = sql_utils.getSearchSourceRssShare(host=sql_utils.getHost())

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
    # axis.plot(xs, ys)

    axis.bar(r, greenBars, color='#b5ffb9', edgecolor='white', width=barWidth, label="available")
    axis.bar(r, orangeBars, bottom=greenBars, color='#f9bc86', edgecolor='white', width=barWidth, label="missing")
    axis.set_xticks(r, names)
    axis.legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=1)

    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response
