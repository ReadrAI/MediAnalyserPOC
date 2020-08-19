import pytz
import datetime

from utils import sql_utils
from utils import scrape_utils
from utils.verbose import Verbose
from utils import models

host = sql_utils.Host.G_CLOUD_SSL
schema = models.schema
verbose = Verbose.WARNING

print("==================================")
print("Article Fetching Routine Started")
print("Timestamp:", datetime.datetime.now(tz=pytz.timezone('Europe/Brussels')).strftime("%Y.%m.%d %H:%M %Z"))
print("Log level:", verbose)
print("Host:", host.name)
print("Schema:", schema)

count = scrape_utils.loadRoutine(host=host, schema=schema, verbose=verbose)
print("Article count:", count)

print("Article Fetching Routine Finished\n")
