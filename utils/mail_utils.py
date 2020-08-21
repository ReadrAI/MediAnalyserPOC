"""
Util functions for mail reception and sending
"""

import itertools
import re
import pickle
import base64
import email
import os.path
from urllib.parse import urlparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from utils import sql_utils
from utils import data_science_utils
from utils import scrape_utils
from utils.verbose import Verbose
from utils import models


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/gmail.modify']

SENDER_EMAIL = "newshorizonapp@gmail.com"


def getGmailService():
    global service
    try:
        service
    except (NameError, UnboundLocalError):
        service = __createGmailService()
    return service


def getModulePath():
    for root, subdirs, files in os.walk(os.path.expanduser("~")):
        for sd in subdirs:
            if sd == "MediAnalyserPOC":
                return root + os.sep + sd


def __createGmailService():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    modulePath = getModulePath()
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


def create_message(sender, to, subject, plain_text, html_text=None):
    # message = MIMEText(message_text)
    # message['to'] = to
    # message['from'] = sender
    # message['subject'] = subject

    message = MIMEMultipart('alternative')
    message["subject"] = subject
    message["from"] = sender
    message["to"] = to

    part1 = MIMEText(plain_text, "plain")
    message.attach(part1)
    if html_text is not None:
        part2 = MIMEText(html_text, "html")
        message.attach(part2)

    return {'raw': base64.urlsafe_b64encode(bytes(message.as_string(), "utf-8")).decode("utf-8")}


def create_draft(service, user_id, message_body):
    try:
        message = {'message': message_body}
        draft = service.users().drafts().create(userId=user_id, body=message).execute()

        print("Draft id: %s\nDraft message: %s" %
              (draft['id'], draft['message']))

        return draft
    except Exception as e:
        print('An error occurred: %s' % e)
        return None


def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(
            userId=user_id, body=message).execute()
        # print('Message Id: %s' % message['id'])
        return message
    except Exception as e:
        print('An error occurred: %s' % e)
        return None


def get_messages(service, user_id):
    try:
        return service.users().messages().list(userId=user_id).execute()
    except Exception as error:
        print('An error occurred: %s' % error)


def get_message(service, user_id, msg_id):
    try:
        return service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
    except Exception as error:
        print('An error occurred: %s' % error)


def get_mime_message(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id,
                                                 format='raw').execute()
        print('Message snippet: %s' % message['snippet'])
        print('Message keys: %s' % message.keys())
        msg_str = base64.urlsafe_b64decode(
            message['raw'].encode("utf-8")).decode("utf-8")
        mime_msg = email.message_from_string(msg_str)

        return mime_msg
    except Exception as error:
        print('An error occurred: %s' % error)


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
        print('An error occurred: %s' % error)


def getMessageContent(message):
    service = getGmailService()
    raw = get_message(service, 'me', message['id'])
    values = {}
    for entry in raw['payload']['headers']:
        values[entry['name'].lower()] = entry['value']

    values['snippet'] = raw['snippet']
    if 'parts' in raw['payload']:
        values['content'] = decode(raw['payload']['parts'][0]['body']['data'])
    if 'data' in raw['payload']['body']:
        values['content'] = decode(raw['payload']['body']['data'])
    values['id'] = message['id']
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


def getSourceFromUrl(url):
    stem = urlparse(url).netloc.split('.')[-2]
    return sql_utils.getDBSession().query(models.Source).filter(models.Source.website_url.contains(stem)).all()


def downloadArticle(article_search, verbose=Verbose.ERROR):
    sources = getSourceFromUrl(article_search.search_url)
    if len(sources) == 0:
        if verbose <= Verbose.ERROR:
            print('FAILURE: Source not found', article_search.article_search_uuid)
        sql_utils.updateSearchStatus(article_search.article_search_uuid, 'FAILURE: Source not found')
        return None
    else:
        if len(sources) == 1:
            source = sources[0]
        else:
            path_elements = urlparse(article_search.search_url).path.split('/')
            sources = getSourceFromUrl(article_search.search_url)

            print(path_elements)
            for element in path_elements:
                if element != '':
                    print(sources)
                    sources = [s for s in sources if element in s.website_url]
                    if len(sources) <= 1:
                        break
            if len(sources) == 0:  # eliminated too many sources, should not happen
                sql_utils.updateSearchStatus(article_search.article_search_uuid, 'FAILURE: Source domain not found')
                if verbose <= Verbose.ERROR:
                    print('FAILURE: Source domain not found', article_search.article_search_uuid)
                return None
            else:
                source = sources[0]
        # TODO add TF-IDF weights on key-words to select most frequent/relevant
        search_elements = article_search.search_url.split('/')[-1]
        if '.' in search_elements:
            search_elements = search_elements.split('.')[-2]
        search_elements = [x for x in map(data_science_utils.cleanText, search_elements.split('-'))
                           if not x.isdecimal() and x != '']
        search_keys = [list(x) for r in min(range(len(search_elements)), 2)
                       for x in itertools.combinations(search_elements, r + 1)]
        for key in search_keys:
            scrape_utils.pipelineNewsAPIArticle(
                " ".join(key),
                source.source_name.lower().replace(" ", "-"),
                fetchSource=True,
                verbose=verbose)
        articles = sql_utils.getArticle(article_search.search_url)
        if len(articles) == 0:
            # could not find article easily
            # TODO add scraping procedure
            return None
        else:
            return articles[0]


