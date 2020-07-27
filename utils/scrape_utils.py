"""
Util functions for scraping and html queries
"""

import json
import requests
import pandas as pd

from selenium.webdriver import Chrome

from .NYTParser import NYTParser
from . import sql_utils
from data_model import models


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
    url = source.api_url.replace("API_KEY", source.api_key)
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
        sql_utils.insertEntry(
            models.Source(
                source_name=s['name'],
                country=s['country'],
                website_url=s['url'],
                aliases=[s['id']]
            )
        )
    return sources


def fetchNewsAPI(content_type, url):
    page = 0
    content = []
    while True:
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


def importNYT(data, source_name):
    if data['status'] == 'OK':
        for i in range(data['num_results']):
            article = data['results'][i]
            source_uuid = sql_utils.getSourceID(source_name)
            if source_uuid is None:
                print("Source Not Found:", source_name)
            sql_utils.insertEntry(models.Article(
                article_url=article['url'],
                source_uuid=source_uuid,
                provider_uuid=source_uuid,
                title=article['title'],
                description=article['abstract'],
                authors=article['byline'],
                published_at=article['published_date'],
                updated_at=article['updated_date']
            ))
    else:
        print("Data error:", data['status']
              if 'status' in data.keys() else "JSON Error")


def pipelineNYT(name, loadDisk=False, fetchSource=False):
    source_name = 'New York Times'
    if fetchSource:
        data = getUrlContent(source_name)
        saveData(data, name)
    if loadDisk:
        data = loadData(name)
    importNYT(data, source_name)


def loadData(name):
    with open('../raw_data/%s.txt' % name) as json_file:
        data = json.load(json_file)
    return data


def saveData(data, name):
    with open('../raw_data/%s.txt' % name, 'w') as outfile:
        json.dump(data, outfile)


def importNewsAPIArticles(articles, source_name):
    provider_uuid = str(sql_utils.getSource(source_name).source_uuid)
    missing_sources = []
    for i, a in articles.iterrows():
        source = sql_utils.getSource(a['source']['name'])
        if source is not None:
            source_uuid = str(source.source_uuid)
            sql_utils.insertEntry(models.Article(
                article_url=a['url'],
                source_uuid=source_uuid,
                provider_uuid=provider_uuid,
                title=a['title'],
                description=a['description'],
                published_at=a['publishedAt'],
                authors=[a['author']]
            ))
            if a['content'] is not None:
                article = sql_utils.getDBSession().query(models.Article).filter(
                    models.Article.article_url == a['url']).first()
                if article is not None:
                    sql_utils.insertEntry(models.ArticleContent(
                        article_uuid=str(article.article_uuid),
                        article_content=a['content']
                    ))
        else:
            missing_sources.append(a['source']['name'])
    return missing_sources


def pipelineAPINews(name, loadDisk=False, fetchSource=False):
    source_name = 'NewsAPI'
    file_name = '../raw_data/' + name + '.csv'
    if fetchSource:
        data = fetchNewsAPI(
            content_type="articles",
            url=('http://newsapi.org/v2/top-headlines?'
                 'pageSize=100&'
                 'page={page}&'
                 'language=en&'
                 'country=us&'
                 'apiKey=e30a64cfe1734e6794bdab67106590fa'))
        articles = pd.DataFrame(data)
        articles.to_csv(file_name)
    if loadDisk:
        articles = pd.read_csv(file_name)
    importNewsAPIArticles(articles, source_name)
