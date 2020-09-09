import os
import pytz
import datetime
import logging

from utils import sql_utils
from utils import models
from utils import data_science_utils
from utils.data_manager import DataManager

host = sql_utils.Host.G_CLOUD_SSL
schema = models.schema

log_file_name = DataManager.getModulePath() + os.sep + 'main' + os.sep + 'logs' + os.sep + 'ml_model_creation_log.txt'
logging.basicConfig(filename=log_file_name, level=logging.WARNING)

print("==================================")
print("ML Model Creation Routine Started")
print("Timestamp:", datetime.datetime.now(tz=pytz.timezone('Europe/Brussels')).strftime("%Y.%m.%d %H:%M %Z"))
print("Host:", host.name)
print("Schema:", schema)

data_science_utils.createNlpModels(schema=schema, host=host)

print("ML Model Creation Routine Finished\n")