def answer_emails(request_emails, verbose=Verbose.ERROR):
    count = 0
    for request_i in request_emails:
        if verbose <= Verbose.INFO:
            print("Processing request", request_i['id'])
            print("Subject:", request_i['subject'])
            print("Content:", request_i['content'])
        requester_email = parse_email(request_i['from'])
        customer_uuid = sql_utils.getOrSetCustomerID(requester_email)
        search_url = getUrlFromText(request_i['subject'])
        if search_url is None:
            search_url = getUrlFromText(request_i['content'])
        if search_url is None:
            if verbose <= Verbose.ERROR:
                print("No URL found for message %s: %s\n %s\n" % (
                        request_i['id'], request_i['subject'], request_i['content']))
            success = sql_utils.insertEntry(models.ArticleSearch(
                gmail_request_uuid=request_i['id'],
                customer_uuid=customer_uuid,
                status='FAILURE: missing URL'
            ))
            continue
        success = sql_utils.insertEntry(models.ArticleSearch(
            gmail_request_uuid=request_i['id'],
            search_url=search_url,
            customer_uuid=customer_uuid,
        ))
        if not success:
            if verbose <= Verbose.WARNING:
                print("Could not insert search for entry %s" % request_i['id'])
            continue
        else:
            article_search = sql_utils.getSearch(request_i['id'])
            print(article_search)
            print(article_search.search_url)
            print(str(article_search.search_url))
            search_article = sql_utils.getArticle(article_search.search_url)
            if search_article is None:
                search_article = downloadArticle(article_search, verbose=verbose)
                if search_article is None:
                    if verbose <= Verbose.ERROR:
                        print('FAILURE: Article not found', article_search.article_search_uuid)
                    sql_utils.updateSearchStatus(article_search.article_search_uuid, 'FAILURE: Article not found')
                    continue
            search_attribute = 'title'
            result = data_science_utils.getSimilarArticlesFromText(
                search_article.title if search_attribute == 'title' else search_article.description,
                search_attribute, article_search.n_results)
            result['title_url'] = result[['title', 'article_url']].apply(__addUrlLinks, axis=1)
            html_text = result[['source_name', 'title_url']].to_html(escape=False, header=False, index=False)
            plain_text = result[['source_name', 'title']].to_string(header=False, index=False)
            message = create_message(
                SENDER_EMAIL,
                article_search.customer.customer_email,
                "Your News search is ready.",
                plain_text,
                html_text)
            sent_message = send_message(service, 'me', message)
            if sent_message is None:
                sql_utils.updateSearchStatus(article_search.article_search_uuid, 'FAILURE: Message not sent')
            else:
                count += sql_utils.updateSearchStatus(article_search.article_search_uuid, 'SUCCESS')
                sql_utils.updateSearch(article_search.article_search_uuid, sent_message['id'])
    return count


def __addUrlLinks(entry):
    return '<a href="' + entry['article_url'] + '">' + entry['title'] + '</a>'


def pipelineEmails(verbose=Verbose.ERROR):
    service = getGmailService()
    messages = get_messages(service, 'me')
    past_requests = sql_utils.getSearchMailIDs()
    invalid_emails = sql_utils.getInvalidEmailIDs()
    request_emails = []
    for m in messages['messages']:
        if m['id'] not in past_requests and m['id'] not in invalid_emails:
            values = getMessageContent(m)
            request_email_i = parse_email(values['from'])
            if 'no-reply' in values['from']:
                sql_utils.insertEntry(models.InvalidEmail(
                    gmail_request_uuid=m['id'],
                    customer_uuid=sql_utils.getOrSetCustomerID(request_email_i),
                    status='NO-REPLY sender'
                ))
            elif values['from'] == SENDER_EMAIL:
                sql_utils.insertEntry(models.InvalidEmail(
                    gmail_request_uuid=m['id'],
                    customer_uuid=sql_utils.getOrSetCustomerID(request_email_i),
                    status='SELF sender'
                ))
            else:
                request_emails.append(values)
    answer_emails(request_emails, verbose=verbose)
