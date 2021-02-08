"""
Util functions for scraping and html queries
"""

import os
import time
import json
import logging
import sqlalchemy
import psycopg2
import requests
import feedparser
import pandas as pd

from bs4 import BeautifulSoup

from datetime import datetime
from urllib.parse import urlparse

import tldextract

from utils import sql_utils
from utils import models
from utils.data_manager import DataManager


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
    tld = tldextract.extract(article_url)
    if tld.ipv4 == '':
        parsed_uri = urlparse(article_url)
        return '{uri.scheme}://{tld.registered_domain}/'.format(uri=parsed_uri, tld=tld)


def getFileName(topic, source_name, page=None):
    homeDir = DataManager.getModulePath()
    return homeDir + os.sep + 'raw_data' + os.sep + source_name.lower().replace(" ", "") \
        + '_' + datetime.now().strftime("%Y%m%d_%H%M") + '_' + topic.lower().replace(" ", "-") + \
        ('' if page is None else ('_%d' % page)) + '.csv'


def downloadPage(url):
    headers = {
        'User-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)'
                       'Chrome/88.0.4324.96 Safari/537.36'),
        'referer': 'https://stackoverflow.com/'}
    return requests.get(url, headers=headers, allow_redirects=True)


def scrapeArticleTitle(page):
    soup = BeautifulSoup(page.text, "html.parser")
    all_h1 = map(lambda x: x.text.replace("\n", ''), soup.find_all('h1'))
    title = list(filter(lambda x: x != '' and len(x.split(' ')) > 2, all_h1))
    if len(title) == 0:
        all_titles = map(lambda x: x.text.replace("\n", ''), soup.find_all('title'))
        title = list(filter(lambda x: x != '' and len(x.split(' ')) > 2, all_titles))
        if len(title) == 0:
            return None
    return title[0]


def importNYT(data, source_name, host, schema=models.schema):
    count = 0
    if 'status' in data and data['status'] == 'OK' and data['results'] is not None:
        if len(data['results']) != data['num_results']:
            logging.warning("Number of results not matching: " + len(data['results']) + " != " + data['num_results'])
        for i in range(len(data['results'])):
            article = data['results'][i]
            source_uuid = sql_utils.getSourceID(source_name, host=host, schema=schema)
            if source_uuid is None:
                logging.error("Source Not Found: " + source_name)
                return False
            model_article = models.Article(
                article_url=article['url'],
                source_uuid=source_uuid,
                provider_uuid=source_uuid,
                title=article['title'],
                description=article['abstract'],
                authors=[article['byline']],
                published_at=article['published_date'],
                updated_at=article['updated_date']
            )
            try:
                count += sql_utils.insertEntry(model_article, host=host, schema=schema)
            except (sqlalchemy.exc.DataError, psycopg2.errors.DatetimeFieldOverflow):
                sql_utils.rollbackSession(host=host, schema=schema)
                model_article.published_at = datetime.now()
                model_article.updated_at = datetime.now()
                count += sql_utils.insertEntry(model_article, host=host, schema=schema)

    else:
        logging.error("Data error: " + (data['status'] if 'status' in data.keys() else str(data)))
    return count


def getNYTSections(api_key):
    url = "https://api.nytimes.com/svc/news/v3/content/section-list.json?api-key=%s" % api_key
    return requests.get(url=url, params={}).json()


def pipelineNYTHeadlines(loadDisk=False, fetchSource=False, host=None, schema=models.schema):
    source_name = 'New York Times'
    source = sql_utils.getSource(source_name, host=host, schema=schema)
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
                               fetchSource=fetchSource, host=host, schema=schema)
    return count


def pipelineNYTNewsWire(startPage=0, loadDisk=False, fetchSource=False, host=None, schema=models.schema):
    source_name = 'New York Times'
    source = sql_utils.getSource(source_name, host=host, schema=schema)
    increment = 500  # conditions: 20 <= increment <= 500; increment % 20 == 0
    page = startPage
    file_name = getFileName('newswire', source_name, page)
    url = "https://api.nytimes.com/svc/news/v3/content/all/all.json?limit=%d&offset=%d&api-key=%s" % (
        increment, page * increment, source.api_key)
    return __pipelineNYT(source_name, file_name, url, loadDisk=loadDisk,
                         fetchSource=fetchSource, host=host, schema=schema)


