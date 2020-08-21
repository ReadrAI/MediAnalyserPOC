"""
Util functions for scraping and html queries
"""

import os
from os.path import expanduser
import time
import json
import requests
import feedparser
import pandas as pd

from datetime import datetime
from urllib.parse import urlparse

from utils import sql_utils
from utils import models
from utils.verbose import Verbose


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
    homeDir = expanduser("~")
    return homeDir + os.sep + 'MediAnalyserPOC' + os.sep + 'raw_data' + os.sep + source_name.lower().replace(" ", "") \
        + '_' + datetime.now().strftime("%Y%m%d_%H%M") + '_' + topic.lower().replace(" ", "-") + \
        ('' if page is None else ('_%d' % page)) + '.csv'


def importNYT(data, source_name, schema=models.schema, host=sql_utils.Host.G_CLOUD_SSL, verbose=Verbose.ERROR):
    count = 0
    if data['status'] == 'OK' and data['results'] is not None:
        if verbose <= Verbose.WARNING and len(data['results']) != data['num_results']:
            print("Number of results not matching:",
                  len(data['results']), data['num_results'])
        for i in range(len(data['results'])):
            article = data['results'][i]
            source_uuid = sql_utils.getSourceID(source_name, schema=schema, host=host)
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
            ), schema=schema, host=host)
    else:
        if verbose <= Verbose.ERROR:
            print("Data error:", data['status']
                  if 'status' in data.keys() else "JSON Error")
    return count


def getNYTSections(api_key):
    url = "https://api.nytimes.com/svc/news/v3/content/section-list.json?api-key=%s" % api_key
    return requests.get(url=url, params={}).json()


def pipelineNYTHeadlines(loadDisk=False, fetchSource=False, schema=models.schema, host=sql_utils.Host.G_CLOUD_SSL, 
                         verbose=Verbose.ERROR):
    source_name = 'New York Times'
    source = sql_utils.getSource(source_name, schema=schema, host=host)
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
                               fetchSource=fetchSource, schema=schema, host=host, verbose=verbose)
    return count


def pipelineNYTNewsWire(startPage=0, loadDisk=False, fetchSource=False, schema=models.schema, 
                        host=sql_utils.Host.G_CLOUD_SSL, verbose=Verbose.ERROR):
    source_name = 'New York Times'
    source = sql_utils.getSource(source_name, schema=schema, host=host)
    increment = 500  # conditions: 20 <= increment <= 500; increment % 20 == 0
    page = startPage
    file_name = getFileName('newswire', source_name, page)
    url = "https://api.nytimes.com/svc/news/v3/content/all/all.json?limit=%d&offset=%d&api-key=%s" % (
        increment, page * increment, source.api_key)
    return __pipelineNYT(source_name, file_name, url, loadDisk=loadDisk,
                         fetchSource=fetchSource, schema=schema, host=host, verbose=verbose)


def __pipelineNYT(source_name, file_name, url, loadDisk=False, fetchSource=False, schema=models.schema,
                  host=sql_utils.Host.G_CLOUD_SSL, verbose=Verbose.ERROR):
    if fetchSource:
        if verbose <= Verbose.INFO:
            print("Fetching", url)
        # TODO upadate with pyhton lib: https://newsapi.org/docs/client-libraries/python
        r = requests.get(url=url, headers={"Accept": "application/json"})
        data = r.json()
        saveData(data, file_name)
        time.sleep(10)
    if loadDisk:
        data = loadData(file_name)
    return importNYT(data, source_name, schema=schema, host=host, verbose=verbose)


def importNewsAPIArticles(articles, source_name, schema=models.schema, host=sql_utils.Host.G_CLOUD_SSL,
                          verbose=Verbose.ERROR):
    provider_uuid = str(sql_utils.getSource(source_name, schema=schema, host=host).source_uuid)
    count = 0
    for i, a in articles.iterrows():
        source_name = a['source']['name']
        source = sql_utils.getSource(source_name, schema=schema, host=host)
        if source is None:
            source_url = getRootUrl(a['url'])
            sql_utils.insertEntry(models.Source(
                source_name=source_name,
                website_url=source_url
            ), schema=schema, host=host)
            source = sql_utils.getSource(source_name, schema=schema, host=host)
        source_uuid = str(source.source_uuid)
        count += sql_utils.insertEntry(models.Article(
            article_url=a['url'],
            source_uuid=source_uuid,
            provider_uuid=provider_uuid,
            title=a['title'],
            description=a['description'],
            published_at=a['publishedAt'],
            authors=[a['author']]
        ), schema=schema, host=host)
        if a['content'] is not None:
            article = sql_utils.getDBSession(schema=schema, host=host).query(models.Article).filter(
                models.Article.article_url == a['url']).first()
            if article is not None:
                sql_utils.insertEntry(models.ArticleContent(
                    article_uuid=str(article.article_uuid),
                    article_content=a['content']
                ), schema=schema, host=host)
    return count


def importNewsAPISources(schema=models.schema, host=sql_utils.Host.G_CLOUD_SSL, verbose=Verbose.ERROR):
    sources = __fetchNewsAPI(
        content_type="sources",
        url="https://newsapi.org/v2/sources?language=en&apiKey=e30a64cfe1734e6794bdab67106590fa",
        verbose=verbose)
    for s in sources:
        sql_utils.insertEntry(models.Source(
            source_name=s['name'],
            country=s['country'],
            website_url=s['url'],
            aliases=[s['id']]
        ), schema=schema, host=host)
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
            if len(json_response[content_type]) > 0 and json_response[content_type][0] in content:
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


