"""
Util functions for cleaning and processing data
"""

import logging
import sqlalchemy

from utils import models
from utils import sql_utils
from utils import translate_utils


def correctArticleLanguage(host=sql_utils.Host.G_CLOUD_SSL, schema=models.schema):
    count = 0
    articles_by_language = sql_utils.getDBSession(host=host, schema=schema).query(
            sqlalchemy.func.array_agg(models.Article.article_uuid), models.Source.language
        ).join(
            models.Source, models.Article.source_uuid == models.Source.source_uuid
        ).group_by(models.Source.language).all()

    for language_i in range(len(articles_by_language)):
        logging.info('Processing language', articles_by_language[language_i][1])
        if articles_by_language[language_i][1] != 'en':
            for article_i in range(len(articles_by_language[language_i])):
                logging.info('   Processing article', articles_by_language[language_i][0][article_i])
                article = sql_utils.getDBSession(host=host, schema=schema).query(models.Article).filter(
                        models.Article.article_uuid == str(articles_by_language[language_i][0][article_i])
                    ).first()

                title_translation = translate_utils.translateText(article.title)
                if title_translation.detected_language_code != 'en':
                    if article.description is not None:
                        description_translation = translate_utils.translateText(article.description)

                    mutli_lingual_article = models.MultiLingualArticle(
                        article_uuid=str(article.article_uuid),
                        title=article.title,
                        description=article.description,
                        language=title_translation.detected_language_code
                    )

                    count += sql_utils.insertEntry(mutli_lingual_article, host=host, schema=schema)

                    article.title = title_translation.translated_text
                    if article.description is not None:
                        article.description = description_translation.translated_text
                    sql_utils.commitSession(host=host, schema=schema)
    return count
