# integration tests for FileHandler classes in File_Handler.py and Polar_File_Handler.py
# since they have the same API we'll combine them in 1 parameterized test class

import os
import pytest
from pandas import read_excel as pd_read_excel
from polars import read_excel as pl_read_excel
from ...File_Handler import FileHandler as fh
from ...Polar_File_Handler import FileHandler as pfh


# mocks of pd.read_excel and pl.read_excel
# essentially pretends input file only contains 5 rows

def mock_pd_read_excel(*args, **kwargs):
    # only want to target input file, exclude call to metadata
    if "Metadata" not in args[0]:
        df = pd_read_excel(args[0], index_col=kwargs['index_col'])
        # return only the first 5 rows from input file
        return df.head()
    else:
        return pd_read_excel(args[0], index_col=kwargs['index_col'])
        
def mock_pl_read_excel(*args, **kwargs):
    # in Polar_File_handler.py, input file is called with the 'source'-kw instead of as a non-kwarg, unlike the call for metadata file
    if len(args) == 0:
        f = pl_read_excel(source=kwargs['source'], columns=kwargs['columns'])
        # return only the first 5 rows from input file
        return f.head()
    else:
        return pl_read_excel(args[0], columns=kwargs['columns'])



@pytest.mark.parametrize('fh', [fh, pfh], ids=["File_Handler", "Polar_File_Handler"])
@pytest.mark.parametrize('tnum', [10, 1], ids=["10_threads", "1_thread"]) # (right now default amount of threads is 10)
class TestFileHandler:
    input = os.path.join("customer_data", "GRI_2017_2020.xlsx")
    output = os.path.join("tests", "integration", "Metadata2017_2020.xlsx")
    dest = os.path.join("tests", "integration", "files")


    # helper functions for controlling what files we have downloaded and not
    def remove_dls(self):
        if os.path.exists(self.dest):
            for file in os.listdir(self.dest):
                os.remove(os.path.join("tests", "integration", "files", file))
            os.rmdir(self.dest)

    def remove_metadata(self):
        if os.path.exists(self.output):
            os.remove(self.output)

    def clean_slate(self):
        self.remove_dls()
        self.remove_metadata()


    # FileHandler's 2 functions return nothing so testing will need to consist of checking side effects
    # this (vvv) is helper functions to do that (^^^)
    def crossreference_metadata(self):
        meta = pd_read_excel(self.output)
        self.amount_downloaded_matches(meta)
        self.metadata_is_correct(meta)

    def amount_downloaded_matches(self, meta):
        # get a dataframe only containing the rows of (allegedly) downloaded files
        meta_amount = meta.loc[meta['pdf_downloaded'] == "yes"]
        # count number of files present in destination folder
        dl_amount = len([name for name in os.listdir(self.dest) if os.path.isfile(os.path.join(self.dest, name))])
        assert meta_amount.shape[0] == dl_amount, f"Metadata file claims {meta_amount.shape[0]} files have been downloaded, and found {dl_amount} files in destination folder"

    def metadata_is_correct(self, meta):
        for row in meta.itertuples():
            if row.pdf_downloaded == "yes" and os.path.exists(os.path.join(self.dest, f"{row.BRnum}.pdf")):
                continue
            elif row.pdf_downloaded == "no" and not os.path.exists(os.path.join(self.dest, f"{row.BRnum}.pdf")):
                continue
            else:
                assert False, f"The downloaded pdf's ({row.BRnum}) existence did not correspond to its status ({row.pdf_downloaded}) in metadata file"


    # TODO mock out the excel input?

    ### start_download() tests
    def test_start_download_clean(self, fh, tnum):
        """
        Test start_download() from a clean slate (no previously downloaded files, no metadata file).
        Checking that files logged as downloaded in metadata file are actually present in downloads folder
        """
        self.clean_slate()

        fh = fh(tnum)
        fh.start_download(self.input, self.output, self.dest)

        # check side effects
        self.crossreference_metadata()

    def test_start_download_unclean(self, fh, tnum):
        """
        Test start_download() from an unclean slate (previously downloaded files, metadata file).
        Checking that files logged as downloaded in metadata file are actually present in downloads folder
        """
        self.clean_slate()

        fh = fh(tnum)
        fh.start_download(self.input, self.output, self.dest)
        fh.start_download(self.input, self.output, self.dest)
        
        # check side effects
        self.crossreference_metadata()

    def test_start_download_no_meta(self, fh, tnum):
        """
        Run start_download() on a clean slate, remove the metadata file but not the downloaded files, and run start_download() again
        """
        self.clean_slate()

        fh = fh(tnum)
        fh.start_download(self.input, self.output, self.dest)
        self.remove_metadata()
        fh.start_download(self.input, self.output, self.dest)

        # check side effects
        self.crossreference_metadata()

    def test_start_download_no_dls(self, fh, tnum):
        """
        Run start_download() on a clean slate, remove the downloaded files but not the metadata file, and run start_download() again
        """
        self.clean_slate()

        fh = fh(tnum)
        fh.start_download(self.input, self.output, self.dest)
        self.remove_dls()
        fh.start_download(self.input, self.output, self.dest)

        # check side effects
        self.crossreference_metadata()


    ### test some weird input

    # input less than 20 rows - use mocked pd.read_excel and polars.read_excel
    def test_start_download_small_input(self, fh, tnum, monkeypatch):
        self.clean_slate()

        monkeypatch.setattr('File_Handler.pd.read_excel', mock_pd_read_excel)
        monkeypatch.setattr('Polar_File_Handler.pl.read_excel', mock_pl_read_excel)

        fh = fh(tnum)
        fh.start_download(self.input, self.output, self.dest)

        # check side effects
        self.crossreference_metadata()


    # bad input
    # empty strings on input, output and dest (parameterized)
    @pytest.mark.parametrize('p_input', ["", input], ids=["bad_input", "normal_input"])
    @pytest.mark.parametrize('p_output', ["", output], ids=["bad_output", "normal_output"])
    @pytest.mark.parametrize('p_dest', ["", dest], ids=["bad_dest", "normal_dest"])
    def test_start_download_empty_input(self, fh, tnum, p_input, p_output, p_dest):
        self.clean_slate()

        fh = fh(tnum)
        fh.start_download(p_input, p_output, p_dest)
        # we are testing for errors during execution, so dont check side effects


    # download_thread() - ahhh...