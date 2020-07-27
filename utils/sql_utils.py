"""
Util functions for postgres connections and sql
"""

import psycopg2
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from data_model import models
from utils import sql_utils


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
    global engines
    global sessions
    meta = sqlalchemy.MetaData(sql_utils.getEngine(schema=schema))
    meta.reflect()
    meta.drop_all()


def getSource(name, schema=models.schema):
    sources = getDBSession(schema=schema).query(
        models.Source).filter(models.Source.source_name == name).all()
    if len(sources) > 1:
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


def insertEntry(entry, schema=models.schema):
    session = getDBSession()
    try:
        session.add(entry)
        session.commit()
    except (psycopg2.errors.UniqueViolation, sqlalchemy.exc.IntegrityError):
        print("Entry already exists for ", entry)
        session.rollback()
