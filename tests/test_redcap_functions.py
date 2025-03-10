# tests/test_redcap_functions.py
import pytest
import requests_mock
import pandas as pd
from redcap_functions import fetch_redcap_records, write_to_redcap


# tests/test_redcap_functions.py
import pytest
import requests_mock
import pandas as pd
from redcap_functions import fetch_redcap_records


@pytest.fixture
def redcap_response_no_repeat():
    return [
        {"cfsubjid": "1", "field1": "value1"},
        {"cfsubjid": "2", "field1": "value2"},
    ]


@pytest.fixture
def redcap_response_with_repeat():
    return [
        {
            "cfsubjid": "1",
            "field1": "value1",
            "redcap_repeat_instrument": "",
            "redcap_repeat_instance": "",
        },
        {
            "cfsubjid": "1",
            "field1": "value3",
            "redcap_repeat_instrument": "instrument1",
            "redcap_repeat_instance": "1",
        },
        {
            "cfsubjid": "2",
            "field1": "value2",
            "redcap_repeat_instrument": "",
            "redcap_repeat_instance": "",
        },
    ]


@pytest.fixture
def redcap_response_two_fields_no_repeat():
    return [
        {"cfsubjid": "1", "field1": "value1", "field2": "valueA"},
        {"cfsubjid": "2", "field1": "value2", "field2": "valueB"},
    ]


@pytest.fixture
def redcap_response_two_fields_with_repeat():
    return [
        {
            "cfsubjid": "1",
            "field1": "value1",
            "field2": "valueA",
            "redcap_repeat_instrument": "",
            "redcap_repeat_instance": "",
        },
        {
            "cfsubjid": "1",
            "field1": "value3",
            "field2": "valueC",
            "redcap_repeat_instrument": "instrument1",
            "redcap_repeat_instance": "1",
        },
        {
            "cfsubjid": "2",
            "field1": "value2",
            "field2": "valueB",
            "redcap_repeat_instrument": "",
            "redcap_repeat_instance": "",
        },
    ]


@pytest.fixture
def redcap_write_response():
    return {"count": 2}


def test_fetch_redcap_records_one_field_no_repeat(redcap_response_no_repeat):
    api_url = "https://redcap.example.com/api/"
    token = "fake_token"
    fields = ["cfsubjid", "field1"]

    with requests_mock.Mocker() as m:
        m.post(api_url, json=redcap_response_no_repeat)
        df = fetch_redcap_records(api_url, token, fields)

        assert df.equals(pd.DataFrame(redcap_response_no_repeat))


def test_fetch_redcap_records_one_field_with_repeat(redcap_response_with_repeat):
    api_url = "https://redcap.example.com/api/"
    token = "fake_token"
    fields = ["cfsubjid", "field1"]

    with requests_mock.Mocker() as m:
        m.post(api_url, json=redcap_response_with_repeat)
        df = fetch_redcap_records(api_url, token, fields)

        assert df.equals(pd.DataFrame(redcap_response_with_repeat))


def test_fetch_redcap_records_two_fields_no_repeat(
    redcap_response_two_fields_no_repeat,
):
    api_url = "https://redcap.example.com/api/"
    token = "fake_token"
    fields = ["cfsubjid", "field1", "field2"]

    with requests_mock.Mocker() as m:
        m.post(api_url, json=redcap_response_two_fields_no_repeat)
        df = fetch_redcap_records(api_url, token, fields)

        assert df.equals(pd.DataFrame(redcap_response_two_fields_no_repeat))


def test_fetch_redcap_records_two_fields_with_repeat(
    redcap_response_two_fields_with_repeat,
):
    api_url = "https://redcap.example.com/api/"
    token = "fake_token"
    fields = ["cfsubjid", "field1", "field2"]

    with requests_mock.Mocker() as m:
        m.post(api_url, json=redcap_response_two_fields_with_repeat)
        df = fetch_redcap_records(api_url, token, fields)

        assert df.equals(pd.DataFrame(redcap_response_two_fields_with_repeat))


def test_write_to_redcap(redcap_write_response):
    api_url = "https://redcap.example.com/api/"
    token = "fake_token"
    df = pd.DataFrame(
        [
            {"record_id": "1", "field1": "value1", "field2": "value2"},
            {"record_id": "2", "field1": "value3", "field2": "value4"},
        ]
    )

    with requests_mock.Mocker() as m:
        m.post(api_url, json=redcap_write_response)
        success, count = write_to_redcap(api_url, token, df)

        assert success is True
        assert count == redcap_write_response["count"]
