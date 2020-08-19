import sys
import datetime

sys.path.append("./")

from utils import sql_utils
from utils import scrape_utils
from utils.verbose import Verbose
from utils import models

host = sql_utils.Host.G_CLOUD_SSL
schema = models.schema
verbose = Verbose.WARNING

print("Article Fetching Routine Started")
print("Timestamp:", datetime.datetime.now().strftime("%Y.%m.%d %H:%M"))
print("Log level:", verbose)
print("Host:", host.name)
print("Schema:", schema)

scrape_utils.loadRoutine(host=host, schema=schema, verbose=verbose)
