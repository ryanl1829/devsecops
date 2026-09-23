from unittest.mock import patch

import web_service

def test_parse_count_zero():
    assert web_service._parse_count('0') == 0

def test_parse_count_positive():
    assert web_service._parse_count('123') == 123

def test_parse_count_empty():
    assert web_service._parse_count('') == 0

def test_parse_count_invalid():
    assert web_service._parse_count('hello') == 0

@patch('web_service.increment_visits_s3')
@patch('web_service.increment_visits_local')
def test_increment_visits_local(mock_increment_local, mock_increment_s3):
    web_service.increment_visits()
    mock_increment_local.assert_called()
    mock_increment_s3.assert_not_called()

@patch('web_service.increment_visits_s3')
@patch('web_service.increment_visits_local')
def test_increment_visits_s3(mock_increment_local, mock_increment_s3):
    with patch('web_service.COUNTER_FILE', new='s3://counter/count.txt'):
        web_service.increment_visits()
    mock_increment_local.assert_not_called()
    mock_increment_s3.assert_called()
