import threading
import pytz
import datetime
import os

from flask import Flask
from flask import send_from_directory


from utils import mail_utils
from utils.verbose import Verbose

app = Flask(__name__)


@app.route("/")
def hello():
    thread = threading.Thread(target=mail_utils.pipelineEmails, args=[Verbose.INFO])
    thread.start()
    now = datetime.datetime.now(tz=pytz.timezone('Europe/Brussels')).strftime("%Y.%m.%d %H:%M %Z")
    print("Email Request: Loading new emails", now)
    return "<h1 style='color:blue'>Hello There!</h1>"


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
