"""
Util functions for mail reception and sending
"""

import re
import pytz
import pickle
import base64
import email
import logging
import os.path
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from utils import sql_utils
from utils import data_science_utils
from utils import scrape_utils
from utils import models
from utils.data_manager import DataManager

logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/gmail.modify',
          'https://www.googleapis.com/auth/pubsub',
          'https://www.googleapis.com/auth/gmail.readonly']

SENDER_EMAIL = "newshorizonapp@gmail.com"


def getCurrentTimestamp():
    return datetime.datetime.now(tz=pytz.timezone('Europe/Brussels')).strftime("%Y.%m.%d %H:%M %Z")


def getGmailService():
    global service
    try:
        service
    except (NameError, UnboundLocalError):
        service = __createGmailService()
    return service


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


def create_message(sender, to, subject, plain_text, html_text=None, thread_id=None, in_reply_to=None):

    message = MIMEMultipart('alternative')
    message["subject"] = subject
    message["from"] = sender
    message["to"] = to

    part1 = MIMEText(plain_text, "plain")
    message.attach(part1)
    if html_text is not None:
        part2 = MIMEText(html_text, "html")
        message.attach(part2)

    message.add_header("In-Reply-To", in_reply_to)
    message.add_header("References", in_reply_to)

    output = {'raw': base64.urlsafe_b64encode(bytes(message.as_string(), "utf-8")).decode("utf-8")}

    if thread_id is not None:
        output['threadId'] = thread_id

    return output


