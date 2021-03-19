import os
import pytz
import datetime
import logging

from utils import sql_utils
from utils import scrape_utils
from utils import models
from utils import mail_utils
from utils.data_manager import DataManager

host = sql_utils.getHost()
schema = models.schema

log_file_name = DataManager.getModulePath() + os.sep + 'main' + os.sep + 'logs' + os.sep +\
    'feed_source_fetching_log.txt'
logging.basicConfig(filename=log_file_name, level=logging.ERROR)


print("==================================")
print("Feed Source Fetching Routine Started")
print("Timestamp:", datetime.datetime.now(tz=pytz.timezone('Europe/Brussels')).strftime("%Y.%m.%d %H:%M %Z"))
print("Host:", host.name)
print("Schema:", schema)

try:
    count = scrape_utils.importSourceFeeds(0, host=host, schema=schema)
    print("Feed Source count:", count)
except BaseException as e:
    mail_utils.sendEmailNotification('Feed Source Fetching Exception', e)

print("Feed Source Fetching Routine Finished\n")
