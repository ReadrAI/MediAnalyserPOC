import pytz
import datetime

from utils import sql_utils
from utils import scrape_utils
from utils import models

host = sql_utils.Host.G_CLOUD_SSL
schema = models.schema

log_file_name = DataManager.getModulePath() + os.sep + 'main' + os.sep + 'logs' + os.sep + 'article_fetching_log.txt'
logging.basicConfig(filename=log_file_name, level=logging.INFO)


print("==================================")
print("Article Fetching Routine Started")
print("Timestamp:", datetime.datetime.now(tz=pytz.timezone('Europe/Brussels')).strftime("%Y.%m.%d %H:%M %Z"))
print("Host:", host.name)
print("Schema:", schema)

count = scrape_utils.loadRoutine(host=host, schema=schema)
print("Article count:", count)

print("Article Fetching Routine Finished\n")