def answerEmail(request_email, to, plain_text, html_text=None, host=sql_utils.Host.G_CLOUD_SSL, schema=models.schema):
    message = create_message(
        sender=SENDER_EMAIL,
        to=to,
        subject="RE: " + request_email['subject'],
        plain_text=plain_text,
        html_text=html_text,
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


def get_messages(service, user_id):
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
            if 'parts' in raw['payload'] and len(raw['payload']['parts']) > 0 and 'body' in raw['payload']['parts'][0]\
                    and 'data' in raw['payload']['parts'][0]['body']:
                values['content'] = decode(raw['payload']['parts'][0]['body']['data'])
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
    reg = re.search("(?P<url>https?://[^\s]+)", text)
    if reg is not None:
        return reg.group("url")


def parse_email(email_tag):
    x = email_tag.find("<")
    if x >= 0:
        return email_tag[x+1:-1]
    else:
        return email_tag


def downloadArticle(article_search, host=sql_utils.Host.G_CLOUD_SSL, schema=models.schema):
    sources = sql_utils.getSourceFromUrl(article_search.search_url, host=host, schema=schema)
    if len(sources) == 0:
        logging.error('FAILURE: Source not found ' + str(article_search.article_search_uuid))
        sql_utils.updateSearchStatus(article_search.article_search_uuid, 'FAILURE: Source not found', host=host,
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
            #     sql_utils.updateSearchStatus(article_search.article_search_uuid, 'FAILURE: Source domain not found',
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


def processEmails(request_emails, host=sql_utils.Host.G_CLOUD_SSL, schema=models.schema):
    logging.debug("### Starting to answer emails at " + getCurrentTimestamp())
    count = 0
    for request_i in request_emails:
        logging.debug("### Article search for article %s at " % request_i['subject'] + getCurrentTimestamp())
        logging.info("Processing request " + request_i['id'])
        logging.info("Subject: " + request_i['subject'])
        logging.info("Content: " + request_i['content'])
        requester_email = parse_email(request_i['from'])
        logging.debug("### Customer ID search at " + getCurrentTimestamp())
        customer_uuid = sql_utils.getOrSetCustomerID(requester_email, host=host, schema=schema)
        search_url = getUrlFromText(request_i['subject'])
        if search_url is None:
            search_url = getUrlFromText(request_i['content'])
        logging.debug("### Inserting search entry at " + getCurrentTimestamp())
        if search_url is None:
            logging.error("No URL found for message %s: %s\n %s\n" % (
                        request_i['id'], request_i['subject'], request_i['content']))
            logging.debug(str(customer_uuid) + " " + str(customer_uuid) + " " + str(type(customer_uuid)))
            sql_utils.insertEntry(models.ArticleSearch(
                gmail_request_uuid=request_i['id'],
                customer_uuid=str(customer_uuid),
                status='FAILURE: missing URL'
            ), host=host, schema=schema)
            continue
        success = sql_utils.insertEntry(models.ArticleSearch(
            gmail_request_uuid=request_i['id'],
            search_url=search_url,
            customer_uuid=customer_uuid
        ), host=host, schema=schema)
        if not success:
            logging.error("Could not insert search for entry %s" % request_i['id'])
            continue
        else:
            logging.error("### Getting article search at " + getCurrentTimestamp())
            article_search = sql_utils.getSearch(request_i['id'], host=host, schema=schema)
            search_article = sql_utils.getArticle(search_url, host=host, schema=schema)
            if search_article is None:
                # broken code, add when fixed
                # search_article = downloadArticle(article_search, host=host, schema=schema)
                if search_article is None:
                    logging.error('FAILURE: Article not found for search ' + str(article_search))
                    sql_utils.updateSearchStatus(article_search.article_search_uuid, 'FAILURE: Article not found',
                                                 host=host, schema=schema)
                    continue
            sql_utils.updateSearchArticle(article_search.article_search_uuid, search_article.article_uuid, host=host, 
                                          schema=schema)
            search_attribute = 'title'
            logging.debug("### Starting similarity search at " + getCurrentTimestamp())
            result = data_science_utils.getSimilarArticlesFromText(
                search_article.title if search_attribute == 'title' else search_article.description,
                search_attribute, article_search.n_results)
            result['title_url'] = result[['title', 'article_url']].apply(__addUrlLinks, axis=1)
            html_text = result[['source_name', 'title_url']].to_html(escape=False, header=False, index=False)
            plain_text = result[['source_name', 'title']].to_string(header=False, index=False)
            logging.debug("### Sending answer email at " + getCurrentTimestamp())
            sent_message = answerEmail(request_email=request_i, to=article_search.customer.customer_email,
                                       plain_text=plain_text, html_text=html_text, host=host, schema=schema)
            logging.debug("### Seting article search status at " + getCurrentTimestamp())
            if sent_message is None:
                sql_utils.updateSearchStatus(article_search.article_search_uuid, 'FAILURE: Message not sent', host=host,
                                             schema=schema)
            else:
                count += sql_utils.updateSearchStatus(article_search.article_search_uuid, 'SUCCESS', host=host,
                                                      schema=schema)
                sql_utils.updateSearchAnswer(article_search.article_search_uuid, sent_message['id'], host=host, 
                                             schema=schema)
    return count


def __addUrlLinks(entry):
    return '<a href="' + entry['article_url'] + '">' + entry['title'] + '</a>'


def pipelineEmails(host=sql_utils.Host.G_CLOUD_SSL, schema=models.schema):
    logging.debug("### Email pipeline started at " + getCurrentTimestamp())
    emails = fetchEmails(host=host, schema=schema)
    count = processEmails(emails, host=host, schema=schema)
    logging.debug("### Email pipeline done at " + getCurrentTimestamp())
    logging.info("Answered Email Count: " + str(count))
    return count


def fetchEmails(host=sql_utils.Host.G_CLOUD_SSL, schema=models.schema):
    service = getGmailService()
    messages = get_messages(service, 'me')
    logging.debug("### Past request loading at " + getCurrentTimestamp())
    past_requests = sql_utils.getSearchMailIDs(host=host, schema=schema)
    logging.debug("### Invalid email loading at " + getCurrentTimestamp())
    invalid_emails = sql_utils.getInvalidEmailIDs(host=host, schema=schema)
    logging.debug("### New emails fetching at " + getCurrentTimestamp())
    logging.debug("### %d emails to fetch" % len(messages['messages']))
    request_emails = []
    for m in messages['messages']:
        if m['id'] not in past_requests and m['id'] not in invalid_emails:
            values = getMessageContent(m)
            request_email_i = parse_email(values['from'])
            if 'no-reply' in values['from']:
                sql_utils.insertEntry(models.InvalidEmail(
                    gmail_request_uuid=m['id'],
                    customer_uuid=sql_utils.getOrSetCustomerID(request_email_i, host=host, schema=schema),
                    status='NO-REPLY sender'
                ), host=host, schema=schema)
            elif values['from'] == SENDER_EMAIL:
                sql_utils.insertEntry(models.InvalidEmail(
                    gmail_request_uuid=m['id'],
                    customer_uuid=sql_utils.getOrSetCustomerID(request_email_i, host=host, schema=schema),
                    status='SELF sender'
                ), host=host, schema=schema)
            else:
                request_emails.append(values)
    return request_emails


def setPushNotifications():
    service = getGmailService()
    request = {
        'labelIds': ['INBOX'],
        'topicName': 'projects/future-oasis-286707/topics/email-request-topic'
    }
    return service.users().watch(userId=SENDER_EMAIL, body=request).execute()
