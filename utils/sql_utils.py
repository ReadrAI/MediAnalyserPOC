"""
Util functions for postgres connections and sql
"""

import os
import logging
import tldextract
import threading
import datetime
from os.path import expanduser
import psycopg2
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from urllib.parse import urlparse

from utils import models


class Host:
    class G_CLOUD_SSL:
        name = "gcloud_ssl"
        username = "postgres"  # "worker"
        password = "H1Jos0fOziriMHxL"  # "letravailleurabondos"
        host = "35.195.3.218"
        port = "5432"
        database = "media"

        @classmethod
        def createEngine(cls, connect_args):
            homeDir = expanduser("~")
            connect_args["sslmode"] = "require"
            connect_args["sslcert"] = homeDir + os.sep + ".postgresql/postgresql.crt"
            connect_args["sslkey"] = homeDir + os.sep + ".postgresql/postgresql.key"
            connect_args["sslrootcert"] = homeDir + os.sep + ".postgresql/root.crt"
            return sqlalchemy.create_engine(getDBURLFromHost(cls), connect_args=connect_args)

    class LOCAL_JEAN:
        name = "jean_localhost"
        username = "jean"
        password = ""
        host = "127.0.0.1"
        port = "5432"
        database = "media"

        @classmethod
        def createEngine(cls, connect_args):
            return sqlalchemy.create_engine(getDBURLFromHost(cls), connect_args=connect_args)


def getHost():
    host_var = os.getenv('NHHOST')
    if host_var == 'LOCAL_JEAN':
        return Host.LOCAL_JEAN
    elif host_var == 'G_CLOUD_SSL':
        return Host.G_CLOUD_SSL
    elif host_var == '':
        raise ValueError('Host variable \'NHHOST\' not set.')
    else:
        raise ValueError('Host variable \'NHHOST\' must be one of the following: [\'LOCAL_JEAN\', \'G_CLOUD_SSL\']')


def getDBUrl(username, password, database, host, port, params={}):
    return 'postgres://' + username + ':' + password + '@' + host + ':' + str(port) + '/' + database


def getDBURLFromHost(host):
    username = host.username
    password = host.password
    host_address = host.host
    port = host.port
    database = host.database
    return getDBUrl(username, password, database, host_address, port)


# This function should not be called outside of sql_utils.
def getEngine(connect_args={}, host=getHost(), schema=models.schema):
    global engines
    try:
        engines
    except (NameError, UnboundLocalError):
        engines = {}
    thread_id = threading.get_ident()
    if thread_id not in engines:
        engines[thread_id] = {}
    if host.name not in engines[thread_id]:
        engines[thread_id][host.name] = {}
    if schema not in engines[thread_id][host.name]:
        if schema is not None:
            if 'options' not in connect_args:
                connect_args['options'] = ''
            connect_args['options'] = connect_args['options'] + '-csearch_path=' + schema
        engines[thread_id][host.name][schema] = host.createEngine(connect_args)
    return engines[thread_id][host.name][schema]


# This function should not be called outside of sql_utils.
def getDBSession(host, schema=models.schema):
    global sessions
    try:
        sessions
    except (NameError, UnboundLocalError):
        sessions = {}
    thread_id = threading.get_ident()
    if thread_id not in sessions:
        sessions[thread_id] = {}
    if schema not in sessions[thread_id]:
        Session = sessionmaker(bind=getEngine(host=host, schema=schema))
        sessions[thread_id][schema] = Session()
    try:
        sessions[thread_id][schema].commit()
    except Exception as e:
        sessions[thread_id][schema].rollback()
        logging.error('Rolled back session (%s, %s)' % (host.host, schema))
        logging.error(e)
    return sessions[thread_id][schema]


def dropAllTables(host, schema=models.schema):
    if False:
        meta = sqlalchemy.MetaData(getEngine(host=host, schema=schema))
        meta.reflect()
        meta.drop_all()
    else:
        raise NotImplementedError


def getArticle(url, host, schema=models.schema):
    return getDBSession(host=host, schema=schema).query(models.Article)\
        .filter(models.Article.article_url == url).first()


def getSource(name, host, schema=models.schema):
    sources = getDBSession(host=host, schema=schema).query(
        models.Source).filter(models.Source.source_name == name).all()
    if len(sources) > 1:
        logging.warning("Warning: multiple sources matching name " + name)
        logging.warning("Possible matches " + [x['source_name'] for x in sources])
    elif len(sources) == 0:
        return None
    return sources[0]


def getSourceFromUrl(url, host, schema=models.schema):
    domain = tldextract.extract(url).domain
    sources = getDBSession(host=host, schema=schema).query(models.Source)\
        .filter(sqlalchemy.func.lower(models.Source.website_url).contains(domain)).all()
    for source_i in sources:
        if tldextract.extract(source_i.website_url).domain == domain:
            return source_i
    logging.error("No source found for article " + str(url))
    return None


def getSearch(gmail_request_uuid, host, schema=models.schema):
    return getDBSession(host=host, schema=schema).query(models.ArticleSearch)\
        .filter(models.ArticleSearch.gmail_request_uuid == gmail_request_uuid).first()


def getSourceID(name, host, schema=models.schema):
    source = getSource(name, host=host, schema=schema)
    if source is None:
        return None
    else:
        return str(source.source_uuid)


