import threading
import pytz
import datetime
import os
import logging
from os import path, walk

from flask import Flask
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy

from flask_app.dashboard import dashboard
from flask_app.data_input import data_input
from utils.data_manager import DataManager
from utils import mail_utils
from utils import models
from utils import sql_utils

host = sql_utils.getHost()

app = Flask(__name__)
app.register_blueprint(dashboard.dashboard_app)
app.register_blueprint(data_input.data_input_app)

app.config['SQLALCHEMY_DATABASE_URI'] = sql_utils.getDBURLFromHost(host)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True

db = SQLAlchemy(app)
db.init_app(app)

log_file_name = DataManager.getModulePath() + os.sep + 'flask_app' + os.sep + 'logs' + os.sep + 'flask_app_log.txt'
logging.basicConfig(filename=log_file_name, level=logging.INFO)


@app.route("/", methods=['GET', 'POST'])
def hello():
    thread = threading.Thread(target=mail_utils.pipelineEmails, args=[host, models.schema])
    thread.start()
    now = datetime.datetime.now(tz=pytz.timezone('Europe/Brussels')).strftime("%Y.%m.%d %H:%M %Z")
    print("Email Request: Loading new emails", now)
    logging.info("Email Request: Loading new emails at " + now)
    return "<h1 style='color:blue'>Hello There!</h1>"


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


def createExtraFileList(extra_dirs=['.']):
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in walk(extra_dir):
            if '__' not in dirname:
                for filename in files:
                    filename = path.join(dirname, filename)
                    if path.isfile(filename):
                        if '__' not in filename:
                            extra_files.append(filename)
    return extra_files


if __name__ == "__main__":
    app.run(extra_files=createExtraFileList(), host='0.0.0.0')  # debug=True, port=5000
