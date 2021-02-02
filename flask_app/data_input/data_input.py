from flask import render_template, request, Blueprint

from utils import sql_utils
from utils import models

data_input_app = Blueprint('data_input', __name__, template_folder='templates')


@data_input_app.route("/data-input")
def dashboard():
    return render_template('di_index.html')


@data_input_app.route('/data-input', methods=['POST'])
def dashboard_post():
    try:
        sql_utils.populateFeeds(
            source_name=request.form['sourceName'],
            feed_url=request.form['feedUrl'],
            section=request.form['section'] if request.form['section'] != '' else None,
            host=sql_utils.getHost(),
            schema=models.schema)
    except Exception as e:
        print(e)
    return render_template('di_index.html')