def __pipelineNYT(source_name, file_name, url, loadDisk=False, fetchSource=False, host=None, schema=models.schema):
    if fetchSource:
        logging.info("Fetching " + url)
        # TODO upadate with pyhton lib: https://newsapi.org/docs/client-libraries/python
        r = requests.get(url=url, headers={"Accept": "application/json"})
        data = r.json()
        saveData(data, file_name)
        time.sleep(10)
    elif loadDisk:
        data = loadData(file_name)
    else:
        return None
    return importNYT(data, source_name, host=host, schema=schema)


def importNewsAPIArticles(articles, source_name, host, schema=models.schema):
    provider_uuid = str(sql_utils.getSource(source_name, host=host, schema=schema).source_uuid)
    count = 0
    for i, a in articles.iterrows():
        source_name = a['source']['name']
        source = sql_utils.getSource(source_name, host=host, schema=schema)
        if source is None:
            source_url = getRootUrl(a['url'])
            sql_utils.insertEntry(models.Source(
                source_name=source_name,
                website_url=source_url
            ), host=host, schema=schema)
            source = sql_utils.getSource(source_name, host=host, schema=schema)
        source_uuid = str(source.source_uuid)
        count += sql_utils.insertEntry(models.Article(
            article_url=a['url'],
            source_uuid=source_uuid,
            provider_uuid=provider_uuid,
            title=a['title'],
            description=a['description'],
            published_at=a['publishedAt'],
            authors=[a['author']]
        ), host=host, schema=schema)
        if a['content'] is not None:
            article = sql_utils.getArticle(a['url'], host=host, schema=schema)
            if article is not None:
                sql_utils.insertEntry(models.ArticleContent(
                    article_uuid=str(article.article_uuid),
                    article_content=a['content']
                ), host=host, schema=schema)
    return count


def importNewsAPISources(language=None, country=None, host=None, schema=models.schema):
    url = 'https://newsapi.org/v2/sources?' +\
          'page=%d&' +\
          ('' if language is None or type(language) != str else 'language=' + language + '&') +\
          ('' if country is None or type(country) != str else 'country=' + country + '&') +\
          'apiKey=e30a64cfe1734e6794bdab67106590fa'
    sources = __fetchNewsAPI(
        content_type="sources",
        url=url)

    count = 0
    for s in sources:
        source = models.Source(
            source_name=s['name'],
            country=s['country'],
            website_url=s['url'],
            aliases=[s['id']],
            language=s['language']
        )
        result = sql_utils.insertEntry(source, host=host, schema=schema)
        if not result:
            db_source = sql_utils.getSourceFromUrl(s['url'], host=host, schema=schema)
            if db_source is not None:
                db_source.language = s['language']
                sql_utils.commitSession(host=host, schema=schema)
        count += result
    return count


def __fetchNewsAPI(content_type, url):
    page = 1
    content = []
    while True:
        logging.info("Fetching " + (url % page))
        response = requests.get(url % page)
        json_response = response.json()
        if json_response['status'] == 'ok':
            if len(json_response[content_type]) > 0 and json_response[content_type][0] in content:
                logging.error("Loading twice the same content")
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
            logging.warning("Query status not ok")
            for k, v in json_response.items():
                logging.warning(k + ": " + v)
            break
    return content


def pipelineNewsAPIHeadline(loadDisk=False, fetchSource=False, host=None, schema=models.schema):
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
                             host=host, schema=schema)


def pipelineNewsAPITopic(topic, loadDisk=False, fetchSource=False, host=None,
                         schema=models.schema):
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
                             host=host, schema=schema)


def pipelineNewsAPIArticle(title, source_name=None, loadDisk=False, fetchSource=False, host=None, schema=models.schema):
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
                             host=host, schema=schema, )


def __pipelineNewsAPI(source_name, file_name, url=None, loadDisk=False, fetchSource=False,
                      host=None, schema=models.schema):
    if fetchSource:
        data = __fetchNewsAPI(content_type="articles", url=url)
        articles = pd.DataFrame(data)
        articles.to_csv(file_name)
    elif loadDisk:
        articles = pd.read_csv(file_name)
    else:
        return None
    return importNewsAPIArticles(articles, source_name, host=host, schema=schema)


