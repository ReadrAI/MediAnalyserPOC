"""
Util functions for scraping and html queries
"""

import json
import requests

from selenium.webdriver import Chrome

from .NYTParser import NYTParser
from . import sql_utils


"""
Scraping
"""


webdriver_path = './scrape_drivers/chromedriver_v84'


def getDriver():
    global driver
    try:
        driver
    except (NameError, UnboundLocalError):
        driver = Chrome(webdriver_path)
        driver.get("https://www.google.com/")
    return driver


def fetchPage(driver, url):
    driver.get(url)
    html_page = driver.page_source
    return html_page


def getUrlContent(source_name, params={}):
    source = sql_utils.getSource(source_name)
    url = source['api_url'].replace("API_KEY", source['api_key'])
    r = requests.get(url=url, params={})
    return r.json()


"""
Fetching APIs
"""


def getNYTArticleContent(url):
    html_content = fetchPage(driver, url)
    parser = NYTParser()
    parser.feed(html_content)
    return parser.getText()


def importNewsAPISources():
    sources = fetchNewsAPI(
        content_type="sources",
        url="https://newsapi.org/v2/sources?language=en&apiKey=e30a64cfe1734e6794bdab67106590fa")
    for s in sources:
        sql_utils.insertSource(s['name'], {
            'country': s['country'],
            'website_url': s['url'],
            'aliases': '{' + sql_utils.array_for_sql([s['id']]) + '}'})
    return sources


def fetchNewsAPI(content_type, url):
    page = 0
    content = []
    while True:
        print(url)
        response = requests.get(url)
        json_response = response.json()
        if json_response['status'] == 'ok':
            content.extend(json_response[content_type])
            if 'totalResults' in json_response:
                if len(content) == json_response['totalResults']:
                    break
                elif len(content) > json_response['totalResults']:
                    raise ValueError("More %s (%d) than possible to fetch (%d)" % (
                        content_type,
                        len(content),
                        json_response['totalResults']))
                    break
                page += 1
            else:
                break
        else:
            print("Query status not ok")
            for k, v in json_response.items():
                print(k, v)
            break
    return content


def importNYT(data):
    source_name = "NYTimes"
    if data['status'] == 'OK':
        for i in range(data['num_results']):
            article = data['results'][i]
            source_uuid = sql_utils.getSourceID(source_name)
            if source_uuid is None:
                print("Source Not Found:", source_name)
            sql_utils.insertArticle(
                article['url'],
                source_uuid,
                source_uuid,
                article['title'],
                article['abstract'],
                article['byline'],
                article['published_date'],
                article['updated_date'])
    else:
        print("Data error:", data['status']
              if 'status' in data.keys() else "JSON Error")


def pipelineNYT(name, loadDisk=False, fetchSource=False):
    if fetchSource:
        data = getUrlContent('NYTimes')
        saveData(data, name)
    if loadDisk:
        data = loadData(name)
    importNYT(data)


def loadData(name):
    with open('../raw_data/%s.txt' % name) as json_file:
        data = json.load(json_file)
    return data


def saveData(data, name):
    with open('../raw_data/%s.txt' % name, 'w') as outfile:
        json.dump(data, outfile)
