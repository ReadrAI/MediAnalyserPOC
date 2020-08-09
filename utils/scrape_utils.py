"""
Util functions for scraping and html queries
"""

import time
import json
import requests
import feedparser
import pandas as pd

from datetime import datetime
from urllib.parse import urlparse

from selenium.webdriver import Chrome

from .NYTParser import NYTParser
from . import sql_utils
from data_model import models
from utils.verbose import Verbose


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


def __fetchPage(driver, url):
    driver.get(url)
    html_page = driver.page_source
    return html_page


"""
Fetching APIs
"""


def loadData(name):
    with open(name) as json_file:
        data = json.load(json_file)
    return data


def saveData(data, name):
    with open(name, 'w') as outfile:
        json.dump(data, outfile)


def getRootUrl(article_url):
    parsed_uri = urlparse(article_url)
    return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)


def getFileName(topic, source_name, page=None):
    return '../raw_data/' + source_name.lower().replace(" ", "") + '_' + \
        datetime.now().strftime("%Y%m%d_%H%M") + '_' + topic + \
        ('' if page is None else ('_%d' % page)) + '.csv'


def getNYTArticleContent(url):
    html_content = __fetchPage(driver, url)
    parser = NYTParser()
    parser.feed(html_content)
    return parser.getText()


def importNYT(data, source_name, verbose=Verbose.ERROR):
    count = 0
    if data['status'] == 'OK' and data['results'] is not None:
        if verbose <= Verbose.WARNING and len(data['results']) != data['num_results']:
            print("Number of results not matching:",
                  len(data['results']), data['num_results'])
        for i in range(len(data['results'])):
            article = data['results'][i]
            source_uuid = sql_utils.getSourceID(source_name)
            if source_uuid is None:
                if verbose <= Verbose.ERROR:
                    print("Source Not Found:", source_name)
                return False
            count += sql_utils.insertEntry(models.Article(
                article_url=article['url'],
                source_uuid=source_uuid,
                provider_uuid=source_uuid,
                title=article['title'],
                description=article['abstract'],
                authors=[article['byline']],
                published_at=article['published_date'],
                updated_at=article['updated_date']
            ))
    else:
        if verbose <= Verbose.ERROR:
            print("Data error:", data['status']
                  if 'status' in data.keys() else "JSON Error")
    return count


def getNYTSections(api_key):
    url = "https://api.nytimes.com/svc/news/v3/content/section-list.json?api-key=%s" % api_key
    return requests.get(url=url, params={}).json()


def pipelineNYTHeadlines(loadDisk=False, fetchSource=False, verbose=Verbose.ERROR):
    source_name = 'New York Times'
    source = sql_utils.getSource(source_name)
    sections = [
        'arts', 'automobiles', 'books', 'business', 'fashion', 'food', 'health', 'home',
        'insider', 'magazine', 'movies', 'nyregion', 'obituaries', 'opinion', 'politics',
        'realestate', 'science', 'sports', 'sundayreview', 'technology', 'theater', 't-magazine',
        'travel', 'upshot', 'us', 'world']

    count = 0
    for topic in sections:
        url = "https://api.nytimes.com/svc/topstories/v2/%s.json?api-key=%s" % (
            topic, source.api_key)
        # source.api_url.replace("API_KEY", source.api_key)
        file_name = getFileName(topic, source_name)
        count += __pipelineNYT(source_name, file_name, url, loadDisk=loadDisk,
                               fetchSource=fetchSource, verbose=verbose)
    return count


def pipelineNYTNewsWire(startPage=0, loadDisk=False, fetchSource=False, verbose=Verbose.ERROR):
    source_name = 'New York Times'
    source = sql_utils.getSource(source_name)
    increment = 500  # conditions: 20 <= increment <= 500; increment % 20 == 0
    page = startPage
    file_name = getFileName('newswire', source_name, page)
    url = "https://api.nytimes.com/svc/news/v3/content/all/all.json?limit=%d&offset=%d&api-key=%s" % (
        increment, page * increment, source.api_key)
    return __pipelineNYT(source_name, file_name, url, loadDisk=loadDisk,
                         fetchSource=fetchSource, verbose=verbose)


def __pipelineNYT(source_name, file_name, url, loadDisk=False, fetchSource=False, verbose=Verbose.ERROR):
    if fetchSource:
        if verbose <= Verbose.INFO:
            print("Fetching", url)
        r = requests.get(url=url, headers={"Accept": "application/json"})
        data = r.json()
        saveData(data, file_name)
        time.sleep(10)
    if loadDisk:
        data = loadData(file_name)
    return importNYT(data, source_name, verbose=verbose)


