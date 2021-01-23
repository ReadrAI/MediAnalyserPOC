"""
Machine Learning models creation and usage function
"""

import gensim
import spacy
import logging

import numpy as np
import pandas as pd

from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer

from utils import models
from utils import sql_utils
from utils.data_manager import DataManager

nlp = spacy.load('en_core_web_sm')

"""
NLP model dimension
"""
w2v_size = 50

"""
NLP model attributes
"""
w2v_attributes = {
    'title': 'title',
    'description': 'description',
    'article_content': 'article_content',
}


class Models:
    NEWS_DICT = 'NEWS_DICT'  # News Dictionnary
    NEWS_INDEX = 'NEWS_INDEX'  # News Index
    W2V = 'W2V'  # Word to Vec
    NEWS_VECT = 'NEWS_VECT'  # News Vectors
    KNN = 'KNN'  # K Nearest Neighbour


def cleanText(text, to_remove=['PUNCT', 'PRON', 'SYM', 'NUM', 'ADP']):
    return ' '.join([y.lemma_ for y in nlp(text.lower()) if not y.is_stop and y.pos_ not in to_remove])


def createArticleDictionnary(attributes=list(w2v_attributes.keys()), host=sql_utils.Host.G_CLOUD_SSL,
                             schema=models.schema):
    query = sql_utils.getRawArticlesQuery(n_days=8, host=host, schema=schema)
    df = pd.read_sql(query.statement, query.session.bind)
    news_dict = {}
    progress = 0
    for i, article in df.iterrows():
        p = int(i / df.shape[0] * 100)
        if p > progress and p % 10 == 0:
            progress = p
            logging.info(("%d" % progress) + "%")
        article_uuid = str(article.article_uuid)
        news_dict[article_uuid] = {}
        for attribute_i in attributes:
            if article[attribute_i] is not None:
                news_dict[article_uuid][attribute_i] = cleanText(
                    article[attribute_i])
    DataManager.setTmpModel(Models.NEWS_DICT, news_dict)
    DataManager.setTmpModel(Models.NEWS_INDEX, list(news_dict.keys()))
    return df.shape[0]


def createWord2VectorModel(attributes=list(w2v_attributes.keys())):
    news_dict = DataManager.getTmpModel(Models.NEWS_DICT)
    documents = []
    for article in news_dict.values():
        for attribute_i in attributes:
            if attribute_i in article:
                documents.append(article[attribute_i].split())
    w2v_model = gensim.models.Word2Vec(
        documents,
        size=w2v_size,
        window=5,
        min_count=2,
        workers=4)
    w2v_model.train(
        documents,
        total_examples=len(documents),
        epochs=200)
    w2v_model.init_sims(replace=True)
    DataManager.setTmpModel(Models.W2V, w2v_model)
    return w2v_size


def createTFIDFModel(attribute, min_df=1, max_df=1., ngram_range=(1, 1)):
    news_dict = DataManager.getTmpModel(Models.NEWS_DICT)
    w2v_model = DataManager.getTmpModel(Models.W2V)

    result = {}
    result['documents'] = [(v[attribute]) for v in news_dict.values() if attribute in v]
    result['tfidf_vectorizer'] = TfidfVectorizer(stop_words=None, min_df=min_df, max_df=max_df, ngram_range=ngram_range)
    result['tfidf_weights'] = result['tfidf_vectorizer'].fit_transform(result['documents'])
    result['tfidf_embeddings'] = [getWordVector(word, w2v_model)
                                  for word in result['tfidf_vectorizer'].get_feature_names()]
    result['news_vector'] = np.array(result['tfidf_weights'].todense() * result['tfidf_embeddings'])
    return result


def getWordVector(word, w2v_model):
    try:
        return w2v_model.wv.get_vector(word)
    except KeyError:
        return np.zeros([w2v_size])


def createNewsVectors(attributes=list(w2v_attributes.keys())):
    news_vect = {}
    for attribute_i in attributes:
        news_vect[attribute_i] = createTFIDFModel(attribute_i, min_df=3, max_df=0.05, ngram_range=(1, 1))
    DataManager.setTmpModel(Models.NEWS_VECT, news_vect)


def createKNNModel(attributes=list(w2v_attributes.keys()), neighbors=5):
    news_vect = DataManager.getTmpModel(Models.NEWS_VECT)
    neighbours = {}
    for attribute_i in attributes:
        neighbours[attribute_i] = NearestNeighbors(n_neighbors=neighbors).fit(news_vect[attribute_i]['news_vector'])
    DataManager.setTmpModel(Models.KNN, neighbours)


def createNlpModels(attributes=list(w2v_attributes.keys()), schema=models.schema, host=sql_utils.Host.G_CLOUD_SSL):
    article_count = createArticleDictionnary(host=host, schema=schema)
    model_dim = createWord2VectorModel(attributes=attributes)
    createNewsVectors(attributes=attributes)
    createKNNModel(attributes=attributes)
    DataManager.validateModels([Models.NEWS_DICT, Models.NEWS_INDEX, Models.W2V, Models.NEWS_VECT, Models.KNN])
    return article_count, model_dim


def getTextEmbedding(search_text, attribute):

    news_vect = DataManager.getModel(Models.NEWS_VECT)
    w2v_model = DataManager.getModel(Models.W2V)

    embedding = np.zeros([w2v_size])
    word_count = 0

    for word in cleanText(search_text).split():
        try:
            index = news_vect[attribute]['tfidf_vectorizer'].get_feature_names().index(word)
            weight = news_vect[attribute]['tfidf_vectorizer'].idf_[index]
            vec = news_vect[attribute]['tfidf_embeddings'][index]
            word_count += 1
            embedding += vec * weight
        except (ValueError, KeyError):
            try:
                embedding += w2v_model.wv.get_vector(word)
                word_count += 1
            except KeyError:
                logging.error('Word not found: ' + word)

    if word_count > 0:
        return embedding / word_count
    else:
        return embedding


def getSimilarArticlesFromText(search_text, attribute='title', nb_articles=10, schema=models.schema,
                               host=sql_utils.Host.G_CLOUD_SSL):
    news_index = DataManager.getModel(Models.NEWS_INDEX)
    neighbours = DataManager.getModel(Models.KNN)
    embedding = getTextEmbedding(search_text, attribute)

    neighbour_articles = neighbours[attribute].kneighbors(embedding.reshape(1, w2v_size), n_neighbors=nb_articles)
    similar_articles = {}
    for i, j in enumerate(neighbour_articles[1][0]):
        similar_articles[news_index[j]] = {}
        similar_articles[news_index[j]]['distance'] = neighbour_articles[0][0][i]
    article_uuids = list(similar_articles.keys())
    query = sql_utils.getArticleData(article_uuids, host=host, schema=schema)
    similar_article_details = pd.read_sql(query.statement, query.session.bind)
    similar_article_details['article_uuid'] = similar_article_details['article_uuid'].astype(str)
    similar_articles_df = pd.DataFrame(similar_articles).T
    similar_articles_df.index.rename('article_uuid', inplace=True)
    similar_article_details = similar_article_details.set_index('article_uuid').join(similar_articles_df)
    return similar_article_details.sort_values('distance').head(nb_articles)
