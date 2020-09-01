import pytz
import datetime
import tzlocal

from utils import mail_utils

print("==================================")
print("Email Push Notification Routine Started")
print("Timestamp:", datetime.datetime.now(tz=pytz.timezone('Europe/Brussels')).strftime("%Y.%m.%d %H:%M %Z"))

watch = mail_utils.setPushNotifications()

base = datetime.datetime(1970, 1, 1, tzinfo=pytz.timezone('Europe/Brussels'))
expiration = base + datetime.timedelta(milliseconds=int(watch['expiration']))
print("Expiration:", expiration.astimezone(tzlocal.get_localzone()).strftime("%Y.%m.%d %H:%M %Z"))
print("Email Push Notification Routine Finished\n")
