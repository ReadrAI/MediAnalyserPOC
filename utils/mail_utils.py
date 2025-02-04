"""
Util functions for mail reception and sending
"""

import re
import sys
import pytz
import pickle
import base64
import email
import logging
import os.path
import datetime
import threading
import tldextract
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from utils import sql_utils
from utils import data_science_utils
from utils import scrape_utils
from utils import models
from utils import translate_utils
from utils import data_visualisation
from utils.data_manager import DataManager


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/gmail.modify',
          'https://www.googleapis.com/auth/pubsub',
          'https://www.googleapis.com/auth/gmail.readonly']

SENDER_EMAIL = "newshorizonapp@gmail.com"


def getCurrentTimestamp():
    return datetime.datetime.now(tz=pytz.timezone('Europe/Brussels')).strftime("%Y.%m.%d %H:%M %Z")


def getGmailService():
    global services
    try:
        services
    except (NameError, UnboundLocalError):
        services = {}
    thread_id = threading.get_ident()
    if thread_id not in services:
        services[thread_id] = __createGmailService()
    return services[thread_id]


def __createGmailService():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    modulePath = DataManager.getModulePath()
    tokenPath = modulePath + os.sep + 'credentials' + os.sep + 'newshorizonmail_token.pickle'
    credentialPath = modulePath + os.sep + 'credentials' + os.sep + 'newshorizonmail_credentials.json'
    if os.path.exists(tokenPath):
        with open(tokenPath, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentialPath, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(tokenPath, 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service


def create_message(sender, to, subject, plain_text, html_text=None, map_img=None, thread_id=None, in_reply_to=None):

    message = MIMEMultipart('related')
    message["subject"] = subject
    message["from"] = sender
    message["to"] = to

    # part1 = MIMEText(plain_text, "plain")
    # message.attach(part1)
    # if html_text is not None:
    part2 = MIMEText(html_text or plain_text or "", "html")
    message.attach(part2)

    message.add_header("In-Reply-To", in_reply_to)
    message.add_header("References", in_reply_to)

    if map_img is not None:
        message.attach(map_img)

    output = {'raw': base64.urlsafe_b64encode(message.as_string().encode("utf-8")).decode("utf-8")}

    if thread_id is not None:
        output['threadId'] = thread_id

    return output


def answerEmail(request_email, to, plain_text, html_text=None, map_img=None, host=None, schema=models.schema):
    service = getGmailService()
    message = create_message(
        sender=SENDER_EMAIL,
        to=to,
        subject="RE: " + request_email['subject'],
        plain_text=plain_text,
        html_text=html_text,
        map_img=map_img,
        thread_id=request_email['threadId'],
        in_reply_to=request_email['message-id'])
    return send_message(service, 'me', message)


def create_draft(service, user_id, message_body):
    try:
        message = {'message': message_body}
        draft = service.users().drafts().create(userId=user_id, body=message).execute()

        return draft
    except Exception as e:
        logging.error('An error occurred: %s' % e)
        return None


def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(
            userId=user_id, body=message).execute()
        return message
    except Exception as e:
        logging.error('An error occurred: %s' % e)
        return None


def get_message_list(service, user_id):
    try:
        return service.users().messages().list(userId=user_id).execute()
    except Exception as error:
        logging.error('An error occurred: %s' % error)


def get_message(service, user_id, msg_id):
    try:
        return service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
    except Exception as error:
        logging.error('An error occurred: %s' % error)


def get_mime_message(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id,
                                                 format='raw').execute()
        msg_str = base64.urlsafe_b64decode(
            message['raw'].encode("utf-8")).decode("utf-8")
        mime_msg = email.message_from_string(msg_str)

        return mime_msg
    except Exception as error:
        logging.error('An error occurred: %s' % error)


def get_attachments(service, user_id, msg_id, store_dir):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()

        for part in message['payload']['parts']:
            if(part['filename'] and part['body'] and part['body']['attachmentId']):
                attachment = service.users().messages().attachments()\
                    .get(id=part['body']['attachmentId'], userId=user_id, messageId=msg_id).execute()

                file_data = base64.urlsafe_b64decode(attachment['data'].encode('utf-8'))
                path = ''.join([store_dir, part['filename']])

                f = open(path, 'wb')
                f.write(file_data)
                f.close()
    except Exception as error:
        logging.error('An error occurred: %s' % error)


def getMessageContent(message):
    service = getGmailService()
    values = {}
    values['id'] = message['id']
    values['threadId'] = message['threadId']
    raw = get_message(service, 'me', message['id'])
    if raw is not None:
        if 'payload' in raw:
            if 'headers' in raw['payload']:
                for entry in raw['payload']['headers']:
                    values[entry['name'].lower()] = entry['value']
            if 'parts' in raw['payload'] and len(raw['payload']['parts']) > 0:
                if 'body' in raw['payload']['parts'][0] and 'data' in raw['payload']['parts'][0]['body']:
                    values['content'] = decode(raw['payload']['parts'][0]['body']['data'])
                if len(raw['payload']['parts']) > 1 and 'body' in raw['payload']['parts'][1] and\
                        'data' in raw['payload']['parts'][1]['body']:
                    html = decode(raw['payload']['parts'][1]['body']['data'])
                    links = BeautifulSoup(html, 'lxml').find_all('a', href=True)
                    found_urls = [l_i['href'] for l_i in links if not l_i['href'].startswith('mailto:')]
                    if len(found_urls) > 0:
                        values['url'] = found_urls[0]
            elif 'body' in raw['payload'] and 'data' in raw['payload']['body']:
                values['content'] = decode(raw['payload']['body']['data'])
            else:
                values['content'] = ''
        if 'snippet' in raw:
            values['snippet'] = raw['snippet']
    return values


def decode(text):
    return base64.urlsafe_b64decode(text).decode("utf-8")


def getUrlFromText(text):
    reg = re.search("(?P<url>https?://[^\s>\"]+)", text)
    if reg is not None:
        return reg.group("url")


def parseEmail(email_tag):
    x = email_tag.find("<")
    if x >= 0:
        return email_tag[x+1:-1]
    else:
        return email_tag


def downloadArticle(article_search, host, schema=models.schema):
    page = scrape_utils.downloadPage(article_search.search_url)
    if page.status_code != 200:
        logging.error("Page could not be fetched (status code " + page.status + "): " + article_search.search_url)
        return None
    if page.url != article_search.search_url:
        sql_utils.updateSearchUrl(article_search, page.url, host=host, schema=schema)

    title = scrape_utils.scrapeArticleTitle(page)
    if title is None:
        return None

    source = sql_utils.getSourceFromUrl(article_search.search_url, host=host, schema=schema)
    if source is None:
        source_entry = models.Source(
            website_url=scrape_utils.getRootUrl(article_search.search_url),
            source_name=tldextract.extract(article_search.search_url).domain
        )
        source_added = sql_utils.insertEntry(source_entry, host=host, schema=schema)
        if source_added:
            source = source_entry
    if source is None:
        return None

    if source.language != 'en':
        translation = translate_utils.translateText(title)
        language = translation.detected_language_code
        if language != 'en':
            multi_lingual_article = models.MultiLingualArticle(
                language=language,
                title=title
            )
            title = translation.translated_text

    article = models.Article(
        article_url=article_search.search_url,
        source_uuid=str(source.source_uuid),
        provider_uuid=str(source.source_uuid),
        title=title
    )

    insert_result = sql_utils.insertEntry(article, host=host, schema=schema)
    if not insert_result:
        return None

    if source.language != 'en' and language != 'en':
        multi_lingual_article.article_uuid = str(article.article_uuid)
        sql_utils.insertEntry(multi_lingual_article, host=host, schema=schema)
    return article

    # TODO correct code and add if useful
    sources = sql_utils.getSourceFromUrl(article_search.search_url, host=host, schema=schema)
    if len(sources) == 0:
        logging.error('FAILURE: Source not found ' + str(article_search.article_search_uuid))
        sql_utils.updateSearchStatus(article_search, 'FAILURE: Source not found', host=host,
                                     schema=schema)
        return None
    else:
        if len(sources) == 1:
            source = sources[0]
        else:
            logging.error('FAILURE: Source domain not found ' + str(article_search.article_search_uuid))
            return None
            # Code not functional. TODO fix and add back

            # path_elements = urlparse(article_search.search_url).path.split('/')
            # sources = getSourceFromUrl(article_search.search_url)

            # logging.debug(path_elements)
            # for element in path_elements:
            #     if element != '':
            #         logging.debug(sources)
            #         sources = [s for s in sources if element in s.website_url]
            #         if len(sources) <= 1:
            #             break
            # if len(sources) == 0:  # eliminated too many sources, should not happen
            #     sql_utils.updateSearchStatus(article_search, 'FAILURE: Source domain not found',
            #                                  host=host, schema=schema)
            #     logging.error('FAILURE: Source domain not found ' + str(article_search.article_search_uuid))
            #     return None
            # else:
            #     source = sources[0]
        # TODO add TF-IDF weights on key-words to select most frequent/relevant
        search_elements = article_search.search_url.split('/')[-1]
        if '.' in search_elements:
            search_elements = search_elements.split('.')[-2]
        search_elements = [x for x in map(data_science_utils.cleanText, search_elements.split('-'))
                           if not x.isdecimal() and x != '']
        scrape_utils.pipelineNewsAPIArticle(
            " ".join(search_elements),
            source.source_name.lower().replace(" ", "-"),
            fetchSource=True,
            host=host, schema=schema)
        articles = sql_utils.getArticle(article_search.search_url, host=host, schema=schema)
        if len(articles) == 0:
            # could not find article easily
            # TODO add scraping procedure
            return None
        else:
            return articles[0]


def getCustomer(request, host, schema=models.schema):
    requester_email = parseEmail(request['from'])
    customer_uuid = sql_utils.getOrSetCustomerID(requester_email, host=host, schema=schema)
    return customer_uuid


def addArticleSearch(customer_uuid, request, host, schema=models.schema):
    article_search = models.ArticleSearch(gmail_request_uuid=request['id'], customer_uuid=str(customer_uuid),
                                          status='Processing', n_results=20)
    success = sql_utils.insertEntry(article_search, host=host, schema=schema)
    if not success:
        logging.error("Could not insert search for entry %s" % request['id'])
    return article_search


def getSearchUrl(article_search, request, host, schema=models.schema):
    search_url = None
    if 'url' in request:
        search_url = request['url']

    if search_url is None:
        search_url = getUrlFromText(request['subject'])

    if search_url is None:
        search_url = getUrlFromText(request['content'])

    if search_url is None:
        logging.error("No URL found for message %s: %s\n %s\n" % (
                    request['id'], request['subject'], request['content']))
        sql_utils.updateSearchStatus(article_search, 'FAILURE: missing URL', host=host,
                                     schema=schema)
        failure_text = 'We could not find any news article URL in your email.\nWe work hard to remedy to the problem!'
        answerEmail(request, article_search.customer.customer_email, failure_text, host=host, schema=schema)
        notification_content = "sender: %s\nsubjet: %s\ncontent:\n%s" % (
                    request['from'], request['subject'], request['content'])
        sendEmailNotification("Processing request, url not found", notification_content)
        return None
    else:
        article_search.search_url = search_url
        sql_utils.commitSession(host=host, schema=schema)
    return article_search


def getSearchArticle(article_search, request, host, schema=models.schema):
    search_article = sql_utils.getArticle(article_search.search_url, host=host, schema=schema)
    if search_article is None:
        search_article = downloadArticle(article_search, host=host, schema=schema)

    if search_article is None:
        logging.error('FAILURE: Article not found for search ' + str(article_search))
        sql_utils.updateSearchStatus(article_search, 'FAILURE: Article not found', host=host,
                                     schema=schema)
        failure_text = 'We could not find your article in our database.\nWe work hard to remedy to the problem!'
        answerEmail(request, article_search.customer.customer_email, failure_text, host=host, schema=schema)
        notification_content = "sender: %s\nsubjet: %s\ncontent:\n%s" % (
                    request['from'], request['subject'], request['content'])
        sendEmailNotification("Processing request, article not found", notification_content)
        return None
    else:
        article_search.search_article = str(search_article.article_uuid)
        sql_utils.commitSession(host=host, schema=schema)
    return article_search


def getSearchResults(article_search, search_attribute, host, schema=models.schema):
    search_results = data_science_utils.getSimilarArticlesFromText(
        article_search.article.title if search_attribute == 'title' else article_search.article.description,
        search_attribute, article_search.n_results * 3)
    search_results['title_url'] = search_results[['title', 'article_url']].apply(__addUrlLinks, axis=1)
    search_results.drop_duplicates(subset=['article_url'])
    search_results = search_results[(search_results['article_url'] != article_search.article.article_url) &
                                    (search_results['article_url'] != article_search.search_url)]
    return search_results.head(article_search.n_results)


def getEmailContent(article_search, search_results):
    html_text = search_results[['source_name', 'title_url']].to_html(escape=False, header=False, index=False)
    plain_text = search_results[['source_name', 'title']].to_string(header=False, index=False)
    img, filename = data_visualisation.getMapImage(search_results, str(article_search.article_search_uuid))
    msgImg = None
    if img is not None:
        html_text = """\
            <p>
                <img src="cid:image1">
            </p>
        """ + html_text
        msgImg = MIMEImage(img, 'png')
        msgImg.add_header('Content-ID', '<image1>')
        msgImg.add_header('Content-Disposition', 'attachement', filename=filename)
    return plain_text, html_text, msgImg


def sendResults(article_search, search_results, request, host, schema=models.schema):
    plain_text, html_text, map_img = getEmailContent(article_search, search_results)
    sent_message = answerEmail(request_email=request, to=article_search.customer.customer_email,
                               plain_text=plain_text, html_text=html_text, map_img=map_img, host=host, schema=schema)
    if sent_message is None:
        sql_utils.updateSearchStatus(article_search, 'FAILURE: Message not sent', host=host, schema=schema)
        return False
    else:
        sql_utils.updateSearchStatus(article_search, 'SUCCESS', host=host, schema=schema)
        sql_utils.updateSearchAnswer(article_search, sent_message['id'], host=host, schema=schema)
        return True


def processEmails(request_emails, host, schema=models.schema):
    count = 0
    for request_i in request_emails:
        logging.info("Processing request " + request_i['id'])
        if 'subject' in request_i:
            logging.info("Subject: " + request_i['subject'])
        else:
            request_i['subject'] = ''

        try:
            customer_uuid = getCustomer(request_i, host=host, schema=schema)

            article_search = addArticleSearch(customer_uuid, request_i, host=host, schema=schema)

            article_search = getSearchUrl(article_search, request_i, host=host, schema=schema)
            if article_search is None or article_search.search_url is None:
                continue

            article_search = getSearchArticle(article_search, request_i, host=host, schema=schema)
            if article_search is None or article_search.search_article is None:
                continue

            search_results = getSearchResults(article_search, search_attribute='title', host=host, schema=schema)

            # add search results to db

            count += sendResults(article_search, search_results, request_i, host=host, schema=schema)
            notification_content = "sender: %s\nsubjet: %s\ncontent:\n%s\nresults:\n%s" % (
                    request_i['from'], request_i['subject'], request_i['content'],
                    search_results[['title', 'article_url']].to_string())
            sendEmailNotification("Processing request, done", notification_content)
        except Exception as e:
            logging.error(e)
            logging.error(sys.exc_info()[0])
            notification_content = ""
            if request_i is not None:
                if 'from' in request_i:
                    notification_content += "sender: %s\n" % request_i['from']
                if 'subject' in request_i:
                    notification_content += "subject: %s\n" % request_i['subject']
                if 'content' in request_i:
                    notification_content += "content:\n%s\n" % request_i['content']
            notification_content += "error:\n%s\n" % e
            sendEmailNotification("Pipeline Error", notification_content)
            raise e
    return count


def __addUrlLinks(entry):
    return '<a href="' + entry['article_url'] + '">' + entry['title'] + '</a>'


def pipelineEmails(host, schema=models.schema):
    logging.debug("### Email pipeline started at " + getCurrentTimestamp())
    emails = fetchEmails(host=host, schema=schema)
    count = processEmails(emails, host=host, schema=schema)
    logging.debug("### Email pipeline done at " + getCurrentTimestamp())
    logging.info("Answered Email Count: " + str(count))
    sql_utils.closeSession(host=host, schema=schema)
    return count


def isBlocked(sender_email, host, schema=models.schema):
    if 'no-reply' in sender_email or 'noreply' in sender_email or 'support' in sender_email:
        return True
    elif sql_utils.isCustomerBlocked(sender_email, host=host, schema=schema):
        return True
    else:
        return False


def fetchEmails(host, schema=models.schema):
    request_emails = []
    service = getGmailService()
    messages = get_message_list(service, 'me')
    past_requests = sql_utils.getSearchMailIDs(host=host, schema=schema)
    invalid_emails = sql_utils.getInvalidEmailIDs(host=host, schema=schema)
    if messages is not None and past_requests is not None and invalid_emails is not None:
        if 'messages' in messages:
            logging.debug("### %d emails to fetch" % len(messages['messages']))
            for m in messages['messages']:
                if m['id'] not in past_requests and m['id'] not in invalid_emails:
                    values = getMessageContent(m)
                    if 'from' in values:
                        request_email_i = parseEmail(values['from'])
                        if values['from'] == SENDER_EMAIL:
                            sql_utils.insertEntry(models.InvalidEmail(
                                gmail_request_uuid=m['id'],
                                customer_uuid=sql_utils.getOrSetCustomerID(request_email_i, host=host, schema=schema),
                                status='SELF sender'
                            ), host=host, schema=schema)
                        elif isBlocked(values['from'], host=host, schema=schema):
                            sql_utils.insertEntry(models.InvalidEmail(
                                gmail_request_uuid=m['id'],
                                customer_uuid=sql_utils.getOrSetCustomerID(request_email_i, host=host, schema=schema),
                                status='NO-REPLY sender'
                            ), host=host, schema=schema)
                        else:
                            request_emails.append(values)
                    else:
                        logging.error("No key 'from' in values for message %s" % m['id'])
        else:
            logging.error("### No email to fetch: key error. %s" % str(messages.keys()))
    else:
        logging.error("### No email to fetch: loading error. %s, %s, %s" % (
            str(messages is None), str(past_requests is None), str(invalid_emails is None)))
    return request_emails


def setPushNotifications():
    service = getGmailService()
    request = {
        'labelIds': ['INBOX'],
        'topicName': 'projects/future-oasis-286707/topics/email-request-topic'
    }
    return service.users().watch(userId=SENDER_EMAIL, body=request).execute()


def sendEmailNotification(subject, plain_text):
    message = create_message(SENDER_EMAIL, 'jean.haizmann@gmail.com', subject, plain_text)
    sent_message = send_message(getGmailService(), 'me', message)
    if sent_message is None:
        logging.error("Notification not sent at " + getCurrentTimestamp() + ": " + subject + "\n" + plain_text)


def processFailedArticleSearches(host, schema=models.schema):
    count = 0
    uncompleted_article_searches = sql_utils.getUncompletedArticleSearches(host=host, schema=schema)
    for article_search in uncompleted_article_searches:
        print('search_url: ' + article_search.search_url)
        search_article = sql_utils.getArticle(article_search.search_url, host=host, schema=schema)

        if search_article is None:
            search_article = downloadArticle(article_search, host=host, schema=schema)

        if search_article is None:
            logging.error("Article not found, nor downloaded: " + str(article_search))
            continue

        article_search.search_article = str(search_article.article_uuid)
        sql_utils.commitSession(host=host, schema=schema)

        search_results = getSearchResults(article_search, search_attribute='title', host=host, schema=schema)

        # add search results to db

        message = get_message(getGmailService(), 'me', article_search.gmail_request_uuid)
        request = getMessageContent(message)

        count += sendResults(article_search, search_results, request, host=host, schema=schema)
    return count


def renewEmailAnalysis(article_search, host, schema=models.schema):
    sql_utils.getDBSession(host=host, schema=schema).delete(article_search)
    sql_utils.commitSession(host=host, schema=schema)
    return pipelineEmails(host=host, schema=schema) >= 1
