import os
import pytz
import datetime
import logging

from utils import sql_utils
from utils import scrape_utils
from utils import models
from utils import mail_utils
from utils.data_manager import DataManager

host = sql_utils.Host.G_CLOUD_SSL
schema = models.schema

log_file_name = DataManager.getModulePath() + os.sep + 'main' + os.sep + 'logs' + os.sep + 'article_fetching_log.txt'
logging.basicConfig(filename=log_file_name, level=logging.ERROR)


print("==================================")
print("Article Fetching Routine Started")
print("Timestamp:", datetime.datetime.now(tz=pytz.timezone('Europe/Brussels')).strftime("%Y.%m.%d %H:%M %Z"))
print("Host:", host.name)
print("Schema:", schema)

try:
    count = scrape_utils.loadRoutine(host=host, schema=schema)
except BaseException as e:
    mail_utils.sendEmailNotification('Article Fetching Exception', e)

print("Article count:", count)
print("Article Fetching Routine Finished\n")
