# import the required libraries
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
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
          'https://www.googleapis.com/auth/gmail.modify']


def create_message(sender="californiaexperessmail@gmail.com", to="musechika@gmail.com", subject="Acess token expires soon..", message_text=''):
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


def send_message(service, mail, user="trekmovers.alex@gmail.com"):
    try:
        message = (service.users().messages().send(userId=user, body=mail)
                   .execute())
    except Exception as ex:
        print (ex)        

        
def validate_token_time(service, token_path="secret_files/token.pickle"):
    today = datetime.today()
    created_at = datetime.strptime(time.ctime(os.path.getctime(token_path)), "%a %b %d %H:%M:%S %Y")
    timedelta = today - created_at
    if timedelta.seconds >= 6 * 24 * 60 * 60:
        user="californiaexperessmail@gmail.com"
        timerange = 7 * 24 * 60 * 60 - timedelta.seconds
        message_text = f'Attention, expiration token soon will be refreshed!\n You will be asked to proceed manually. Token will expire in less than {timerange/3600} hours.\nIn case you want to refresh it now, delete Documents/movers_optimization/secret_files/token.pickle and wait for the pop-up window.'
        message = create_message(to=user, message_text=message_text)
        send_message(service, mail=message, user=user)


def token_check(path='secret_files/token.pickle'):
    creds = None
    if os.path.exists(path):
        with open(path, 'rb') as token:
            creds = pickle.load(token)
    return creds


def refresh_token(creds, credentials_path="secret_files/credentials.json", token_path="secret_files/token.pickle"):
    refresh_counter = 0
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except RefreshError:
            os.remove(token_path)
            refresh_counter += 1
    if refresh_counter or not creds:
        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
        # Indicate where the API server will redirect the user after the user completes
        # the authorization flow. The redirect URI is required. The value must exactly
        # match one of the authorized redirect URIs for the OAuth 2.0 client, which you
        # configured in the API Console. If this value doesn't match an authorized URI,
        # you will get a 'redirect_uri_mismatch' error.
        flow.redirect_uri = 'https://www.example.com/oauth2callback'
        
        # Generate URL for request to Google's OAuth 2.0 server.
        # Use kwargs to set optional request parameters.
        authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type='offline',
            login_hint = "californiaexperessmail@gmail.com",
            approval_prompt="force",
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes='true')
        creds = flow.run_local_server(port=0)         
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    return creds


def build_service():
    creds = token_check()
    if not creds or not creds.valid:  
        creds = refresh_token(creds)
    service = build('gmail', 'v1', credentials=creds)
    return service


def get_unread_mails():
    service = build_service()
    validate_token_time(service)
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
            if txt.get("snippet") and "expiration token" in txt.get("snippet"):
                continue
            if txt:
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
    
                            soup = BeautifulSoup(decoded_data , "lxml")
                            link = soup.findAll("a")[-4].get("href") #-4
                            service.users().messages().modify(userId='me',
                                                              id=msg['id'],
                                                              body={'removeLabelIds': ['UNREAD']}).execute()
                            scraped_links.append(link)
    return scraped_links

