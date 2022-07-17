# import the required libraries
from googleapiclient.discovery import build
from google.oauth2 import service_account
#from google_auth_oauthlib.flow import InstalledAppFlow
#from google.auth.transport.requests import Request
#from google.auth.exceptions import RefreshError
import pickle
import os.path
from bs4 import BeautifulSoup
from base64 import urlsafe_b64decode
import time
import os
from datetime import datetime
import logging
import socket
from email.mime.text import MIMEText
import base64


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 
          'https://www.googleapis.com/auth/gmail.modify',
          'https://www.googleapis.com/auth/service.management',
          'https://www.googleapis.com/auth/cloud-platform']


def create_message(sender="helper@tomatoland.info", to="helper@tomatoland.info", subject="Acess token expires soon..", message_text=''):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  message['value'] = 'robot'
  return {'raw': base64.urlsafe_b64encode(message.as_string().encode("utf-8")).decode()}


def send_message(service, mail, user="helper@tomatoland.info"):
    try:
        message = (service.users().messages().send(userId=user, body=mail)
                   .execute())
    except Exception as ex:
        print (ex)        

    

def build_service():
    credentials = service_account.Credentials.from_service_account_file(
            'secret_files/service_acc.json', scopes=SCOPES, subject="helper@tomatoland.info")
    service = build('gmail', 'v1', credentials=credentials)
    return service


def get_unread_mails():
    service = build_service()
    num_retries = 0
    response_valid = False
    while num_retries < 10: 
        try: 
            unread_mail_list_request = service.users().messages().list(userId='me', q="is:unread").execute()
            response_valid = True
            break
        except socket.timeout:
            num_retries = num_retries + 1 
            time.sleep(0.05*num_retries)
    if response_valid:
        messages = unread_mail_list_request.get('messages')
        scraped_links = parse_messages(messages, service)
    else:
        scraped_links = []
    return scraped_links


def get_encoded_message(service, msg):
    try:
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        return txt
    except Exception as ex:
        logging.error(ex)
        print(ex)


def parse_messages(messages, service):
    scraped_links = []
    # messages is a list of dictionaries where each dictionary contains a message id.
    if messages:
        for msg in messages:
            # Get the message from its id
            txt = get_encoded_message(service, msg)
            # Get value of 'payload' from dictionary 'txt'

            if txt:
                if txt.get("snippet") and "Attention, " in txt.get("snippet"):
                    continue
                payload = txt['payload']
                headers = payload['headers']
                # Look for Subject and Sender Email in the headers
                for d in headers:
                    if d['name'] == 'Subject':
                        subject = d['value']

                if "job for" in subject:
                    parts = payload.get('parts')
                    for part in parts:
                        mtype = part.get("mimeType")
                        if mtype == "text/html":
                            
                            data = part['body']['data']
                            decoded_data = urlsafe_b64decode(data)
    
                            soup = BeautifulSoup(decoded_data , "html.parser")
                            link = soup.findAll("a")[-4].get("href") #-4
                            service.users().messages().modify(userId='me',
                                                              id=msg['id'],
                                                              body={'removeLabelIds': ['UNREAD']}).execute()
                            scraped_links.append(link)
    return scraped_links

