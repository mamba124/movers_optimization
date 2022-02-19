from src import gmail_processor
import json
import os
import pickle
from unittest.mock import patch, MagicMock, Mock


class MockedGService:
    def __init__(self):
        pass
    
    def run_local_service(self, port):
        return {"key": "value"}
    
    def users():
        return Creds()
    
    def modify(*args):
        pass


class Creds:
    def __init__(self):
        self.expired = True
        self.refresh_token = True
    
    def refresh(self, request_object):
        self.expired = False
    
    def from_client_secrets_file(self, path):
        return MockedGService()
    
    def messages():
        return MockedGService()

    
def test_tokentime_val():
    token_path = "tests/test_files/dummy_token"
    
    service = Mock()
    gmail_processor.validate_token_time(service, token_path)
    assert "dummy_token" not in os.listdir("tests/test_files/")

    with open(token_path, "w") as f:
        f.write("")

    gmail_processor.token_time_validation(140, token_path)
    assert "dummy_token" in os.listdir("tests/test_files/")


def test_token_check():
    path = "tests/test_files/dummy_pickle.pickle"
    with open(path, "wb") as f:
        pickle.dump({"key": "value"}, f)
    creds = gmail_processor.token_check(path)
    assert creds == {"key": "value"}


@patch("google_auth_oauthlib.flow.InstalledAppFlow", return_value=Creds)
def test_refresh_token(mocked_flow):
    input_creds = Creds()
    creds = gmail_processor.refresh_token(input_creds, "tests/test_files/credentials.json", "tests/test_files/dummy_pickle.pickle")
    assert creds.expired == False


mocked_google_service = MagicMock()
mocked_google_service.users.return_value.messages.return_value.modify.return_value = Mock()
txt_template = json.load(open("tests/test_files/api_response.json"))
ivn_txt_template = json.load(open("tests/test_files/inv_text.json"))
template = None

@patch("src.gmail_processor.get_encoded_message", return_value=txt_template)
def test_parse_message_valid(mocked_enc):
    links = gmail_processor.parse_messages([{'id': '17e5b4abce9f0fb4', 'threadId': '17e5b4abce9f0fb4'}], mocked_google_service)
    assert links == ['https://biz.yelp.com/messaging/gGbHoiu9Q9WUQcNbWf1qUg/opportunity/JpQd_Dkbv9Qlz_RQtqHeew?ytl_=68e8cd998612572719c0a2f4e13ed03f&utm_medium=email&utm_source=nearby_jobs_new_job_email&utm_campaign=Jan-14-2022']


@patch("src.gmail_processor.get_encoded_message", return_value=ivn_txt_template)
def test_parse_message_invalid(mocked_enc):
    links = gmail_processor.parse_messages([{'id': '17e5b4abce9f0fb4', 'threadId': '17e5b4abce9f0fb4'}], mocked_google_service)
    assert links == []


@patch("src.gmail_processor.get_encoded_message", return_value=template)
def test_parse_message_none(mocked_enc):
    links = gmail_processor.parse_messages([{'id': '17e5b4abce9f0fb4', 'threadId': '17e5b4abce9f0fb4'}], mocked_google_service)
    assert links == []
    