import os
import pytz
import datetime
import tzlocal
import logging

from utils import mail_utils
from utils.data_manager import DataManager

log_file_name = DataManager.getModulePath() + os.sep + 'main' + os.sep + 'logs' + os.sep \
    + 'email_push_notifications_log.txt'
logging.basicConfig(filename=log_file_name, level=logging.ERROR)

print("==================================")
print("Email Push Notification Routine Started")
print("Timestamp:", mail_utils.getCurrentTimestamp())

try:
    watch = mail_utils.setPushNotifications()
    base = datetime.datetime(1970, 1, 1, tzinfo=pytz.timezone('Europe/Brussels'))
    expiration = base + datetime.timedelta(milliseconds=int(watch['expiration']))
    print("Expiration:", expiration.astimezone(tzlocal.get_localzone()).strftime("%Y.%m.%d %H:%M %Z"))
except BaseException as e:
    mail_utils.sendEmailNotification('Email Push Notification Exception', e)

print("Email Push Notification Routine Finished\n")
