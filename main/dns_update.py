import os
import sys
import logging
from xml.etree import ElementTree

sys.path.append("../")

from utils import dns_utils
from utils import mail_utils
from utils.data_manager import DataManager

log_file_name = DataManager.getModulePath() + os.sep + 'main' + os.sep + 'logs' + os.sep \
    + 'email_push_notifications_log.txt'
logging.basicConfig(filename=log_file_name, level=logging.ERROR)

print("==================================")
print("DNS Update Routine Started")
print("Timestamp:", mail_utils.getCurrentTimestamp())

past_ip = dns_utils.getLastIP()
ip = dns_utils.fetchIP()
if past_ip != ip:
    dns_utils.updateIPFile(ip)
    print("External IP: " + ip)
    r = dns_utils.updateRecord(ip)
    errCount = ElementTree.fromstring(r.content).find("ErrCount").text
    if int(errCount) > 0:
        errText = ElementTree.fromstring(r.content).find("Err1").text
        if errText is None:
            errText = "Error text is None"
        mail_utils.sendEmailNotification(errText, ip)
        print("API error\n" + r.content)
    else:
        print("IP address successfully updated: %s" % ip)
        mail_utils.sendEmailNotification("IP address successfully updated", ip)

print("DNS Update Routine Finished\n")
