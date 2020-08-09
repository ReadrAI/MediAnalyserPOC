"""
Util functions for postgres connections and sql
"""

import psycopg2
import sqlalchemy
from sqlalchemy.orm import sessionmaker

import pandas as pd

from data_model import models
from utils import sql_utils
from utils.verbose import Verbose


def getDBUrl():
    username = "jean"
    password = ""
    host = "127.0.0.1"
    port = "5432"
    database = "media"
    return 'postgres://' + username + ':' + password + \
        '@' + host + ':' + str(port) + '/' + database


def getEngine(schema=models.schema):
    global engines
    try:
        engines
    except (NameError, UnboundLocalError):
        engines = {}
    if schema not in engines:
        connectArgs = {}
        if schema is not None:
            connectArgs['options'] = '-csearch_path=' + schema
        engines[schema] = sqlalchemy.create_engine(
            getDBUrl(), connect_args=connectArgs)
    return engines[schema]


def getDBSession(schema=models.schema):
    global sessions
    try:
        sessions
    except (NameError, UnboundLocalError):
        sessions = {}
    if schema not in sessions:
        Session = sessionmaker(bind=getEngine(schema))
        sessions[schema] = Session()
    return sessions[schema]


def dropAllTables(schema=models.schema):
    meta = sqlalchemy.MetaData(sql_utils.getEngine(schema=schema))
    meta.reflect()
    meta.drop_all()


def getSource(name, schema=models.schema, verbose=Verbose.ERROR):
    sources = getDBSession(schema=schema).query(
        models.Source).filter(models.Source.source_name == name).all()
    if len(sources) > 1:
        if verbose <= Verbose.WARNING:
            print("Warning: multiple sources matching name", name)
            print("Possible matches", [x['source_name'] for x in sources])
    elif len(sources) == 0:
        return None
    return sources[0]


def getSourceID(name, schema=models.schema):
    source = getSource(name, schema)
    if source is None:
        return None
    else:
        return str(source.source_uuid)


def getRawArticles(schema=models.schema):
    query = getDBSession(models.schema).query(
        models.Article.article_uuid, models.Article.title,
        models.Article.description, models.ArticleContent.article_content
    ).filter(
        models.Article.description.isnot(None)
    ).outerjoin(
        models.ArticleContent, models.ArticleContent.article_uuid == models.Article.article_uuid
    )
    return pd.read_sql(query.statement, query.session.bind)


def insertEntry(entry, schema=models.schema, verbose=Verbose.ERROR):
    session = getDBSession()
    try:
        session.add(entry)
        session.commit()
        return True
    except (psycopg2.errors.UniqueViolation, sqlalchemy.exc.IntegrityError):
        if verbose <= Verbose.WARNING:
            print("Entry already exists for ", entry)
        session.rollback()
        return False


def populateFeeds(source_name, feed_url, section=None):
    source_uuid = sql_utils.getSourceID(source_name)
    return sql_utils.insertEntry(models.RSSFeed(
        source_uuid=source_uuid,
        feed_url=feed_url,
        feed_section=section
    ))
