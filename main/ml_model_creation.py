import pytz
import datetime

from utils import sql_utils
from utils.verbose import Verbose
from utils import models
from utils import data_science_utils

host = sql_utils.Host.G_CLOUD_SSL
schema = models.schema
verbose = Verbose.WARNING

print("==================================")
print("ML Model Creation Routine Started")
print("Timestamp:", datetime.datetime.now(tz=pytz.timezone('Europe/Brussels')).strftime("%Y.%m.%d %H:%M %Z"))
print("Log level:", verbose)
print("Host:", host.name)
print("Schema:", schema)

data_science_utils.createNlpModels(verbose=verbose, schema=schema, host=host)

print("ML Model Creation Routine Finished\n")