def pipelineNewsAPIHeadline(loadDisk=False, fetchSource=False, schema=models.schema, host=sql_utils.Host.G_CLOUD_SSL,
                            verbose=Verbose.ERROR):
    source_name = 'NewsAPI'
    file_name = getFileName('headlines', source_name)
    url = ('http://newsapi.org/v2/top-headlines?'
           'pageSize=100&'
           'page=%s&'
           'language=en&'
           'country=us&'
           'sortBy=publishedAt&'
           'apiKey=e30a64cfe1734e6794bdab67106590fa')
    return __pipelineNewsAPI(source_name, file_name, url=url, fetchSource=fetchSource, loadDisk=loadDisk,
                             schema=schema, host=host, verbose=verbose)


def pipelineNewsAPITopic(topic, loadDisk=False, fetchSource=False, host=sql_utils.Host.G_CLOUD_SSL,
                         schema=models.schema, verbose=Verbose.ERROR):
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
    return __pipelineNewsAPI(source_name, file_name, url=url, fetchSource=fetchSource, loadDisk=loadDisk,
                             schema=schema, host=host, verbose=verbose)


def pipelineNewsAPIArticle(title, source_name=None, loadDisk=False, fetchSource=False, schema=models.schema,
                           host=sql_utils.Host.G_CLOUD_SSL, verbose=Verbose.ERROR):
    provider_name = 'NewsAPI'
    file_name = getFileName(title, source_name)
    url = ('https://newsapi.org/v2/everything?'
           'q=' + title + '&' +
           ('' if source_name is None else 'source=' + source_name.lower().replace(" ", "-") + '&') +
           'pageSize=100&'
           'page=%s&'
           'language=en&'
           'sortBy=publishedAt&'
           'apiKey=e30a64cfe1734e6794bdab67106590fa')
    return __pipelineNewsAPI(provider_name, file_name, url=url, fetchSource=fetchSource, loadDisk=loadDisk,
                             schema=schema, host=host, verbose=verbose)


def __pipelineNewsAPI(source_name, file_name, url=None, loadDisk=False, fetchSource=False,
                      schema=models.schema, host=sql_utils.Host.G_CLOUD_SSL, verbose=Verbose.ERROR):
    if fetchSource:
        data = __fetchNewsAPI(content_type="articles", url=url, verbose=verbose)
        articles = pd.DataFrame(data)
        articles.to_csv(file_name)
    if loadDisk:
        articles = pd.read_csv(file_name)
    return importNewsAPIArticles(articles, source_name, schema=schema, host=host, verbose=verbose)


def __feedImporter(feed_data, source_uuid, schema=models.schema, host=sql_utils.Host.G_CLOUD_SSL,
                   verbose=Verbose.ERROR):
    if 'entries' not in feed_data:
        raise ValueError("No entries in feed for", source_uuid)
    if 'status' not in feed_data:
        if verbose <= Verbose.DEBUG:
            print("No status in feed for %s" % source_uuid)
        raise ValueError("No status in feed for %s" % source_uuid)
    count = 0
    for a in feed_data['entries']:
        try:
            count += sql_utils.insertEntry(models.Article(
                article_url=a['link'],
                source_uuid=source_uuid,
                provider_uuid=source_uuid,
                title=a['title'],
                description=(a['summary'] if 'summary' in a else ''),
                published_at=(
                    a['published'] if ('published' in a and a['published'] != '' and a['published'] is not None)
                    else datetime.utcnow()),
                authors=([a['author']] if 'author' in a else [''])
            ), schema=schema, host=host)
        except KeyError:
            if verbose <= Verbose.ERROR:
                print("Key Error for source", source_uuid, a.keys(), a['link'])
    return count


def importAllFeeds(schema=models.schema, host=sql_utils.Host.G_CLOUD_SSL, verbose=Verbose.ERROR):
    n_imported = 0
    feeds = sql_utils.getDBSession(schema=schema, host=host).query(models.RSSFeed).all()
    for feed_i in feeds:
        if verbose <= Verbose.DEBUG:
            print("Parsing feed %s" % feed_i.feed_url)
        data = feedparser.parse(feed_i.feed_url)
        try:
            count = __feedImporter(data, feed_i.source_uuid, schema=models.schema, host=host, verbose=verbose)
        except ValueError as ve:
            if verbose <= Verbose.ERROR:
                print(ve)
                print("Feed error at %s" % feed_i.feed_url)
        n_imported += count
    return n_imported


def loadRoutine(schema=models.schema, host=sql_utils.Host.G_CLOUD_SSL, verbose=Verbose.INFO):
    count = 0
    # RSS feeds
    count += importAllFeeds(schema=schema, host=host, verbose=verbose)
    # NYT
    count += pipelineNYTHeadlines(fetchSource=True, schema=schema, host=host, verbose=verbose)
    count += pipelineNYTNewsWire(fetchSource=True, schema=schema, host=host, verbose=verbose)
    # NewsAPI
    count += pipelineNewsAPIHeadline(fetchSource=True, schema=schema, host=host, verbose=verbose)
    for topic in [
            'people', 'fashion', 'politics', 'COVID', 'elections', 'sport', 'news', 'world', 'europe',
            'technology', 'science', 'art', 'business', 'tax', 'jobs', 'trends', 'design']:
        count += pipelineNewsAPITopic(topic=topic, fetchSource=True, schema=schema, host=host, verbose=verbose)
    return count
