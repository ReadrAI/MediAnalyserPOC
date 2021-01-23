import requests
import certifi

HOSTNAME = ".newshorizon.xyz"   # Namecheap hostname (including subdomain)
APIKEY = "5f8193ee673742b3a46ea225e7f5db25"  # Namecheap DDNS Token (Accounts > Domain List > Advanced DNS)


def getIP():
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
    print(url)
    return requests.get(url, verify=certifi.where())
