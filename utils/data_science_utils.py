"""
Machine Learning models creation and usage function
"""

import plotly
import pickle
import gensim
import en_core_web_sm

import numpy as np
import pandas as pd

from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer

from data_model import models
from utils import sql_utils
from utils.verbose import Verbose

nlp = en_core_web_sm.load()

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

plotly.offline.init_notebook_mode(connected=True)

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
    NEWS_DICT = 'NEWS_DICT'  #  news Dictionnary
    W2V = 'W2V'  #  Word to vec
    NEWS_VECT = 'NEWS_VECT'  #  news Vectors
    KNN = 'KNN'  #  K Nearest Neighbour


def setModel(w2v_model, data):
    with open('../ml_models/' + w2v_model + '.pickle', 'wb') as f:
        pickle.dump(data, f)


def getModel(w2v_model):
    with open('../ml_models/' + w2v_model + '.pickle', 'rb') as f:
        return pickle.load(f)


def cleanText(text, to_remove=['PUNCT', 'PRON', 'SYM', 'NUM', 'ADP']):
    return ' '.join([y.lemma_ for y in nlp(text.lower()) if not y.is_stop and y.pos_ not in to_remove])


def createArticleDictionnary(schema=models.schema, attributes=list(w2v_attributes.keys()), verbose=Verbose.ERROR):
    df = sql_utils.getRawArticles(schema=schema)
    news_dict = {}
    progress = 0
    for i, article in df.iterrows():
        p = int(i / df.shape[0] * 100)
        if p > progress and p % 10 == 0 and verbose <= Verbose.INFO:
            progress = p
            print("%d" % progress, "%")
        article_uuid = str(article.article_uuid)
        news_dict[article_uuid] = {}
        for attribute_i in attributes:
            if article[attribute_i] is not None:
                news_dict[article_uuid][attribute_i] = cleanText(
                    article[attribute_i])
    setModel(Models.NEWS_DICT, news_dict)


def createWord2VectorModel(attributes=list(w2v_attributes.keys())):
    news_dict = getModel(Models.NEWS_DICT)
    documents = []
    for _, article in news_dict.items():
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
    setModel(Models.W2V, w2v_model)


def createTFIDFModel(attribute, min_df=1, max_df=1.):
    news_dict = getModel(Models.NEWS_DICT)
    w2v_model = getModel(Models.W2V)

    result = {}
    result['documents'] = [(v[attribute]) for v in news_dict.values()]
    result['tfidf_vectorizer'] = TfidfVectorizer(stop_words=None, min_df=min_df, max_df=max_df)
    result['tfidf_weights'] = result['tfidf_vectorizer'].fit_transform(result['documents'])
    result['tfidf_embeddings'] = [w2v_model.wv.get_vector(word) for word
                                  in result['tfidf_vectorizer'].get_feature_names()]
    result['news_vector'] = np.array(result['tfidf_weights'].todense() * result['tfidf_embeddings'])

    # df = pd.DataFrame(
    #     result['tfidf_weights'][0].T.todense(),
    #     index=result['tfidf_vectorizer'].get_feature_names(),
    #     columns=["tfidf_weight"])
    return result


def createNewsVectors(attributes=list(w2v_attributes.keys())):
    news_vect = {}
    for attribute_i in attributes:
        news_vect[attribute_i] = createTFIDFModel(attribute_i, min_df=3, max_df=0.001)
    setModel(Models.NEWS_VECT, news_vect)


def createKNNModel(attributes=list(w2v_attributes.keys()), neighbors=5):
    news_vect = getModel(Models.NEWS_VECT)
    neighbours = {}
    for attribute_i in attributes:
        neighbours[attribute_i] = NearestNeighbors(n_neighbors=neighbors).fit(news_vect[attribute_i]['news_vector'])
    setModel(Models.KNN, neighbours)


def createNlpModel(attributes=list(w2v_attributes.keys()), schema=models.schema, verbose=Verbose.ERROR):
    createArticleDictionnary()
    createWord2VectorModel(attributes=attributes)
    createNewsVectors(attributes=attributes)
    createKNNModel(attributes=attributes)
