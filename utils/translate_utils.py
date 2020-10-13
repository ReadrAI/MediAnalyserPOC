"""
Util functions for translation
"""

from google.cloud import translate


# This function should not be called outside of translate_utils.
def getTranslationClient():
    global translationClient
    try:
        translationClient
    except (NameError, UnboundLocalError):
        translationClient = __createTranslationClient()
    return translationClient


def __createTranslationClient():
    return translate.TranslationServiceClient()


# This function should not be called outside of translate_utils.
def getTranslationParent(project_id="future-oasis-286707", location="global"):
    global parents
    try:
        parents
    except (NameError, UnboundLocalError):
        parents = {}
    if project_id not in parents:
        parents[project_id] = {}
    if location not in parents[project_id]:
        parents[project_id][location] = "projects/%s/locations/%s" % (project_id, location)
    return parents[project_id][location]


def translateBatch(textArray):
    translationClient = getTranslationClient()
    parent = getTranslationParent()
    response = translationClient.translate_text(contents=textArray, target_language_code='en', parent=parent)
    return response.translations


def translateText(text):
    return translateBatch([text])[0]


def detectLanguage(text):
    translationClient = getTranslationClient()
    parent = getTranslationParent()
    response = translationClient.detect_language(parent=parent, content=text)

    sorted_languages = sorted(response.languages, key=lambda x: x.confidence, reverse=True)
    return sorted_languages[0].language_code


def getSupportedLanguages():
    translationClient = getTranslationClient()
    parent = getTranslationParent()
    supported_languages = translationClient.get_supported_languages(parent=parent)
    return supported_languages
