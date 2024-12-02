# unit tests for downloader.py with pytest

import os
import pytest
from ...Downloader import Downloader

class TestDownloader:
    url = "http://cdn12.a1.net/m/resources/media/pdf/A1-Umwelterkl-rung-2016-2017.pdf"
    bad_url = "not a url"
    weird_url = "https://en.wikipedia.org/wiki/File:Bucephala-albeola-010.jpg"
    output = "./tests/unit/test.pdf"
    bad_output = "this_folder_doesnt_exist/test.pdf"
    alt = "http://www.acomo.nl/wp-content/uploads/2018/04/Acomo-Annual-Report-2017-interactive.pdf"

    @pytest.fixture(autouse=True)
    def tearDown(self):
        if os.path.exists(self.output):
            os.remove(self.output)

    def test_download(self):
        d = Downloader()
        did_it_work = d.download(self.url, self.output)
        assert did_it_work == True

    def test_download_bad(self):
        d = Downloader()
        did_it_work = d.download(self.bad_url, self.output)
        assert did_it_work == False

    def test_download_alt(self):
        """download from alt url when first url doesnt suceed"""
        d = Downloader()
        did_it_work = d.download(self.bad_url, self.output, self.alt)
        assert did_it_work == True

    def test_download_bad_alt(self):
        """test if, upon first url succeeding, bad input on alt url won't matter"""
        d = Downloader()
        did_it_work = d.download(self.url, self.output, self.bad_url)
        assert did_it_work == True

    def test_download_None_input(self):
        d = Downloader()
        did_it_work = d.download(None, None)
        assert did_it_work == False

    def test_download_empty_str(self):
        d = Downloader()
        did_it_work = d.download("", "")
        assert did_it_work == False

    def test_download_not_pdf(self):
        d = Downloader()
        did_it_work = d.download(self.weird_url, self.output)
        assert did_it_work == False

    def test_download_bad_destination(self):
        d = Downloader()
        did_it_work = d.download(self.url, self.bad_output)
        assert did_it_work == False