def getOrSetSourceID(name, url, host, schema=models.schema):
    source_uuid = getSourceID(name, host=host, schema=schema)
    if source_uuid is None:
        url_stem = urlparse(url).netloc
        if url_stem != '':
            url_stem = url_stem("feeds.", "")
            insertEntry(models.Source(
                source_name=name,
                website_url=url_stem,
            ), host=host, schema=schema)
            source_uuid = getSourceID(name, host=host, schema=schema)
        else:
            logging.error("Could not add source %s with url %s: stem is %s." % (name, url, url_stem))
    return source_uuid


def getCustomer(email, host, schema=models.schema):
    return getDBSession(host=host, schema=schema).query(models.Customer)\
        .filter(models.Customer.customer_email == email).first()


def getCustomerID(email, host, schema=models.schema):
    customer_uuid = getDBSession(host=host, schema=schema).query(models.Customer.customer_uuid)\
        .filter(models.Customer.customer_email == email).first()
    if customer_uuid is None:
        return None
    else:
        return str(customer_uuid[0])


def getOrSetCustomerID(email, host, schema=models.schema):
    customer_uuid = getCustomerID(email, host=host, schema=schema)
    if customer_uuid is None:
        insertEntry(models.Customer(
            customer_email=email
        ), host=host, schema=schema)
        customer_uuid = getCustomerID(email, host=host, schema=schema)
    return customer_uuid


def isCustomerBlocked(email, host, schema=models.schema):
    is_blocked = getDBSession(host=host, schema=schema).query(models.Customer.is_blocked)\
        .filter(models.Customer.customer_email == email).first()
    if is_blocked is None:
        return False
    else:
        return is_blocked[0]


def blockCustomer(email, host, schema=models.schema):
    customer = getCustomer(email, host=host, schema=schema)
    if customer is not None:
        customer.is_blocked = True
        try:
            commitSession(host=host, schema=schema)
            return True
        except Exception:
            rollbackSession(host=host, schema=schema)
            return False
    return False


def getArticleSearchesForCustomer(email, host, schema=models.schema):
    return getDBSession(host=host, schema=schema).query(models.ArticleSearch).join(
            models.Customer, models.Customer.customer_uuid == models.ArticleSearch.customer_uuid
        ).filter(models.Customer.customer_email == email).all()


def getSearchMailIDs(host, schema=models.schema):
    return [r[0] for r in getDBSession(host=host, schema=schema).query(models.ArticleSearch.gmail_request_uuid).all()]


def getInvalidEmailIDs(host, schema=models.schema):
    return [i[0] for i in getDBSession(host=host, schema=schema).query(models.InvalidEmail.gmail_request_uuid).all()]


def getRawArticlesQuery(n_days=None, host=getHost(), schema=models.schema):
    query = getDBSession(host=host, schema=schema).query(
        models.Article.article_uuid, models.Article.title,
        models.Article.description, models.ArticleContent.article_content
    ).filter(
        models.Article.description.isnot(None)
    ).outerjoin(
        models.ArticleContent, models.ArticleContent.article_uuid == models.Article.article_uuid
    )
    if n_days is not None:
        current_time = datetime.datetime.utcnow()
        start = current_time - datetime.timedelta(days=n_days)
        query = query.filter(models.Article.published_at >= start)
    return query


def insertEntry(entry, host, schema=models.schema):
    session = getDBSession(host=host, schema=schema)
    try:
        session.add(entry)
        session.commit()
        return True
    except (psycopg2.errors.UniqueViolation, sqlalchemy.exc.IntegrityError):
        logging.warning("Entry already exists for " + str(entry))
        session.rollback()
        return False


def populateFeeds(source_name, feed_url, section=None, host=getHost(), schema=models.schema):
    source_uuid = getSourceID(source_name, host=host, schema=schema)
    return insertEntry(models.RSSFeed(
        source_uuid=source_uuid,
        feed_url=feed_url,
        feed_section=section
    ), host, schema=models.schema)


def updateSearchStatus(article_search, status, host, schema=models.schema):
    article_search.status = status
    commitSession(host=host, schema=schema)


def updateSearchAnswer(article_search, gmail_answer_uuid, host, schema=models.schema):
    article_search.gmail_answer_uuid = str(gmail_answer_uuid)
    commitSession(host=host, schema=schema)


def updateSearchArticle(article_search, article_uuid, host, schema=models.schema):
    article_search.search_article = str(article_uuid)
    commitSession(host=host, schema=schema)


def getRSSFeeds(host, schema=models.schema):
    return getDBSession(host=host, schema=schema).query(models.RSSFeed).all()


def getArticleData(article_uuids, host, schema=models.schema):
    return getDBSession(host=host, schema=schema).query(
        models.Article.article_uuid,
        models.Article.title,
        models.Article.description,
        models.Source.source_name,
        models.Article.article_url
    ).filter(
        models.Article.article_uuid.in_(article_uuids)
    ).join(
        models.Source, models.Source.source_uuid == models.Article.source_uuid
    )


def rollbackSession(host, schema=models.schema):
    logging.error('Rolled back session (%s, %s)' % (host.host, schema))
    getDBSession(host=host, schema=schema).rollback()


def commitSession(host, schema=models.schema):
    getDBSession(host=host, schema=schema).commit()


def closeSession(host, schema=models.schema):
    getDBSession(host=host, schema=schema).close()


def getUncompletedArticleSearches(host, schema=models.schema):
    return getDBSession(host=host, schema=schema).query(models.ArticleSearch).filter(
        models.ArticleSearch.status == 'FAILURE: Article not found').all()
