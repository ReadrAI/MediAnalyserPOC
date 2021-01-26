import os
import pytz
import datetime
import logging

from utils import sql_utils
from utils import models
from utils import data_science_utils
from utils import mail_utils
from utils.data_manager import DataManager

host = sql_utils.getHost()
schema = models.schema

log_file_name = DataManager.getModulePath() + os.sep + 'main' + os.sep + 'logs' + os.sep + 'ml_model_creation_log.txt'
logging.basicConfig(filename=log_file_name, level=logging.ERROR)

print("==================================")
print("ML Model Creation Routine Started")
print("Timestamp:", datetime.datetime.now(tz=pytz.timezone('Europe/Brussels')).strftime("%Y.%m.%d %H:%M %Z"))
print("Host:", host.name)
print("Schema:", schema)

try:
    article_count, model_dim = data_science_utils.createNlpModels(host=host, schema=schema)
    print("Created model for %d articles and %d dimensions" % (article_count, model_dim))
except BaseException as e:
    mail_utils.sendEmailNotification('ML Model Creation Exception', e)


print("ML Model Creation Routine Finished\n")
