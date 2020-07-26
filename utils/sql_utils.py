"""
Util functions for postgres connections and sql
"""

import psycopg2
import sqlalchemy

# agressivité
# orientation politique

# ploting
# clustering, analyse multifactorielle sémantique points communs
# recommendation articles qui couvrent tout le sujet (2-3 de divers opinions)


# story instagram (titre, nom journal, phrase clé) pour différents articles, story suivant -> thème intéressant
# titre, citation venant de l'article

# Revue de presse
# Avoir les opinions

# Huffington post vs France Inter
# différents opinions sur un même sujet politique intérnationnal

# Plongeon sur un topic
# Références historiques (quelques semaines)

# Composition personnelle de revue de presse
#

# People? Meme catégories que dans les journeaux: sport,
# Devanture de kioscke de journal avec toutes les unes

def getDBUrl(schema=None):
    username = "jean"
    password = ""
    host = "127.0.0.1"
    port = "5432"
    database = "media"
    return 'postgres://' + username + ':' + password + \
        '@' + host + ':' + str(port) + '/' + database


def getDBConnection(schema=None):
    connectArgs = {}
    if schema is not None:
        connectArgs['options'] = '-csearch_path=' + schema
    return sqlalchemy.create_engine(getDBUrl(schema=schema), connect_args=connectArgs).connect()


def getConnection():
    global connection
    try:
        connection
    except (NameError, UnboundLocalError):
        connection = getDBConnection()
    return connection


def getSourceID(name):
    connection = getConnection()
    sql = f"""select * from media.listing.sources where source_name = '{name}';"""
    sources = connection.execute(sql).fetchall()
    if len(sources) > 1:
        print("Warning: multiple sources matching name", name)
        print("Possible matches", [x['source_name'] for x in sources])
    elif len(sources) == 0:
        return None
    return str(sources[0]['source_uuid'])


# source_name, country, website_url, api_url, api_key, aliases):
def insertSource(source_name, params={}):
    possible_source_params = ['country',
                              'website_url',
                              'api_url',
                              'api_key',
                              'aliases']
    connection = getConnection()
    params = {k: v for k, v in params.items(
    ) if k in possible_source_params and v is not None}
    sql = f"""insert into media.listing.sources (source_name, {", ".join(params.keys())}, addedat)
        values ('%s', {"%s, " * len(params.values())}, current_timestamp);"""
    try:
        connection.execute(sql, tuple([source_name].append(params.values())))
    except (psycopg2.errors.UniqueViolation, sqlalchemy.exc.IntegrityError):
        print("Source already exists:", source_name)


def escape(elements):
    return [e.replace("'", "\\'") for e in elements]


def list_for_sql(elements):
    elements = escape(elements)
    return ("'" + "', '".join(list(elements)) + "'").replace("'NULL'", "NULL")


def array_for_sql(elements):
    elements = escape(elements)
    return "\"" + "\", \"".join(list(elements)) + "\"".replace("'NULL'", "NULL")


def insertArticle(params):

    possible_article_params = ['article_url',
                               'source_uuid',
                               'provider_uuid',
                               'title',
                               'description',
                               'author',
                               'publishedAt',
                               'updatedAt']

    connection = getConnection()
    params = {k: v for k, v in params.items(
    ) if k in possible_article_params and v is not None}
    sql = f"""insert into media.listing.articles ({", ".join(params.keys())})
        values ({ "%s, " * (len(params.values()) - 1) + "%s"});"""
    try:
        connection.execute(sql, tuple(params.values()))
        if 'article_url' in params and 'description' in params:
            article_uuid_sql = f"""select article_uuid from articles where article_url = '{params['article_url']}';"""
            article_uuid = str(connection.execute(
                article_uuid_sql).fetchall()[0][0])
            description_sql = f"""insert into media.listing.article_contents
                values (%s, %s);"""
            connection.execute(
                description_sql, (article_uuid, params['description']))
    except (psycopg2.errors.UniqueViolation, sqlalchemy.exc.IntegrityError):
        if 'article_url' in params:
            print("Article article already exists:", params['article_url'])
        else:
            print("Article url is required.")
        # todo manage article duplicates with difference or different sources


def getSource(source_name):
    connection = getConnection()
    sql = f"""select source_name, api_url, api_key from sources where source_name = '{source_name}'"""
    return connection.execute(sql).fetchall()[0]
    # todo include aliases in search