def importNewsAPIArticles(articles, source_name, verbose=Verbose.ERROR):
    provider_uuid = str(sql_utils.getSource(source_name).source_uuid)
    count = 0
    for i, a in articles.iterrows():
        source_name = a['source']['name']
        source = sql_utils.getSource(source_name)
        if source is None:
            source_url = getRootUrl(a['url'])
            count += sql_utils.insertEntry(models.Source(
                source_name=source_name,
                website_url=source_url
            ))
            source = sql_utils.getSource(source_name)
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
    return count


def importNewsAPISources(verbose=Verbose.ERROR):
    sources = __fetchNewsAPI(
        content_type="sources",
        url="https://newsapi.org/v2/sources?language=en&apiKey=e30a64cfe1734e6794bdab67106590fa",
        verbose=verbose)
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


def __fetchNewsAPI(content_type, url, verbose=Verbose.ERROR):
    page = 1
    content = []
    while True:
        if verbose <= Verbose.DEBUG:
            print("Fetching", url % page)
        response = requests.get(url % page)
        json_response = response.json()
        if json_response['status'] == 'ok':
            if json_response[content_type][0] in content:
                if verbose <= Verbose.ERROR:
                    print("Loading twice the same content")
                break
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
            if True:
                # NewsAPI Only provides 100 entries in the free version. Subscribe to paid plan for more
                break
        else:
            if verbose <= Verbose.WARNING:
                print("Query status not ok")
                for k, v in json_response.items():
                    print(k, v)
            break
    return content


def pipelineAPINewsHeadline(loadDisk=False, fetchSource=False, verbose=Verbose.ERROR):
    source_name = 'NewsAPI'
    file_name = getFileName('headlines', source_name)
    url = ('http://newsapi.org/v2/top-headlines?'
           'pageSize=100&'
           'page=%s&'
           'language=en&'
           'country=us&'
           'sortBy=publishedAt&'
           'apiKey=e30a64cfe1734e6794bdab67106590fa')
    return __pipelineAPINews(source_name, file_name, url=url, fetchSource=fetchSource, loadDisk=loadDisk,
                             verbose=verbose)


def pipelineAPINewsTopic(topic, loadDisk=False, fetchSource=False, verbose=Verbose.ERROR):
    source_name = 'NewsAPI'
    now = datetime.now()
    file_name = getFileName(topic, source_name)
    url = ('https://newsapi.org/v2/everything?'
           'q=' + topic + '&'
           'from=' + now.strftime("%Y-%m-%d") + '&'
           'to=' + now.strftime("%Y-%m-%d") + '&'
           'pageSize=100&'
           'page=%s&'
           'language=en&'
           'sortBy=publishedAt&'
           'apiKey=e30a64cfe1734e6794bdab67106590fa')
    return __pipelineAPINews(source_name, file_name, url=url, fetchSource=fetchSource, loadDisk=loadDisk,
                             verbose=verbose)


def __pipelineAPINews(source_name, file_name, url=None, loadDisk=False, fetchSource=False, verbose=Verbose.ERROR):
    source_name = 'NewsAPI'
    if fetchSource:
        data = __fetchNewsAPI(
            content_type="articles",
            url=url,
            verbose=verbose)
        articles = pd.DataFrame(data)
        articles.to_csv(file_name)
    if loadDisk:
        articles = pd.read_csv(file_name)
    return importNewsAPIArticles(articles, source_name, verbose=verbose)


def __feedImporter(feed_data, source_uuid):
    if 'entries' not in feed_data:
        raise ValueError("No entries in feed")
    if 'status' not in feed_data:
        raise ValueError("No entries in feed")
    count = 0
    for a in feed_data['entries']:
        count += sql_utils.insertEntry(models.Article(
            article_url=a['link'],
            source_uuid=source_uuid,
            provider_uuid=source_uuid,
            title=a['title'],
            description=a['summary'],
            published_at=a['published'],
            authors=([a['author']] if 'author' in a else [])
         ))
    return count


def importAllFeeds():
    n_imported = 0
    feeds = sql_utils.getDBSession().query(models.RSSFeed).all()
    for feed_i in feeds:
        data = feedparser.parse(feed_i.feed_url)
        count = __feedImporter(data, feed_i.source_uuid)
        n_imported += count
    return n_imported


def loadRoutine(verbose=Verbose.INFO):
    count = 0
    # RSS feeds
    count += importAllFeeds()
    # NYT
    count += pipelineNYTHeadlines(fetchSource=True, verbose=verbose)
    count += pipelineNYTNewsWire(fetchSource=True, verbose=verbose)
    # NewsAPI
    count += pipelineAPINewsHeadline(fetchSource=True, verbose=verbose)
    for topic in [
            'people', 'fashion', 'politics', 'COVID', 'elections', 'sport', 'news', 'war', 'world', 'europe',
            'technology', 'science', 'movie', 'Trump', 'Biden', 'news', 'business', 'trade', 'stock', 'S&P500', 'tax',
            'jobs', 'trends', 'design', 'tv']:
        count += pipelineAPINewsTopic(topic=topic, fetchSource=True, verbose=verbose)
    return count