def __feedImporter(feed_data, feed, host, schema=models.schema):
    if 'entries' not in feed_data:
        raise ValueError("No entries in feed for", feed.feed_url)
    if 'status' not in feed_data:
        logging.info("No status in feed for %s:%s" % (feed.source.source_name, feed.feed_url))
        return 0
        # raise ValueError("No status in feed for %s:%s" % (feed.source.source_name, feed.feed_url))
    count = 0
    for a in feed_data['entries']:
        try:
            count += sql_utils.insertEntry(models.Article(
                article_url=a['link'],
                source_uuid=str(feed.source_uuid),
                provider_uuid=str(feed.source_uuid),
                rss_uuid=str(feed.feed_uuid),
                title=a['title'],
                description=(a['summary'] if 'summary' in a else ''),
                published_at=(
                    a['published'] if ('published' in a and a['published'] != '' and a['published'] is not None)
                    else datetime.utcnow()),
                authors=([a['author']] if 'author' in a else [''])
            ), host=host, schema=schema)
        except KeyError:
            logging.error("Key Error for source " + feed.feed_url + "; " + a.keys() + "; " + a['link'])
    return count


def importAllFeeds(host, schema=models.schema):
    n_imported = 0
    feeds = sql_utils.getRSSFeeds(host=host, schema=schema)
    for feed_i in feeds:
        logging.info("Parsing feed %s" % feed_i.feed_url)
        data = feedparser.parse(feed_i.feed_url)
        try:
            n_imported += __feedImporter(data, feed_i, host=host, schema=models.schema)
        except ValueError as ve:
            logging.error(ve)
            logging.error("Feed error at %s" % feed_i.feed_url)
    return n_imported


def loadRoutine(host, schema=models.schema):
    count = 0
    # RSS feeds
    count += importAllFeeds(host=host, schema=schema)
    # NYT
    count += pipelineNYTHeadlines(fetchSource=True, host=host, schema=schema)
    count += pipelineNYTNewsWire(fetchSource=True, host=host, schema=schema)
    # NewsAPI
    count += pipelineNewsAPIHeadline(fetchSource=True, host=host, schema=schema)
    for topic in [
            'people', 'fashion', 'politics', 'COVID', 'elections', 'sport', 'news', 'world', 'europe',
            'technology', 'science', 'art', 'business', 'tax', 'jobs', 'trends', 'design']:
        count += pipelineNewsAPITopic(topic=topic, fetchSource=True, host=host, schema=schema)
    return count


def scrapeRssFeed(query, host, schema=models.schema):
    count = 0
    if type(query) == str:
        url = 'http://cloud.feedly.com/v3/search/feeds?n=100&q=' + query
        page = requests.get(url)
        if page.status_code == 200:
            data = json.loads(page.text)
            for feed_search_result in data['results']:
                feed_url = feed_search_result['feedId'][5:]  # remove 'feed/'
                if feed_url.startswith('http'):
                    count += sql_utils.importRSSFeed(feed_url, host=host, schema=schema)
                else:
                    logging.error("Feed url not recognised: " + feed_search_result['feedId'])
        elif page.status_code == 429:
            raise Exception("429: Too many requests")
        else:
            logging.error("page could not be fetched, code " + str(page.status_code) + " for url " + url)
    else:
        logging.error("query must be of type str, not " + type(query))
    return count


def importRssFeedFromCsv(file_path, host, schema=models.schema):
    count = 0
    rssFeeds = pd.read_csv(file_path)
    for i, feed in rssFeeds.iterrows():
        feedDbEntry = sql_utils.importRSSFeed(feed[0], host=host, schema=schema)
        count += 1 if feedDbEntry is not None else 0
    return count


def importSourceFeeds(limit, host, schema=models.schema):
    count = 0
    sources = sql_utils.getMissingRssFeedSources(host=host, schema=schema)
    sources_to_fetch = [x for x in sources if x[1] <= limit]
    for s in sources_to_fetch:
        count += scrapeRssFeed(s.source_name, host=host, schema=schema)
    return count
