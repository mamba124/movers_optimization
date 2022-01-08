# import the required libraries
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
from bs4 import BeautifulSoup
from base64 import urlsafe_b64decode

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 
          'https://www.googleapis.com/auth/gmail.modify']
  
def get_unread_mails():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
  
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
  
    service = build('gmail', 'v1', credentials=creds)
  
    result = service.users().messages().list(userId='me', q="is:unread").execute()
  
    # We can also pass maxResults to get any number of emails. Like this:
    # result = service.users().messages().list(maxResults=200, userId='me').execute()
    messages = result.get('messages')
    scraped_links = []
    # messages is a list of dictionaries where each dictionary contains a message id.
    if messages:
        # iterate through all the messages
        for msg in messages:
            # Get the message from its id
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()
           # raw_txt = service.users().messages().get(userId='me', id=msg['id'], format="raw").execute()
            # Use try-except to avoid any Errors
            try:
                # Get value of 'payload' from dictionary 'txt'
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
    
            except:
                pass
            
        return scraped_links
