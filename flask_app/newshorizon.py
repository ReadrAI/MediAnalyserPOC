import threading
import pytz
import datetime
import os
import logging

from flask import Flask
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy

from utils.data_manager import DataManager
from utils import mail_utils
from utils import models
from utils import sql_utils

host = sql_utils.getHost()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = sql_utils.getDBURLFromHost(host)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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


if __name__ == "__main__":
    app.run(host='0.0.0.0')
