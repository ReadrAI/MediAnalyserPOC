"""
Util functions for postgres connections and sql
"""

import os
from os.path import expanduser
import psycopg2
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from utils import models
from utils.verbose import Verbose


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

    class G_CLOUD_FUNCTION:
        name = "gcloud_function"
        username = "worker"
        password = "letravailleurabondos"
        host = "35.195.3.218"
        port = "5432"
        database = "media"
        source_path = os.getcwd() + os.sep + "cert" + os.sep
        # connection_name = "future-oasis-286707:europe-west1:media"

        @classmethod
        def createEngine(cls, connect_args):
            print("SSL cert path %s" % (cls.source_path + "postgresql.crt"))
            connect_args["sslmode"] = "require"
            connect_args["sslcert"] = cls.source_path + "postgresql.crt"
            connect_args["sslkey"] = cls.source_path + "postgresql.key"
            connect_args["sslrootcert"] = cls.source_path + "root.crt"
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


def getDBUrl(username, password, database, host, port, params={}):
    return 'postgres://' + username + ':' + password + '@' + host + ':' + str(port) + '/' + database


def getDBURLFromHost(host):
    username = host.username
    password = host.password
    host_address = host.host
    port = host.port
    database = host.database
    return getDBUrl(username, password, database, host_address, port)


def getEngine(host=Host.G_CLOUD_SSL, schema=models.schema, connect_args={}):
    global engines
    try:
        engines
    except (NameError, UnboundLocalError):
        engines = {}
    if host.name not in engines:
        engines[host.name] = {}
    if schema not in engines[host.name]:
        if schema is not None:
            if 'options' not in connect_args:
                connect_args['options'] = ''
            connect_args['options'] = connect_args['options'] + '-csearch_path=' + schema
        engines[host.name][schema] = host.createEngine(connect_args)
    return engines[host.name][schema]


def getDBSession(host=Host.G_CLOUD_SSL, schema=models.schema):
    global sessions
    try:
        sessions
    except (NameError, UnboundLocalError):
        sessions = {}
    if schema not in sessions:
        Session = sessionmaker(bind=getEngine(host=host, schema=schema))
        sessions[schema] = Session()
    return sessions[schema]


def dropAllTables(host=Host.G_CLOUD_SSL, schema=models.schema):
    meta = sqlalchemy.MetaData(getEngine(host=host, schema=schema))
    meta.reflect()
    meta.drop_all()


def getArticle(url, host=Host.G_CLOUD_SSL, schema=models.schema):
    articles = getDBSession(host=host, schema=schema).query(models.Article)\
        .filter(models.Article.article_url == url).all()
    if len(articles) == 0:
        return None
    else:
        return articles[0]


def getSource(name, host=Host.G_CLOUD_SSL, schema=models.schema, verbose=Verbose.ERROR):
    sources = getDBSession(host=host, schema=schema).query(
        models.Source).filter(models.Source.source_name == name).all()
    if len(sources) > 1:
        if verbose <= Verbose.WARNING:
            print("Warning: multiple sources matching name", name)
            print("Possible matches", [x['source_name'] for x in sources])
    elif len(sources) == 0:
        return None
    return sources[0]


def getSearch(gmail_request_uuid, host=Host.G_CLOUD_SSL, schema=models.schema):
    searches = getDBSession(host=host, schema=schema).query(models.ArticleSearch)\
        .filter(models.ArticleSearch.gmail_request_uuid == gmail_request_uuid).all()
    if searches is None:
        return None
    else:
        return searches[0]


def getSourceID(name, host=Host.G_CLOUD_SSL, schema=models.schema):
    source = getSource(name, host=host, schema=schema)
    if source is None:
        return None
    else:
        return str(source.source_uuid)


def getCustomerID(email, host=Host.G_CLOUD_SSL, schema=models.schema):
    customer_uuid = getDBSession(host=host, schema=schema).query(models.Customer.customer_uuid)\
        .filter(models.Customer.customer_email == email).all()
    if customer_uuid is None or len(customer_uuid) == 0:
        return None
    else:
        return str(customer_uuid[0][0])


def getOrSetCustomerID(email, host=Host.G_CLOUD_SSL, schema=models.schema):
    customer_uuid = getCustomerID(email, host=host, schema=schema)
    if customer_uuid is None:
        insertEntry(models.Customer(
            customer_email=email
        ))
        customer_uuid = getCustomerID(email, host=host, schema=schema)
    return customer_uuid


def getSearchMailIDs(host=Host.G_CLOUD_SSL, schema=models.schema):
    return [r[0] for r in getDBSession(host=host, schema=schema).query(models.ArticleSearch.gmail_request_uuid).all()]


def getInvalidEmailIDs(host=Host.G_CLOUD_SSL, schema=models.schema):
    return [i[0] for i in getDBSession(host=host, schema=schema).query(models.InvalidEmail.gmail_request_uuid).all()]


def getRawArticlesQuery(host=Host.G_CLOUD_SSL, schema=models.schema):
    query = getDBSession(host=host, schema=schema).query(
        models.Article.article_uuid, models.Article.title,
        models.Article.description, models.ArticleContent.article_content
    ).filter(
        models.Article.description.isnot(None)
    ).outerjoin(
        models.ArticleContent, models.ArticleContent.article_uuid == models.Article.article_uuid
    )
    return query


def insertEntry(entry, host=Host.G_CLOUD_SSL, schema=models.schema, verbose=Verbose.ERROR):
    session = getDBSession(host=host, schema=schema)
    try:
        session.add(entry)
        session.commit()
        return True
    except (psycopg2.errors.UniqueViolation, sqlalchemy.exc.IntegrityError):
        if verbose <= Verbose.WARNING:
            print("Entry already exists for ", entry)
        session.rollback()
        return False


def populateFeeds(source_name, feed_url, section=None, host=Host.G_CLOUD_SSL, schema=models.schema):
    source_uuid = getSourceID(source_name, host=host, schema=schema)
    return insertEntry(models.RSSFeed(
        source_uuid=source_uuid,
        feed_url=feed_url,
        feed_section=section
    ), host=Host.G_CLOUD_SSL, schema=models.schema)


def updateSearchStatus(article_search_uuid, status, host=Host.G_CLOUD_SSL, schema=models.schema):
    stmt = sqlalchemy.update(models.ArticleSearch)\
        .where(models.ArticleSearch.article_search_uuid == article_search_uuid)\
        .values(status=status)
    try:
        result = getEngine(host=host, schema=schema).connect().execute(stmt)
        if result.row == 1:
            return 1
        elif result.row == 0:
            return 0
        else:
            print("ERROR: Updating multiple rows at the same time")
            pass
    except BaseException as e:
        print(article_search_uuid, status, host.name, schema)
        print(e)
        return 0
    return 0
    # getDBSession(host=host, schema=schema).commit()


def updateSearch(article_search_uuid, gmail_answer_uuid, host=Host.G_CLOUD_SSL, schema=models.schema):
    stmt = sqlalchemy.update(models.ArticleSearch)\
        .where(models.ArticleSearch.article_search_uuid == article_search_uuid)\
        .values(gmail_answer_uuid=gmail_answer_uuid)
    getEngine(host=host, schema=schema).connect().execute(stmt)
    # getDBSession(host=host, schema=schema).commit()
