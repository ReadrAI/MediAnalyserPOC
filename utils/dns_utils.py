import os
from xml.etree import ElementTree

from utils import dns_utils
from utils import mail_utils

past_ip = os.getenv('EXTIP', '')
ip = dns_utils.getIP()
if past_ip != ip:
    os.environ['EXTIP'] = ip
    print("External IP: " + ip)
    r = dns_utils.updateRecord(ip)
    errCount = ElementTree.fromstring(r.content).find("ErrCount").text
    if int(errCount) > 0:
        errText = ElementTree.fromstring(r.content).find("Err1").text
        mail_utils.sendEmailNotification(errText, ip)
        print("API error\n" + r.content)
    else:
        print("Update IP success!")
        mail_utils.sendEmailNotification("Update IP success!", ip)
