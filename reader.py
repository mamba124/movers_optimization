# import the required libraries
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
from bs4 import BeautifulSoup
from base64 import urlsafe_b64decode
import time
import os
from datetime import datetime
import logging

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 
          'https://www.googleapis.com/auth/gmail.modify']


def token_time_validation(default_delta=7):
    today = datetime.today()
    created_at = datetime.strptime(time.ctime(os.path.getctime("token.pickle")), "%a %b %d %H:%M:%S %Y")
    timedelta = today - created_at
    if timedelta.days >= default_delta:
        os.remove("tocken.pickle")


def token_check():
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    return creds


def refresh_token(creds):
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
    return creds


def get_unread_mails():
    token_time_validation()
    creds = token_check()
    if not creds or not creds.valid:   
        creds = refresh_token(creds)
    service = build('gmail', 'v1', credentials=creds)
    unread_mail_list_request = service.users().messages().list(userId='me', q="is:unread").execute()
    messages = unread_mail_list_request.get('messages')
    scraped_links = parse_messages(messages, service)
    return scraped_links


def get_encoded_message(service, msg):
    try:
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        return txt
    except Exception as ex:
        logging.ERROR(ex)


def parse_messages(messages, service):
    scraped_links = []
    # messages is a list of dictionaries where each dictionary contains a message id.
    if messages:
        for msg in messages:
            # Get the message from its id
            txt = get_encoded_message(service, msg)
            # Get value of 'payload' from dictionary 'txt'
            if txt:
                payload = txt['payload']
                headers = payload['headers']
                # Look for Subject and Sender Email in the headers
                for d in headers:
                    if d['name'] == 'Subject':
                        subject = d['value']
            #        if d['name'] == 'From':
            #            sender = d['value']
                if "job for" in subject:
                    parts = payload.get('parts')
                    for part in parts:
                        mtype = part.get("mimeType")
                        if mtype == "text/html":
                            
                            data = part['body']['data']
                            decoded_data = urlsafe_b64decode(data)
    
                            soup = BeautifulSoup(decoded_data , "lxml")
                            link = soup.findAll("a")[-4].get("href") #-4
                            service.users().messages().modify(userId='me',
                                                              id=msg['id'],
                                                              body={'removeLabelIds': ['UNREAD']}).execute()
                            scraped_links.append(link)
    return scraped_links
        