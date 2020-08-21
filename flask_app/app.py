import threading
import pytz
import datetime

from flask import Flask

from utils import mail_utils
from utils.verbose import Verbose

app = Flask(__name__)


@app.route("/")
def hello():
    thread = threading.Thread(target=mail_utils.pipelineEmails, args=(Verbose.INFO))
    thread.start()
    now = datetime.datetime.now(tz=pytz.timezone('Europe/Brussels')).strftime("%Y.%m.%d %H:%M %Z")
    print("Email Request: Loading new emails", now)
    return "<h1 style='color:blue'>Hello There!</h1>"
