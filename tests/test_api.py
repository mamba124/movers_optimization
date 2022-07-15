from src import gmail_processor
import json
from unittest.mock import patch, MagicMock, Mock


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
    