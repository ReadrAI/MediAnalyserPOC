import os
import requests
import certifi
import pandas as pd

from datetime import datetime

HOSTNAME = ".newshorizon.xyz"   # Namecheap hostname (including subdomain)
APIKEY = "5f8193ee673742b3a46ea225e7f5db25"  # Namecheap DDNS Token (Accounts > Domain List > Advanced DNS)
FILE_PATH = os.getenv('REPOPATH', '.') + os.sep + 'ip_addresses.csv'


def fetchIP():
    r = requests.get("https://ifconfig.co/json", verify=certifi.where()).json()
    return r['ip']


def updateRecord(ip):
    global HOSTNAME
    global APIKEY
    d = HOSTNAME.find('.')
    host = HOSTNAME[:d]
    domain = HOSTNAME[(d+1):]
    # DO NOT change the url "dynamicdns.park-your-domain.com". It's vaild domain provide by namecheap.
    url = "https://dynamicdns.park-your-domain.com/update?host=" + host + "&domain=" + \
        domain + "&password=" + APIKEY + "&ip=" + ip
    return requests.get(url, verify=certifi.where())


def getLastIP():
    if os.path.isfile(FILE_PATH):
        past_addr = pd.read_csv(FILE_PATH)
        return past_addr.sort_values(by='timestamp', ascending=False).iloc[0]['ip address']


def updateIPFile(ip):
    if os.path.isfile(FILE_PATH):
        past_addr = pd.read_csv(FILE_PATH)
    else:
        past_addr = pd.DataFrame(columns=['timestamp', 'ip address'])
    past_addr = past_addr.append({'timestamp': str(datetime.now()), 'ip address': ip}, ignore_index=True)
    past_addr.to_csv(FILE_PATH, index=False)
