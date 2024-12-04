# unit tests for downloader.py with pytest

import os
import pytest
from ...Downloader import Downloader


# set up some mocks for requests.get()
import requests
class MockResponsePDF:
    def __init__(self):
        self.headers = {"content-type": "application/pdf"}
        self.content = b"im pdf content"

class MockResponseNotPDF:
    def __init__(self):
        self.headers = {"content-type": "im something else"}
        self.content = b"im not pdf content"

class MockResponseFailed:
    def __init__(self):
        self.headers = None
        self.content = None

def mock_get(*args, **kwargs):
    """
    mocked version of requests.get().
    if first non-kw argument (corresponds to url for requests.get()) is \"fail\" or None, then mimics a failed request.
    if first non-kw argument is \"not pdf\" then return a non-pdf response.
    """
    if args[0] == "fail" or args[0] == None:
        return MockResponseFailed()
    elif args[0] == "not pdf":
        return MockResponseNotPDF()
    else:
        return MockResponsePDF()


class TestDownloader:
    url = "https://fakeurl"
    url_not_pdf = "not pdf"
    url_fail = "fail"
    output = "./tests/unit/test.pdf"
    bad_output = "this_folder_doesnt_exist/test.pdf"

    @pytest.fixture(autouse=True)
    def tearDown(self):
        if os.path.exists(self.output):
            os.remove(self.output)


    # test first download link
    def test_download(self, monkeypatch):
        monkeypatch.setattr(requests, "get", mock_get)
        d = Downloader()
        did_it_work = d.download(self.url, self.output)
        assert did_it_work == True

    def test_download_bad(self, monkeypatch):
        monkeypatch.setattr(requests, "get", mock_get)
        d = Downloader()
        did_it_work = d.download(self.url_fail, self.output)
        assert did_it_work == False

    def test_download_not_pdf(self, monkeypatch):
        monkeypatch.setattr(requests, "get", mock_get)
        d = Downloader()
        with pytest.raises(Exception, match="Not pdf type") as e_info:
            did_it_work = d.download(self.url_not_pdf, self.output)
            raise Exception("Not pdf type")
        assert e_info.type is Exception
        assert did_it_work == False


    # test alt download link
    def test_download_alt(self, monkeypatch):
        monkeypatch.setattr(requests, "get", mock_get)
        d = Downloader()
        did_it_work = d.download(self.url_fail, self.output, self.url)
        assert did_it_work == True

    def test_download_alt_bad(self, monkeypatch):
        monkeypatch.setattr(requests, "get", mock_get)
        d = Downloader()
        did_it_work = d.download(self.url_fail, self.output, self.url_fail)
        assert did_it_work == False

    def test_download_alt_not_pdf(self, monkeypatch):
        monkeypatch.setattr(requests, "get", mock_get)
        d = Downloader()
        with pytest.raises(Exception, match="Not pdf type") as e_info:
            did_it_work = d.download(self.url_fail, self.output, self.url_not_pdf)
            raise Exception("Not pdf type")
        assert e_info.type is Exception
        assert did_it_work == False

    
    # test destination
    def test_download_bad_destination(self, monkeypatch):
        monkeypatch.setattr(requests, "get", mock_get)
        d = Downloader()
        did_it_work = d.download(self.url, self.bad_output)
        assert did_it_work == False


    # test weird input, no need for mock bcus no chance of download
    def test_download_None_input(self):
        d = Downloader()
        did_it_work = d.download(None, None)
        assert did_it_work == False

    def test_download_empty_str(self):
        d = Downloader()
        did_it_work = d.download("", "")
        assert did_it_work == False
